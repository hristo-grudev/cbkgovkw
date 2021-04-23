import scrapy

from scrapy.loader import ItemLoader

from ..items import CbkgovkwItem
from itemloaders.processors import TakeFirst


class CbkgovkwSpider(scrapy.Spider):
	name = 'cbkgovkw'
	start_urls = ['https://www.cbk.gov.kw/ar/cbk-news/announcements-and-press-releases/press-releases/get-list']

	def parse(self, response):
		post_links = response.xpath('//h4/a[@class="title-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="page-item page-next "]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//*[(@id = "cbkMain")]//div//div//p//text()[normalize-space() and not(ancestor::p[@class="media-meta"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date"]/text()').get()

		item = ItemLoader(item=CbkgovkwItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
