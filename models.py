# 1450 / ????
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _
from helpful.fields import upload_to


class URL(models.Model):
    name = models.CharField(_("Title"), max_length=256)
    url = models.CharField(_("URL or URL RegEx"), max_length=2048)
    regex = models.BooleanField(_("RegEx"), default=False)

    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("URL")
        verbose_name_plural = _("URLs")


class Page(models.Model):
    name = models.CharField(_("Name"), max_length=128)

    # SEO
    title = models.CharField(_("Title"), max_length=256, blank=True, null=True)
    header = models.CharField(_("Header"), max_length=256, blank=True, null=True)
    keywords = models.CharField(_("Keywords"), max_length=1024, blank=True, null=True)
    description = models.CharField(_("Description"), max_length=2048, blank=True, null=True)
    head_code = models.TextField(_("Head code"), blank=True, null=True)
    footer_code = models.TextField(_("Footer code"), blank=True, null=True)

    # img? cover?
    cover = models.FileField(_("Image"), upload_to=upload_to, blank=True)
    intro = models.TextField(_("Intro"), blank=True, null=True)
    text = models.TextField(_("Text"), blank=True, null=True)

    sites = models.ManyToManyField(Site, related_name="pages", verbose_name=_("Sites"), blank=True)
    slug = models.CharField(_("Slug"), max_length=128, unique=True)
    url = models.CharField(_("URL"), max_length=1024, editable=False)

    # Tree
    parent = models.ForeignKey(
        "self",
        verbose_name=_("Parent"),
        null=True,
        blank=True,
        related_name="childs",
        on_delete=models.CASCADE,
    )
    level = models.IntegerField(_("Level"), default=0, editable=False)
    sorting = models.PositiveIntegerField(_("Sorting"), default=500)
    tree_sorting = models.IntegerField(_("Tree sorting"), default=500, editable=False)

    # Techno
    template = models.CharField(_("Template"), max_length=32, null=True, blank=True)
    per_page = models.IntegerField(
        _("Items per page"),
        help_text=_("The maximum number of items to include on a page"),
        default=10,
    )

    tags = models.ManyToManyField(Tag, related_name="pages", verbose_name=_("Tags"), blank=True)

    # Future
    # blocks = models.ManyToManyField('Block', verbose_name=_('Blocks'), blank=True, related_name='pages')
    # regex = models.BooleanField(verbose_name=_('RegEx'), default=False)
    # related?
    # views?

    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Page, self).__init__(*args, **kwargs)
        self._prev_parent = self.parent
        self._prev_level = self.level
        self._prev_sorting = self.sorting

    def __str__(self):
        padding = (self.level - 1) * 8
        display = "&nbsp;" * padding + self.name
        return mark_safe(display)

    def get_absolute_url(self):
        return self.url

    def public_childs(self):
        return self.childs.filter(public=True)

    def public_media(self):
        return self.media.filter(public=True)

    def group(self):
        groups = {}
        block_groups = self.blocks.order_by("group").distinct().values_list("group", flat=True)
        for group in block_groups:
            groups[group] = self.blocks.filter(group=group, public=True)
        return groups

    def resort(self, parent, i):
        if parent:
            pages = Page.objects.filter(parent=parent).order_by("sorting")
        else:
            pages = Page.objects.filter(parent__isnull=True).order_by("sorting")

        for page in pages:
            i += 1
            page.tree_sorting = i
            page.save(sort=False)
            i = self.resort(page.id, i)
        return i

    def save(self, sort=True, *args, **kwargs):
        if not self.title:
            self.title = self.name

        if not self.header:
            self.header = self.name

        if self.parent:
            self.level = self.parent.level + 1
            self.url = self.parent.url
            if not settings.APPEND_SLASH:
                self.url += "/"
        else:
            self.level = 1
            self.url = "/"

        self.url += self.slug

        if settings.APPEND_SLASH:
            self.url += "/"

        if self.slug == "/":
            self.url = "/"

        super(Page, self).save(*args, **kwargs)

        if sort:
            if self._prev_parent != self.parent or self._prev_sorting != self.sorting or self._prev_level != self.level:
                self.resort(0, 0)

    class Meta:
        ordering = ["tree_sorting"]
        # unique_together = ['sites', 'url']
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")


class Block(models.Model):
    name = models.CharField(_("Name"), max_length=128)
    slug = models.SlugField(_("Slug"), max_length=128)
    # unique=False,
    # help_text=_("A slug is the part of a URL which identifies a page using human-readable keywords"),

    # header
    title = models.CharField(_("Title"), max_length=256, blank=True, null=True)
    show_title = models.BooleanField(verbose_name=_("Show title"), default=False)

    # sub title? sub header
    description = models.CharField(_("Description"), max_length=2048, blank=True, null=True)

    text = models.TextField(_("Text"), blank=True, null=True)

    image = models.FileField(_("Image"), upload_to=upload_to, blank=True, null=True)

    bg = models.FileField(_("Background"), upload_to=upload_to, blank=True, null=True)
    url = models.CharField(_("URL"), max_length=1024, default="#", blank=True, null=True)

    pages = models.ManyToManyField(Page, verbose_name=_("Pages"), related_name="blocks", blank=True)

    sites = models.ManyToManyField(Site, related_name="site_bloks", verbose_name=_("Sites"), null=True, blank=True)
    urls = models.ManyToManyField(URL, related_name="url_bloks", verbose_name=_("URLs"), null=True, blank=True)
    # template = models.CharField(_('Template'), max_length=124, blank=True, null=True)

    # order
    sorting = models.PositiveIntegerField(_("Sorting"), default=500)

    # Area (choices?)
    group = models.CharField(_("Group"), max_length=64, default="content")

    template = models.CharField(_("Template"), max_length=124, blank=True, null=True)

    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def public_elements(self):
        return self.elements.filter(public=True)

    def __str__(self):
        return self.name

    def public_subblocks(self):
        return self.subblocks.filter(public=True)

    class Meta:
        ordering = ["sorting"]
        verbose_name = _("Block")
        verbose_name_plural = _("Blocks")


class Element(models.Model):
    name = models.CharField(_("Name"), max_length=128)

    title = models.CharField(_("Title"), max_length=256, blank=True, null=True)
    # header/ subheader/ subtitle
    description = models.CharField(_("Description"), max_length=2048, blank=True, null=True)
    text = models.TextField(_("Text"), blank=True, null=True)
    image = models.FileField(_("Image"), upload_to=upload_to, blank=True, null=True)

    block = models.ForeignKey(
        Block,
        verbose_name=_("Block"),
        related_name="elements",
        on_delete=models.CASCADE,
    )

    # order
    sorting = models.PositiveIntegerField(_("Sorting"), default=500)

    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def dependent_from(self):
        return self.block

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["sorting"]
        verbose_name = _("Element")
        verbose_name_plural = _("Elements")


# File
class Media(models.Model):
    page = models.ForeignKey(Page, verbose_name=_("Page"), related_name="media", on_delete=models.CASCADE)

    name = models.CharField(_("Name"), max_length=256)

    # TextField
    description = models.CharField(_("Description"), max_length=2048, blank=True, null=True)

    doc = models.FileField(_("Document"), upload_to=upload_to)

    # created = models.DateTimeField(_("dateCreated"), blank=True, null=True)
    # downloads = models.PositiveIntegerField(_("Downloads"), editable=False, default=0)

    sorting = models.PositiveIntegerField(_("Sorting"), default=500)
    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["sorting"]
        verbose_name = _("Media")
        verbose_name_plural = _("Media")

    # content_type = models.ForeignKey(ContentType, verbose_name=_("Content Type"))
    # object_id = models.PositiveIntegerField(_("Object ID"))
    # content_object = GenericForeignKey("content_type", "object_id")
    #
    # group = models.CharField(_("Group media"), max_length=64, blank=True)
    #
    # def __init__(self, *args, **kwargs):
    #     super(File, self).__init__(*args, **kwargs)
    #     if hasattr(self, "id"):
    #         for es in self.properties.all():
    #             setattr(self, es.key.key, es.value)
    #
    # def ext(self):
    #     filename = self.file.url.split(".")
    #     ext = filename[len(filename) - 1].lower()
    #     return ext
    #
    # def type(self):
    #     if self.ext() in ["jpg", "png", "gif"]:
    #         return "image"
    #     elif self.ext() in ["avi", "mp4", "oog", "flw"]:
    #         return "video"
    #     else:
    #         return "file"
    #
    # def dependent_from(self):
    #     return self.content_object
    #
    # @models.permalink
    # def get_absolute_url(self):
    #     return ("files_download", (), {"id": self.id})


# ---------------------------------------

# ---------------------------------------
# KEY-VAL-PROPERTY
# PropertiesGroup =
class FileKey(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    key = models.SlugField(_("key"), unique=True)

    def __unicode__(self):
        return self.name


class FileProperty(models.Model):
    file = models.ForeignKey(File, verbose_name=_("File"), related_name="properties")
    key = models.ForeignKey(FileKey, verbose_name=_("Key"))
    value = models.CharField(verbose_name=_("Value"), max_length=2048)

    def __unicode__(self):
        return "%s: %s" % (self.key.key, self.value)


class Property(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=256)
    slug = models.SlugField(verbose_name=_("Slug"))
    unit = models.CharField(verbose_name=_("Unit"), max_length=32, blank=True)
    description = models.TextField(verbose_name=_("Description"), blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")


class Value(models.Model):
    property = models.ForeignKey(Property, verbose_name=_("Property"), related_name="values")
    value = models.CharField(verbose_name=_("Value"), max_length=256)
    image = models.ForeignKey(Image, verbose_name=_("Image"), related_name="values")

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = _("Value")
        verbose_name_plural = _("Values")


class Tag(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=128)
    slug = models.SlugField(_("Slug"), max_length=128, unique=True)

    def pages_count(self):
        return self.pages.filter(public=True).count()

    @models.permalink
    def get_absolute_url(self):
        return ("pages_tag", (), {"slug": self.slug})

    class Meta:
        ordering = ["name"]
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __unicode__(self):
        return self.name


# CMS2 FROM SEO DELETE
class Redirect(models.Model):
    PROTOCOLS = (
        ("http://", _("HTTP")),
        ("https://", _("HTTPS")),
    )
    from_protocol = models.CharField(_("From Protocol"), max_length=32, choices=PROTOCOLS)
    from_domain = models.CharField(_("From Domain"), max_length=256, blank=True, null=True)
    from_url = models.CharField(_("From URL"), max_length=2048)

    to_protocol = models.CharField(_("To Protocol"), max_length=32, choices=PROTOCOLS)
    to_domain = models.CharField(_("To Domain"), max_length=256)
    to_url = models.CharField(_("To URL"), max_length=2048)

    regex = models.BooleanField(_("RegEx"), default=False)

    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return "%s%s/%s &rarr; %s%s/%s" % (
            self.from_protocol,
            self.from_domain,
            self.from_url,
            self.to_protocol,
            self.to_domain,
            self.to_url,
        )

    __str__.allow_tags = True

    class Meta:
        verbose_name = _("Redirect")
        verbose_name_plural = _("Redirects")


class Settings(models.Model):
    site = models.OneToOneField(Site, models.CASCADE, verbose_name=_("Site"), related_name="settings")
    language = models.CharField(_("Language"), max_length=32)

    robots_txt = models.TextField(_("robots.txt"), blank=True)
    sitemap_xml = models.TextField(_("sitemap.xml"), blank=True)

    head_code = models.TextField(_("Head code"), blank=True, null=True)
    footer_code = models.TextField(_("Footer code"), blank=True, null=True)

    public = models.BooleanField(_("Public"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __init__(self, *args, **kwargs):
        super(Settings, self).__init__(*args, **kwargs)
        if hasattr(self, "site"):
            for es in self.site.variables.all():
                setattr(self.site, es.key, es.value)
                setattr(self, es.key, es.value)

    class Meta:
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")

    def __str__(self):
        return "%s &rarr; %s" % (self.site, self.language)

    __str__.allow_tags = True


# CMS2 FROM SEO ADD
class Variable(models.Model):
    site = models.ForeignKey(Site, models.CASCADE, verbose_name=_("Site"), related_name="variables")
    name = models.CharField(_("Name"), max_length=128)
    key = models.CharField(_("Key"), max_length=128)
    VAR_TYPE = (
        ("text", _("Text")),
        ("string", _("String")),
        ("int", _("Integer")),
        ("double", _("Double")),
        ("file", _("File")),
    )
    var_type = models.CharField(_("Type"), max_length=32, choices=VAR_TYPE)
    value = models.FileField(_("Value"), max_length=5000, null=True, blank=True)

    def get_value(self):
        if self.var_type == "text":
            if self.value:
                short = "%s" % self.value
                return short[:200] + "..."
        else:
            return self.value

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Variable")
        verbose_name_plural = _("Variables")


# 1500
# add menu
