from django.db import models


class Swiped(models.Model):
    MARK = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('superlike', 'superlike')
    )
    uid = models.IntegerField(verbose_name='用户自身id')  ,
    sid = models.IntegerField(verbose_name='被滑的陌生人id'),
    mark = models.CharField(max_length=128, verbose_name='滑动类型', choices=MARK)
    time = models.DateTimeField(verbose_name='滑动的时间', auto_now_add=True)

    @classmethod
    def like(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='like')

    @classmethod
    def dislike(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='dislike')

    @classmethod
    def superlike(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=uid, mark='superlike')

    @classmethod
    def has_like(cls, uid, sid):
        return cls.objects.filter(uid=uid, sid=sid).exists()


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        friendship = cls.objects.create(uid1=uid1, uid2=uid2)
        return friendship

    @classmethod
    def is_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return Friend.objects.create(uid1=uid1, uid2=uid2)

    @classmethod
    def delete_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return Friend.objects.filter(uid1=uid1, uid2=uid2).delete()
