"""Minimal cantilever: 2-node 3D elastic beam, tip point load.

Analytic tip deflection: delta = P*L^3 / (3*E*I).
Inputs are SI: E=2.0e11 Pa, I=1.333333e-4 m^4, L=2 m, P=1000 N -> delta = 1.0e-4 m.
The script asserts the analytic value itself; the runner status file only says
the script reached its end.
"""
import os

import openseespy.opensees as ops

print("cwd", os.getcwd())

E = 2.0e11
G = 0.8e11
A = 0.04
I = 0.2 * 0.2**3 / 12  # 1.333...e-4 m^4
L = 2.0
P = 1000.0
EXPECTED = P * L**3 / (3.0 * E * I)
TOL = 1.0e-9

ops.wipe()
ops.model("basic", "-ndm", 3, "-ndf", 6)
ops.node(1, 0.0, 0.0, 0.0)
ops.node(2, L, 0.0, 0.0)
ops.fix(1, 1, 1, 1, 1, 1, 1)
ops.geomTransf("Linear", 1, 0.0, 0.0, 1.0)
ops.element("elasticBeamColumn", 1, 1, 2, A, E, G, I, I, I, 1)
ops.timeSeries("Linear", 1)
ops.pattern("Plain", 1, 1)
ops.load(2, 0.0, -P, 0.0, 0.0, 0.0, 0.0)
ops.recorder("Node", "-file", "disp.out", "-time", "-node", 2, "-dof", 2, "disp")
ops.system("BandGeneral")
ops.numberer("RCM")
ops.constraints("Plain")
ops.integrator("LoadControl", 1.0)
ops.algorithm("Linear")
ops.analysis("Static")
rc = ops.analyze(1)
print("analyze_rc", rc)
print("node2_disp2", ops.nodeDisp(2, 2))
print("expected", -EXPECTED, "tol", TOL)
assert rc == 0, f"analyze returned {rc}"
assert abs(ops.nodeDisp(2, 2) - (-EXPECTED)) <= TOL, "tip deflection does not match analytic value"
print("ANALYTIC_CHECK_OK")
