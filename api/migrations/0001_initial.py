from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name="sunil",email="sunil@gmail.com",is_staff=True,is_superuser=True,phone="9847098470",gender="Male")
        user.set_password('sunil')
        user.save()

    dependencies = [

    ]

    operations = [
        migrations.RunPython(seed_data),
    ]