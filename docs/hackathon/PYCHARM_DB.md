# PyCharm Database — metrics-pg

Ya preconfigurado en `.idea/dataSources.xml`.

## Si no aparece

1. **File → Invalidate Caches** no hace falta normalmente.
2. Cierra y reabre el proyecto: `pycharm /home/angel/Documentos/_Metrics_`
3. **View → Tool Windows → Database**
4. Debe verse: **metrics_db @ metrics-pg**
5. Click derecho → **Refresh** / **Test Connection**

## Valores

| Campo | Valor |
|-------|--------|
| Host | 127.0.0.1 |
| Port | **5433** |
| User | metrics |
| Password | metrics_pass |
| Database | metrics_db |
| SSL | **disable** |

## Contenedor

```bash
docker start metrics-pg
```
