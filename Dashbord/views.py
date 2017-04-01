from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from Dashbord.models import Site


def base(request):
    return render(request, 'Dashbord/base.html')


def dashboard(request):
    Sites = Site.objects.all()
    context = {
        'Sites': Sites
    }
    return render(request, 'Dashbord/dashboard.html', context)


def home(request):
    Sites = Site.objects.all()
    context = {
        'Sites': Sites
    }
    return render(request, 'Dashbord/home.html', context)


def software_development(request):
    return render(request, 'Dashbord/software_development.html')


def about(request):
    return render(request, 'Dashbord/about.html')


def json(request):
    if request.is_ajax():
        if request.method == 'GET':
            mimetype = 'Dashbord/json.html'
            #return HttpResponse(mimetype)
            return render(request, mimetype)


        elif request.method == 'POST':
            mimetype = 'Dashbord/json.html'
            #return HttpResponse(mimetype)
            return render(request, mimetype)


    else:
        message = "No support request!"


    return HttpResponse(message)
        #HttpResponse(message)
        #render(request, 'Dashbord/json.html')