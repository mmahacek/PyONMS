# test.py

import os

from pyonms.portal import Portal
import pyonms.portal.models
from dotenv import load_dotenv

load_dotenv()

my_portal = Portal(secret=os.getenv("portal_secret"))

minion_user = os.getenv("minion_user")
minion_pass = os.getenv("minion_pass")
broker_host = os.getenv("broker_host")
broker_jms = os.getenv("broker_jms")

new_broker = pyonms.portal.models.PortalBrokerJms(
    type="JMS",
    url=broker_jms,
    user=minion_user,
    password=minion_pass,
)

new_instance = pyonms.portal.models.PortalInstanceCreate(name="TestDocker")

core = pyonms.portal.models.PortalHttpConfig(
    url=broker_host, user=minion_user, password=minion_pass
)
created_instance = my_portal._post(
    uri=f"{my_portal.base_v1}instance", json=new_instance.to_dict()
)

new_con_profile = pyonms.portal.models.PortalConnectivityProfileCreate(
    name="ConProfile",
    onmsInstance=created_instance,
    httpConfig=core,
    brokerConfig=new_broker,
)

con_profile = my_portal._post(
    uri=f"{my_portal.base_v1}connectivity-profile", json=new_con_profile.to_dict()
)
# ----

new_location = pyonms.portal.models.PortalLocationCreate(
    name="Location Name",
    onmsInstance=created_instance,
    connectivityProfile=con_profile,
)
location = my_portal._post(
    uri=f"{my_portal.base_v1}location", json=new_location.to_dict()
)
minion = pyonms.portal.models.PortalMinion(locationId=location)

appliance_list = my_portal._get(
    uri=f"{my_portal.base_v1}appliance",
)
appliance = pyonms.portal.models.PortalAppliance(**appliance_list["pagedRecords"][0])
appliance.minion = minion

updated_appliance = my_portal._put(
    uri=f"{my_portal.base_v1}appliance/{appliance.id}", json=appliance.to_dict()
)
pass
