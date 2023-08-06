from django.db import models
from django import forms
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
import base64

PHOTOBOOTH_DATASTREAM_PREFIX="data:image/png;base64"

class PhotoboothImage():
    def __init__(self, image=None):
        self._base64_image = None
        self._raw_image = None
        self.has_image = False

        if image is not None:
            if isinstance(image,str):
                print ("string")
                self.base64_image(image)
#            else:
#                print (type(image))
#                self.raw_image(image)

    def base64_image(self, base64_image=None):
        if base64_image is not None:
            photo = base64_image.split(",")
            if photo[0] == PHOTOBOOTH_DATASTREAM_PREFIX:
                base64_image = photo[1]

            #TODO: have to validade base64
            self._base64_image = base64_image
            self._raw_image = base64.b64decode(base64_image)
            self.has_image = True
        return self._base64_image

    def raw_image(self, raw_image=None):
        print (raw_image)
        if raw_image is not None:
            self._raw_image = raw_image
            self._base64_image = base64.b64encode(raw_image)
            self.has_image = False
        return self._raw_image


# Model Field

# FIXME: Transform in a ImageField
class PhotoboothModelField(models.ImageField):

    description = "A photo taken by the device camera"

    def __init__(self, *args, **kwargs):
        #kwargs['max_length'] = 104
        super().__init__(*args, **kwargs)
        #print(vars(self))
        self.photobooth = PhotoboothImage()

    def __str__(self):
        return "Photobooth Image Field"

    def formfield(self, **kwargs):
        defaults = {'form_class': PhotoboothFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def wvalidate(self, value):
        print("In validate")
        super().validate(value)

#    def to_python(self, value):
#        print ("In to_python ")
#        if value:
#            self.photobooth = PhotoboothImage(value)
#            return self.photobooth.raw_image()


#    def prepare_value(self, value):
#        print ("In prepare_value " )
#        print (type(value))
#        if isinstance(value, str):
#            print ("value: ")
#            print (value)
#        else:
#            print ("Nao e str")
#        if self.photobooth.has_image:
#            return PHOTOBOOTH_DATASTREAM_PREFIX + "," + self.photobooth.base64_image()
#        else:
#            print ("no image")
#        return "Prepare Value"

# Form Field
class PhotoboothFormField(forms.Field):

    def __init__(self, *args, **kwargs):
        defaults = {}
        defaults.update(kwargs)
        if "max_length" in defaults:
            del defaults["max_length"]
            print("deleting defaults")

        super().__init__(*args, **defaults)
        self.widget = PhotoboothWidget()

# Widget
class PhotoboothWidget(forms.Widget):
    template_name = "photobooth_widget/photobooth_widget.html"

    class Media:
        css = {
            'screen': (
                staticfiles_storage.url(
                    'photobooth_widget/css/photobooth_widget.css',
                    ),
                )}
        js = ( staticfiles_storage.url('photobooth_widget/js/photobooth_min.js'),
               staticfiles_storage.url('photobooth_widget/js/photobooth_activate.js'),
              )

    def __init__(self, attrs=None, *args, **kwargs):
        attrs = attrs or {}
        super().__init__(attrs)
    

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ""
        output = render_to_string(self.template_name, {"name": name, "value": value})
        return mark_safe(output)