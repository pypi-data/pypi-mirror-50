# example

import json
import traceback
from typing import Any, Dict, Union, Tuple

import flask
from celery import Celery
from flask import abort
from flask.views import MethodView
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from pysubway.async_task.task_notification import emailAbout, dingUrl
from pysubway.cache import FlaskCache
from pysubway.errors import IncomingDataError, RequestFailed
from pysubway.model.guard.company import Company
from pysubway.model.guard.company_product import CompanyProduct
from pysubway.model.guard.product import Product
from pysubway.service.booldata.base import BoolDataBase
from pysubway.service.booldata.hz_risk_model import HzRiskModel
from pysubway.utils.file import File
from pysubway.utils.file import FileIni
from pysubway.utils.ustring import unique_id
from pysubway.view import View
from pysubway.view import ViewUsedCodeBookAndUrlToken

# ********************************* config start ***************************
BOOLDATA_ACCOUNT = dict(
    rsa_prv_key="""-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA3PgggZllwepRByXqAeqrWU4Zx7m+0kvhcbEvpbGTez7PAj8u
IJRKGnH2QfOkZHsRknamuBtJr9c2Js9yrrWbazNPFQrjekprroBSC7DO+EUHQqxZ
mV8ldqukT+C/UOHXavNH3FHnrYSgU7yj4I1+AnAzQq33xbSASE9DkTyoEzJnlRjn
TBopidDVA+P/bxR9z6FBWv8M6P/VAcKamYGIwsx9AbsVhHDd8yOzMDJHOuJza4ku
KFyjf/N+2Fwc7d6ZbKhRYITio7nerw6/XYrcWhAAyB6XhEp3wfCA5SpgCBWGbdve
fiPsme5qqirCy2rlPn76Biev3wW2zhVWTw7HDwIDAQABAoIBABA3vdsFMSy8T9og
dD5TxOO3EblQ7qpsm01G3eJhWBuxjmvxyybk+1NZjeNlSGl/htijELVue0gGmZjb
nOUpuxBxIZq/w9ZT4/dYv6zP+0DJgDDqiWDyVMOS8WpTanc7PB5DYMDQ2hooI8RB
kh2HBPqU1Y5NSmQeTVQBTUo5k3RlGbeAE05U3kVfg6j6xf/67rceCOKa6G+Tkp6h
eebLmuuc19rqg7jBblCsoMgb76P+STlnpvyB8fIYkb1W64bHkX/m4Qj/f4SiDh5t
9W3/bmB+2ygsQCaTPGS9y6z8EfnWZT74Fd+o8XuStubEFw0q+b/BdrmEfL5CjEnO
q57Ep4ECgYEA4/rO82UlKQ6YS0pv4Z7yqPSrJSYwtoazGbGtgp1EHuRk//VEfLOT
4Yo665CbBIrTJxfgZlNkSkBoYaZA8KBg1fP56iuCBUvqBRhSvy94E8dNYjLEjX1q
gskOFrfJ2UaHdp6alctrNSIuWd5q/1LIA4qUBD+mLbnRVWC6dIV2W68CgYEA+CC9
Zw3M1w+5EYWXgq7D6PiDXMjGgvVn+J0/9nDSxVi41zhnxGQD40h/9eNAai67rJHG
xvjK313aUVvMJRSXZuR9Y3zwh1Qb6wUdFgDlGUMuJbazVEgNQDrexf9oCGkvlmPH
/5WDHTOdch07rNaE6/0xnSk45intCIbZy3bEQqECgYACHlWH+3uh6wnNQU7S2OhG
W6eve7BeMdg+N+F14kI8y0CJBF1zjzOjl+Y+RCS8oRGfPmCOct3utrSBm8rksYjU
1CSRYYAeznrJO1Whgy5peKOmcvRSoES6HGYuHd0ZUMd3ebfUBoTjhILLwP5biwhi
yAniFDlWGXDxiymQZaEY7wKBgQC1r6OAdkZro4OsJNoQQtAJIw9tPUa+VdvP27Ue
SvbKsnCGhzLURzfhkRDBh6l/FsEtV4Dp6PsEG8Dkmgcdj7pdCSoXU0D8lsXqjVAC
8JzQprR/wQwGxsuNII5HBQG0RvEleeLUbzIWi9jZ2jX8FQg3lKpjne+f+UsrVzLb
HRgQgQKBgDeMsUFxAeNFN9iHu0IqUboe09ULrZ0NZMHOJ3zoFnuus4sEQpNDC32y
TuzAQumL7z6U5EzzKfdOZX1aAaLoId6+WNjaYkaSD+r/Iz8EzA8V3maip4M2usDl
NLm+JyWqvj9Ze9y7VOgIqRarqjgNwjBoWysNzKIOMpxxItEWUE6b
-----END RSA PRIVATE KEY-----""",
    aes_key='vo8N6ZPawqLDhGj7',
    company_uuid='01b20490-4a1e-11e9-9eb7-247703d210dc',
)

DEV_DB = dict(
    host='47.102.132.18',
    user='root',
    password='qwe123456',
    database='lightning',
)

PROD_DB = dict(
    # open
    host='rm-uf6xfyemz1085v2a48o.mysql.rds.aliyuncs.com',
    # inner
    # host='rm-uf6xfyemz1085v2a4.mysql.rds.aliyuncs.com',
    user='root',
    password='Qwe123456',
    database='lighting',
    inner_platform='inner_platform',
)

EMAIL_LIST = [
    'booleandatamsg@shouxin168.com',
    'booleandatamsg002@shouxin168.com',
    'booleandatamsg003@shouxin168.com',
    'booleandatamsg004@shouxin168.com',
    'booleandatamsg005@shouxin168.com',
]

EMAIL_PASSWORD = 'Qwe123456_'

# remove mypy hints: error: Value of type "object" is not indexable
DB_CONF: Dict[str, Any] = {
    'SQLALCHEMY_DATABASE_URI':
        f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["inner_platform"]}?charset=utf8',
    'SQLALCHEMY_BINDS': {
        'guard': f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["database"]}?charset=utf8',
        'default': f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}'
        f'/{PROD_DB["inner_platform"]}?charset=utf8',
    },
    'SQLALCHEMY_ECHO': True,
}
# ********************************* config end ***************************

# ********************************* constant variable start ***************************
app = flask.Flask(__name__)
CACHE = FlaskCache(app)
app.config.from_mapping(DB_CONF)
SQLAlchemy().init_app(app)
# SQLAlchemy().create_all(app=app)
HASH_SALT = 'sdaer3rf'
KEY_USERNAME = 'userName'
KEY_PASSWORD = 'password'
CODE_BOOK = f'{File.this_dir(__file__)}/static/code_book.ini'
THIS_DIR = File.this_dir(__file__)
KEY_ACCESS_TOKEN = 'access_token'
VIEW_INS = ViewUsedCodeBookAndUrlToken(CODE_BOOK,
                                       CACHE,
                                       KEY_USERNAME,
                                       KEY_PASSWORD,
                                       key_access_token=KEY_ACCESS_TOKEN,
                                       hash_salt=HASH_SALT)
# inner platform web module
MODULE_ACCOUNT_USERNAME = 'account_username'
MODULE_ACCOUNTS_AUTHENTICATION = 'accounts_authentication'
# ++++++++++++++++++++++++
MODULE_EMAIL_NOTIFICATION = 'email_notification'
OPTION_BATCH_TEST = 'batch_test'
# ++++++++++++++++++++++++
MODULE_RECHARGE_MONEY_ACCOUNT = 'recharge_money_account'
# ++++++++++++++++++++++++
MODULE_OPEN_TEST_ACCOUNT = 'open_company_test_account'
# +++++++++++++++++++++++
MODULE_INNER_MODULES = 'inner_modules'
MODULE_USER_MANAGER = 'user_manager'
MODULE_PRODUCT_BATCH_TEST = 'product_batch_test'

DING_TIMOR = 'https://oapi.dingtalk.com/robot/send?access_token=ad34f7787f6232a5c82ccdd30210565ae0de828bc8566d0aebf1e5becf03d263'
DING_CHI_JIAO_DA_XIAN = 'https://oapi.dingtalk.com/robot/send?access_token=73caa869cc06fc5bb37bf853d7d782784f09dd3705d0c31ade9852f4cf444c25'
DING_QI_BAO = 'https://oapi.dingtalk.com/robot/send?access_token=a37dd3149f79bc903ed5b2135dfe988f2e32bf652c85de04b4e531b2669d9ea9'
DEFAULT_RECEIVERS = VIEW_INS.get_code_book_val(MODULE_EMAIL_NOTIFICATION, 'default')
REDIS_DEV = 'redis://47.102.132.18:6379/10'
RESULT_BACKEND = 'db+mysql+pymysql://root:Qwe123456@rm-uf6xfyemz1085v2a48o.mysql.rds.aliyuncs.com/inner_platform?charset=utf8'
APP_CELERY = Celery('async_task')
APP_CELERY.config_from_object('async_task.conf')
APP_CELERY.add_defaults({
    'BROKER_URL': REDIS_DEV,
    'CELERY_RESULT_BACKEND': REDIS_DEV,
})
MgClient = MongoClient(host='47.103.33.79', port=27017, username='root', password='51mongodb!!', authSource="admin")


# ********************************* constant variable end ***************************

# ********************************* tool function start ***************************
def get_real_name(account: str) -> str:
    val = VIEW_INS.get_code_book_val(MODULE_ACCOUNT_USERNAME, account)
    if not isinstance(val, str):
        raise TypeError(f'account {account} get val {val} is not str')
    return val


def open_guard_test_account() -> str:
    # todo open_guard_test_account
    return ''


# ********************************* tool function end ***************************


# ********************************* view function start ***************************
@app.before_request
def verify_token() -> Union[flask.Response, str, None]:
    """
    :key cache key is access_token
    :return:
    """
    return VIEW_INS.verify_before_request()


class BatchTest(MethodView):

    @staticmethod
    def generate_send_msg(real_name: str, remarks: str) -> Tuple[str, str]:
        title = '布尔数据个人信用查询测试申请'
        content = f'申请者: {real_name}\n测试理由：{remarks}' if remarks else ''
        return title, content

    @staticmethod
    def get_company_uuid() -> str:
        return VIEW_INS.login_cache_password

    def len_biz_data(self, biz_data: str) -> int:
        return len(biz_data.split('\n')) - 1

    @staticmethod
    def product_table(key: str) -> str:
        products = {
            'huizumodel': 'batch_test_huizumodel',
            'multi_platforms_v2': 'multi_platforms_v2',

        }
        try:
            return products[key]
        except KeyError:
            raise NotImplementedError(f'product {key} not exist')

    def post(self) -> flask.Response:
        VIEW_INS.check_operation_authority(MODULE_PRODUCT_BATCH_TEST)
        account = VIEW_INS.login_cache_username
        try:
            company_uuid = self.get_company_uuid()
            if not CompanyProduct.has_permission_for_product(company_uuid,
                                                             HzRiskModel.service,
                                                             HzRiskModel.mode):
                raise IncomingDataError(f'company_uuid {company_uuid} do not has_permission_for_product')
            biz_data, product, remarks, specified_receivers = View.request.get_data('biz_data',
                                                                                    'product',
                                                                                    'remarks',
                                                                                    'email')
            real_name = get_real_name(account)
            title, content = self.generate_send_msg(real_name, remarks)
            print('-' * 10)
            email_about = emailAbout(mail_user=EMAIL_LIST[0],
                                     mail_pass=EMAIL_PASSWORD,
                                     title=title,
                                     content=content,
                                     filename='',
                                     receivers=DEFAULT_RECEIVERS,
                                     specified_receivers=specified_receivers)
            # todo for test
            ding_url = dingUrl(ding_msg=DING_TIMOR, ding_exception=DING_TIMOR)
            # ding_url = dingUrl(ding_msg=DING_CHI_JIAO_DA_XIAN, ding_exception=DING_TIMOR)
            async_task_name = self.product_table(product)
            if async_task_name == 'batch_test_huizumodel':
                APP_CELERY.send_task(name=async_task_name,
                                     args=(BOOLDATA_ACCOUNT,
                                           'prod',
                                           company_uuid,
                                           biz_data,
                                           File.this_dir(__file__)),
                                     kwargs={'email_about': email_about,
                                             'ding_url': ding_url})
            elif async_task_name == "multi_platforms_v2":
                print(f'it is calling {async_task_name}, biz_data {biz_data}')
                APP_CELERY.send_task(name=async_task_name,
                                     kwargs={
                                         'input': biz_data,
                                         'input_is_str': True,
                                         'account': BOOLDATA_ACCOUNT,
                                         'names': ('name', 'phone', 'idcard'),
                                         'raise_failed_exception': True,
                                         'output_dir': File.join_path(File.this_dir(__file__), unique_id()),
                                         'email_about': email_about,
                                         'ding_url': ding_url})
            else:
                raise NotImplementedError(f'async_task {async_task_name} not exist')
            return View.response.success()
        except (IncomingDataError, NotImplementedError) as e:
            traceback.print_exc()
            return abort(403)
        except RequestFailed as e:
            APP_CELERY.send_task(name='send_dingding_text', args=(DING_TIMOR, traceback.format_exc()))
            traceback.print_exc()

            def parse_error(e: Exception) -> object:
                return json.loads(str(e))

            error = parse_error(e)
            if isinstance(error, dict) and error.get('resp_code') in BoolDataBase.resp_code_biz_data_error:
                return abort(403)
            else:
                return abort(500)
        except Exception as e:
            APP_CELERY.send_task(name='send_dingding_text', args=(DING_TIMOR, traceback.format_exc()))
            traceback.print_exc()
            return abort(500)


app.add_url_rule('/batch-test-huizu/', view_func=BatchTest.as_view('batch_test_huizu'))


@app.route('/login', methods=['post'])  # type: ignore
def login() -> Union[flask.Response, str]:
    return VIEW_INS.login_with_cache()


@app.route('/companies', methods=['get'])
def display_companies() -> flask.Response:
    return View.response.success({ins.uuid: ins.name for ins in Company.get_all()})


@app.route('/products', methods=['get'])
def get_all_products() -> flask.Response:
    return View.response.success({'/'.join((ins.service_name, ins.mode)): ins.name for ins in Product.get_all()})


@app.route('/products/v2', methods=['get'])
def get_all_products_v2() -> flask.Response:
    result = []
    for ins in Product.get_all():
        result.append({
            'index': '/'.join((ins.service_name, ins.mode)),
            'name': ins.name,
            'price': '0',
        })
    return View.response.success(result)  # type: ignore


@app.route('/modules', methods=['get'])
def get_all_modules() -> flask.Response:
    VIEW_INS.check_operation_authority(MODULE_USER_MANAGER)
    print('get_all_modules >>>>>', FileIni(CODE_BOOK).items(MODULE_INNER_MODULES))
    return VIEW_INS.response.success(dict(FileIni(CODE_BOOK).items(MODULE_INNER_MODULES)))


@app.route('/transfer/official-website', methods=['post'])  # type: ignore
def transfer_official_website() -> None:
    msg, phone, name = VIEW_INS.request.get_data('popup', 'iphoneCode', 'name')
    APP_CELERY.send_task('send_dingding_markdown', ('', f'#官网留言+姓名：{name}+手机号：{phone}+留言内容：{msg}'))


# ********************************* view function end ***************************
if __name__ == '__main__':
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.run(port=8889, host='0.0.0.0', debug=False, use_reloader=True, processes=True)
