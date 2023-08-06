""" Provides the user with access to the Access Point device. """

import struct
from collections import namedtuple
from enum import IntEnum

import conductor

"""
{'self': {
'href': 'https://networkasset-conductor.link-labs.com/networkAsset/module/$301$0-0-0-03000a37a'},
'nodeAddress': '$301$0-0-0-03000a37a',
'initialDetectionTime': '2019-06-13T14:56:10.376',
'registrationTime': '2019-07-22T20:23:10.551',
'registrationToken': '5578ab6f7997519df80b',
'assetInfo': {
    'accessors':{'owners': [{'href': 'accountId/6', 'desc': ''}]},
    'metadata': {
        'tags': [],
        'props': {
            'assertCount': '250',
            'assertFileName': '000000000000000000000000',
            'assertLineNumber': '0',
            'assertOccured': 'false',
            'averageRssi': '-89.16',
            'batteryPercentage': '100',
            'dbBlacklistLength': '0',
            'dbNodeCount': '128',
            'deviceType': 'SymBLE SLAP Transport',
            'downlinkMode': '1',
            'downlinkMode_quanta': '0',
            'downlinkMulticastCount': '0',
            'downlinkUnicastCount': '0',
            'firmware_version': '1.5.0',
            'lastEventTime': '2019-07-22T16:29:32.496',
            'lastModified': '2019-07-22T20:55:16.557',
            'lastMsgType': 'f0',
            'lastResetCause': '00000000',
            'msgCounter': '1554',
            'msgType': '240',
            'networkLoading': '16',
            'registeredByGateway': '$101$0-0-0-db9504a40',
            'resetCount': '434',
            'rpCount': '0',
            'rssiCollectTime': '2019-07-24T04:14:42.888Z',
            'symMsgPayloadLength': '86',
            'symbleAPFirmwareVersion': '01010002',
            'symbleVersion': '00',
            'systemTimestamp_epochMilliseconds': '481',
            'systemTimestamp_epochSeconds': '1563812973',
            'taskBHConnectionErrorCount': '0',
            'taskBHTaskErrorCount': '0',
            'taskBHTimeoutErrorCount': '0',
            'taskBHTxErrorCount': '0',
            'taskBLEConnectionCount': '1589',
            'taskBLEDisconnectionCount': '1589',
            'taskBLEErrorCount': '0',
            'taskCacheErrorCount': '0',
            'taskErrorCount': '1',
            'temperature': '27080',
            'timestamp': '1.563812972496E12',
            'timestamp_milliseconds': '496',
            'timestamp_seconds': '1563812972',
            'uplinkQueueFillLevel': '1358954496',
            'uplinkQueueMsgCount': '17',
            'uptime': '3605'}},
        'enabled': True}}
"""

DL_AP_CONFIG_HEADER_STRUCT = '>H'
DLAPConfigData = namedtuple('DLAPConfigData', ['cmd',
                                               'data'])

DL_AP_CONFIG_QUERY_STRUCT = '>L'
DLAPConfigQuery = namedtuple('DLAPConfigQuery', ['uuid'])

DL_AP_CONFIG_MODE_STRUCT = '>L4s10s16s'
DLAPConfigMode = namedtuple('DLAPConfigMode', ['timeout',
                                               'net_token',
                                               'app_token',
                                               'crypto_key'])

CONTROL_HEADER_STRUCT = '>H'
ControlDownlink = namedtuple('ControlDownlink', ['command', 'data'])

CONTROL_TYPES = {
    'SET_NET_TOKEN':        0x0001,
    'SET_AP_TYPE':          0x0002,
    'SET_LOCATION_GROUP':   0x0003,
    'SET_LOCATION_WEIGHT':  0x0004,
    'SET_RSSI_ADJ':         0x0005,
    'SET_ADV_RATE':         0x0006,
    'SET_ADV_REFRESH':      0x0007,
    'SET_TIME_SYNC_RATE':   0x0008,
    'SET_CONN_TIMEOUT':     0x0009,
    'SET_STATUS_RATE':      0x000A,
    'SET_MAILBOX_RATE':     0x000B,
    'SET_QUEUE_SEND_RATE':  0x000C,
    'SET_QUEUE_THRESH':     0x000D,
    'SET_LED_FUNCTION':     0x000E,
    'SET_BATT_SAMPLE_RATE': 0x000F,
    'SET_BATT_ALERT_LEVEL': 0x0010,
    'SET_RP_CONN_INTERVAL': 0x0011,
    'SET_SYNC_DC':          0x0012,
    'SET_SCHEDULE':         0x0020,
    'SET_DST':              0x0021,
    'SET_DUTY_CYCLE':       0x0022,
    'SET_DL_BAND':          0x00A0,
    'SET_ENABLE_BLE':       0x0100,
    'GET_BLACKLIST':        0x0101,
    'CLEAR_BLACKLIST':      0x0102,
    'SAMPLE_BATT':          0x0103,
    'GET_BATTERY_LEVEL':    0x0104,
    'GET_TEMP':             0x0105,
    'GET_STATUS':           0x0106,
    'SET_ENABLE_LOCATION':  0x0107,
    'SET_ACK_MODE':         0x0108,
    'SET_TX_POWER':         0x0109,
    'CONFIG_BLE_FRONT_END': 0x010A,
    'ENABLE_DEBUG':         0x04FF,
    'TRIGGER_ASSERT':       0x0500,
}

SET_DL_BAND_BUFF_LEN = 14
BLE_FE_CONFIG_ENABLE_FLAG = 0x01
BLE_FE_CONFIG_ANTENNA_FLAG = 0x02
SYMBLE_MTU = 200
CONTROL_HEADER_LEN = 2
CONTROL_MSG_DATA_INDEX = 2


class CommandBase(IntEnum):
    """ """
    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class AckMode(CommandBase):
    """ """
    DISABLED = 0x00
    TAG = 0x01
    ALL = 0xFF


class AntennaPort(CommandBase):
    """ """
    ANT_A = 0
    ANT_B = 1



class AccessPoint(conductor.Module):
    """ Represents an Access Point and it's functionality. """


    def __init__(self, module):
        super().__init__(module.session, module.subject_id, module._data)


    def _build_control_msg(self, command, data=None):
        """
        Sends the control message
        :param command: the control command being issued
        :param data: the control command data (if any)
        :return: buffer with the control message being sent
        """
        payload = self._build_control_payload(command, data)
        payload_len = CONTROL_HEADER_LEN
        if data:
            payload_len += len(data)

        msg = SymBLEDownlink(DOWNLINK_TYPES['DL_AP_CONFIG'], payload_len, payload)

        # Pack the data into a buffer
        buff = bytearray(b'\x00' * (DOWNLINK_HEADER_LEN + payload_len))
        struct.pack_into(DL_HEADER_STRUCT, buff, 0, msg.type, msg.len)
        struct.pack_into(CONTROL_HEADER_STRUCT, buff, DOWNLINK_MSG_DATA_INDEX,
                         msg.data.command)
        if msg.data.data:
            data_struct = '{}s'.format(len(msg.data.data))
            struct.pack_into(data_struct, buff,
                             (DOWNLINK_MSG_DATA_INDEX + CONTROL_MSG_DATA_INDEX),
                             msg.data.data)
        return buff


    def _build_control_payload(self, command, data=None):
        """
        Sends the control message namedtuple
        :param command: the control command being issued
        :param data: the control command data (if any)
        :return: ControlDownlink namedtuple
        """
        payload = ControlDownlink(command, data)
        return payload


    def set_net_token(self, token, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_NET_TOKEN message
        :param token: network token (uint32_t)
        :return: buffer with the packed data payload
        :note: THIS CANNOT BE SENT VIA BACKHAUL METHOD (SYM)
        """
        data = token.to_bytes(4, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_NET_TOKEN'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_dl_band(self, edge_lower, edge_upper, edge_guard, step_size, step_offset,
            gateway_addr=None, acked=True, time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_DL_BAND message
        :param edge_lower: band edge lower frequency
        :param edge_upper: band edge upper frequency
        :param edge_guard: band edge guard
        :param step_size: channel step size
        :param step_offset: channel step offset
        :return:
        """
        buff = bytearray(b'\x00' * SET_DL_BAND_BUFF_LEN)
        struct.pack_into('>L', buff, 0, edge_lower)
        struct.pack_into('>L', buff, 4, edge_upper)
        struct.pack_into('>L', buff, 8, edge_guard)
        struct.pack_into('>B', buff, 12, step_size)
        struct.pack_into('>B', buff, 13, step_offset)
        msg = self._build_control_msg(CONTROL_TYPES['SET_DL_BAND'], buff)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_ap_type(self, type, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_AP_TYPE message
        :param type: AP type (uint8_t)
        :return: buffer with the packed data payload
        """
        data = type.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_AP_TYPE'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_location_group(self, group, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_LOCATION_GROUP message
        :param group: location group (uint8_t)
        :return: buffer with the packed data payload
        """
        data = group.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_LOCATION_GROUP'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_location_weight(self, weight, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_LOCATION_WEIGHT message
        :param weight: location weight (uint8_t)
        :return: buffer with the packed data payload
        """
        data = weight.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_LOCATION_WEIGHT'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_rssi_adj(self, offset, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_TX_PWR_ADJ message
        :param offset: TX power adjustment offset (int8_t)
        :return: buffer with the packed data payload
        """
        data = offset.to_bytes(1, byteorder='big', signed=True)
        msg = self._build_control_msg(CONTROL_TYPES['SET_RSSI_ADJ'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_adv_rate(self, rate, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_ADV_RATE message
        :param rate: advertising rate (ms) (uint16_t)
        :return: buffer with the packed data payload
        """
        if (rate < 20) or (rate > 10000):
            raise ValueError('Advertising rate must be in the range 20-10000ms!')
        data = rate.to_bytes(2, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_ADV_RATE'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_adv_refresh(self, interval, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_ADV_REFRESH message
        :param interval: advertising refresh interval (ms) (uint16_t)
        :return: buffer with the packed data payload
        """
        if (interval < 200) or (interval > 10000):
            raise ValueError('Advertising refresh interval must be in the range 200-10000ms!')
        data = interval.to_bytes(2, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_ADV_REFRESH'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_time_sync_rate(self, rate, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_TIME_SYNC_RATE message
        :param rate: time sync rate (s) (uint32_t)
        :return: buffer with the packed data payload
        """
        if (rate < 5) or (rate > 86400):
            raise ValueError('Time sync rate must be in the range 5-86400s!')
        data = rate.to_bytes(4, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_TIME_SYNC_RATE'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_conn_timeout(self, interval, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_CONN_TIMEOUT message
        :param interval: connection timeout interval (ms) (uint32_t)
        :return: buffer with the packed data payload
        """
        if (interval < 500) or (interval > 300000):
            raise ValueError('Connection timeout interval must be in the range 500-300000ms!')
        data = interval.to_bytes(4, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_CONN_TIMEOUT'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_status_rate(self, rate, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_STATUS_RATE message
        :param rate: status message rate (s) (uint32_t)
        :return: buffer with the packed data payload
        """
        if (rate < 60) or (rate > 86400):
            raise ValueError('Status message interval must be in the range 60-86400s!')
        data = rate.to_bytes(4, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_STATUS_RATE'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_mailbox_rate(self, rate, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_MAILBOX_RATE message
        :param rate: mailbox check rate (s) (uint32_t)
        :return: buffer with the packed data payload
        """
        if (rate < 60) or (rate > 86400):
            raise ValueError('Mailbox check rate must be in the range 60-86400s!')
        data = rate.to_bytes(4, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_MAILBOX_RATE'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def queue_send_rate(self, rate, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_QUEUE_SEND_RATE message
        :param rate: queue send rate (ms) (uint32_t)
        :return: buffer with the packed data payload
        """
        if (rate < 5000) or (rate > 1800000):
            raise ValueError('Queue send rate must be in the range 10000-1800000s!')
        data = rate.to_bytes(4, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_QUEUE_SEND_RATE'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def queue_threshold(self, thresh, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_QUEUE_THRESH message
        :param thresh: queue send threshold (uint8_t)
        :return: buffer with the packed data payload
        """
        if thresh > 100:
            raise ValueError('Queue threshold cannot be > 100%!')
        data = thresh.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_QUEUE_THRESH'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def led_function(self, led, function, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_LED_FUNCTION message
        :param led: the LED to set (uint8_t)
        :param function: the function to set (uint8_t)
        :return: buffer with the packed data payload
        """
        raise NotImplementedError('SET_LED_FUNCTION not yet implemented!')
        data = led.to_bytes(1, byteorder='big') + function.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_LED_FUNCTION'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def batt_sample_rate(self, rate, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_BATT_SAMPLE_RATE message
        :param rate: battery sample rate (s) (uint32_t)
        :return: buffer with the packed data payload
        """
        raise NotImplementedError('SET_BATT_SAMPLE_RATE not yet implemented!')
        if (rate < 60) or (rate > 172800):
            raise ValueError('Battery sample rate must be in the range 60-172800s!')
        data = rate.to_bytes(4, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_BATT_SAMPLE_RATE'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def battery_alert_level(self, level, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_BATT_ALERT_LEVEL message
        :param level: battery alert level (uint8_t)
        :return: buffer with the packed data payload
        """
        raise NotImplementedError('SET_BATT_ALERT_LEVEL not yet implemented!')
        if level > 100:
            raise ValueError('Battery alert level cannot be > 100%!')
        data = level.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_BATT_ALERT_LEVEL'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def rp_conn_interval(self, interval, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_RP_CONN_INTERVAL message
        :param interval: RP connection interval (ms) (uint32_t)
        :return: buffer with the packed data payload
        """
        raise NotImplementedError('SET_RP_CONN_INTERVAL not yet implemented!')
        if (interval < 3000) or (interval > 86400):
            raise ValueError('RP Connection interval must be in the range 3000-86400ms!')
        data = interval.to_bytes(4, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_RP_CONN_INTERVAL'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def sync_duty_cycle(self, duty_cycle, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_SYNC_DC message
        :param duty_cycle: sync advertisement duty cycle (uint8_t)
        :return: buffer with the packed data payload
        """
        if duty_cycle > 3:
            raise ValueError('Sync duty cycle cannot be > 3 (10/100)!')
        data = duty_cycle.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_SYNC_DC'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_enable_ble(self, enable, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_ENABLE_BLE message
        :param enable: BLE enable (uint8_t)
        :return: buffer with the packed data payload
        """
        data = enable.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_ENABLE_BLE'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def get_blacklist(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
            port=0, priority=10):
        """
        Sends a GET_BLACKLIST message
        :return: buffer with the packed data payload
        """
        raise NotImplementedError('GET_BLACKLIST not yet implemented!')
        msg = self._build_control_msg(CONTROL_TYPES['GET_BLACKLIST'])
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def clear_blacklist(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
            port=0, priority=10):
        """
        Sends a CLEAR_BLACKLIST message
        :return: buffer with the packed data payload
        """
        raise NotImplementedError('CLEAR_BLACKLIST not yet implemented!')
        msg = self._build_control_msg(CONTROL_TYPES['CLEAR_BLACKLIST'])
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def sample_batt(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
            port=0, priority=10):
        """
        Sends a SAMPLE_BATT message
        :return: buffer with the packed data payload
        """
        msg = self._build_control_msg(CONTROL_TYPES['SAMPLE_BATT'])
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def get_battery_level(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
            port=0, priority=10):
        """
        Sends a GET_BATTERY_LEVEL message
        :return: buffer with the packed data payload
        """
        raise NotImplementedError('GET_BATTERY_LEVEL not yet implemented!')
        msg = self._build_control_msg(CONTROL_TYPES['GET_BATTERY_LEVEL'])
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def get_temp(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
            port=0, priority=10):
        """
        Sends a GET_TEMP message
        :return: buffer with the packed data payload
        """
        raise NotImplementedError('GET_TEMP not yet implemented!')
        msg = self._build_control_msg(CONTROL_TYPES['GET_TEMP'])
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def get_status(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
            port=0, priority=10):
        """
        Sends a GET_STATUS message
        :return: buffer with the packed data payload
        """
        msg = self._build_control_msg(CONTROL_TYPES['GET_STATUS'])
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def enable_location(self, enable, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_ENABLE_LOCATION message
        :param enable: AP location flag enable
        :return: buffer with the packed data payload
        """
        if type(enable) != bool:
            raise TypeError('enable must be True or False')
        data = enable.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_ENABLE_LOCATION'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_ack_mode(self, mode, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_ACK_MODE message
        :param mode: ACK mode
        :return: buffer with the packed data payload
        """
        if not AckMode.has_value(mode):
            raise ValueError('{} is not a valid ACK mode'.format(mode))
        ack_mode = AckMode(mode)
        data = ack_mode.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['SET_ACK_MODE'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def set_tx_power(self, power, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a SET_TX_POWER message
        :param power: TX power level
        :return: buffer with the packed data payload
        """
        # TODO: Add parameter checking
        data = power.to_bytes(1, byteorder='big', signed=True)
        msg = self._build_control_msg(CONTROL_TYPES['SET_TX_POWER'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def config_ble_front_end(self, enable, antenna, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a CONFIG_BLE_FRONT_END message
        :param enable: True if front-end is to be enabled
        :param antenna: Antenna port setting
        :return: buffer with the packed data payload
        """
        val = BLE_FE_CONFIG_ENABLE_FLAG if enable else 0
        val += BLE_FE_CONFIG_ANTENNA_FLAG if antenna == AntennaPort.ANT_B else 0
        data = val.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['CONFIG_BLE_FRONT_END'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def enable_debug(self, enable, gateway_addr=None, acked=True,
                     time_to_live_s=60.0, port=0, priority=10):
        """
        Sends a ENABLE_DEBUG message
        :param enable: debug enable (uint8_t)
        :return: buffer with the packed data payload
        """
        raise NotImplementedError('ENABLE_DEBUG not yet implemented!')
        data = enable.to_bytes(1, byteorder='big')
        msg = self._build_control_msg(CONTROL_TYPES['ENABLE_DEBUG'], data)
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


    def trigger_assert(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
            port=0, priority=10):
        """
        Triggers an assert in the AP
        :return: buffer with the packed data payload
        """
        msg = self._build_control_msg(CONTROL_TYPES['TRIGGER_ASSERT'])
        return self.send_message(msg, gateway_addr, acked, time_to_live_s, port, priority)


