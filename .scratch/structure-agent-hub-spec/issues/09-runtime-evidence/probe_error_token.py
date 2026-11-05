"""Probe 6: do any OpenSeesPy paths print a literal 'ERROR' line?"""
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


def bad_model_ndm():
    ops.wipe()
    return ops.model("basic", "-ndm", 9, "-ndf", 2)


def bad_node_coords():
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    return ops.node(1, 0.0)


def bad_recorder():
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    ops.node(1, 0.0, 0.0)
    return ops.recorder("Node", "-file", "x.out", "-node", 1)


def bad_analysis_type():
    ops.wipe()
    return ops.analysis("NoSuchAnalysis")


def bad_integrator():
    ops.wipe()
    return ops.integrator("NoSuchIntegrator")


def missing_element_material():
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    ops.node(1, 0.0, 0.0)
    ops.node(2, 1.0, 0.0)
    ops.fix(1, 1, 1)
    ops.fix(2, 0, 1)
    return ops.element("Truss", 1, 1, 2, 1.0, 99)


case("bad_model_ndm", bad_model_ndm)
case("bad_node_coords", bad_node_coords)
case("bad_recorder", bad_recorder)
case("bad_analysis_type", bad_analysis_type)
case("bad_integrator", bad_integrator)
case("missing_element_material", missing_element_material)
