"""WLANs as part of a UniFi network."""

from .api import APIItems

URL = 's/{site}/rest/wlanconf'  #List WLAN configuration


class Wlans(APIItems):
    """Represents WLAN configurations."""

    def __init__(self, raw, request):
        super().__init__(raw, request, URL, Wlan)

    async def async_enable(self, id):
        """Block client from controller."""
        data = {
            '_id': id,
            'enabled': True
        }
        await self._request('post', URL, json=data)

    async def async_disable(self, id):
        """Unblock client from controller."""
        data = {
            '_id': id,
            'enabled': False
        }
        await self._request('post', URL, json=data)


class Wlan:
    """Represents a WLAN configuration."""

    def __init__(self, raw, request):
        self.raw = raw
        self._request = request

    @property
    def id(self):
        return self.raw['_id']

    @property
    def bc_filter_enabled(self):
        return self.raw['bc_filter_enabled']

    @property
    def bc_filter_list(self):
        return self.raw['bc_filter_list']

    @property
    def dtim_mode(self):
        return self.raw['dtim_mode']

    @property
    def dtim_na(self):
        return self.raw['dtim_na']

    @property
    def dtim_ng(self):
        return self.raw['dtim_ng']

    @property
    def enabled(self):
        return self.raw['enabled']

    @property
    def group_rekey(self):
        return self.raw['group_rekey']

    @property
    def is_guest(self):
        return self.raw['is_guest']

    @property
    def mac_filter_enabled(self):
        return self.raw['mac_filter_enabled']

    @property
    def mac_filter_list(self):
        return self.raw['mac_filter_list']

    @property
    def mac_filter_policy(self):
        return self.raw['mac_filter_policy']

    @property
    def minrate_na_advertising_rates(self):
        return self.raw['minrate_na_advertising_rates']

    @property
    def minrate_na_beacon_rate_kbps(self):
        return self.raw['minrate_na_beacon_rate_kbps']

    @property
    def minrate_na_data_rate_kbps(self):
        return self.raw['minrate_na_data_rate_kbps']

    @property
    def minrate_na_enabled(self):
        return self.raw['minrate_na_enabled']

    @property
    def minrate_na_mgmt_rate_kbps(self):
        return self.raw['minrate_na_mgmt_rate_kbps']

    @property
    def minrate_ng_advertising_rates(self):
        return self.raw['minrate_ng_advertising_rates']

    @property
    def minrate_ng_beacon_rate_kbps(self):
        return self.raw['minrate_ng_beacon_rate_kbps']

    @property
    def minrate_ng_cck_rates_kbps(self):
        return self.raw['minrate_ng_cck_rates_kbps']

    @property
    def minrate_ng_data_rate_kbps(self):
        return self.raw['minrate_ng_data_rate_kbps']

    @property
    def minrate_ng_enabled(self):
        return self.raw['minrate_ng_enabled']

    @property
    def minrate_ng_mgmt_rate_kbps(self):
        return self.raw['minrate_ng_mgmt_rate_kbps']

    @property
    def name(self):
        return self.raw['name']

    @property
    def schedule(self):
        return self.raw['schedule']

    @property
    def security(self):
        return self.raw['security']

    @property
    def site_id(self):
        return self.raw['site_id']

    @property
    def usergroup_id(self):
        return self.raw['usergroup_id']

    @property
    def wep_idx(self):
        return self.raw['wep_idx']

    @property
    def wlangroup_id(self):
        return self.raw['wlangroup_id']

    @property
    def wpa_enc(self):
        return self.raw['wpa_enc']

    @property
    def wpa_mode(self):
        return self.raw['wpa_mode']

    @property
    def x_iapp_key(self):
        return self.raw['x_iapp_key']

    @property
    def x_passphrase(self):
        return self.raw['x_passphrase']
