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



class PublicMessage(models.Model):
    STATUSES = {
        "PENDING": "Pending Review",
        "REVIEWED": "Reviewed",
        "CLOSED": "Closed"
    }
    name = models.CharField(blank=False, null=False, max_length=64)
    email = models.EmailField(blank=True, null=True, max_length=128)
    phone = models.CharField(blank=True, null=True, max_length=42)
    subject = models.CharField(blank=False, null=False, max_length=64)
    body = models.CharField(blank=False, null=False, max_length=2048)
    status = models.CharField(max_length=14, choices=STATUSES, default=STATUSES['PENDING'])