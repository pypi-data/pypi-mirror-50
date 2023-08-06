# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 深圳星河软通科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.astar.ltd
# @file: __init__.py
# @time: 2019/8/11 0:14
# @Software: PyCharm


from astartool.setuptool import get_version
version = (0 , 0, 1, 'final', 0)

__version__ = get_version(version)

del get_version
