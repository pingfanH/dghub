# Source Generated with Decompyle++
# File: update_urls.pyc (Python 3.11)

'''更新服务器公开 URL（单点修改，避免 http/https 散落各处）。

有正规 TLS 证书后：把 USE_HTTPS 改为 True，并改 UPDATE_HOST（建议用域名而非裸 IP）。
'''
UPDATE_HOST = '60.205.197.179'
USE_HTTPS = False
_SCHEME = 'https' if USE_HTTPS else 'http'
UPDATE_BASE_URL = f'''{_SCHEME}://{UPDATE_HOST}'''
UPDATE_JSON_URL = f'''{UPDATE_BASE_URL}/update.json'''
INSTALLER_DOWNLOAD_URL = f'''{UPDATE_BASE_URL}/DGHub-Setup.exe'''
