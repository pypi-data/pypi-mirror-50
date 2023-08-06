from core import eamonn


li=[1,2,3]
a=eamonn.save_xlsx("test",li)
b=eamonn.save_xlsx("test",li)

lis=[4,5,6]
print(a==b)
print(id(a),id(b))
a.save([9,7,8])
b.save([9,111,8])
b.save([9,111,8])
b.save([9,111,8])
b.save([9,111,8])

a.close("a.xls")
b.close("b.xls")