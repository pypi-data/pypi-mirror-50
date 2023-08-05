from setuptools import setup


long_description = """
```shell
pip install tisdk
tireq --help

tireq username secret_key method url [foo:bar,foo2:bar2...]

tireq to_9012345678_grs 3292a4f76c0d46bf post http://taiqiyun.wowfintech.cn/grs/v1/open_match name:oppo

```

```python
import tisdk

username = 'to_9012345678_grs'
secret_key = '3292a4f76c0d46bf'
method = 'post'
url = 'http://taiqiyun.wowfintech.cn/grs/v1/open_match'
data = {'name': 'oppo'}

tisdk.ti_request(username, secret_key, method, url, data)

ti = tisdk.Ti(username, secret_key)
ti.request(method, url, data)

```
"""

setup(
    name='tisdk',
    version='0.0.13',
    description='python sdk of taiqiyun',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['requests', 'pycrypto'],
    py_modules=['tisdk'],
    entry_points={
        'console_scripts': ['tireq=tisdk:main'],
    },
    include_package_data=True,
)
