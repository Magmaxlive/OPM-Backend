import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_enquiry_form_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry_form',
            name='date',
            field=models.DateField(default=datetime.date(2026, 4, 21)),
            preserve_default=False,
        ),
    ]
