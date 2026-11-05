"""Probe 7: does merged-log ordering survive Python's stdout buffering?

Prints without flush before and after an OpenSees call that writes to stderr.
Run once normally and once with PYTHONUNBUFFERED=1 to compare.
"""
import openseespy.opensees as ops

print("PY-BEFORE-ANALYZE")
ops.wipe()
ops.model("basic", "-ndm", 2, "-ndf", 2)
ops.node(1, 0.0, 0.0)
ops.node(2, 0.0, 1.0)
ops.node(3, 1.0, 0.0)
ops.node(4, 1.0, 1.0)
ops.fix(1, 1, 1)
ops.fix(2, 1, 1)
ops.fix(3, 1, 1)
ops.uniaxialMaterial("Elastic", 1, 29000.0)
ops.element("Truss", 1, 1, 4, 1.0, 1)
ops.element("Truss", 2, 2, 3, 1.0, 1)
ops.timeSeries("Linear", 1)
ops.pattern("Plain", 1, 1)
ops.load(4, 1.0, 0.0)
ops.system("FullGeneral")
ops.numberer("RCM")
ops.constraints("Plain")
ops.integrator("LoadControl", 1.0)
ops.algorithm("Linear")
ops.analysis("Static")
rc = ops.analyze(1)
print("PY-AFTER-ANALYZE", rc)
