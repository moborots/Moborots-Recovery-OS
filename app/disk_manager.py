"""Read-only disk inventory. No partition or filesystem write operations."""
import json
import subprocess


def collect_disk_info():
    try:
        result = subprocess.run(
            ["lsblk", "--json", "--bytes", "--output", "NAME,PATH,SIZE,TYPE,FSTYPE,LABEL,MOUNTPOINT,MODEL,RO"],
            capture_output=True, text=True, timeout=10, check=True
        )
        data = json.loads(result.stdout)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        return f"Could not read block-device information: {exc}"

    lines = ["DISK AND PARTITION INVENTORY", "=" * 34]

    def add_devices(devices, depth=0):
        for item in devices:
            indent = "  " * depth
            size = int(item.get("size") or 0)
            gib = size / (1024 ** 3)
            lines.append(
                f"{indent}{item.get('path') or item.get('name')}  "
                f"{gib:.2f} GiB  [{item.get('type', 'unknown')}]"
            )
            details = []
            for key, label in (("model", "Model"), ("fstype", "FS"), ("label", "Label"), ("mountpoint", "Mount"), ("ro", "Read-only")):
                if item.get(key) not in (None, ""):
                    details.append(f"{label}: {item[key]}")
            if details:
                lines.append(f"{indent}  " + " | ".join(details))
            add_devices(item.get("children") or [], depth + 1)

    add_devices(data.get("blockdevices") or [])
    lines += ["", "SMART health (if smartctl is installed):"]
    try:
        smart = subprocess.run(["smartctl", "--scan"], capture_output=True, text=True, timeout=8, check=False)
        lines.append(smart.stdout.strip() or smart.stderr.strip() or "No SMART devices reported.")
        lines.append("For detailed device health, use smartctl -H on a selected device.")
    except (OSError, subprocess.TimeoutExpired):
        lines.append("smartctl is not available.")
    return "\n".join(lines)
