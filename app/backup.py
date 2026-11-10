"""Basic file/folder copy helper; source data is never intentionally deleted."""
from pathlib import Path
import shutil


def copy_path(source, destination):
    src = Path(source).expanduser().resolve()
    dst_root = Path(destination).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(f"Source does not exist: {src}")
    if not dst_root.is_dir():
        raise NotADirectoryError(f"Destination is not a directory: {dst_root}")
    target = dst_root / src.name
    if src == dst_root or src == target or src in dst_root.parents:
        raise ValueError("Choose a destination outside the source folder.")
    if src.is_dir():
        shutil.copytree(src, target, dirs_exist_ok=True, copy_function=shutil.copy2)
    else:
        shutil.copy2(src, target)
    return f"Copied to: {target}"
