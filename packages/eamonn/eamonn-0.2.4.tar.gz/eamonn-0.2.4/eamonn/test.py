from core import eamonn
lis = ['企业名称', '企业类型', '企业链接地址', '法定代表人', '企业地址', '在甘办公电话', '注册资本', '经济性质', '营业执照注册号（统一社会信用编码）', '在甘办公地址', '主项资质',
           '所在城市', '城市编码', '抓取时间']
x=eamonn.save_xlsx("甘肃",lis)
get_mongo=eamonn.get_mongo(dname="2019_8_14",fname="info_list_product").find()
for i in get_mongo:
    i.pop("_id")
    x.save(list(i.values()))
x.close("甘肃.xls")