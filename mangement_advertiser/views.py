from django.shortcuts import render, get_object_or_404, redirect

from .form import AdForm
from .models import Ad, Advertiser


def show_ad(request):
    advertisers = Advertiser.objects.all()
    for advert in advertisers:
        advert.inc_views()
        advert.save()
        ads = advert.ads.all()
        for ad in ads:
            ad.inc_views()
            ad.save()

    context = {
        'advertisers': advertisers
    }
    return render(request, 'ads.html', context)


def number_of_click(request, ad_id):
    ad = get_object_or_404(Ad, unique_id_ad = ad_id)

    ad.inc_clicks()
    ad.save()

    advertiser = ad.advertiser
    advertiser.inc_clicks()
    advertiser.save()

    external_link = ad.link

    return redirect(external_link)


def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/show_ad/')
    else:
        form = AdForm()

    return render(request, 'create_ad.html', {'form': form})
