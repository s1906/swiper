from django.http import JsonResponse
from django.core.cache import cache

from lib.sms import send_sms
from common import erros
from common import keys
from lib.http import render_json

from user.form import ProfileModelForm
from user.models import User
from user.logic import handle_upload


def summit_phone(request):
    """提交手机号码, 发送验证码"""
    phone = request.POST.get('phone')
    # 发送验证码
    status, msg = send_sms(phone)
    if not status:
        return JsonResponse({'code': erros.SMS_ERROE, 'data': '短信发送失败'})
    else:
        # 发送成功
        return JsonResponse({'code': 0, 'data': None})


def submit_vcode(request):
    """提交手机号, 发送验证码"""
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    # 从缓存中取出vcode
    cached_vcode = cache.get(keys.VCODE_KEY % phone)
    if vcode == cached_vcode:
        # 说明验证码正确, 可以登录或注册
        # try:
        #     user = User.objects.get(phonenum=phone)
        # except User.DoesNotExist:
        #     # 说明是注册
        #     user = User.objects.create(phonenum=phone, nickname=phone)
        user, _ =User.objects.get_or_create(phonenum=phone, defaults={'nickname': phone})

            # 把用户的id存入session,完成登录
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())

    else:
        # 验证码错误
        return render_json(code=erros.VCODE_ERROR, data='验证码错误')

def get_profile(request):
    uid = request.POST.get('uid')
    if not uid:
        return render_json(code=erros.LOGIN_REQUIRED, data='请登录')

    user = User.objects.get(id=uid)
    return render_json(data=user.profile.to_dict())

def edit_profile(request):
    """修改个人资料"""
    form = ProfileModelForm(request.POST)
    if form.is_valid():
        # 可以接收并保存
        profile = form.save(commit=False)
        uid = request.user.id
        profile.id = uid
        profile.save()
        return render_json(data=profile.to_dict())
    return render_json(code=erros.PROFILE_ERROR, data=form.errors)


def upload_avatar(request):
    """上传个人头像"""
    # 获取上传图片数据
    avatar = request.POST.get('avatar')
    print(avatar.name)
    print(avatar.size)
    user = request.user
    handle_upload.delay(user, avatar)
    return render_json()












# def user_form(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             # 取数据
#             nickname = form.cleaned_data['nickname']
#             location = form.cleaned_data['location']
#             sex = form.cleaned_data['sex']
#             age = form.cleaned_data['age']
#             print(nickname, location, sex, age)
#         else:
#             print(form.errors)
#     else:
#         return render_json(request, 'user')

