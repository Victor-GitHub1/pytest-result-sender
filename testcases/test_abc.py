# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project: pytest-result-sender03
@File   : test_abc.py
@Contact: 12705290+victorgugit@user.noreply.gitee.com
@License: (C)Copyright 2017-2023

@Modify Time      @Author      @Version      @Description
------------      -------      --------      ------------
5/19/2023 2:29 PM   Victor.Gu       1.0         None
"""
import time


def test_abc():
    time.sleep(2.5)


def test_pass():
    pass


def test_fail():
    assert False