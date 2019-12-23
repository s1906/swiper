import random
import requests
import resp as resp

from swiper import config
def gen_vode(size=4):
    start = 10 ** (size-1)
    end = 1** size - 1
    return random.randint(start, end)


def send_sms(phone):
    params = config.YZX_PARAMS.copy()
    params['mobile'] = phone
    params['params'] = gen_vode()
    requests.post(config.YZX_URL, json=params)

    if resp.status_code ==200:
        # 说明服务器没有问题
        result = resp.json()
        if result['code'] == '000000':
            return True, 'OK'
        else:
            return False, result['msg']
    else:
        return False, '访问短息服务器有误'

