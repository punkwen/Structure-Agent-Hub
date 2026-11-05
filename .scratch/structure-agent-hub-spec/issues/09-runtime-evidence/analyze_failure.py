"""Analyze failure reached through the planned runner path.

ops.analyze() returning a negative flag does not raise, so under the ticket 07
rule this script should reach its end and be reported TGC_DONE even though the
solve failed. Prints the return value so the log shows both facts.
"""
import openseespy.opensees as ops

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
print("analyze_rc", rc)
print("script reached its end")
