# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('PrisonerExpress', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('prisoner', models.ForeignKey(to='PrisonerExpress.Prisoner')),
                ('program', models.ForeignKey(related_name=b'letters', to='PrisonerExpress.Program')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('material_type', models.CharField(default=b'BO', max_length=2, choices=[(b'BO', b'Book'), (b'MA', b'Magazine'), (b'MO', b'Movie'), (b'TV', b'TV Show'), (b'PO', b'Poem'), (b'SS', b'Short Story'), (b'PH', b'Word or Phrase'), (b'PI', b'Picture'), (b'OO', b'Other')])),
                ('program', models.ForeignKey(related_name=b'materials', to='PrisonerExpress.Program')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prison',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('rules', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='address',
            field=models.CharField(default=b'', max_length=200),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='last_active',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'last active date'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='prison',
            field=models.ForeignKey(to='PrisonerExpress.Prison', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='prisoner',
            name='programs',
            field=models.ManyToManyField(related_name=b'prisoners', to='PrisonerExpress.Program'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='continuous',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='program',
            name='description',
            field=models.CharField(default=b'N/A', max_length=1000),
            preserve_default=True,
        ),
    ]
