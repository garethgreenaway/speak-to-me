from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Field, Fieldset, HTML, Hidden, Layout, Row, Submit
from crispy_forms.bootstrap import AppendedText, FormActions, PrependedText

from django.forms import ModelForm

from home.forms.profile_presentation_form import ProfilePresentationForm
from home.forms.profile_location_form import ProfileLocationForm
from home.forms.profile_personal_form import ProfilePersonalForm
from home.forms.advanced_search_form import AdvancedSearchForm
from home.forms.add_event_form import EventForm

import logging
  
logger = logging.getLogger('home.views')
