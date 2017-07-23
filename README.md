# 项目名: `jd_spider`


### 爬虫表的设计:

*设计宗旨, 怎么简单怎么来!*

### 初始化程序:

1. 更改配置

`vim config.py`

2. 自动初始化库表

`python models.py`

3. 启动爬虫

`python spider`

4. 启动数据清理

`python extractor.py`

#### 架构图
*缺少一个图，后期补上...*
```
push url ---> redis (urls task) ---> spider ---> redis (urls result) --->  extractor --->  mysql
                     |                                                           |
                     ------------------------------------------------------------|
```

`京东所有的品类都是三层.`

**详情页表**

```
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
```

**关联表**

```
class ProductAndCategory(Model):
    pid = BigIntegerField(primary_key=True)
    top_id = IntegerField() # 厨具
    second_id = IntegerField()  # 烹饪锅具
    third_id = IntegerField()  # 炒锅
    top_name =  CharField()
    second_name = CharField()
    third_name = CharField()
    created_on = DateTimeField(default=datetime.now)
```


**品类表**

```
class Category(Model):
    cat_id = IntegerField(primary_key=True)
    cat_name = CharField()
    cat_url = CharField()
    level = IntegerField()
    created_on = DateTimeField(default=datetime.now)

```

### 说明:

该项目没有做深层次递归抓取，所以说需要构建一批索引页的，那么什么索引页？如下...

某个商品类别的索引页:
http://list.jd.com/list.html?cat=6196,6197,6201

如果需要翻页，需要加page及排序参数:

&page=2&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main

最后生成索引页的逻辑:
```
for page in range(1, 10):
    url = "http://list.jd.com/list.html?cat=6196,6197,6201&page={0}&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main".format(page)
    push_mq(url)
```

### 抓取的流程:
### step: 1
首先把厨具类的子类给拿出来,这些url可以作为后面的种子索引页面.

http://channel.jd.com/kitchenware.html

### step: 2
通过种子可以拿到相关产品的列表页.
某一个种子列表页面 `http://list.jd.com/list.html?cat=6196,6197,6199` , 可以获取所有的商品页的url.


### step: 3

通过具体的商品页面 `http://item.jd.com/137179.html` , 可以拿到 商品的名，品牌，编号ID，材质等,面包屑(含有 递归的类别、品牌、产品名)

注: JD的价格是特殊处理的，需要调下面api来获取.  `http://p.3.cn/prices/get?skuid=J_{pid}`


------
