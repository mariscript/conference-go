from common.json import ModelEncoder
from .models import Attendee


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
