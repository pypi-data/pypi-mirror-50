# ipa-utils

Freeipa管理工具集。请指定子命令进行操作。

## 安装

```
pip install ipa-utils
```

## 安装的命令

- ipa-utils

## ipa-utils提供的子命令

- get-user-details 查询用户信息，支持yaml/json等格式输出。
- get-users 导出全部用户，并保存到csv文件。

## 命令帮助信息

ipa-utils命令下提供全局参数用于ldap服务的连接，各子命令下提供其它参数详细子命令帮助信息。

```
    E:\ipa-utils>ipa-utils --help
    Usage: ipa-utils [OPTIONS] COMMAND [ARGS]...

      Freeipa管理工具集。请指定子命令进行操作。

    Options:
      -h, --host TEXT      Ldap服务器地址，默认为127.0.0.1。
      -p, --port INTEGER   Ldap服务端口，默认为389。
      -u, --username TEXT  Ldap帐号，不提供时使用匿名查询。不同权限的帐号，查询范围或字段可能不相同。
      -p, --password TEXT  Ldap帐号，不提供时使用匿名查询。不同权限的帐号，查询范围或字段可能不相同。
      -b, --base-dn TEXT   Ldap的BaseDN。不提供则自动获取，若有多个则自动选择第1个命名空间（排除非dc类命名空间）。
      --help               Show this message and exit.

    Commands:
      get-user-detail  查询用户信息，支持yaml/json等格式输出。
```

get-user-detail子命令用于查询用户详细信息。支持yaml/json等格式输出。

```
    E:\ipa-utils>ipa-utils get-user-detail --help
    Usage: ipa-utils get-user-detail [OPTIONS] USERNAME

      查询用户信息，支持yaml/json等格式输出。

    Options:
      -o, --output-format [yaml|json]
                                      信息输出格式，默认为yaml格式输出。
      --help                          Show this message and exit.
```

get-users子命令用于导出全部用户，并保存到csv文件。

```
    E:\ipa-utils>ipa-utils get-users --help
    Usage: ipa-utils get-users [OPTIONS]

      导出全部用户，并保存到csv文件。

    Options:
      -o, --output TEXT
      -e, --encoding TEXT
      --help               Show this message and exit.
```