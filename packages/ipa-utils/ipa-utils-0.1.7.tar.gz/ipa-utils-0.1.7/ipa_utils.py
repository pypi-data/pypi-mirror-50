# -*- coding: utf-8 -*-
import os
import json
import yaml
import csv
import ldap3
import click


USER_BASE_DN_TEMPLATE = u"cn=users,cn=accounts,{base_dn}"
USER_SEARCH_TEMPLATE = u"(&(objectclass=person)(uid={username}))"
USERS_SEARCH_TEMPLATE = u"(objectclass=person)"

class IpaService(object):

    def __init__(self, host=u"127.0.0.1", port=389, base_dn=None, username=None, password=None, server_params=None, connection_params=None):
        self.host = host
        self.port = port
        self.base_dn = base_dn
        self.server_params = server_params or {}
        self.server_params.update({
            "get_info": ldap3.ALL,
        })
        self.connection_params = connection_params or {}
        if username:
            self.connection_params["user"] = username
        if password:
            self.connection_params["password"] = password
        if not base_dn:
            self.base_dn = self.auto_get_base_dn()
            if not self.base_dn:
                raise RuntimeError(u"异常：未提供BaseDN，且自动获取失败。")

    def auto_get_base_dn(self):
        connection = self.get_connection()
        base_dns = [x for x in connection.server.info.naming_contexts if u"dc=" in x]
        if base_dns:
            return base_dns[0]
        else:
            return None

    @property
    def user_base_dn(self):
        return USER_BASE_DN_TEMPLATE.format(base_dn=self.base_dn)

    def get_connection(self):
        server = ldap3.Server(self.host, self.port, **self.server_params)
        connection = ldap3.Connection(server, **self.connection_params)
        connection.bind()
        return connection

    def get_user_entry(self, username, connection=None):
        connection = connection or self.get_connection()
        connection.search(
            search_base=self.user_base_dn,
            search_filter=USER_SEARCH_TEMPLATE.format(username=username),
            attributes=[ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES],
            )
        if len(connection.entries):
            return connection.entries[0]
        else:
            return None

    def get_user_detail_from_entry(self, user_entry):
        user_detail = json.loads(user_entry.entry_to_json())
        data = {
            u"dn": user_detail[u"dn"],
        }
        data.update(user_detail[u"attributes"])
        for key in data.keys():
            value = data[key]
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]
        return data

    def get_user_detail(self, username, connection=None):
        user_entry = self.get_user_entry(username, connection)
        if not user_entry:
            return None
        return self.get_user_detail_from_entry(user_entry)

    def get_user_entries(self, connection=None, paged_size=200):
        entries = []
        connection = connection or self.get_connection()
        extra_params = {}
        while True:
            connection.search(
                search_base=self.user_base_dn,
                search_filter=USERS_SEARCH_TEMPLATE,
                attributes=[ldap3.ALL_ATTRIBUTES, ldap3.ALL_OPERATIONAL_ATTRIBUTES],
                paged_size=paged_size,
                **extra_params
                )
            entries += connection.entries
            paged_cookie = connection.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
            if paged_cookie:
                extra_params["paged_cookie"] = paged_cookie
            else:
                break
        return entries

@click.group()
@click.option("-h", "--host", default="127.0.0.1", help=u"Ldap服务器地址，默认为127.0.0.1。")
@click.option("-p", "--port", default=389, type=int, help=u"Ldap服务端口，默认为389。")
@click.option("-u", "--username", help=u"Ldap帐号，不提供时使用匿名查询。不同权限的帐号，查询范围或字段可能不相同。")
@click.option("-P", "--password", help=u"Ldap帐号，不提供时使用匿名查询。不同权限的帐号，查询范围或字段可能不相同。")
@click.option("-b", "--base-dn", help=u"Ldap的BaseDN。不提供则自动获取，若有多个则自动选择第1个命名空间（排除非dc类命名空间）。")
@click.pass_context
def ipa(ctx, host, port, username, password, base_dn):
    u"""Freeipa管理工具集。请指定子命令进行操作。
    """
    ctx.ensure_object(dict)
    ctx.obj["host"] = host
    ctx.obj["port"] = port
    ctx.obj["username"] = username
    ctx.obj["password"] = password
    ctx.obj["base_dn"] = base_dn


@ipa.command(name="get-user-detail")
@click.option("-o", "--output-format", default="yaml", type=click.Choice(['yaml', 'json']), help=u"信息输出格式，默认为yaml格式输出。")
@click.argument("username", nargs=1, required=True)
@click.pass_context
def get_user_detail(ctx, output_format, username):
    u"""查询用户信息，支持yaml/json等格式输出。
    """
    service = IpaService(ctx.obj["host"], ctx.obj["port"], ctx.obj["base_dn"], ctx.obj["username"], ctx.obj["password"])
    user = service.get_user_detail(username)
    if not user:
        click.echo(u"错误：没有找到用户名为 {username} 的帐号。".format(username=username))
        os.sys.exit(1)
    else:
        if output_format.lower() == u"json":
            click.echo(json.dumps(user, ensure_ascii=False))
        else:
            click.echo(yaml.safe_dump(user, allow_unicode=True))

@ipa.command(name="get-users")
@click.option("-o", "--output", default="users.csv")
@click.option("-e", "--encoding", default="gb18030")
@click.pass_context
def get_users(ctx, output, encoding):
    u"""导出全部用户，并保存到csv文件。
    """
    service = IpaService(ctx.obj["host"], ctx.obj["port"], ctx.obj["base_dn"], ctx.obj["username"], ctx.obj["password"])
    user_entries = service.get_user_entries()
    if not user_entries:
        print("no user entry found...")
        os.sys.exit(1)
    users = [service.get_user_detail_from_entry(user) for user in user_entries]
    user = users[0]
    headers = list(user.keys())
    headers.sort()
    rows = []
    for user in users:
        row = []
        for field in headers:
            row.append(user.get(field, None))
        rows.append(row)
    with open(output, "w", encoding=encoding, newline="") as fobj:
        f_csv = csv.writer(fobj)
        f_csv.writerow(headers)
        f_csv.writerows(rows)


if __name__ == "__main__":
    ipa()
