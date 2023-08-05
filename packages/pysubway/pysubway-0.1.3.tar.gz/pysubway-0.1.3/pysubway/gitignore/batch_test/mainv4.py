# example
import json
import traceback
from typing import Any, Optional, Dict, Tuple

import flask
from celery import Celery
from flask import abort
from flask.views import MethodView
from flask_cors import CORS
from pysubway.cache import FlaskCache
from pysubway.errors import IncomingDataError, RequestFailed
from pysubway.model import call_procedure
from pysubway.model import db
from pysubway.model.guard.company import Company
from pysubway.model.guard.company_product import CompanyProduct
from pysubway.model.guard.product import Product
from pysubway.service.aliyun.dingding.robot import Robot
from pysubway.service.aliyun.uemail import Email
from pysubway.service.booldata.base import BoolDataBase
from pysubway.service.booldata.hz_risk_model import HzRiskModel
from pysubway.service.booldata.hz_risk_model import batch_test_used_web
from pysubway.utils.file import File
from pysubway.utils.file import FileIni
from pysubway.utils.utime import strftime
from pysubway.view import View

# todo modify the import
from view import ViewUsedDBAndUrlToken

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

REDIS_URL = 'redis://47.102.132.18:6379/2'

DB_CONF.update(dict(
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_BROKER_URL=REDIS_URL,
    CELERY_RESULT_BACKEND=REDIS_URL,
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TASK_SERIALIZER='json',
    CELERY_TASK_RESULT_EXPIRES=3600 * 24,
    CELERY_ACCEPT_CONTENT=['json', 'json'],
    # CELERY_INCLUDE=[
    #     'task_celery.tasks.sw_tasks.company_balance_monitor.main_monitor',
    #     'task_celery.tasks.sw_tasks.product_called_times_period.main',
    # ],
))

app = flask.Flask(__name__)
CACHE = FlaskCache(app)
app.config.from_mapping(DB_CONF)
db.init_app(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

with app.app_context():
    db.create_all(app=app)
    db.session.commit()
HASH_SALT = 'sdaer3rf'
KEY_USERNAME = 'userName'
KEY_PASSWORD = 'password'
THIS_DIR = File.this_dir(__file__)
KEY_ACCESS_TOKEN = 'access_token'
VIEW_INS = ViewUsedDBAndUrlToken(CACHE,
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

_DING_TIMOR = 'https://oapi.dingtalk.com/robot/send?access_token=ad34f7787f6232a5c82ccdd30210565ae0de828bc8566d0aebf1e5becf03d263'
_DING_CHI_JIAO_DA_XIAN = 'https://oapi.dingtalk.com/robot/send?access_token=73caa869cc06fc5bb37bf853d7d782784f09dd3705d0c31ade9852f4cf444c25'
TIMOR = Robot(_DING_TIMOR)
CHI_JIAO_DA_XIAN = Robot(_DING_CHI_JIAO_DA_XIAN)


def send_timor(text: str) -> None:
    try:
        return TIMOR.send_text(text)
    except Exception as e:
        traceback.print_exc()


def send_chijiaodaxian(text: str) -> None:
    try:
        return CHI_JIAO_DA_XIAN.send_text(text)
    except Exception as e:
        traceback.print_exc()


def get_real_name(account: str) -> str:
    return VIEW_INS.get_code_book_val(MODULE_ACCOUNT_USERNAME, account)


def send_email(mail_user: str = EMAIL_LIST[0],
               mail_pass: str = EMAIL_PASSWORD,
               title: str = '',
               content: str = '',
               specified_receivers: str = '',
               disable_default_receiver: bool = False,
               content_is_file: bool = False) -> None:
    try:
        if disable_default_receiver:
            receivers = specified_receivers
        else:
            receivers = Email.update_receiver(
                VIEW_INS.get_code_book_val(MODULE_EMAIL_NOTIFICATION, 'default'),
                specified_receivers
            )
        Email(mail_user, mail_pass).send_email(title, content, receivers, content_is_file=content_is_file)
    except Exception as e:
        traceback.print_exc()


def send_email_attach(mail_user: str = EMAIL_LIST[0],
                      mail_pass: str = EMAIL_PASSWORD,
                      title: str = '',
                      content: str = '',
                      filename: str = '',
                      specified_receivers: str = '') -> Any:
    try:
        receivers = Email.update_receiver(
            VIEW_INS.get_code_book_val(MODULE_EMAIL_NOTIFICATION, 'default'),
            specified_receivers
        )
        Email(mail_user, mail_pass).send_email_attach(title, content, filename, receivers)
    except Exception as e:
        traceback.print_exc()


def open_guard_test_account() -> str:
    # todo open_guard_test_account
    return ''


@app.before_request
def verify_token() -> Optional[flask.Response]:
    """
    :key cache key is access_token
    :return:
    """
    return VIEW_INS.verify_before_request()


class BatchTestHuizu(MethodView):

    @staticmethod
    def generate_send_msg(real_name, remarks):
        title = '布尔数据个人信用查询测试申请'
        content = f'申请者: {real_name}\n测试理由：{remarks}' if remarks else ''
        return title, content

    @classmethod
    def send_email_batch_test(cls,
                              account: str = '',
                              remarks: str = '',
                              filename: str = '',
                              specified_receivers: str = '') -> None:
        real_name = get_real_name(account)
        title, content = cls.generate_send_msg(real_name, remarks)
        send_email_attach(title=title,
                          content=content,
                          filename=filename,
                          specified_receivers=specified_receivers)

    @staticmethod
    def get_company_uuid() -> str:
        return VIEW_INS.login_cache_password

    @staticmethod
    def batch_test(account_info: Dict[str, str],
                   env: str,
                   company_uuid: str,
                   biz_data: str,
                   raise_failed_exception: bool = True,
                   ) -> Tuple[str, str]:
        biz_data = biz_data if biz_data.startswith('name') else '\n'.join(('name,phone,idcard', biz_data))
        return batch_test_used_web(account_info,
                                   env,
                                   company_uuid,
                                   biz_data,
                                   THIS_DIR,
                                   raise_failed_exception=raise_failed_exception)

    def post(self) -> str:
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
            print('biz_data, product, remarks', biz_data, product, remarks)
            result, output_file = self.batch_test(BOOLDATA_ACCOUNT,
                                                  env='prod',
                                                  company_uuid=company_uuid,
                                                  biz_data=biz_data)
            real_name = get_real_name(account)
            title, content = self.generate_send_msg(real_name, remarks)
            send_chijiaodaxian(f'{title}\n{content}')
            self.send_email_batch_test(account=account,
                                       remarks=remarks,
                                       filename=output_file)
            self.send_email_batch_test(account=account,
                                       remarks='',
                                       filename=output_file,
                                       specified_receivers=specified_receivers)
            return result
        except IncomingDataError as e:
            traceback.print_exc()
            return abort(403)
        except RequestFailed as e:
            traceback.print_exc()

            def parse_error(e: Exception) -> object:
                return json.loads(str(e))

            error = parse_error(e)
            if isinstance(error, dict) and error.get('resp_code') in BoolDataBase.resp_code_biz_data_error:
                return abort(403)
            else:
                send_timor(traceback.format_exc())
                return abort(500)
        except Exception as e:
            send_timor(traceback.format_exc())
            traceback.print_exc()
            return abort(500)


@app.route('/login', methods=['POST'])
def login() -> flask.Response:
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
    return View.response.success(result)


@app.route('/modules', methods=['get'])
def get_all_modules() -> flask.Response:
    VIEW_INS.check_operation_authority(MODULE_USER_MANAGER)
    return VIEW_INS.response.success(dict(FileIni(CODE_BOOK).items(MODULE_INNER_MODULES)))


# @app.route('add/user', methods=['post'])
# def add_user():
#     VIEW_INS.check_operation_authority(MODULE_USER_MANAGER)


# class AddUser(MethodView):
#
#     @staticmethod
#     def send_email(
#             account: str = '',
#             company_name: str = '',
#             recharged_money: int = 0,
#             balanced: int = 0,
#             specified_receivers: str = '') -> None:
#         real_name = get_real_name(account)
#         content = f'{company_name} 于 {strftime()} 充值 {recharged_money} 元，' \
#             f'该公司当前账户余额为 {balanced}, 充值操作者为 {real_name}.'
#         send_email(title='公司充值邮件提醒', content=content, specified_receivers=specified_receivers)
#
#     def add_module_authority(self, module_name: str, english: str, authority_val: bool = True) -> None:
#         FileIni(CODE_BOOK).set(module_name, english, authority_val)
#
#     def register(self, englishname: str, realname: str) -> None:
#         FileIni(CODE_BOOK).set(MODULE_ACCOUNT_USERNAME, englishname, realname)
#         FileIni(CODE_BOOK).set(MODULE_ACCOUNTS_AUTHENTICATION, englishname, open_guard_test_account())
#
#     # def post(self) -> flask.Response:
#     #     VIEW_INS.check_operation_authority(MODULE_USER_MANAGER)
#     #     englishname, realname, email, comment, moduleArr = View.request.get_data('englishname',
#     #                                                                              'realname',
#     #                                                                              'email',
#     #                                                                              'comment',
#     #                                                                              'moduleArr')
#     #     self.register(englishname, realname)
#     #     self.send_email(
#     #         account=VIEW_INS.login_cache_username,
#     #         company_name=ins.name,
#     #         recharged_money=money,
#     #         balanced=ins.balance / 100)
#     #     return View.response.success({"msg": "操作成功"})


class RechargeCompany(MethodView):

    @staticmethod
    def send_email(
            account: str = '',
            company_name: str = '',
            recharged_money: int = 0,
            balanced: int = 0,
            specified_receivers: str = '') -> None:
        real_name = get_real_name(account)
        content = f'{company_name} 于 {strftime()} 充值 {recharged_money} 元，' \
            f'该公司当前账户余额为 {balanced}, 充值操作者为 {real_name}.'
        send_email(title='公司充值邮件提醒', content=content, specified_receivers=specified_receivers)

    def post(self) -> flask.Response:
        company_uuid, money = View.request.get_data('company', 'money')
        print(f'account, money >>>>>> {company_uuid},{money}+++++++++++++++++++')
        VIEW_INS.check_operation_authority(MODULE_RECHARGE_MONEY_ACCOUNT)
        call_procedure(DB_CONF['SQLALCHEMY_BINDS']['guard'], 'company_recharge_money', company_uuid, money)
        ins = Company.get_one(uuid=company_uuid)
        self.send_email(account=VIEW_INS.login_cache_username,
                        company_name=ins.name,
                        recharged_money=money,
                        balanced=ins.balance / 100)
        return View.response.success({"msg": "操作成功"})


class OpenCompanyTestAccount(MethodView):

    @staticmethod
    def open_company_test_account(email: str) -> None:
        file = File.join_path(THIS_DIR, 'static', 'open_company_test_account.html')
        send_email(title='布尔数据测试环境信息',
                   content=file,
                   specified_receivers=email,
                   content_is_file=True,
                   disable_default_receiver=True)

    @staticmethod
    def open_company_prod_account(company_name: str, email: str) -> None:
        pass

    def post(self) -> flask.Response:
        company_name, email, comment = View.request.get_data('company', 'email', 'comment')
        VIEW_INS.check_operation_authority(MODULE_OPEN_TEST_ACCOUNT)
        self.open_company_test_account(email)
        operator = get_real_name(VIEW_INS.login_cache_username)
        send_email(title='测试环境开通账户', content=f'{company_name} 开通布尔数据测试环境, 操作者 {operator}. 备注信息:{comment}')
        return View.response.success({})


app.add_url_rule('/open/company_test_account', view_func=OpenCompanyTestAccount.as_view('open_company_test_account'))
app.add_url_rule('/recharge/company', view_func=RechargeCompany.as_view('recharge_company'))
app.add_url_rule('/batch-test-huizu/', view_func=BatchTestHuizu.as_view('batch_test_huizu'))

if __name__ == '__main__':
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    app.run(port=8889, host='0.0.0.0', debug=False, use_reloader=True, processes=True)
