# _*_ coding:utf-8 _*_
__author__ = 'WANGY'
__date__ = '2019/8/17 9:37'

import datetime


def get_first_last_day_in_week():
    """
    获取当周周一的日期和下周一的日期
    :return:
    """
    today = datetime.date.today()
    weekday = today.weekday()  # 获取当前周的排序, 周一为0, 周日为6
    monday_delta = datetime.timedelta(weekday)  # 当前日期距离周一的时间差
    sunday_delta = datetime.timedelta(7 - weekday)  # 当前日期距离下周一的时间差
    monday = today - monday_delta  # 获取这周一日期
    next_monday = today + sunday_delta  # 获取下周一日期
    return monday, next_monday


def get_previous_day(days=1):
    """
    获取当前日期之前某一天的日期，默认是昨天
    :param days:
    :return:
    """
    today = datetime.date.today()
    delta = datetime.timedelta(days=days)
    previous_day = today - delta
    return today, previous_day


def get_yesterday_day():
    """
    获取昨天日期
    :return:
    """
    today, yesterday = get_previous_day()
    return today, yesterday


def get_next_day(days=1):
    """
    获取当前日期之后某一天的日期，默认是明天
    :param days:
    :return:
    """
    today = datetime.date.today()
    delta = datetime.timedelta(days=days)
    next_day = today + delta
    return today, next_day


def get_tomorrow_day():
    """
    获取明天日期
    :param days:
    :return:
    """
    today, tomorrow = get_next_day()
    return today, tomorrow
