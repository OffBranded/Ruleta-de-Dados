import base64, pathlib, re, sys

base = pathlib.Path(__file__).parent
src = base / "icons"
files = sorted(src.glob("*.svg")) if src.is_dir() else []
if not files:
    sys.exit("No encontré SVGs en " + str(src))

out = ["/* Generado por el script de python — no editar a mano. */"]
for f in files:
    svg = f.read_text(encoding="utf-8")
    svg = re.sub(r"<\?xml[^>]*\?>|<!--.*?-->|<!DOCTYPE[^>]*>", "", svg, flags=re.S).strip()
    if "xmlns=" not in svg:  # necesario para que el navegador lo lea como imagen
        svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    out.append('.ic[data-i="%s"]{--u:url("data:image/svg+xml;base64,%s")}' % (f.stem, b64))

(base / "icons.css").write_text("\n".join(out) + "\n", encoding="utf-8")
print("icons.css generado con %d iconos: %s" % (len(files), ", ".join(f.stem for f in files)))
