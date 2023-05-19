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
from datetime import datetime, timedelta

data = {}


def pytest_configure():
    # 配置加载完毕后执行，所有测试用例执行前执行
    data["start_time"] = datetime.now()
    print(f"{datetime.now()} pytest开始执行")


def pytest_unconfigure():
    # 配置卸载完毕后执行，所有测试用例执行完毕后执行
    data["end_time"] = datetime.now()
    print(f"{datetime.now()} pytest结束执行")

    data["duration"] = data["end_time"] - data["start_time"]

    print(data)
    assert timedelta(seconds=3) > data["duration"] >= timedelta(seconds=2.5)