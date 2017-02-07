from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify

from .models import Profile
from .forms import ProfileForm



def index(request):
   profiles = Profile.objects.all().order_by('?')
   return render(request, 'index.html', {'profiles': profiles,})

def profile_detail(request, slug):
    profile = Profile.objects.get(slug=slug)
    return render(request, 'profiles/profile_detail.html', {'profile': profile,})

@login_required
def edit_profile(request, slug):
	
	profile = Profile.objects.get(slug=slug)

	if profile.user != request.user:
		raise Http404

	form_class = ProfileForm
    
	if request.method == 'POST':

	    form = form_class(data=request.POST, instance=profile)
	    
	    if form.is_valid():
	    	form.save()
	    	return redirect('profile_detail', slug=profile.slug)
	else:
	    form = form_class(instance=profile)
	return render(request, 'profiles/edit_profile.html', {'profile': profile, 'form': form,})

def create_profile(request):
    form_class = ProfileForm

    # if we're coming from a submitted form, do this
    if request.method == 'POST':
        # grab the data from the submitted form and apply to the form
        form = form_class(request.POST)
        if form.is_valid():
            # create an instance but do not save yet
            profile = form.save(commit=False)

            # set the additional details
            profile.user = request.user
            profile.slug = slugify(profile.name)

            # save the object
            profile.save()

            # redirect to our newly created profile
            return redirect('profile_detail', slug=profile.slug)

    # otherwise just create the form
    else:
        form = form_class()

    return render(request, 'profiles/create_profile.html', {
        'form': form,
    })

def browse_by_name(request, initial=None):
    if initial:
        profiles = Profile.objects.filter(name__istartswith=initial)
        profiles = profiles.order_by('name')
    else:
        profiles = Profile.objects.all().order_by('name')

    return render(request, 'search/search.html', {
    	'profiles': profiles,
        'initial': initial,
        })
