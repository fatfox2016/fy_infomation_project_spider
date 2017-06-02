import re
import requests
import xlrd
import xlwt
from processText import cleanData,matchWord,filterInfo,removeDuplicate

class Spider(object):
    '''single thread ,single layer, spider'''
    def __init__(self,url,headers,datas):
        self.url = url
        self.headers = headers
        self.datas = datas
        print('start crawling...')

    def getSource(self):
        '''get the web page source code'''
        source = requests.get(self.url,self.headers)
        source.encoding = 'utf-8'
        # print(source.text)
        return source.text

    def getInfo(self):
        '''get each item information'''
        source = self.getSource()
        info = re.findall('<a style="margin-left:-105px;"(.*?)</li>\\r\\n\\t\\t',source,re.S)
        return info

    def getInfoDict(self,eachInfo):
        '''get the infomation of dictionary'''
        info_dict = {}
        info_dict['title'] = re.search('title="(.*?)"',eachInfo,re.S).group(1)
        _link = re.search('target="_blank" href="(.*?)">',eachInfo,re.S).group(1)
        info_dict['link'] = 'http://www.ahzfcg.gov.cn/' + _link
        info_dict['time'] = re.search('<span class="date">(.*?)</span>',eachInfo,re.S).group(1)
        info_dict['status'] = 0
        return info_dict

    def generateLinks(self):
        '''generate a link , srote it into a dictionary'''
        project_links = []
        # project_spider = Spider()

        for i in self.datas:
            source = requests.post(url,data = i) # get source of html
            infoList = self.getInfo()
            for each in infoList:
                info = self.getInfoDict(each)
                project_links.append(info)

        return project_links

    def generatePageLink(self,url,total_page):
        '''generate a page link'''
        now_page = int(re.search('pageing=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('pageing=\d+','pageing=%s'%i,url,re.S)
            page_group.append(link)
        return page_group

def getDataList(page_num,key):
    # get list of data
    datas = []
    for i in range(page_num):
        data = {'pageSize':'300',
                'channelCode':'sjcg',
                'bType':'03',
                'areaCode':'341200',
                'key':key,
                'pageNo':i}
        datas.append(data)
    # print(datas)
    return datas

def getInfoList(headers,links):
    '''get text of info,store it into dictionary'''
    i=1
    for each in links:
        print(i)
        if each['status'] == 0:
            url_link = each['link']
            print(url_link)
            try:
                html_source = requests.get(url_link,headers)
                html_source.encoding = 'utf-8'
                # print(html_source)
                info = re.findall('<div class="frameNews">(.*?)<div class="operationBtnDiv">',html_source.text,re.S)
                _text = cleanData(info[0])
                print(_text)
                each['text'] = _text

                each['project_num'] = filterInfo(project_num_list,_text)
                print(each['project_num'])

                purchaser_r = matchWord(purchaser_names,_text)
                if purchaser_r == None:
                    each['purchaser'] = filterInfo(purchaser_list,_text)
                else:
                    each['purchaser'] = purchaser_r

                supplier_r = matchWord(supplier_names,_text)
                if supplier_r == None:
                    each['supplier'] = filterInfo(supplier_list,_text)
                else:
                    each['supplier'] = supplier_r

                each['status'] = 1
                i += 1
            except:
                each['status'] = 0
                pass

    return links

def searchKeyToInfo(headers,links):
    '''search for keywords to get content,store it in a list'''
    i = 1
    for each in links:
        print(i)
        if each['status'] == 0:
            url_link = each['link']
            print(url_link)
            try:
                html_source = requests.get(url_link,headers)
                html_source.encoding = 'utf-8'
                info = re.findall('<div class="frameNews">(.*?)<div class="operationBtnDiv">',html_source.text,re.S)
                # print(info)
                _text = cleanData(info[0])
                print(_text)

                supplier_r = matchWord(supplier_names,_text)
                print(supplier_r)
                if supplier_r:
                    each['supplier'] = supplier_r
                    each['text'] = _text
                    each['project_num'] = filterInfo(project_num_list,_text)
                    each['purchaser'] = matchWord(purchaser_names,_text)
                    each['status'] = 1
                    i += 1
            except:
                each['status'] = 0
                pass

    return links

def saveExcal(area,filename,project_infomation):
    '''save to the file of Excal'''
    row_num = len(project_infomation)
    file = xlwt.Workbook()
    table = file.add_sheet(area)

    for row in range(row_num):
        info = project_infomation[row]
        # print(info)
        table.write(row,0,info['link'])
        table.write(row,1,info['title'])
        table.write(row,2,info['project_num'])
        table.write(row,3,info['purchaser'])
        table.write(row,4,info['supplier'])
        table.write(row,5,info['time'])
        table.write(row,6,info['text'])
        table.write(row,7,info['status'])

    file.save(filename)



if __name__ == '__main__':

    headers = {'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/58.0.3029.110 Safari/537.36'}


    url = 'http://www.ahzfcg.gov.cn/mhxt/MhxtSearchBulletinController.zc?method=bulletinChannelRightDown'
    pageNum = 10

    project_num_list = ['备案编号','备案编号,','项目编号,','项目编号','招标编号,','招标编码,'
                        '访问次数,颍上县黄坝乡人民政府路灯采购项目',
                        '访问次数,颍上县司法局办公设备采购项目,二次,','采购项目,','编号,']
    purchaser_list = ['采购人名称,','采购人,','采购单位,','采购单位','采购人','招标人,','招标人','采购代理机构,','采购代理机构',
                      '招,标,人','特此公告,','特此公示,']
    supplier_list = ['第一中标候选单位,','预中标人,','成交供应商及成交金额,','供应商为,','供应商名称,','中标供应商,','中标供应商',
                     '成交供应商,','中标人名称,','中标人,','中标推荐单位,','中标候选人,报价,元,1,','中标候选单位,',
                     '第一中标候选人,','中标候选单位名称第一名,','成交候选人,','成交人,','候选人,','成交单位,',
                     '成交供应商','中标候选人,','中标候选人,','第一、二包,','第一预中标人,','一包,','最终确定,'
                     ]

    purchaser_names = removeDuplicate('purchaser.txt')

    supplier_names = removeDuplicate('supplier.txt')

    datas = getDataList(pageNum,key = '智能') # get the list of datas
    links = Spider(url,headers,datas).generateLinks()
    # project_ = getInfoList(headers,links)
    # project_ = searchKeyToInfo(headers,links)
    for i in links:
    # for i in project_:
        print(i)




    # datas = getDataList(pageNum,key = '公安') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','公安_fy_WinningInfomation.xls',project_list)
    #
    # datas = getDataList(pageNum,key = '司法') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','司法_fy_WinningInfomation.xls',project_list)
    #
    # datas = getDataList(pageNum,key = '国土') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','国土_fy_WinningInfomation.xls',project_list)
    #
    # datas = getDataList(pageNum,key = '水务') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','水务_fy_WinningInfomation.xls',project_list)
    #
    # datas = getDataList(pageNum,key = '环境') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','环境_fy_WinningInfomation.xls',project_list)
    #
    # datas = getDataList(pageNum,key = '智能') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','智能_fy_WinningInfomation.xls',project_list)

    # datas = getDataList(pageNum,key = '信息') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','信息_fy_WinningInfomation.xls',project_list)
    #
    # datas = getDataList(pageNum,key = '智慧') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','智慧_fy_WinningInfomation.xls',project_list)
    #
    # datas = getDataList(pageNum,key = '系统') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','系统_fy_WinningInfomation.xls',project_list)



















# def greatInfoDict(url,pageNum,datas,headers):
#     # great dictionary of the project infomation
#     project_infomation = []
#     project_spider = Spider()
#
#     for i in datas:
#         source = requests.post(url,data = i) # get source of html
#         infoList = project_spider.getItemInfo(source)
#         for each in infoList:
#             info = project_spider.getInfoDict(each)
#             project_infomation.append(info)
#     i=1
#     # get text of info
#     for each in project_infomation:
#         print(i)
#         if each['status'] == 0:
#             url_link = each['link']
#             print(url_link)
#             try:
#                 html_source = project_spider.getSource(url_link,headers)
#                 # print(html_source)
#                 info = re.findall('<div class="frameNews">(.*?)<div class="operationBtnDiv">',html_source,re.S)
#                 _text = cleanData(info[0])
#                 print(_text)
#                 each['text'] = _text
#
#                 each['project_num'] = filterInfo(project_num_list,_text)
#                 print(each['project_num'])
#
#                 purchaser_r = matchWord(purchaser_names,_text)
#                 # print(purchaser_r)
#                 if purchaser_r == None:
#                     each['purchaser'] = filterInfo(purchaser_list,_text)
#                 else:
#                     each['purchaser'] = purchaser_r
#
#                 supplier_r = matchWord(supplier_names,_text)
#                 if supplier_r == None:
#                     each['supplier'] = filterInfo(supplier_list,_text)
#                 else:
#                     each['supplier'] = supplier_r
#
#                 each['status'] = 1
#                 i += 1
#             except:
#                 each['status'] = 0
#                 pass
#
#     return project_infomation