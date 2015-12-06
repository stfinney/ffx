import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views import generic
from forms import RegistrationUserForm, RegistrationProfileForm, CreateEventForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Event, EventType, Registration, Profile

def index(request, template='events.html', page_template='events_list_page.html'):
    latest_events = Event.objects.filter(event_date__gte=datetime.date.today()).order_by('event_date')[:5]
    events = Event.objects.filter(event_date__gte=datetime.date.today()).order_by('event_date')

    event_types = EventType.objects.order_by('name')

    context = {
        'latest_events': latest_events,
        'events': events,
        'event_types': event_types,
        'page_template': page_template,
    }

    if request.is_ajax():
        template = page_template
    return render_to_response(template, context, context_instance=RequestContext(request))

class EventDetail(generic.DetailView):
    model = Event
    template_name = "events_detail.html"

    def get_queryset(self):
        return Event.objects


def register(request, pk):
    # Check if user is logged in
    if not request.user.is_authenticated():
        return JsonResponse({'return_code': 100, 'return_desc': "User not logged in yet"})

    # Check if the user is already registered for the event
    event = get_object_or_404(Event, pk=pk)
    registered = Registration.objects.filter(user=request.user, event=event).exists()
    if registered:
        return JsonResponse({'return_code': 200, 'return_desc': "User has already registered this event"})

    # Register the user for the event
    registration = Registration(user=request.user, event=event)
    registration.save()
    return JsonResponse({'return_code': 0, 'return_desc': 'success'})


def cancel_register(request, event_id):
    # Check if user is logged in
    if not request.user.is_authenticated():
        return JsonResponse({'return_code': 100, 'return_desc': "User not logged in yet"})

    # Check if the user is already registered for the event
    event = get_object_or_404(Event, pk=event_id)
    try:
        # Unregister the user from the event
        registration = Registration.objects.get(user=request.user, event=event)
        registration.delete()

        return JsonResponse({'return_code': 0, 'return_desc': 'success'})
    except Registration.DoesNotExist:
        return JsonResponse({'return_code': 200, 'return_desc': "User hasn't registered this event yet"})


@login_required
def myinfo(request, template='myinfo.html',
          page_template='events_list_page.html',type='p'):
    if type == 'p':
        context = {
            'events': [{'id': 1, 'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
                        'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
                        'tags': 'Free Food, Job Info Session', 'participants_count': 10},
                       {'id': 2, 'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
                        'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
                        'tags': 'Free Food', 'participants_count': 100}],
            'page_template': page_template, 'type': type
        }
    else:
        context = {
            'events': [{'id': 1, 'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_2.jpg',
                        'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
                        'tags': 'Free Food, Job Info Session', 'participants_count': 10},
                       {'id': 2, 'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_1.jpg',
                        'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
                        'tags': 'Free Food', 'participants_count': 100}],
            'page_template': page_template, 'type': type
        }
    if request.is_ajax():
        template = page_template
    return render_to_response(
        template, context, context_instance=RequestContext(request))

@login_required
def myinfo_c(request, template='myinfo_c.html',
          page_template='events_list_page.html'):
    context = {
        'events': [{'id': 1, 'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
                    'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
                    'tags': 'Free Food, Job Info Session', 'participants_count': 10},
                   {'id': 2, 'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
                    'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
                    'tags': 'Free Food', 'participants_count': 100}],
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(
        template, context, context_instance=RequestContext(request))


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('ffx:event_index')
        else:
            return render(request, 'signin.html',{'error': 'Wrong username or password.'})

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html',{})
    elif request.method == 'POST':
        userform = RegistrationUserForm(data=request.POST)
        profileform = RegistrationProfileForm(data=request.POST)

        if userform.is_valid() and profileform.is_valid():
            # Save user and profile
            user = userform.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile = profileform.save(commit=False)
            profile.user = user
            profile.save()

            # Login the user
            login(request, user)

            # Redirect to events page
            return redirect('ffx:event_index')
        else:
            return render(request, 'signup.html', {'userform': userform, 'profileform': profileform})

def signout(request):
    logout(request)
    return redirect('/events')

@login_required
def createevent(request):
    if request.method == 'POST':
        form = CreateEventForm(request.post)
        if form.is_valid():
            event = form.save()
            return redirect('ffx:event_detail', pk=event.id)
    else:
        form = CreateEventForm()
        return render(request, 'createevent.html', {'form': form})
