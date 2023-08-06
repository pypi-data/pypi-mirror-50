from django.apps import AppConfig as BaseConfig
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from imagekit import register
from .utils import load_path_attr

class AppConfig(BaseAppConfig):
    name = "artek.images"
    label = "artek_images"
    verbose_name = _("Artek Images")

    def ready(self):
        thumbnail_path = getattr(
            settings,
            "ARTEK_IMAGES_THUMBNAIL_SPEC",
            "artek.images.specs.ImageThumbnail"
        )
        thumbnail_spec_class = load_path_attr(thumbnail_path)
        register.generator("artek_images:image:thumbnail", thumbnail_spec_class)

        list_thumbnail_path = getattr(
            settings,
            "ARTEK_IMAGES_LIST_THUMBNAIL_SPEC",
            "artek.images.specs.ImageListThumbnail"
        )
        list_thumbnail_spec_class = load_path_attr(list_thumbnail_path)
        register.generator("artek_images:image:list_thumbnail", list_thumbnail_spec_class)

        small_thumbnail_path = getattr(
            settings,
            "ARTEK_IMAGES_SMALL_THUMBNAIL_SPEC",
            "artek.images.specs.ImageSmallThumbnail"
        )
        small_thumbnail_spec_class = load_path_attr(small_thumbnail_path)
        register.generator("artek_images:image:small_thumbnail", small_thumbnail_spec_class)

        medium_thumbnail_path = getattr(
            settings,
            "ARTEK_IMAGES_MEDIUM_THUMBNAIL_SPEC",
            "artek.images.specs.ImageMediumThumbnail"
        )
        medium_thumbnail_spec_class = load_path_attr(medium_thumbnail_path)
        register.generator("artek_images:image:medium_thumbnail", medium_thumbnail_spec_class)