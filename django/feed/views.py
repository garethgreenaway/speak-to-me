import logging

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from feed.forms import AddFeedForm
from feed.models import FeedStaging

logger = logging.getLogger('feed.views')

@login_required
def addFeed(request):

	email = request.user.email
	logger.error(email)
	user = User.objects.get(email = email)

	if request.method == 'POST':
		form = AddFeedForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data

			#task_addFeed.delay(FeedStaging(url=cd['url'], user=username))
			FeedStaging(url=cd['url'], user=email).save()
			return HttpResponseRedirect('/feed/added')
	else:
		form = AddFeedForm()

	return render_to_response('addfeed.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def addedFeed(request):
	return render_to_response('addedfeed.html', context_instance=RequestContext(request))
