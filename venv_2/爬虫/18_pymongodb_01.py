
from pymongo import MongoClient

# 实例化client，建立链接
client = MongoClient(host="127.0.0.1",port=27017)

# 与shool库中的t251集合建立联系
collection = client["shool"]["t251"]

# 插入一条数据
# ret1 = collection.insert_one({"name":"xiaowang","age":10})
# print(ret1)

# 插入多条数据
# data_list = [{"name":"test{}".format(i)} for i in range(1000)]
# collection.insert_many(data_list)

# 查询一条记录
t = collection.find({"name":"xiaowang"})
print(t)
# 通过遍历才能查看到内容
for  i in t:
    print(i)
# 这里的t就像是一个游标，当i将其遍历完之后，t会在文章尾部，再取t得值时，t为空
# 但是我感觉，collection才应该是一个游标
print(list(t))

