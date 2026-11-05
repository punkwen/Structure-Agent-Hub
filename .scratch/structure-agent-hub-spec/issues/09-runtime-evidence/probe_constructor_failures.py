"""Probe 9: constructor failures that only warn, then analyze()."""
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


def bad_analysis_then_analyze():
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    ops.node(1, 0.0, 0.0)
    ops.fix(1, 1, 1)
    ops.analysis("NoSuchAnalysis")
    return ops.analyze(1)


def bad_integrator_then_analyze():
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 2)
    ops.node(1, 0.0, 0.0)
    ops.fix(1, 1, 1)
    ops.system("BandGeneral")
    ops.numberer("RCM")
    ops.constraints("Plain")
    ops.integrator("NoSuchIntegrator")
    ops.algorithm("Linear")
    ops.analysis("Static")
    return ops.analyze(1)


case("bad_analysis_then_analyze", bad_analysis_then_analyze)
case("bad_integrator_then_analyze", bad_integrator_then_analyze)
