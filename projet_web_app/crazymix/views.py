from django.shortcuts import render

# Create your views here.


def index (request):
    return render (request,'crazymix/index.html')

def infos(request):
    return render(request,'crazymix/infos.html')