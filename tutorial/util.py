import re
from lxml import html

def extra_channel(url):
    if not url:
        return 'news'
    m = re.match(r'^.+?/(\w+)/.*', url)
    if m:
        return m.group(1)
    else:
        return 'news'

def extra_post_id(url):
    if not url:
        return None
    m = re.match(r'.*\-(\d+)$', url)
    if m:
        return m.group(1)

#remove html tags in body
def extra_content(body):
    return html.fromstring(body).text_content().strip()
