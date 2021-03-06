from django import forms
from .widgets import CustomClearableFileInput
from .models import Gin, GinCategory


class GinForm(forms.ModelForm):
    class Meta:
        model = Gin
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        """ Get Friendly Names """
        super().__init__(*args, **kwargs)
        gincategories = GinCategory.objects.all()
        friendly_names = [(gc.id,
                           gc.get_friendly_name()
                           ) for gc in gincategories]

        """ Use Friendly Names """
        self.fields['gincategory'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'rounded-5'
