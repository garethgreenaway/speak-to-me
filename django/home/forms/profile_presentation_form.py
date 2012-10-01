from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Column, Div, Field, Fieldset, HTML, Hidden, Layout, MultiField, Row, Submit
from crispy_forms.bootstrap import AppendedText, FormActions, PrependedText

from django.forms import ModelForm

from home.models import Location, Presentation, UserProfile

import logging
  
logger = logging.getLogger('home.views')

class ProfilePresentationForm(ModelForm):
        
  class Meta:
    model = Presentation
    exclude = ( 'presentation_slides', 'presentation_slides_url', 'presentation_pdf', 'presentation_pdf_url', 'presentation_thumbnail', 'presentation_hash' )
    include = ( 'presentation_description', 'presentation_topics', 'presentation_length', 'presentation_hidden', 'presentation_title' )    
    widgets = {
      'presentation_description': forms.Textarea(),
    }    
    
  def __init__(self, *args, **kwargs):
  
    if kwargs.has_key('form_skip_button'):
      form_skip_button = kwargs.pop('form_skip_button')
    else:
      form_skip_button = None

    if kwargs.has_key('modal_form'):
      modal_form = kwargs.pop('modal_form')
    else:
      modal_form = None
            
    super(ProfilePresentationForm, self).__init__(*args, **kwargs)
    self.form_skip_button = form_skip_button

    self.helper = FormHelper()
    self.helper.form_id = "id-presentation-form"
    self.helper.form_class = "form-horizontal"
    self.helper.form_method = "post"
    self.helper.form_action = ""
    self.helper.help_text_inline = True 

    if self.form_skip_button:
      form_actions_layout = FormActions(
            Div(
              Submit('presentation-form-skip', 'Skip', css_class="ajax_skip btn btn-success"),
              Submit('presentation-form-save-changes', 'Next', css_class="ajax_submit btn btn-success"),
              css_class="pull-right"
            ),
      )
    else:
      form_actions_layout = FormActions(
            Div(
              Submit('presentation-form-save-changes', 'Next', css_class="ajax_submit btn btn-success"),
              css_class="pull-right"
            ),
      )
    
    title_layout = Layout(
      Div(
        Div(
          Field('presentation_title', css_class="input-xlarge span4"),
          style="display:inline-block;"
        ),
        Div(
          Button("upload-button", "Upload", css_class="btn btn-success"),
          css_id="presentation-upload-button",
          style="display:inline-block; margin-left: 10px;"
        ),
        Div(
          Field('presentation_hidden'),
          style="display:inline-block; margin-left: 10px;"
        )
      )
    )
    common_layout = Layout(
      title_layout,
      Div(
        HTML("""<span id="upload-status">Hello
                </span>
              """),
      ),
      Hidden('presentation_slides','', id="id_presentation_slides"),
      Field('presentation_description', style="resize: none;", css_class="input-xlarge span6"),
      Field('presentation_topics', css_class="input-xlarge span6"),
      Field('presentation_length'),
    )

    if modal_form:                  
      self.helper.layout = Layout(
        common_layout
      )
    else:
      self.helper.layout = Layout(
        Fieldset(
          'Add A Presentation',
          common_layout
        ),
        form_actions_layout
      )    
      
  def clean(self):
    cleaned_data = self.cleaned_data
    
    # Hidden field
    if self.data['presentation_slides']:
      cleaned_data['presentation_slides'] = self.data['presentation_slides']
      
    return cleaned_data
