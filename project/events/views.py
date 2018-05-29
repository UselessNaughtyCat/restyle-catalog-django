import json

from django.http import HttpResponse, JsonResponse
from easy_thumbnails.files import get_thumbnailer

from project.style.models import Style, Site, Url

def subscription(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            subs_style = Style.objects.get(pk=data['style_id'])
            if request.user != subs_style.creator:
                if not subs_style is None:
                    response_data = {}
                    if subs_style in request.user.person.subscriptions.all():
                        request.user.person.subscriptions.remove(subs_style)
                        response_data['subscribed'] = False
                        response_data['unsub_style'] = {
                            "id": subs_style.id,
                        }
                    else:
                        request.user.person.subscriptions.add(subs_style)
                        response_data['subscribed'] = True
                        response_data['sub_style'] = {
                            "author": subs_style.creator.user.username,
                            "domains": list(subs_style.site.urls.values_list('name', flat=True)),
                            "enabled": True,
                            "preview": request.scheme + "://" + request.get_host() + get_thumbnailer(subs_style.logo)['style-logo-tmb'].url,
                            "id": subs_style.id,
                            "name": subs_style.name,
                            "styles": json.loads(subs_style.source or "{}"),
                        }
                    subs_style.save()
                    subs_style.subscribed = subs_style.person_set.count()
                    subs_style.save()
                    response_data['subs_count'] = subs_style.person_set.count()
                    return JsonResponse(response_data)
                else:
                    return HttpResponse(status=400)
            else:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=405)

def rating(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            style = Style.objects.get(pk=data['style_id'])
            rate = data['rate']
            if request.user != style.creator:
                if not style is None and not rate is None:
                    response_data = {}
                    # TODO: need make this shit more smarter
                    style.average_rating = (style.average_rating + rate)/2 if style.average_rating != 0 else rate
                    style.average_rating = round(style.average_rating * 100) / 100
                    style.save()
                    response_data['average_rating'] = style.average_rating
                    return JsonResponse(response_data)
                else:
                    return HttpResponse(status=400)
            else:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=405)

def get_site(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        response_data = {}
        try:
            urls_qs = Url.objects.filter(name__in=data['urls'])
            site = Site.objects.get(urls__in=urls_qs)
            response_data['site'] = site.name
        except:
            response_data['site'] = '[new]'+data['urls'][0]
        return JsonResponse(response_data)
    else:
        return HttpResponse(status=405)

def create_style(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            site_str = data["site"]
            selected_site = None
            if site_str.find("[new]") == -1:
                selected_site = Site.objects.get(name=data["site"])
            else:
                l = len("[new]")
                selected_site = Style.get_new_site(site_str[l:], site_str[l:])
            new_style = Style.objects.create(name=data["name"], site=selected_site, source=str(data["styles"]), creator=request.user.person)
            new_style.save()
            response_data = {}
            response_data['id'] = new_style.id
            return JsonResponse(response_data)
        else:
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=405)