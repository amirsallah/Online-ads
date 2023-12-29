from django.http import HttpResponse


def show_ad(request):
    # body
    return HttpResponse('Welcome to AmirShop')


def number_of_click(request):
    # body
    return HttpResponse('2')


def create_ad(request):
    # body
    return HttpResponse('3')
