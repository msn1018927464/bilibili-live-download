#coding = utf-8
import re
import requests
from bs4 import BeautifulSoup
import wget
from time import gmtime, strftime


'''
#Download Bilibili live

*author: Lo Ben (loben#illimited.cf) //repace # to @* \n
date: 2017-03-04
'''

def get_room_id(url):
    '''
    get_room_id(url)
    url - Bilibili live url
    '''
    url_source_code = requests.get(url)
    room_id_str = re.findall("var.*ROOMID.*=.*", url_source_code.text)
    room_id = "".join(re.findall(r"\d", room_id_str[0]))
    return room_id


def get_live_url_address(live_room_id):
    '''
    get_live_url_address(live_room_id)
    live_room_id - var ROOMID
    '''
    get_playurl = "http://live.bilibili.com/api/playurl?player=1&cid="+live_room_id+"&quality=0"
    playurl_sourcecode = requests.get(get_playurl)
    tmp = BeautifulSoup(playurl_sourcecode.text, 'html.parser')
    live_url = ["", "", "", ""]
    live_url[0] = tmp.url.string
    live_url[1] = tmp.b1url.string
    live_url[2] = tmp.b2url.string
    live_url[3] = tmp.b3url.string
    return live_url

#live_url = get_live_url_address(get_room_id(url))

def get_now_time():
    '''
    ##get_now_time
    *return* now **time**
    '''
    return strftime("%Y-%m-%d_%H%M%S", gmtime())

def get_live_room_info(url):
    '''
    ##get_live_room_info(url)
    GET bilibili room info
    '''
    source_code = requests.get(url)
    website_source_code = BeautifulSoup(source_code.text, 'html.parser')
    title = website_source_code.title.string
    return title

def download_live_video(live_url, url):
    '''
    ##download_live_video()
    '''
    filename = get_live_room_info(url)+"_"+str(get_now_time())+".flv"
    print(filename)
    url = live_url[0]
    wget.download(url, bar=wget.bar_adaptive, out=filename)
    return

def function():
    '''
    功能列表
    '''

    print('''
        Bilibili live download tool \n
        
        作者：Lo Ben (loben#illimited.cf)
        
        有甚麼可以幫到你? \n
        1. 查詢直播影片url \n
        2. 下載直播影片 \n
        3. 查詢直播室的title \n
    ''')
    choose = input(">>>")
    if choose == "1":
        url = input("請輸入bilibili直播網頁： ")
        url_list = get_live_url_address(get_room_id(url))
        for i in range(3):
            print("Url "+str(i)+": "+url_list[i])
    elif choose == "2":
        url = input("請輸入bilibili直播網頁： ")
        print("注意： 如果下載Bilibili直播影片下列的狀態列不會有任何變化喔!")
        live_url = get_live_url_address(get_room_id(url))
        download_live_video(live_url, url)
    elif choose == "3":
        print(get_live_room_info(str(input("輸入直播室url: "))))
    return

function()
