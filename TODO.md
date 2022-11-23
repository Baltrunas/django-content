Ideas to add:

Pages:
    tags = models.ManyToManyField(Tag, related_name="pages", verbose_name=_("Tags"), blank=True)
    blocks = models.ManyToManyField('Block', verbose_name=_('Blocks'), blank=True, related_name='pages')
    regex = models.BooleanField(verbose_name=_('RegEx'), default=False)
    related_pages
    views

Block:
    template = models.CharField(_('Template'), max_length=124, blank=True, null=True)




############################################################################################
EXTRA FILES OR MEDIA make design to recreate separate FILES app or add to CONTENT
############################################################################################
# class Media(models.Model): # File
#     page = models.ForeignKey(Page, verbose_name=_("Page"), related_name="media", on_delete=models.CASCADE)
#
#     name = models.CharField(_("Name"), max_length=256)
#
#     # TextField
#     description = models.CharField(_("Description"), max_length=2048, blank=True, null=True)
#
#     doc = models.FileField(_("Document"), upload_to=upload_to)
#
#     # created = models.DateTimeField(_("dateCreated"), blank=True, null=True)
#     # downloads = models.PositiveIntegerField(_("Downloads"), editable=False, default=0)
#
#     position = models.PositiveIntegerField(_("Pisition"), default=500)
#     public = models.BooleanField(_("Public"), default=True)
#     created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
#     updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         ordering = ["sorting"]
#         verbose_name = _("Media")
#         verbose_name_plural = _("Media")
#
#     # content_type = models.ForeignKey(ContentType, verbose_name=_("Content Type"))
#     # object_id = models.PositiveIntegerField(_("Object ID"))
#     # content_object = GenericForeignKey("content_type", "object_id")
#     #
#     # group = models.CharField(_("Group media"), max_length=64, blank=True)
#     #
#     # def __init__(self, *args, **kwargs):
#     #     super(File, self).__init__(*args, **kwargs)
#     #     if hasattr(self, "id"):
#     #         for es in self.properties.all():
#     #             setattr(self, es.key.key, es.value)
#     #
#     # def ext(self):
#     #     filename = self.file.url.split(".")
#     #     ext = filename[len(filename) - 1].lower()
#     #     return ext
#     #
#     # def type(self):
#     #     if self.ext() in ["jpg", "png", "gif"]:
#     #         return "image"
#     #     elif self.ext() in ["avi", "mp4", "oog", "flw"]:
#     #         return "video"
#     #     else:
#     #         return "file"
#     #
#     # def dependent_from(self):
#     #     return self.content_object
#     #
#     # @models.permalink
#     # def get_absolute_url(self):
#     #     return ("files_download", (), {"id": self.id})
#

# KEY-VAL-PROPERTY
# PropertiesGroup =
# class FileKey(models.Model):
#     name = models.CharField(_("Name"), max_length=255)
#     key = models.SlugField(_("key"), unique=True)
#
#     def __unicode__(self):
#         return self.name
#
#
# class FileProperty(models.Model):
#     file = models.ForeignKey(File, verbose_name=_("File"), related_name="properties")
#     key = models.ForeignKey(FileKey, verbose_name=_("Key"))
#     value = models.CharField(verbose_name=_("Value"), max_length=2048)
#
#     def __unicode__(self):
#         return "%s: %s" % (self.key.key, self.value)
#
#
# class Property(models.Model):
#     name = models.CharField(verbose_name=_("Name"), max_length=256)
#     slug = models.SlugField(verbose_name=_("Slug"))
#     unit = models.CharField(verbose_name=_("Unit"), max_length=32, blank=True)
#     description = models.TextField(verbose_name=_("Description"), blank=True)
#
#     def __unicode__(self):
#         return self.name
#
#     class Meta:
#         ordering = ["name"]
#         verbose_name = _("Property")
#         verbose_name_plural = _("Properties")
#
#
# class Value(models.Model):
#     property = models.ForeignKey(Property, verbose_name=_("Property"), related_name="values")
#     value = models.CharField(verbose_name=_("Value"), max_length=256)
#     image = models.ForeignKey(Image, verbose_name=_("Image"), related_name="values")
#
#     def __unicode__(self):
#         return self.value
#
#     class Meta:
#         verbose_name = _("Value")
#         verbose_name_plural = _("Values")






ADD TO django-notyfy

```python
title = models.CharField(verbose_name=_('Title'), max_length=128)
email = models.EmailField(max_length=128, verbose_name=_('E-Mail'))
send_email = models.BooleanField(verbose_name=_('Send E-Mail'), default=True)
phone = models.CharField(max_length=32, verbose_name=_('Phone'))
send_sms = models.BooleanField(verbose_name=_('Send SMS'), default=True)
sms_key = models.CharField(verbose_name=_('SMS.RU Key'), max_length=64, blank=True, null=True)
sms_name = models.CharField(verbose_name=_('SMS Name'), help_text=_('From 2 to 11 Latin characters.'), max_length=11)
```




FROM SEO README.md
<!--
Widgets
	Widgets handling input of text
		TextInput
		NumberInput
		EmailInput
		URLInput
		PasswordInput
		HiddenInput
		DateInput
		DateTimeInput
		TimeInput
		Textarea

	Selector and checkbox widgets
		CheckboxInput
		Select
		NullBooleanSelect
		SelectMultiple
		RadioSelect
		CheckboxSelectMultiple

	File upload widgets
		FileInput
		ClearableFileInput

	Composite widgets
		MultipleHiddenInput
		SplitDateTimeWidget
		SplitHiddenDateTimeWidget
		SelectDateWidget


Built-in Field classes
	- BooleanField
	+ CharField
	+\- ChoiceField
	- TypedChoiceField
	+ DateField
	+ DateTimeField
	+ DecimalField
	+ DurationField
	+ EmailField
	+ FileField
	+ FilePathField
	+ FloatField
	+ ImageField
	+ IntegerField
	+ GenericIPAddressField
	- MultipleChoiceField
	- TypedMultipleChoiceField
	- NullBooleanField
	+ RegexField
	+ SlugField
	+ TimeField
	+ URLField
	+ UUIDField



-->



# TODO: Refactor on seo app
# LocaleMiddleware
class SwitchLocale:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        LOCALE_SPECIFIC_URL = getattr(settings, "LOCALE_SPECIFIC_URL", "domain")
        LOCALE_DEFAULT = getattr(settings, "LOCALE_DEFAULT", "de")
        LOCALE_EXCLUDE = getattr(settings, "LOCALE_EXCLUDE", [])
        LANGUAGES = getattr(settings, "LANGUAGES")

        if LOCALE_SPECIFIC_URL == "domain":
            if hasattr(request.site, "settings"):
                language = request.site.settings.language
            else:
                language = settings.LANGUAGE_CODE

            translation.activate(language)
            request.LANGUAGE_CODE = language

            response = self.get_response(request)

        elif LOCALE_SPECIFIC_URL == "dir":
            url = request.path_info
            lang = LOCALE_DEFAULT

            replace = True
            for EX_URL in LOCALE_EXCLUDE:
                if url.startswith(EX_URL):
                    replace = False

            if replace:
                #  def withoud dir
                for lk in LANGUAGES:
                    if url.startswith("/" + lk[0] + "/") and lk[0] != LOCALE_DEFAULT:
                        lang = lk[0]
                        request.path_info = url[3:]

                translation.activate(lang)
                request.LANGUAGE_CODE = lang

                response = self.get_response(request)

                if lang != LOCALE_DEFAULT:
                    response.content = re.sub(
                        b"<a (.*?) (href)='/", rb"<a \1 href='/" + bytes(lang + "/", "utf-8"), response.content
                    )
                    response.content = re.sub(
                        b'<a (.*?) (href)="/', rb'<a \1 href="/' + bytes(lang + "/", "utf-8"), response.content
                    )

                for lk in LANGUAGES:
                    lng = bytes(lk[0], "utf-8")
                    if request.GET.urlencode():
                        rget = bytes("?" + request.GET.urlencode(), "utf-8")
                    else:
                        rget = b""
                    if lk[0] == LOCALE_DEFAULT:
                        response.content = re.sub(
                            b'<a (.*?) href="lang-' + lng + b'"',
                            rb'<a \1 href="' + bytes(request.path_info, "utf-8") + b'"' + rget,
                            response.content,
                        )
                    else:
                        response.content = re.sub(
                            b'<a (.*?) href="lang-' + lng + b'"',
                            rb'<a \1 href="/' + lng + bytes(request.path_info, "utf-8") + b'"' + rget,
                            response.content,
                        )

            else:
                response = self.get_response(request)

        return response
