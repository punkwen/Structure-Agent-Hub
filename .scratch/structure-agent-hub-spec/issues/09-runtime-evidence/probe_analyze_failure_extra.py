"""Probe 5: more analyze() failure modes, checking the
'OpenSees > analyze failed, returned: N error flag' line and the return value.
"""
import traceback

import openseespy.opensees as ops


def show(label, fn):
    print(f"=== CASE {label} BEGIN", flush=True)
    try:
        value = fn()
        print(f"RESULT {label} returned {value!r}", flush=True)
    except BaseException as exc:  # noqa: BLE001
        print(f"RESULT {label} raised {type(exc).__name__}: {exc}", flush=True)
        traceback.print_exc()
    print(f"=== CASE {label} END", flush=True)


def _frame(bad_material=False):
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)
    ops.node(1, 0.0, 0.0)
    ops.node(2, 1.0, 0.0)
    ops.fix(1, 1, 1, 1)
    ops.fix(2, 0, 1, 0)
    ops.geomTransf("Linear", 1)
    if bad_material:
        ops.uniaxialMaterial("NoSuchMaterial", 1)
    else:
        ops.uniaxialMaterial("Elastic", 1, 29000.0)
    ops.section("Elastic", 1, 29000.0, 100.0, 1.0)
    ops.beamIntegration("Lobatto", 1, 1, 3)
    ops.element("forceBeamColumn", 1, 1, 2, 1, 1)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    ops.load(2, 0.0, -10.0, 0.0)


def norm_unbalance_fail():
    _frame()
    ops.system("BandGeneral")
    ops.numberer("RCM")
    ops.constraints("Plain")
    ops.integrator("DisplacementControl", 2, 1, 100.0)
    ops.algorithm("Newton")
    ops.test("NormUnbalance", 1.0e-30, 1, 0)
    ops.analysis("Static")
    return ops.analyze(5)


def bad_element_after_frame():
    _frame(bad_material=True)
    return "not reached"


def unconstrained_dof():
    # Node 3 has mass but no element: its DOFs carry no stiffness.
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    ops.node(1, 0.0, 0.0)
    ops.node(2, 1.0, 0.0)
    ops.node(3, 2.0, 0.0)
    ops.fix(1, 1, 1)
    ops.fix(2, 0, 1)
    ops.fix(3, 0, 1)
    ops.mass(3, 1.0, 1.0)
    ops.uniaxialMaterial("Elastic", 1, 29000.0)
    ops.element("Truss", 1, 1, 2, 1.0, 1)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    ops.load(3, 1.0, 0.0)
    ops.system("FullGeneral")
    ops.numberer("RCM")
    ops.constraints("Plain")
    ops.integrator("LoadControl", 1.0)
    ops.algorithm("Linear")
    ops.analysis("Static")
    return ops.analyze(1)


show("norm_unbalance_fail", norm_unbalance_fail)
show("unconstrained_dof", unconstrained_dof)
