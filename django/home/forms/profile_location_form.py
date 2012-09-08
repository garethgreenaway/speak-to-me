from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Field, Fieldset, HTML, Hidden, Layout, Row, Submit
from crispy_forms.bootstrap import AppendedText, FormActions, PrependedText

from django.forms import ModelForm

from home.models import Location, Presentation, UserProfile

import logging
  
logger = logging.getLogger('home.views')

class ProfileLocationForm(ModelForm):
  class Meta:
    model = Location
    exclude = ('longitude', 'latitude', 'postalcode', 'hidden' )
    
  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = "id-location-form"
    self.helper.form_class = "form-horizontal"
    self.helper.form_method = "post"
    self.helper.form_action = ""
        
    self.helper.layout = Layout(
      Fieldset(
        'Primary Address',
        Field('nickname', css_class="input-xlarge"),
        Div(
          Field('street_address', css_class="input-xlarge"),
          Field('street_address_hidden', css_class="input-xlarge"),
          css_id="street_address_block"
        ),
        Field('city', css_class="input-xlarge"),
        Field('city_hidden', css_class="input-xlarge"),
        Field('state', css_class="input-xlarge"),
        Field('country', css_class="input-xlarge"),
      ),
      FormActions(
        Submit('location-form-save-changes', 'Next', css_class="ajax_submit btn btn-success pull-right")
      )
    )
    super(ProfileLocationForm, self).__init__(*args, **kwargs)
