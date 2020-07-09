from quart import Quart, jsonify, request
# from flask_cors import CORS
import newspaper
from date_guesser import guess_date, Accuracy
from langdetect import detect, detect_langs
import json
import asyncio
import aiohttp
import requests
from requests.exceptions import HTTPError
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('punkt')

# loop = asyncio.get_event_loop()
app = Quart(__name__)
app.config['JSON_SORT_KEYS'] = False
# CORS(app)


@app.route('/', methods=['GET'])
def start():
    return 'Welcome!', 200


finalJSON = []
urls = []


async def main(urls):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(get_article(session, url))
            tasks.append(task)
        await asyncio.wait(tasks)


async def get_article(session, url):
    if url == None:
        return 'url parameter is required', 400

    async with session.get(url) as response:
        content = await response.read()
        article = newspaper.Article(url)
        article.set_html(content)

        if response.status == 200:
            article.parse()
            article_dict = {}
            article_dict['status'] = 'ok'

            article_dict['article'] = {}
            article_dict['article']['source_url'] = article.source_url

            try:
                guess = guess_date(url=url, html=article.html)
                article_dict['article']['published'] = guess.date
                article_dict['article']['published_method_found'] = guess.method
                article_dict['article']['published_guess_accuracy'] = None
                if guess.accuracy is Accuracy.PARTIAL:
                    article_dict['article']['published_guess_accuracy'] = 'partial'
                if guess.accuracy is Accuracy.DATE:
                    article_dict['article']['published_guess_accuracy'] = 'date'
                if guess.accuracy is Accuracy.DATETIME:
                    article_dict['article']['published_guess_accuracy'] = 'datetime'
                if guess.accuracy is Accuracy.NONE:
                    article_dict['article']['published_guess_accuracy'] = None
            except:
                article_dict['article']['published'] = article.publish_date
                article_dict['article']['published_method_found'] = None
                article_dict['article']['published_guess_accuracy'] = None

            article.nlp()

            article_dict['article']['title'] = article.title
            article_dict['article']['summary'] = article.summary
            article_dict['article']['keywords'] = list(article.keywords)
            article_dict['article']['authors'] = list(article.authors)

            sentiString = article.title + article.summary
            analyzer = SentimentIntensityAnalyzer()
            vs = analyzer.polarity_scores(sentiString)

            try:
                title_lang = detect(article.title)
            except:
                title_lang = None

            try:
                text_lang = detect(article.text)
            except:
                text_lang = None

            article_dict['article']['images'] = list(article.images)
            article_dict['article']['top_image'] = article.top_image
            article_dict['article']['meta_image'] = article.meta_img
            article_dict['article']['movies'] = list(article.movies)
            article_dict['article']['meta_keywords'] = list(
                article.meta_keywords)
            article_dict['article']['tags'] = list(article.tags)
            article_dict['article']['meta_description'] = article.meta_description
            article_dict['article']['meta_lang'] = article.meta_lang
            article_dict['article']['title_lang'] = str(title_lang)
            article_dict['article']['text_lang'] = str(text_lang)
            article_dict['article']['meta_favicon'] = article.meta_favicon
            article_dict['article']['url'] = str(url)
            article_dict['article']['positive'] = vs['pos']
            article_dict['article']['neutral'] = vs['neu']
            article_dict['article']['negative'] = vs['neg']
            finalJSON.append(article_dict)
            # return article_dict
            # finalJSON = {**finalJSON, **article_dict}
        else:
            article_dict = {}
            article_dict['status'] = 'error'
            article_dict['article'] = 'An error occured parsing this article'
            # return article_dict
            finalJSON.append(article_dict)


@app.route('/v0/goodvibes/', methods=['GET'])
async def get_reddit_urls():
    try:
        response = requests.get(
            'https://reddit.com/r/UpliftingNews/hot/.json?limit=50', headers={'user-agent': 'Mozilla/5.0'})
        # Access JSON Content
        for url in response.json()['data']['children']:
            urls.append(url['data']['url'])

        await main(urls)

        # loop.run_until_complete(main(urls))
        # loop.close()

        return jsonify(finalJSON), 200
    except Exception as err:
        return str(err), 400


if __name__ == '__main__':
    app.run(debug=True)
