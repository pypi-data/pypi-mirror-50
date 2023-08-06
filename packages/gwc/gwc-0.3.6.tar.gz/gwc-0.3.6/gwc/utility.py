#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import functools
import random
import time
import os
import sys

import gdpy

from gwc import globals
from gwc.globals import _logger

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser


class catch_exceptions(object):
    """给函数增加重试功能
    :param retry_times: 重试次数 ( **note**: 重试 1 次会执行 2 次函数)
    :param catch_exceptions: 需要捕获的异常，出现这个异常时才进行重试。
                             默认是 ``Exception``
    :rtype catch_exceptions: 单个异常类或者多个异常类组成的 **元组**
    """

    def __init__(self, retry_times=1, catch_exceptions=None):
        self.retry_times = retry_times
        self.catch_exceptions = catch_exceptions or (Exception,)

    def __call__(self, func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            retry_times = kwargs.pop('_retry_times', self.retry_times)

            for n in range(retry_times):
                try:
                    return func(*args, **kwargs)
                except self.catch_exceptions as exc:
                    # 404异常返回到调用处处理
                    if exc.status // 100 == 4:
                        raise

                    # 不捕获特定的异常
                    no_retry_exception(exc, func)

                    random_time = random.randint(n * 60, (1 << n) * 60)
                    _logger.warning('gdpy operation: %s failed. Retry after %d seconds', func.__name__, random_time)
                    print('gdpy operation: {} failed. Retry after {} seconds'.format(func.__name__, random_time))
                    time.sleep(random_time)

                    if n == retry_times - 1:
                        # 最后一次重试失败，重新抛出异常给上一层
                        retry_exception(exc, func)

        return _wrapper


def retry_exception(exc, func):
    """需要重试的异常
    :return:
    """
    if isinstance(exc, gdpy.exceptions.RequestError):
        _logger.warning(
            'Failed to %s! status: %s, error: %s\nNetWork Connection Error, '
            'please check your network and retry.', func.__name__, exc.status,
            exc.error_message.decode('utf-8'))
        print('Failed to {}!\nstatus: {}\nerror: {}\n'.format(func.__name__, exc.status,
                                                              exc.error_message.decode(
                                                                  'utf-8')), file=sys.stderr)
        print('NetWork Connection Error, please check your network and retry.', file=sys.stderr)
        os._exit(-1)
    elif isinstance(exc, gdpy.exceptions.ServerError) and exc.status // 100 == 5:
        print('Please retry, if failed again, contact with the staff of GeneDock.', file=sys.stderr)
        os._exit(-1)


def no_retry_exception(exc, func):
    """不需要重试的异常
    :return:
    """
    if isinstance(exc, ConfigParser.NoSectionError):
        _logger.warning(
            'Can not find section: "{}" in config file: "{}".'.format(exc.section, globals.CONFIGFILE))
        print('Please config your account information.', file=sys.stderr)
        print(
            'Using: "gwc config" or "gwc config -e [endpoint] -i [access_id] -k [access_key]".',
            file=sys.stderr)
        sys.exit(-1)
    elif isinstance(exc, ConfigParser.NoOptionError):
        _logger.warning(
            'Can not find option: "{}" in section: "{}" in config file: "{}".'.format(exc.option,
                                                                                      exc.section,
                                                                                      globals.CONFIGFILE))
        print('Please config your account information.', file=sys.stderr)
        print(
            'Using: "gwc config" or "gwc config -e [endpoint] -i [access_id] -k [access_key]".',
            file=sys.stderr)
        sys.exit(-1)
    elif isinstance(exc, ValueError):
        _logger.warning('Failed to %s! error: %s', func.__name__, exc)
        print('Failed to {}!\nerror: {}'.format(func.__name__, exc), file=sys.stderr)
        os._exit(-1)
    elif isinstance(exc, gdpy.exceptions.ServerError) and exc.status // 100 != 5:
        _logger.warning('Failed to %s! status: %s, error: %s, 错误: %s', func.__name__, exc.status,
                        exc.error_message.decode('utf-8'),
                        exc.error_message_chs.decode('utf-8'))
        print('Failed to {}!\nstatus: {}\nerror: {}\n错误: {}'.format(func.__name__, exc.status,
                                                                    exc.error_message.decode('utf-8'),
                                                                    exc.error_message_chs.decode(
                                                                        'utf-8')), file=sys.stderr)
        os._exit(-1)

