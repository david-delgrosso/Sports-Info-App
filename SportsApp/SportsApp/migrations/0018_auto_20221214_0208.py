# Generated by Django 3.2.15 on 2022-12-14 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SportsApp', '0017_auto_20221212_2231'),
    ]

    operations = [
        migrations.AddField(
            model_name='nbateam',
            name='rank_assists_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_blocks_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_defReb_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_fga_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_fgm_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_fgp',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_fta_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_ftm_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_ftp',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_offReb_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_assists_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_blocks_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_defReb_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_fga_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_fgm_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_fgp',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_fta_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_ftm_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_ftp',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_offReb_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_pFouls_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_plusMinus_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_points_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_steals_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_totReb_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_tpa_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_tpm_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_tpp',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_opp_turnovers_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_pFouls_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_plusMinus_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_points_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_steals_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_totReb_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_tpa_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_tpm_pg',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_tpp',
            field=models.IntegerField(default=0.0),
        ),
        migrations.AddField(
            model_name='nbateam',
            name='rank_turnovers_pg',
            field=models.IntegerField(default=0.0),
        ),
    ]
