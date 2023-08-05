try:
    from newspaper import Article
except:
    print("Requires newspaper3k http://github.com/codelucas/newspaper")


def get_article_info(url):
    """ Takes a media article URL and returns the details scrapped using newspaper3k."""

    article = Article(url, keep_article_html=True)
    article.download()
    article.parse()

    article_details = {
        "title": article.title,
        "text": article.text,
        "url": article.url,
        "authors": article.authors,
        "html": article.article_html,
        "date": article.publish_date,
    }
    for key in article.meta_data:
        article_details[key.replace(".", "_")] = article.meta_data[key]

    return article_details
