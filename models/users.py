from tortoise import fields
from tortoise.models import Model


class Users(Model):
    user_id = fields.IntField(pk=True)
    user_rank = fields.IntField(default=1)
    balance = fields.IntField(default=0)
    token = fields.TextField(default="None")
    prefix_commands = fields.TextField(default="ф")
    prefix_scripts = fields.TextField(default="ск")
    prefix_admin = fields.TextField(default="адм")
    user_name = fields.TextField(default="NickName")
    info_mode = fields.TextField(default="default")
    ignore_list = fields.JSONField(default=list)
    trust_list = fields.JSONField(default=list)
    trust_prefix = fields.TextField(default="#")
    troll_list = fields.JSONField(default=list)
    subscriber = fields.TextField(default="free")


class Pattern(Model):
    user_id = fields.IntField()
    name = fields.TextField()
    types = fields.TextField()
    attachments = fields.TextField(default="None")
    text = fields.TextField(default="None")


class Spam(Model):
    user_id = fields.IntField()
    peer_id = fields.IntField()
    text = fields.TextField()
    spam_sleep = fields.FloatField()
    attachments = fields.JSONField(default=list)
    is_active = fields.BooleanField(default=False)


class Scripts(Model):
    user_id = fields.IntField(pk=True)
    spam = fields.BooleanField(default=False)
    auto_online = fields.BooleanField(default=False)
    auto_offline = fields.BooleanField(default=False)
    auto_sms = fields.BooleanField(default=False)
    auto_sms_users = fields.JSONField(default=dict(users=[]))
    auto_sms_text = fields.TextField(default="None")
    auto_cover = fields.BooleanField(default=False)
    cover_id = fields.IntField(default=1)
