import datetime, time

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.views import generic
from forms import RegistrationUserForm, RegistrationProfileForm, CreateEventForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Event, EventType, Registration, Profile

def index(request, template='events.html', page_template='events_list_page.html'):
    latest_events = Event.objects.filter(event_date__gte=datetime.date.today()).order_by('event_date')[:5]
    event_types = EventType.objects.order_by('name')

    if request.method == 'GET':
        if 'date' in request.GET and request.GET['date'] != '':
            tmp = request.GET['date'].split("-")
            r_event_date = datetime.date(int(tmp[0]),int(tmp[1]),int(tmp[2]))
            dateQ = Q(  event_date__year=r_event_date.year,
                        event_date__month=r_event_date.month,
                        event_date__day=r_event_date.day)
        else:
            dateQ = Q(event_date__gte=datetime.date.today())

        mainQ = dateQ

        if 'type' in request.GET and request.GET['type'] != '' and request.GET['type'] != 'all':
            r_type = request.GET['type']
            typeQ = Q(event_type__name__contains=r_type)
            mainQ = mainQ & typeQ

        if 'title' in request.GET and request.GET['title'] != '':
            r_title = request.GET['title']
            titleQ = Q(title__contains=r_title)
            mainQ = mainQ & titleQ

        if 'organizer' in request.GET and request.GET['organizer'] != '':
            r_org = request.GET['organizer']
            organizerQ = Q(organizer__name__contains=r_org)
            mainQ = mainQ & organizerQ

        events = Event.objects.filter(mainQ).order_by('event_date')
        print mainQ

    context = {
        'latest_events': latest_events,
        'events': events,
        'event_types': event_types,
        'page_template': page_template,
    }


    my_events = Event.objects.filter(
        event_id__in=Registration.objects.filter(user = request.user.id).only(Registration.event)
    )
    #reg = Registration.objects.filter(user = request.user.id).only(Registration.event)
    print '--------'
    print my_events
    print '--------'

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
          page_template='events_list_page.html'):
    if not request.user.is_authenticated():
        return redirect('ffx:signin')

    type = request.GET['type'] if request.GET['type'] else 'to_attend'
    # need to change to filter by role
    if type == 'to_attend':
        events = Event.objects.filter(
            event_id__in=Registration.objects.filter(user=request.user.id).values_list('event_id', flat=True),
            event_date__gte=datetime.date.today()
        ).order_by('event_date')
    elif type == 'attended':
        events = Event.objects.filter(
            event_id__in=Registration.objects.filter(user=request.user.id).values_list('event_id', flat=True),
            event_date__lt=datetime.date.today()
        ).order_by('event_date')
    else:
        events = Event.objects.filter(
            organizer=request.user, event_date__gte=datetime.date.today()
        ).order_by('event_date')

    context = {
        'events': events, 'page_template': page_template, 'type': type
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
            user = authenticate(username=user.username, password=request.POST['password'])
            login(request, user)

            # Redirect to events page
            return redirect('ffx:event_index')
        else:
            return render(request, 'signup.html', {'userform': userform, 'profileform': profileform})

def signout(request):
    logout(request)
    return redirect('/events')

def create(request):
    return render(request, 'events_create.html',{})
