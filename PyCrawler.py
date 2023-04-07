from cgitb import text
from itertools import tee
from msilib.schema import Error
from turtle import update
from typing import List
import aiohttp
from htmlParser import PyHtmlParser
import asyncio


baseurl = input("type base url: ")
tasks_limit = 10

redirect_urls = set()
current_list = set()
crawled_list = set()

current_list.add(baseurl)

my_headers = {
  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36",
  "Connection":"close"
}

def get_task_limit(length):
    return length if length < tasks_limit else tasks_limit

def has_redirect_param(url):
    return url.find("redirect")
    

async def request(url):
    crawled_list.add(url)

    if has_redirect_param(url) != -1:
        redirect_urls.add(url)

    if not url.startswith("http"):
        url = "https://" + url

    print(url)
    try:
        async with aiohttp.request('GET',url) as response:
            if response.headers["Content-Type"].split(';')[0] == "text/html":
                text = await response.text()
                urls = PyHtmlParser.parser(baseurl, text)
                for url in urls:
                    current_list.add(url)
    except:
        print("ERROR 404")


async def waitForTaskCompletion(_task_queue):
    for task in _task_queue:
        try:
            await asyncio.wait_for(task, timeout=5)
        except TimeoutError:
            print("sorry! Timeout Error")

        

async def main():
    global urls_count

    while current_list:

        tasks = []

        for i in range(0, get_task_limit(len(current_list))):
            task = asyncio.create_task(request(current_list.pop()))
            tasks.append(task)

        await asyncio.gather(*tasks)

    print(f"we have found {len(crawled_list)} urls")
    print(f"we have found {len(redirect_urls)} redirect param urls")
    
        

    

asyncio.run(main())


    
    
	  
    
