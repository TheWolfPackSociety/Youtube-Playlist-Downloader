import bs4 as bs 
from pytube import YouTube
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing.pool import ThreadPool as Pool
import sys
import os
pool_size = 5
pool = Pool(pool_size)
def VideoDownload(d):
    filename=d[0]
    url=d[1]
    filename=filename.replace(" ","_")
    path=os.getcwd()+"\\"+title+"\\"
    try: 
        yt = YouTube(url) 
        video= yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first()
        print(d[0]+" Started Downloading")
        video.download(output_path=path,filename=filename)
        print(d[0]+" Completed")
        return True
    except Exception as e: 
        print("Error with "+filename)
        return False
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
if len(sys.argv)>=2:
    url = sys.argv[len(sys.argv)-1]
else:
    url=input("Enter the URL : ")
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get(url)
time.sleep(2)
req = browser.page_source
browser.close()
os.system("cls")
soup=bs.BeautifulSoup(req,'html.parser')
title=soup.find("h1",{"id":"title"}).text.strip()
bsoup=soup.find("div",id="contents")
videos=bsoup.find_all('a',{"class":"yt-simple-endpoint style-scope ytd-playlist-video-renderer"})
links={}
for video in videos:
    href="http://youtube.com"+video['href']
    name=video.find("h3").text.strip()
    links[name]=href
for item in links.items():
    pool.apply_async(VideoDownload, (item,))
pool.close()
pool.join()