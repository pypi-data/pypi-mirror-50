# Broker Client Module Repository

Instructions for using broker_client.

## Dependencies

`sudo apt-get install python3-setuptools`


## Install

Install with `pip`: `pip install broker_client`

Or, put this on your `requirements.txt`:

```
broker_client
```

## Use

```
import broker_core

# then, if you are a service provider, register your service:
register("service-description-filename.jsonld")
# the response is a tuple, either:
#  (True, service_description_dict) for when the request worked, or
#  (False, service_description_dict) for when the request failed

# and if you want to discover a service of type FictionalType:
locate({"@type": "http://schema.org/FictionalType"}, "http://put-the-broker.url.here")
# the response is a list of the found service descriptions
```

## Publish a new version

If you are *changing* the code of this library, and want to make a new release, follow these steps:

1. Change the version in `setup.py`
2. Run `python setup.py sdist upload`

If a password is asked and you don't know what to do, ask the maintainer (Geovane Fedrecheski).
