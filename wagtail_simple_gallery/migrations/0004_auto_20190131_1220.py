# Generated by Django 2.1.5 on 2019-01-31 11:20

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('wagtailimages', '0001_squashed_0021'),
        ('wagtail_simple_gallery', '0003_simplegalleryindex_order_images_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleGalleryPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro_title', models.CharField(blank=True, help_text='Optional H1 title for the gallery page.', max_length=250, verbose_name='Intro title')),
                ('intro_text', wagtail.core.fields.RichTextField(blank=True, help_text='Optional text to go with the intro text.', verbose_name='Intro text')),
                ('images_per_page', models.IntegerField(default=8, help_text='How many images there should be on one page.', verbose_name='Images per page')),
                ('use_lightbox', models.BooleanField(default=True, help_text='Use lightbox to view larger images when clicking the thumbnail.', verbose_name='Use lightbox')),
                ('order_images_by', models.IntegerField(choices=[(1, 'Image title'), (2, 'Newest image first')], default=1)),
                ('collection', models.ForeignKey(help_text='Show images in this collection in the gallery view.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Collection', verbose_name='Collection')),
            ],
            options={
                'verbose_name': 'Gallery page',
                'verbose_name_plural': 'Gallery pages',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterModelOptions(
            name='simplegalleryindex',
            options={'verbose_name': 'Gallery index page'},
        ),
        migrations.RemoveField(
            model_name='simplegalleryindex',
            name='collection',
        ),
        migrations.RemoveField(
            model_name='simplegalleryindex',
            name='images_per_page',
        ),
        migrations.RemoveField(
            model_name='simplegalleryindex',
            name='intro_title',
        ),
        migrations.RemoveField(
            model_name='simplegalleryindex',
            name='order_images_by',
        ),
        migrations.RemoveField(
            model_name='simplegalleryindex',
            name='use_lightbox',
        ),
        migrations.AddField(
            model_name='simplegalleryindex',
            name='feed_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image'),
        ),
    ]
