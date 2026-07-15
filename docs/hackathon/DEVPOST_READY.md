# ✅ Devpost — Estado Listo para Entregar

**Fecha:** 2026-07-14  
**Deadline:** 2026-07-21 @ 5:00 PM PT  
**Tiempo restante:** 7 días

## Estado Verificado (2026-07-14)

| Área | Estado | Evidencia / siguiente paso |
|------|--------|----------------------------|
| GitHub | ✅ Publicado | `NerTzhuLz/NerTzh` es público y `main` contiene la integración GPT-5/multiagente. |
| Registro Build Week | ⏳ Por verificar | El conector Devpost requiere reautenticación antes de poder comprobarlo desde Codex. |
| Proyecto en Devpost | ⏳ Por verificar | Confirmar que existe un borrador o envío para **NertzMetalEngine** tras reconectar Devpost. |
| Créditos Codex | ⏳ En revisión | Solicitud de USD 100 enviada; esperar hasta 24 horas y no enviar otra solicitud. |

---

## 🟢 YA LISTO (copiar a Devpost)

| Item | Status | Ubicación |
|------|--------|-----------|
| ✅ Project name | READY | `NerTzh` |
| ✅ Tagline | READY | `docs/hackathon/DEVPOST_COPY_PASTE.md` (seccion 2) |
| ✅ Long description | READY | `docs/hackathon/DEVPOST_COPY_PASTE.md` (seccion 3) |
| ✅ Built with | READY | `docs/hackathon/DEVPOST_COPY_PASTE.md` (seccion 4) |
| ✅ Code quality | ✓ | `src/gpt_integration.py`, `src/hackathon/agents.py`, etc. |
| ✅ API endpoint | ✓ | `src/api_app.py` → `/agent/chat` |
| ✅ Web UI | ✓ | `web_ui/index.html` → http://127.0.0.1:8081/web/ |
| ✅ No secrets in git | ✓ | `.env` → `.gitignore` |
| ✅ Demo mode safe | ✓ | `ENV=demo` (no real trading) |
| ✅ Setup docs | ✓ | `README.md` + `docs/hackathon/QUICKSTART.md` |

---

## 🟡 EN PROGRESO (falta esto)

| Item | Status | Prioridad | Acción |
|------|--------|-----------|--------|
| ⏳ Video demo (< 3 min) | NOT RECORDED | 🔴 URGENTE | Grabar antes del 20 de julio |
| ⏳ YouTube link | PENDING | 🔴 URGENTE | Subir video a YouTube (public/unlisted) |
| ✅ Repository link | READY | — | `https://github.com/NerTzhuLz/NerTzh` es público |
| ⏳ Registro Devpost | VERIFY | 🔴 URGENTE | Reautenticar el plugin y comprobar el registro en OpenAI Build Week |
| ⏳ Proyecto Devpost | VERIFY | 🔴 URGENTE | Confirmar borrador, campos obligatorios y estado de envío |
| ⏳ Créditos Codex | IN REVIEW | 🟡 | Esperar la resolución del formulario; no reenviar mientras esté en revisión |

---

## 🟢 CHECKLIST FINAL (antes de Submit)

```
PRE-SUBMISSION (do this 1 day before deadline):

☐ 1. Test completo:
    $ make setup && make db-up && make check
    
☐ 2. API + Web UI funcionan:
    $ make api
    Abrir: http://127.0.0.1:8081/web/
    Probar query: "¿BUY en BTCUSDT?"
    
☐ 3. Video grabado:
    [ ] Segment 1 — Problem (30 sec) ✓
    [ ] Segment 2 — Solution (90 sec) ✓
    [ ] Segment 3 — Live Demo (30 sec) ✓
    [ ] Segment 4 — Tech Stack (30 sec) ✓
    Total: < 3 min ✓
    
☐ 4. Video subido a YouTube:
    [ ] Link público o unlisted
    [ ] Abierto sin restricciones
    
☐ 5. Devpost form completo:
    [ ] Nombre del proyecto
    [ ] Tagline (1 línea)
    [ ] Descripción larga (copy-paste ready)
    [ ] Built with (tecnologías)
    [ ] Repository URL (GitHub public)
    [ ] Demo URL (YouTube video)
    [ ] Your contribution (1 párrafo)
    [ ] Category: "Developer tools"
    
☐ 6. Links verificados:
    [ ] GitHub repo accesible
    [ ] YouTube video visible
    [ ] Devpost form 100% completo
    
☐ 7. Final check:
    [ ] No typos
    [ ] Emojis claros
    [ ] Formato markdown correcto
    [ ] All dates & times correct
    
☐ 8. SUBMIT
    Click "Submit" en Devpost
    Guardar confirmación (screenshot)
```

---

## 📹 VIDEO RECORDING (Quick Reference)

**Tool:** OBS Studio, Screenflow (Mac), o similar  
**Duration:** < 3 minutes total  
**Resolution:** 1080p or 720p  
**Quality:** Screen + voice clear

### Segments

```
[0:00-0:30]   Segment 1 — PROBLEM
              Show: Orderbook chaos (bid/ask bouncing)
              Say: "Crypto traders need AI-powered signals"

[0:30-2:00]   Segment 2 — SOLUTION
              Run: $ make api
              Show: Web UI at 127.0.0.1:8081/web/
              Type: "¿BUY BTCUSDT Combined=7.2?"
              Show: GPT-5 response {action, confidence, reasoning}
              Highlight: Context Bridge + function calling

[2:00-2:30]   Segment 3 — LIVE DEMO
              Type query: "Market momentum?"
              Show: JSON response
              Click: Audit trail in PostgreSQL

[2:30-3:00]   Segment 4 — TECH STACK
              Show diagram: Bybit → Metrics → GPT-5 → UI
              Say: "OpenAI GPT-5, FastAPI, PostgreSQL, DuckDB"
              Say: "Multi-agent consensus decisions"
```

**Upload:**
1. Save as MP4 (h264 codec)
2. Upload to YouTube (public or unlisted)
3. Get shareable link
4. Paste in Devpost "Demo URL / Video"

---

## 📝 COPY-PASTE CHECKLIST

**These files are 100% ready to copy from:**

```
1. Tagline:
   → docs/hackathon/DEVPOST_COPY_PASTE.md (section 2)
   
2. Description:
   → docs/hackathon/DEVPOST_COPY_PASTE.md (section 3)
   
3. Built with:
   → docs/hackathon/DEVPOST_COPY_PASTE.md (section 4)
   
4. Setup instructions:
   → README.md (DevOps section)
   
5. Your contribution:
   → docs/hackathon/DEVPOST_COPY_PASTE.md (section 9)
```

---

## 🎯 Timeline

| Date | Milestone | Status |
|------|-----------|--------|
| 2026-07-14 (hoy) | GitHub público + docs listas | ✅ |
| 2026-07-14 (hoy) | Verificar registro y borrador Devpost | ⏳ |
| 2026-07-14 (hoy) | Solicitud de créditos Codex en revisión | ⏳ |
| 2026-07-17 | ⏳ **DEADLINE: Video ready** | ⏳ |
| 2026-07-18 | ⏳ **Devpost form 90% complete** | ⏳ |
| 2026-07-20 | ⏳ **Final checks** | ⏳ |
| 2026-07-21 @ 5PM | 🚀 **SUBMIT** | 🚀 |

---

## 🆘 Troubleshooting

**"make api" fails:**
```bash
# 1. Check Postgres running
docker ps | grep metrics-pg

# 2. Check env vars
cat .env | grep OPENAI

# 3. Reinstall deps
uv sync
```

**Web UI not loading:**
```bash
# Check port 8081
lsof -i :8081

# Restart API
pkill -f "python.*api_app"
make api
```

**Video too long:**
- Cut Segment 2 from 90 sec to 70 sec
- Total should stay < 3 min (target: 2:45)

---

## 💡 Final Notes

- ✅ **No hardcoded model** — uses `OPENAI_MODEL` env var
- ✅ **Demo mode safe** — `ENV=demo` prevents real trading
- ✅ **No secrets in git** — `.gitignore` covers `.env`, keys, etc.
- ✅ **Production-ready** — Postgres audit trail, Prometheus metrics
- 🔐 **Security conscious** — multi-agent consensus validates all decisions

---

**Generated:** 2026-07-14  
**Ready to submit:** 2026-07-21

Good luck! 🎯

