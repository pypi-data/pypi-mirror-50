""" Represents an Alert Tag """

from enum import IntEnum
from collections import namedtuple

from conductor.airfinder.tag import Tag, compile_msg


AlertTagDownlink = namedtuple('AlertTagDownlink', ['msgType', 'msgSpec', 'data'])
BASE_MSG_STRUCT = "<BB"

AlertTagConfiguration = namedtuple('AlertTagConfiguration', ['mask',
    'idleModeHeartbeat', 'alertModeHeartbeat', 'alertModeLocationUpdateRate',
    'networkLostScanCount', 'networkLostScanInterval', 'maxSymBLERetries',
    'buttonHoldLength', 'audibleAlarmEnable'])
CFG_STRUCT = "<BBBHBBBHBBB"


class DownlinkMessageType(IntEnum):
    """ Downlink Message Types for Alert Tags. """
    DOWNLINK_CONFIGURATION = 0x01
    ALT_RXED = 0x06
    ALT_DISABLE = 0x07


class AlertTag(Tag):
    """ TODO """

    def update_configuration(self, configuration, gateway_addr=None, acked=True,
            time_to_live_s=60.0, port=0, priority=10):
        """ TODO """
        d = AlertTagDownlink(DownlinkMessageType.DOWNLINK_CONFIGURATION, 0x01, configuration)
        msg = struct.pack(BASE_MSG_STRUCT, d.msgType, d.msgSpec)
        msg = compile_msg(CFG_STRUCT, d.data, msg)

        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)

    def send_alert_received(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
                            port=0, priority=10):
        """ TODO """
        d = AlertTagDownlink(DownlinkMessageType.ALT_RXED, 0x01)
        msg = struct.pack(BASE_MSG_STRUCT, d.msgType, d.msgSpec)

        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)

    def send_alert_disable(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
                           port=0, priority=10):
        """ TODO """
        d = AlertTagDownlink(DownlinkMessageType.ALT_DISABLE, 0x01)
        msg = struct.pack(BASE_MSG_STRUCT, d.msgType, d.msgSpec)

        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)



