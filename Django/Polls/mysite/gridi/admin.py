# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import GSCapabilitySet,GSGroup,GSInstance,GSOrg,GSUser


# Register your models here.
admin.site.register(GSCapabilitySet)
admin.site.register(GSGroup)
admin.site.register(GSInstance)
admin.site.register(GSOrg)
admin.site.register(GSUser)