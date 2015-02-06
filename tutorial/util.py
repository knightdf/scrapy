import re
from lxml import html
from scrapy import log


#remove html tags in body
def extra_content(body):
    #remove scripts and css styles
    body = re.sub(r"<script[^>]*?>[\s\S]*?</script>", "", body)
    body = re.sub(r"<style[^>]*?>[\s\S]*?</style>", "", body)
    #remove redundant blanks
    body = re.sub(r"\s+"," ", body)
    #remove html tags
    try:
        return html.fromstring(body).text_content().strip()
    except:
        return None
