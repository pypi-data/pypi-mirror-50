# -*- encoding: utf-8 -*-
# create_date: 2019-08-02
# author: Paradox

"""
封装与时间有关的所有的操作
"""
import datetime


def get_current_datetime():
    """
    获取当前的时间
    :return: datetime格式
    """
    return datetime.datetime.now()


def get_current_date_and_hour():
    """
    获取当前的日期和小时
    :return: int格式
    """
    return convert_date_to_str(datetime.date.today()), get_current_datetime().hour


def convert_date_to_str(date):
    """
    将日期格式化为字符串的格式返回
    :param date: 待转换的日期
    :return: 转换完成后的日期字符串: "2019-05-12"
    """
    return date.strftime("%Y-%m-%d")


def get_date_by_days(days):
    """
    获取过去或将来的某个日期，例如：days=1，为明天的日期， days=-1，为昨天的日期
    :param days:
    :return: date格式
    """
    today = datetime.date.today()
    return today + datetime.timedelta(days=days)


def get_today():
    """
    获取今天的日期
    :return: date格式
    """
    return datetime.date.today()
