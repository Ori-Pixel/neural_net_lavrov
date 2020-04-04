import scrapy
from scrapy_splash import SplashRequest
from scrapy.http.request import Request
#from bs4 import BeautifulSoup
import re
from unidecode import unidecode

class First_Spider(scrapy.Spider):
  name = "second"
  allowed_domains = ["mid.ru"]
  start_urls = ["https://www.mid.ru/en/press_service/minister_speeches"]


  def start_requests(self):
      for url in self.start_urls:
          yield SplashRequest(url, self.parse,
              endpoint='render.html',
              args={'wait': 10},
          )

  def parse(self, response):
    blocks = response.xpath('//section[@class="page-block news-articles"]') #with xpath = class page... = blocks
    for a in blocks.xpath('.//a'): #[@class="anons-title"] for all <a> in blocks
        article_url = blocks.xpath('.//a/@href').get()  #article_url = href of a 
        for href in a.xpath('./@href').get(): 
            yield SplashRequest(article_url, callback=self.parse_article_contents, args={'wait': 10}, meta={'item':{
            'Title' : unidecode(a.xpath('./text()').get().strip()), #text of 
            'url' : a.xpath('./@href').get(),
            'articleID' : a.xpath('./@href').get().split("/")[-1]
            }})

    #next_page = response.xpath('//*[@id="_101_INSTANCE_7OvQR5KJWVmR_ocerSearchContainerPageIterator"]/div/div/ul/li[3]/a').get()
    #if next_page is not None:
      #page = response.url.split("/")[-1]
      #filename = page + '.html'
      #with open(filename, 'wb') as f:
          #f.write(response.body)
      #next_page = response.urljoin(next_page)
      #yield SplashRequest(next_page, callback=self.parse)

  def parse_article_contents(self, response):
      item = response.meta['item']
      article_string = ''
      x = ''
      article_body = response.xpath('.//div[@class="text article-content"]/text()').get()
      for span in response.xpath('//span[contains(., "")]/text()').getall():
        span = striphtml(span)
        article_string = article_string + span
      item['ArticleText'] = unidecode(striphtml(article_string)).rstrip('\n').rstrip('\t')
      return item
    
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)



#xpath to next page
#//*[@id="_101_INSTANCE_7OvQR5KJWVmR_ocerSearchContainerPageIterator"]/div/div/ul/li[3]/a