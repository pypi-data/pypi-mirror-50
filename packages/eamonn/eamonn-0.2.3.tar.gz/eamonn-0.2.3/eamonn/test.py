from core import eamonn
save=eamonn.save_mongo(dname="test",fname="test")
res=eamonn.get_mongo(dname="2019_8_12",fname="新浪地产tech")
save.insert({
    "title" : "滨州市以体制机制创新 推动铝产业加速向中高端迈进",
    "url" : "http://news.dichan.sina.com.cn/2019/08/13/1268040.html",
    "target" : "门窗",
    "time" : "08-13"
})