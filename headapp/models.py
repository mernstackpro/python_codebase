from django.db import models
from django.contrib.auth.models import AbstractUser
import json
import datetime


class User(AbstractUser):
    user_profile = models.ImageField(upload_to='user_profiles/',height_field=None,width_field=None,max_length=100,blank=True,null=True)
    ROLES = (
        ('admin','admin'),
        ('member','member'),
        ('request','request'),
        ('general_manager','general_manager'),
        ('f&b_director','f&b_director'),
        ('executive_chef','executive_chef'),
        ('spa_manager','spa_manager'),
        ('sales_maketing','sales_marketing'),
    )
    saluation = models.CharField(max_length=10,null=True,blank=True)
    role = models.CharField(max_length=20, choices=ROLES,default='request')
    date_of_birth = models.DateField(blank=True,null=True)
    country = models.CharField(max_length=25,blank=True)
    phone_number = models.CharField(max_length=10,blank=True)
    signup_for_notification = models.BooleanField(default=False)
    plan_id = models.IntegerField(blank=True,null=True)
    temp_password = models.CharField(blank=True,null=True,max_length=100)
    membership_start_date = models.DateField(blank=True,null=True)
    membership_end_date = models.DateField(blank=True,null=True)
    token = models.CharField(max_length=255,blank=True,null=True)
    # shiji fileds
    RecID = models.CharField(max_length=255,blank=True,null=True)
    CustNo = models.CharField(max_length=255,blank=True,null=True)
    PMSID = models.CharField(max_length=255,blank=True,null=True)
    PMSCrsID = models.CharField(max_length=255,blank=True,null=True)
    AssocNo = models.CharField(max_length=255,blank=True,null=True)


    def get_required_fields_list():
        return ['firstname','lastname','email','country','password','phone_number','saluation']



    @property
    def html_dob(self):
        if self.date_of_birth:
            return self.date_of_birth.strftime('%Y-%m-%d')

    @property
    def get_user_profile_url(self):
        if self.user_profile:
            return self.user_profile.url
        return '/static/demo.jpg'

    @property
    def get_date_joined(self):
        return self.date_joined.strftime('%d %b %Y')
        
    @property
    def get_membership_start_date(self):
        if self.membership_start_date:
            return self.membership_start_date.strftime('%Y-%m-%d')
        else : return ''

    @property
    def get_membership_end_date(self):
        if self.membership_end_date:
            return self.membership_end_date.strftime('%Y-%m-%d')
        else:return ''
        
    def __str__(self):
        return f'{self.id}. '+self.username

    # @property
    # def is_membership_active(self):
        # if self.membership_end_date > 

class Tab(models.Model):
    TAB_TYPES = (
        ('menu','menu'),
        ('tab','tab'),
        ('subtab','subtab'),
    )
    tab_type = models.CharField(max_length=50,choices=TAB_TYPES)
    parent_tab_name = models.CharField(max_length=50,null=True,blank=True)
    tab_name = models.CharField(max_length=50,null=True,blank=True)
    title = models.CharField(max_length=255,null=True,blank=True)
    tagline = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='tab_img',null=True,blank=True)


    