from django.shortcuts import render, render_to_response


# Create your views here.
from django.template import RequestContext


def index(request, template='events.html',
        page_template='events_list_page.html'):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = RequestContext(request, {
    #     'latest_question_list': latest_question_list
    # })
    # return HttpResponse(template.render(context))

    context = {
        'latest_events': [{'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg'},
                          {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg'}],
        'events': [{'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
                    'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
                    'tags': 'Free Food, Job Info Session'},
                   {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
                    'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
                    'tags': 'Free Food'},
                   {'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
                    'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
                    'tags': 'Free Food, Job Info Session'},
                   {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
                    'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
                    'tags': 'Free Food'},
                   {'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
                    'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
                    'tags': 'Free Food, Job Info Session'},
                   {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
                    'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
                    'tags': 'Free Food'},
                   {'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
                    'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
                    'tags': 'Free Food, Job Info Session'},
                   {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
                    'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
                    'tags': 'Free Food'},
                   {'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
                    'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
                    'tags': 'Free Food, Job Info Session'},
                   {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
                    'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
                    'tags': 'Free Food'},
                   {'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
                    'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
                    'tags': 'Free Food, Job Info Session'},
                   {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
                    'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
                    'tags': 'Free Food'},
                   {'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
                    'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall',
                    'tags': 'Free Food, Job Info Session'},
                   {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
                    'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library',
                    'tags': 'Free Food'}],
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render_to_response(
        template, context, context_instance=RequestContext(request))