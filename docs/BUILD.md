# راهنمای ساخت ISO

## پیش‌نیازها

- سیستم میزبان Debian/Ubuntu با معماری amd64
- دسترسی اینترنت برای دریافت بسته‌های Debian
- حداقل 25 گیگابایت فضای خالی
- حداقل 4 گیگابایت RAM (۸ گیگابایت یا بیشتر پیشنهاد می‌شود)

## نصب ابزارهای ساخت

```bash
sudo apt update
sudo apt install -y git live-build debootstrap squashfs-tools xorriso
```

## دریافت سورس و ساخت

```bash
git clone https://github.com/moborots/Moborots-Recovery-OS.git
cd Moborots-Recovery-OS
sudo chmod +x boot/build_iso.sh
sudo ./boot/build_iso.sh
```

فایل خروجی مورد انتظار:

```text
output/Moborots-Recovery-OS-amd64.iso
```

## آزمایش در VMware

1. یک ماشین مجازی جدید با نوع Linux و Debian 64-bit بسازید.
2. حداقل 2 هسته CPU و 4 گیگابایت RAM اختصاص دهید.
3. ISO را به CD/DVD مجازی متصل کنید.
4. ماشین مجازی را از ISO بوت کنید.
5. ابتدا نمایش سیستم، فهرست دیسک‌ها و رابط شبکه را آزمایش کنید.

برای آزمایش USB روی کامپیوتر واقعی، ISO را با ابزاری مانند Rufus روی فلش بنویسید. نوشتن ISO روی فلش تمام اطلاعات قبلی آن را پاک می‌کند؛ قبل از ادامه، از فایل‌های فلش نسخه پشتیبان بگیرید.

## نکته مهم

این اسکریپت یک پیکربندی اولیه Debian Live می‌سازد. اولین build ممکن است طول بکشد و به اینترنت و مخازن Debian وابسته است. ISO باید قبل از استفاده واقعی روی VMware و سخت‌افزار واقعی آزمایش شود.
