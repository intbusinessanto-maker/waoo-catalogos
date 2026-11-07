# Waoo Jeans — catálogos y listas de precios

Este repositorio es la **fuente de la verdad** de los catálogos y precios que se ven en
https://waootujeans.com/catalogos/ y que envía el bot de WhatsApp.

Es público a propósito: la web lee los archivos directamente de aquí. **Solo van catálogos y listas de precios** (nada de documentos internos ni datos de clientes).

## Carpetas
| Carpeta | Qué va | Se ve en la web como |
|---|---|---|
| `coleccion/` | Catálogos de productos de línea (colección vigente) | Pestaña "Colección nueva" |
| `promociones/` | Catálogos de stock / colecciones anteriores con descuento (remarketing) | Pestaña "Promociones" |
| `precios/` | Listas de precios (PDF o imagen) | Pestaña "Precios" |

## Cómo actualizar
1. Pon el PDF en la carpeta correcta. El nombre del archivo es el título: `Coleccion-VI-26.pdf` → "Colección VI 26".
   - Para fijar el orden, antepón un número: `01_Coleccion-VI-26.pdf` (el número no se muestra).
2. Haz commit y push. Una GitHub Action genera la portada (página 1) en `portadas/` y actualiza `manifest.json`.
3. La web se actualiza sola en unos minutos.

Para reemplazar un catálogo, sube el nuevo con el **mismo nombre** (el enlace no cambia). Para retirarlo, bórralo.

## Enlaces
- Hub: `https://waootujeans.com/catalogos/`
- Un catálogo: `https://waootujeans.com/catalogos/?c=<id>` (el `id` está en `manifest.json`, p. ej. `coleccion/coleccion-c`).
- Pestañas: `?tab=coleccion`, `?tab=promociones`, `?tab=precios`.

Generación local: `python3 scripts/build_manifest.py` (requiere poppler-utils).

## Equivalencia con los archivos originales (carpeta del proyecto)
| Archivo aquí | Original | Portada |
|---|---|---|
| `coleccion/01_Actitud-que-Inspira.pdf` | CATALOGO WAOO VI-26.pdf | "Actitud que Inspira" · Campaña 2026-6 |
| `coleccion/02_Denim-con-Actitud.pdf` | CAT WAOO D.pdf | "Denim con Actitud" · Campaña 2026-4 |
| `coleccion/03_Coleccion-2026.pdf` | CAT WAOO C.pdf | "EST 2026" |
| `promociones/01_Promociones-A.pdf` | remarketing/CAT WAOO A.pdf | Stock |
| `promociones/02_Promociones-B.pdf` | remarketing/CAT WAOO B.pdf | Stock (San Valentín) |
