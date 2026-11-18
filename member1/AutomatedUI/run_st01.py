"""Prompt for the browser password and run ST01 twice, saving full pytest output."""
import getpass
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent

def main():
    env = os.environ.copy()
    env.setdefault("SHOP_USERNAME", "itcs386-g07")
    env.setdefault("BROWSER", "chrome")
    if "--collect-only" not in sys.argv:
        env["SHOP_PASSWORD"] = env.get("SHOP_PASSWORD") or getpass.getpass("Group 7 browser password (hidden): ")
        if not env["SHOP_PASSWORD"]:
            raise SystemExit("A browser password is required.")
    logs = HERE / "run-logs"
    logs.mkdir(exist_ok=True)
    stamp = datetime.now(ZoneInfo("Asia/Bangkok")).strftime("%Y%m%d-%H%M%S")
    log = logs / f"st01-{stamp}.txt"
    cmd = [sys.executable, "-m", "pytest", "-v", "-s", "--tb=short", "-x",
           "test_st01_product_purchase.py", *sys.argv[1:]]
    with log.open("w", encoding="utf-8") as out:
        proc = subprocess.Popen(cmd, cwd=HERE, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in proc.stdout:
            if env.get("SHOP_PASSWORD"):
                line = line.replace(env["SHOP_PASSWORD"], "[REDACTED]")
            print(line, end="", flush=True); out.write(line); out.flush()
        code = proc.wait()
        print(f"Exit code: {code}"); out.write(f"Exit code: {code}\n")
    print(f"Saved log: {log}")
    return code

if __name__ == "__main__":
    raise SystemExit(main())
