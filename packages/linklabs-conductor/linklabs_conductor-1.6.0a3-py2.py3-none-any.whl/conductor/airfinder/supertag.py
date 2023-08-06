""" Represents a Supertag and its functionality. """

from enum import IntEnum
from conductor.airfinder.tag import Tag


SYMBLE_SETTINGS = {
    "symbleHeartbeat_reported": 60,
    "locationUpdateRate_reported": 11,
    "scansPerFix_reported": 4,
    "networkLostTimeout_reported": 600,
    "refLostTimeout": 600,
    "networkScanInterval_reported": 180,
    "networkToken": "4f50454e"
}

BACKHAUL_SETTINGS = {
    "noApHeartbeatInterval": 86400,
    "noRpHeartbeatInterval": 86400,
    "noApLocationUpdateRate": 21600,
    "noRpLocationUpdateRate": 21600,
    "maxWifis": 10,
    "maxCellIds": 0,
    "locationUpdateOrder": {
        "gpsLocationOrder": 1,
        "wifiLocationOrder": 2,
        "cellLocationOrder": 3
    }
}

ACCEL_SETTINGS = {
    "Enable": 1,
    "MovementDuration": 3,
    "Threshold": 80,
    "shockThreshold": 160
}

CACHING_SETTINGS = {
    "cachedMessagesEnable": 0,
    "noRpMessagesCached": 0
}

GPS_SETTINGS = {
    "gpsPowerMode": 0,
    "gpsTimeout": 180
}

HELP_MODE_SETTINGS = {
    "helpModeUpdateRate": 60
}

class DownlinkMessageType(IntEnum):
    DOWNLINK_CONFIGURATION = 0x01
    TEST_MODE_EN = 0x02
    HELP_MSG_RXED = 0x03


# TODO: New format...
DL_f = "{msg_type:02x}{msg_spec:02x}{data}".format
DL_CONF_V1_f = "{change_msk:04x}{heartbeat_int:08x}{no_ap_heartbeat_int:08x}" \
               "{no_rp_heartbeat_int:08x}{loc_update_rate:08x}{no_ap_loc_update_rate:08x}" \
               "{no_rp_loc_update_rate:08x}{scan_per_fix:02x}{wifi_ap:02x}{cell_id:02x}" \
               "{loc_update_order:02x}{net_lost_timeout:04x}{ref_lost_timeout:04x}" \
               "{net_scan_int:04x}".format
DL_CONF_V2_f = "{change_msk:08x}{heartbeat_int:08x}{no_ap_heartbeat_int:08x}" \
               "{no_rp_heartbeat_int:08x}{loc_update_rate:08x}{no_ap_loc_update_rate:08x}" \
               "{no_rp_loc_update_rate:08x}{help_mode_update_rate:08x}{scan_per_fix:02x}" \
               "{wifi_ap:02x}{cell_id:02x}{loc_update_order:02x}{accel_en:02x}" \
               "{accel_mvm_dur:04x}{accel_thresh:04x}{shock_thresh:04x}{msg_cache_en:02x}" \
               "{msg_cache_num:02x}{gps_pwr_mode:02x}{gps_timeout:04x}{net_lost_timeout:04x}" \
               "{ref_lost_timeout:04x}{net_scan_int:04x}{net_tok:08x}".format




class Supertag(Tag):
    """ """
    def update_configuration(self, symble_conf=None, accel_conf=None, help_conf=None, backhaul_conf=None,
                             caching_conf=None, gps_conf=None, gateway_addr=None, acked=True, time_to_live_s=60.0,
                             port=0, priority=10):
        """ TODO """
        if not symble_conf:
            symble_conf = SYMBLE_SETTINGS
        if not accel_conf:
            accel_conf = ACCEL_SETTINGS
        if not help_conf:
            help_conf = HELP_MODE_SETTINGS
        if not backhaul_conf:
            backhaul_conf = BACKHAUL_SETTINGS
        if not caching_conf:
            caching_conf = CACHING_SETTINGS
        if not gps_conf:
            gps_conf = GPS_SETTINGS

        #    "locationUpdateOrder"
        #        "gpsLocationOrder": 1,
        #        "wifiLocationOrder": 2,
        #        "cellLocationOrder": 3

        self.send_message(
            self.DL_f(msg_type=self.DownlinkMessageType.DOWNLINK_CONFIGURATION,
                      msg_spec=0x02,  # TODO
                      data=
                      self.DL_CONF_V2_f(
                          change_msk=0,
                          heartbeat_int=symble_conf[''],
                          no_ap_heartbeat_int=backhaul_conf['noApHeartbeatInterval'],
                          no_rp_heartbeat_int=backhaul_conf['noRpHeartbeatInterval'],
                          loc_update_rate=symble_conf[''],
                          no_ap_loc_update_rate=backhaul_conf['noApLocationUpdateRate'],
                          no_rp_loc_update_rate=backhaul_conf['noRpLocationUpdateRate'],
                          help_mode_update_rate=backhaul_conf['helpModeUpdateRate'],
                          scan_per_fix=symble_conf[''],
                          wifi_ap=backhaul_conf['maxWifis'],
                          cell_id=backhaul_conf['maxCellIds'],
                          loc_update_order=backhaul_conf[''],
                          accel_en=accel_conf[''],
                          accel_mvm_dur=accel_conf[''],
                          accel_thresh=accel_conf[''],
                          shock_thresh=accel_conf[''],
                          msg_cache_en=caching_conf['cachedMessagesEnable'],
                          msg_cache_num=caching_conf['noRpMessagesCached'],
                          gps_pwr_mode=gps_conf['gpsPowerMode'],
                          gps_timeout=gps_conf['gpsTimeout'],
                          net_lost_timeout=symble_conf[''],
                          ref_lost_timeout=symble_conf[''],
                          net_scan_int=symble_conf[''],
                          net_tok=symble_conf['networkToken']) if True else \
                          self.DL_CONF_V1_f(
                              change_msk=0,
                              heartbeat_int=0,
                              no_ap_heartbeat_int=0,
                              no_rp_heartbeat_int=0,
                              loc_update_rate=0,
                              no_ap_loc_update_rate=0,
                              no_rp_loc_update_rate=0,
                              scan_per_fix=0,
                              wifi_ap=0,
                              cell_id=0,
                              loc_update_order=0,
                              net_lost_timeout=0,
                              ref_lost_timeout=0,
                              net_scan_int=0)),
            gateway_addr=gateway_addr,
            acked=acked,
            time_to_live_s=time_to_live_s,
            port=port,
            priority=priority)

    def notify_help_mode_rxed(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
                              port=0, priority=10):
        """ TODO """
        self.send_message(
            self.DL_f(
                msg_type=self.DownlinkMessageType.HELP_MSG_RXED,
                msg_spec=0x02,  # TODO
                data=0x4357),
            gateway_addr=gateway_addr,
            acked=acked,
            time_to_live_s=time_to_live_s,
            port=port,
            priority=priority)

    def activate_test_mode(self, gateway_addr=None, acked=True, time_to_live_s=60.0,
                           port=0, priority=10):
        """ TODO """
        self.send_message(
            self.DL_f(
                msg_type=self.DownlinkMessageType.TEST_MODE_EN,
                msg_spec=0x02),
            gateway_addr=gateway_addr,
            acked=acked,
            time_to_live_s=time_to_live_s,
            port=port,
            priority=priority)



