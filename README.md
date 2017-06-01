## 任务
- 分析当前政府招标市场信息，生成市场情况报告

## 目标分析
- 目标网站：jyzx.fy.gov.cn,http://www.ahzfcg.gov.cn/
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

## 分析数据
