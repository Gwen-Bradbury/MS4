from django import forms
from .models import Recipe, RecipeCategory


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """ Get Friendly Names """
        super().__init__(*args, **kwargs)
        recipecategories = RecipeCategory.objects.all()
        friendly_names = [(rc.id,
                           rc.get_friendly_name()
                           ) for rc in recipecategories]

        """ Use Friendly Names """
        self.fields['recipecategory'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'rounded-5'
