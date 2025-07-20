from django.db import models

# Create your models here.


class PermissionRights(models.Model):   
    class Meta:
        # No database table creation or deletion
        # operations will be performed for this model.
        managed = False

        # disable "add", "change", "delete"   
        # and "view" default permissions
        default_permissions = ()

        permissions = ( 
            ('employee_rights', 'Employee rights'),  
        )