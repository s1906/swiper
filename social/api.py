from django.shortcuts import render

from lib.http import render_json
from social import logic


def get_recd_list(request):
    """获取推荐列表"""
    # 注意事项: 1. 已经滑过的人,不应该再出现
    # 2. 自己也不能出现在推荐列表
    # 3. 只推荐符合自己交友资料的用户
    user = request.user
    # 根据最大和最小的交友年龄计算对方的出生年份
    data = logic.get_recd_list(user)
    return render_json(data=data)


def like(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.like(user.id, sid)
    return render_json(data={'match': flag})


def dislike(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.dislike(user.id, sid)
    return render_json(data={'unmatch': flag})


def superlike(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.dislike((user.id, sid))
    return render_json(data={'match': flag})


def rewind(request):
    """
    每天允许反悔3ci,把已经反悔的次数记录在redis中.
    内次执行反悔之前, 先判断反悔次数是否小于配置的丹田最大反悔次数
    """
    # 先从缓存中获取大年已经反悔的次数.
    user = request.user
    code, data =logic.rewind(user)
    return render_json(code, data)


def show_friends(request):
    """
    查看好友列表
    """
    user = request.user
    data = logic.show_friends(user)
    return render_json(data=data)