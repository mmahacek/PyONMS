# portal.__init__.py

from typing import List, Optional

import requests
from tqdm import tqdm

from pyonms.models.exceptions import DuplicateEntityError

from pyonms.portal.models import (
    PortalAppliance,
    PortalApplianceStatus,
    PortalApplianceProfile,
    PortalInstance,
    PortalSubscription,
    PortalConnectivityProfile,
    PortalFeatureProfile,
    PortalLocation,
    PortalInstanceCreate,
    PortalConnectivityProfileCreate,
    PortalLocationCreate,
    PortalMinion,
)


class Portal:
    def __init__(self, secret: str):
        self.hostname = "https://portal.opennms.com/api/v1/external/"
        self.base_v1 = self.hostname
        self.secret = secret
        self.headers = {"Accept": "application/json", "X-API-Key": secret}

    def _get_batch(
        self,
        url: str,
        endpoint: str,
        limit: int = 0,
        batch_size: int = 100,
        params: dict = {},
    ) -> List[dict]:
        with tqdm(total=limit, unit="record") as pbar:
            result = []
            params["offset"] = 0
            if limit > batch_size:
                params["limit"] = batch_size
            else:
                params["limit"] = limit
            records = self._get(uri=url, params=params, endpoint=endpoint)
            if records.get(endpoint, [None]) == [None]:
                return [None]
            if limit == 0 or records["totalCount"] < limit:
                target_count = records["totalCount"]
                pbar.total = target_count
            else:
                target_count = limit
            while params["offset"] < target_count:
                for record in records[endpoint]:
                    result.append(record)
                    params["offset"] += 1
                    pbar.update(1)
                    if params["offset"] >= target_count:
                        return result
                records = self._get(uri=url, params=params, endpoint=endpoint)
            return result

    def _get(self, uri: str, headers: dict = {}, params: dict = {}) -> dict:
        if not headers:
            headers = self.headers
        response = requests.get(uri, headers=headers, params=params)
        if response.status_code == 200:
            if "was not found" not in response.text:
                return response.json()
        return {}

    def _post(
        self,
        uri: str,
        headers: dict = {},
        json: dict = None,
        params: dict = {},
    ) -> dict:
        if not headers:
            headers = self.headers
        if json:
            response = requests.post(uri, headers=headers, json=json, params=params)
        else:
            response = requests.post(uri, headers=headers)
        if response.status_code in [409]:
            raise DuplicateEntityError(name=json["name"], model="PortalInstance")
        return response.text

    def _put(
        self, uri: str, json: dict, headers: dict = {}, params: dict = {}
    ) -> requests.Response:
        if not headers:
            headers = self.headers
        return requests.put(uri, headers=headers, json=json, params=params)

    def get_appliance(self, id: str) -> PortalAppliance:
        data = self._get(uri=f"{self.base_v1}appliance/{id}")
        if data:
            return PortalAppliance(**data)
        else:
            return None

    def update_appliance(self, appliance: PortalAppliance) -> PortalAppliance:
        response = self._put(
            uri=f"{self.base_v1}appliance/{appliance.id}", json=appliance.to_dict()
        )
        if response.status_code in [204]:
            new_instance = self.get_appliance(id=appliance.id)
            return new_instance

    def get_all_appliances(self) -> List[Optional[PortalAppliance]]:
        appliances = []
        data = self._get(uri=f"{self.base_v1}appliance")
        for appliance in data["pagedRecords"]:
            appliances.append(PortalAppliance(**appliance))
        return appliances

    def get_appliance_status(self, appliance: PortalAppliance) -> PortalApplianceStatus:
        data = self._get(uri=f"{self.base_v1}appliance/{appliance.id}/status")
        return PortalApplianceStatus(**data)

    def get_appliance_profile(self, id: str) -> PortalApplianceProfile:
        data = self._get(uri=f"{self.base_v1}appliance-profile/{id}")
        if data:
            return PortalApplianceProfile(**data)
        else:
            return None

    def get_instance(self, id: str) -> PortalInstance:
        data = self._get(uri=f"{self.base_v1}instance/{id}")
        if data:
            return PortalInstance(**data)
        else:
            return None

    def create_instance(self, instance: PortalInstanceCreate) -> PortalInstance:
        instance_id = self._post(uri=f"{self.base_v1}instance", json=instance.to_dict())
        new_instance = self.get_instance(id=instance_id)
        return new_instance

    def get_subscription(self, id: str) -> PortalSubscription:
        data = self._get(uri=f"{self.base_v1}subscription/{id}")
        if data:
            return PortalSubscription(**data)
        else:
            return None

    def get_connectivity_profile(self, id: str) -> PortalConnectivityProfile:
        data = self._get(uri=f"{self.base_v1}connectivity-profile/{id}")
        if data:
            return PortalConnectivityProfile(**data)
        else:
            return None

    def create_connectivity_profile(
        self, connectivity_profile: PortalConnectivityProfileCreate
    ) -> PortalConnectivityProfile:
        instance_id = self._post(
            uri=f"{self.base_v1}connectivity-profile",
            json=connectivity_profile.to_dict(),
        )
        new_instance = self.get_connectivity_profile(id=instance_id)
        return new_instance

    def get_feature_profile(self, id: str) -> PortalFeatureProfile:
        data = self._get(uri=f"{self.base_v1}feature-profile/{id}")
        if data:
            return PortalFeatureProfile(**data)
        else:
            return None

    def get_location(self, id: str) -> PortalLocation:
        data = self._get(uri=f"{self.base_v1}location/{id}")
        if data:
            location = PortalLocation(**data)
            if isinstance(location.onmsInstanceId, str):
                location.onmsInstanceId = self.get_instance(location.onmsInstanceId)
            if isinstance(location.minionFeatureProfileId, str):
                location.minionFeatureProfileId = self.get_feature_profile(
                    location.minionFeatureProfileId
                )
            if isinstance(location.connectivityProfileId, str):
                location.connectivityProfileId = self.get_connectivity_profile(
                    location.connectivityProfileId
                )
            return location
        else:
            return None

    def create_location(self, location: PortalLocationCreate) -> PortalLocation:
        instance_id = self._post(uri=f"{self.base_v1}location", json=location.to_dict())
        new_instance = self.get_location(id=instance_id)
        return new_instance
