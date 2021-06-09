# -*- coding: utf-8 -*-
# author： caoji
# datetime： 2021-06-08 13:41 
# ide： PyCharm
import os
import sys

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)));
execute(["srcapy", "crawl", "yg"])
