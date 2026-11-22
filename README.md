# Filmoteca Noir — Balas y Estrellas

Bóveda de datos del catálogo cinematográfico del blog **Balas y Estrellas**.

- **[peliculas.json](peliculas.json)**: 54 películas catalogadas con título, país, año, dirección, reparto, sinopsis, carteles, enlaces y clasificaciones originales.
- **[scripts/verificar_carteles.py](scripts/verificar_carteles.py)**: comprobador de URLs de los carteles.
- **[Revisar enlaces de carteles](.github/workflows/revisar-carteles.yml)**: automatización semanal (lunes, 07:30 UTC) y ejecución manual desde la pestaña **Actions**. Genera archivos `revision_carteles.csv` y `revision_carteles.json`.

## Blogger

La página Filmoteca Noir obtiene el catálogo de:

`https://raw.githubusercontent.com/davidrubiosanchez76-bot/filmoteca-noir/main/peliculas.json`

**No cambiar** los valores `crime`, `tone` ni `genres` al añadir o actualizar películas sin revisar los filtros y el recomendador de Blogger. El HTML y las ilustraciones del sitio permanecen en Blogger.

## Carteles

Los enlaces de carteles siguen siendo externos inicialmente. El informe permite detectar URLs sospechosas; **una respuesta HTTP 403 o 429 puede indicar bloqueo a robots, no necesariamente una imagen desaparecida**.

No se descargan ni redistribuyen imágenes ajenas. El campo `posterAlternativo` está preparado para incorporar una URL de reserva previamente verificada, respetando las condiciones de uso y los derechos aplicables.

Para ejecutar una revisión: **Actions → Revisar enlaces de carteles → Run workflow → main → Run workflow**. Los resultados aparecerán en la raíz del repositorio cuando finalice con éxito.

## Seguridad de actualización

Mantener el HTML actual de Blogger hasta comprobar en una vista de prueba que el código que carga esta bóveda funciona correctamente.
