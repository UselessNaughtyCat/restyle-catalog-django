import json

from django.http import HttpResponse, JsonResponse

from project.style.models import Style

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
                        subs_style.subscribed -= 1
                        response_data['subscribed'] = False
                    else:
                        request.user.person.subscriptions.add(subs_style)
                        subs_style.subscribed += 1
                        response_data['subscribed'] = True
                    subs_style.save()
                    response_data['subs_count'] = subs_style.subscribed
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