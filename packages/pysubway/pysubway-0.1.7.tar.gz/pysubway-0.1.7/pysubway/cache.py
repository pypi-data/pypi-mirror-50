from functools import wraps
from typing import Union, Callable, Any

from flask import Flask
from flask import abort
from flask_cache import Cache

from .errors import AuthenticationFailed
from .utils.hash import hash_md5, hash_hmac


class FlaskCache:

    def __new__(cls, app: Flask, config=None) -> Cache:
        config = config if config else {'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600 * 24}
        return Cache(app=app, config=config,
                     with_jinja2_ext=False)

    @staticmethod
    def generate_token(plaintext: Union[str, bytes],
                       key: Union[str, bytes],
                       mode: str = 'hmac', ) -> Union[str, bytes]:
        if mode == 'hmac':
            return hash_hmac(key, plaintext)
        elif mode == 'md5':
            return hash_md5(plaintext, key=key)
        else:
            raise NotImplementedError('')

    @staticmethod
    def verify_token(token: str, cache: Any, is_aborted: bool = True) -> Callable:
        """
        The method is a decorator.
         if token in cache, it can pass the authentication
         else authentication failed.
        :param token: maybe you can get token from this way, request.args.get('token').
        :param cache: cache, dict like, must implement get method.
        :return: bool
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrap(*args: Any, **kwargs: Any) -> Callable:
                if cache.get(token):
                    return func(*args, **kwargs)
                else:
                    if is_aborted:
                        return abort(401)
                    else:
                        raise AuthenticationFailed(f'token {token} is invalid')

            return wrap

        return decorator
