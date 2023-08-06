"""" Represents an Airfinder Site. """

class SiteUser():
    """
    This class is used to manage other Airfinder SiteUsers,
    given the User has Admin-level permissions.
    """
    subject_name = 'SiteUser'

    def __init__(self, session, subject_id, _data=None):
        super().__init__(session, subject_id, _data)

    @property
    def can_add_tags(self):
        """ Can the SiteUser add tags? """
        return bool(self.metadata.get('AddTags'))

    @property
    def is_admin(self):
        """ Is the SiteUser an Admin? """
        return bool(self.metadata.get('Admin'))

    @property
    def can_edit_delete_groups_categories(self):
        """ Can the SiteUser Edit/Delete Groups and Categories? """
        return bool(self.metadata.get('EditDeleteGroupsCategories'))

    @property
    def can_edit_delete_tags(self):
        """ Can the SiteUser Edit/Delete tags? """
        return bool(self.metadata.get('EditDeleteTags'))

    @property
    def email(self):
        """ The SiteUser's email address. """
        return self.metadata.get('email')

    @property
    def user_id(self):
        return self.metadata.get('userId')

    @property
    def status(self):
        return bool(self.metadata.get('Status'))

    @property
    def site(self):
        return Site(self.session, self.metadata.get('siteId'))

    def forgot_password(self):
        """ Sends the site user an email to reset their password. """
        url = ''.join([NETWORK_ASSET_URL, 'users/forgotPassword'])
        params = {'email': self.email}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def resend_email(self):
        """ Resends the site user an email to reset their password. """
        url = ''.join([NETWORK_ASSET_URL, 'users/resend'])
        params = {'email': self.email}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


class Site():
    """ Represents an Airfinder Site. """
    subject_name = 'Site'

    def __init__(self, session, subject_id, _data=None):
        super().__init__(session, subject_id, _data)

    @property
    def owner_account_id(self):
        return self.metadata.get('accountId')

    def _get_registered_asset_by_site(self, subject_name, subject_id):
        """ Gets a registered asset by site-id. """
        url = ''.join([NETWORK_ASSET_URL, '{}/{}'.format(subject_name, subject_id)])
        params = {'siteId': self.subject_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def _get_registered_assets_by_site(self, asset_name):
        """ Gets all the registered assets by site-id. """
        url = ''.join([NETWORK_ASSET_URL, asset_name])
        params = {'siteId': self.subject_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def rename(self, name):
        """ Rename an existing site. """
        # TODO
        url = ''.join([NETWORK_ASSET_URL, 'sites'])
        param = {'siteId': self.subject_id}
        updates = {
            "name": name,
        }
        resp = self.session.put(url, params=param, json=updates)
        resp.raise_for_status()
        _data = resp.json()

    def get_site_users(self):
        """ Gets all the site-users, in the site. """
        return [SiteUser(self.session, x.get('id'), _data=x) for x in
                self._get_registered_assets_by_site('users')]

    def get_site_user(self, site_user_id):
        """ Gets a site-user in a site. """
        x = self._get_registered_asset_by_site('user', site_user_id)
        return SiteUser(self.session, x.get('id'), _data=x)

    def get_areas(self):
        """ Gets all the areas for a site. """
        return [Area(self.session, x.get('id'), self, _data=x) for x in
                self._get_registered_assets_by_site('areas')]

    def create_area(self, name):
        """ Create an area as a part of this Site. """
        url = ''.join([NETWORK_ASSET_URL, asset_name])
        params = {'siteId': self.subject_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def delete_area(self, area_id):
        """ Delete an area. """
        url = ''.join([NETWORK_ASSET_URL, asset_name])
        params = {'siteId': self.subject_id}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_area(self, area_id):
        """ Gets an area in a site. """
        x = self._get_registered_asset_by_site('area', area_id)
        return Area(self.session, x.get('id'), self, _data=x)

    def get_workflows(self):
        """ Gets all the workflows for the Site. """
        return self._get_registered_assets_by_site('workflows')

    def get_workflow(self, workflow_id):
        """" Gets a workflow for the Site. """
        return self._get_registered_asset_by_site('workflow', workflow_id)

    def remove_locations(self, locations):
        """ Remove locations from a Site. """
        # TODO: test
        url = ''.join([NETWORK_ASSET_URL, 'tags'])
        data = {
            "nodeAddresses": [locations],
            "siteId": self.subject_id
        }
        resp = self.session.delete(url, json=data)
        resp.raise_for_status()
        return resp.json()

    def get_tags(self):
        """ Gets all the tags in a site. """
        return self._get_registered_assets_by_site('tags')

    def get_tag(self, mac_id):
        """ Gets a tag in the site. """
        return self._get_registered_asset_by_site('tag', mac_id)

    def add_tag(self, mac_id, field1="", field2="", category=None, description=""):
        """ Adds a tag in the site. """
        url = ''.join([NETWORK_ASSET_URL, 'tags'])
        params = {
            "accountId": self.metadata.get('accountId'),
            "macAddress": mac_id,
            "siteId": self.subject_id,
            "description": description,
            "categoryId": category,
            "groups": [""],
            "field1": field1,
            "field2": field2,
            "properties": "object",
            "homeLocation": "",
            "adjacentLocations": [""],
            "trackTagAge": ""
        }
        resp = self.session.post(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def bulk_add_tags(self, file_name):
        """ Bulk-add tags to an airfinder site. """
        raise NotImplemented

    def remove_tag(self, mac_id):
        """ Remove a tag to an airfinder site. """
        url = ''.join([NETWORK_ASSET_URL, 'tags'])
        params = {
            "nodeAddress": mac_id,
            "accountId": self.metadata.get('accountId'),
            "siteId": self.subject_id
        }
        resp = self.session.post(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def bulk_add_locations(self, file_name):
        """ Bulk-add locations to a site. """
        raise NotImplemented

    def get_groups(self):
        """ Get all the groups in a site. """
        return self._get_registered_assets_by_site('groups')

    def get_group(self, group_id):
        """ Get a group from a site. """
        return self._get_registered_asset_by_site('group', group_id)

    def get_categories(self):
        """ Get all the categories in a site."""
        return self._get_registered_assets_by_site('categories')

    def get_category(self, category_id):
        """ Get a category in a site. """
        return self._get_registered_asset_by_site('category', category_id)

    def get_asset_group(self):
        """ Get the Site as an Asset Group. """
        x = _get_registered_asset_by_site('assetGroup')
        return AssetGroup(self.session, x['id'], _data=x)


