from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from tutorial import util
from tutorial.items import BroadItem
from scrapy import log

class BBCItemLoader(ItemLoader):
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()

    content_in = MapCompose(util.extra_content)
    content_out = Join(separator=u'\r\n')
    channel_in = MapCompose(util.extra_channel)
    postId_in = MapCompose(util.extra_post_id)

class BroadItemLoader(ItemLoader):
    default_item_class = BroadItem
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()

    body_in = MapCompose(util.extra_content)
