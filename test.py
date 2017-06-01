import re
import requests

url = 'http://www.ahzfcg.gov.cn/mhxt/MhxtSearchBulletinController.zc?method=bulletinChannelRightDown'

# for i in range(67):
#     data ={ 'pageSize':'15',
#             'channelCode':'sjcg',
#             'bType':'03',
#             'areaCode':'341200',
#             'pageNo':str(i)}

data ={ 'pageSize':'10',
        'channelCode':'sjcg',
        'bType':'03',
        'areaCode':'341200',
        'pageNo':1}

def getDataList(page_num):
    # get list of data
    datas = []
    for i in range(page_num):
        data = {'pageSize':'100',
                'channelCode':'sjcg',
                'bType':'03',
                'areaCode':'341200',
                'pageNo':i}
        datas.append(data)

    return datas

# datas = getDataList(8)
# for i in datas:
#     print(i)

html = requests.post(url,data = data)

# print(html.text)

info = re.findall('<a style="margin-left:-105px;"(.*?)</li>\\r\\n\\t\\t',html.text,re.S)

# print(info)
for i in info[:1]:
    title = re.search('title="(.*?)"',i,re.S).group(1)
    print(title)

    _link = re.search('target="_blank" href="(.*?)">',i,re.S).group(1)
    link = 'http://www.ahzfcg.gov.cn/' + _link
    print(link)

    time = re.search('<span class="date">(.*?)</span>',i,re.S).group(1)
    print(time)

def cleanData(data):
    # 使用正则表达式清洗数据
    link = re.compile('<(.*?)>')
    _text = re.sub(link,'',data)
    _text = _text.replace('&nbsp;','')
    _text = _text.replace('：',',')
    _text = _text.replace('，',',')
    _text = _text.replace(':',',')
    _text = _text.replace('）',',')
    _text = _text.replace(' ','')
    _text = _text.replace('\r\n',',')
    _text = _text.replace('\n',',')
    for i in range(5):
        _text = _text.replace(',,',',')

    return _text

source = requests.get(link)
source.encoding = 'utf-8'
# print(source.text)

info = re.findall('<div class="frameNews">(.*?)<div class="operationBtnDiv">',source.text,re.S)
# print(info)
_text = cleanData(info[0])

print(_text)

project_num_list = ['备案编号','备案编号,','项目编号']

def filterInfo(list,_text):
    # the filter of infomation
    for i in project_num_list:
        filter = i + '(.*?),'
        project_num = re.search(filter,_text,re.S)
        if project_num:
            value = project_num.group(1)
            break
        else:
            pass

    return value

a = filterInfo(project_num_list,_text)

print(a)



# project_num = project_num.replace('：','').strip()
# a = project_num.replace(':','').strip()
#
# print(project_num)
#
# purchaser = re.search('采购单位,(.*?),',_text,re.S).group(1)
# print(purchaser)
# purchaser = purchaser.replace('：','').strip()
# b = purchaser.replace(':','').strip()

# contact_person =  re.search('联 系 人(.*?)\\n',_text,re.S).group(1)
#
# b = removeColon(contact_person)
#
# print(b)
