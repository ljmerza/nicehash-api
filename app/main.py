import asyncio
import os 
import sys

from fastapi import FastAPI

from .nicehash import NiceHashPrivateAPI


version = f"{sys.version_info.major}.{sys.version_info.minor}"

CONFIG_ORG_ID = os.getenv('CONFIG_ORG_ID')
CONFIG_KEY = os.getenv('CONFIG_KEY')
CONFIG_SECRET = os.getenv('CONFIG_SECRET')
NICEHASH_API_ENDPOINT = os.getenv('NICEHASH_API_ENDPOINT')
ROOT_PATH = os.getenv('ROOT_PATH')

app = FastAPI()

api = NiceHashPrivateAPI(
      NICEHASH_API_ENDPOINT,
      CONFIG_ORG_ID,
      CONFIG_KEY,
      CONFIG_SECRET,
    )


async def get_rig(rig_id):
  """Return the rig object."""
  rig = None
  rigs = await api.get_rigs_data()
  for rig_entry in rigs.get("miningRigs", []):
    if rig_entry.get("rigId") == rig_id:
      rig = rig_entry
  return rig


@app.get("/")
async def read_root():
    message = f"Hello world! Using Python {version}"
    return {"message": message}

@app.get("/available/{rig_id}")
async def available(rig_id):
  """Return availability"""
  rig = await get_rig(rig_id)
  message = (
      rig is not None
      and rig.get("minerStatus", "UNKNOWN")
      not in ["DISABLED", "TRANSFERED", "UNKNOWN", "OFFLINE"]
  )
  return {"message": message}

@app.get("/device_info/{rig_id}")
async def device_info(rig_id):
    rig = await get_rig(rig_id)
    message = {
        "identifiers": rig_id,
        "name": rig.get("name"),
        "sw_version": rig.get("softwareVersions"),
        "model": rig.get("softwareVersions"),
        "manufacturer": "NiceHash",
    }
    return {"message": message}

@app.get("/is_on/{rig_id}")
async def is_on():  
  rig = await get_rig(rig_id)
  if rig is not None:
      status = rig.get("minerStatus", "UNKNOWN")
      if status in ["BENCHMARKING", "MINING"]:
          return {"message": True}
  return {"message": False}
        
@app.get("/turn_on/{rig_id}")
async def turn_on(rig_id):  
  """Turn the switch on."""
  try:
      await api.set_rig_status(rig_id, True)
  except Exception as err:
      return {"message": False}
  return {"message": True}

@app.get("/turn_off/{rig_id}")
async def turn_off(rig_id):  
  """Turn the switch off."""
  try:
      await api.set_rig_status(rig_id, False)
  except Exception:
      return {"message": False}
  return {"message": True}