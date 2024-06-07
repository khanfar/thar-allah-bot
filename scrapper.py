from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from configparser import ConfigParser 
from tabulate import tabulate
import csv
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser()
config.read(dir_path+'/config.ini')



api_id =  config['account']['id']       #enter here api_id
api_hash = str(config['account']['hash']) #Enter here api_hash id
phone = str(config['account']['phone'])        #enter here phone number with country code
client = TelegramClient(phone, api_id, api_hash)
async def main():
    # Now you can use all client methods listed below, like for example...
    await client.send_message('me', 'Start scarping groups')
with client:
    client.loop.run_until_complete(main())
client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter verification code: '))


groups=[]
supergroups=[]
finalgroups=[]
flag = False
dialogs=client.iter_dialogs()

for dialog in dialogs:
    try:
        if dialog.is_group and dialog.is_channel:
            supergroups.append(dialog)
        groups.append(dialog)
    except:
        continue


for g in groups:
    for sg in supergroups:
        if (g.title == sg.title and g.id != sg.id):
            print (str(g.id) +" "+str(sg.id))
            continue 
        finalgroups.append(g)
                
finalgroups = list(dict.fromkeys(finalgroups))


print('Saving In file...')
with open(dir_path+"/groups.txt","w",encoding='UTF-8') as f:
    final =[]
    for g in finalgroups:
        final.append([g.title , str(g.id)])
    f.write(tabulate(final))
    print('Groups scraped successfully.......')