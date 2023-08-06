# """
# this is example of using ViewUsedCodeBookAndUrlToken
# """
#
# import json
# import traceback
# from typing import Any, Optional, Dict, Tuple
#
# import flask
# from flask import abort
# from flask.views import MethodView
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from pysubway.cache import FlaskCache
# from pysubway.errors import IncomingDataError, RequestFailed
# from pysubway.model import call_procedure
# from pysubway.model.guard.company import Company
# from pysubway.model.guard.company_product import CompanyProduct
# from pysubway.model.guard.product import Product
# from pysubway.service.aliyun.dingding.robot import Robot
# from pysubway.service.aliyun.uemail import Email
# from pysubway.service.booldata.base import BoolDataBase
# from pysubway.service.booldata.hz_risk_model import HzRiskModel
# from pysubway.service.booldata.hz_risk_model import batch_test_used_web
# from pysubway.utils.file import File
# from pysubway.utils.file import FileIni
# from pysubway.utils.utime import strftime
# from pysubway.view import View
# from pysubway.view import ViewUsedCodeBookAndUrlToken
#
# BOOLDATA_ACCOUNT = dict(
#     rsa_prv_key="""""",
#     aes_key='',
#     company_uuid='',
# )
#
# PROD_DB = dict(
#     # open
#     host='',
#     user='root',
#     password='',
#     database='',
# )
#
# EMAIL_LIST = [
#     'jack@qq.com',
# ]
#
# EMAIL_PASSWORD = 'i can not tell you'
#
# # remove mypy hints: error: Value of type "object" is not indexable
# DB_CONF: Dict[str, Any] = {
#     'SQLALCHEMY_DATABASE_URI':
#         f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["database"]}?charset=utf8',
#     'SQLALCHEMY_BINDS': {
#         'guard': f'mysql+pymysql://root:{PROD_DB["password"]}@{PROD_DB["host"]}/{PROD_DB["database"]}?charset=utf8'
#     },
# }
#
# _DING_TIMOR = 'dingding robot url'
# _DING_CHI_JIAO_DA_XIAN = 'dingding robot url'
#
# app = flask.Flask(__name__)
# CACHE = FlaskCache(app)
# app.config.from_mapping(DB_CONF)
# SQLAlchemy().init_app(app)
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
# # inner platform web section
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
# TIMOR = Robot(_DING_TIMOR)
# CHI_JIAO_DA_XIAN = Robot(_DING_CHI_JIAO_DA_XIAN)
#
#
# def send_timor(text: str) -> None:
#     try:
#         return TIMOR.send_text(text)
#     except Exception as e:
#         traceback.print_exc()
#
#
# def send_chijiaodaxian(text: str) -> None:
#     try:
#         return CHI_JIAO_DA_XIAN.send_text(text)
#     except Exception as e:
#         traceback.print_exc()
#
#
# def get_real_name(account: str) -> str:
#     result = VIEW_INS.get_code_book_val(MODULE_ACCOUNT_USERNAME, account)
#     if isinstance(result, bool):
#         raise TypeError(f'result {result} should be str')
#     return result
#
#
# def send_email(mail_user: str = EMAIL_LIST[0],
#                mail_pass: str = EMAIL_PASSWORD,
#                title: str = '',
#                content: str = '',
#                specified_receivers: str = '',
#                disable_default_receiver: bool = False,
#                content_is_file: bool = False) -> None:
#     try:
#         if disable_default_receiver:
#             receivers = specified_receivers
#         else:
#             receivers = Email.update_receiver(
#                 VIEW_INS.get_code_book_val(MODULE_EMAIL_NOTIFICATION, 'default'),
#                 specified_receivers
#             )
#         Email(mail_user, mail_pass).send_email(title, content, receivers, content_is_file=content_is_file)
#     except Exception as e:
#         traceback.print_exc()
#
#
# def send_email_attach(mail_user: str = EMAIL_LIST[0],
#                       mail_pass: str = EMAIL_PASSWORD,
#                       title: str = '',
#                       content: str = '',
#                       filename: str = '',
#                       specified_receivers: str = '') -> Any:
#     try:
#         receivers = Email.update_receiver(
#             VIEW_INS.get_code_book_val(MODULE_EMAIL_NOTIFICATION, 'default'),
#             specified_receivers
#         )
#         Email(mail_user, mail_pass).send_email_attach(title, content, filename, receivers)
#     except Exception as e:
#         traceback.print_exc()
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
# class BatchTestHuizu(MethodView):
#
#     @staticmethod
#     def generate_send_msg(real_name, remarks):
#         title = 'Test Application'
#         content = f'applicant: {real_name}\ntest reason：{remarks}' if remarks else ''
#         return title, content
#
#     @classmethod
#     def send_email_batch_test(cls,
#                               account: str = '',
#                               remarks: str = '',
#                               filename: str = '',
#                               specified_receivers: str = '') -> None:
#         real_name = get_real_name(account)
#         title, content = cls.generate_send_msg(real_name, remarks)
#         send_email_attach(title=title,
#                           content=content,
#                           filename=filename,
#                           specified_receivers=specified_receivers)
#
#     @staticmethod
#     def get_company_uuid() -> str:
#         return VIEW_INS.login_cache_password
#
#     @staticmethod
#     def batch_test(account_info: Dict[str, str],
#                    env: str,
#                    company_uuid: str,
#                    biz_data: str,
#                    raise_failed_exception: bool = True,
#                    ) -> Tuple[str, str]:
#         biz_data = biz_data if biz_data.startswith('name') else '\n'.join(('name,phone,idcard', biz_data))
#         return batch_test_used_web(account_info,
#                                    env,
#                                    company_uuid,
#                                    biz_data,
#                                    THIS_DIR,
#                                    raise_failed_exception=raise_failed_exception)
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
#                                                                                     'email')
#             print('biz_data, product, remarks', biz_data, product, remarks)
#             result, output_file = self.batch_test(BOOLDATA_ACCOUNT,
#                                                   env='prod',
#                                                   company_uuid=company_uuid,
#                                                   biz_data=biz_data)
#             real_name = get_real_name(account)
#             title, content = self.generate_send_msg(real_name, remarks)
#             send_chijiaodaxian(f'{title}\n{content}')
#             self.send_email_batch_test(account=account,
#                                        remarks=remarks,
#                                        filename=output_file)
#             self.send_email_batch_test(account=account,
#                                        remarks='',
#                                        filename=output_file,
#                                        specified_receivers=specified_receivers)
#             return result
#         except IncomingDataError as e:
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
#                 send_timor(traceback.format_exc())
#                 return abort(500)
#         except Exception as e:
#             send_timor(traceback.format_exc())
#             traceback.print_exc()
#             return abort(500)
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
#         content = f'{company_name} 于 {strftime()} recharge ￥{recharged_money}，' \
#             f'company current balance {balanced}, operator {real_name}.'
#         send_email(title='Balance Notification', content=content, specified_receivers=specified_receivers)
#
#     def add_module_authority(self, module_name: str, english: str, authority_val: bool = True) -> None:
#         FileIni(CODE_BOOK).set(module_name, english, authority_val)
#
#     def register(self, englishname: str, realname: str) -> None:
#         FileIni(CODE_BOOK).set(MODULE_ACCOUNT_USERNAME, englishname, realname)
#         FileIni(CODE_BOOK).set(MODULE_ACCOUNTS_AUTHENTICATION, englishname, open_guard_test_account())
#
#
# class RechargeCompany(MethodView):
#
#     @staticmethod
#     def send_email(
#             account: str = '',
#             company_name: str = '',
#             recharged_money: int = 0,
#             balanced: int = 0,
#             specified_receivers: str = '') -> None:
#         real_name = get_real_name(account)
#         content = f'{company_name} 于 {strftime()} recharge ￥{recharged_money}，' \
#             f'company current balance {balanced}, operator {real_name}.'
#         send_email(title='Balance Notification', content=content, specified_receivers=specified_receivers)
#
#     def post(self) -> flask.Response:
#         company_uuid, money = View.request.get_data('company', 'money')
#         print(f'account, money >>>>>> {company_uuid},{money}+++++++++++++++++++')
#         VIEW_INS.check_operation_authority(MODULE_RECHARGE_MONEY_ACCOUNT)
#         call_procedure(DB_CONF['SQLALCHEMY_BINDS']['guard'], 'company_recharge_money', company_uuid, money)
#         ins = Company.get_one(uuid=company_uuid)
#         self.send_email(account=VIEW_INS.login_cache_username,
#                         company_name=ins.name,
#                         recharged_money=money,
#                         balanced=ins.balance / 100)
#         return View.response.success({"msg": "success"})
#
#
# class OpenCompanyTestAccount(MethodView):
#
#     @staticmethod
#     def open_company_test_account(email: str) -> None:
#         file = File.join_path(THIS_DIR, 'static', 'open_company_test_account.html')
#         send_email(title='Product Test Env',
#                    content=file,
#                    specified_receivers=email,
#                    content_is_file=True,
#                    disable_default_receiver=True)
#
#     @staticmethod
#     def open_company_prod_account(company_name: str, email: str) -> None:
#         pass
#
#     def post(self) -> flask.Response:
#         company_name, email, comment = View.request.get_data('company', 'email', 'comment')
#         VIEW_INS.check_operation_authority(MODULE_OPEN_TEST_ACCOUNT)
#         self.open_company_test_account(email)
#         operator = get_real_name(VIEW_INS.login_cache_username)
#         send_email(title='Add Account of Product Test Env',
#                    content=f'{company_name} add account of product test env, operator {operator}. comment:{comment}')
#         return View.response.success({})
#
#
# app.add_url_rule('/open/company_test_account', view_func=OpenCompanyTestAccount.as_view('open_company_test_account'))
# app.add_url_rule('/recharge/company', view_func=RechargeCompany.as_view('recharge_company'))
# app.add_url_rule('/batch-test-huizu/', view_func=BatchTestHuizu.as_view('batch_test_huizu'))
#
# if __name__ == '__main__':
#     CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
#     app.run(port=8889, host='0.0.0.0', debug=False, use_reloader=True, processes=True)
