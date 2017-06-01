import re
import requests
import xlrd
import xlwt
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

def getDataList(page_num,key):
    # get list of data
    datas = []
    for i in range(page_num):
        data = {'pageSize':'240',
                'channelCode':'sjcg',
                'bType':'03',
                'areaCode':'341200',
                'key':key,
                'pageNo':i}
        datas.append(data)

    return datas

class Spider(object):
    def __init__(self):
        print('start crawling...')

    def getSource(self,url,headers):
        # get the web page source code
        source = requests.get(url,headers)
        source.encoding = 'utf-8'
        # print(source.text)
        return source.text

    def getItemInfo(self,source):
        # get each item information
        # print(source)
        info = re.findall('<a style="margin-left:-105px;"(.*?)</li>\\r\\n\\t\\t',source.text,re.S)
        return info

    def getInfoDict(self,itemInfo):
        # get the infomation of dictionary
        info = {}
        info['title'] = re.search('title="(.*?)"',itemInfo,re.S).group(1)
        _link = re.search('target="_blank" href="(.*?)">',itemInfo,re.S).group(1)
        info['link'] = 'http://www.ahzfcg.gov.cn/' + _link
        info['time'] = re.search('<span class="date">(.*?)</span>',itemInfo,re.S).group(1)
        info['status'] = 0
        return info

    def generatePageLink(self,url,total_page):
        # generate a page link
        now_page = int(re.search('pageing=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('pageing=\d+','pageing=%s'%i,url,re.S)
            page_group.append(link)
        return page_group


def cleanData(data):
    # 使用正则表达式清洗数据

    _text = re.sub(r'</?\w+[^>]*>','',data)
     # _text = re.sub(r'\p{P}+', ',', _text)
    _text = re.sub("[():]+|[：，。？、（）]+", ",",_text)
    _text = _text.replace('&nbsp;','')
    _text = _text.replace('&mdash;','')
    _text = _text.replace(' ',',')
    _text = _text.replace('　',',')
    _text = _text.replace('\r\n',',')
    _text = _text.replace('\n',',')
    for i in range(20):
        _text = _text.replace(',,',',')

    return _text

def filterInfo(list,_text):
    # the filter of infomation
    for i in list:
        filter = i + '(.*?),'
        project_num = re.search(filter,_text,re.S)
        if project_num:
            value = project_num.group(1)
            break
        else:
            value = 'None'
            pass

    return value

def greatInfoDict(url,pageNum,datas,headers):
    project_infomation = []
    project_spider = Spider()

    for i in datas:
        source = requests.post(url,data = i) # get source of html
        infoList = project_spider.getItemInfo(source)
        for each in infoList:
            info = project_spider.getInfoDict(each)
            project_infomation.append(info)
    i=1
    # get text of info
    for each in project_infomation:
        print(i)
        if each['status'] == 0:
            url_link = each['link']
            print(url_link)
            try:
                html_source = project_spider.getSource(url_link,headers)
                # print(html_source)
                info = re.findall('<div class="frameNews">(.*?)<div class="operationBtnDiv">',html_source,re.S)
                _text = cleanData(info[0])
                print(_text)
                each['text'] = _text

                each['project_num'] = filterInfo(project_num_list,_text)
                print(each['project_num'])

                each['purchaser'] = filterInfo(purchaser_list,_text)
                print(each['purchaser'])

                each['supplier'] = filterInfo(supplier_list,_text)
                print(each['supplier'])

                # each['text'] = _text
                # each['area'] = area
                each['status'] = 1
                i += 1
            except:
                each['status'] = 0


    return project_infomation

def saveExcal(area,filename,project_infomation):
    # save to the file of Excal
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
    pageNum = 1

    project_num_list = ['备案编号','备案编号,','项目编号,','项目编号','招标编号,','招标编码,'
                        '访问次数,颍上县黄坝乡人民政府路灯采购项目',
                        '访问次数,颍上县司法局办公设备采购项目,二次,','采购项目,','编号,']
    purchaser_list = ['采购人名称,','采购人,','采购单位,','采购单位','采购人','招标人,','招标人','采购代理机构,','采购代理机构',
                      '招,标,人','特此公告,','特此公示,']
    supplier_list = ['第一中标候选单位,','预中标人,','成交供应商及成交金额,','供应商为,','供应商名称,','中标供应商,','中标供应商','成交供应商,',
                     '中标人名称,','中标人,','中标推荐单位,','中标候选人,报价,元,1,','中标候选单位,',
                     '第一中标候选人,','中标候选单位名称第一名,','成交候选人,','成交人,','候选人,','成交单位,',
                     '成交供应商','中标候选人,','中标候选人,','第一、二包,','第一预中标人,','一包,','最终确定,'
                     ]

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

    # datas = getDataList(pageNum,key = '环境') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','环境_fy_WinningInfomation.xls',project_list)

    datas = getDataList(pageNum,key = '智能') # get the list of datas
    project_list = greatInfoDict(url,pageNum,datas,headers)
    saveExcal('fuyang','智能_fy_WinningInfomation.xls',project_list)


    # datas = getDataList(pageNum,key = '信息') # get the list of datas
    # project_list = greatInfoDict(url,pageNum,datas,headers)
    # saveExcal('fuyang','信息_fy_WinningInfomation.xls',project_list)


