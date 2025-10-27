import os
import requests
import urllib.request
from telegram import Bot
import asyncio
from hashlib import sha256
from bs4 import BeautifulSoup
from datetime import *
from mastodon import Mastodon

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
MASTODON_ACCESS_TOKEN = os.getenv('MASTODON_ACCESS_TOKEN')
MASTODON_URL = 'https://mastodon.eus'
tmp_img = '/tmp/image.png'
def get_news():
    albisteak=[]
    url = f'https://xiberokobotza.eus/aktualitatea'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="highlights-content")
    
    left_element = results.find("div", id="left-column")
    albiste1=get_albistea(left_element)
    albisteak.append(albiste1)

    right_element = results.find("div", id="right-column")
    albiste2=get_albistea(right_element)
    albisteak.append(albiste2)
        
    return albisteak

def get_albistea(element):

    albistea=[]
    #print(element)
    albiste1_url=element.find_all("a")[0]['href']
    response1 = requests.get(albiste1_url)
    soup1 = BeautifulSoup(response1.content, "html.parser")
    data = soup1.find("h5",id="egilea-data").text.strip()

    new_datatime = datetime.strptime(data, '%Y/%m/%d %H:%M')

    title_element = soup1.find("h1",id="title")
    news_element = soup1.find("div",id="news")
    img_element   = news_element.find_all("img")
    print(img_element[0])
    if len(img_element) == 0:
        img_element   = soup1.find_all("img")
        albistea.append("https://www.xiberokobotza.eus"+img_element[0]['src'])
    else:
        albistea.append("https://www.xiberokobotza.eus"+img_element[0]['src'])

    albistea.append(title_element.text.strip()+ "\n" +albiste1_url)
    albistea.append(new_datatime)
    return albistea    

async def send_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def send_photo(photo, caption):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    response = await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo, caption=caption)

async def send_mastodon(photo_url, caption):
    Masto_api = Mastodon(
                access_token=MASTODON_ACCESS_TOKEN,
                api_base_url=MASTODON_URL
            )
    
    r = requests.get(photo_url)
    with open(tmp_img,'wb') as f:
        f.write(r.content)
        
    image = Masto_api.media_post(tmp_img, 
                            mime_type ="image/png",
                            description = caption
                            )
    Masto_api.status_post(caption, 
                      media_ids=image["id"],
                      )

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
            await send_mastodon(irudia[0],caption)
   
if __name__ == '__main__':
    asyncio.run(main())
