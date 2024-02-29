import telebot
import pyautogui
from io import BytesIO
from pathlib import Path
import random
import time
import os

# Replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token
BOT_TOKEN = ...
# Initialize the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

mode = None
line_number_founded = None
WordOrSentence = None
target_word = ''
# Handle text messages

def inial_value():
    global mode , line_number_founded , WordOrSentence 
    line_number_founded = WordOrSentence = mode =None 

def replace_line_in_file(file_path, line_number, new_line):
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    # Replace the line at the specified line number with the new line
    lines[line_number-1] = new_line + '\n'  # Adjust index since line numbers start from 1

    with open(file_path, 'w', encoding="utf-8") as file:
        file.writelines(lines)

def AvoidRepetition(data,text):
    lines = []
    for line in data:
        if '\n' in line:
            line = line.replace('\n','')
        lines.append(line)
    if text not in lines:
        return True
    else:
        return False

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    global line_number_founded ,WordOrSentence , mode , target_word
    chat_id = message.chat.id
    text = message.text
    command = text[-2:]

#____________________________________________________________________________________________________________
# To see the instructions and exit of any mode
    text_lower = text.lower()
    if text_lower == 'start' or text_lower == 'exit'or text_lower == '/exit' or text_lower == '/start':
        bot.reply_to(message, f"/AddW\n/AddS\n/AddN\n/DisplayW\n/DisplayS\n/DisplayN\n/DisplayAutoW\n/DisplayAutoS\n/Edit\n/help\n/Exit")
        inial_value()

#____________________________________________________________________________________________________________
# Adding data in offline mode, in addition, with this method, you can save information faster
        
    elif command == '/S': #Add to sentences
        text = text[:-2]
        with open("Sentencelist.txt",'r+',encoding='utf-8') as Sentencelist:
            data = Sentencelist.readlines()
            if AvoidRepetition(data,text):
                Sentencelist.write(f"{text}\n")
                bot.send_message(chat_id, f"\"{text}\" Added to Sentencelist")
            else :
                bot.send_message(chat_id, f"This sentence has already existed")

    elif command == '/W': #Add to Words
        text = text[:-2]
        with open("Wordlist.txt",'r+',encoding='utf-8') as Wordlist:
            data = Wordlist.readlines()
            if AvoidRepetition(data,text):
                Wordlist.write(f"{text}\n")
                bot.send_message(chat_id, f"\"{text}\" Added to Wordlist")
            else :
                bot.send_message(chat_id, f"This Word has already existed")

    elif command == '/N': #Add to Notes
        text = text[:-2]
        with open("Note.txt",'r+',encoding='utf-8') as Sentencelist:
            data = Sentencelist.readlines()
            if AvoidRepetition(data,text):
                Sentencelist.write(f"{text}\n")
                bot.send_message(chat_id, f"\"{text}\" Added to Note")
            else :
                bot.send_message(chat_id, f"This Note has already existed")
#____________________________________________________________________________________________________________
# Edit mode
    elif text_lower == "/edit" or mode == "edit":
        if text_lower == '/edit':
            mode = "edit"
            bot.reply_to(message, f"Wrong word or sentence :")

        elif mode == "edit" and line_number_founded != None:
            if WordOrSentence == "Word" :
                replace_line_in_file('Wordlist.txt',line_number_founded,text)
                bot.send_message(chat_id, f"{target_word} to {text} was Edited")
            elif WordOrSentence == "Sentence" :
                replace_line_in_file('Sentencelist.txt',line_number_founded,text)
                bot.send_message(chat_id, f"{target_word} to {text} was Edited")
            inial_value()

        elif mode == "edit" :
            target_word = text
            words2 = []
            words = []
            with open('Wordlist.txt', 'r', encoding="utf-8") as Wordlist:
                for line_number, line in enumerate(Wordlist, start=1):
                    words.append(line.strip())  # Split the line into words
                try:
                    line_number_founded = words.index(target_word)+1
                    bot.reply_to(message,f"Found '{target_word}' in line {line_number_founded} of {'Wordlist'} file ")
                    WordOrSentence = "Word"
                    bot.reply_to(message, f"Correct word or sentence :")
                except:
                    with open('Sentencelist.txt', 'r', encoding="utf-8") as Sentencelist:
                        for line_number, line in enumerate(Sentencelist, start=1):
                            words2.append(line.strip())   # Split the line into words
                        try:
                            line_number_founded = words2.index(target_word)+1
                            bot.reply_to(message,f"Found '{target_word}' in line {line_number_founded} of {'Sentencelist'} file ")
                            WordOrSentence = "Sentence"
                            bot.reply_to(message, f"Correct word or sentence :")
                        except:
                            bot.reply_to(message,f"Not Founded '{target_word}'")
#____________________________________________________________________________________________________________
#Add Word to Wordlist.txt
    elif text == "/AddW" or mode=="AddW" :
        # user_modes[chat_id] = 'get_link'
        if text=="/AddW":
            bot.send_message(chat_id, "Now, Please Enter New Word:")
            mode = "AddW"

        elif mode=="AddW":
            with open("Wordlist.txt",'r+',encoding='utf-8') as Wordlist:
                data = Wordlist.readlines()
                if AvoidRepetition(data,text):
                    Wordlist.write(f"{text}\n")
                    bot.send_message(chat_id, f"\"{text}\" Added to Wordlist")
                else :
                    bot.send_message(chat_id, f"This Word has already existed")

#____________________________________________________________________________________________________________
#Add Sentence to Sentencelist.txt
        
    elif text == "/AddS" or mode=="AddS" :
        # user_modes[chat_id] = 'get_link'
        if text=="/AddS":
            bot.send_message(chat_id, "Now, Please Enter New Sentence:")
            mode = "AddS"

        elif mode=="AddS":
            with open("Sentencelist.txt",'r+',encoding='utf-8') as Sentencelist:
                data = Sentencelist.readlines()
                if AvoidRepetition(data,text):
                    Sentencelist.write(f"{text}\n")
                    bot.send_message(chat_id, f"\"{text}\" Added to Sentencelist")
                else :
                    bot.send_message(chat_id, f"This sentence has already existed")
#____________________________________________________________________________________________________________
#Add Note to Notelist.txt
    elif text == "/AddN" or mode=="AddN" :
        # user_modes[chat_id] = 'get_link'
        if text=="/AddN":
            bot.send_message(chat_id, "Now, Please Enter New Note:")
            mode = "AddN"

        elif mode=="AddN":
            with open("Note.txt",'r+',encoding='utf-8') as Sentencelist:
                data = Sentencelist.readlines()
                if AvoidRepetition(data,text):
                    Sentencelist.write(f"{text}\n")
                    bot.send_message(chat_id, f"\"{text}\" Added to Note")
                else :
                    bot.send_message(chat_id, f"This Note has already existed")
#____________________________________________________________________________________________________________
# Dislplay Word of Wordlist.txt (The next word is displayed when a message is sent from the user)
    elif text == "/DisplayW" or mode=="DisplayW":
        mode = "DisplayW"
        file = open('Wordlist.txt', 'r', encoding="utf-8")
        lines = file.readlines()
        if lines:
            random_line = random.choice(lines)
            bot.send_message(chat_id, random_line.strip())

#____________________________________________________________________________________________________________
# Dislplay Sentence of Sentencelist.txt (The next sentence is displayed when a message is sent from the user)

    elif text == "/DisplayS" or mode=="DisplayS":
        mode = "DisplayS"
        file = open('Sentencelist.txt', 'r', encoding="utf-8")
        lines = file.readlines()
        if lines:
            random_line = random.choice(lines)
            bot.send_message(chat_id, random_line.strip())
#____________________________________________________________________________________________________________
# Dislplay Word of Wordlist.txt 
# Automatically displays a Word every 5 seconds. The number of repetitions is 20 by default
# The user can change the number of times by putting the number in front of the command Like /DisplayAutoW 50  
    elif "/DisplayAutoW" in text:
        try:
            command , count = text.split()
            count = int(count)
            bot.send_message(chat_id, f"It started with {count} words ...")
        except:
            count = 20
            bot.send_message(chat_id, "It started with 20 words")
        with open('Wordlist.txt', 'r', encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                for i in range(count):
                    random_line = random.choice(lines)
                    bot.send_message(chat_id, random_line.strip())
                    time.sleep(5)
                bot.send_message(chat_id, "_______________________")

#____________________________________________________________________________________________________________
# Display Sentence of  sentencelist.txt
# Automatically displays a sentence every 10 seconds. The number of repetitions is 20 by default
# The user can change the number of times by putting the number in front of the command Like /DisplayAutoS 50             
    elif "/DisplayAutoS" in text:
        try:
            command , count = text.split()
            count = int(count)
            bot.send_message(chat_id, f"It started with {count} sentences ...")
        except:
            count = 20
            bot.send_message(chat_id, "It started with 20 sentences ...")
        with open('Sentencelist.txt', 'r', encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                for i in range(count):
                    random_line = random.choice(lines)
                    bot.send_message(chat_id, random_line.strip())
                    time.sleep(10)
                bot.send_message(chat_id, "_______________________")
#____________________________________________________________________________________________________________
# Dislplay Note of Note.txt (The next Note is displayed when a message is sent from the user)
    elif "/DisplayN" in text:
        try:
            command , count = text.split()
            count = int(count)
            bot.send_message(chat_id, f"The display of {count}  note has started ...")
        except:
            count = 20
            bot.send_message(chat_id, "The display of 20 note has started ...")
        with open('Note.txt', 'r', encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                for i in range(count):
                    random_line = random.choice(lines)
                    bot.send_message(chat_id, random_line.strip())
                    time.sleep(10)
                bot.send_message(chat_id, "_______________________")

    elif "/help" in text_lower:
        bot.send_message(chat_id, "Add Word to Wordlist\n"
                            "/AddW"
                            "\n\nAdd Sentence to Sentencelist\n"
                            "/AddS"
                            "\n\nAdd Note to Notelist\n"
                            "/AddN"
                            "\n\nDislplay Word of Wordlist (The next Word is displayed when a message is sent from you)\n"
                            "/DisplayW"
                            "\n\nDislplay Sentence of Sentencelist (The next sentence is displayed when a message is sent from you)\n"
                            "/DisplayS"
                            "\n\nDisplay Notelist (The next Note is displayed when a message is sent from you)\n"
                            "/DisplayN"
                            "\n\n"
                            "Dislplay Word of Wordlist.txt \n"
                            "Automatically displays a Word every 5 seconds. The number of repetitions is 20 by default \n"
                            "You can change the number of times by putting the number in front of the command Like /DisplayAutoW 50 \n"
                            "/DisplayAutoW"
                            "\n\n"
                            "Display Sentence of  sentencelist.txt\n"
                            "Automatically displays a sentence every 10 seconds. The number of repetitions is 20 by default\n"
                            "You can change the number of times by putting the number in front of the command Like /DisplayAutoS 50\n"
                            "/DisplayAutoS"
                            "\n\nEdit mode\n"
                            "/Edit"
                            "\n\nTo Exit\n"
                            "/Exit\n\n")
        bot.send_message(chat_id, "اضافه کردن کلمه\n"
                            "/AddW"
                             "\n\nافزودن جمله به لیست جمله ها\n"
                             "/AddS"
                             "\n\nافزودن نکته به لیست نکات\n"
                             "/AddN"
                             "\n\n# نمایش کلمه از لیست کلمه ها (کلمه بعدی وقتی پیامی از شما ارسال می شود نمایش داده می شود)\n"
                             "/DisplayW"
                             "\n\nنمایش جمله از لیست جملات (جمله بعدی هنگامی که پیامی از شما ارسال می شود نمایش داده می شود)\n"
                             "/DisplayS"
                             "\n\nنمایش نکات از لیست نکات (نکته بعدی هنگامی که پیامی از شما ارسال می شود نمایش داده می شود)\n"
                             "/DisplayN"
                             "\n\n"
                             "نمایش کلمه از لیست کلمه ها \n"
                             "به طور خودکار یک کلمه را هر 5 ثانیه نمایش می دهد. تعداد تکرارها به طور پیش فرض 20 است \n"
                             "کاربر می تواند تعداد دفعات را با قرار دادن عدد مقابل دستور تغییر دهد."
                             "/DisplayAutoW"
                             "\n\n"
                             "نمایش جمله sentencelist.txt\n"
                             "به طور خودکار یک جمله را هر 10 ثانیه نمایش می دهد. تعداد تکرارها به طور پیش فرض 20 است\n"
                             "کاربر می تواند تعداد دفعات را با قرار دادن عدد مقابل دستور تغییر دهد."
                             "/DisplayAutoS"
                             "\n\nحالت ویرایش\n"
                             "/Edit"
                             "\n\nبرای خروج\n"
                             "/Exit\n\n")
    else:
        bot.send_message(chat_id, "I don't understand your command, if you need help, use the /help command")

#____________________________________________________________________________________________________________

# Start the bot and keep it running
bot.polling()
