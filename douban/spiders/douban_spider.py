# -*- coding: utf-8 -*-
import scrapy
from  douban.items import DoubanItem

class DoubanSpiderSpider(scrapy.Spider):

     #爬虫名字
     name = 'douban_spider'

     #允许的域名
     allowed_domains = ['movie.douban.com']

     #入口，扔到调度器
     start_urls = ['https://movie.douban.com/top250']

     def parse(self, response):
         movie_list=response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
         for i_item in movie_list:

             #item文件导入
             douban_item=DoubanItem()
             douban_item['serial_number']=i_item.xpath(".//div[@class='item']//em//text()").extract_first()
             douban_item['movie_name']=i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='hd']//a//span[1]/text()").extract_first()

             #电影介绍数据处理
             content=i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
             for i_content in content:
                 content_s="".join(i_content.split())
                 douban_item['introduce']=content_s

             douban_item['star']=i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//div[@class='star']//span[2]/text()").extract_first()
             douban_item['evaluate']=i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//div[@class='star']//span[4]/text()").extract_first()

             douban_item['describe']=i_item.xpath(".//div[@class='item']//div[@class='info']//div[@class='bd']//p[2]//span//text()").extract_first()

             #将数据yield到pipelines
             yield  douban_item

            # 解析下一页
             # next_link=response.xpath("//div[@class='article']/div[@class='paginator']/span[@class='next']/link/@href").extract()
             # if next_link:
             #     next_link = next_link[0]
             #     yield scrapy.Request('https://movie.douban.com/top250' + next_link, callback=self.parse)

            # scrapy crawl douban_spider


             print(douban_item)