import subprocess

def download(download_link):
    # مسیر اجرایی IDM در سیستم
    idm_executable_path = "C:\\Program Files (x86)\\Internet Download Manager\\IDMan.exe"

    try:
        # اجرای IDM با دستور دانلود لینک بدون نمایش صفحه "Start Download"
        subprocess.Popen([idm_executable_path, "/dswait", "/n", "/d", download_link])
        print(f"دانلود لینک '{download_link}' با IDM آغاز شد.")
    except Exception as e:
        print("خطا در دانلود با IDM:", str(e))
