#!usr/bin/env python
#encoding:utf-8
from __future__ import division
 
'''
__Author__:沂水寒城
功能： GitHub项目爬虫可视化操作界面
'''

 
 
from gitSpider import *
from gooey import Gooey
from gooey import GooeyParser

 
 
@Gooey(monospace_display=True)
def guiOperation():
    my_cool_parser = GooeyParser(description=u'GitHub项目爬虫可视化操作界面')
    my_cool_parser.add_argument(
        "kw",
        metavar=u'搜索关键词：',
        help="请输入搜索关键词：",
        default='spider')
    my_cool_parser.add_argument(
        "pagenum",
        metavar=u'爬取页面总数',
        help="0-100",
        default='5')
    my_cool_parser.add_argument(
        'savedir',
        metavar=u'结果保存路径：',
        help=u'请输入保存路径：',
        default='downloadProjects/')
    args=my_cool_parser.parse_args()
    kw=args.kw
    pagenum=int(args.pagenum)
    savedir=args.savedir
    gitSpider(kw=kw,topN=pagenum,saveDir=savedir)
    print('Finished!!!')

 
 
if __name__ == '__main__':
    guiOperation()