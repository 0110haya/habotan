import requests
import os.path
import re
import discord
import asyncio
from bs4 import BeautifulSoup
from django.conf import settings

#Botのアクセストークン
TOKEN = settings.bot_TOKEN

#チャンネルID(int)
CHANNEL_ID = settings.CHANNEL_ID

#確認したいコミュニティ
target = "co2517090"

#放送URLから放送ID取得
def getLiveId(liveURL):
    id = re.compile("lv[0-9]+")
    return id.search(liveURL).group()

#放送URLから放送タイトル取得
def getLiveTitle(liveURL):
    r = requests.get(liveURL)
    soup = BeautifulSoup(r.content, "html.parser")
    for meta_tag in soup.find_all("meta", attrs={"property": "og:title"}):
        return meta_tag.get("content")

#放送URLから放送者名取得
def getLiveName(liveURL):
    r = requests.get(liveURL)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup.find("span", {"class":"name"}).text

#接続に必要なオブジェクトを生成
client = discord.Client()

#起動時に動作する処理
@client.event
async def on_ready():
    while(True):
        #URLを設定
        url = requests.get("https://com.nicovideo.jp/community/" + target)

        #コミュニティTOPページを確認
        soup = BeautifulSoup(url.content, "html.parser")
        result = soup.find("section", "now_live")

        #放送が始まっていた時
        if result is not None:
            #放送URL取得
            liveURL = result.find("a", "now_live_inner").get("href")
            #放送タイトル取得
            liveTitle = getLiveTitle(liveURL)
            #放送者名取得
            lineName = getLiveName(liveURL)

            #Discordへ送信
            channel = client.get_channel(CHANNEL_ID)
            await channel.send(liveName + "さんが配信を開始しました\n\n" + liveTitle + "\n" + liveURL)
    await asyncio.sleep(60)

#Discordに接続
client.run(TOKEN)
