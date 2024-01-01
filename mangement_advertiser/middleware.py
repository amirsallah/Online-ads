from django.utils.deprecation import MiddlewareMixin

from mangement_advertiser.models import Click, View


class ClickViewMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        if request.path.startswith('/click'):
            click = Click.objects.create(
                ad_id=request.GET.get('ad_id'),
                ip_address=ip_address
            )
            click.save()
        elif request.path.startswith('/view'):
            view = View.objects.create(
                ad_id=request.GET.get('ad_id'),
                ip_address=ip_address
            )
            view.save()
        return None

