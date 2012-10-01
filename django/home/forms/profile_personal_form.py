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
    fields = ('first_name','last_name','company' )

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = "id-profile-personal-form"
    self.helper.form_class = "form-horizontal"
    self.helper.form_method = "post"
    self.helper.form_action = ""
    
    self.helper.layout = Layout(
      Div(
        Field('first_name', css_class="input-xlarge"),
      ),    
      Div(
        Field('last_name', css_class="input-xlarge"),
      ),
      Div(
        Field('company', css_class="input-xlarge"),
      ),
      FormActions(
        Button('personal-form-cancel-changes', 'Cancel', css_class="btn pull-right"),
        Submit('personal-form-save-changes', 'Save', css_class="ajax_submit btn btn-success pull-right")
      )
    )
    
    super(ProfilePersonalForm, self).__init__(*args, **kwargs)    

class ProfileSpeakerForm(ModelForm):

  class Meta:
    model = UserProfile
    fields = ('personal_bio','languages', 'website_url' )
    widgets = {
      'personal_bio': forms.Textarea(),
    }
    

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = "id-profile-speaker-form"
    self.helper.form_class = "form-horizontal"
    self.helper.form_method = "post"
    self.helper.form_action = ""
    
    self.helper.layout = Layout(
      Div(
        Field('personal_bio', style="resize: none;", css_class="input-xlarge span6"),
      ),
      Div(
        Field('website_url', css_class="input-xlarge span6"),
      ),      
      Div(
        Field('languages', css_class="input-xlarge"),
      ),
      FormActions(
        Button('speaker-form-cancel-changes', 'Cancel', css_class="btn pull-right"),
        Submit('speaker-form-save-changes', 'Save', css_class="ajax_submit btn btn-success pull-right")
      )      
    )
    
    super(ProfileSpeakerForm, self).__init__(*args, **kwargs)    

class ProfileSocialForm(ModelForm):

  class Meta:
    model = UserProfile
    fields = ('twitter_url','gplus_url' )

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = "id-profile-social-form"
    self.helper.form_class = "form-horizontal"
    self.helper.form_method = "post"
    self.helper.form_action = ""
    
    self.helper.layout = Layout(
      Div(
        Field('twitter_url', css_class="input-xlarge"),
      ),    
      Div(
        Field('gplus_url', css_class="input-xlarge"),
      ),
      FormActions(
        Button('social-form-cancel-changes', 'Cancel', css_class="btn pull-right"),      
        Submit('social-form-save-changes', 'Save', css_class="ajax_submit btn btn-success pull-right")
      )      
    )
    
    super(ProfileSocialForm, self).__init__(*args, **kwargs)

class ProfileNotificationsForm(ModelForm):

  class Meta:
    model = UserProfile
    fields = ( 'days_to_event_notify', )

  def __init__(self, *args, **kwargs):
    self.helper = FormHelper()
    self.helper.form_id = "id-profile-notifications-form"
    self.helper.form_class = "form-horizontal"
    self.helper.form_method = "post"
    self.helper.form_action = ""
    
    self.helper.layout = Layout(
      AppendedText('days_to_event_notify', 'days in advance', active=True),    
      FormActions(
        Button('notifications-form-cancel-changes', 'Cancel', css_class="btn pull-right"),      
        Submit('notifications-form-save-changes', 'Save', css_class="ajax_submit btn btn-success pull-right")
      )      
    )
    
    super(ProfileNotificationsForm, self).__init__(*args, **kwargs)
        
#class ProfilePersonalForm(ModelForm):

#  class Meta:
#    model = UserProfile
#    exclude = ('new_profile', 'presentations', 'user_hash', 'headshots', 'locations', 'user', 'relationships' )
#    widgets = {
#      'personal_bio': forms.Textarea(),
#    }

#  def __init__(self, *args, **kwargs):
#    self.helper = FormHelper()
#    self.helper.form_id = "id-personal-form"
#    self.helper.form_class = "form-horizontal"
#    self.helper.form_method = "post"
#    self.helper.form_action = ""
#    
#    self.helper.layout = Layout(
#      Fieldset(
#        'Personal Information',
#        Div(
#          Div(
#            Field('first_name', css_class="input-xlarge"),
#            css_class="span4"
#          ),
#          Div(
#            Field('twitter_url', css_class="input-xlarge"),
#            css_class="span4"
#          ),
#          css_class="row-fluid"
#        ),
#        Div(
#          Div(
#            Field('last_name', css_class="input-xlarge"),
#            css_class="span4"
#          ),
#          Div(
#            Field('gplus_url', css_class="input-xlarge"),
#            css_class="span4"
#          ),
#          css_class="row-fluid"
#        ),        
#        Div(
#          Div(
#            Field('company', css_class="input-xlarge"),
#            css_class="span4"
#          ),
#          Div(
#            Field('website_url', css_class="input-xlarge"),
#            css_class="span4"
#          ),
#          css_class="row-fluid"
#        ),
#        HTML("<hr />"),
#        Field('languages', placeholder="eg. comma separated list of spoken languages", css_class="input-xlarge"),
#        Field('personal_bio', style="resize: none;", css_class="input-xlarge span6"),
#        HTML("<hr />"),
#        AppendedText('days_to_event_notify', 'days in advance', active=True),
#      ),
#      FormActions(
#        Submit('personal-form-save-changes', 'Next', css_class="ajax_submit btn btn-success pull-right")
#      )
#    )
#    super(ProfilePersonalForm, self).__init__(*args, **kwargs)

