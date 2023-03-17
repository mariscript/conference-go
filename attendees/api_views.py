import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Attendee
from events.models import Conference
from common.json import ModelEncoder


class AttendeeListEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "name"
    ]


class AttendeeDetailEncoder(ModelEncoder):
    model = Attendee
    properties = [
        "email",
        "name",
        "company_name",
        "created",
        "conference",
    ]

    def get_extra_data(self, o):
        return {"conference": o.conference.name}


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_id):
    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
            safe=False,
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

        attendee = Attendee.objects.create(**content)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_attendee(request, id):
    if request.method == "GET":
        try:
            attendee = Attendee.objects.get(id=id)
            return JsonResponse(
                attendee,
                encoder=AttendeeDetailEncoder,
                safe=False,
            )
        # added an error message instead of yellow page of sadness
        except Attendee.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid attendee id"},
                status=400,
                )
    elif request.method == "DELETE":
        count, _ = Attendee.objects.filter(id=id).delete()
        return JsonResponse({"deleted": count > 0})
    else:
        content = json.loads(request.body)
        Attendee.objects.filter(id=id).update(**content)
        attendee = Attendee.objects.get(id=id)
        return JsonResponse(
            attendee,
            encoder=AttendeeDetailEncoder,
            safe=False,
        )
