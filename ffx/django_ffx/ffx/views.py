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
        'latest_events': [{'name': 'E1', 'desc': 'D1', 'image_url': '/static/img/event_1.jpg'}, {'name': 'E2', 'desc': 'D2', 'image_url': '/static/img/event_2.jpg'}],
        'events': [{'name': 'E1', 'desc': 'D1', 'image_url': '/static/img/event_1.jpg'}, {'name': 'E2', 'desc': 'D2', 'image_url': '/static/img/event_2.jpg'}]
    })