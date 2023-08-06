from logging import getLogger

from newspaper import Article, ArticleException

logger = getLogger(__name__)


def extract_story_article(story):
    try:
        article = Article(story["url"])
        article.download()
        article.parse()
        article.nlp()
    except ArticleException:
        logger.error("failed to extract article for story with id %s",
                     story["id"])

        return None

    return {
        "html": article.html,
        "authors": article.authors,
        "publish_date": article.publish_date,
        "text": article.text,
        "top_image": article.top_image,
        "images": article.images,
        "movies": article.movies,
        "keywords": article.keywords,
        "summary": article.summary
    }
