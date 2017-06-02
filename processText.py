import re
import datetime

def readfile(filename):
    '''read a fiel, store the contents of each row into the list'''
    list = []
    with open(filename,'r',encoding = 'utf-8') as f:
    	lines = f.readlines() #读取文件中所有行，存入一个列表中
    return lines

def removeDuplicate(filename):
    '''remove duplicate item in the list'''
    list = readfile(filename)
    return [ i.replace('\n','').strip() for i in set(list) ]

def cleanData(data):
    '''Use a regular expression data cleaning'''
    _text = re.sub(r'</?\w+[^>]*>','',data)
     # _text = re.sub(r'\p{P}+', ',', _text)
    _text = re.sub("[():]+|[：，。？、（）]+", ",",_text)
    _text = _text.replace('&nbsp;','')
    _text = _text.replace('&mdash;','')
    _text = _text.replace('- ','-')
    _text = _text.replace(' ',',')
    _text = _text.replace('　',',')
    _text = _text.replace('\r\n',',')
    _text = _text.replace('\n',',')
    for i in range(20):
        _text = _text.replace(',,',',')

    return _text

def matchWord(name_list,_text):
    '''According to whether the text contains the word, and returns the result  '''
    for i in name_list:
        try:
            result = re.search(i,_text).group(0)
            break
        except:
            result = None
            pass

    return result

def filterInfo(start_char_,_text,end_char = ','):
    '''the filter of infomation'''
    for i in start_char_:
        filter = i + '(.*?)' + end_char
        try:
            result = re.search(filter,_text,re.S)
            value = result.group(1)
            break
        except:
            value = 'None'
            pass

    return value

def listToFile(list,filename):
    '''the list content written to the file'''
    with open(filename,'w',encoding = 'utf-8') as f:
        for i in list:
            f.write(i+'\n')

if __name__ == '__main__':

    # purchaser_list = removeDuplicate('purchaser.txt')
    # print(len(purchaser_list),purchaser_list[:10])

    supplier_list = removeDuplicate('supplier.txt')
    print(len(supplier_list),supplier_list[:10])

    # filename = str(datetime.date.today()) + '-purchaser.txt'
    # listToFile(purchaser_list,'purchaser.txt')

    # filename1 = str(datetime.date.today()) + '-supplier.txt'
    listToFile(supplier_list,'supplier.txt')
