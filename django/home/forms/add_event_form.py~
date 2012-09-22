from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Field, Fieldset, HTML, Hidden, Layout, Row, Submit
from crispy_forms.bootstrap import AppendedText, FormActions, PrependedText

from django.forms import ModelForm

from home.models import Location, Presentation, UserProfile, Event

import logging
  
logger = logging.getLogger('home.views')

class EventForm(ModelForm):
  class Meta:
    model = Event
    exclude = ('locations', 'event_hash')
           
  def __init__(self, *args, **kwargs):               

    self.helper = FormHelper()
    self.helper.form_id = "id-add-event-form"
    self.helper.form_class = "form-horizontal"
    self.helper.form_method = "post"
    self.helper.form_action = ""
    
    self.helper.layout = Layout(
      Fieldset(
        'Add Event',
        Div(
          Div('event_name', css_class="input-xlarge span4"),
          Div('event_website', css_class="input-xlarge span4"),
          css_class="row-fluid"
        ),
        HTML("<hr />"),
        Div(
          Div('start_date', css_class="span4"),
          Div('end_date', css_class="span4"),
          css_class="row-fluid"),
        ),
        FormActions(
          Submit('event-form-save-changes', 'Next', css_class="ajax_submit btn btn-success pull-right")
        )
      )
    super(EventForm, self).__init__(*args, **kwargs)
