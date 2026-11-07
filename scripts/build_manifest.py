#!/usr/bin/env python3
"""Genera portadas/ y manifest.json a partir de los archivos en coleccion/, promociones/ y precios/.

Reglas:
- Cada PDF o imagen (jpg, jpeg, png, webp) de esas carpetas es un ítem.
- El título sale del nombre del archivo: guiones -> espacios ("Coleccion-C.pdf" -> "Colección C").
- Un prefijo numérico opcional define el orden y no se muestra ("01_Coleccion-VI-26.pdf").
- Para cada PDF se genera la portada (página 1) en portadas/ y se cuenta el número de páginas.
Requiere poppler-utils (pdfinfo, pdftoppm).
"""
import json
import re
import subprocess
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = [
    ("coleccion", "Colección nueva"),
    ("promociones", "Promociones"),
    ("precios", "Precios"),
]
EXT_PDF = {".pdf"}
EXT_IMG = {".jpg", ".jpeg", ".png", ".webp"}
FIXES = {"Coleccion": "Colección", "Catalogo": "Catálogo", "Dolares": "Dólares"}


def slug(text: str) -> str:
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")


def title_from(stem: str) -> str:
    stem = re.sub(r"^\d+[_-]", "", stem)
    words = re.split(r"[-_ ]+", stem)
    return " ".join(FIXES.get(w, w) for w in words if w)


def order_key(p: Path):
    m = re.match(r"^(\d+)[_-]", p.name)
    return (int(m.group(1)) if m else 9999, p.name.lower())


def pdf_pages(path: Path) -> int:
    out = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else 0


def make_cover(path: Path, dest: Path) -> None:
    dest.parent.mkdir(exist_ok=True)
    base = dest.with_suffix("")
    subprocess.run(
        ["pdftoppm", "-f", "1", "-l", "1", "-jpeg", "-jpegopt", "quality=80",
         "-scale-to-x", "600", "-scale-to-y", "-1", "-singlefile", str(path), str(base)],
        check=True,
    )


def main() -> None:
    manifest = {"secciones": []}
    covers_used = set()
    for folder, label in SECTIONS:
        items = []
        d = ROOT / folder
        files = sorted([p for p in d.glob("*") if p.is_file() and p.suffix.lower() in EXT_PDF | EXT_IMG], key=order_key) if d.exists() else []
        for p in files:
            item = {
                "id": f"{folder}/{slug(re.sub(r'^\d+[_-]', '', p.stem))}",
                "titulo": title_from(p.stem),
                "archivo": f"{folder}/{p.name}",
                "tipo": "pdf" if p.suffix.lower() in EXT_PDF else "imagen",
                "bytes": p.stat().st_size,
            }
            if item["tipo"] == "pdf":
                cover = ROOT / "portadas" / f"{folder}__{slug(p.stem)}.jpg"
                make_cover(p, cover)
                covers_used.add(cover.name)
                item["portada"] = f"portadas/{cover.name}"
                item["paginas"] = pdf_pages(p)
            else:
                item["portada"] = item["archivo"]
            items.append(item)
        manifest["secciones"].append({"id": folder, "titulo": label, "items": items})
    # quitar portadas huérfanas
    pdir = ROOT / "portadas"
    if pdir.exists():
        for c in pdir.glob("*.jpg"):
            if c.name not in covers_used:
                c.unlink()
    (ROOT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({s["id"]: [i["titulo"] for i in s["items"]] for s in manifest["secciones"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
