import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Attendee, ConferenceVO
from .encoders import (
    AttendeeListEncoder,
    AttendeeDetailEncoder,
    )


@require_http_methods(["GET", "POST"])
def api_list_attendees(request, conference_vo_id=None):
    if request.method == "GET":
        attendees = Attendee.objects.filter(conference=conference_vo_id)
        return JsonResponse(
            {"attendees": attendees},
            encoder=AttendeeListEncoder,
            safe=False,
        )
    else:
        content = json.loads(request.body)

        try:
            conference_href = f'/api/conferences/{conference_vo_id}/'
            conference = ConferenceVO.objects.get(import_href=conference_href)
            content["conference"] = conference
        except ConferenceVO.DoesNotExist:
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
