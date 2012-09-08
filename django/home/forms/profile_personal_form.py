from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Field, Fieldset, HTML, Hidden, Layout, Row, Submit
from crispy_forms.bootstrap import AppendedText, FormActions, PrependedText

from django.forms import ModelForm

from home.models import Location, Presentation, UserProfile

import logging
  
logger = logging.getLogger('home.views')

class ProfilePersonalForm(ModelForm):

  class Meta:
    model = UserProfile
    exclude = ('new_profile', 'presentations', 'user_hash', 'headshots', 'locations', 'user', 'relationships' )
    widgets = {
      'personal_bio': forms.Textarea(),
    }

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = "id-personal-form"
    self.helper.form_class = "form-horizontal"
    self.helper.form_method = "post"
    self.helper.form_action = ""
    
    self.helper.layout = Layout(
      Fieldset(
        'Personal Information',
        Field('first_name', css_class="input-xlarge disabled"),
        Field('last_name', css_class="input-xlarge"),
        Field('company', css_class="input-xlarge"),
        Field('languages', placeholder="eg. comma separated list of spoken languages", css_class="input-xlarge"),
        Field('personal_bio', style="resize: none;", css_class="input-xlarge span6"),
        Field('twitter_url', css_class="input-xlarge"),
        Field('gplus_url', css_class="input-xlarge"),
        Field('website_url', css_class="input-xlarge")        
      ),
      FormActions(
        Submit('personal-form-save-changes', 'Next', css_class="ajax_submit btn btn-success pull-right")
      )
    )
    super(ProfilePersonalForm, self).__init__(*args, **kwargs)

