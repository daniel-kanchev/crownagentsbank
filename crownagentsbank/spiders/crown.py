import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from crownagentsbank.items import Article


class CrownSpider(scrapy.Spider):
    name = 'crown'
    start_urls = ['https://www.crownagentsbank.com/news/']

    def parse(self, response):
        links = response.xpath('//a[@class="elementor-post__read-more"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

        next_page = response.xpath('//a[@class="page-numbers next"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//small/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="entry-content animated fadeIn"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content[3:]).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
