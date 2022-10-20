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

new_instance = pyonms.portal.models.PortalInstanceCreate(name="TestDocker2")

core = pyonms.portal.models.PortalHttpConfig(
    url=broker_host, user=minion_user, password=minion_pass
)
created_instance = my_portal.create_instance(new_instance)

new_con_profile = pyonms.portal.models.PortalConnectivityProfileCreate(
    name="ConProfile",
    onmsInstance=created_instance,
    httpConfig=core,
    brokerConfig=new_broker,
)

con_profile = my_portal.create_connectivity_profile(new_con_profile)

new_location = pyonms.portal.models.PortalLocationCreate(
    name="LocationName",
    onmsInstance=created_instance,
    connectivityProfile=con_profile,
)
location = my_portal.create_location(new_location)

minion = pyonms.portal.models.PortalMinion(locationId=location)

appliance_list = my_portal.get_all_appliances()

appliance = appliance_list[0]

appliance.minion = minion

updated_appliance = my_portal.update_appliance(appliance)
pass
