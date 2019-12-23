from django.shortcuts import render

from lib.sms import send_sms
from common import erros
from common import keys


# Create your views here.
from django.core.cache import cache

def summit_phone(request):
    """提交手机号码, 发送验证码"""
    phone = request.POST.get('phone')
    # 发送验证码
    status, msg = send_sms(phone)
    if not status:
        return