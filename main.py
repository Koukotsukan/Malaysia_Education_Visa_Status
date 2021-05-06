import requests
import os
import re
from bs4 import BeautifulSoup


url = "https://visa.educationmalaysia.gov.my/emgs/application/searchForm"
postUrl = "https://visa.educationmalaysia.gov.my/emgs/application/searchPost/"
s = requests.session()
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
}
captcha = re.findall('<input name="form_key" type="hidden" value="(.+?)" />',s.get(url,headers=headers).text)[0]
print (captcha)
data = {
    "form_key" : captcha,
    "travel_doc_no" : "你的护照号| YOUR PASSPORT NUMBER",
    "nationality" : "你的国籍，如果是中国则填CN | YOUR COUNTRY CODE",
    "agreement" : "1"
}
poster = s.post(postUrl,headers=headers,data=data).text
status =  BeautifulSoup(poster, "lxml")

def color(value):
  digit = list(map(str, range(10))) + list("ABCDEF")
  if isinstance(value, tuple):
    string = '#'
    for i in value:
      a1 = i // 16
      a2 = i % 16
      string += digit[a1] + digit[a2]
    return string
  elif isinstance(value, str):
    a1 = digit.index(value[1]) * 16 + digit.index(value[2])
    a2 = digit.index(value[3]) * 16 + digit.index(value[4])
    a3 = digit.index(value[5]) * 16 + digit.index(value[6])
    if a1 < a2:
        c = "绿色"
    elif a2 - a3 > 50:
        c = "橙色"
    elif a2 -a3 <= 50:
        c = "红色"
    return (c)

try:
    application_status = re.findall('</label>:\xa0\xa0\n(.*)</li>',str(status.select("body > div > div > div.main-container.col1-layout > div > div > div > div > div > div > div:nth-child(4) > table > tbody > tr > td:nth-child(2) > div > div > ul > div > li:nth-child(5)")[0]))[0].replace("  ","")
except:
    application_status = ""

try:
    percentage_color = re.findall('<td style="padding:10px;  border-radius:5px; vertical-align:middle; color:white; background-color:(.+?); border-right:none; text-align:center;"',poster)[0]
except:
    percentage_color = ""

try:
    issues_status = re.findall('">(.*)<div>',str(status.select("#child-issue1")[0]))[0]
except:
    issues_status = ""

try:
    issues_content = re.findall('<div id="child-issue1">\n(.*)<br/>',str(status.select("#child-issue1")[1]))[0].replace("  ","")
except:
    issues_content = ""

try:
    issues_date = re.findall('<span class="nobr">\n(.*)</span>',str(status.select('#child-issue1 > span')[0]))[0].replace(" ","")
except:
    issues_date = ""

try:
    percentage_content = re.findall('<td style="padding:10px;  border-radius:5px; vertical-align:middle; color:white; background-color:.+?; border-right:none; text-align:center;">\n.*<h2>.*\n(.*)</h2>',poster)[0].replace(" ","")
except:
    percentage_content = ""

try:
    print (application_status,color(percentage_color),issues_status,issues_date,issues_content,percentage_content)
except:
    print ("打印失败")

try:
    history = re.findall('<tr class="first last">([\s\S]*)<tr>',poster)[0]
    history_date = re.findall('<td class="a-center">\n(.*)</td>',history)[0].replace("  ","")
    history_status = re.findall('<td>\n(.*)</td>',history)[0].replace("  ","")
    history_content = re.findall('<td>\n(.*)</td>',history)[1].replace("  ","")
except:
    history = ""
    history_date = ""
    history_status = ""
    history_content = ""

num_dict = {'1':'一', '2':'二', '3':'三', '4':'四', '5':'五', '6':'六', '7':'七', '8':'八', '9':'九', '0':'零', }
index_dict = {1:'', 2:'十', 3:'百', 4:'千', 5:'万', 6:'十', 7:'百', 8:'千', 9:'亿'}

num = percentage_content.replace("%","")
nums = list(num)
nums_index = [x for x in range(1, len(nums)+1)][-1::-1]

str1 = ''
for index, item in enumerate(nums):
    str1 = "".join((str1, num_dict[item], index_dict[nums_index[index]]))

str1 = re.sub("零[十百千零]*", "零", str1)
str1 = re.sub("零万", "万", str1)
str1 = re.sub("亿万", "亿零", str1)
str1 = re.sub("零零", "零", str1)
str1 = re.sub("零\\b" , "", str1)
str1 = str1.replace('一十','十')
percentage_content2 = str1

if issues_status == "" and issues_date == "" and issues_content == "":
    log = "申请状态:" + application_status + "\n\n\n\n" + "申请颜色:" + color(percentage_color) + "\n\n\n\n" +"申请进度:"+ percentage_content +"\n\n\n\n" + "历史状态:" + history_status + "\n\n\n\n" + "历史时间:" + history_date + "\n\n\n\n"+ "历史内容:" + history_content + "\n\n\n\n"
else:
    log = "申请状态:" + application_status + "\n\n\n\n" + "申请颜色:" + color(percentage_color) + "\n\n\n\n" +"申请进度:"+ percentage_content +"\n\n\n\n" + "问题状态:" + issues_status + "\n\n\n\n" + "问题时间:" + issues_date + "\n\n\n\n"+ "问题内容:" + issues_content + "\n\n\n\n"

print (log)



