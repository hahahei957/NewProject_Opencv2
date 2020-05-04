from lxml import etree

text = ''' <div> <ul> 
        <li class="item-1"><a>first item</a></li> 
        <li class="item-1"><a href="link2.html">second item</a></li> 
        <li class="item-inactive"><a href="link3.html">third item</a></li> 
        <li class="item-1"><a href="link4.html">fourth item</a></li> 
        <li class="item-0"><a href="link5.html">fifth item</a>  
        </ul> </div> '''

html = etree.HTML(text=text)

print(html)
# 通过etree.tostring可以将html的内容展现出来，并且，etree函数具有html文段修复功能，会将我们原来的str修改，所以在报错时一定要打印一下这个内容看看

print("*"*50, etree.tostring(html).decode())   # 得到的是bytes类型，所以我们要用decode()
print("*"*50, type(etree.tostring(html)))

#获取class为item-1 li下的a的href
"""ret1得到的是一个包含属性href里面内容的列表"""
ret1 = html.xpath("//li[@class='item-1']/a/@href")
print('ret1 -->  ',ret1)

#获取class为item-1 li下的a的文本
"""ret2得到了一个包含多个a内文本内容的一个列表"""
ret2 = html.xpath("//li[@class='item-1']/a/text()")
print('ret2 -->  ',ret2)

#每个li是一条新闻，把url和文本组成字典
for href in ret1:
    item = dict()
    item["url"] = href

    """下面这句写的很好，但是就是通过这整个循环得到的组合后的字典是不合适的，
    因为如果html得到的url或者a有残缺，会导致item["text"]和ret2[ret1.index(href)]对应出错误"""
    "笨例子就很好的说明了问题，第一个中的a没有对应的url"
    item["text"] = ret2[ret1.index(href)]
    print(item)
print("___________________________________")
# 通过分组的方法，从而更好的将url和文本组成字典
"""ret3是得到是包含了三个element对象的列表，由于成员们都不是指向属性如@href或者指向文本的，那么他们就是指向html内所有带有限定的标签为li的对象，可以用xpth访问"""
ret3 = html.xpath("//li[@class='item-1']")
print(ret3)
item = dict()
for i in ret3:
    # print(1)
    # print(etree.tostring(i).decode())
    # item["url"] = i.xpath("//a/@href")[0] if len(i.xpath("//a/@href")[0])>0 else None
    "上面那一句是错的, 一定要切记: ./值得是当前路径下的a，也就我们之前给ret3指定到了的路径， 而 // 是重新定位一个路径，并重新定位到了新的一个a上"
    # 并且我之前用的是 if len(i.xpath("./a/@href")[0])>0 来判断列表中是否为空值，但如果列表是None，那么我们取list[0]就会越界，因为列表中一个成员都没有
    item["url"] = i.xpath("./a/@href")[0] if len(i.xpath("./a/@href"))>0 else None
    item["text"] = i.xpath("./a/text()")[0] if len(i.xpath("./a/text()"))>0 else None
    print(item)


