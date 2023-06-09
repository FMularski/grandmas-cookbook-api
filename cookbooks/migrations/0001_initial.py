# Generated by Django 4.2 on 2023-04-24 16:41

import cookbooks.models
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
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('difficulty', models.CharField(choices=[('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard')], default='E', max_length=1)),
                ('rating', models.FloatField(default=0, validators=[cookbooks.models.validate_between_0_and_5])),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='created_recipes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Instruction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(blank=True)),
                ('action', models.CharField(max_length=200)),
                ('tip', models.CharField(blank=True, max_length=200, null=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instructions', to='cookbooks.recipe')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.FloatField(validators=[cookbooks.models.validate_greater_than_0])),
                ('amount_unit', models.CharField(choices=[('M', 'ml'), ('G', 'g'), ('T', 'tablespoons'), ('C', 'cups'), ('U', 'units')], max_length=1)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='cookbooks.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Cookbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipes', models.ManyToManyField(blank=True, related_name='cookbooks', to='cookbooks.recipe')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cookbook', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
