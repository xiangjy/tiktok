# 抖音数据抓取

- 参考链接

  https://idig8.com/2019/04/08/dockershizhanpianpythondedocker-douyinwebduanshujuzhuaqu19/

- 模拟手机请求数据

  设置user-agent

  "User-Agent","Mozilla/5.0 (Linux;U;Android 2.3;en-us;Nexus One Build/FRF91)AppleWebKit/999+(KHTML, like Gecko)Version/4.0 Mobile Safari/999.9"

  设置方法：

  1、

  ```python
  # -*- coding:utf-8 -*-
  from urllib2 import Request, urlopen
  
  
  def fetchurl(url):
      req = Request(url)
      req.add_header("User-Agent", "Mozilla/5.0 (Linux;U;Android 2.3;en-us;Nexus One Build/FRF91)AppleWebKit/999+(KHTML, like Gecko)Version/4.0 Mobile Safari/999.9")
      f = urlopen(req)
      return f.read()
  
  if __name__ == "__main__":
      url = "https://www.iesdouyin.com/share/video/6686379726505774349/?region=CN&mid=6686395143635077901&u_code=hldm8blf&titleType=title"
      print fetchurl(url)
  ```

  2、

  ```python
  # -*- coding:utf-8 -*-
  import requests
  
  
  def fetchurl(url):
      header = {
          'user-agent': 'Mozilla/5.0 (Linux;U;Android 2.3;en-us;Nexus One Build/FRF91)AppleWebKit/999+(KHTML, like Gecko)Version/4.0 Mobile Safari/999.9'
      }
      response = requests.get(url=url, headers=header)
      return response.text
  
  if __name__ == "__main__":
      url = 'https://www.douyin.com/share/user/76055758243'
      print fetchurl(url)
  ```

- 抖音做了反爬，数字变成icon font，进行替换。

  ```python
  regex_list = [
          {'name':[' &#xe603; ',' &#xe60d; ',' &#xe616; '],'value':0},
          {'name':[' &#xe602; ',' &#xe60e; ',' &#xe618; '],'value':1},
          {'name':[' &#xe605; ',' &#xe610; ',' &#xe617; '],'value':2},
          {'name':[' &#xe604; ',' &#xe611; ',' &#xe61a; '],'value':3},
          {'name':[' &#xe606; ',' &#xe60c; ',' &#xe619; '],'value':4},
          {'name':[' &#xe607; ',' &#xe60f; ',' &#xe61b; '],'value':5},
          {'name':[' &#xe608; ',' &#xe612; ',' &#xe61f; '],'value':6},
          {'name':[' &#xe60a; ',' &#xe613; ',' &#xe61c; '],'value':7},
          {'name':[' &#xe60b; ',' &#xe614; ',' &#xe61d; '],'value':8},
          {'name':[' &#xe609; ',' &#xe615; ',' &#xe61e; '],'value':9},
      ]
  ```

- 获取信息的节点xpath

- ```python
  # 昵称
  //div[@class='personal-card']/div[@class='info1']//p[@class='nickname']/text()
  
  #抖音ID
  //div[@class='personal-card']/div[@class='info1']//p[@class='nickname']/text()
  
  #工作
  //div[@class='personal-card']/div[@class='info2']/div[@class='verify-info']/span[@class='info']/text()
  
  #描述
  //div[@class='personal-card']/div[@class='info2']/p[@class='signature']/text()
  
  #地址 已去掉
  //div[@class='personal-card']/div[@class='info2']/p[@class='extra-info']/span[1]/text()
  
  #星座 已去掉
  //div[@class='personal-card']/div[@class='info2']/p[@class='extra-info']/span[2]/text()
  
  #关注数
  //div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='focus block']//i[@class='icon iconfont follow-num']/text()
  
  #粉丝数
  //div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='follower block']//i[@class='icon iconfont follow-num']/text()
  
  #赞数
  //div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='follower block']/span[@class='num']/text()
  ```

- 获取一个人的信息

  ```python
  # -*- coding:utf-8 -*-
  
  import re
  import requests
  from lxml import etree
  
  
  def handle_decode(input_data):
      search_douyin_str = re.compile(r'抖音ID：')
      # 匹配icon font
      regex_list = [
          {'name': [' &#xe603; ', ' &#xe60d; ', ' &#xe616; '], 'value': 0},
          {'name': [' &#xe602; ', ' &#xe60e; ', ' &#xe618; '], 'value': 1},
          {'name': [' &#xe605; ', ' &#xe610; ', ' &#xe617; '], 'value': 2},
          {'name': [' &#xe604; ', ' &#xe611; ', ' &#xe61a; '], 'value': 3},
          {'name': [' &#xe606; ', ' &#xe60c; ', ' &#xe619; '], 'value': 4},
          {'name': [' &#xe607; ', ' &#xe60f; ', ' &#xe61b; '], 'value': 5},
          {'name': [' &#xe608; ', ' &#xe612; ', ' &#xe61f; '], 'value': 6},
          {'name': [' &#xe60a; ', ' &#xe613; ', ' &#xe61c; '], 'value': 7},
          {'name': [' &#xe60b; ', ' &#xe614; ', ' &#xe61d; '], 'value': 8},
          {'name': [' &#xe609; ', ' &#xe615; ', ' &#xe61e; '], 'value': 9},
      ]
  
      for i1 in regex_list:
          for i2 in i1['name']:
              input_data = re.sub(i2, str(i1['value']), input_data)
  
      html = etree.HTML(input_data)
      douyin_info = {}
      # 获取昵称
      douyin_info['nick_name'] = html.xpath("//div[@class='personal-card']/div[@class='info1']//p[@class='nickname']/text()")[0]
      # 获取抖音ID
      douyin_id = ''.join(html.xpath("//div[@class='personal-card']/div[@class='info1']/p[@class='shortid']/i/text()"))
      douyin_info['douyin_id'] = re.sub(search_douyin_str, '', html.xpath("//div[@class='personal-card']/div[@class='info1']//p[@class='nickname']/text()")[0]).strip() + douyin_id
      # 职位类型
      try:
          douyin_info['job'] = html.xpath("//div[@class='personal-card']/div[@class='info2']/div[@class='verify-info']/span[@class='info']/text()")[0].strip()
      except:
          pass
      # 描述
      douyin_info['describe'] = html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='signature']/text()")[0].replace('\n', ',')
      # 关注
      douyin_info['follow_count'] = html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='focus block']//i[@class='icon iconfont follow-num']/text()")[0].strip()
      # 粉丝
      fans_value = ''.join(html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='follower block']//i[@class='icon iconfont follow-num']/text()"))
      unit = html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='follower block']/span[@class='num']/text()")
      if unit[-1].strip() == 'w':
          douyin_info['fans'] = str(float(fans_value) / 10) + 'w'
      else:
          douyin_info['fans'] = fans_value
      # 点赞
      like = ''.join(html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='liked-num block']//i[@class='icon iconfont follow-num']/text()"))
      unit = html.xpath("//div[@class='personal-card']/div[@class='info2']/p[@class='follow-info']//span[@class='liked-num block']/span[@class='num']/text()")
      if unit[-1].strip() == 'w':
          douyin_info['like'] = str(float(like) / 10) + 'w'
      else:
          douyin_info['like'] = like
  
      return douyin_info
  
  
  def handle_douyin_info(url):
      header = {
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
      }
      response = requests.get(url=url, headers=header)
      return handle_decode(response.text, url)
  
  
  if __name__ == '__main__':
      url = 'https://www.douyin.com/share/user/76055758243'
      print handle_douyin_info(url)
  ```

- 获取一个视频

  ```python
  # -*- coding:utf-8 -*-
  
  import re
  import requests
  from lxml import etree
  
  
  def handle_decode(input_data, url):
      search_douyin_str = re.compile(r'抖音ID：')
      # 匹配icon font
      regex_list = [
          {'name':[' &#xe603; ',' &#xe60d; ',' &#xe616; '],'value':0},
          {'name':[' &#xe602; ',' &#xe60e; ',' &#xe618; '],'value':1},
          {'name':[' &#xe605; ',' &#xe610; ',' &#xe617; '],'value':2},
          {'name':[' &#xe604; ',' &#xe611; ',' &#xe61a; '],'value':3},
          {'name':[' &#xe606; ',' &#xe60c; ',' &#xe619; '],'value':4},
          {'name':[' &#xe607; ',' &#xe60f; ',' &#xe61b; '],'value':5},
          {'name':[' &#xe608; ',' &#xe612; ',' &#xe61f; '],'value':6},
          {'name':[' &#xe60a; ',' &#xe613; ',' &#xe61c; '],'value':7},
          {'name':[' &#xe60b; ',' &#xe614; ',' &#xe61d; '],'value':8},
          {'name':[' &#xe609; ',' &#xe615; ',' &#xe61e; '],'value':9},
      ]
  
      for i1 in regex_list:
          for i2 in i1['name']:
              input_data = re.sub(i2,str(i1['value']),input_data)
  
      html = etree.HTML(input_data)
      douyin_info = {}
      douyin_info['nick_name'] = html.xpath("//p[@class='user-info-name']/text()")[0]
      douyin_id = ''.join(html.xpath("//p[@class='user-info-id']/i/text()"))
      douyin_info['douyin_id'] = re.sub(search_douyin_str,'',html.xpath("//p[@class='user-info-name']/text()")[0]).strip() + douyin_id
  
      douyin_info['describe'] = html.xpath("//div[@class='user-title']/text()")[0].replace('\n',',')
  
      like = ''.join(html.xpath("//div[@data-item='like']/p[@class='count']//i[@class='icon iconfont ']/text()"))
      unit = html.xpath("//div[@data-item='like']/p[@class='count']/text()")
      if unit[-1].strip() == 'w':
          douyin_info['like'] = str(float(like)/10)+'w'
      else:
          douyin_info['like'] = like
  
      comment = ''.join(html.xpath("//div[@data-item='comment']//i[@class='icon iconfont ']/text()"))
      unit = html.xpath("//div[@data-item='comment']/p[@class='count']/text()")
      if unit[-1].strip() == 'w':
          douyin_info['comment'] = str((float(comment)/10))+'w'
      else:
          douyin_info['comment'] = comment
  
      return douyin_info
  
  
  def handle_douyin_info(url):
      header = {
          'User-Agent':'Mozilla/5.0 (Linux;U;Android 2.3;en-us;Nexus One Build/FRF91)AppleWebKit/999+(KHTML, like Gecko)Version/4.0 Mobile Safari/999.9'
      }
      response = requests.get(url=url, headers=header)
      return handle_decode(response.text, url)
  
  if __name__ == '__main__':
      url = 'https://www.iesdouyin.com/share/video/6681141729246186760/?mid=6659642087115328259'
      print handle_douyin_info(url)
  ```

  
