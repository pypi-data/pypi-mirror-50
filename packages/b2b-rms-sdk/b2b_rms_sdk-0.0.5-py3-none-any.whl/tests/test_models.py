import itertools as it

from datetime import datetime, timedelta, date

import pytest
import pytz
from shuttlis.geography import Location
from shuttlis.time import WeekDay, TimeWindow

from b2b_rms_sdk.models import (
    military_time_from_dict,
    location_from_dict,
    Image,
    Stop,
    VIA,
    WayPoint,
    Slot,
    StopDepartureTime,
    SlotStopDepartureTimes,
    RouteDepartureInfo,
    B2BRoute,
)
from tests.factories import (
    mt_ist,
    image_dm,
    stop_dm,
    way_point_dm,
    slot_dm,
    stop_departure_time_dm,
    ist,
    slot_stop_departure_times_dm,
    utc,
    route_departure_info_dm,
    holiday_dm,
    via_dm,
    mt_utc,
    partner_site_dm,
    b2b_route_dm,
)

ist_tz = pytz.timezone("Asia/Kolkata")


def test_from_dict_to_military_time():
    mt_dict = {"time": 1002, "timezone": "Asia/Kolkata"}
    assert mt_ist(1002) == military_time_from_dict(mt_dict)


def test_from_dict_to_location():
    location_dikt = {"lat": 23.234234, "lng": 76.234234}
    assert Location(23.234234, 76.234234) == location_from_dict(location_dikt)


def test_from_dict_to_image():
    tag = "FRONT"
    url = "https://media.mnn.com/assets/images/2012/11/pw_1.jpg"
    image_dict = {"tag": tag, "url": url}
    assert image_dm(tag, url) == Image.from_dict(image_dict)


def test_from_dict_to_stop():
    stop_dict = {
        "created_at": "2019-01-07T07:18:23.313702",
        "description": "dummy_description",
        "id": "6",
        "images": [],
        "location": {"lat": 28.889512, "lng": 77.309528},
        "name": "stop7",
        "tags": ["sample_tag"],
        "updated_at": "2019-01-07T07:18:23.313702",
    }
    stop = stop_dm(id="6", location=Location(28.889512, 77.309528), name="stop7")
    assert stop == Stop.from_dict(stop_dict)


def test_from_dict_to_via():
    via_dict = {"location": {"lat": 23.234234, "lng": 76.234234}}
    assert VIA(location=Location(23.234234, 76.234234)) == VIA.from_dict(via_dict)


def test_from_dict_to_way_point_via():
    via_dict = {"location": {"lat": 23.234234, "lng": 76.234234}}
    via = VIA(location=Location(23.234234, 76.234234))
    way_point_via_dict = {"type": "VIA", "point": via_dict}
    wp = way_point_dm(type="VIA", point=via)

    assert wp == WayPoint.from_dict(way_point_via_dict)


def test_from_dict_to_way_point_stop():
    stop_dict = {
        "created_at": "2019-01-07T07:18:23.313702",
        "description": "dummy_description",
        "id": "6",
        "images": [],
        "location": {"lat": 28.889512, "lng": 77.309528},
        "name": "stop7",
        "tags": ["sample_tag"],
        "updated_at": "2019-01-07T07:18:23.313702",
    }
    stop = stop_dm(id="6", location=Location(28.889512, 77.309528), name="stop7")
    way_point_stop_dict = {"type": "PICKUP", "point": stop_dict}
    wp = way_point_dm(type="PICKUP", point=stop)

    assert wp == WayPoint.from_dict(way_point_stop_dict)


def test_from_dict_to_slot():
    slot_dict = {
        "day_of_week": "MONDAY",
        "start_time": {"time": 1002, "timezone": "Asia/Kolkata"},
    }
    slot = slot_dm(start_time=mt_ist(1002))
    assert slot == Slot.from_dict(slot_dict)


def test_slot_creation_from_datetime():
    tz = pytz.timezone("Asia/Kolkata")
    dt = tz.localize(datetime.fromisoformat("2019-01-07T07:18:00"))
    assert Slot.from_dt(dt) == slot_dm(start_time=mt_ist(718))


def test_slot_ordering():
    slot1 = slot_dm(start_time=mt_ist(723))
    slot2 = slot_dm(start_time=mt_ist(724))
    assert slot1 < slot2


def test_from_dict_to_stop_departure_times():
    stop_deparutre_time = {
        "departure_time": {"time": 500, "timezone": "Asia/Kolkata"},
        "stop_id": "s1",
    }
    stop_departure = stop_departure_time_dm(stop_id="s1", departure_time=mt_ist(500))

    assert stop_departure == StopDepartureTime.from_dict(stop_deparutre_time)


def test_stop_departure_time_conversion_to_concrete_time_for_a_given_date():
    stop_departure_time = stop_departure_time_dm(departure_time=mt_ist(900))
    dt = ist.localize(datetime(2019, 1, 1, 9))

    assert stop_departure_time.for_date(dt.date()).departure_time == dt


def test_from_dict_to_slot_stop_departures():
    slot_stop_times = {
        "departure_times": [
            {
                "departure_time": {"time": 926, "timezone": "Asia/Kolkata"},
                "stop_id": "s1",
            },
            {
                "departure_time": {"time": 943, "timezone": "Asia/Kolkata"},
                "stop_id": "s2",
            },
        ],
        "slot": {
            "day_of_week": "MONDAY",
            "start_time": {"time": 800, "timezone": "Asia/Kolkata"},
        },
    }
    dt1 = stop_departure_time_dm(stop_id="s1", departure_time=mt_ist(926))
    dt2 = stop_departure_time_dm(stop_id="s2", departure_time=mt_ist(943))
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800))
    slot_stop_departures = slot_stop_departure_times_dm(slot, [dt1, dt2])

    assert slot_stop_departures == SlotStopDepartureTimes.from_dict(slot_stop_times)


def test_slot_stop_departure_times_get_departure_time_for_date_returns_none_on_slot_mismatch():
    dt1 = stop_departure_time_dm(stop_id="s1", departure_time=mt_ist(926))
    dt2 = stop_departure_time_dm(stop_id="s2", departure_time=mt_ist(943))
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800))
    slot_stop_departures = slot_stop_departure_times_dm(slot, [dt1, dt2])

    dt = ist.localize(datetime(2019, 1, 1, 9))
    assert slot_stop_departures.get_departure_time_for_date(dt) is None


def test_slot_stop_departure_times_get_departure_time_for_date():
    dt1 = stop_departure_time_dm(stop_id="s1", departure_time=mt_ist(926))
    dt2 = stop_departure_time_dm(stop_id="s2", departure_time=mt_ist(943))
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800))
    slot_stop_departures = slot_stop_departure_times_dm(slot, [dt1, dt2])

    concrete_dts = [
        ist.localize(datetime(2019, 7, 1, 9, 26)),
        ist.localize(datetime(2019, 7, 1, 9, 43)),
    ]

    dt = ist.localize(datetime(2019, 7, 1, 8))
    result = [
        s.departure_time for s in slot_stop_departures.get_departure_time_for_date(dt)
    ]

    assert result == concrete_dts


def test_slot_stop_departure_times_get_departure_time():
    dt1 = stop_departure_time_dm(stop_id="awe_stop", departure_time=mt_ist(926))
    dt2 = stop_departure_time_dm()
    slot = slot_dm()
    slot_stop_departures = slot_stop_departure_times_dm(slot, [dt1, dt2])

    t = slot_stop_departures.get_departure_time_for_stop("awe_stop")

    assert mt_ist(926) == t


def test_slot_stop_departure_times_get_departure_time_for_invalid_stop_returns_none():
    slot = slot_dm()
    slot_stop_departures = SlotStopDepartureTimes(slot, [])
    t = slot_stop_departures.get_departure_time_for_stop("random")

    assert not t


def test_slot_stop_departure_time_for_date():
    tz = pytz.timezone("Asia/Kolkata")
    dt1 = stop_departure_time_dm(departure_time=mt_ist(718))
    slot = slot_dm(start_time=mt_ist(800))
    slot_stop_departures = slot_stop_departure_times_dm(slot, [dt1])

    t = slot_stop_departures.get_departure_time_for_stop_on_date(
        stop_id=dt1.stop_id, dt=datetime.fromisoformat("2019-01-07T07:18:00").date()
    )
    dt = tz.localize(datetime.fromisoformat("2019-01-07T07:18:00"))
    assert dt == t


def test_slot_stop_departure_time_for_date_when_date_does_not_concide_with_slot():
    dt1 = stop_departure_time_dm(departure_time=mt_ist(718))
    slot = slot_dm(day_of_week=WeekDay.MONDAY)
    slot_stop_departures = slot_stop_departure_times_dm(slot, [dt1])

    t = slot_stop_departures.get_departure_time_for_stop_on_date(
        stop_id=dt1.stop_id, dt=datetime.fromisoformat("2019-01-09T07:18:00").date()
    )
    assert t is None


@pytest.mark.parametrize(
    "slot,start_date,first",
    [
        (
            Slot(day_of_week=WeekDay.MONDAY, start_time=mt_ist(900)),
            ist.localize(datetime(year=2019, month=1, day=7, hour=8)),
            ist.localize(datetime(year=2019, month=1, day=7, hour=9)),
        ),
        (
            Slot(day_of_week=WeekDay.MONDAY, start_time=mt_ist(930)),
            ist.localize(datetime(year=2019, month=1, day=7, hour=8)),
            ist.localize(datetime(year=2019, month=1, day=7, hour=9, minute=30)),
        ),
        (
            Slot(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800)),
            ist.localize(datetime(year=2019, month=1, day=7, hour=8)),
            ist.localize(datetime(year=2019, month=1, day=7, hour=8)),
        ),
        (
            Slot(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800)),
            ist.localize(datetime(year=2019, month=1, day=7, hour=9)),
            ist.localize(datetime(year=2019, month=1, day=14, hour=8)),
        ),
        (
            Slot(day_of_week=WeekDay.TUESDAY, start_time=mt_ist(800)),
            ist.localize(datetime(year=2019, month=1, day=7, hour=9)),
            ist.localize(datetime(year=2019, month=1, day=8, hour=8)),
        ),
        (
            Slot(day_of_week=WeekDay.TUESDAY, start_time=mt_ist(800)),
            ist.localize(datetime(year=2019, month=1, day=9, hour=9)),
            ist.localize(datetime(year=2019, month=1, day=15, hour=8)),
        ),
        (
            Slot(day_of_week=WeekDay.TUESDAY, start_time=mt_utc(800)),
            ist.localize(datetime(year=2019, month=1, day=8, hour=9)),
            utc.localize(datetime(year=2019, month=1, day=8, hour=8)),
        ),
    ],
)
def test_slot_occurrences(slot, start_date, first):
    occurrences = [first, first + timedelta(days=7), first + timedelta(days=14)]
    assert occurrences == list(it.islice(slot.occurrences(start_date), 3))


def test_slot_occurrences_in_time_window_raises_error_when_no_upper_limit():
    slot = slot_dm()
    tw = TimeWindow()
    with pytest.raises(ValueError):
        slot.occurrences_in_window(tw)


def test_slot_occurrences_in_time_window():
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(900))
    tw = TimeWindow(
        ist.localize(datetime(year=2019, month=1, day=7, hour=8)),
        ist.localize(datetime(year=2019, month=1, day=28, hour=8)),
    )
    occurrences = [
        ist.localize(datetime(year=2019, month=1, day=7, hour=9)),
        ist.localize(datetime(year=2019, month=1, day=14, hour=9)),
        ist.localize(datetime(year=2019, month=1, day=21, hour=9)),
    ]
    assert occurrences == slot.occurrences_in_window(tw)


def test_from_dict_to_route_departure_info():
    slot_stop_times = {
        "departure_times": [
            {
                "departure_time": {"time": 926, "timezone": "Asia/Kolkata"},
                "stop_id": "s1",
            },
            {
                "departure_time": {"time": 943, "timezone": "Asia/Kolkata"},
                "stop_id": "s2",
            },
        ],
        "slot": {
            "day_of_week": "MONDAY",
            "start_time": {"time": 800, "timezone": "Asia/Kolkata"},
        },
    }
    dt1 = stop_departure_time_dm(stop_id="s1", departure_time=mt_ist(926))
    dt2 = stop_departure_time_dm(stop_id="s2", departure_time=mt_ist(943))
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800))
    slot_stop_departures = slot_stop_departure_times_dm(slot, [dt1, dt2])
    route_departure_info = RouteDepartureInfo([slot_stop_departures])

    assert route_departure_info == RouteDepartureInfo.from_dict([slot_stop_times])


def test_route_departure_info_get_departure_time_for_returns_time_for_a_potential_trip():
    tz = pytz.timezone("Asia/Kolkata")
    dt1 = stop_departure_time_dm(departure_time=mt_ist(718))
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(718))
    slot_stop_departures = slot_stop_departure_times_dm(slot, [dt1])
    route_departure_info = RouteDepartureInfo([slot_stop_departures])

    t = route_departure_info.get_departure_time_for_stop(
        stop_id="s1",
        start_time=tz.localize(datetime.fromisoformat("2019-01-07T07:18:00")),
    )
    dt = tz.localize(datetime.fromisoformat("2019-01-07T07:18:00"))
    assert dt == t


def test_route_departure_info_trip_start_time_generation():
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(900))
    slot_stop_departures_1 = slot_stop_departure_times_dm(slot)

    slot = slot_dm(day_of_week=WeekDay.TUESDAY, start_time=mt_ist(800))
    slot_stop_departures_2 = slot_stop_departure_times_dm(slot)

    route_departure_info = route_departure_info_dm(
        [slot_stop_departures_1, slot_stop_departures_2]
    )

    tw = TimeWindow(
        ist.localize(datetime(year=2019, month=1, day=7, hour=8)),
        ist.localize(datetime(year=2019, month=1, day=21, hour=10)),
    )

    occurrences = [
        ist.localize(datetime(year=2019, month=1, day=7, hour=9)),
        ist.localize(datetime(year=2019, month=1, day=8, hour=8)),
        ist.localize(datetime(year=2019, month=1, day=14, hour=9)),
        ist.localize(datetime(year=2019, month=1, day=15, hour=8)),
        ist.localize(datetime(year=2019, month=1, day=21, hour=9)),
    ]

    assert occurrences == route_departure_info.get_trip_start_times(tw)


def test_route_departure_info_trip_start_time_is_in_utc():
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(900))
    slot_stop_departures_1 = slot_stop_departure_times_dm(slot)
    route_departure_info = route_departure_info_dm([slot_stop_departures_1])
    tw = TimeWindow(
        ist.localize(datetime(year=2019, month=1, day=7, hour=8)),
        ist.localize(datetime(year=2019, month=1, day=21, hour=10)),
    )
    occurrences = [
        ist.localize(datetime(year=2019, month=1, day=7, hour=9)),
        ist.localize(datetime(year=2019, month=1, day=14, hour=9)),
        ist.localize(datetime(year=2019, month=1, day=21, hour=9)),
    ]

    start_times = route_departure_info.get_trip_start_times(tw)
    assert occurrences == start_times
    assert {pytz.utc} == {dt.tzinfo for dt in start_times}


def test_route_departure_info_returns_proper_tz_info():
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(900))
    slot_stop_departures_1 = slot_stop_departure_times_dm(slot)
    route_departure_info = route_departure_info_dm([slot_stop_departures_1])
    assert pytz.timezone("Asia/Kolkata") == route_departure_info.tz


def test_route_departure_info_returns_next_operational_day():
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(900))
    slot_stop_departures_1 = slot_stop_departure_times_dm(slot)
    route_departure_info = route_departure_info_dm([slot_stop_departures_1])

    d = date(year=2019, month=6, day=6)

    assert route_departure_info.next_operational_day_after(d) == date(
        year=2019, month=6, day=10
    )


def test_route_departure_info_returns_next_operational_day_when_slot_on_same_day():
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(900))
    slot_stop_departures_1 = slot_stop_departure_times_dm(slot)
    route_departure_info = route_departure_info_dm([slot_stop_departures_1])

    d = date(year=2019, month=6, day=10)

    assert route_departure_info.next_operational_day_after(d) == date(
        year=2019, month=6, day=17
    )


def test_route_departure_info_next_opeartional_day_returns_none_for_route_wo_slots():
    route_departure_info = RouteDepartureInfo([])
    d = date(year=2019, month=6, day=10)

    assert route_departure_info.next_operational_day_after(d) is None


def test_route_departure_info_get_departure_time_for_returns_concreate_times():
    dt1 = stop_departure_time_dm(stop_id="s1", departure_time=mt_ist(926))
    dt2 = stop_departure_time_dm(stop_id="s2", departure_time=mt_ist(943))
    slot = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800))
    slot_stop_departures = slot_stop_departure_times_dm(slot, [dt1, dt2])
    route_departure_info = route_departure_info_dm([slot_stop_departures])

    concrete_dts = [
        ist.localize(datetime(2019, 7, 1, 9, 26)),
        ist.localize(datetime(2019, 7, 1, 9, 43)),
    ]

    dt = ist.localize(datetime(2019, 7, 1, 8))
    result = [s.departure_time for s in route_departure_info.get_departure_time_for(dt)]
    assert result == concrete_dts


def test_route_deaparture_info_slots_returns_slots_in_sorted_order():
    dt1 = stop_departure_time_dm(stop_id="s1", departure_time=mt_ist(926))
    dt2 = stop_departure_time_dm(stop_id="s2", departure_time=mt_ist(943))
    slot1 = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800))
    slot2 = slot_dm(day_of_week=WeekDay.FRIDAY, start_time=mt_ist(900))
    slot_stop_departures1 = slot_stop_departure_times_dm(slot1, [dt1, dt2])
    slot_stop_departures2 = slot_stop_departure_times_dm(slot2, [dt1, dt2])
    route_departure_info = route_departure_info_dm(
        [slot_stop_departures2, slot_stop_departures1]
    )

    assert [slot1, slot2] == route_departure_info.slots


def test_route_departure_info_occurences_in_time_window():
    slot1 = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800))
    slot2 = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(900))
    slot3 = slot_dm(day_of_week=WeekDay.FRIDAY, start_time=mt_ist(900))

    slot_stop_departures1 = slot_stop_departure_times_dm(slot1, [])
    slot_stop_departures2 = slot_stop_departure_times_dm(slot2, [])
    slot_stop_departures3 = slot_stop_departure_times_dm(slot3, [])

    route_departure_info = route_departure_info_dm(
        [slot_stop_departures2, slot_stop_departures1, slot_stop_departures3]
    )

    time_window = TimeWindow(
        from_date=ist.localize(datetime(2019, 7, 1, 8, 30)),
        to_date=ist.localize(datetime(2019, 7, 8, 8, 30)),
    )

    concrete_dts = [
        ist.localize(datetime(2019, 7, 1, 9)),
        ist.localize(datetime(2019, 7, 5, 9)),
        ist.localize(datetime(2019, 7, 8, 8)),
    ]

    assert route_departure_info.occurences_in_window(time_window) == concrete_dts


def test_route_departure_info_get_departure_time_for_returns_none_on_slot_mismatch():
    route_departure_info = route_departure_info_dm([])

    dt = ist.localize(datetime(2019, 7, 1, 9))
    assert route_departure_info.get_departure_time_for(dt) is None


@pytest.mark.parametrize(
    "dt", [ist.localize(datetime(2019, 7, 1, 7)), ist.localize(datetime(2019, 7, 1, 3))]
)
def test_holiday_returns_true_if_datetime_falls_on_that_day(dt):
    d = date(2019, 7, 1)
    holiday = holiday_dm(declared_date=d)
    assert dt in holiday


@pytest.mark.parametrize("dt", [ist.localize(datetime(2019, 7, 2, 3))])
def test_holiday_returns_false_if_datetime_does_no_fall_on_that_day(dt):
    d = date(2019, 7, 1)
    holiday = holiday_dm(declared_date=d)
    assert dt not in holiday


def test_from_dict_to_route():
    route_dict = {
        "approver": None,
        "created_at": "2019-01-07T07:18:23.358624",
        "creator": {"id": "acb7c10e-f8ef-49d9-b58b-21380fc1a4d9", "type": "user"},
        "description": "dummy description",
        "id": "e3f51a8f-bf90-48ea-8d28-c2ccbd5afd3b",
        "last_updated_by": {
            "id": "acb7c10e-f8ef-49d9-b58b-21380fc1a4d9",
            "type": "user",
        },
        "name": "one_two_route",
        "route_number": 1147,
        "old_id": None,
        "path": {"type": "path"},
        "revision": "60fd1f95-f4f1-4d09-b470-4f9536b93bee",
        "slots": [
            {
                "day_of_week": "MONDAY",
                "start_time": {"time": 800, "timezone": "Asia/Kolkata"},
            }
        ],
        "state": "ACTIVE",
        "updated_at": "2019-01-07T07:18:23.358624",
        "way_points": [
            {
                "point": {
                    "created_at": "2019-01-07T07:18:23.013509",
                    "description": "dummy_description",
                    "id": "5ccfaab0-7691-4e65-882f-456ae0840221",
                    "images": [],
                    "location": {"lat": 24, "lng": 77},
                    "name": "stop1",
                    "tags": ["sample_tag"],
                    "updated_at": "2019-01-07T07:18:23.013509",
                },
                "type": "PICKUP_AND_DROP",
            },
            {
                "point": {
                    "created_at": "2019-01-07T07:18:23.337257",
                    "description": "dummy_description",
                    "id": "63e363c1-22ce-4f7b-ada2-cb96bc2d562f",
                    "images": [],
                    "location": {"lat": 28.864796, "lng": 77.290286},
                    "name": "stop8",
                    "tags": ["sample_tag"],
                    "updated_at": "2019-01-07T07:18:23.337257",
                },
                "type": "PICKUP_AND_DROP",
            },
        ],
        "partner_site": {
            "name": "Google 32nd ave",
            "location": {"lat": 28.864796, "lng": 77.290286},
            "config": {"nfc": True},
            "shifts": [
                {"type": "START", "time": {"time": 800, "timezone": "Asia/Kolkata"}}
            ],
            "holidays": [],
            "booking_opening_time": {
                "days_before_booking": 1,
                "time_of_day": {"time": 800, "timezone": "Asia/Kolkata"},
            },
            "created_at": "2018-04-27T17:53:20",
            "updated_at": "2018-04-27T17:53:20",
            "id": "8cc5b8a9-1e3d-4928-b6c5-b0a311757fc4",
            "partner": {
                "id": "8cc5b8a9-1e3d-4928-b6c5-b0a311757fc4",
                "name": "Google",
                "email_domains": ["@google.com"],
                "created_at": "2018-04-27T17:53:20",
                "updated_at": "2018-04-27T17:53:20",
            },
        },
    }
    route_path_dict = [{"lat": 24, "lng": 77}, {"lat": 28.864796, "lng": 77.290286}]
    stop_times = [
        {
            "departure_times": [
                {
                    "departure_time": {"time": 800, "timezone": "Asia/Kolkata"},
                    "stop_id": "5ccfaab0-7691-4e65-882f-456ae0840221",
                },
                {
                    "departure_time": {"time": 943, "timezone": "Asia/Kolkata"},
                    "stop_id": "63e363c1-22ce-4f7b-ada2-cb96bc2d562f",
                },
            ],
            "slot": {
                "day_of_week": "MONDAY",
                "start_time": {"time": 800, "timezone": "Asia/Kolkata"},
            },
        }
    ]

    route = B2BRoute.from_dict(route_dict, route_path_dict, stop_times)

    assert route.id == "e3f51a8f-bf90-48ea-8d28-c2ccbd5afd3b"


def test_way_point_of_type_via_throw_value_error_when_trying_to_access_stop_id():
    wp = way_point_dm(type="VIA", point=via_dm())
    with pytest.raises(ValueError):
        wp.stop_id


def test_way_point_of_type_stop_returns_stop_id_when_accessing_stop_id():
    stop = stop_dm()
    wp = way_point_dm(type="VIA", point=stop)

    assert wp.stop_id == stop.id


def test_route_start_time_generation():
    slot1 = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800))
    slot2 = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(900))
    slot3 = slot_dm(day_of_week=WeekDay.FRIDAY, start_time=mt_ist(900))

    slot_stop_departures1 = slot_stop_departure_times_dm(slot1, [])
    slot_stop_departures2 = slot_stop_departure_times_dm(slot2, [])
    slot_stop_departures3 = slot_stop_departure_times_dm(slot3, [])

    route_departure_info = route_departure_info_dm(
        [slot_stop_departures2, slot_stop_departures1, slot_stop_departures3]
    )
    route = b2b_route_dm(departure_info=route_departure_info)

    time_window = TimeWindow(
        from_date=ist.localize(datetime(2019, 7, 1, 8, 30)),
        to_date=ist.localize(datetime(2019, 7, 8, 8, 30)),
    )

    concrete_dts = [
        ist.localize(datetime(2019, 7, 1, 9)),
        ist.localize(datetime(2019, 7, 5, 9)),
        ist.localize(datetime(2019, 7, 8, 8)),
    ]

    assert route.start_times(time_window) == concrete_dts


def test_route_start_times_respect_holidays():
    slot1 = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(800))
    slot2 = slot_dm(day_of_week=WeekDay.MONDAY, start_time=mt_ist(900))
    slot3 = slot_dm(day_of_week=WeekDay.FRIDAY, start_time=mt_ist(900))

    slot_stop_departures1 = slot_stop_departure_times_dm(slot1, [])
    slot_stop_departures2 = slot_stop_departure_times_dm(slot2, [])
    slot_stop_departures3 = slot_stop_departure_times_dm(slot3, [])

    route_departure_info = route_departure_info_dm(
        [slot_stop_departures2, slot_stop_departures1, slot_stop_departures3]
    )
    holiday = holiday_dm(declared_date=date(2019, 7, 1))
    partner_site = partner_site_dm(holidays=[holiday])

    route = b2b_route_dm(departure_info=route_departure_info, partner_site=partner_site)

    time_window = TimeWindow(
        from_date=ist.localize(datetime(2019, 7, 1, 8, 30)),
        to_date=ist.localize(datetime(2019, 7, 8, 8, 30)),
    )

    concrete_dts = [
        ist.localize(datetime(2019, 7, 5, 9)),
        ist.localize(datetime(2019, 7, 8, 8)),
    ]

    assert route.start_times(time_window) == concrete_dts
