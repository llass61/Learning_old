"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User, Group, UserManager
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField


# from django.template.defaultfilters import escape
# from django.core.urlresolvers import reverse

# def user_link(self):
#    return '<a href="%s">%s</a>' % (reverse("admin:auth_user_change", args=(self.user.id,)) , escape(self.user))

# user_link.allow_tags = True
# user_link.short_description = "User"

class GSCapabilitySet(models.Model):
    name = models.CharField(max_length=100, default='View Only', unique=True)
    load_profile = models.BooleanField(default=False)
    outage_mgmt = models.BooleanField(default=False)
    editing = models.BooleanField(default=False)
    power_flow = models.BooleanField(default=False)
    model_editing = models.BooleanField(default=False)

    def getList(self):
        return ",".join(["%s:%s" % (a, v) for a, v in self.__dict__.items() if a[0] != '_' and a not in ['id', 'name']])

    def __str__(self):
        return self.name
        # out = ""
        # for attr, value in self.__dict__.items():
        #    if value and (attr != "_state") and (attr != "id"):
        #        out += attr + ", "
        # return out


class GSInstance(models.Model):
    name = models.CharField(max_length=100, default='EPE', unique=True)
    gis_server = models.CharField(max_length=100, default='')
    db_server = models.CharField(max_length=100, default='')
    db_instance = models.CharField(max_length=100, default='')
    map_instance = models.CharField(max_length=100, default='')
    sde_instance = models.CharField(max_length=100, default='')
    sde_pfx = models.CharField(max_length=100, default='')
    grid_instance = models.CharField(max_length=100, default='')
    capabilities = models.ForeignKey(GSCapabilitySet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class GSOrg(models.Model):
    name = models.CharField(max_length=100)
    instances = models.ManyToManyField(GSInstance)

    def __str__(self):
        return self.name


# extends Django group
class GSGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    org = models.ForeignKey(GSOrg, on_delete=models.CASCADE)
    capabilities = models.ForeignKey(GSCapabilitySet, on_delete=models.CASCADE)

    def __str__(self):
        return self.group.name


# extends Django user
class GSUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_instance = models.ForeignKey(GSInstance, on_delete=models.CASCADE)
    # instances = models.ManyToManyField(GSInstance)
    org = models.ForeignKey(GSOrg, on_delete=models.CASCADE)
    group = ChainedForeignKey(
        GSGroup,
        chained_field="org",
        chained_model_field="org",
        show_all=False,
        auto_choose=True,
        sort=True
    )

    objects = UserManager()

    def __str__(self):
        return self.user.username

