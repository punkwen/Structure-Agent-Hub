"""Probe 1: import facts and banner channel. Run from any CWD."""
import importlib.metadata as md
import json
import platform
import sys

print("PYEXE", sys.executable)
print("PYVER", sys.version)
print("PLATFORM", platform.platform())
for name in ("openseespy", "openseespywin"):
    try:
        d = md.distribution(name)
        print(name, "version=", d.version, "requires_python=", d.metadata["Requires-Python"])
        print(name, "requires=", d.requires)
    except md.PackageNotFoundError as exc:
        print(name, "NOT INSTALLED:", exc)

import openseespy
import openseespy.opensees as ops

print("OPENSEESPY_FILE", openseespy.__file__)
print("OPS_MODULE_FILE", ops.__file__)
ops.wipe()
print("OPS_VERSION_CALL_BEGIN")
version = ops.version()
print("OPS_VERSION", json.dumps(version))
print("OPS_VERSION_CALL_END")
