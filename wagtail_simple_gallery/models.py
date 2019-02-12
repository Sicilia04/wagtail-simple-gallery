from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images import get_image_model
from wagtail.search import index

from wagtail_simple_gallery.fields import UniqueBooleanField

IMAGE_ORDER_TYPES = (
	(1, 'Image title'),
	(2, 'Newest image first'),
)


class SimpleGalleryIndex(Page):
	"""
	This is the index page for the Photo Gallery. It contains the links to
	Gallery pages.  Gallery Page displays the Gallery images according to tags
	defined.
	"""

	intro_text = RichTextField(
		blank=True,
		verbose_name=_('Intro text'),
		help_text=_('Optional text to go with the intro text.')
	)

	search_fields = Page.search_fields + [
		index.SearchField('intro_text'),
	]

	feed_image = models.ForeignKey(
		'wagtailimages.Image',
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name='+'
	)

	@property
	def children(self):
		return self.get_children().live()

	def get_context(self, request, **kwargs):
		# Get list of live Gallery pages that are descendants of this page
		pages = SimpleGalleryPage.objects.live().descendant_of(self).order_by('-first_published_at')

		# Update template context
		context = super(SimpleGalleryIndex, self).get_context(request)
		context['pages'] = pages

		return context

	class Meta:
		verbose_name = _('Gallery index page')

	# Only allow EventPages beneath this page.
	subpage_types = ['wagtail_simple_gallery.SimpleGalleryPage']

	content_panels = [
		FieldPanel('title', classname="full title"),
		FieldPanel('intro_text', classname="full")
	]

	template = 'wagtail_simple_gallery/simple_gallery_index.html'


class SimpleGalleryPage(Page):
	intro_title = models.CharField(
		verbose_name=_('Intro title'),
		max_length=250,
		blank=True,
		help_text=_('Optional H1 title for the gallery page.')
	)
	intro_text = RichTextField(
		blank=True,
		verbose_name=_('Intro text'),
		help_text=_('Optional text to go with the intro text.')
	)
	collection = models.ForeignKey(
		'wagtailcore.Collection',
		verbose_name=_('Collection'),
		null=True,
		blank=False,
		on_delete=models.SET_NULL,
		related_name='+',
		help_text=_('Show images in this collection in the gallery view.')
	)
	images_per_page = models.IntegerField(
		default=8,
		verbose_name=_('Images per page'),
		help_text=_('How many images there should be on one page.')
	)
	use_lightbox = models.BooleanField(
		verbose_name=_('Use lightbox'),
		default=True,
		help_text=_('Use lightbox to view larger images when clicking the thumbnail.')
	)
	highlight = UniqueBooleanField(
		verbose_name=_("Highlight"),
		default=False,
		help_text=_('If page will be highlight.')
	)
	order_images_by = models.IntegerField(choices=IMAGE_ORDER_TYPES, default=1)

	content_panels = Page.content_panels + [
		FieldPanel('intro_title', classname='full title'),
		FieldPanel('intro_text', classname='full title'),
		FieldPanel('collection'),
		FieldPanel('images_per_page', classname='full title'),
		FieldPanel('use_lightbox'),
		FieldPanel('order_images_by'),
	]

	@property
	def images(self):
		return get_gallery_images(self.collection.name, self)

	def get_context(self, request, **kwargs):
		images = self.images
		page = request.GET.get('page')
		paginator = Paginator(images, self.images_per_page)
		try:
			images = paginator.page(page)
		except PageNotAnInteger:
			images = paginator.page(1)
		except EmptyPage:
			images = paginator.page(paginator.num_pages)
		context = super(SimpleGalleryPage, self).get_context(request)
		context['gallery_images'] = images
		return context

	class Meta:
		verbose_name = _('Gallery page')
		verbose_name_plural = _('Gallery pages')

	parent_page_types = ['wagtail_simple_gallery.SimpleGalleryIndex']

	template = getattr(settings, 'SIMPLE_GALLERY_TEMPLATE', 'wagtail_simple_gallery/simple_gallery.html')


def get_gallery_images(collection, page=None, tags=None):
	images = None
	try:
		images = get_image_model().objects.filter(collection__name=collection)
		if page:
			if page.order_images_by == 0:
				images = images.order_by('title')
			elif page.order_images_by == 1:
				images = images.order_by('-created_at')
	except Exception as e:
		pass
	if images and tags:
		images = images.filter(tags__name__in=tags).distinct()
	return images