# from pysubway.apps.app_batch_test.main import view_batch_huzumodel
# from pysubway.apps.app_batch_test.main import generate_app
# from pysubway.utils.file import File
# from pysubway.view import View
#
# app = generate_app()
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
#     company_uuid='',
# )
#
#
# @app.route('/')
# def index() -> str:
#     return View.resp_template('index.html')
#
#
# @app.route("/batch-test-huizu/", methods=['POST'])
# def batch_test_huizu() -> str:
#     account, passwd, biz_data, test_reason = View.request_form('account', 'passwd', 'biz_data', 'test_reason')
#     code_book = f'{File.this_dir(__file__)}/static/code_book.ini'
#     section = 'huizumodel'
#     env = 'prod'
#     print('it running batch_test_huizu')
#     return view_batch_huzumodel(code_book, section, BOOLDATA_ACCOUNT, env)
#
#
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=False, processes=True)
