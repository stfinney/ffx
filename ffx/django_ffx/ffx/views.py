from django.shortcuts import render

# Create your views here.
def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = RequestContext(request, {
    #     'latest_question_list': latest_question_list
    # })
    # return HttpResponse(template.render(context))
    return render(request, 'events.html', {
        'latest_events': [{'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg'},
                          {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg'}],
        'events': [{'title': 'E1', 'description': 'D1', 'image_url': '/static/img/event_1.jpg',
                    'organizer': 'CSE', 'date': '2015-12-10', 'duration': 2, 'location': 'Central Hall'},
                   {'title': 'E2', 'description': 'D2', 'image_url': '/static/img/event_2.jpg',
                    'organizer': 'UCSD Graduate', 'date': '2015-12-20', 'duration': 2, 'location': 'Geisel Library'}]
    })