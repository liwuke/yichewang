# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class YichewangPipeline:
    def open_spider(self,spider):
        self.connection = pymysql.connect (host = 'localhost',user = 'root',password = 'root',db = 'dict',charset = 'utf8')
        self.cursor = self.connection.cursor (cursor = pymysql.cursors.SSCursor)
        self.select_parent_id_sql='select id from car where name = %s'
        self.name_sql='insert into car(parent_id,name,type) select %s,%s,%s from DUAL where not EXISTS (select name from car where name = %s);commit '

    def close_spider(self,spider):
        self.cursor.close()
        self.connection.close()

    def process_item(self, item, spider):
        letter=item['letter']
        brand_name=item['brand_name']
        logo=item['logo']
        car_name=item['car_name']
        type_name=item['type_name']
        sort=item['sort']
        letter_sql='insert into car(parent_id,name,type,sort) select %s,%s,%s,%s from DUAL where not EXISTS (select name from car where name = %s);commit '
        letter_args=[ 0, letter, 0, sort,letter]
        self.cursor.execute(letter_sql,letter_args)
        letter_parent_id_args=[letter]
        self.cursor.execute(self.select_parent_id_sql,letter_parent_id_args)
        letter_parent_id=self.cursor.fetchone()
        brand_name_sql='insert into car(parent_id,name,type,logo) select %s,%s,1,%s from DUAL where not EXISTS (select name from car where name = %s);commit '
        brand_name_args=[letter_parent_id,brand_name,logo,brand_name]
        self.cursor.execute(brand_name_sql,brand_name_args)
        brand_name_parent_id_args=[brand_name]
        self.cursor.execute(self.select_parent_id_sql,brand_name_parent_id_args)
        brand_name_parent_id =self.cursor.fetchone()
        car_name_args=[brand_name_parent_id,car_name,2,car_name]
        self.cursor.execute(self.name_sql,car_name_args)
        car_name_parent_id_args=[car_name]
        self.cursor.execute(self.select_parent_id_sql,car_name_parent_id_args)
        car_name_parent_id=self.cursor.fetchone()
        type_name_args=[car_name_parent_id,type_name,3,type_name]
        self.cursor.execute(self.name_sql,type_name_args)
