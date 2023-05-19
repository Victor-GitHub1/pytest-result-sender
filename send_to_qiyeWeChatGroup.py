# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project: pytest-result-sender03
@File   : send_to_qiyeWeChatGroup.py
@Contact: 12705290+victorgugit@user.noreply.gitee.com
@License: (C)Copyright 2017-2023

@Modify Time      @Author      @Version      @Description
------------      -------      --------      ------------
5/19/2023 2:33 PM   Victor.Gu       1.0         None
"""
import requests

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=aef8c0d1-b4ec-4336-b8d6-a08bee286d5e"

# datas = {
#     "msgtype": "text",
#     "text": {
#         "content": "hello world",
#         "mentioned_list": ["xiaohe", "@all"],
#         "mentioned_mobile_list": ["13800001111", "@all"]
#     }
# }

# datas = {
#     "msgtype": "markdown",
#     "markdown": {
#         "content": "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n> 类型:<font color=\"comment\">用户反馈</font>>普通用户反馈:<font color=\"comment\">117例</font>>VIP用户反馈:<font color=\"comment\">1例</font>"
#     }
# }

content = """
pytest自动化测试结果

测试时间：xxx-xxxx-xx <br />
用例数量：100 <br />
执行时长：50s <br />
测试通过：<font color="green"> 2 </font> <br />
测试失败：<font color="red"> 1 </font> <br />
测试通过率：66.67% <br />

测试报告地址：https://www.baidu.com
"""

datas = {"msgtype": "markdown", "markdown": {"content": content}}

requests.post(url=url, json=datas)