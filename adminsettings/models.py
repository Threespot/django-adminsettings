from django.db import models

from adminsettings.fields import PickledObjectField


class AdminSetting(models.Model):
    """
    Model representation of an admin setting. Only contains fields for the name
    and value, which is stored in the database as a pickled Python object.
    """
    name = models.CharField(max_length=128)
    value = PickledObjectfield()

    @property
    def setting_name(self):
        return self.name.replace(' ', '_').upper()