"""Regenerate runs/install_meta/install.txt from live commands (no hand-typed output)."""
import hashlib
import importlib.metadata as md
import json
import os
import pathlib
import subprocess
import sys

SITE = pathlib.Path(sys.prefix) / "Lib" / "site-packages"
OUT = pathlib.Path(__file__).parent / "runs" / "install_meta" / "install.txt"
OUT.parent.mkdir(parents=True, exist_ok=True)

lines = []
for name in ("openseespy", "openseespywin"):
    d = md.distribution(name)
    lines.append(json.dumps({
        "name": d.metadata["Name"],
        "version": d.version,
        "requires_python": d.metadata["Requires-Python"],
        "requires_dist": d.requires,
    }, ensure_ascii=False))
    lines.append(f"WHEEL {name}: " + (SITE / f"{name}-{d.version}.dist-info" / "WHEEL").read_text().replace("\n", " | ").strip())

pyd = SITE / "openseespywin" / "opensees.pyd"
lines.append(f"opensees.pyd size={pyd.stat().st_size} sha256={hashlib.sha256(pyd.read_bytes()).hexdigest()}")
record = (SITE / "openseespywin-3.8.0.0.dist-info" / "RECORD").read_text()
lines.append("RECORD pyd line: " + next(l for l in record.splitlines() if l.endswith(".pyd,sha256=JbpC4WclJhN9dl2cNjHRQD4JH1T1r825JC-SQ8Y8OpY,17206272")))

dl = pathlib.Path(os.environ["TEMP"]) / "tgc_os_dl"
for whl in sorted(dl.glob("*.whl")):
    lines.append(f"downloaded {whl.name} size={whl.stat().st_size} sha256={hashlib.sha256(whl.read_bytes()).hexdigest()}")

OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))
