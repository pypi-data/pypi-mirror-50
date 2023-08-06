""" Represents a Location Beacon. """
from collections import namedtuple
from enum import IntEnum

from conductor.airfinder.tag import Tag, compile_msg


LocationBeaconDownlink = namedtuple('LocationBeaconDownlink', ['msgType', 'msgSpec', 'data'])
BASE_MSG_STRUCT = "<BB"

LocationBeaconConfiguration = namedtuple('LocationBeaconConfiguration', ['mask',
    'advertisementEnable', 'schedule', 'heartbeatInterval', 'rssiAdjustment',
    'locationWeight', 'locationGroup', 'transmitPower'])
CFG_STRUCT = "<BB"


class DownlinkMessageType(IntEnum):
    """ Downlink Message Types for Location Beacons. """
    DOWNLINK_CONFIGURATION = 0x01
    RESET = 0x06

class Schedule():
    """ """
    DAY_S = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    class Day(IntEnum):
        SUNDAY = 0
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6

    def __init__(self):
        """ """
        self.schedule = [[0x01] * 24] * 7

    def set_hour_per_day(self, hour, val):
        """ Set a certain hour to be (in)active every day.
        :param hour - the hour that should be affected.
        :param val - True/False, enabled or disabled.
        """
        for day in self.schedule:
            day[hour] = val

    def set_day(self, day, val):
        """ Set all the hours in a day to a certain value.
        :param day - the day to modify.
        :param val = True/False, enabled or disabled."""
        for hour_i in range(len(self.schedule[day])):
            self.schedule[day][hour_i] = val

    def print_day(self, day):
        """ """
        for hour_i in range(len(self.schedule[day])):
            print("\tHour {:02}: Advertising = {}".format(hour_i, bool(self.schedule[day][hour_i])))

    def print(self):
        """ """
        for day_i in range(len(self.schedule)):
            print("{}:".format(self.DAY_S[day_i]))
            for hour_i in range(len(self.schedule[day_i])):
                print("\tHour {:02}: Advertising = {}".format(hour_i, bool(self.schedule[day_i][hour_i])))
            print()

    def consolodate(self):
        val = ""
        for day in self.schedule:
            for hour in day:
                val = val + str(hour)
        return int(val, 2)


class Location(Tag):
    """ Represents an Airfinder Location. """
    subject_name = 'Location'
    device_type = "SymBLE Smart RP Application"

    def __init__(self, session, subject_id, _data=None):
        super().__init__(session, subject_id, _data)

    def reset(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
            port=0, priority=10):
        """ """
        RESET_KEY = [0xd5, 0x83, 0x7e, 0xd6]
        msg = LocationBeaconDownlink(DownlinkMessageType.RESET, self.msg_spec, RESET_KEY)
        msg = compile_msg(CFG_STRUCT, d.data, msg)

        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)

    @property
    def node_address(self):
        return self._data.get('nodeAddress')

    @property
    def mac_address(self):
        return self.metadata.get('macAddress')

    @property
    def initial_detection_time(self):
        return conductor.parse_time(self._data.get('initialDetectionTime'))

    @property
    def registration_detection_time(self):
        return conductor.parse_time(self._data.get('registrationTime'))

    @property
    def last_provisioned_time(self):
        return conductor.parse_time(self.metadata.get('lastProvisionedTime'))

    @property
    def initial_provisioned_time(self):
        return conductor.parse_time(self.metadata.get('initialProvisionedTime'))

    @property
    def name(self):
        return self._data.get('nodeName')

    @property
    def site(self):
        return Site(self.session, self.metadata.get('siteId'))

    @property
    def area(self):
        return Area(self.session, self.site, self.metadata.get('areaId'))

    @property
    def zone(self):
        return Zone(self.session, self.area, self.metadata.get('zoneId'))

    @property
    def battery_status(self):
        return bool(self.metadata.get('batteryStatus'))

    @property
    def is_lost(self):
        return self.metadata.get('isLost')



