import scrapy
from scrapy_splash import SplashRequest
from scrapy.http.request import Request
#from bs4 import BeautifulSoup
import re
from unidecode import unidecode

class First_Spider(scrapy.Spider):
  name = "first"
  allowed_domains = ["mid.ru"]
  start_urls = [
        "https://www.mid.ru/en/press_service/minister_speeches?p_p_id=101_INSTANCE_7OvQR5KJWVmR&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_pos=1&p_p_col_count=2&_101_INSTANCE_7OvQR5KJWVmR_delta=10&_101_INSTANCE_7OvQR5KJWVmR_keywords=&_101_INSTANCE_7OvQR5KJWVmR_advancedSearch=false&_101_INSTANCE_7OvQR5KJWVmR_andOperator=true&p_r_p_564233524_resetCur=false&_101_INSTANCE_7OvQR5KJWVmR_cur=%s" % page for page in range(1, 359)
        ]


  def start_requests(self):
      for url in self.start_urls:
          yield SplashRequest(url, self.parse,
              endpoint='render.html',
              args={'wait': 20},
          )

  def parse(self, response):
    blocks = response.xpath('//section[@class="page-block news-articles"]') #with xpath = class page... = blocks
    links = blocks.xpath("//*[contains(@class, 'anons-title')]")
    #for links in blocks.xpath("//*[contains(@class, 'anons-title')]"): #[@class="anons-title"] for all <a> in blocks 
    url_addresses = links.xpath('./@href').getall() #get all url addresses into list
    for i in range(0, len(url_addresses)):
      yield SplashRequest(url_addresses[i], callback=self.parse_article_contents, args={'wait': 10}, meta={'item':{
        }})

  def parse_article_contents(self, response):
      item = response.meta['item']
      article_string = ''
      x = ''5
      article_body = response.xpath('.//div[@class="text article-content"]/text()').get()
      article_title_list = response.xpath('.//div[@class="article article-part article-country     "]/h1/text()').getall()
      article_title = article_title_list[0]
      span = response.xpath('//span[contains(., "")]/text()').getall() #span = every <span> tag in article content space
      span = " ".join(str(v) for v in span) #combine the returned getall list into a single string
      #operations go here to remove unwanted list items?
      span = striphtml(span) #clean html tags if any
      span = span.replace('\n', '') #remove newline in string
      span = span.replace('\t', '') #remove hgorizontal tab in string
      span = span.replace('\r', '') #remove carriage return in string
      span = unidecode(span) #convert unicode substring characters
      item['Title'] = unidecode(article_title).strip()
      item['articleID'] = response.request._original_url.split("/")[-1]
      item['article_URL'] = response.request._original_url
      item['ArticleText'] = span #unidecode(striphtml(article_string)).rstrip('\n').rstrip('\t')
      return item

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)
