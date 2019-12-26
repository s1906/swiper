from django.utils.deprecation import MiddlewareMixin

from common import erros
from lib.http import render_json
from user.models import User


class AUthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 判断request的seession中是否存uid,如果存在, 则说明已经登录
        # 不存在就没登录,就提示没有登陆
        uid = request.session.get('uid')
        if not uid:
            return render_json(code=erros.LOGIN_REQUIRED, data='请登录')
        # 如果登陆了, 酒吧user写入request
        user = User.objects.get(id=uid)
        request.user = user