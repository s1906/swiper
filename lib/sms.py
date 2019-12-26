import random
import requests
from django.core.cache import cache

from common import keys
from swiper import config
from worker import celery_app


def gen_vcode(size=4):
    start = 10 ** (size-1)
    end = 10 ** size - 1
    return random.randint(start, end)


@celery_app.task
def send_sms(phone):
    params = config.YZX_PARAMS.copy()
    params['mobile'] = phone
    vcode = gen_vcode()
    cache.set(keys.VCODE_KEY % phone, vcode, timeout=300)
    params['params'] = gen_vcode()
    resp = requests.post(config.YZX_URL, json=params)

    if resp.status_code == 200:
        # 说明服务器没有问题
        result = resp.json()
        if result['code'] == '000000':
            return True, 'OK'
        else:
            return False, result['msg']
    else:
        return False, '访问短息服务器有误'

