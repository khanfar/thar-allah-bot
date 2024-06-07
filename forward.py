import platform
from telethon.sync import TelegramClient, events
from configparser import ConfigParser
import os
import time
import sys

print()
print(' KHANFAR BOT --- THAR-ALLAH -- BOT ')
print()
print()

dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser()
config.read(dir_path + '/config.ini')

api_id = int(config['account']['id'])
api_hash = str(config['account']['hash'])
phone = str(config['account']['phone'])
client = TelegramClient(phone, api_id, api_hash)

# Add your bot's API credentials
bot_token = '6309058196:AAGaqUW7T3yr-CaM0hMp3BC-yh67HHC3dlQ'
bot_username = 'TharAllahMonitor_bot'  # Replace with your bot's username

# Function to send a message to the specified bot
def send_start_message_to_bot():
    try:
        # Get the entity using the bot's username
        bot_entity = client.get_entity(bot_username)
        
        # Send a message to the bot
        client.send_message(bot_entity, 'Your script is now running.')
    except Exception as e:
        print(f"Failed to send start message to bot: {e}")

# Telegram channels to monitor
channels = [int(x) for x in config['config']['from'].split(",")]

try:
    reciver = int(config['config']['to'])
except:
    reciver = config['config']['to']

def beep_sound():
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(1000, 200)  # Adjust the frequency and duration as needed
    else:
        sys.stdout.write('\a')
        sys.stdout.flush()

post_counter = 0  # Counter for tracking posts

@client.on(events.NewMessage(chats=channels))
def my_event_handler(event):
    global post_counter
    post_counter += 1  # Increment the post counter

    check = False
    try:
        saved_path = event.download_media()
        msg_words = event.text.split()
        msg_display = ' '.join(msg_words[:3])  # Get the first three words of the message
        msg = ' '.join(msg_words)  # Get the entire message for sending
        
        if event.media and hasattr(event.media, 'document') and event.media.document.mime_type == "video/mp4":
            client.send_file(reciver, saved_path, caption=f"🔴 {msg}")
        else:
            client.send_file(reciver, saved_path, caption=f"🔴 \n{msg}")
        
        os.remove(saved_path)
        chatid = event.chat_id
        check = True
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {post_counter}. {str(chatid)}  {event.chat.title} {msg_display}: FILE  -------> FORWARD 🔴")
        beep_sound()
        pass
    except:
        if check:
            chatid = event.chat_id
            sender = event.get_sender()
            check = True
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {post_counter}. {str(chatid)}  {sender.username} {msg_display} : FILE  -------> FORWARD 🔴")
            beep_sound()
        pass

    if not check:
        try:
            client.send_message(reciver, f"🔴 {msg}")
            
            chatid = event.chat_id
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {post_counter}. {str(chatid)}  {event.chat.title} : {msg_display}  -------> FORWARD 🔴")
            beep_sound()
            check = False
            pass
        except:
            sender = event.get_sender()
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {post_counter}. {str(chatid)}  {sender.username} : {msg_display}  -------> FORWARD 🔴")
            beep_sound()
            check = False
            pass

# Run the client and send start message after connecting
with client:
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter verification code: '))
    send_start_message_to_bot()
    client.run_until_disconnected()
