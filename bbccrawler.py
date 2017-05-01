
# coding: utf-8

# In[ ]:
import scrapy
from scrapy.spiders import XMLFeedSpider
from bbc_crawler.items import BbcCrawlerItem
from bs4 import BeautifulSoup

class BBCSpider(XMLFeedSpider):
    name = 'testbbc'
    allowed_domains = ['bbc.co.uk', 'bbc.com', 'bbci.co.uk']
    start_urls = ['http://feeds.bbci.co.uk/news/world/rss.xml']
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))

        item = BbcCrawlerItem()
        url = node.xpath('link/text()').extract()
        yield scrapy.Request(url[0], callback=self.parse_news)

    def parse_news(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        #instead of parsing the news, you want to instead gather all articles, pass into the subject verb object finder 
        #after doing so take the subjects and look to see if these subjects fit with any of the categories we have mentioned, if we do we also
        #want to build the relationship between the other subjects and the category so that way in the future if it recognizes these subjects itll automatically categorize it as 
        #being global warming related for example 
        #EXAMPLE: Pass in a article about the ['United States', 'Climate Change'] -> automatically gets associated with climate change, build relationship between US and Climate Change
        #if we see US again, look to see if we have a significant enough sample (or other subjects) that would indicate this is a climate change article even in the absense of
            #climate change. Any time the subject is mentioned in the context of another topic, we want to remove it from this because it isn't special to this.
        #so if we seee US in the context of climate change and then politics, we not only don't add it to plitics, but also remove a point on the US --- Climate Change relationship. 
        #We want to build this as a graph though between US and the other subjects that are frequently seen with it
        words = ["United States", "in US", "by US", "the US", "Trump", "Donald Trump", "Mike Pence", "Inauguration", "inauguration"]
        div_main = soup.find('div', class_="story-body")
        for word in words:
            if word in div_main.get_text():
                print(response.url + " hahaha")