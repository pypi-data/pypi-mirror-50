#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-01 14:36:25
# @Author  : eamonn (china.eamonn@gmail.com)
# @Link    : elanpy.com
# 要么做第一个，要么做最好的一个。

import eamonn
import sys
sys.path.append("../")

import core 
alist = [93, 77, 44,0,1,5,7,2,6]
# print("原列表为：%s" % alist)
# bubble_sort(alist)
# print("新列表为：%s" % alist)
arr=core.count_sort(alist)
print(alist)