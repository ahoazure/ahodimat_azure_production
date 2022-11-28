from django.db import models

"""
The classes in this module overrides native  User,Group and ObectManager.
"""
from django.db import models

from django.contrib.auth.models import (Group,
    AbstractUser,BaseUserManager,)

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from utilities import security # used to encrypt sensitive passwords

def make_choices(values):
    return [(v, v) for v in values]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('New user must be DCT admin staff.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('New user account must be actived.'))
        if not email:
            raise ValueError(_('Valid Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractUser):
    GENDER_CHOICE = ( 'Male','Female', 'Other')
    TITLE_CHOICE = ( 'Mr.','Ms.', 'Mrs.','Dr.', 'Prof.', 'Other')
    title = models.CharField(_('title'),choices=make_choices(TITLE_CHOICE),
        max_length=45,default=TITLE_CHOICE[0])  
    gender = models.CharField(_('gender'),max_length=45,
        choices=make_choices(GENDER_CHOICE),default=GENDER_CHOICE[0])  
    email = models.EmailField(_('e-mail'),unique=True,blank=False,
        null=False)
    postcode = models.CharField(_('postal code'),blank=True, null=True,
        max_length=6)
    username = models.CharField(_('user name'),blank=False, null=False,
        max_length=150)
    date_created = models.DateTimeField(blank=True, null=True,
        auto_now_add=True,verbose_name = _('Date Created'))
    date_lastupdated = models.DateTimeField(blank=True, null=True,
        auto_now=True,verbose_name = _('Date Modified'))

    USERNAME_FIELD = 'email' # Replaced using username as unique identifier
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        managed = True
        verbose_name = _('User')
        verbose_name_plural = _('  User Accounts')
        ordering = ('username', )

    def __str__(self):
        return self.email


class CustomGroup(Group):
    role = models.OneToOneField('auth.Group', parent_link=True,unique=True,
        on_delete=models.CASCADE,verbose_name=_('System Role'))
    roles_manager = models.ForeignKey(CustomUser, models.PROTECT,
        verbose_name='Logged Admin',related_name='roles_admin') # request helper field
    date_created = models.DateTimeField(blank=True, null=True,auto_now_add=True,
        verbose_name = _('Date Created'))
    date_lastupdated = models.DateTimeField(blank=True, null=True,auto_now=True,
        verbose_name = _('Date Modified'))

    class Meta:
        managed = True
        verbose_name = _('System Role')
        verbose_name_plural = _(' System Roles')



class MediatorConfigs(models.Model):  
    CHOICES=((1,"Active"),(0,"Innactive"))

    url_regex = RegexValidator(
        regex=r'https?:\/\/(?:w{1,3}\.)?[^\s.]+(?:\.[a-z]+)*(?::\d+)?(?![^<]*(?:<\/\w+>|\/?>))',
        message="Valid URL:'https://abc.com; or http://abc.com:8000'") 
    id = models.AutoField(primary_key=True) 
    user = models.ForeignKey(CustomUser, models.PROTECT, blank=True,
        verbose_name='DHIS2 User/Email')   
    mediator_url = models.CharField(max_length=200,validators=[url_regex],
        verbose_name='Mediator URL')
    mediator_port = models.IntegerField(verbose_name='Mediator Port',default=443)

    # Mediator settings for OpenHIM authetication if transaction logs needed
    openhim_url = models.CharField(max_length=200,validators=[url_regex],
        verbose_name='OpenHIM URL',blank=True,null=True,) #base url
    openhim_port = models.IntegerField(verbose_name='OpenHIM Port',
        default=None,blank=True,null=True,)
    openhim_user = models.CharField(max_length=200,blank=True,null=True,
        verbose_name='Username') #auth user
    openhim_passkey = models.CharField(max_length=300,blank=True,null=True,
        verbose_name='Password') #auth pass
    status = models.BooleanField(choices=CHOICES,verbose_name='Status',
        default=CHOICES[0][0])

    class Meta:
        managed = True
        db_table = 'ahomediator_configs'
        verbose_name = 'Server Setup'
        verbose_name_plural = 'Server Settings'
        
    def __str__(self):
        return "%s" %(self.mediator_url)

    def clean(self):
        if self.status:
            active = MediatorConfigs.objects.filter(status=1)
            if self.pk:
                active = active.exclude(pk=self.pk)
            if active.exists():
                raise ValidationError("Only one mediator can be active at a time")

    def encrypt_password(self):
        password = security.encrypt(self.openhim_passkey)
        return password

    # Override Save method to store only one instance
    def save(self, *args, **kwargs):
        self.openhim_passkey = self.encrypt_password()  
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super(MediatorConfigs, self).save(*args, **kwargs)