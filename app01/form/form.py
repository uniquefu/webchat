#Author:Jeff Lee
from django import forms
from django.forms import widgets
from django.forms import fields
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app01 import models
from  app01.form.baseform import BaseForm

class LoginForm(BaseForm,forms.Form):
    username = fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '用户名为6-20个字符'}),
        min_length=4,
        max_length=20,
        strip=True,
        error_messages={'required': '用户名不能为空',
                        'min_length': '用户名最少为4个字符',
                        'max_length': '用户名最不超过为20个字符'},
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': '请输入密码，必须包含数字,字母,特殊字符'},
                                     render_value=True),
        required=True,
        min_length=6,
        max_length=12,
        strip=True,
        validators=[
            # 下面的正则内容一目了然，我就不注释了
            RegexValidator(r'((?=.*\d))^.{6,12}$', '必须包含数字'),
            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,12}$', '必须包含字母'),
            RegexValidator(r'((?=.*[^a-zA-Z0-9]))^.{6,12}$', '必须包含特殊字符'),
            RegexValidator(r'^.(\S){6,10}$', '密码不能包含空白字符'),
        ],  # 用于对密码的正则验证
        error_messages={'required': '密码不能为空!',
                        'min_length': '密码最少为6个字符',
                        'max_length': '密码最多不超过为12个字符'},
    )
    rmb = fields.IntegerField(required=False)

    check_code = fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )

    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')

class Register(BaseForm,forms.Form):
    username = fields.CharField(
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control",'placeholder': '用户名为6-20个字符'}),
        min_length=4,
        max_length=20,
        error_messages={'required': '用户名不能为空',
                         'min_length': '用户名最少为4个字符',
                         'max_length': '用户名最不超过为20个字符'},
    )
    nickname = fields.CharField(
        required=True,
        min_length=2,
        max_length=32,
        strip=True,
        error_messages={'required': '昵称不能为空.',
                        'min_length': "昵称长度不能小于2个字符",
                        'max_length': "昵称长度不能大于32个字符"},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '昵称为2-32个字符'}),
    )

    email = fields.EmailField(
        required=True,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': '请输入邮箱'}),
        error_messages={'required': '邮箱不能为空',
                        'invalid': '请输入正确的邮箱格式'},
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': '请输入密码，必须包含数字,字母,特殊字符'},
                                     render_value=True),
        required=True,
        min_length=6,
        max_length=12,
        strip=True,
        validators=[
            # 下面的正则内容一目了然，我就不注释了
            RegexValidator(r'((?=.*\d))^.{6,12}$', '必须包含数字'),
            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,12}$', '必须包含字母'),
            RegexValidator(r'((?=.*[^a-zA-Z0-9]))^.{6,12}$', '必须包含特殊字符'),
            RegexValidator(r'^.(\S){6,10}$', '密码不能包含空白字符'),
        ],  # 用于对密码的正则验证
        error_messages={'required': '密码不能为空!',
                        'min_length': '密码最少为6个字符',
                        'max_length': '密码最多不超过为12个字符'},
    )

    repassword = fields.CharField(
        # render_value会对于PasswordInput，错误是否清空密码输入框内容，默认为清除，我改为不清楚
        widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': '请再次输入密码!'}, render_value=True),
        required=True,
        strip=True,
        error_messages={'required': '请再次输入密码!', }
    )

    check_code = fields.CharField(
        error_messages={'required': '验证码不能为空.'}
    )

    def _clean_new_password2(self):  # 查看两次密码是否一致
        password1 = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')
        # if password1 and repassword:
        if password1 != repassword:
            # self.error_dict['repassword'] = '两次密码不匹配'
            self._errors["repassword"] = '两次密码不匹配'
            # print("*********")
            # raise ValidationError('两次密码不匹配！')
        return repassword

    def clean(self):
        # 是基于form对象的验证，字段全部验证通过会调用clean函数进行验证
        self._clean_new_password2()  # 简单的调用而已

    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper() != self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')

    def clean_username(self):

        username = self.cleaned_data.get('username')

        u = models.UserInfo.objects.filter(username=username).first()
        if u:
            raise ValidationError(message='用户已注册', code='invalid')

        return username

    def clean_email(self):

        email = self.cleaned_data.get('email')

        u = models.UserInfo.objects.filter(email=email).first()
        if u:
            raise ValidationError(message='邮箱已使用', code='invalid')

        return email