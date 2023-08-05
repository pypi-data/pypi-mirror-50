from datetime import date
from typing import List

import pytz
from shuttlis.geography import Location, Path
from shuttlis.time import MilitaryTime, WeekDay
from shuttlis.utils import random_location, uuid4_str

from b2b_rms_sdk.models import (
    Image,
    Stop,
    VIA,
    WayPoint,
    Holiday,
    Shift,
    BookingOpeningTime,
    PartnerSite,
    StopDepartureTime,
    Slot,
    SlotStopDepartureTimes,
    RouteDepartureInfo,
    B2BRoute,
    Partner,
    Schedule,
)


def mt_ist(time):
    tz = pytz.timezone("Asia/Kolkata")
    return MilitaryTime(time, tz)


def mt_utc(time):
    return MilitaryTime(time, pytz.utc)


ist = pytz.timezone("Asia/Kolkata")
utc = pytz.utc


def image_dm(tag="FRONT", url="https://www.google.com") -> Image:
    return Image(tag, url)


def stop_dm(id: str = None, location=None, name="stop_1", images=None) -> Stop:
    return Stop(
        id=id or uuid4_str(),
        location=location or random_location(),
        name=name,
        images=images or [],
    )


def via_dm(location=None) -> VIA:
    return VIA(location=location or random_location())


def way_point_dm(type="PICKUP_AND_DROP", point=None):
    return WayPoint(type=type, point=point or stop_dm())


def slot_dm(day_of_week=WeekDay.MONDAY, start_time=None):
    return Slot(day_of_week=day_of_week, start_time=start_time or mt_ist(900))


def stop_departure_time_dm(stop_id="s1", departure_time=mt_ist(900)):
    return StopDepartureTime(stop_id, departure_time)


def slot_stop_departure_times_dm(slot=None, stop_departure_times=None):
    return SlotStopDepartureTimes(
        slot=slot or slot_dm(),
        stop_departure_times=stop_departure_times or [stop_departure_time_dm()],
    )


def route_departure_info_dm(slot_stop_departures=None):
    return RouteDepartureInfo(
        slot_stop_times_list=slot_stop_departures
        if slot_stop_departures is not None
        else [slot_stop_departure_times_dm()]
    )


def shift_dm(type: str = "START", time: MilitaryTime = None):
    return Shift(type=type, time=time or mt_ist(900))


def partner_dm(id: str = None, name: str = None, email_domains: List[str] = None):
    return Partner(id=id or uuid4_str(), name=name, email_domains=email_domains or [])


def holiday_dm(name: str = "Lodhi", declared_date: date = None):
    return Holiday(name=name, declared_date=declared_date or date(2019, 7, 1))


def partner_site_dm(
    id: str = None,
    name: str = "ps-1",
    location: Location = None,
    shifts: List[Shift] = None,
    booking_opening_time: BookingOpeningTime = None,
    holidays: List[Holiday] = None,
):
    return PartnerSite(
        id=id or uuid4_str(),
        name=name,
        location=location or random_location(),
        shifts=shifts or [shift_dm()],
        booking_opening_time=booking_opening_time,
        holidays=holidays or [],
        partner=partner_dm(),
    )


def b2b_route_dm(
    id="r1",
    name="route-r1",
    number="1",
    partner_site=None,
    way_points=None,
    departure_info=None,
    path=None,
    slots=None,
):
    way_points = way_points or [way_point_dm(), way_point_dm(), way_point_dm()]
    return B2BRoute(
        id=id,
        partner_site=partner_site or partner_site_dm(),
        way_points=way_points,
        departure_info=departure_info or route_departure_info_dm(),
        path=path or Path([wp.location for wp in way_points]),
        schedule=Schedule(slots or [slot_dm(), slot_dm(day_of_week=WeekDay.TUESDAY)]),
        name=name,
        number=number,
    )
