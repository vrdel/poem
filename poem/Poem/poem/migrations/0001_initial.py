# Generated by Django 2.0.7 on 2018-07-18 15:00

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters', max_length=30, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$'), 'Enter a valid username.', 'invalid')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='GroupOfMetrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Group of metrics',
                'verbose_name_plural': 'Groups of metrics',
            },
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='GroupOfProbes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='name')),
                ('permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='permissions')),
            ],
            options={
                'verbose_name': 'Group of probes',
                'verbose_name_plural': 'Groups of probes',
            },
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='GroupOfProfiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='name')),
                ('permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='permissions')),
            ],
            options={
                'verbose_name': 'Group of profiles',
                'verbose_name_plural': 'Groups of profiles',
            },
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('probeversion', models.CharField(max_length=128)),
                ('parent', models.CharField(max_length=128)),
                ('probeexecutable', models.CharField(max_length=128)),
                ('config', models.CharField(max_length=1024)),
                ('attribute', models.CharField(max_length=1024)),
                ('dependancy', models.CharField(max_length=1024)),
                ('flags', models.CharField(max_length=1024)),
                ('files', models.CharField(max_length=1024)),
                ('parameter', models.CharField(max_length=1024)),
                ('fileparameter', models.CharField(max_length=1024)),
                ('cloned', models.CharField(max_length=128, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poem.GroupOfMetrics')),
            ],
        ),
        migrations.CreateModel(
            name='MetricAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=384)),
                ('value', models.CharField(max_length=384)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poem.Metric')),
            ],
        ),
        migrations.CreateModel(
            name='MetricConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(blank=True, max_length=384, null=True)),
                ('value', models.CharField(blank=True, max_length=384, null=True)),
                ('metric', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='poem.Metric')),
            ],
        ),
        migrations.CreateModel(
            name='MetricDependancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=384)),
                ('value', models.CharField(max_length=384)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poem.Metric')),
            ],
        ),
        migrations.CreateModel(
            name='MetricFileParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=384)),
                ('value', models.CharField(max_length=384)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poem.Metric')),
            ],
        ),
        migrations.CreateModel(
            name='MetricFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=384)),
                ('value', models.CharField(max_length=384)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poem.Metric')),
            ],
        ),
        migrations.CreateModel(
            name='MetricFlags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=384)),
                ('value', models.CharField(max_length=384)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poem.Metric')),
            ],
        ),
        migrations.CreateModel(
            name='MetricInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('service_flavour', models.CharField(max_length=128)),
                ('metric', models.CharField(max_length=128)),
                ('vo', models.CharField(blank=True, max_length=128, null=True)),
                ('fqan', models.CharField(blank=True, max_length=128, null=True, verbose_name='FQAN')),
            ],
            options={
                'ordering': ['service_flavour', 'metric', 'vo', 'fqan'],
            },
        ),
        migrations.CreateModel(
            name='MetricParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=384)),
                ('value', models.CharField(max_length=384)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poem.Metric')),
            ],
        ),
        migrations.CreateModel(
            name='MetricParent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(help_text='Parent metric', max_length=384, null=True)),
                ('metric', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='poem.Metric')),
            ],
        ),
        migrations.CreateModel(
            name='MetricProbeExecutable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(help_text='Probe executable', max_length=384, null=True)),
                ('metric', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='poem.Metric')),
            ],
        ),
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'permissions': (('metricsown', 'Read/Write/Modify'),),
            },
        ),
        migrations.CreateModel(
            name='Probe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the probe.', max_length=128)),
                ('version', models.CharField(help_text='Version of the probe.', max_length=28)),
                ('nameversion', models.CharField(help_text='Name, version tuple.', max_length=128)),
                ('description', models.CharField(max_length=1024)),
                ('comment', models.CharField(max_length=512)),
                ('repository', models.CharField(max_length=512)),
                ('docurl', models.CharField(max_length=512)),
                ('group', models.CharField(max_length=1024)),
                ('user', models.CharField(blank=True, max_length=32)),
                ('datetime', models.DateTimeField(blank=True, max_length=32, null=True)),
            ],
            options={
                'permissions': (('probesown', 'Read/Write/Modify'),),
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Name of the profile.', max_length=128)),
                ('version', models.CharField(default='1.0', help_text='Multiple versions of the profile can exist (defaults to 1.0).', max_length=10)),
                ('vo', models.CharField(max_length=128, verbose_name='VO')),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('groupname', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ['name', 'version'],
                'permissions': (('profileown', 'Read/Write/Modify'),),
            },
        ),
        migrations.CreateModel(
            name='ServiceFlavour',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='Service flavour')),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=255, null=True, verbose_name='distinguishedName')),
                ('egiid', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='eduPersonUniqueId')),
                ('displayname', models.CharField(blank=True, max_length=30, null=True, verbose_name='displayName')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VO',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='Virtual organization')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='profile',
            unique_together={('name', 'version')},
        ),
        migrations.AddField(
            model_name='metricinstance',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metric_instances', to='poem.Profile'),
        ),
        migrations.AddField(
            model_name='metric',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poem.Tags'),
        ),
        migrations.AddField(
            model_name='groupofprofiles',
            name='profiles',
            field=models.ManyToManyField(blank=True, to='poem.Profile'),
        ),
        migrations.AddField(
            model_name='groupofprobes',
            name='probes',
            field=models.ManyToManyField(blank=True, to='poem.Probe'),
        ),
        migrations.AddField(
            model_name='groupofmetrics',
            name='metrics',
            field=models.ManyToManyField(blank=True, to='poem.Metrics'),
        ),
        migrations.AddField(
            model_name='groupofmetrics',
            name='permissions',
            field=models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='permissions'),
        ),
        migrations.AddField(
            model_name='custuser',
            name='groupsofmetrics',
            field=models.ManyToManyField(blank=True, help_text='The groups of metrics that this user belongs to', related_name='user_set', related_query_name='user', to='poem.GroupOfMetrics', verbose_name='groups of metrics'),
        ),
        migrations.AddField(
            model_name='custuser',
            name='groupsofprobes',
            field=models.ManyToManyField(blank=True, help_text='The groups of probes that this user belongs to', related_name='user_set', related_query_name='user', to='poem.GroupOfProbes', verbose_name='groups of probes'),
        ),
        migrations.AddField(
            model_name='custuser',
            name='groupsofprofiles',
            field=models.ManyToManyField(blank=True, help_text='The groups of profiles that this user belongs to', related_name='user_set', related_query_name='user', to='poem.GroupOfProfiles', verbose_name='groups of profiles'),
        ),
        migrations.AddField(
            model_name='custuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='metricinstance',
            unique_together={('profile', 'service_flavour', 'metric', 'fqan')},
        ),
        migrations.AlterUniqueTogether(
            name='metric',
            unique_together={('name', 'tag')},
        ),
    ]
