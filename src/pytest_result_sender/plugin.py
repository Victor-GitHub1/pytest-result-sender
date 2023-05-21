# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project: pytest-result-sender03
@File   : plugin.py
@Contact: 12705290+victorgugit@user.noreply.gitee.com
@License: (C)Copyright 2017-2023

@Modify Time      @Author      @Version      @Description
------------      -------      --------      ------------
5/19/2023 2:27 PM   Victor.Gu       1.0         None
"""
from datetime import datetime

import pytest
import requests

data = {
    "passed": 0,
    "failed": 0,
}


# 加载(收集)测试用例之前，加载pytest.ini中的配置项的hook函数（钩子函数）
def pytest_addoption(parser):
    parser.addini("send_when", help="什么时候发送测试结果？every表示每次都发送，on_fail表示只有遇到失败时才发送")
    parser.addini("send_where", help="测试结果发送到哪里？")


# 测试用例执行结束后，判断测试结果的hook函数（钩子函数）
def pytest_runtest_logreport(report):
    # print(report)
    if report.when == "call":
        print("该测试用例的执行结果：", report.outcome)
        data[report.outcome] += 1


# 测试用例全部加载(收集)完成后执行的hook函数（钩子函数）
def pytest_collection_finish(session):
    # print(session.items)
    # 返回collected 3 items
    # [<Function test_abc>, <Function test_pass>, <Function test_fail>]
    data["total"] = len(session.items)
    print("用例的总数：", data["total"])


# 配置加载完毕后执行，所有测试用例执行前执行的hook函数（钩子函数）
def pytest_configure(config: pytest.Config):
    data["start_time"] = datetime.now()
    # print(f"{datetime.now()} pytest开始执行")
    data["send_when"] = config.getini("send_when")
    data["send_where"] = config.getini("send_where")
    # print(config.getini("send_when"))
    # print(config.getini("send_where"))


# 配置卸载完毕后执行，所有测试用例执完毕后执行的hook函数（钩子函数）
def pytest_unconfigure():
    data["end_time"] = datetime.now()
    # print(f"{datetime.now()} pytest结束执行")
    # print(data)
    data["duration"] = data["end_time"] - data["start_time"]
    data["pass-ratio"] = data["passed"] / data["total"] * 100
    data["pass-ratio"] = f"{data['pass-ratio']:.2f}"
    # print(data["pass-ratio"])  # 打印66.67

    # 单元测试断言
    # assert timedelta(seconds=3) > data["duration"] >= timedelta(seconds=2.5)
    # assert data['total'] == 3
    # assert data['passed'] == 2
    # assert data['failed'] == 1
    # assert data['pass-ratio'] == '66.67%'

    send_result()


def send_result():
    # 如果遇到测试失败才发送，但实际测试没有失败，则不发送
    if data["send_when"] == "on_fail" and data["failed"] == 0:
        return

    # 如果没有配置发送到哪里，则什么都不发送
    if not data["send_where"]:
        return

    # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=aef8c0d1-b4ec-4336-b8d6-a08bee286d5e"
    # 动态指定将测试结果发到哪里
    url = data["send_where"]

    content = f"""
    pytest自动化测试结果

    测试时间：{data['start_time']}
    用例数量：{data['total']}
    执行时长：{data['duration']}
    测试通过：<font color="green"> {data['passed']} </font>
    测试失败：<font color="red"> {data['failed']} </font>
    测试通过率：{data['pass-ratio']}%

    测试报告地址：https://www.baidu.com
    """

    datas = {"msgtype": "markdown", "markdown": {"content": content}}

    # 对请求进行异常判断
    try:
        requests.post(url=url, json=datas)
    except Exception:
        pass

    # 标记 测试结果发送成功
    data["send_done"] = 1
