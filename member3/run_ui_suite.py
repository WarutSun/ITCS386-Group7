"""Run the whole Group 7 UI suite (ST01, ST02, ST03) with one command, from the repo root:

    python member3/run_ui_suite.py            # all UI tests
    python member3/run_ui_suite.py -k st03     # extra pytest options are passed through

Every scenario keeps its own folder and evidence; this script only collects them together.
Environment (same for all scenarios): SHOP_USERNAME, SHOP_PASSWORD (browser login password),
optional BROWSER=edge|chrome, HEADLESS=1. The full pytest output is also written to
member3/ui-suite-<date-time>.txt as run evidence.
"""
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENARIOS = {
    "ST01 product purchase (Member 1)": ROOT / "member1" / "AutomatedUI",
    "ST02 coupon purchase (Member 4)": ROOT / "member4" / "AutomatedUI",
    "ST03 stock and cart validation (Member 3)": ROOT / "member3" / "UI testing",
}


def main():
    paths = []
    for name, path in SCENARIOS.items():
        if path.is_dir():
            paths.append(str(path))
            print(f"[include] {name}: {path.relative_to(ROOT)}")
        else:
            print(f"[missing] {name}: {path.relative_to(ROOT)} not in the repo yet")
    if not paths:
        sys.exit("No UI test folders found.")
    log = Path(__file__).parent / f"ui-suite-{datetime.now():%Y%m%d-%H%M%S}.txt"
    cmd = [sys.executable, "-m", "pytest", "-v", "-rA", *paths, *sys.argv[1:]]
    print("$", " ".join(cmd))
    with log.open("w", encoding="utf-8") as out:
        proc = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            print(line, end="")
            out.write(line)
    print(f"\nFull output saved to {log.relative_to(ROOT)}")
    sys.exit(proc.wait())


if __name__ == "__main__":
    main()
