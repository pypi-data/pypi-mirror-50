import itertools as it
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, date, timedelta, time
from typing import List, Union, Optional, Dict, Set

import pytz
from shuttlis.geography import Location
from shuttlis.time import WeekDay, MilitaryTime, total_ordering, TimeWindow


def military_time_from_dict(mt_dikt) -> MilitaryTime:
    return MilitaryTime(time=mt_dikt["time"], tzinfo=pytz.timezone(mt_dikt["timezone"]))


def location_from_dict(location_dikt) -> Location:
    return Location(lat=location_dikt["lat"], lng=location_dikt["lng"])


@dataclass
class Image:
    tag: str
    url: str

    @classmethod
    def from_dict(cls, dikt) -> "Image":
        return cls(tag=dikt["tag"], url=dikt["url"])


@dataclass(frozen=True)
class Stop:
    id: str
    location: Location
    name: str
    images: List[Image]

    @classmethod
    def from_dict(cls, dikt) -> "Stop":
        return cls(
            id=dikt["id"],
            name=dikt["name"],
            location=location_from_dict(dikt["location"]),
            images=[Image.from_dict(image_dict) for image_dict in dikt["images"]],
        )


@dataclass
class VIA:
    location: Location

    @classmethod
    def from_dict(cls, dikt) -> "VIA":
        return cls(location=location_from_dict(dikt["location"]))


@dataclass
class WayPoint:
    type: str
    point: Union[Stop, VIA]

    @classmethod
    def from_dict(cls, dikt) -> "WayPoint":
        wp_type = dikt["type"]

        if wp_type == "VIA":
            return cls(type=wp_type, point=VIA.from_dict(dikt["point"]))

        if wp_type in ["PICKUP", "DROP", "PICKUP_AND_DROP"]:
            return cls(type=wp_type, point=Stop.from_dict(dikt["point"]))

        raise RuntimeError("Invalid WayPoint type")

    @property
    def stop_id(self) -> str:
        if isinstance(self.point, Stop):
            return self.point.id
        raise ValueError("VIA Point don't have id")

    @property
    def location(self):
        return self.point.location

    def is_stop(self):
        return self.type != "VIA"


@total_ordering
@dataclass(frozen=True)
class Slot:
    day_of_week: WeekDay
    start_time: MilitaryTime

    @property
    def tz(self) -> pytz.timezone:
        return self.start_time.tz

    def __lt__(self, other):
        if self.day_of_week == other.day_of_week:
            return self.start_time < other.start_time
        return self.day_of_week < other.day_of_week

    def occurrences(self, date: datetime = None):
        dt = date or datetime.utcnow()
        dt = dt.astimezone(self.tz)
        dt = self._first_occurrence_from(dt)
        while True:
            yield dt.astimezone(pytz.utc)
            dt = self._next_week_occurence(dt)

    def occurrences_in_window(self, time_window: TimeWindow) -> List[datetime]:
        if not time_window.to_date:
            raise ValueError("Time Window should have upper limit")

        gen = self.occurrences(time_window.from_date)
        return list(it.takewhile(lambda o: o < time_window.to_date, gen))

    def _first_occurrence_from(self, dt):
        days_ahead = self.day_of_week - WeekDay.extract_from_datetime(dt)
        if days_ahead == 0 and self.start_time < MilitaryTime.extract_from_datetime(dt):
            days_ahead = 7
        dt += timedelta(days=days_ahead)
        return self.start_time.combine(dt.date())

    def _next_week_occurence(self, dt: datetime) -> datetime:
        return dt + timedelta(days=7)

    @classmethod
    def from_dt(cls, dt: datetime) -> "Slot":
        mt = MilitaryTime.extract_from_datetime(dt)
        weekday = WeekDay.extract_from_datetime(dt)

        return cls(weekday, mt)

    @classmethod
    def from_dict(cls, dikt):
        return cls(
            day_of_week=WeekDay[dikt["day_of_week"]],
            start_time=military_time_from_dict(dikt["start_time"]),
        )


@dataclass
class ConcreteStopDepartureTime:
    stop_id: str
    departure_time: datetime


@dataclass
class StopDepartureTime:
    stop_id: str
    departure_time: MilitaryTime

    @classmethod
    def from_dict(cls, dikt) -> "StopDepartureTime":
        return cls(
            stop_id=dikt["stop_id"],
            departure_time=military_time_from_dict(dikt["departure_time"]),
        )

    def for_date(self, d: date) -> ConcreteStopDepartureTime:
        dt = self.departure_time.combine(d)
        return ConcreteStopDepartureTime(self.stop_id, dt)


@dataclass
class SlotStopDepartureTimes:
    def __init__(self, slot: Slot, stop_departure_times: List[StopDepartureTime]):
        self.slot = slot
        self.stop_departure_times = stop_departure_times
        self._times = {s.stop_id: s.departure_time for s in stop_departure_times}

    def get_departure_time_for_stop(self, stop_id: str) -> Optional[MilitaryTime]:
        departure_mt = self._times.get(stop_id)
        if not departure_mt:
            return None

        return departure_mt

    def get_departure_time_for_date(
        self, dt: datetime
    ) -> Optional[List[ConcreteStopDepartureTime]]:
        slot = Slot.from_dt(dt)
        if slot != self.slot:
            return None

        return [sdt.for_date(dt.date()) for sdt in self.stop_departure_times]

    def get_departure_time_for_stop_on_date(
        self, stop_id: str, dt: date = None
    ) -> Optional[datetime]:
        departure_mt = self.get_departure_time_for_stop(stop_id)
        if not departure_mt:
            return None

        weekday = WeekDay.extract_from_date(dt)
        if self.slot.day_of_week != weekday:
            return None

        dt = datetime.combine(dt, time=departure_mt.tz_unaware_time())
        return departure_mt.tz.localize(dt)

    @classmethod
    def from_dict(cls, dikt) -> "SlotStopDepartureTimes":
        slot = Slot.from_dict(dikt["slot"])
        stop_departure_times = [
            StopDepartureTime.from_dict(dt) for dt in dikt["departure_times"]
        ]
        return cls(slot=slot, stop_departure_times=stop_departure_times)


@dataclass
class RouteDepartureInfo:
    def __init__(self, slot_stop_times_list: List[SlotStopDepartureTimes]):
        self._data = {s.slot: s for s in slot_stop_times_list}

    @property
    def tz(self) -> Optional[pytz.timezone]:
        if not self._data:
            return None

        return next(iter(self._data.keys())).tz

    @property
    def slots(self) -> List[Slot]:
        return list(sorted(self._data.keys()))

    def occurences_in_window(self, time_window: TimeWindow) -> List[datetime]:
        all_occurences = it.chain.from_iterable(
            slot.occurrences_in_window(time_window) for slot in self.slots
        )
        return list(sorted(all_occurences))

    def next_operational_day_after(self, d: date = None) -> Optional[date]:
        if not self._data:
            return None

        dt = self.tz.localize(datetime.combine(d, time(hour=0, minute=0, second=1)))

        slot_occurences = (slot.occurrences(dt) for slot in self._data)
        all_next_occurences = it.chain.from_iterable(
            (next(o), next(o)) for o in slot_occurences
        )

        def present_day_slot(dt: datetime):
            return dt.astimezone(self.tz).date() == d

        return next(it.dropwhile(present_day_slot, sorted(all_next_occurences))).date()

    def get_departure_time_for_stop(
        self, stop_id: str, start_time: datetime
    ) -> Optional[datetime]:
        same_tz_start_time = start_time.astimezone(self.tz)
        slot = Slot.from_dt(same_tz_start_time)
        departure_times = self._data.get(slot)

        if not departure_times:
            return None

        dt = departure_times.get_departure_time_for_stop_on_date(
            stop_id, start_time.date()
        )

        if not dt:
            return None

        return dt.astimezone(pytz.utc)

    def get_departure_time_for(
        self, start_time: datetime
    ) -> Optional[List[ConcreteStopDepartureTime]]:
        same_tz_start_time = start_time.astimezone(self.tz)

        slot = Slot.from_dt(same_tz_start_time)
        slot_stop_departure_times: SlotStopDepartureTimes = self._data.get(slot)

        if not slot_stop_departure_times:
            return None

        return slot_stop_departure_times.get_departure_time_for_date(start_time)

    def get_trip_start_times(self, time_window: TimeWindow) -> List[datetime]:
        start_times = []
        for slot in self._data:
            start_times += slot.occurrences_in_window(time_window)

        return sorted(start_times)

    @classmethod
    def from_dict(cls, dikt) -> "RouteDepartureInfo":
        return cls([SlotStopDepartureTimes.from_dict(d) for d in dikt])


class Schedule:
    def __init__(self, slots: [Slot]):
        self._schedule = defaultdict(list)
        for slot in slots:
            self._schedule[slot.day_of_week].append(slot.start_time)
        for slot in slots:
            self._schedule[slot.day_of_week].sort()

    def __eq__(self, other):
        return self._schedule == other._schedule

    def __len__(self):
        return len(list(it.chain(*self._schedule.values())))

    def __sub__(self, other) -> Set[Slot]:
        return self.slots - other.slots

    def intersecting_slots(self, other) -> Set[Slot]:
        return self.slots.intersection(other.slots)

    def runs_on(self, weekday: WeekDay) -> bool:
        return weekday in self._schedule

    def start_times_for(self, weekday: WeekDay) -> [MilitaryTime]:
        return self._schedule[weekday]

    def has_slot(self, slot: Slot) -> bool:
        runs_on_slot_weekday = self._schedule[slot.day_of_week]
        return slot.start_time in runs_on_slot_weekday

    @property
    def slots(self):
        slots = [
            Slot(weekday, run)
            for weekday, runs in self._schedule.items()
            for run in runs
        ]
        return set(slots)

    def as_list(self) -> [Slot]:
        return list(self.slots)

    def as_sorted_list(self) -> [Slot]:
        return sorted(self.slots)

    @classmethod
    def from_slots(cls, slots: Dict) -> "Schedule":
        return Schedule([Slot.from_dict(slot) for slot in slots])


@dataclass
class Shift:
    type: str
    time: MilitaryTime

    @classmethod
    def from_dict(cls, dikt):
        return cls(dikt["type"], military_time_from_dict(dikt["time"]))


@dataclass
class BookingOpeningTime:
    days_before_booking: int
    time_of_day: MilitaryTime

    @property
    def tz(self):
        return self.time_of_day.tz

    def exact_time_for(self, dt: datetime) -> datetime:
        tz_dt = dt.astimezone(self.tz)
        tz_dt -= timedelta(days=self.days_before_booking)
        return self.time_of_day.combine(tz_dt.date()).astimezone(pytz.utc)

    @classmethod
    def from_dict(cls, dikt):
        return cls(
            dikt["days_before_booking"], military_time_from_dict(dikt["time_of_day"])
        )


@dataclass
class Holiday:
    name: str
    declared_date: date
    description: Optional[str] = None

    def __contains__(self, dt: datetime) -> bool:
        d = dt.date()
        return d == self.declared_date

    @classmethod
    def from_dict(cls, dikt):
        return cls(
            name=dikt["name"],
            declared_date=date.fromisoformat(dikt["declared_date"]),
            description=dikt["description"],
        )


@dataclass
class Partner:
    id: str
    name: str
    email_domains: List[str]

    @classmethod
    def from_dict(cls, dikt):
        return cls(
            id=dikt["id"], name=dikt["name"], email_domains=dikt["email_domains"]
        )


@dataclass
class PartnerSite:
    id: str
    name: str
    location: Location
    shifts: List[Shift]
    partner: Partner
    booking_opening_time: BookingOpeningTime
    holidays: List[Holiday]

    @property
    def partner_id(self):
        return self.partner.id

    def get_booking_opening_time_for(self, dt: datetime) -> datetime:
        return self.booking_opening_time.exact_time_for(dt)

    def falls_on_holiday(self, dt: datetime) -> bool:
        return any(dt in h for h in self.holidays)

    @classmethod
    def from_dict(cls, dikt):
        return cls(
            id=dikt["id"],
            name=dikt["name"],
            location=location_from_dict(dikt["location"]),
            shifts=[Shift.from_dict(s) for s in dikt["shifts"]],
            booking_opening_time=BookingOpeningTime.from_dict(
                dikt["booking_opening_time"]
            ),
            holidays=[Holiday.from_dict(h) for h in dikt["holidays"]],
            partner=Partner.from_dict(dikt["partner"]),
        )


@dataclass
class Path:
    locations: List[Location]

    @classmethod
    def from_dict(cls, lizt) -> "Path":
        return cls(locations=[location_from_dict(loc) for loc in lizt])


@dataclass
class B2BRoute:
    def __init__(
        self,
        id: str,
        name: str,
        number: str,
        partner_site: PartnerSite,
        way_points: List[WayPoint],
        path: Path,
        departure_info: RouteDepartureInfo,
        schedule: Schedule,
    ):
        self.id = id
        self.partner_site = partner_site
        self.way_points = way_points
        self.path = path
        self._departure_info = departure_info
        self.name = name
        self.number = number
        self.schedule = schedule

    @property
    def tz(self) -> Optional[pytz.timezone]:
        return self._departure_info.tz

    @property
    def booking_opening_time(self):
        return self.partner_site.booking_opening_time

    @property
    def partner_id(self):
        return self.partner_site.partner_id

    @property
    def partner_site_id(self):
        return self.partner_site.id

    @property
    def way_points_stops(self):
        return [wp for wp in self.way_points if wp.is_stop()]

    @property
    def slots(self) -> [Slot]:
        return self.schedule.slots

    def falls_on_holiday(self, dt: datetime) -> bool:
        tz_dt = dt.astimezone(self.tz)
        return self.partner_site.falls_on_holiday(tz_dt)

    def start_times(self, time_window: TimeWindow) -> List[datetime]:
        start_times = self._departure_info.occurences_in_window(time_window)
        return [st for st in start_times if not self.falls_on_holiday(st)]

    def get_departure_times_for(self, start_time) -> List[ConcreteStopDepartureTime]:
        return self._departure_info.get_departure_time_for(start_time)

    def get_booking_opening_time_for(self, dt: datetime) -> datetime:
        return self.booking_opening_time.exact_time_for(dt)

    def next_operational_day(self, from_time: datetime) -> Optional[date]:
        if not self.has_slots():
            return None
        from_time = from_time.astimezone(self.tz)
        return self._departure_info.next_operational_day_after(from_time.date())

    def has_slot(self, slot: Slot) -> bool:
        return self.schedule.has_slot(slot)

    @classmethod
    def from_dict(
        cls, route_dikt, route_path_dikt=None, route_departure_dikt=None
    ) -> "B2BRoute":
        route_path_dikt = route_path_dikt or []
        route_departure_dikt = route_departure_dikt or {}

        return cls(
            id=route_dikt["id"],
            name=route_dikt["name"],
            number=route_dikt["route_number"],
            partner_site=PartnerSite.from_dict(route_dikt["partner_site"]),
            way_points=[WayPoint.from_dict(wp) for wp in route_dikt["way_points"]],
            path=Path.from_dict(route_path_dikt),
            departure_info=RouteDepartureInfo.from_dict(route_departure_dikt),
            schedule=Schedule.from_slots(slots=route_dikt["slots"]),
        )

    def has_slots(self) -> bool:
        return bool(self._departure_info.slots)

    def next_operational_day_window(self, dt: datetime = None) -> Optional[TimeWindow]:
        if not dt:
            utc_now = pytz.utc.localize(datetime.utcnow())
            dt = utc_now.astimezone(self.tz)

        next_op_date = self.next_operational_day(dt)

        if not next_op_date:
            return None

        next_op_date_min_time = self.tz.localize(
            datetime.combine(next_op_date, time=datetime.min.time())
        )
        next_op_date_max_time = self.tz.localize(
            datetime.combine(next_op_date, time=datetime.max.time())
        )

        return TimeWindow(next_op_date_min_time, next_op_date_max_time)
