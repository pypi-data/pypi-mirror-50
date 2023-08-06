### 钛旗云 SDK 使用说明

#### 安装 SDK

通过 `pip` 一键完成安装

```sh
pip install tisdk -U
```

#### 使用 SDK 调试接口

安装完成后, 可直接在命令行使用 `tireq` 命令调试接口

```sh
tireq username secret_key method url [foo:bar,foo2:bar2...]
```

`tireq` 命令的参数依次是:

1. 用户名 (由钛旗云系统分配)
2. 密钥 (由钛旗云系统分配)
3. 请求方法名 (`get` `post` `put` ...)
4. 请求 url
5. 请求体参数 (参数名和参数值以 `:` 相隔, 多对参数之间以 `,` 相隔) **非必须**

参考示例如下

```sh
tireq myusername 4fbe6e7084ec4d05 post /api/xxx/v1 name1:value1
```

#### 在代码中调用 SDK 发起请求

参考 `Python` 代码如下

```python
import tisdk

username = 'myusername'
secret_key = '4fbe6e7084ec4d05'
method = 'post'
url = '/api/xxx/v1'
data = {'name1': 'value1'}

# 直接调用 ti_request 方法发起请求
# 每次发起请求时都传入`用户名`和`密钥`
tisdk.ti_request(username, secret_key, method, url, data)

# 以`用户名`和`密钥`初始化 Ti 对象
# 之后调用 Ti.request 方法发起请求, 不需每次传`用户名`和`密钥`
ti = tisdk.Ti(username, secret_key)
ti.request(method, url, data)

```

