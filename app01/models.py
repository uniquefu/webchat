from django.db import models

# Create your models here.
class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    brief = models.CharField(max_length=255, blank=True, null=None)
    avatar = models.ImageField(verbose_name='头像',blank=True)
    status_choices =category_choices = [
        (0, "在线"),
        (1, "隐身"),
        (2, "离开"),
        (3, "忙碌"),
    ]
    status =models.IntegerField(choices=status_choices,default=0)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    friends = models.ManyToManyField('self',verbose_name='朋友们',related_name='f',null=True,blank=True)

    def __str__(self):
        return self.username
class Group(models.Model):
    name =models.CharField(verbose_name='群名', max_length=32)
    brief=models.CharField(max_length=255,blank=True,null=None)
    owner =models.ForeignKey(UserInfo)
    admins=models.ManyToManyField(UserInfo,related_name='admin_group')
    members =models.ManyToManyField(UserInfo,related_name='members_group')
    max_members=models.IntegerField(default=300)

    def __str__(self):
        return  self.name