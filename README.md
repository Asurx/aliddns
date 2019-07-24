# AliDDNS

基于阿里云DNS提供的SDK实现的动态 DNS 解析工具。

## 开始使用

使用前请详细阅读以下说明，若在使用时遇到问题请提`issues`，我会在看到消息后及时回复。

### 运行要求

1、运行环境安装有python并且版本是`3.x`

2、拥有阿里云的[Access Key](https://help.aliyun.com/document_detail/34414.html)，没有可以按照链接中的文档操作获取

### 安装依赖

```
pip3 install requests aliyun-python-sdk-alidns
```

### 修改配置

修改或者自行在`ddns.py`同级目录新建`config.json`文件，配置文件格式如下

```json
 [
    {
      "ak": "阿里云Access Key ID",
      "secret": "阿里云Access Key Secret",
      "domain": "主域名",
      "prefix": "域名前缀"
    }
  ]
```

如需配置多个域名则按以下格式追加即可

```json
 [
    {
      "ak": "阿里云Access Key ID",
      "secret": "阿里云Access Key Secret",
      "domain": "abc.com",
      "prefix": "home"
    },
    {
      "ak": "阿里云Access Key ID",
      "secret": "阿里云Access Key Secret",
      "domain": "def.com",
      "prefix": "home"
    }
  ]
```

### 初次运行

现在一切都已经准备就绪了，我们只需要运行下面的命令即可

```shell
python3 ddns.py
```

脚本执行后返回的格式如下

`````json
[
    {
        "status" : "更新状态: successful/failed",
        "full_domain" : "域名前缀.主域名",
        "original" : "上一次解析到的IP，如果之前没有记录则为空",
        "current": "当前解析到的IP"
    }
]
`````

有多少个域名有更新就会返回多少个对象，如果只返回了`[]`则表示所有域名IP都没有变化。

如果一切正常，你将会看到以下提示

```json
[
    {
        "status" : "successful",
        "full_domain" : "home.abc.com",
        "original" : "",
        "current": "123.123.123.123"
    }
]
```

如果配置文件有误，将会出现以下提示，这时我们唯一需要做的一件事就是修正配置文件并重新运行。

```json
[
    {
        "status" : "failed",
        "message" : "HTTP Status: 400 Error:InvalidAccessKeySecret The AccessKeySecret is incorrect. Please check your AccessKeyId and AccessKeySecret. RequestID: XXXXXX-BC1E-4F29-B3B6-01D299F099AE",
        "full_domain" : "home.abc.com"
    }
]
```

### 定时运行

手动测试没有问题后，我们就可以使用`crontab -e`写入定时任务，让脚本自动运行即可。

```text
*/1 * * * * nohup python3 脚本绝对路径/ddns.py > /tmp/aliddns.log 2>&1 &
```