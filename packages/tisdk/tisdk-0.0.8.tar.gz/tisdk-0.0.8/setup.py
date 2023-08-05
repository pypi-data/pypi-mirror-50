from setuptools import setup


long_description = """
```shell
pip install tisdk
tireq --help

tireq username secret_key method url [foo:bar,foo2:bar2...]

tireq to_9012345678_grs 3292a4f76c0d46bf post http://taiqiyun.wowfintech.cn/grs/v1/open_match name:美团

```

```python
import tisdk

res = tisdk.ti_request(username, secret_key, method, url)
print(res)

data = {'foo': 'bar'}
tisdk.ti_request(username, secret_key, method, url, data)

```
"""

setup(
    name='tisdk',
    version='0.0.8',
    description='python sdk of taiqiyun',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['request', 'pycrypto'],
    py_modules=['tisdk'],
    entry_points={
        'console_scripts': ['tireq=tisdk:main'],
    },
    include_package_data=True,
)
