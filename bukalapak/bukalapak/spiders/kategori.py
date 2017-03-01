import scrapy
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapy.http import TextResponse
from scrapy.http import Request
# from tokorobet.items import tcategory
# from impala.dbapi import connect
import traceback
import MySQLdb

import time


class ProductSpider(scrapy.Spider):
    name = "kategori"
    allowed_domains = ["https://bukalapak.com"]
    start_urls = ["https://www.bukalapak.com/products"]

    def __init__(self,conn):
        self.conn = conn
        # path_to_chromedriver = 'D://chromedriver'
        # self.driver = webdriver.Chrome(executable_path = path_to_chromedriver)
        self.driver = webdriver.PhantomJS()
    @classmethod
    def from_crawler(cls,crawler):
        conn=MySQLdb.connect(
            host=crawler.settings['MYSQL_HOST'],
            port=crawler.settings['MYSQL_PORT'],
            user=crawler.settings['MYSQL_USER'],
            passwd=crawler.settings['MYSQL_PASS'],
            db=crawler.settings['MYSQL_DB'])
        return cls(conn)

    def parse(self, response):
        cur = self.conn.cursor()
        url = 'https://www.bukalapak.com/products'
        try:
            # import pdb;pdb.set_trace()
            self.driver.get(url)
        except:
            print traceback.print_exc()
        for tidur in range(0, 100):
            time.sleep(1)
            try:
                for kat in range(0,20):
                    response = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
                    url = response.xpath('/html/body/div[1]/section/div/nav/div/div/div/ul/li['+str(kat+1)+']/a/@href').extract_first()
                    url = "https://bukalapak.com" + url
                    nama_kategori = response.xpath('/html/body/div[1]/section/div/nav/div/div/div/ul/li['+str(kat+1)+']/a/text()').extract_first()
                    time.sleep (2)
                    print "========================================"
                    print(nama_kategori)
                    print(url)
                    print "========================================"
                    sql = "select * from bukalapak_category where url = '{}' and nama_kategori = '{}'".format(url, nama_kategori)
                    cur.execute(sql)
                    results = cur.fetchall()
                    if len(results) == 0:
                        sql = "INSERT INTO bukalapak_category VALUES ('{}','{}')".format(url, nama_kategori)
                        print sql
                        cur.execute(sql)
                        conn.commit()
                        print "======================================"
                        print "[INFO] Mysql insert sukses : {}".format(sql)
                        print "======================================"
                    else:
                        print "======================================"
                        print "[ERROR] Mysql insert failure : {}".format(sql)
                        print "============s=========================="
            except:
                pass
        cur.close()
        try:
            self.driver.close()
        except:
            pass