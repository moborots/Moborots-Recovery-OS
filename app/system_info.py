"""Safe, read-only system information helpers."""
import platform
import shutil
import subprocess


def _run(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=8, check=False)
        return result.stdout.strip() or result.stderr.strip() or "(no output)"
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"Unavailable: {exc}"


def collect_system_info():
    lines = [
        "MOBOROTS RECOVERY OS",
        "=" * 34,
        f"Operating system: {platform.platform()}",
        f"Kernel: {platform.release()}",
        f"Architecture: {platform.machine()}",
        f"Hostname: {platform.node()}",
        f"Python: {platform.python_version()}",
        "",
        "CPU:",
        _run(["sh", "-c", "grep -m1 'model name' /proc/cpuinfo | cut -d: -f2-"]),
        "",
        "Memory:",
        _run(["sh", "-c", "free -h"]),
        "",
        "Filesystem usage:",
        _run(["df", "-h", "-x", "tmpfs", "-x", "devtmpfs"]),
        "",
        "Network interfaces:",
        _run(["ip", "-brief", "address"]),
    ]
    return "\n".join(lines)
