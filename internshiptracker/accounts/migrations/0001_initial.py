from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=120)),
                ('role', models.CharField(max_length=160)),
                ('status', models.CharField(choices=[('wishlist', 'Wishlist'), ('applied', 'Applied'), ('assessment', 'Assessment'), ('interview', 'Interview'), ('offer', 'Offer'), ('rejected', 'Rejected')], default='wishlist', max_length=20)),
                ('date_applied', models.DateField(blank=True, null=True)),
                ('job_url', models.URLField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]