#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ "$EUID" -ne 0 ]]; then
  echo "Run with sudo: sudo ./boot/build_iso.sh" >&2
  exit 1
fi

for cmd in lb debootstrap mksquashfs xorriso; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Missing build dependency: $cmd" >&2
    echo "Install: live-build debootstrap squashfs-tools xorriso" >&2
    exit 1
  }
done

mkdir -p config/package-lists config/includes.chroot/opt/moborots/app
mkdir -p config/includes.chroot/etc/xdg/autostart output

cp -a app/. config/includes.chroot/opt/moborots/app/
cat > config/includes.chroot/etc/xdg/autostart/moborots.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Moborots Recovery OS
Exec=python3 /opt/moborots/app/main.py
Terminal=false
X-GNOME-Autostart-enabled=true
EOF

lb config \
  --mode debian \
  --distribution trixie \
  --architectures amd64 \
  --binary-images iso-hybrid \
  --archive-areas "main contrib non-free-firmware" \
  --debian-installer false \
  --bootappend-live "boot=live components username=user locales=fa_IR.UTF-8,en_US.UTF-8 keyboard-layouts=us,ir"

lb build

shopt -s nullglob
images=(live-image-amd64.hybrid.iso live-image-amd64.iso)
built=""
for image in "${images[@]}"; do
  if [[ -f "$image" ]]; then
    built="$image"
    break
  fi
done
if [[ -z "$built" ]]; then
  echo "Build finished but expected ISO was not found. Check live-build output." >&2
  exit 1
fi
cp -f "$built" output/Moborots-Recovery-OS-amd64.iso
echo "ISO created: $ROOT/output/Moborots-Recovery-OS-amd64.iso"
