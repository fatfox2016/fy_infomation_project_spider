## 任务
- 分析当前政府招标市场信息，生成市场情况报告

## 目标分析
- 目标网站：http://www.ahzfcg.gov.cn/,(参考后备:http://jyzx.fy.gov.cn)
- 有效资料：招标公告，中标公告
- 网页类型：动态页面，AJAX

## 所需工具
- Chroma开发者工具
- Python
    + requests
    + re
    + xlwt

## 页面信息特征
- 所需信息：
    + title 
    + project link 
    + purchaser
    + supplier
    + time

- 特征提取（分析网页源代码）
  + 分步提取
    * 提取正文
    * 清洗噪点信息
    * 分析所需信息上下文context特征
  + 获取信息value,生成信息字典

- 存储
  + 使用xlwt库，把信息字典存为.xls文件。
 
## 代码仓库
- 网址:https://github.com/fatfox2016/fy_infomation_project_spider

- spider.py : 爬虫主程序
    + 重要参数：
        * url : 目标网站网址
        * headers : 模拟浏览器信息
        * datas : 请求数据信息
        * pageNum : 页面数
        * key ：搜索关键字

- proessText.py : 处理文本信息模块文件

## 分析数据
