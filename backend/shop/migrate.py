import uuid
from django.db import migrations


class GenerateUUID(migrations.RunPython):
    def __init__(self, app_label, model_name, reverse_code=None, **kwargs):
        self.app_label = app_label
        self.model_name = model_name
        self.reverse_code = reverse_code or migrations.RunPython.noop
        super().__init__(self._gen_uuid, reverse_code=self.reverse_code, **kwargs)

    def _gen_uuid(self, apps, schema_editor):
        Order = apps.get_model(self.app_label, self.model_name)
        for row in Order.objects.all():
            row.uuid = uuid.uuid4().hex[:12].upper()
            row.save(update_fields=["uuid"])