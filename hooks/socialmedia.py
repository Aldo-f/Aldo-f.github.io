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

    icon_x = "{:fontawesome-brands-x-twitter:}"
    icon_linkedin = "{:fontawesome-brands-linkedin:}"
    icon_mastodon = "{:fontawesome-brands-mastodon:}"
    icon_facebook = "{:fontawesome-brands-facebook:}"

    html = f"""\
    <p style="margin-top:1em;padding-top:.5em;border-top:1px solid var(--md-default-fg-color--lightest)">
      <a href="{x_intent}?text={page_title}&url={page_url}" target="_blank" rel="noopener" title="Share on X" style="margin-right:.5em;text-decoration:none">{icon_x}</a>
      <a href="{linkedin_sharer}?url={page_url}" target="_blank" rel="noopener" title="Share on LinkedIn" style="margin-right:.5em;text-decoration:none">{icon_linkedin}</a>
      <a href="{mastodon_sharer}?text={page_title}&url={page_url}" target="_blank" rel="noopener" title="Share on Mastodon" style="margin-right:.5em;text-decoration:none">{icon_mastodon}</a>
      <a href="{fb_sharer}?u={page_url}" target="_blank" rel="noopener" title="Share on Facebook" style="margin-right:.5em;text-decoration:none">{icon_facebook}</a>
    </p>
    """
    return markdown + dedent(html)
