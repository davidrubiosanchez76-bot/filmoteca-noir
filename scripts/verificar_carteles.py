#!/usr/bin/env python3
"""Comprueba los enlaces de carteles sin descargar ni copiar imágenes."""
import concurrent.futures
import csv
import json
import urllib.request
import urllib.error
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
films = json.loads((ROOT / "peliculas.json").read_text(encoding="utf-8"))
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; FilmotecaNoirLinkAudit/1.0)",
    "Accept": "image/avif,image/webp,image/*,*/*;q=0.7",
}

def check(film):
    url = film.get("poster", "")
    row = {"pelicula": film.get("title", ""), "url": url,
           "estado": "sin_comprobar", "http": "", "tipo": "", "detalle": ""}
    if not url.startswith("https://"):
        row["estado"] = "url_invalida"
        return row
    try:
        req = urllib.request.Request(url, headers=HEADERS, method="HEAD")
        try:
            resp = urllib.request.urlopen(req, timeout=14)
        except urllib.error.HTTPError as exc:
            if exc.code not in (405, 501):
                raise
            req = urllib.request.Request(
                url, headers={**HEADERS, "Range": "bytes=0-1023"}, method="GET")
            resp = urllib.request.urlopen(req, timeout=14)
        with resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
        row.update(http=str(status), tipo=content_type)
        row["estado"] = "ok" if content_type.startswith("image/") else "respuesta_no_imagen"
    except urllib.error.HTTPError as exc:
        row["http"] = str(exc.code)
        row["estado"] = ("no_encontrado" if exc.code in (404, 410)
                         else "bloqueado_o_antibot" if exc.code in (401, 403, 429)
                         else "error_http")
        row["detalle"] = str(exc.reason)
    except Exception as exc:
        row["estado"] = "fallo_red_o_servidor"
        row["detalle"] = str(exc)[:180]
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    rows = list(pool.map(check, films))
result = {
    "revisado_utc": datetime.now(timezone.utc).isoformat(),
    "advertencia": "403/429 pueden ser bloqueos a robots, no prueban que la imagen no aparezca en el navegador.",
    "total": len(rows),
    "resultados": rows,
}
(ROOT / "revision_carteles.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
with (ROOT / "revision_carteles.csv").open("w", encoding="utf-8-sig", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print("Películas comprobadas:", len(rows))
print(dict(Counter(row["estado"] for row in rows)))
