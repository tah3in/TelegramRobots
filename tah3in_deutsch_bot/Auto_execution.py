import time
import subprocess
import os

while True:
    try:
        os.chdir(r"D:\TelegramBot\tah3in_deutsch_bot")
        command = r"python D:\TelegramBot\tah3in_deutsch_bot\tah3in_deutsch_bot.py"
        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except:
        time.sleep(60)



