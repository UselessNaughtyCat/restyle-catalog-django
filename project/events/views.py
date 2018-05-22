import json

from django.http import HttpResponse

from project.style.models import Style

def subscription(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            data = json.loads(request.body)
            subs_style = Style.objects.get(pk=data['style_id'])
            if not subs_style is None:
                response_data = {}
                if subs_style in request.user.person.subscriptions.all():
                    request.user.person.subscriptions.remove(subs_style)
                    response_data['subscribed'] = False
                else:
                    request.user.person.subscriptions.add(subs_style)
                    response_data['subscribed'] = True
                return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
            else:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=401)
