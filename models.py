# -*- coding: utf-8 -*-

from datetime import datetime

from peewee import *

from config import mysql_config


db = MySQLDatabase(mysql_config['db'], host=mysql_config['host'], user=mysql_config['user'], passwd=mysql_config['passwd'], threadlocals=True, charset='utf8mb4')


class Product(Model):
    pid = BigIntegerField(primary_key=True)
    purl = CharField(unique=True,index=True)
    pname = CharField(max_length=200)
    brand = CharField(max_length=30)
    brand_img = CharField()
    product_img = CharField()
    price = FloatField()
    extra = BlobField()
    created_on = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        db_table = 'product'


class Category(Model):
    cat_id = IntegerField(primary_key=True)
    cat_name = CharField()
    cat_url = CharField()
    level = IntegerField()
    created_on = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        db_table = 'category'


class ProductAndCategory(Model):
    pid = BigIntegerField(primary_key=True)
    top_id = IntegerField() # 厨具
    second_id = IntegerField()  # 烹饪锅具
    third_id = IntegerField()  # 炒锅
    top_name =  CharField()
    second_name = CharField()
    third_name = CharField()
    created_on = DateTimeField(default=datetime.now)

    class Meta:
        database = db
        db_table = 'product_and_cat'


if __name__ == '__main__':
    db.connect()
    select = raw_input("是否要删掉所有表, 再创建表: Y/n  \n")
    for one in [Product, Category, ProductAndCategory]:
        if select == "Y":
            one.drop_table(fail_silently=True)
        try:
            one.create_table()
        except OperationalError:
            print one , "already existed"

