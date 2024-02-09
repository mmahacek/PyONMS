# dao.business_services.py

# cspell:ignore snmpinterfaces, ipinterfaces

"Business Service data access"

import concurrent.futures
from typing import List, Optional

from tqdm import tqdm

import pyonms.models.business_service
from pyonms.dao.base import Endpoint


class BSMAPI(Endpoint):
    "Business Service API endpoint"

    def __init__(self, kwargs):
        super().__init__(**kwargs)
        self.url = self.base_v2 + "business-services"
        self._init_cache()

    def _init_cache(self):
        self.cache = {}
        self.cache_name = {}

    def get_bsm(
        self, id: int
    ) -> Optional[pyonms.models.business_service.BusinessService]:
        """Get BusinessService object by ID number."""
        record = self._get(url=f"{self.url}/{id}")
        if record is not None:
            bsm = self._process_bsm(record)
            self.cache[bsm.id] = bsm
            self.cache_name[bsm.name] = bsm.id
            return bsm
        else:
            return None

    def _get_bsm_ids(
        self,
    ) -> dict:
        response = self._get(url=self.url)
        if response.get("business-services"):
            return response
        else:
            return {"business-services": []}

    def get_bsms(
        self, threads: int = 10
    ) -> List[pyonms.models.business_service.BusinessService]:
        """Get all BusinessService objects."""
        service_list = []
        services = self._get_bsm_ids()

        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as pool:
            with tqdm(
                total=len(services["business-services"]),
                unit="business-service",
                desc=f"Getting {self.name} Business Services",
            ) as progress:
                futures = []
                for service_url in services["business-services"]:
                    future = pool.submit(
                        self.get_bsm,
                        id=service_url[26:],
                    )
                    future.add_done_callback(lambda p: progress.update())
                    futures.append(future)
                for future in futures:
                    bsm = future.result()
                    if isinstance(bsm, pyonms.models.business_service.BusinessService):
                        self.cache[bsm.id] = bsm
                        self.cache_name[bsm.name] = bsm.id
                        service_list.append(bsm)

        return service_list

    def find_bsm_name(
        self, name: str, cache_only: bool = False
    ) -> Optional[pyonms.models.business_service.BusinessService]:
        """Get all BusinessService objects and filter to matching names."""
        if self.cache_name.get(name):
            return self.cache[self.cache_name[name]]
        elif cache_only:
            return None
        else:
            services = self._get(url=self.url)
            for service_url in services.get("business-services", []):
                service_record = self._get(url=f"{self.hostname}{service_url}")
                if service_record["name"] == name:
                    return self._process_bsm(service_record)
        return None

    def _process_bsm(
        self, data: dict
    ) -> pyonms.models.business_service.BusinessService:
        data["ip_services_edges"] = data.get("ip-service-edges", [])
        data["reduction_key_edges"] = data.get("reduction-key-edges", [])
        data["child_edges"] = data.get("child-edges", [])
        data["application_edges"] = data.get("application-edges", [])
        data["parent_services"] = data.get("parent-services", [])
        data["reduce_function"] = data.get("reduce-function", [])
        data["operational_status"] = data.get("operational-status", [])
        del data["operational-status"]
        del data["ip-service-edges"]
        del data["reduction-key-edges"]
        del data["child-edges"]
        del data["application-edges"]
        del data["parent-services"]
        del data["reduce-function"]
        business_service = pyonms.models.business_service.BusinessService(**data)
        return business_service

    def reload_bsm_daemon(self) -> None:
        """Trigger reload of the `bsmd` daemon."""
        self._post(url=f"{self.url}/daemon/reload", json={})

    def create_bsm(
        self, bsm: pyonms.models.business_service.BusinessServiceRequest
    ) -> None:
        """Create new BusinessService object."""
        response = self._post(url=self.url, json=bsm.to_dict())
        if "constraint [bsm_service_name_key]" in response.text:
            raise pyonms.models.exceptions.DuplicateEntityError(bsm.name, bsm)

    def update_bsm(
        self, id: int, bsm: pyonms.models.business_service.BusinessServiceRequest
    ):
        """Update existing BusinessService object."""
        self._put(url=f"{self.url}/{id}", json=bsm.to_dict())  # noqa: W0612

    def _merge_bsm_request(
        self,
        bsm: pyonms.models.business_service.BusinessService,
        request: pyonms.models.business_service.BusinessServiceRequest,
    ) -> pyonms.models.business_service.BusinessServiceRequest:
        new_request = bsm.request()
        new_request.name = request.name
        new_request.reduce_function = request.reduce_function
        new_request.attributes = request.attributes
        for ip_edge in request.ip_service_edges:
            if ip_edge in new_request.ip_service_edges:
                new_request.ip_service_edges.remove(ip_edge)
            new_request.ip_service_edges.append(ip_edge)
        for child_edge in request.child_edges:
            if child_edge in new_request.child_edges:
                new_request.child_edges.remove(child_edge)
            new_request.child_edges.append(child_edge)
        for app_edge in request.application_edges:
            new_request.application_edges.append(app_edge)
        for key_edge in request.reduction_key_edges:
            new_request.reduction_key_edges.append(key_edge)
        for parent in request.parent_services:
            new_request.parent_services.append(parent)
        return new_request

    def delete_bsm(self, bsm: pyonms.models.business_service.BusinessService) -> None:
        """Delete BusinessService object."""
        self._delete(url=f"{self.url}/{bsm.id}")
        if self.cache.get(bsm.id):
            del self.cache[bsm.id]
        if self.cache_name.get(bsm.name):
            del self.cache_name[bsm.name]
