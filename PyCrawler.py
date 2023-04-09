import aiohttp
from UrlFilter import UrlFilter
from htmlParser import PyHtmlParser
import asyncio


def get_task_limit(length):
    return length if length < tasks_limit else tasks_limit
   
def validate_url(url):
    if not url.startswith("http"):
        url = "https://" + url
    return url


baseUrl = input("type base url: ")
baseUrl = validate_url(baseUrl)
tasks_limit = 20
wait = 5

current_list = set()
crawled_list = set()
urlFilter = UrlFilter(baseUrl)

current_list.add(baseUrl)

headers = {
  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.5249.62 Safari/537.36",
  "Connection":"close"
}


async def request(url):
    crawled_list.add(url)

    url = validate_url(url)

    print(url)
    try:
        async with aiohttp.request('GET',url) as response:
            if response.headers["Content-Type"].split(';')[0] == "text/html":
                text = await response.text()
                urls = urlFilter.filter(PyHtmlParser.parse(baseUrl, text))
                for url in urls:
                    current_list.add(url)
    except:
        print("ERROR 404")


async def waitForTaskCompletion(_task_queue, wait):
    for task in _task_queue:
        try:
            await asyncio.wait_for(task, timeout=wait)
        except TimeoutError:
            print("sorry! Timeout Error")

        

async def main():
    global urls_count
    global current_list
    global crawled_list

    tasks = []
    while current_list:
        for _ in range(0, get_task_limit(len(current_list))):
            task = asyncio.create_task(request(current_list.pop()))
            tasks.append(task)

        await waitForTaskCompletion(tasks, wait)
        current_list = current_list.difference(crawled_list)

    print(f"we have found {len(crawled_list)} urls")
    
        

    

asyncio.run(main())


    
    
	  
    
