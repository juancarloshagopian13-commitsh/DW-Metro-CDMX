from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import Any


def configurar_logger(nombre: str = "etl_metro", carpeta_logs: str = "logs") -> logging.Logger:
    Path(carpeta_logs).mkdir(parents=True, exist_ok=True)
    ruta_log = Path(carpeta_logs) / f"{nombre}.log"

    logger = logging.getLogger(nombre)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formato = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

        handler_archivo = logging.FileHandler(ruta_log, encoding="utf-8")
        handler_archivo.setFormatter(formato)

        handler_consola = logging.StreamHandler()
        handler_consola.setFormatter(formato)

        logger.addHandler(handler_archivo)
        logger.addHandler(handler_consola)

    return logger


def emitir_evento_json(
    etapa: str,
    estado: str,
    detalle: str,
    metricas: dict[str, Any] | None = None,
    carpeta_mensajes: str = "mensajes",
) -> Path:
    Path(carpeta_mensajes).mkdir(parents=True, exist_ok=True)
    ahora = datetime.now(timezone.utc)
    payload = {
        "timestamp_utc": ahora.isoformat(),
        "proyecto": "DW-Metro-CDMX",
        "etapa": etapa,
        "estado": estado,  # "OK", "WARNING", "ERROR"
        "detalle": detalle,
        "metricas": metricas or {},
    }
    marca = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    archivo_evento = Path(carpeta_mensajes) / f"evento_{etapa}_{marca}.json"
    archivo_evento.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return archivo_evento