# coding: utf-8

from Crypto.PublicKey import RSA
from subprocess import call

from juser.models import AdminGroup
from pushell.api import *
from pushell.settings import BASE_DIR, EMAIL_HOST_USER as MAIL_FROM


def group_add_user(group, user_id=None, username=None):
    """
    用户组中添加用户
    UserGroup Add a user
    """
    if user_id:
        user = get_object(User, id=user_id)
    else:
        user = get_object(User, username=username)

    if user:
        group.user_set.add(user)


def db_add_group(**kwargs):
    """
    add a user group in database
    数据库中添加用户组
    """
    name = kwargs.get('name')
    group = get_object(UserGroup, name=name)
    users = kwargs.pop('users_id')

    if not group:
        group = UserGroup(**kwargs)
        group.save()
        for user_id in users:
            group_add_user(group, user_id)


def group_update_member(group_id, users_id_list):
    """
    user group update member
    用户组更新成员
    """
    group = get_object(UserGroup, id=group_id)
    if group:
        group.user_set.clear()
        for user_id in users_id_list:
            user = get_object(UserGroup, id=user_id)
            if isinstance(user, UserGroup):
                group.user_set.add(user)


def db_add_user(**kwargs):
    """
    add a user in database
    数据库中添加用户
    """
    groups_post = kwargs.pop('groups')
    admin_groups = kwargs.pop('admin_groups')
    role = kwargs.get('role', 'CU')
    user = User(**kwargs)
    user.set_password(kwargs.get('password'))
    user.save()
    if groups_post:
        group_select = []
        for group_id in groups_post:
            group = UserGroup.objects.filter(id=group_id)
            group_select.extend(group)
        user.group = group_select

    if admin_groups and role == 'GA':  # 如果是组管理员就要添加组管理员和组到管理组中
        for group_id in admin_groups:
            group = get_object(UserGroup, id=group_id)
            if group:
                AdminGroup(user=user, group=group).save()
    return user


def db_update_user(**kwargs):
    """
    update a user info in database
    数据库更新用户信息
    """
    groups_post = kwargs.pop('groups')
    admin_groups_post = kwargs.pop('admin_groups')
    user_id = kwargs.pop('user_id')
    user = User.objects.filter(id=user_id)
    if user:
        user_get = user[0]
        password = kwargs.pop('password')
        user.update(**kwargs)
        if password.strip():
            user_get.set_password(password)
            user_get.save()
    else:
        return None

    group_select = []
    if groups_post:
        for group_id in groups_post:
            group = UserGroup.objects.filter(id=group_id)
            group_select.extend(group)
    user_get.group = group_select

    if admin_groups_post != '':
        user_get.admingroup_set.all().delete()
        for group_id in admin_groups_post:
            group = get_object(UserGroup, id=group_id)
            AdminGroup(user=user, group=group).save()


def db_del_user(username):
    """
    delete a user from database
    从数据库中删除用户
    """
    user = get_object(User, username=username)
    if user:
        user.delete()


def gen_ssh_key(username, password='',
                key_dir=os.path.join(KEY_DIR, 'user'),
                authorized_keys=True, home="/home", length=2048):
    """
    generate a user ssh key in a property dir
    生成一个用户ssh密钥对
    """
    logger.debug('生成ssh key， 并设置authorized_keys')
    private_key_file = os.path.join(key_dir, username+'.pem')
    mkdir(key_dir, mode=777)
    if os.path.isfile(private_key_file):
        os.unlink(private_key_file)
    ret = bash('echo -e  "y\n"|ssh-keygen -t rsa -f %s -b %s -P "%s"' % (private_key_file, length, password))

    if authorized_keys:
        auth_key_dir = os.path.join(home, username, '.ssh')
        mkdir(auth_key_dir, username=username, mode=700)
        authorized_key_file = os.path.join(auth_key_dir, 'authorized_keys')
        with open(private_key_file+'.pub') as pub_f:
            with open(authorized_key_file, 'w') as auth_f:
                auth_f.write(pub_f.read())
        os.chmod(authorized_key_file, 0600)
        chown(authorized_key_file, username)


def server_add_user(username, ssh_key_pwd=''):
    """
    add a system user in pushell
    在pushell服务器上添加一个用户
    """
    bash("useradd -s '%s' '%s'" % (os.path.join(BASE_DIR, 'init.sh'), username))
    gen_ssh_key(username, ssh_key_pwd)


def user_add_mail(user, kwargs):
    """
    add user send mail
    发送用户添加邮件
    """
    user_role = {'SU': u'超级管理员', 'GA': u'组管理员', 'CU':u'普通用户','AU':'审计管理员','PU':'配置管理员'}
    mail_title = u'[华龙强渝] 堡垒机Pushell账户通知！请及时更改初始密码!' 
    mail_msg = u"""
Hi, %s

 Pushell的web用户名： %s
 Pusehll的web登录密码： %s
 Pusehll的密钥文件密码： %s
 Pushell的登录地址: %s

说明:请将 119.84.15.139  pushell.hlxy.com 写入 [windows] c:/windows/system32/drivers/etc/hosts   [类unix] /etc/hosts
     请登陆 pushell后台下载密钥! 可使用密钥登录pushell ssh！
    
提示:Pusehll将作为唯一登录生产环境的系统！请妥善保管自己的账号和密码!
     若设置简单密码或密码泄露，造成一切后果，自负!
    """ % (user.name, user.username,kwargs.get('password'),kwargs.get('ssh_key_pwd'),'https://pushell.hlxy.com')
           #kwargs.get('password'), kwargs.get('ssh_key_pwd'), URL, user.uuid)
    send_mail(mail_title, mail_msg, MAIL_FROM, [user.email], fail_silently=False)


def server_del_user(username):
    """
    delete a user from pushell linux system
    删除系统上的某用户
    """
    bash('userdel -r -f %s' % username)
    logger.debug('rm -f %s/%s_*.pem' % (os.path.join(KEY_DIR, 'user'), username))
    bash('rm -f %s/%s_*.pem' % (os.path.join(KEY_DIR, 'user'), username))
    bash('rm -f %s/%s.pem*' % (os.path.join(KEY_DIR, 'user'), username))


def get_display_msg(user, password='', ssh_key_pwd='', send_mail_need=False):
    if send_mail_need:
        msg = u'添加用户 %s 成功！ 用户密码已发送到 %s 邮箱！' % (user.name, user.email)
    else:
        msg = u"""
        Pushell 的地址： %s <br />
        用户名：%s <br />
        web密码：%s <br />
        登录web后才能下载密钥,密钥密码：%s <br />
        该账号密码可以登陆web和Pushell。
        """ % ('https://pushell.hlxy.com', user.username, password, ssh_key_pwd)
    return msg

