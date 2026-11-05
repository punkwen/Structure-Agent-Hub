"""Probe 3: runner-shaped subprocess harness (no MCP code).

Mimics the completion rule chosen in ticket 07: execute a user script with
runpy.run_path, then write a separate status file; status is TGC_DONE only when
the script returns normally or raises SystemExit(0)/SystemExit(None).
Merged log = stdout+stderr written to one file by the child, so OS-level
interleaving is preserved as far as the OS pipe allows.
"""
import json
import os
import runpy
import subprocess
import sys
import traceback

SCRIPT = os.path.abspath(sys.argv[1])
# Absolute: the child runs with cwd=RUN_DIR, so a relative run dir breaks here.
RUN_DIR = os.path.abspath(sys.argv[2])
STATUS = os.path.join(RUN_DIR, ".tgc-run-status.json")


def child():
    status = "TGC_DONE"
    record = {"status": status, "exception": None, "system_exit_code": None}
    try:
        runpy.run_path(SCRIPT, run_name="__main__")
    except SystemExit as exc:
        code = exc.code
        record["system_exit_code"] = code
        if code not in (0, None):
            record["status"] = "TGC_FAILED"
            record["exception"] = f"SystemExit({code!r})"
    except BaseException as exc:  # noqa: BLE001 - record everything
        record["status"] = "TGC_FAILED"
        record["exception"] = f"{type(exc).__name__}: {exc}"
        traceback.print_exc()
    with open(STATUS, "w", encoding="utf-8") as fh:
        json.dump(record, fh, ensure_ascii=False, indent=2)
    return 0 if record["status"] == "TGC_DONE" else 1


if __name__ == "__main__":
    if os.environ.get("TGC_CHILD") == "1":
        sys.exit(child())
    os.makedirs(RUN_DIR, exist_ok=True)
    log_path = os.path.join(RUN_DIR, "run.log")
    env = dict(os.environ, TGC_CHILD="1")
    # Redirect the child's stdout and stderr to the SAME file handle: a single
    # fd for both streams, so order of writes is the order they happened.
    with open(log_path, "wb") as log:
        proc = subprocess.run(
            [sys.executable, os.path.abspath(__file__), SCRIPT, RUN_DIR],
            cwd=RUN_DIR,
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=subprocess.STDOUT,
            env=env,
            check=False,
        )
    print("child_exit_code", proc.returncode)
    print("run_dir", RUN_DIR)
    print("status_file", open(STATUS, encoding="utf-8").read() if os.path.exists(STATUS) else "MISSING")
    print("log_path", log_path)
    for name in sorted(os.listdir(RUN_DIR)):
        p = os.path.join(RUN_DIR, name)
        print("artifact", name, os.path.getsize(p) if os.path.isfile(p) else "<dir>")
