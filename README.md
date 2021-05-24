# nicehash-api

## required ENV variables

```env
CONFIG_ORG_ID
CONFIG_KEY
CONFIG_SECRET
NICEHASH_API_ENDPOINT
```

## Docker Compose

```docker-compose
version: "3.7"

services:
  nicehash_api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: nicehash_api
    restart: always
    env_file: nicehash_api.env
    ports:
      - 5000:5000
```

## API

```Python
/ # GET hello world API test
/available/{rig_id} # GET is rig available?
/device_info/{rig_id} # GET info on rig
/is_on/{rig_id} # GET is the rig on?
/turn_on/{rig_id} # POST turn on rig
/turn_off/{rig_id} # POST turn off rig
```
