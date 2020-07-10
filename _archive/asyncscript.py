# ---------------------------------------------------------------- #

import hashlib
import newspaper
import aiohttp
import asyncio
import time
print("Aynchronous")

urls = [
    'http://www.baltimorenews.net/index.php/sid/234363921',
    'http://www.baltimorenews.net/index.php/sid/234323971',
    'http://www.atlantanews.net/index.php/sid/234323891',
    'http://www.wpbf.com/news/funeral-held-for-gabby-desouza/33874572',
    'http://www.tennessean.com/story/news/politics/2015/06/30/obama-focus-future-health-care-burwell-says/29540753/',
    'http://www.atlantanews.net/index.php/sid/234323901',
    'http://www.baltimorenews.net/index.php/sid/234323975',
    'http://www.utsandiego.com/news/2015/jun/30/backcountry-lilac-development-opposition-general/',
    'http://www.newsnet5.com/newsy/apples-ebook-pricing-scandal-a-long-road-to-a-small-fine',
    'http://www.baltimorenews.net/index.php/sid/234323977',
    'http://www.wsmv.com/story/29447077/trying-to-make-hitting-skid-disappear-maddon-hires-magician',
    'http://www.atlantanews.net/index.php/sid/234323913',
    'http://www.baltimorenews.net/index.php/sid/234323979',
    'http://www.newsleader.com/story/sports/2015/06/30/virginia-baseball-fan-happy-proven-wrong/29540965/',
    'http://www.baltimorenews.net/index.php/sid/234323981',
    'http://www.baltimorenews.net/index.php/sid/234323987',
    'http://www.mcall.com/entertainment/dining/mc-fratzolas-pizzeria-bethlehem-review-20150630-story.html',
    'http://www.atlantanews.net/index.php/sid/234323911',
    'http://www.baltimorenews.net/index.php/sid/234323985',
    'http://www.atlantanews.net/index.php/sid/234323887',
    'http://wtvr.com/2015/06/30/man-who-vandalized-confederate-statue-deeply-regrets-actions/',
    'http://www.baltimorenews.net/index.php/sid/234323923',
    'http://www.witn.com/home/headlines/Goldsboro-teens-charged-with-shooting-into-home-311067541.html',
    'http://www.atlantanews.net/index.php/sid/234323995'
]

start_time = time.time()

finalJSON = []


async def get_article(session, url):
    print(url)

    async with session.get(url) as response:
        content = await response.read()
        article = newspaper.Article(url)
        article.set_html(content)
        try:
            article.parse()
        except newspaper.article.ArticleException:
            return

        # with open(hashlib.md5(url.encode('utf-8')).hexdigest() + ".txt", "w") as f:
        #     f.write(article.text)
        finalJSON.append(article.text)


async def main(urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(get_article(session, url))
            tasks.append(task)
        await asyncio.gather(*tasks)

    return finalJSON

loop = asyncio.get_event_loop()
loop.run_until_complete(main(urls))
loop.close()

print("finalJSON", finalJSON, "\n")
print("async", time.time() - start_time, "\n")
