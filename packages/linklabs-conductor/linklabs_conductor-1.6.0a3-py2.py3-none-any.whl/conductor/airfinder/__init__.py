""" """
from enum import IntEnum

import conductor
from conductor.airfinder.access_point import AccessPoint
from conductor.airfinder.tag import Tag
from conductor.airfinder.supertag import Supertag
from conductor.airfinder.alert_tag import AlertTag
#from conductor.airfinder.site import SiteUser, Site
#from conductor.airfinder.area import Area
#from conductor.airfinder.zone import Zone

NETWORK_ASSET_URL = conductor.NETWORK_ASSET_URL() + '/airfinder/'

SITE_USER_PERMISSIONS = {
    "Admin": False,
    "Status": True,
    "AddTags": True,
    "EditDeleteTags": True,
    "EditDeleteGroupsCategories": False
}


class EventCount(conductor.EventCount):
    event_type = 'airfinderLocation'


class User(conductor.ConductorAccount):
    """
    This class provides methods for interacting with Airfinder through Conductor for any
    particular account.

    This is the starting point for everything else in this module. Initialize with your
    username and password. If the password is omitted the initializer will prompt for one.
    Optionally provide the account name that you're trying to access (if you don't provide
    the account, the constructor will try to figure out which account is linked to your username).
    """
    subject_name = "User"

    def _get_registered_af_asset(self, subject_name, subject_id):
        """ Base function for getting a registered asset from the Network Asset API. """
        return self._get_registered_asset("airfinder/" + subject_name, subject_id)

    def _get_registered_af_assets(self, asset_name):
        """ Base function for getting list of registered assets from the Network Asset API. """
        return self._get_registered_assets("airfinder/" + asset_name)

    def get_sites(self):
        """ Get all the sites this user has access to. """
        return [Site(self.session, x.get('id'), _data=x)
                for x in self._get_registered_af_assets('sites')]

    def get_site(self, site_id):
        """ Get a specific site. """
        x = self._get_registered_af_asset('site', site_id)
        return Site(self.session, x.get('id'), _data=x)

    def get_tags(self):
        """ Gets all the tags in a site. """
        return self._get_registered_af_assets('tags')

    def get_tag(self, mac_id):
        """ Gets a tag in the site. """
        return self._get_registered_af_asset('tag', mac_id)

    def get_locations(self):
        """ Get all the locations in a site. """
        return [Location(self.session, x.get('assetInfo').get('metadata').get('props').get('macAddress'), _data=x) for x in
                self._get_registered_af_assets('locations')]

    def get_location(self, mac_id):
        """ Gets a location, in a site. """
        x = self._get_registered_af_asset('location', mac_id)
        return Location(self.session, mac_id, _data=x)


    def create_site(self, name):
        """" Create a site with the given name. """
        url = ''.join([NETWORK_ASSET_URL, 'sites'])
        data = {
            "configType": "Site",
            "configValue": name,
            "properties": {}
        }
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        x = resp.json()
        return Site(self.session, x.get('id'), _data=x)

    def delete_site(self, site):
        """ Delete a specific site. """
        url = ''.join([NETWORK_ASSET_URL, 'site'])
        param = {'siteId': site}
        resp = self.session.delete(url, params=param)
        resp.raise_for_status()
        return resp.json()

    def create_site_user(self, email, site, site_user_permissions=None):
        """ Create a Site User. """
        if site_user_permissions is None:
            site_user_permissions = SITE_USER_PERMISSIONS

        url = ''.join([NETWORK_ASSET_URL, 'users'])
        data = {
            "sites": [str(site)],
            "email": email,
            "permissions": site_user_permissions
        }
        resp = self.session.post(url, json=data)
        resp.raise_for_status()
        x = resp.json()
        return SiteUser(self.session, x['id'], _data=x)


def mac_to_addr(mac):
    """ Converts a BLE MAC Address into a Conductor Endnode Address. """
    if len(mac) == 26: return mac
    if len(mac) == 17: mac = mac.replace(':', '')
    af_fmt = mac[:3] + '-' + mac[3:]
    return "$501$0-0-00{}".format(af_fmt)


def addr_to_mac(addr):
    """ Converts a BLE MAC Address into a Conductor Endnode Address. """
    mac_addr = "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(
        addr[5] | 0xc0, addr[4], addr[3], addr[2], addr[1], addr[0])
