import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Presentation
from events.models import Conference
from common.json import ModelEncoder


class PresentationListEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "title",
        "status",
    ]

    def get_extra_data(self, o):
        return {"status": o.status.name}


class PresentationDetailEncoder(ModelEncoder):
    model = Presentation
    properties = [
        "presenter_name",
        "company_name",
        "presenter_email",
        "title",
        "synopsis",
        "created",
    ]


@require_http_methods(["GET", "POST"])
def api_list_presentations(request, conference_id):
    presentations = Presentation.objects.filter(conference=conference_id)
    if request.method == "GET":
        return JsonResponse(
            {"presentations": presentations},
            encoder=PresentationListEncoder,
            safe="False",
        )
    else:
        content = json.loads(request.body)
        try:
            conference = Conference.objects.get(id=conference_id)
            content["conference"] = conference
        except Conference.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid conference id"},
                status=400,
            )
        presentation = Presentation.create(**content)
        return JsonResponse(
            presentation,
            encoder=PresentationListEncoder,
            safe=False,
        )


@require_http_methods(["GET", "DELETE", "PUT"])
def api_show_presentation(request, id):
    if request.method == "GET":
        try:
            presentation = Presentation.objects.get(id=id)
            return JsonResponse(
                presentation,
                encoder=PresentationDetailEncoder,
                safe=False,
            )
        except Presentation.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid presentation id"},
                status=400,
            )
    elif request.method == "DELETE":
        count, _ = Presentation.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
    Presentation.objects.filter(id=id).update(**content)
    presentation = Presentation.objects.get(id=id)
    return JsonResponse(
        presentation,
        encoder=PresentationDetailEncoder,
        safe=False,
    )
