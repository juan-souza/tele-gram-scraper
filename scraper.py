from telethon.sync import TelegramClient, events
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys
import configparser
import csv
import time
import json

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

            version : 3.1
        """)
        
#//////////////////////////////////////////////////////////////////////////////////////////////////            
        
def test():
    txt = "#BAT/BTC (Binance) Buy zone 2.454 - 2.500 Sell zone 2.588 - 2.700 - 2.800"
    print(convertMessage(txt))        
        
#txt = "#BAT/BTC (Binance) Buy zone 2.454 - 2.500 Sell zone 2.588 - 2.700 - 2.800"       
def convertMessage(txt):
    pair=''
    action=''
    buys=[]
    sells=[]
    
    #entra no if se tiver o #... se nao retorna o testo

    for word in txt.split(" "):
         if "#" in word:
            symbol=word.split("/")[0]
            symbol=symbol.replace("#","")
            pair=word.split("/")[1]
         if "(" in word:
            exchange=word
            exchange=exchange.replace("(","")
            exchange=exchange.replace(")","")
         if "Buy" in word:
            action=word
         if "Sell" in word:
            action=word
         if "zone" in word:
            action+=word
         if "Buyzone" in action:
            #buy
            if "-" not in word and "zone" not in word:
                buys.append(word)
         if "Sellzone" in action:
            #sell
            if "-" not in word and "zone" not in word:
                sells.append(word)
                 
    return str({"pair": pair,"symbol": symbol,"exchange":exchange,"buys":buys,"sells":sells })
    
#//////////////////////////////////////////////////////////////////////////////////////////////////    

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
 
os.system('clear')
banner()
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        #if chat.megagroup== True:
        if chat.broadcast== True:
            groups.append(chat)
    except:
        continue
 
#Channel 1
 
print(gr+'[+] Choose a Channel to scrape copy :'+re)
i=0
for g in groups:
    print(gr+'['+cy+str(i)+gr+']'+cy+' - '+ g.title)
    i+=1
 
print('')
g_index = input(gr+"[+] Enter a Number : "+re)
target_group=groups[int(g_index)]
print('')

##Channel 2

print(gr+'[+] Choose a Channel to scrape reply :'+re)
i2=0
for g in groups:
    print(gr+'['+cy+str(i2)+gr+']'+cy+' - '+ g.title)
    i2+=1

print('')
g2_index = input(gr+"[+] Enter a Number : "+re)
target_group2=groups[int(g2_index)]
 
print(gr+'[+] Start Event NewMessage...')

time.sleep(1)

@client.on(events.NewMessage(chats=[target_group]))
async def my_event_handler(event):
    print(event.raw_text)
    #await client.forward_messages(target_group2, event.message)
    await client.send_message(target_group2, convertMessage(event.raw_text))


print(gr+'[+] Run aplication!')

client.run_until_disconnected()
