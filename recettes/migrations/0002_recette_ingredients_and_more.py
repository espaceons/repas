# Generated by Django 5.1.7 on 2025-04-02 15:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
        ('recettes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recette',
            name='ingredients',
            field=models.ManyToManyField(through='recettes.CompositionRecette', to='ingredients.ingredient'),
        ),
        migrations.AlterField(
            model_name='compositionrecette',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.ingredient'),
        ),
        migrations.AlterField(
            model_name='compositionrecette',
            name='quantite',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='compositionrecette',
            name='recette',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recettes.recette'),
        ),
        migrations.AlterField(
            model_name='recette',
            name='instructions',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='recette',
            name='nom',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='recette',
            name='temps_preparation',
            field=models.PositiveIntegerField(help_text='Temps en minutes'),
        ),
    ]
