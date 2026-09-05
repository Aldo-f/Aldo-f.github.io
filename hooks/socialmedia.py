"""MkDocs hook: add share buttons to blog posts."""

from textwrap import dedent
import urllib.parse
import re

x_intent = "https://x.com/intent/tweet"
linkedin_sharer = "https://www.linkedin.com/sharing/share-offsite/"
mastodon_sharer = "https://mastodon.social/share"
fb_sharer = "https://www.facebook.com/sharer/sharer.php"
include = re.compile(r"blog/[1-9].*")


def on_page_markdown(markdown, **kwargs):
    page = kwargs['page']
    config = kwargs['config']
    if not include.match(page.url):
        return markdown

    page_url = config.site_url + page.url
    page_title = urllib.parse.quote(page.title + '\n')

    return markdown + dedent(f"""\\
    [Share on :fontawesome-brands-x-twitter:]({x_intent}?text={page_title}&url={page_url}){{ .md-button }}
    [Share on :fontawesome-brands-linkedin:]({linkedin_sharer}?url={page_url}){{ .md-button }}
    [Share on :fontawesome-brands-mastodon:]({mastodon_sharer}?text={page_title}&url={page_url}){{ .md-button }}
    [Share on :fontawesome-brands-facebook:]({fb_sharer}?u={page_url}){{ .md-button }}
    """)