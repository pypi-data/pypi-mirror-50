from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class EpicModelMeta(models.base.ModelBase):
    """ Add export and print permissions to Django Model Class """
    def __new__(cls, name, bases, attrs):

        super_new = super().__new__
        Meta = attrs.pop('Meta', None)

        if not Meta:
            Meta = type('Meta', (object,), {})

        #add default permission (export, print) to model
        setattr(Meta, 'permissions', (
            ('export_%s'%name.lower(), 'Can export %s'%name.lower()),
            ('detail_%s'%name.lower(), 'Can show %s detail'%name.lower()),
        ))

        attrs['Meta'] = Meta
        return super_new(cls, name, bases, attrs)


class EpicModel(models.Model, metaclass=EpicModelMeta):
    """ Epic Model abstract class """
    class Meta:
        abstract = True


class UserProfile(EpicModel):

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    MALE = 'ML'
    FEMALE = 'FE'
    GENDER = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, verbose_name= _('User'))
    title = models.CharField(max_length=5, blank=True, null=True, verbose_name= _('Title'))
    gender = models.CharField(max_length=2, choices=GENDER, default=MALE, verbose_name= _('Gender'))
    dob = models.DateField(blank=True, null=True, verbose_name= _('Date of birth'))
    phone_1 = models.CharField(max_length=15, blank=True, null=True, verbose_name= _('Phone 1'))
    phone_2 = models.CharField(max_length=15, blank=True, null=True, verbose_name= _('Phone 2'))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name= _('Address'))
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Country'))
    province = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Province'))
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('City'))
    zip = models.CharField(max_length=5, blank=True, null=True, verbose_name=_('ZIP'))
    position = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Position'))
    organization = models.ForeignKey('Organization', on_delete=models.PROTECT, verbose_name=_('Organization'))

    def __str__(self):
        return "{}. {}".format(self.title, self.user.get_full_name())


class Organization(EpicModel):

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    name = models.CharField(max_length=25, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    phone_1 = models.CharField(max_length=15, blank=True, null=True, verbose_name= _('Phone 1'))
    phone_2 = models.CharField(max_length=15, blank=True, null=True, verbose_name= _('Phone 2'))
    fax = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('Fax'))
    email = models.EmailField(max_length=30, blank=True, null=True, verbose_name=_('Email'))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name= _('Address'))
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Country'))
    province = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Province'))
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('City'))
    zip = models.CharField(max_length=5, blank=True, null=True, verbose_name=_('ZIP'))

    def __str__(self):
        return "{}".format(self.name)