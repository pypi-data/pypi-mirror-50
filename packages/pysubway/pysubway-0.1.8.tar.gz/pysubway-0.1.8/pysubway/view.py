import traceback
from typing import Dict, Any, Union, Tuple, Optional

import flask
from flask import abort
from flask import request
from flask_restful import Resource
from pymongo import MongoClient

from .cache import FlaskCache
from .domain import PermissionFactory
from .errors import AuthenticationFailed
from .errors import IncomingDataValueError
from .model.role import Role
from .model.role_permission import RolePermission
from .model.user import User
from .request import Request
from .response import Response
from .service.authentication import AuthenticationFactory
from .utils.file import FileIni
from .utils.package import Package

__all__ = [
    'ViewRestful', 'View'
]


class View:
    request: Request = Request()
    response = Response()

    @classmethod
    def login(cls,
              key_username: str,
              key_password: str,
              response_data: flask.Response,
              is_aborted: bool = True,
              prompt: str = 'account or password is wrong',
              style: str = 'file',
              **kwargs: Any) -> Union[flask.Response, str]:
        """
        login method.

        :param key_username: username key of the incoming data
        :param key_password: username password of the incoming data
        :param response_data: if authenticated successfully, response data.
        :param is_aborted: if not abort, raise  AuthenticationFailed exception.
        :param style: authentication style, default file
        :param prompt: if authenticated failed, the prompt information.
        :param kwargs:
            about the kwargs,please refer to AuthenticationFactory
            if authentication style is file, kwargs is:
                code_book=f'{File.this_dir(__file__)}/static/code_book.ini', section='huizumodel'
        :return:
        """
        account, password = cls.request.get_data(key_username, key_password)
        is_authenticated = AuthenticationFactory(style)(**kwargs).is_authenticated(account, password)  # type: ignore
        if not is_authenticated:
            return cls.response.handle_exception(AuthenticationFailed(prompt), is_aborted, 401)
        return response_data

    # debug: this part will catch all exception including abort exception
    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     print(e)
    #     return abort(500)


class ViewUsedCodeBookAndUrlToken(View):
    """
    configure refer to example

;******************* must existed configure start *******************
[accounts_authentication]
; this section is used for authentication.
; all accounts must register here.
jack = jack's password
[account_username]
; key is account name, value is username
jack = 张三
;******************* must existed configure end *******************
[section-01]
; the value of account is true that can access the section-01
jack = True
"""

    def __init__(self,
                 code_book: str,
                 cache_ins: Any,
                 key_username: str,
                 key_password: str,
                 key_access_token: str = 'access_token',
                 section_authentication: str = 'accounts_authentication',
                 hash_salt: str = 'ishardguesssalt!!!'):
        """
        View class that is suit for code book stored and token passed in url

        :param code_book: the code book that saved account info
        :param cache_ins: like Flask cache redis ...
        :param key_username: key of username  when request login url
        :param key_password: key of password  when request login url
        :param key_access_token: the key in the url, it's like
        :param section_authentication: section name that records account and password in code book ini
        :param hash_salt: that is used to generate token
        """
        self.code_book = code_book
        self.section_authentication = section_authentication
        self.cache_ins = cache_ins
        self.key_access_token = key_access_token
        self.key_username = key_username
        self.key_password = key_password
        self.hash_salt = hash_salt

    def get_code_book_val(self,
                          section: str,
                          option: str,
                          default: Union[str, bool] = '',
                          val_type: str = '') -> Union[str, bool]:
        return FileIni(self.code_book).get_val(section, option, default=default, val_type=val_type)

    def generate_token(self, account: str, password: str, hash_salt: str) -> str:
        result = FlaskCache.generate_token(account + password, hash_salt)
        if not isinstance(result, str):
            raise TypeError(f'generated token {result} is not str')
        return result

    def generate_login_cache(self,
                             token: str,
                             account: str,
                             password: str) -> None:
        self.cache_ins.set(token, {self.key_username: account, self.key_password: password})

    @property
    def login_cache(self) -> Dict[str, str]:
        return self.cache_ins.get(request.args.get(self.key_access_token)) or dict()

    @property
    def login_cache_password(self) -> str:
        return self.login_cache[self.key_password]

    @property
    def login_cache_username(self) -> str:
        return self.login_cache[self.key_username]

    def is_valid_token(self) -> bool:
        # todo verify account and password
        return bool(self.login_cache)

    def login_with_cache(self) -> Union[flask.Response, str]:
        account, password = View.request.get_data(self.key_username, self.key_password)
        token = self.generate_token(account, password, self.hash_salt)
        self.generate_login_cache(token, account, password)
        try:
            return View.login(self.key_username,
                              self.key_password,
                              self.response.login_succeed(token),
                              is_aborted=True,
                              code_book=self.code_book,
                              section=self.section_authentication)
        except AuthenticationFailed:
            self.cache_ins.delete(token)
            return View.response.login_fail()
        except Exception as e:
            traceback.print_exc()
            self.cache_ins.delete(token)
            return abort(500)

    def verify_before_request(self,
                              exclude_path: Tuple[str, ...] = ('/login',),
                              can_abort: bool = True,
                              failed_info: str = '') -> Union[flask.Response, str, None]:
        """
        get token from url and verify it.
        the url is like http://wxadas?access_token=xxxx
        example:

        @app.before_request
        def verify_token() -> Optional[flask.Response]:
            pass

        :param cache_ins: a cache ins that implemented get method and cache tokens
        :param key_token: the key in the url
        :param exclude_path: these paths will be excluded to verify token
        :param failed_info: failed to pass verify and return the info
        :return:
        """
        if request.path not in exclude_path:
            # debug: options is like a ping of chrome browser. 跨域请求前会浏览器会自动进行此操作.
            if not self.is_valid_token() and request.method != 'OPTIONS':
                if can_abort:
                    return abort(401)
                return failed_info
        return None

    def check_operation_authority(self, section: str) -> Optional[str]:
        """
        check current user has authority to operate the section.

        code book configure like:
        [section]
        ; allowed
        username=True
        ; forbidden
        username=False
        :param section: match current name

        example:

        def post(self):
            check_operation(can_open_company_account)

        :return:
        """
        login_cache = self.cache_ins.get(request.args.get(self.key_access_token))
        if not isinstance(login_cache, dict):
            return abort(403)
        username = login_cache.get(self.key_username, '')
        if not FileIni(self.code_book).is_true(section, username):
            return abort(403)
        return None


class ViewUsedMongoAndUrlToken(View):
    """
    accounts collections:
    {'account_name':'',
    'company_uuid':'',
    'password':'',
    'real_name':'real_name'}

    block_permission collection:
    {
        'account_name':'',
        'block_name': bool,
    }
    """

    def __init__(self,
                 db_name: str,
                 mgClient: MongoClient,
                 cache_ins: Any,
                 key_username: str,
                 key_password: str,
                 kc_accounts: str = 'accounts',
                 kc_block_permission: str = 'block_permission',
                 key_access_token: str = 'access_token',
                 section_authentication: str = 'accounts_authentication',
                 hash_salt: str = 'ishardguesssalt!!!'):
        """
        View class that is suit for code book stored and token passed in url

        :param mgClient: mgClient as backend that saved account info
        :param cache_ins: like Flask cache redis ...
        :param key_username: key of username  when request login url
        :param key_password: key of password  when request login url
        :param key_access_token: the key in the url, it's like
        :param section_authentication: section name that records account and password in code book ini
        :param hash_salt: that is used to generate token
        """
        self.db_name = db_name
        self.mgClient = mgClient
        self.section_authentication = section_authentication
        self.cache_ins = cache_ins
        self.key_access_token = key_access_token
        self.kc_accounts = kc_accounts
        self.kc_block_permission = kc_block_permission
        self.key_username = key_username
        self.key_password = key_password
        self.hash_salt = hash_salt

    def generate_token(self, account: str, password: str, hash_salt: str) -> str:
        result = FlaskCache.generate_token(account + password, hash_salt)
        if not isinstance(result, str):
            raise TypeError(f'generated token {result} is not str')
        return result

    def generate_login_cache(self,
                             token: str,
                             account: str,
                             password: str) -> None:
        self.cache_ins.set(token, {self.key_username: account, self.key_password: password})

    @property
    def login_cache(self) -> Dict[str, str]:
        token = request.args.get(self.key_access_token)
        return self.cache_ins.get(token) or dict()

    @property
    def login_cache_password(self) -> str:
        return self.login_cache[self.key_password]

    @property
    def login_cache_username(self) -> str:
        return self.login_cache[self.key_username]

    def is_valid_token(self) -> bool:
        # todo verify account and password
        return bool(self.login_cache)

    def login_with_cache(self) -> Union[flask.Response, str]:
        account, password = View.request.get_data(self.key_username, self.key_password)
        token = self.generate_token(account, password, self.hash_salt)
        self.generate_login_cache(token, account, password)
        try:
            return View.login(self.key_username,
                              self.key_password,
                              self.response.login_succeed(token),
                              is_aborted=True,
                              style='mongo',
                              client=self.mgClient,
                              db_name=self.db_name,
                              collection=self.kc_accounts,
                              section=self.section_authentication)
        except AuthenticationFailed:
            self.cache_ins.delete(token)
            return View.response.login_fail()
        except Exception as e:
            traceback.print_exc()
            self.cache_ins.delete(token)
            return abort(500)

    def verify_before_request(self,
                              exclude_path: Tuple[str, ...] = ('/login',),
                              can_abort: bool = True,
                              failed_info: str = '') -> Union[flask.Response, str, None]:
        """
        get token from url and verify it.
        the url is like http://wxadas?access_token=xxxx
        example:

        @app.before_request
        def verify_token() -> Optional[flask.Response]:
            pass

        :param cache_ins: a cache ins that implemented get method and cache tokens
        :param key_token: the key in the url
        :param exclude_path: these paths will be excluded to verify token
        :param failed_info: failed to pass verify and return the info
        :return:
        """
        if request.path not in exclude_path:
            # debug: options is like a ping of chrome browser. 跨域请求前会浏览器会自动进行此操作.
            if not self.is_valid_token() and request.method != 'OPTIONS':
                if can_abort:
                    return abort(401)
                return failed_info
        return None

    def check_operation_authority(self, block: str) -> Optional[str]:
        """
        check current user has authority to operate the section.

        collection: default self.kc_block_permission kc_block_permission
        :param section: block name
        example:

        def post(self):
            check_operation(can_open_company_account)

        :return:
        """
        login_cache = self.cache_ins.get(request.args.get(self.key_access_token))
        if not isinstance(login_cache, dict):
            return abort(403)
        username = login_cache.get(self.key_username, '')
        result = self.mgClient[self.db_name][self.kc_block_permission].find_one({'account_name': username})
        if not result or not result.get(block):
            return abort(403)
        return None


class ViewUsedDBAndUrlToken(View):
    """
    configure refer to example
    """

    def __init__(self,
                 cache_ins: Any,
                 key_username: str,
                 key_password: str,
                 key_access_token: str = 'access_token',
                 section_authentication: str = 'accounts_authentication',
                 hash_salt: str = 'ishardguesssalt!!!'):
        """
        View class that is suit for code book stored and token passed in url

        :param cache_ins: like Flask cache redis ...
        :param key_username: key of username  when request login url
        :param key_password: key of password  when request login url
        :param key_access_token: the key in the url, it's like
        :param section_authentication: section name that records account and password in code book ini
        :param hash_salt: that is used to generate token
        """
        self.section_authentication = section_authentication
        self.cache_ins = cache_ins
        self.key_access_token = key_access_token
        self.key_username = key_username
        self.key_password = key_password
        self.hash_salt = hash_salt

    def generate_token(self, account: str, password: str, hash_salt: str) -> str:
        token = FlaskCache.generate_token(account + password, hash_salt)
        if not isinstance(token, str):
            raise TypeError(f'generated token {token} is not str')
        return token

    def generate_login_cache(self,
                             token: str,
                             account: str,
                             password: str) -> None:
        self.cache_ins.set(token, {self.key_username: account, self.key_password: password})

    @property
    def login_cache(self) -> Dict[str, str]:
        return self.cache_ins.get(request.args.get(self.key_access_token)) or dict()

    @property
    def login_cache_password(self) -> str:
        return self.login_cache[self.key_password]

    @property
    def login_cache_username(self) -> str:
        return self.login_cache[self.key_username]

    def is_valid_token(self) -> bool:
        # todo verify account and password
        return bool(self.login_cache)

    def login_with_cache(self) -> Union[flask.Response, str]:
        account, password = View.request.get_data(self.key_username, self.key_password)
        token = self.generate_token(account, password, self.hash_salt)
        self.generate_login_cache(token, account, password)
        try:
            return View.login(self.key_username,
                              self.key_password,
                              self.response.login_succeed(token),
                              is_aborted=True,
                              style='db',
                              salt=self.hash_salt)
        except AuthenticationFailed:
            self.cache_ins.delete(token)
            return View.response.login_fail()
        except Exception as e:
            traceback.print_exc()
            self.cache_ins.delete(token)
            return abort(500)

    def verify_before_request(self,
                              exclude_path: Tuple[str, ...] = ('/login',),
                              can_abort: bool = True,
                              failed_info: str = '') -> Union[flask.Response, str, None]:
        """
        get token from url and verify it.
        the url is like http://wxadas?access_token=xxxx
        example:

        @app.before_request
        def verify_token() -> Optional[flask.Response]:
            pass

        :param cache_ins: a cache ins that implemented get method and cache tokens
        :param key_token: the key in the url
        :param exclude_path: these paths will be excluded to verify token
        :param failed_info: failed to pass verify and return the info
        :return:
        """
        if request.path not in exclude_path:
            # debug: options is like a ping of chrome browser. 跨域请求前会浏览器会自动进行此操作.
            if not self.is_valid_token() and request.method != 'OPTIONS':
                if can_abort:
                    return abort(401)
                return failed_info
        return None

    def check_operation_authority(self, block_uuid: str) -> Optional[str]:
        """
        :return:
        """
        login_cache = self.cache_ins.get(request.args.get(self.key_access_token))
        if not isinstance(login_cache, dict):
            return abort(403)
        username = login_cache.get(self.key_username, '')
        verified = PermissionFactory('db')(User, Role, RolePermission).can_do(block_uuid,
                                                                              username=username)  # type: ignore
        if not verified:
            return abort(403)
        return None


class ViewRestful(Resource):
    request: Request = Request()
    service: Dict = dict()

    @classmethod
    def set_service(cls, package_path: str, prefix: str) -> Dict[str, Any]:
        return Package(package_path).get_classes(prefix)

    def exec_service(self) -> Dict[str, Any]:
        if not self.service:
            pass
        cls_name, method_name, _ = self.request.service
        exec_method = getattr(self.service.get(cls_name), method_name)
        if not exec_method:
            raise IncomingDataValueError(f'class cls_name {cls_name} do not have method {method_name}')
        return exec_method(self.request.data)

    def get(self) -> str:
        return 'hello pysubway ...'
