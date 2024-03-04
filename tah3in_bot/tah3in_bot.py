import telebot
import pyautogui
from Open_IDM import download
from io import BytesIO
from pathlib import Path
import os
import subprocess

# Replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token
BOT_TOKEN = ...
# Initialize the Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Dictionary to store user states
user_states = {}
global first_time
first_time = True
# Handle the '/start' command

def Users_desktop_address():
    os.chdir(r"C:\Users")
    list_dir = []
    for i in os.listdir():
        if Path(r"C:\Users\\" + i).is_dir():
            try:
                os.chdir(r"C:\\Users\\{0}\\Desktop\\".format(i))
                list_dir.append(os.getcwd() + "\\")
            except:
                continue

    return list_dir

global gl_username
# Define a dictionary to store usernames and passwords (replace with your actual credentials)
user_credentials = {
    "user1": "123456",
    "user2": "password2",
    # Add more usernames and passwords as needed
}
Owner_ids=[413047741]



@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id in Owner_ids:
        bot.reply_to(message, f"Hello {gl_username}, please give an order.\n\n/start\n\n/screenshot\n\n/download\n\n/send_text\n\n/get_text")
        user_states[message.chat.id] = 'waiting_for_command'
    else:
        bot.reply_to(message, "Hello! Please Enter your username:")
        # Set the user's initial state to 'waiting_for_username'
        user_states[message.chat.id] = 'waiting_for_username'


@bot.message_handler(commands=['deutsch_bot'])
def start(message):
    command = r"python D:\TelegramBot\deutsch_bot\Auto_execution.py"
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

@bot.message_handler(commands=['Shutdown'])
def start(message):
    user_id = message.from_user.id
    if user_id in Owner_ids:
        os.system("shutdown /s /t 0")
        bot.reply_to(message, f"GoodBye...")
    else:
        bot.reply_to(message, f"You can't turn me off :D")


# Handle text messages
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    chat_id = message.chat.id
    # Check the user's current state
    if chat_id in user_states:
        current_state = user_states[chat_id]

        if current_state == 'waiting_for_username':
            username = message.text

            if username in user_credentials:
                # Valid username, prompt for password
                bot.reply_to(message, "Please enter your password:")
                user_states[chat_id] = 'waiting_for_password'
                user_states[f"{chat_id}" + "_username"] = username
            else:
                # Invalid username
                bot.reply_to(message, "Invalid username. Please try again.")

        elif current_state == 'waiting_for_password':
            password = message.text
            username = user_states[f"{chat_id}" + "_username"]
            if user_credentials.get(username) == password:
                user_id = message.from_user.id
                if user_id not in Owner_ids:
                    Owner_ids.append(user_id)
                    bot.send_message(chat_id,f"Your ID ({user_id}) has been added to the list.")
                # Valid password
                global gl_username
                gl_username = username
                bot.reply_to(message, f"Hello {username}, please give an order\n\n/start\n\n/screenshot\n\n/download\n\n/send_text\n\n/get_text")
                user_states[message.chat.id] = 'waiting_for_command'
            else:
                # Invalid password
                bot.reply_to(message, "Invalid password. Please try again.")

        elif current_state == 'waiting_for_send_text':
            message = message.text
            list_dir = Users_desktop_address()
            for i in list_dir:
                user = i.split("\\",3)[2]
                try:
                    os.chdir(i)
                    txt_file_path = os.path.join(i, "inbox.txt")

                    # Check if the script has write permissions in the directory
                    if os.access(i, os.W_OK):
                        with open(txt_file_path, "w+") as txt_file:
                            txt_file.write(message)
                        bot.send_message(chat_id, f"Sent to User :{user}")
                    else:
                        print(f"No write permission in {i}. Skipping.")
                except Exception as e:
                    print(f"Error writing to {i}: {str(e)}")


        elif current_state == 'waiting_for_command':
            # Process the user's command
            user_command = message.text
            bot.send_message(chat_id, f"You entered the command: {user_command}")

            # Reset the user's state (you can set it to something else)
            if message.text == "/download":
                user_states[chat_id] = 'get_link'
                bot.send_message(chat_id, "Now, please enter a link:")
            elif message.text == "/screenshot":
                screenshot = pyautogui.screenshot()
                # Convert the screenshot to bytes with JPEG format and quality 95 (you can adjust the quality as needed)
                img_bytes = BytesIO()
                screenshot.save(img_bytes, format='JPEG', quality=95)
                img_bytes.seek(0)
                # Create a file with a custom filename and send it as a document
                with open('screenshot.jpg', 'wb') as f:
                    f.write(img_bytes.read())
                    bot.send_document(message.chat.id, open('screenshot.jpg', 'rb'))
            elif message.text == "/send_text":
                user_states[chat_id] = 'waiting_for_send_text'
                bot.send_message(chat_id, "Now, please enter text:")

            elif message.text == "/get_text":
                user_states[chat_id] = 'waiting_for_get_text'
                get_text(chat_id)

            else:
                bot.send_message(chat_id, "You are no longer in a specific state.")

        elif current_state == 'get_link':
            user_states[chat_id] = "get_link"
            download(message.text)
            bot.reply_to(message, f"Your link: \n {message.text} \nDownloading...")

    else:
        bot.send_message(chat_id, "I don't know what you want. Please start with /start.")

def get_text(chat_id):
    list_dir = Users_desktop_address()
    for i in list_dir:
        user = i.split("\\",3)[2]
        try:
            os.chdir(i)
            txt_file_path = os.path.join(i, "inbox.txt")

            # Check if the script has write permissions in the directory
            if os.access(i, os.W_OK):
                txt_inbox = open(txt_file_path, "r")
                text=txt_inbox.read()
                bot.send_message(chat_id, f"Taking from the user :{user}")
                bot.send_message(chat_id, f"{text}")
            else:
                print(f"No read permission in {i}. Skipping.")
        except Exception as e:
            print(f"Error reading to {i}: {str(e)}")

# Start the bot and keep it running
bot.polling()
