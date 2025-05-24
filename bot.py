import os
import requests
from telegram import Bot
import asyncio
from hashlib import sha256
from bs4 import BeautifulSoup
from datetime import *

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
        data_fomateatuta= date_eu_to_en(data_element.text)
        new_datatime = datetime.strptime(data_fomateatuta, '%Y %B %d')
        albistea.append(title_element.text.strip()+ "\n" +"https://www.xiberokobotza.org/"+ url_element['href'])
        albistea.append(new_datatime)
        albisteak.append(albistea)
        
    return albisteak
    
def date_eu_to_en(date):
    data_list=date.split(" ")
    if data_list[1] == "Urtarrila":
        return data_list[0]+" January "+data_list[2]
    elif data_list[1] == "Otsaila":
        return data_list[0]+" February "+data_list[2]
    elif data_list[1] == "Martxoa":
        return data_list[0]+" March "+data_list[2]
    elif data_list[1] == "Apirila":
        return data_list[0]+" April "+data_list[2]
    elif data_list[1] == "Maiatza":
        return data_list[0]+" May "+data_list[2]
    elif data_list[1] == "Ekaina":
        return data_list[0]+" June "+data_list[2]
    elif data_list[1] == "Uztaila":
        return data_list[0]+" July "+data_list[2]
    elif data_list[1] == "Abuztua":
        return data_list[0]+" August "+data_list[2]
    elif data_list[1] == "Iraila":
        return data_list[0]+" September "+data_list[2]
    elif data_list[1] == "Urria":
        return data_list[0]+" October "+data_list[2]
    elif data_list[1] == "Azaroa":
        return data_list[0]+" November "+data_list[2]
    else:
        return data_list[0]+" December "+data_list[2]
    

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