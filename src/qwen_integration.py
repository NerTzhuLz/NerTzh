"""
qwen_integration.py - Módulo de integración Qwen CLI en el proyecto
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

class QwenClient:
    """Cliente para usar Qwen CLI desde Python"""
    
    def __init__(self, model: str = "qwen3.6-plus"):
        self.model = model
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        self.qwen_path = self._find_qwen()
        
        if not self.qwen_path:
            raise RuntimeError("Qwen CLI no encontrado. Instala: npm install -g qwen-cli")
        
        if not self.api_key:
            raise RuntimeError("DASHSCOPE_API_KEY no configurada")
    
    @staticmethod
    def _find_qwen() -> Optional[str]:
        """Buscar ubicación de qwen CLI"""
        import shutil
        return shutil.which("qwen")
    
    def analyze(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Analizar con Qwen"""
        return self.chat(prompt, context)
    
    def chat(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Chat con Qwen"""
        try:
            cmd = [self.qwen_path, "chat", "-m", self.model]
            
            # Preparar input
            if context:
                full_message = f"{json.dumps(context)}\n\n{message}"
            else:
                full_message = message
            
            # Ejecutar
            result = subprocess.run(
                cmd,
                input=full_message.encode(),
                capture_output=True,
                timeout=60
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Qwen error: {result.stderr.decode()}")
            
            return result.stdout.decode().strip()
        except Exception as e:
            raise RuntimeError(f"Error using Qwen: {e}")
    
    def list_models(self) -> list:
        """Listar modelos disponibles"""
        try:
            result = subprocess.run(
                [self.qwen_path, "models", "list", "--all"],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.decode().strip().split("\n")
            return []
        except Exception:
            return []
    
    def get_quota(self) -> Dict[str, Any]:
        """Obtener información de quota"""
        try:
            result = subprocess.run(
                [self.qwen_path, "usage"],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                return {"usage": result.stdout.decode().strip()}
            return {}
        except Exception:
            return {}


# Funciones de utilidad
def analyze_market_metrics(metrics: Dict[str, float], model: str = "qwen3.6-plus") -> str:
    """Analizar métricas de mercado con Qwen"""
    client = QwenClient(model)
    
    prompt = f"""
Analiza estas métricas de mercado y proporciona recomendación de trading:

Métricas:
{json.dumps(metrics, indent=2)}

Proporciona:
1. Interpretación de cada métrica
2. Señales alcistas/bajistas
3. Recomendación de acción
"""
    return client.analyze(prompt)


def reasoning_trade_decision(analysis: Dict[str, Any]) -> str:
    """Usar modelo de razonamiento para decisión de trade"""
    client = QwenClient("qwen3-235b-a22b-thinking-2507")
    
    prompt = f"""
Utiliza razonamiento paso a paso para decidir si abrir un trade:

Análisis:
{json.dumps(analysis, indent=2)}

Pasos:
1. Verificar condiciones técnicas
2. Evaluar riesgo
3. Calcular risk/reward
4. Decisión final
"""
    return client.analyze(prompt)


if __name__ == "__main__":
    # Test
    try:
        client = QwenClient()
        print(f"✓ Cliente Qwen inicializado con modelo: {client.model}")
        
        # Listar modelos
        models = client.list_models()
        print(f"✓ Modelos disponibles: {len(models)}")
        
        # Ver quota
        quota = client.get_quota()
        print(f"✓ Quota: {quota}")
    except RuntimeError as e:
        print(f"✗ Error: {e}")
