import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views import generic
from forms import RegistrationUserForm, RegistrationProfileForm, CreateEventForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Event, EventType, Registration, Profile

def index(request, template='events.html', page_template='events_list_page.html'):
    latest_events = Event.objects.filter(event_date__gte=datetime.date.today()).order_by('-event_date')[:5]
    events = Event.objects.filter(event_date__gte=datetime.date.today()).order_by('-event_date')

    context = {
        'latest_events': latest_events,
        'events': events,
        #'latest_events': [{'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg'},
        #                  {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg'}],
        #'events': [{'id': 1, 'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
        #            'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
        #            'tags': 'Free Food, Job Info Session', 'participants_count': 10},
        #           {'id': 2, 'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
        #            'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
        #            'tags': 'Free Food', 'participants_count': 100},
        #           {'id': 3, 'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
        #            'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
        #            'tags': 'Free Food, Job Info Session', 'participants_count': 2},
        #           {'id': 4, 'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
        #            'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
        #            'tags': 'Free Food', 'participants_count': 51},
        #           {'id': 5, 'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
        #            'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
        #            'tags': 'Free Food, Job Info Session', 'participants_count': 33},
        #           {'id': 6, 'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
        #            'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
        #            'tags': 'Free Food', 'participants_count': 23},
        #           {'id': 7, 'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
        #            'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
        #            'tags': 'Free Food, Job Info Session', 'participants_count': 12},
        #           {'id': 8, 'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
        #            'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
        #            'tags': 'Free Food', 'participants_count': 15},
        #           {'id': 9, 'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
        #            'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
        #            'tags': 'Free Food, Job Info Session', 'participants_count': 0},
        #           {'id': 10, 'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
        #            'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
        #            'tags': 'Free Food', 'participants_count': 0},
        #           {'id': 11, 'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
        #            'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
        #            'tags': 'Free Food, Job Info Session', 'participants_count': 1},
        #           {'id': 12, 'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
        #            'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
        #            'tags': 'Free Food', 'participants_count': 2},
        #           {'id': 13, 'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
        #            'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
        #            'tags': 'Free Food, Job Info Session', 'participants_count': 3},
        #           {'id': 14, 'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
        #            'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
        #            'tags': 'Free Food', 'participants_count': 3}],
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

    #event = {
    #    'id': 1,
    #    'title': 'E2',
    #    'description': "HOPE EVERYONE HAD A GREAT DANKSGIVING BUT IT'S WEEK 10 NOW. YO'RE READY TO CRY. "
    #                   "YOU'RE READY TO GO HOME TO THE FAMILY AND TELL THEM ABOUT HOW YOU ACED THAT TEST "
    #                   "BUT IN YOUR MIND YOU'RE WONDERING IF THEY ARE ACTUALLY BUYING YOUR BULLSHIT. "
    #                   "YOU'RE WONDERING WHY THE HELL DO YOU HAVE A TEST DURING WEEK 10. YOU WANNA BUY FOOD BUT MONEY IS "
    #                   "TIGHT AND ALL THAT IS LEFT IN THE CUPBOARD IS A BOX OF STALE CT CRUNCH AND A SMALL "
    #                   "BAG OF CANDY FROM HALLOWEEN FULL OF CRUSHED SMARTIES AND DISAPPOINTMENTS. "
    #                   "YOU CAN'T WAIT TO GO HOME TO MAMA'S COOKING, YOUR AUNT'S SHITTY FRUIT CAKE, AND YOUR DRUNK UNCLE "
    #                   "YELLING ABOUT HOW IT'S TOO DAMN COLD IN HERE. WE ALL ARE LOOKING FORWARD TO BREAK, BUT WHAT ABOUT "
    #                   "A BREAK BEFORE BREAK? A BREAK THAT IS AFTER DANKSGIVING BREAK BUT STILL BEFORE LITMAS BREAK. "
    #                   "WELL LOOK NO FURTHER!!! THIS FRIDAY WE HAVE A DOUBLE HEADER, MEN'S AND WOMEN'S BASKETBALL "
    #                   "ARE LOOKING TO GO INTO FINALS WEEK WITH A WIN AGAINST CSUMB. REMEMBER THAT TIME I TALKED ABOUT FOOD??"
    #                   " WE DECIDED TO GO ALL OUT AND GET Y'ALL PHIL'S BBQ. IT WILL BE SERVED BETWEEN THE MEN'S AND WOMEN'S"
    #                   " GAME RIGHT OUTSIDE OF THE ARENA NEXT TO HOMEPLATE. I KNOW I LIKE TO SPEND MY STUDY BREAKS BINGE "
    #                   "WATCHING NETFLIX SHOWS BUT INSTEAD SPEND IT WITH US AT THE GAME! LETS GET WEIRD. IT'S LIT.",
    #    'image_url': '/static/img/event_2.jpg',
    #    'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
    #    'tags': 'Free Food', 'participants_count': 3
    #}
    #return render(request, 'events_detail.html', {'event': event})


def register(request, event_id):
    # check whether user login
    event_id = int(event_id)
    if event_id % 3 == 0:
        return JsonResponse({'return_code': 0, 'return_desc': 'success'})
    elif event_id % 3 == 1:
        return JsonResponse({'return_code': 100, 'return_desc': "User doesn't login yet"})
    else:
        return JsonResponse({'return_code': 200, 'return_desc': "User has already registered this event"})

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
