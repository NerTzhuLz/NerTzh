# Devpost Hackathons Integration — PyCharm Setup

## Resumen

El archivo `x.py` en la raíz del proyecto integra directamente con **Codex CLI** (sesión ChatGPT web) para buscar, listar y obtener información sobre hackathons en Devpost **sin archivos intermedios** y **sin OPENAI_API_KEY requerida**.

## Requisitos previos

1. **Codex CLI instalado**
   ```bash
   pip install codex
   ```

2. **Autenticación Codex (una sola vez)**
   ```bash
   codex login --device-auth
   ```
   Esto abre una URL en el navegador; sigue las instrucciones para completar la autenticación con tu cuenta ChatGPT.

3. **Plan ChatGPT Plus o acceso a Codex**  
   - Codex tiene cuota mensual gratis (limitada)
   - Con ChatGPT Plus tienes acceso prioritario
   - Si agota cuota, espera al próximo período o usa `OPENAI_API_KEY`

## Uso desde terminal

```bash
# Ver ayuda
python x.py

# Buscar hackathons por palabra clave
python x.py search "AI"
python x.py search "blockchain"

# Listar hackathons abiertos actualmente
python x.py list

# Obtener info de registro para un hackathon específico
python x.py register "NombreHackathon"
```

Ejemplos de salida:
```json
{
  "query": "AI",
  "hackathons": [
    {
      "name": "AI Hackathon 2026",
      "platform": "devpost",
      "status": "open",
      "url": "https://devpost.com/software/...",
      "deadline": "2026-08-15"
    }
  ],
  "count": 1
}
```

## Integración en PyCharm

### Opción A: Ejecutar desde Run Configuration (recomendado)

1. Abre PyCharm → `Run` → `Edit Configurations`
2. Haz clic en `+` → `Python`
3. Configura:
   - **Name**: `Devpost Search`
   - **Script path**: `/path/to/_Metrics_/x.py`
   - **Parameters**: `search AI` (o el parámetro que desees)
   - **Python interpreter**: Selecciona `.venv` (si aún no está configurado: Settings → Project → Python Interpreter)
4. Haz clic en `Run` o presiona Shift+F10

Para otros comandos, crea configuraciones adicionales:
- `Devpost List` con parámetros: `list`
- `Devpost Register` con parámetros: `register "NombreHackathon"`

### Opción B: Run desde PyCharm Console

1. Abre la consola de Python en PyCharm (View → Tool Windows → Python Console)
2. Ejecuta:
   ```python
   import subprocess
   result = subprocess.run([".venv/bin/python", "x.py", "list"], capture_output=True, text=True)
   print(result.stdout)
   if result.stderr:
       print("Error:", result.stderr)
   ```

### Opción C: Importar como módulo

1. En tu script de PyCharm:
   ```python
   import sys
   import os
   
   # Ajusta la ruta según tu estructura
   sys.path.insert(0, "/path/to/_Metrics_")
   
   from x import search_hackathons, list_hackathons, register_info
   
   results = search_hackathons("AI")
   print(results)
   ```

## Configuración del intérprete `.venv` en PyCharm

Si aún no lo has configurado:

1. Abre Settings (Ctrl+Alt+S en Linux)
2. Ve a Project → Python Interpreter
3. Haz clic en el engranaje (⚙) → Add
4. Selecciona "Existing Environment"
5. Navega a `/home/angel/Documentos/_Metrics_/.venv/bin/python`
6. Haz clic en OK

## Solución de problemas

### "codex CLI no encontrado"
```bash
pip install codex
```

### "Not authenticated" / "Device authentication required"
```bash
codex login --device-auth
# Sigue el enlace en el navegador
```

### "You've hit your usage limit"
- Opción 1: Upgrade a ChatGPT Plus (https://chatgpt.com/explore/plus)
- Opción 2: Espera al próximo período (Devpost mostrará la fecha exacta)
- Opción 3: Usa OpenAI API Platform:
  ```bash
  export OPENAI_API_KEY="sk-..."
  # Luego modifica x.py para usar la API en lugar de Codex
  ```

### La salida no es JSON válido
- Codex a veces devuelve markdown con ```json``` alrededor
- El script intenta parsear JSON; si falla, devuelve `raw_response`
- Revisa el output manualmente o retry

### Timeout (>180s)
- Codex se toma tiempo procesando consultas complejas
- Vuelve a intentar o simplifica la consulta

## Arquitectura (sin archivos intermedios)

```
PyCharm
  │
  └─ x.py (Python)
      │
      └─ Codex CLI (subprocess)
          │
          └─ ChatGPT Web Session
              │
              └─ Devpost info → JSON response
```

**Ventajas:**
- No requiere OPENAI_API_KEY (usa sesión web gratis)
- Minimalista: una sola línea de conexión
- Sin archivos de cache, helpers o scrapers
- Comunicación directa con API vía CLI

**Limitaciones:**
- Cuota mensual limitada (Codex free tier)
- Requiere autenticación previa (`codex login`)
- Dependencia de Codex CLI estable

## Archivos

- `x.py` — Script principal (integración completa)
- `.venv/` — Entorno virtual del proyecto

## Comandos rápidos

```bash
# Instalar dependencias
pip install codex

# Autenticar (primera vez)
codex login --device-auth

# Ejecutar desde el proyecto
cd /home/angel/Documentos/_Metrics_
.venv/bin/python x.py search "AI"
```

---

**Nota**: Este script asume que Codex CLI está en PATH. Si se instaló con `pip install codex`, debería estarlo. Si no, usa la ruta completa al ejecutable.

