# Agents — _Metrics_ (sin candados)

Proyecto de hackathon **OpenAI Build Week** ([devpost](https://openai.devpost.com/)), pero **sin locks de modelo ni de herramienta**.

## Libertad de modelos

- Usa **cualquier modelo** que te ofrezca Codex / ChatGPT (GPT-5.x, o los que vengan en tu plan).
- No hay `AGENT_LOCK`, no hay modelo fijo en el repo.
- No fuerces `-m ...` en scripts salvo que **tú** pases `CODEX_MODEL` o `-m` a mano.

## Credenciales del producto (bot)

- Solo Bybit + Postgres en `.env` del proyecto (trading).
- No hardcodees API keys en código ni en `bashrc` desde este repo.
- Keys de LLM las gestiona Codex/ChatGPT (sesión); no hace falta meter `OPENAI_API_KEY` en `.env` del bot.

## Cómo arrancar el agente (libre)

```bash
cd /home/angel/Documentos/_Metrics_
./scripts/codex_here.sh          # TUI — eliges modelo ahí
# o
codex -C /home/angel/Documentos/_Metrics_
# o con modelo que TÚ elijas en el momento:
codex -C /home/angel/Documentos/_Metrics_ -m <el-que-quieras>
```

## Notas del evento (informativas, no restrictivas)

- Submit: ~21 Jul 2026 5 PM PT — ver `docs/hackathon/OPENAI_BUILD_WEEK.md`
- El form puede pedir Session ID `/feedback` y mencionar GPT/Codex: es del **submission**, no un límite técnico del repo.
- Backlog sugerido: `docs/hackathon/BACKLOG.md` (prioridades, no prohibiciones)

## Seguridad trading

- Default recomendado: `ENV=demo` en `.env`. Mainnet solo si el humano lo pide.
