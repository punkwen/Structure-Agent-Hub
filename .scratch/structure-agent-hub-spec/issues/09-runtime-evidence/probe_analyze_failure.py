"""Probe 2: analyze() failure surface.

Each case runs in a fresh interpreter (caller runs this script once) after ops.wipe().
Recorded per case: Python return value, whether a Python exception was raised,
and what reached stdout/stderr.
"""
import traceback

import openseespy.opensees as ops


def show(label, fn):
    print(f"=== CASE {label} BEGIN")
    try:
        value = fn()
        print(f"RESULT {label} returned {value!r} type={type(value).__name__}")
    except BaseException as exc:  # noqa: BLE001 - the point is to record everything
        print(f"RESULT {label} raised {type(exc).__name__}: {exc}")
        traceback.print_exc()
    print(f"=== CASE {label} END")


def no_analysis_defined():
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    ops.node(1, 0.0, 0.0)
    ops.fix(1, 1, 1)
    return ops.analyze(1)


def singular_mechanism():
    # 2D truss, four pinned joints, no diagonal: stiffness matrix is singular.
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
    return ops.analyze(1)


def nonconvergent():
    # Displacement-controlled push past an elastic-perfectly-plastic limit with
    # zero hardening: a single big step, Newton with 2 iterations cannot converge.
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)
    ops.node(1, 0.0, 0.0)
    ops.node(2, 1.0, 0.0)
    ops.fix(1, 1, 1, 1)
    ops.fix(2, 0, 1, 0)
    ops.geomTransf("Linear", 1)
    ops.uniaxialMaterial("Steel01", 1, 29000.0, 29000.0, 0.0)
    ops.section("Fiber", 1)
    ops.patch("rect", 1, 4, 4, -0.25, -0.25, 0.25, 0.25)
    ops.beamIntegration("Lobatto", 1, 1, 3)
    ops.element("forceBeamColumn", 1, 1, 2, 1, 1)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    ops.load(2, 0.0, -100.0, 0.0)
    ops.system("BandGeneral")
    ops.numberer("RCM")
    ops.constraints("Plain")
    ops.integrator("DisplacementControl", 2, 1, 0.05)
    ops.algorithm("Newton")
    ops.test("NormDispIncr", 1.0e-8, 2, 0)
    ops.analysis("Static")
    return ops.analyze(1)


show("no_analysis_defined", no_analysis_defined)
show("singular_mechanism", singular_mechanism)
show("nonconvergent", nonconvergent)
