"""
hackathon/agents.py — OpenAI Agent Orchestration for NertzMetalEngine.

Agentes autónomos que usan GPT-5 + function calling + Context Bridge.
Entrega para OpenAI Build Week: multi-agent trading strategy.
"""

from __future__ import annotations

import json
import os
import asyncio
from typing import Any, Optional, Dict, List
from dataclasses import dataclass

from openai import AsyncOpenAI, OpenAI

# Importa el cliente local (fallback a Codex si no hay API key)
from gpt_integration import GPTClient


@dataclass
class AgentDecision:
    """Decisión de un agente."""
    action: str  # "BUY" | "SELL" | "HOLD"
    confidence: float  # 0.0 - 1.0
    reasoning: str
    symbol: str
    price_target: Optional[float] = None
    stop_loss: Optional[float] = None


class NertzAgent:
    """
    Agente OpenAI para análisis de mercado y decisiones de trading.

    Flujo:
    1. Recibe métricas + contexto del bridge
    2. Llama a GPT-5 con tools (read-only de Bybit, context bridge)
    3. Devuelve decisión estructurada (BUY/SELL/HOLD + razonamiento)
    """

    def __init__(self, symbol: str = "BTCUSDT", use_async: bool = False):
        self.symbol = symbol
        self.use_async = use_async
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        # Para Opción B (Codex/ChatGPT): no fuerces modelo → usa default de la cuenta
        backend = os.getenv("GPT_BACKEND", "").lower()
        if backend in ("chatgpt", "codex", "web", "session"):
            # Opción B: no especificar modelo, Codex usa el default de la cuenta
            self.model = os.getenv("OPENAI_MODEL", "")
        else:
            # Opción A (API) o auto: usa gpt-5 como default
            self.model = os.getenv("OPENAI_MODEL", "gpt-5")

        # Si no hay API key, usa fallback GPTClient (Codex)
        self.gpt_client = GPTClient(model=self.model if self.model else None)

        if self.use_async and self.api_key:
            self.async_client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.async_client = None

        self.sync_client = OpenAI(api_key=self.api_key) if self.api_key else None

    @staticmethod
    def _trading_tools() -> List[Dict[str, Any]]:
        """Define herramientas (tools) disponibles para el agente."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_context_metrics",
                    "description": (
                        "Obtiene métricas del Context Bridge: "
                        "combined signal, ILD, EGM, PIO, estado del bot"
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {
                                "type": "string",
                                "description": "Símbolo de trading (e.g., BTCUSDT)"
                            }
                        },
                        "required": ["symbol"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_market_context",
                    "description": (
                        "Obtiene contexto del bridge: "
                        "últimas decisiones, PnL, win_rate"
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "analyze_price_action",
                    "description": (
                        "Analiza el price action reciente: "
                        "velas, RSI, tendencia"
                    ),
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "symbol": {"type": "string"},
                            "timeframe": {
                                "type": "string",
                                "enum": ["1m", "5m", "15m", "1h", "4h"],
                                "description": "Marco temporal"
                            }
                        },
                        "required": ["symbol"]
                    }
                }
            }
        ]

    def _format_prompt(self, metrics: Dict[str, Any]) -> str:
        """Construye el prompt del sistema y usuario."""
        system = f"""
Eres un trader cuantitativo especializado en crypto. Tu rol es analizar métricas de trading 
en tiempo real y proporcionar decisiones estructuradas (BUY/SELL/HOLD) con razonamiento.

Símbolo: {self.symbol}

Instrucciones:
1. Analiza las métricas proporcionadas (combined signal, ILD, EGM, PIO, precio actual).
2. Responde en español.
3. Proporciona:
   - Decisión clara: BUY | SELL | HOLD
   - Confianza (0-100)
   - Razonamiento breve
   - Precio target (si aplica)
   - Stop loss (si aplica)
4. Sé conservador: preferir HOLD ante dudas.
5. Usa datos de Context Bridge para validar (bridge digest, últimas decisiones).
"""

        user = f"""
Analiza estas métricas para {self.symbol}:

{json.dumps(metrics, indent=2, default=str)}

Proporciona tu decisión en formato JSON:
{{
  "action": "BUY|SELL|HOLD",
  "confidence": 0.0-1.0,
  "reasoning": "Tu análisis breve",
  "price_target": null or número,
  "stop_loss": null o número
}}
"""
        return system, user

    def analyze(self, metrics: Dict[str, Any]) -> AgentDecision:
        """Análisis síncrono usando GPT-5 (sync OpenAI client o fallback GPTClient)."""
        system, user = self._format_prompt(metrics)

        if self.sync_client:
            # Usa OpenAI API con function calling
            try:
                response = self.sync_client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user}
                    ],
                    tools=self._trading_tools(),
                    tool_choice="auto",
                    temperature=0.3  # Conservative
                )

                # Parsea la respuesta
                content = response.choices[0].message.content or ""
                try:
                    decision_data = json.loads(content)
                except json.JSONDecodeError:
                    # Intenta extraer JSON del texto
                    import re
                    match = re.search(r'\{.*\}', content, re.DOTALL)
                    decision_data = json.loads(match.group()) if match else {}

                return AgentDecision(
                    action=decision_data.get("action", "HOLD"),
                    confidence=float(decision_data.get("confidence", 0.5)),
                    reasoning=decision_data.get("reasoning", content[:200]),
                    symbol=self.symbol,
                    price_target=decision_data.get("price_target"),
                    stop_loss=decision_data.get("stop_loss")
                )
            except Exception as e:
                # Fallback a GPTClient (Codex)
                print(f"API error: {e}, usando fallback GPTClient")
                return self._analyze_fallback(system, user)
        else:
            # Usa fallback GPTClient (Codex / web session)
            return self._analyze_fallback(system, user)

    def _analyze_fallback(self, system: str, user: str) -> AgentDecision:
        """Fallback sin function calling (usa Codex o chat simple)."""
        prompt = f"{system}\n\n{user}"
        reply = self.gpt_client.chat(prompt)

        try:
            import re
            match = re.search(r'\{.*\}', reply, re.DOTALL)
            decision_data = json.loads(match.group()) if match else {}
        except (json.JSONDecodeError, AttributeError):
            decision_data = {}

        return AgentDecision(
            action=decision_data.get("action", "HOLD"),
            confidence=float(decision_data.get("confidence", 0.5)),
            reasoning=decision_data.get("reasoning", reply[:200]),
            symbol=self.symbol,
            price_target=decision_data.get("price_target"),
            stop_loss=decision_data.get("stop_loss")
        )

    async def analyze_async(self, metrics: Dict[str, Any]) -> AgentDecision:
        """Análisis asíncrono (requiere OPENAI_API_KEY)."""
        if not self.async_client:
            # Fallback a síncrono
            return self.analyze(metrics)

        system, user = self._format_prompt(metrics)

        try:
            response = await self.async_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                tools=self._trading_tools(),
                tool_choice="auto",
                temperature=0.3
            )

            content = response.choices[0].message.content or ""
            try:
                decision_data = json.loads(content)
            except json.JSONDecodeError:
                import re
                match = re.search(r'\{.*\}', content, re.DOTALL)
                decision_data = json.loads(match.group()) if match else {}

            return AgentDecision(
                action=decision_data.get("action", "HOLD"),
                confidence=float(decision_data.get("confidence", 0.5)),
                reasoning=decision_data.get("reasoning", content[:200]),
                symbol=self.symbol,
                price_target=decision_data.get("price_target"),
                stop_loss=decision_data.get("stop_loss")
            )
        except Exception as e:
            print(f"Async error: {e}")
            return self.analyze(metrics)


class AgentOrchestrator:
    """
    Orquestador de múltiples agentes (consensus-based).

    Ejemplo: ejecuta 3 agentes en paralelo, combina resultados.
    """

    def __init__(self, symbols: List[str] | None = None):
        self.symbols = symbols or ["BTCUSDT", "ETHUSDT"]
        self.agents = {sym: NertzAgent(symbol=sym) for sym in self.symbols}

    def run_consensus(self, metrics_by_symbol: Dict[str, Dict[str, Any]]) -> Dict[str, AgentDecision]:
        """Ejecuta agentes en paralelo (sync), devuelve decisiones por símbolo."""
        results = {}
        for symbol, metrics in metrics_by_symbol.items():
            if symbol in self.agents:
                results[symbol] = self.agents[symbol].analyze(metrics)
        return results

    async def run_consensus_async(
        self, metrics_by_symbol: Dict[str, Dict[str, Any]]
    ) -> Dict[str, AgentDecision]:
        """Ejecuta agentes en paralelo (async)."""
        tasks = {
            symbol: self.agents[symbol].analyze_async(metrics)
            for symbol, metrics in metrics_by_symbol.items()
            if symbol in self.agents
        }
        results = await asyncio.gather(*tasks.values())
        return dict(zip(tasks.keys(), results))


# Test / ejemplo de uso
if __name__ == "__main__":
    import sys

    # Test: crear agente para BTCUSDT
    agent = NertzAgent(symbol="BTCUSDT")

    # Métricas de ejemplo
    test_metrics = {
        "combined": 7.2,
        "pio": 1.1,
        "ild": 2.3,
        "egm": 0.8,
        "price": 98234.50,
        "timestamp": "2026-07-14T01:30:00Z"
    }

    print("🤖 NertzAgent analysis:")
    decision = agent.analyze(test_metrics)
    print(f"  Action: {decision.action} (confidence: {decision.confidence:.0%})")
    print(f"  Reasoning: {decision.reasoning}")
    if decision.price_target:
        print(f"  Target: ${decision.price_target}")
    if decision.stop_loss:
        print(f"  SL: ${decision.stop_loss}")

