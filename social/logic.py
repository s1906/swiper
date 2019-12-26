import datetime

from django.core.cache import cache
from django.db.models import Q

from common import keys
from common import erros
from social.models import Swiped, Friend

from swiper import config
from user.models import User


def get_recd_list(user):
    now = datetime.datetime.now()
    max_birth_year = now.year - user.profile.min_dating_age
    min_birth_year = now.year - user.profile.max_dating_age

    # 查询已经被当前用户滑过的人.
    swiped_list = Swiped.objects.filter(uid=user.id).only('sid')
    # 取出sid
    sid_list = [s.sid for s in swiped_list]
    sid_list.append(user.id)
    # select * from User xxx limit 20
    users =User.objects.filter(location=user.profile.location,
                               birth_year_range=[min_birth_year,
                                                 max_birth_year],
                               sex=user.profile.dating_sex).exclude(id_in=sid_list)[:20]

    data = [user.to_dict() for user in users]
    return data


def like(uid, sid):
    # 穿件一条记录
    Swiped.like(uid, sid)
    # 判断对方是否喜欢我们
    if Swiped.has_like(uid=uid, sid=sid):
        # 如果是,就建立好友关系
        Friend.make_friend(uid1=uid, uid2=sid)
        return True
    return False


def dislike(uid, sid):
    # 创建一条记录
    Swiped.dislike(uid, sid)
    Friend.delete_friend(uid, sid)
    return True


def superlike(uid, sid):
    # 创建一条记录
    Swiped.superlike(uid, sid)
    # 判断对方还是否喜欢我们
    if Swiped.has_like(uid=sid, sid=uid):
        # 如果是就建立好友关系
        Friend.make_friend(uid1=uid, uid2=sid)
        return True
    return False


def rewind(user):
    key = keys.PROFILE_KEY % user.id
    cached_rewinded_times = cache.get(key, 0)
    if cached_rewinded_times < config.MAX_REWIND:
        # 说明当天还有反悔机会
        # 缓存中的反悔次数要加1
        cached_rewinded_times += 1
        now = datetime.datetime.now()
        left_seconds = 86400 - (now.hour * 3600 +now.minute * 60 + now.second)
        cache.set(key, cached_rewinded_times, time = left_seconds)

        # 删除Swiped表中的最近的一条记录
        try:
            record = Swiped.objects.filter(uid=user.id).latest('time')
            # 考虑如果有好友关系, 返回之后,好友关系也应该解除
            Friend.delete_friend(uid1=user.id, uid2=record.sid)
            record.delete()
            return 0, None
        except Swiped.DoesNotExist:
            # return render_json(code=erros.NO_RECORD,data='无操作记录,无法反悔'
            return erros.NO_RECORD, '无操作记录,无法反悔'
    else:
        return erros.EXCEED_MAXIMUM_REWIND, '超过最大反悔次数'


def show_friends(user):
    friends =Friend.objects.filter(Q(uid1=user.id) | Q(uid2=user.id))
    # 把好友的id取出来
    friends_id = []
    for friend in friends:
        if friend.uid1 == user.id:
            friends_id.append(friend.uid2)
        else:
            friends_id.append(friend.uid1)
        # 这种列表推导式不要写,代码可读性太差.
        # [friends_id.append(friend.uid2) if friend.uid1 ==user.id else friends_id.append(friend.uid1) for friend in friends]
        users = User.objects.filter(id_in=friends_id)
        data = [user.to_dict() for user in users]
        return  data
