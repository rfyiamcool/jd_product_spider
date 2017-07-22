pider)

###爬虫表的设计:

*设计宗旨, 怎么简单怎么来!*

###初始化程序:

1. 更改配置
`vim config.py`

2. 自动初始化库表
`python models.py`

3. 启动爬虫
`python spider`

4. 启动数据清理
`python extractor.py`

`架构图`

push url ---> redis (urls task) ---> spider ---> redis (urls result) --->  extractor --->  mysql
                     |                                                           |
                     ------------------------------------------------------------|

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
//京东配送  +  &page=1&delivery=1&trans=1&JL=4_10_0#J_main


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



### 抓取的流程:
### step: 1
首先把厨具类的子类给拿出来,这些url可以作为后面的种子索引页面.

http://channel.jd.com/kitchenware.html`

### step: 2
通过种子可以拿到相关产品的列表页.
某一个种子列表页面 `http://list.jd.com/list.html?cat=6196,6197,6199` , 可以获取所有的商品页的url.


### step: 3

通过具体的商品页面 `http://item.jd.com/137179.html` , 可以拿到 商品的名，品牌，编号ID，材质等,面包屑(含有 递归的类别、品牌、产品名)

注: JD的价格是特殊处理的，需要调下面api来获取.  `http://p.3.cn/prices/get?skuid=J_{pid}`


------

#### 存在的问题: 

**类别的层级要存几层 ？ 咱们的tag就做了一个关联 !**

厨具 > 刀剪菜板 > 菜刀 >  十八子作 > 十八子作菜刀

厨具 > 刀剪菜板 > 砧板 >  三月三 > 三月三砧板

厨具 > 烹饪锅具 > 炒锅 >  苏泊尔（SUPOR） > 苏泊尔无油烟不粘炒锅


**列表页是否需要指定【京东配送]**

选择借助京东配置来介绍重复商品的抓取 (京东自营有苏泊尔，其他几个小贩也卖苏泊尔)



