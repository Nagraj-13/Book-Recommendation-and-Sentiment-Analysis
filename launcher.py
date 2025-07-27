# launcher.py

import asyncio
import os
import sys
from pathlib import Path

async def run_scripts_in_venv():
    project_root = Path(__file__).parent.resolve()

    # 1) Locate the venv python executable
    venv_dir = project_root / ".venv"
    if os.name == "nt":
        py_exe = venv_dir / "Scripts" / "python.exe"
    else:
        py_exe = venv_dir / "bin" / "python"

    if not py_exe.exists():
        print(f"❌ Could not find Python in {py_exe}")
        sys.exit(1)

    # 2) Define the scripts to run
    scripts = [
        project_root / "dashboard.py",
        project_root / "api_dash.py",
        project_root / "backend" / "main.py",
    ]

    # 3) Spawn them in parallel
    procs = []
    for script in scripts:
        if not script.exists():
            print(f"❌ Script not found: {script}")
            sys.exit(1)
        proc = await asyncio.create_subprocess_exec(
            str(py_exe),
            str(script),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        procs.append((script.name, proc))
        print(f"🚀 Launched {script.name} (PID={proc.pid})")

    # 4) Stream each process’s output
    async def stream(name, stream, is_err=False):
        prefix = f"[{name} {'ERR' if is_err else 'OUT'}]"
        async for line in stream:
            print(f"{prefix} {line.decode().rstrip()}")

    # 5) Kick off readers
    for name, proc in procs:
        asyncio.create_task(stream(name, proc.stdout, is_err=False))
        asyncio.create_task(stream(name, proc.stderr, is_err=True))

    # 6) Wait for all to finish
    await asyncio.gather(*(p.wait() for _, p in procs))
    print("✅ All processes have exited.")

if __name__ == "__main__":
    asyncio.run(run_scripts_in_venv())
