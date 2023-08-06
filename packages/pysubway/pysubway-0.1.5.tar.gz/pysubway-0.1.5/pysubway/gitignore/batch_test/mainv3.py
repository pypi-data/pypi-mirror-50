# # example
# import json
# import traceback
# from typing import Any, Optional, Dict
#
# import flask
# from flask import abort
# from flask.views import MethodView
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from pysubway.cache import FlaskCache
# from pysubway.errors import IncomingDataError, RequestFailed
# from pysubway.model.guard.company import Company
# from pysubway.model.guard.company_product import CompanyProduct
# from pysubway.model.guard.product import Product
# from pysubway.service.booldata.base import BoolDataBase
# from pysubway.service.booldata.hz_risk_model import HzRiskModel
# from pysubway.utils.file import File
# from pysubway.utils.file import FileIni
# from pysubway.view import View
# from pysubway.view import ViewUsedCodeBookAndUrlToken
#
# BOOLDATA_ACCOUNT = dict(
#     rsa_prv_key="""-----BEGIN RSA PRIVATE KEY-----
# MIIEowIBAAKCAQEA3PgggZllwepRByXqAeqrWU4Zx7m+0kvhcbEvpbGTez7PAj8u
# IJRKGnH2QfOkZHsRknamuBtJr9c2Js9yrrWbazNPFQrjekprroBSC7DO+EUHQqxZ
# mV8ldqukT+C/UOHXavNH3FHnrYSgU7yj4I1+AnAzQq33xbSASE9DkTyoEzJnlRjn
# TBopidDVA+P/bxR9z6FBWv8M6P/VAcKamYGIwsx9AbsVhHDd8yOzMDJHOuJza4ku
# KFyjf/N+2Fwc7d6ZbKhRYITio7nerw6/XYrcWhAAyB6XhEp3wfCA5SpgCBWGbdve
# fiPsme5qqirCy2rlPn76Biev3wW2zhVWTw7HDwIDAQABAoIBABA3vdsFMSy8T9og
# dD5TxOO3EblQ7qpsm01G3eJhWBuxjmvxyybk+1NZjeNlSGl/htijELVue0gGmZjb
# nOUpuxBxIZq/w9ZT4/dYv6zP+0DJgDDqiWDyVMOS8WpTanc7PB5DYMDQ2hooI8RB
# kh2HBPqU1Y5NSmQeTVQBTUo5k3RlGbeAE05U3kVfg6j6xf/67rceCOKa6G+Tkp6h
# eebLmuuc19rqg7jBblCsoMgb76P+STlnpvyB8fIYkb1W64bHkX/m4Qj/f4SiDh5t
# 9W3/bmB+2ygsQCaTPGS9y6z8EfnWZT74Fd+o8XuStubEFw0q+b/BdrmEfL5CjEnO
# q57Ep4ECgYEA4/rO82UlKQ6YS0pv4Z7yqPSrJSYwtoazGbGtgp1EHuRk//VEfLOT
# 4Yo665CbBIrTJxfgZlNkSkBoYaZA8KBg1fP56iuCBUvqBRhSvy94E8dNYjLEjX1q
# gskOFrfJ2UaHdp6alctrNSIuWd5q/1LIA4qUBD+mLbnRVWC6dIV2W68CgYEA+CC9
# Zw3M1w+5EYWXgq7D6PiDXMjGgvVn+J0/9nDSxVi41zhnxGQD40h/9eNAai67rJHG
# xvjK313aUVvMJRSXZuR9Y3zwh1Qb6wUdFgDlGUMuJbazVEgNQDrexf9oCGkvlmPH
# /5WDHTOdch07rNaE6/0xnSk45intCIbZy3bEQqECgYACHlWH+3uh6wnNQU7S2OhG
# W6eve7BeMdg+N+F14kI8y0CJBF1zjzOjl+Y+RCS8oRGfPmCOct3utrSBm8rksYjU
# 1CSRYYAeznrJO1Whgy5peKOmcvRSoES6HGYuHd0ZUMd3ebfUBoTjhILLwP5biwhi
# yAniFDlWGXDxiymQZaEY7wKBgQC1r6OAdkZro4OsJNoQQtAJIw9tPUa+VdvP27Ue
# SvbKsnCGhzLURzfhkRDBh6l/FsEtV4Dp6PsEG8Dkmgcdj7pdCSoXU0D8lsXqjVAC
# 8JzQprR/wQwGxsuNII5HBQG0RvEleeLUbzIWi9jZ2jX8FQg3lKpjne+f+UsrVzLb
# HRgQgQKBgDeMsUFxAeNFN9iHu0IqUboe09ULrZ0NZMHOJ3zoFnuus4sEQpNDC32y
# TuzAQumL7z6U5EzzKfdOZX1aAaLoId6+WNjaYkaSD+r/Iz8EzA8V3maip4M2usDl
# NLm+JyWqvj9Ze9y7VOgIqRarqjgNwjBoWysNzKIOMpxxItEWUE6b
# -----END RSA PRIVATE KEY-----""",
#     aes_key='vo8N6ZPawqLDhGj7',
#     company_uuid='01b20490-4a1e-11e9-9eb7-247703d210dc',
# )
#
# DEV_DB = dict(
#     host='47.102.132.18',
#     user='root',
#     password='qwe123456',
#     database='lightning',
# )
#
# PROD_DB = dict(
#     # open
#     host='rm-uf6xfyemz1085v2a48o.mysql.rds.aliyuncs.com',
#     # inner
#     # host='rm-uf6xfyemz1085v2a4.mysql.rds.aliyuncs.com',
#     user='root',
#     password='Qwe123456',
#     database='lighting',
#     inner_platform='inner_platform',
# )
#
# EMAIL_LIST = [
#     'booleandatamsg@shouxin168.com',
#     'booleandatamsg002@shouxin168.com',
#     'booleandatamsg003@shouxin168.com',
#     'booleandatamsg004@shouxin168.com',
#     'booleandatamsg005@shouxin168.com',
# ]
#
# EMAIL_PASSWORD = 'Qwe123456_'
#
# # remove mypy hints: error: Value of type "object" is not indexable
# DB_CONF: Dict[str, Any] = {
#     'SQLALCHEMY_DATABASE_URI':
#         f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["inner_platform"]}?charset=utf8',
#     'SQLALCHEMY_BINDS': {
#         'guard': f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["database"]}?charset=utf8',
#         'default': f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}'
#         f'/{PROD_DB["inner_platform"]}?charset=utf8',
#     },
#     'SQLALCHEMY_ECHO': True,
# }
#
# print(DB_CONF)
#
# app = flask.Flask(__name__)
# CACHE = FlaskCache(app)
# app.config.from_mapping(DB_CONF)
# SQLAlchemy().init_app(app)
# SQLAlchemy().create_all(app=app)
# HASH_SALT = 'sdaer3rf'
# KEY_USERNAME = 'userName'
# KEY_PASSWORD = 'password'
# CODE_BOOK = f'{File.this_dir(__file__)}/static/code_book.ini'
# THIS_DIR = File.this_dir(__file__)
# KEY_ACCESS_TOKEN = 'access_token'
# VIEW_INS = ViewUsedCodeBookAndUrlToken(CODE_BOOK,
#                                        CACHE,
#                                        KEY_USERNAME,
#                                        KEY_PASSWORD,
#                                        key_access_token=KEY_ACCESS_TOKEN,
#                                        hash_salt=HASH_SALT)
# # inner platform web module
# MODULE_ACCOUNT_USERNAME = 'account_username'
# MODULE_ACCOUNTS_AUTHENTICATION = 'accounts_authentication'
# # ++++++++++++++++++++++++
# MODULE_EMAIL_NOTIFICATION = 'email_notification'
# OPTION_BATCH_TEST = 'batch_test'
# # ++++++++++++++++++++++++
# MODULE_RECHARGE_MONEY_ACCOUNT = 'recharge_money_account'
# # ++++++++++++++++++++++++
# MODULE_OPEN_TEST_ACCOUNT = 'open_company_test_account'
# # +++++++++++++++++++++++
# MODULE_INNER_MODULES = 'inner_modules'
# MODULE_USER_MANAGER = 'user_manager'
# MODULE_PRODUCT_BATCH_TEST = 'product_batch_test'
#
# DING_TIMOR = 'https://oapi.dingtalk.com/robot/send?access_token=ad34f7787f6232a5c82ccdd30210565ae0de828bc8566d0aebf1e5becf03d263'
# DING_CHI_JIAO_DA_XIAN = 'https://oapi.dingtalk.com/robot/send?access_token=73caa869cc06fc5bb37bf853d7d782784f09dd3705d0c31ade9852f4cf444c25'
# DEFAULT_RECEIVERS = VIEW_INS.get_code_book_val(MODULE_EMAIL_NOTIFICATION, 'default')
# REDIS_DEV = 'redis://47.102.132.18:6379/10'
# from celery import Celery
#
# celery = Celery(main='async_task')
# celery.config_from_object('async_task.conf')
# celery.add_defaults({
#     'BROKER_URL': REDIS_DEV,
#     'CELERY_RESULT_BACKEND': REDIS_DEV,
# })
# # ASYNC_TASK_ENGINE = generate_celery(REDIS_DEV)
# ASYNC_TASK_BATCH_TEST_HUIZUMODEL = 'batch_test_huizumodel'
# from async_task.task_notification import send_dingding_text, echo_hello
#
#
# def get_real_name(account: str) -> str:
#     return VIEW_INS.get_code_book_val(MODULE_ACCOUNT_USERNAME, account)
#
#
# def open_guard_test_account() -> str:
#     # todo open_guard_test_account
#     return ''
#
#
# @app.before_request
# def verify_token() -> Optional[flask.Response]:
#     """
#     :key cache key is access_token
#     :return:
#     """
#     return VIEW_INS.verify_before_request()
#
#
# # todo
#
# class BatchTest(MethodView):
#
#     @staticmethod
#     def generate_send_msg(real_name, remarks):
#         title = '布尔数据个人信用查询测试申请'
#         content = f'申请者: {real_name}\n测试理由：{remarks}' if remarks else ''
#         return title, content
#
#     @classmethod
#     def send_email_batch_test(cls,
#                               account: str = '',
#                               remarks: str = '',
#                               filename: str = '',
#                               receivers: str = '') -> None:
#         real_name = get_real_name(account)
#         title, content = cls.generate_send_msg(real_name, remarks)
#         celery.send_task('send_email_attach',
#                          (EMAIL_LIST[0], EMAIL_PASSWORD, title, content, filename, receivers))
#
#     @staticmethod
#     def get_company_uuid() -> str:
#         return VIEW_INS.login_cache_password
#
#     def len_biz_data(self, biz_data: str) -> int:
#         return len(biz_data.split('\n')) - 1
#
#     def batch_tes(self, biz_data, company_uuid):
#         result, output_file = self.batch_test_huizumodel(BOOLDATA_ACCOUNT,
#                                                          env='prod',
#                                                          company_uuid=company_uuid,
#                                                          biz_data=biz_data)
#         return result
#
#     def batch_test_platformsv2(self):
#         pass
#
#     def product_table(self, product):
#         table = {
#             'huizumodel': ASYNC_TASK_BATCH_TEST_HUIZUMODEL,
#             'multi_platformsv2': self.batch_test_platformsv2
#         }
#         batch_test = table.get(product)
#         if not batch_test:
#             raise NotImplementedError(f'product {product} not implements')
#         return batch_test
#
#     def post(self) -> str:
#         VIEW_INS.check_operation_authority(MODULE_PRODUCT_BATCH_TEST)
#         account = VIEW_INS.login_cache_username
#         try:
#             company_uuid = self.get_company_uuid()
#             if not CompanyProduct.has_permission_for_product(company_uuid,
#                                                              HzRiskModel.service,
#                                                              HzRiskModel.mode):
#                 raise IncomingDataError(f'company_uuid {company_uuid} do not has_permission_for_product')
#             biz_data, product, remarks, specified_receivers = View.request.get_data('biz_data',
#                                                                                     'product',
#                                                                                     'remarks',
#
#                                                                                     'email')
#             print('xxxxxxxxxxxxx++++++++++++++++++')
#             echo_hello.delay()
#             print('*' * 10, biz_data, product, remarks, specified_receivers)
#             # async_task_name = self.product_table(product)
#             real_name = get_real_name(account)
#             title, content = self.generate_send_msg(real_name, remarks)
#             echo_hello.delay()
#             # result, output_file = '', ''
#             # s = celery.send_task('send_dingding_text',
#             #                                 args=(
#             #                                     DING_TIMOR,
#             #                                     f'{title}\n{content}\n测试了{self.len_biz_data(biz_data)}条.'),
#             #                                 )
#             # print('s' * 10, s)
#             # send_dingding_text.delay(DING_TIMOR, 'xxxxxxxxxx')
#             # w = ASYNC_TASK_ENGINE.send_task(name=ASYNC_TASK_BATCH_TEST_HUIZUMODEL,
#             #                                 args=(BOOLDATA_ACCOUNT,
#             #                                       'prod',
#             #                                       company_uuid,
#             #                                       biz_data),
#             #                                 link=[
#             #                                     signature(
#             #                                         'send_email_attach',
#             #                                         (EMAIL_LIST[0], EMAIL_PASSWORD, title, content, output_file,
#             #                                          specified_receivers)),
#             #                                     signature(
#             #                                         'send_email_attach',
#             #                                         (EMAIL_LIST[0], EMAIL_PASSWORD, title, content, output_file,
#             #                                          DEFAULT_RECEIVERS)),
#             #                                 ],
#             #                                 link_error=signature('send_dingding_text', (DING_CHI_JIAO_DA_XIAN, '错误'))
#             #                                 )
#             # print('-' * 10, w)
#             # s = ASYNC_TASK_ENGINE.send_task('send_dingding_text',
#             #                                 args=(
#             #                                     DING_CHI_JIAO_DA_XIAN,
#             #                                     f'{title}\n{content}\n测试了{self.len_biz_data(biz_data)}条.'),
#             #                                 )
#             # print('s' * 10, s)
#             return View.response.success()
#         except (IncomingDataError, NotImplementedError) as e:
#             traceback.print_exc()
#             return abort(403)
#         except RequestFailed as e:
#             traceback.print_exc()
#
#             def parse_error(e: Exception) -> object:
#                 return json.loads(str(e))
#
#             error = parse_error(e)
#             if isinstance(error, dict) and error.get('resp_code') in BoolDataBase.resp_code_biz_data_error:
#                 return abort(403)
#             else:
#                 celery.send_task('send_dingding_text',
#                                             (DING_TIMOR, traceback.format_exc())
#                                             )
#                 return abort(500)
#         except Exception as e:
#             traceback.print_exc()
#             celery.send_task('send_dingding_text',
#                                         (DING_TIMOR, traceback.format_exc())
#                                         )
#             return abort(500)
#
#
# app.add_url_rule('/batch-test-huizu/', view_func=BatchTest.as_view('batch_test_huizu'))
#
#
# @app.route('/login', methods=['POST'])
# def login() -> flask.Response:
#     return VIEW_INS.login_with_cache()
#
#
# @app.route('/companies', methods=['get'])
# def display_companies() -> flask.Response:
#     return View.response.success({ins.uuid: ins.name for ins in Company.get_all()})
#
#
# @app.route('/products', methods=['get'])
# def get_all_products() -> flask.Response:
#     return View.response.success({'/'.join((ins.service_name, ins.mode)): ins.name for ins in Product.get_all()})
#
#
# @app.route('/products/v2', methods=['get'])
# def get_all_products_v2() -> flask.Response:
#     result = []
#     for ins in Product.get_all():
#         result.append({
#             'index': '/'.join((ins.service_name, ins.mode)),
#             'name': ins.name,
#             'price': '0',
#         })
#     return View.response.success(result)
#
#
# @app.route('/modules', methods=['get'])
# def get_all_modules() -> flask.Response:
#     VIEW_INS.check_operation_authority(MODULE_USER_MANAGER)
#     print('get_all_modules >>>>>', FileIni(CODE_BOOK).items(MODULE_INNER_MODULES))
#     return VIEW_INS.response.success(dict(FileIni(CODE_BOOK).items(MODULE_INNER_MODULES)))
#
#
# if __name__ == '__main__':
#     CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
#     app.run(port=8889, host='0.0.0.0', debug=False, use_reloader=True, processes=True)
