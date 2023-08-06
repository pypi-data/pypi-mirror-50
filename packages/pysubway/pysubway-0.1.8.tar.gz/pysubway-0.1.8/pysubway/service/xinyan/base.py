"""
逾期接口，document：https://docs.xinyan.com/docs/fxda-overdue?token=C4GkV156z48h
申请雷达：https://docs.xinyan.com/docs/credit-apply?token=qTb2s8VArJ20

resp
{
    "success": false,
    "data":null,
    "errorCode":"S1000",
    "errorMsg":"请求参数有误"
}

"""
import base64
import json
from typing import Dict, Any

import M2Crypto
import requests
from blinker import signal
from pysubway.errors import IncomingDataError
from pysubway.utils.file import File
from pysubway.utils.hash import hash_md5
from pysubway.utils.ustring import random_key, is_invalid_str
from pysubway.utils.utime import strftime

THIS_DIR = File.this_dir(__file__)


class RsaUtil:

    def __init__(self, private_key: str, current_path: bool = False):
        self.private_key_full_path = File.join_path(THIS_DIR, private_key) if current_path else private_key
        self.private_key = M2Crypto.RSA.load_key(self.private_key_full_path)

    def encrypt(self, digest: str):
        digest = base64.b64encode(digest.encode('utf-8'))
        result = ""
        while (len(digest) > 117):
            some = digest[0:117]
            digest = digest[117:]
            result += self.private_key.private_encrypt(some, M2Crypto.RSA.pkcs1_padding).hex()

        result += self.private_key.private_encrypt(digest, M2Crypto.RSA.pkcs1_padding).hex()

        return result


xinyan_overdue_incoming_data = signal('xinyan_overdue_incoming_data')
xinyan_radar_incoming_data = signal('xinyan_radar_incoming_data')


def xinyan_base(idcard: str,
                id_name: str,
                publisher: Any,
                url: str,
                private_key_path: str,
                phone_no: str = '',
                bankcard_no: str = '',
                member_id: str = '8150751511',
                terminal_id: str = '8150751511') -> Dict:
    """
    :param idcard:
    :param id_name:
    :param phone_no:
    :param bankcard_no:
    :return:
    """
    print('原始入参:', locals())
    try:
        form: Dict = publisher.send(idcard, id_name, phone_no, bankcard_no, member_id, terminal_id).copy()
        form['data_content'] = RsaUtil(private_key_path).encrypt(json.dumps(form['data_content']))
    except IncomingDataError as e:
        return {
            "success": False,
            "data": str(e),
            "errorCode": "S1000",
            "errorMsg": "请求参数有误"
        }
    print('request xinyan_overdue form data', form)
    response = requests.post(url, data=form)
    if response.status_code != response.ok:
        return {
            "success": False,
            "data": f'pysubway formatted: url {url} response status_code is {response.status_code}, not ok',
            "errorCode": "S0001",
            "errorMsg": "系统繁忙，请稍后再试."
        }
    else:
        return response.json()


@xinyan_overdue_incoming_data.connect
def xy_overdue_incoming_data(idcard: str, id_name: str, phone_no: str, bankcard_no: str,
                             member_id: str, terminal_id: str) -> Dict:
    for k, v in dict(idcard=idcard, id_name=id_name).items():
        if is_invalid_str(v):
            raise IncomingDataError(f'param {k} value={v} is invalid')
    incoming_data = {
        'member_id': member_id,
        'terminal_id': terminal_id,
        'data_type': 'json',
        'data_content': {
            'member_id': member_id,
            'terminal_id': terminal_id,
            'trans_id': random_key(50),
            'trade_date': strftime(fmt='%Y%m%d%H%M%S'),
            # MD5(MD5为32位小写)
            'id_no': hash_md5(str(idcard)),
            'id_name': hash_md5(str(id_name)),
            # 'phone_no': phone_no, # may empty
            # 'bankcard_no': bankcard_no, # may empty
            'encrypt_type': 'MD5',
            'versions': '1.3.0'
        }
    }
    if not is_invalid_str(phone_no):
        incoming_data['data_content']['phone_no'] = hash_md5(str(phone_no))
    if not is_invalid_str(bankcard_no):
        incoming_data['data_content']['bankcard_no'] = hash_md5(str(bankcard_no))
    return incoming_data


@xinyan_radar_incoming_data.connect
def xy_radar_incoming_data(idcard: str, id_name: str, phone_no: str, bankcard_no: str,
                           member_id: str, terminal_id: str) -> Dict:
    for k, v in dict(idcard=idcard, id_name=id_name).items():
        if is_invalid_str(v):
            raise IncomingDataError(f'param {k} value={v} is invalid')
    incoming_data = {
        'member_id': member_id,
        'terminal_id': terminal_id,
        'data_type': 'json',
        'data_content': {
            'member_id': member_id,
            'terminal_id': terminal_id,
            'trans_id': random_key(50),
            'trade_date': strftime(fmt='%Y%m%d%H%M%S'),
            # MD5(MD5为32位小写)
            'id_no': hash_md5(str(idcard)),
            'id_name': hash_md5(str(id_name)),
            # 'phone_no': phone_no, # may empty
            # 'bankcard_no': bankcard_no, # may empty
            'encrypt_type': 'MD5',
            'versions': '1.3.0'
        }
    }
    if not is_invalid_str(phone_no):
        incoming_data['data_content']['phone_no'] = hash_md5(str(phone_no))
    if not is_invalid_str(bankcard_no):
        incoming_data['data_content']['bankcard_no'] = hash_md5(str(bankcard_no))
    incoming_data['data_content'] = RsaUtil.encrypt(json.dumps(incoming_data['data_content']))
    return incoming_data


def xinyan_overdue_main(idcard: str,
                        id_name: str,
                        private_key_path: str,
                        url: str = 'https://api.xinyan.com/product/archive/v3/overdue',
                        phone_no: str = '',
                        bankcard_no: str = '',
                        member_id: str = '',
                        terminal_id: str = '') -> Dict:
    return xinyan_base(
        idcard,
        id_name,
        xinyan_overdue_incoming_data,
        url,
        private_key_path,
        phone_no=phone_no,
        bankcard_no=bankcard_no,
        member_id=member_id,
        terminal_id=terminal_id)


def xinyan_radar_main(idcard: str,
                      id_name: str,
                      private_key_path: str,
                      url: str = 'https://api.xinyan.com/product/radar/v3/apply',
                      phone_no: str = '',
                      bankcard_no: str = '',
                      member_id: str = '',
                      terminal_id: str = '') -> Dict:
    return xinyan_base(
        idcard,
        id_name,
        xinyan_radar_incoming_data,
        url,
        private_key_path,
        phone_no=phone_no,
        bankcard_no=bankcard_no,
        member_id=member_id,
        terminal_id=terminal_id)
