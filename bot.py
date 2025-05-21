import os
import requests
from telegram import Bot
import asyncio
import urllib.parse
import hmac
import base64
import time
import urllib.parse
from hashlib import sha256
from bs4 import BeautifulSoup
from datetime import *
import locale


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_news():
    url = f'https://www.xiberokobotza.org/berriak'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="sppb-addon-wrapper-1573106262965")
    job_elements = results.find_all("div", class_="sppb-addon-article")
    albisteak=[]

  #  print(job_elements)
    for job_element in job_elements:
        albistea=[]
        print(job_element)
        title_element = job_element.find("h3")
        print(title_element)
        desk_element  = job_element.find("div", class_="sppb-article-introtext").text
        print(desk_element)
        data_element  = job_element.find("span", class_="sppb-meta-date")
        print(data_element)
        img_element   = job_element.find_all("img")
        print(img_element[0])
        if len(img_element) == 0:
            img_element   = job_element.find_all("img")
            albistea.append("https://www.xiberokobotza.org/"+img_element[0]['src'])
        else:
            albistea.append("https://www.xiberokobotza.org/"+img_element[0]['src'])
        url_element   = title_element.find(href=True)
        #locale.setlocale(locale.LC_ALL, 'eu_ES') 
        new_datatime = datetime.strptime("2025 May 21", '%Y %B %d')
        #new_datatime = datetime.strptime(data_element.text, '%Y %B %d')
        albistea.append(title_element.text.strip()+ "\n" + url_element['href'])
        albistea.append(new_datatime)
        albisteak.append(albistea)
        
    return albisteak
    

async def send_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def send_photo(photo, caption):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo, caption=caption)

async def main():
    albisteak = get_news()
    gaur = datetime.strftime(datetime.today(), '%Y/%m/%d')
    for albistea in albisteak:
        img = albistea[0]
        irudia=img.split('?')
        title= albistea[1]
        print(gaur)
        print(title)
        caption = f"{title}"
        new_datatime = albistea[2]
        albiste_data = datetime.strftime(new_datatime, '%Y/%m/%d')
        if albiste_data != gaur:
            print(gaur)
            print(albiste_data)
        else:
            await send_photo(irudia[0],caption)
   
if __name__ == '__main__':
    asyncio.run(main())