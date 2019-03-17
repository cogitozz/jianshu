# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import ArticleItem

class JianshuSpiderSpider(CrawlSpider):
    name = 'jianshu_spider'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        title = response.xpath("//h1[@class='title']/text()").get()
        avatar = response.xpath("//a[@class='avatar']/img/@src").get()
        author = response.xpath("//span[@class='name']/a/text()").get()
        pub_time = response.xpath("//span[@class='publish-time']/text()").get()
        # https://www.jianshu.com/p/0bf159288503
        # https://www.jianshu.com/p/3a5a54a1ec90?utm_campaign=maleskine&utm_content=note&utm_medium=pc_all_hots&utm_source=recommendation
        url = response.url
        url1 = url.split("?")[0]
        article_id = url1.split('/')[-1]
        content = response.xpath("//div[@class='show-content-free']").get()
        word_count = response.xpath("//span[@class='wordage']/text()").get()
        word_count = int(word_count.split(' ')[1])
        comment_count = response.xpath("//span[@class='comments-count']/text()").get()
        comment_count = int(comment_count.split(' ')[1])
        read_count = response.xpath("//span[@class='views-count']/text()").get()
        read_count = int(read_count.split(' ')[1])
        like_count = response.xpath("//span[@class='likes-count']/text()").get()
        like_count = int(like_count.split(' ')[1])
        subjects = ",".join(response.xpath("//div[@class='include-collection']/a/div/text()").getall())

        item = ArticleItem(
            title=title,
            avatar=avatar,
            author=author,
            pub_time=pub_time,
            origin_url=response.url,
            article_id=article_id,
            content=content,
            word_count=word_count,
            comment_count=comment_count,
            read_count=read_count,
            like_count=like_count,
            subjects=subjects
        )
        yield item




























