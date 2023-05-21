# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project: pytest-result-sender03
@File   : test_ini.py
@Contact: 12705290+victorgugit@user.noreply.gitee.com
@License: (C)Copyright 2017-2023

@Modify Time      @Author      @Version      @Description
------------      -------      --------      ------------
5/20/2023 8:25 PM   Victor.Gu       1.0         None
"""
from pathlib import Path

import pytest

from pytest_result_sender import plugin

# pytester是一个内部的、私有的fixture,一般是测开人员才会使用。其他人要想使用先声明
pytest_plugins = "pytester"


@pytest.fixture(autouse=True)
def mock():
    # 创建一个干净的环境
    data_backup = plugin.data
    plugin.data = {
        "passed": 0,
        "failed": 0,
    }

    yield
    # 恢复测试环境
    plugin.data = data_backup


@pytest.mark.parametrize("send_when", ["every", "on_fail"])
def test_send_when(send_when, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when = {send_when}
send_where = https://www.baidu.com
    """
    )

    # 断言pytest.ini配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini("send_when") == send_when

    # 构造一个场景：用例全部测试通过
    pytester.makepyfile(
        """
        def test_pass():
            ...
        """
    )

    pytester.runpytest("-c", str(config_path))

    # Q: 如何断言 插件到底有没有发送测试结果？
    # print(plugin.data)
    if send_when == "every":
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None


@pytest.mark.parametrize("send_where", ["https://www.baidu.com", ""])
def test_send_where(send_where, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when = every
send_where = {send_where}
    """
    )

    # 断言pytest.ini配置加载成功
    config = pytester.parseconfig(config_path)
    assert config.getini("send_where") == send_where

    # 构造一个场景：用例全部测试通过
    pytester.makepyfile(
        """
        def test_pass():
            ...
        """
    )

    pytester.runpytest("-c", str(config_path))

    # Q: 如何断言 插件到底有没有发送测试结果？
    # print(plugin.data)
    if send_where:
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None
