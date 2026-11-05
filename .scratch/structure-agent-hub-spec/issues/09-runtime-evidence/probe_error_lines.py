"""Probe 4: what OpenSees error/warning lines actually look like.

Also checks whether a Python print before/after OpenSees output keeps its order
in a merged single-fd log, and whether WARNING lines always end with a newline.
"""
import traceback

import openseespy.opensees as ops


def case(label, fn):
    print(f"PY-BEFORE {label}", flush=True)
    try:
        print(f"RET {label} {fn()!r}", flush=True)
    except BaseException as exc:  # noqa: BLE001
        print(f"RAISED {label} {type(exc).__name__}: {exc}", flush=True)
        traceback.print_exc()
    print(f"PY-AFTER {label}", flush=True)


def bad_node_tag():
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    ops.node(1, 0.0, 0.0)
    ops.fix(1, 1, 1)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    return ops.load(99, 1.0, 0.0)


def bad_element():
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    ops.node(1, 0.0, 0.0)
    ops.node(2, 1.0, 0.0)
    ops.fix(1, 1, 1)
    ops.fix(2, 0, 1)
    return ops.element("elasticBeamColumn", 1, 1, 2, 0.0, 1.0)


def bad_material():
    ops.wipe()
    return ops.uniaxialMaterial("NoSuchMaterial", 1)


def duplicate_node():
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    ops.node(1, 0.0, 0.0)
    return ops.node(1, 1.0, 0.0)


def missing_analysis_options_kept():
    # A load pattern with a zero reference load under DisplacementControl:
    # reproduces the WARNING sequence suspected of missing newlines.
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)
    ops.node(1, 0.0, 0.0)
    ops.node(2, 1.0, 0.0)
    ops.fix(1, 1, 1, 1)
    ops.fix(2, 0, 1, 0)
    ops.geomTransf("Linear", 1)
    ops.uniaxialMaterial("Elastic", 1, 29000.0)
    ops.section("Elastic", 1, 29000.0, 100.0, 1.0)
    ops.beamIntegration("Lobatto", 1, 1, 3)
    ops.element("forceBeamColumn", 1, 1, 2, 1, 1)
    ops.timeSeries("Linear", 1)
    ops.pattern("Plain", 1, 1)
    ops.system("BandGeneral")
    ops.numberer("RCM")
    ops.constraints("Plain")
    ops.integrator("DisplacementControl", 2, 1, 0.01)
    ops.algorithm("Newton")
    ops.analysis("Static")
    return ops.analyze(1)


case("bad_node_tag", bad_node_tag)
case("bad_element", bad_element)
case("bad_material", bad_material)
case("duplicate_node", duplicate_node)
case("missing_analysis_options_kept", missing_analysis_options_kept)
