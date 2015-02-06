from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from tutorial import util
from tutorial.items import BroadItem
from scrapy import log

class BroadItemLoader(ItemLoader):
    default_item_class = BroadItem
    default_input_processor = MapCompose(unicode.strip)
    default_output_processor = TakeFirst()

    body_in = MapCompose(util.extra_content)
