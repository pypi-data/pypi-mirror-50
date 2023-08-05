# iotery.io Python Server SDK

The python iotery.io SDK is intended to be used on your server or in your data processing apps to interact with the itoery.io IoT Platform. The SDK is a fully featured wrapper for the [REST API](https://dashboard.iotery.io/docs/account-manager).

## Getting Started

Setup your free account on [iotery.io]() and go to your [settings dashboard]() to get your server API Key.

After you get your key, install the SDK:

```bash
pip install iotery-python-server-sdk
```

> Note: Make sure you are using Python 3.5+!

And finally, some simple example usage:

```python
from iotery_python_server_sdk import Iotery


iotery = Iotery("my-key")

# find the exact `data` specification at https://iotery.io/v1/docs#createDeviceType
device_type = iotery.createDeviceType(
    data={"name": "My Device Type", "enum": "MY_DEVICE_TYPE", ...})

device_type_by_uuid = iotery.getDeviceTypeByUuid(
    deviceTypeUuid=device_type["uuid"], opts={"limit": 1})
```

> The above code connects you to the iotary.io platform, creates a device type and then gets that device type.

Next, you might want to create a data type for the the device type you created...here's an example snippet:

```python
temperature_data_type = iotery.createDataType(
  deviceTypeUuid=device_type_by_uuid["uuid"],
  data = {
    name: "Temperature",
    enum: "TEMPERATURE",
    units: "C",
    isNumber: true
  }
)
```

> To have a "thing" (like a Raspberry Pi) create data, you will want to check out the [iotery.io thing client](link).

For a tutorial on setting up a full stack system in 15 minutes using iotery.io, check [this link](medium_article) out.

## API

This SDK simply wraps the [REST API](https://somelink_to_swagger_docs), so more information and specifics can be found there. Since the API is a wrapper around the REST API, the syntax is standard for each of the Create, Read, Update, and Delete operations on iotery.io resources. All methods return a dictonary containing the API response. If there is an error, the method will `raise` an expection.

### Creating Resources

The generalized syntax for creating resources in iotery.io python sdk looks like:

```python
iotery.methodName(inputParameter="parameter", data={ "data": "variables" })
```

For example, to create a device, the javascript would look like

```python
createDevice(
  deviceTypeUuid="a-valid-device-type-uuid",
  data={ "name": "My Device", "other": "parameter" }
)
```

where `createDevice` maps to `methodName`, `deviceTypeUuid` maps to `inputParameter`, and `name` and `other` map to the dictonary `{data : "variables"}` in the generalized form given above.

The available resource creation methods are

| createDeviceType | `` | [link](https://iotery.io/v1/docs#createDeviceType) | Creates a new device type |
| createDevice | `deviceTypeUuid` | [link](https://iotery.io/v1/docs#createDevice) | Creates a new device with a given device type |

### Reading Resources

The generalized syntax for reading (getting) resources in iotery.io python sdk looks like:

```python
iotery.methodName(inputParameter="parameter", opts={"query":"parameter"})
```

For example, to get a device by it's unique identifier `uuid`, the python would look like

```python
getDeviceByUuid(
  deviceUuid="a-valid-device-uuid",
  opts={ "limit": 1 }
)
```

where `getDeviceByUuid` maps to `methodName`, `deviceUuid` maps to `inputParameter`, and `{ "limit": 1 }` maps to the dictonary `{"query" : "parameters"}` in the generalized form given above.

> The `limit` option is for instructive purposes only. By definition, a `uuid` is unique and so there will never be more than one device for a given `uuid`.

For more advanced queries, some parameters allow for an array of values to be passed in. Two options available are `$in` and `$btwn`, which allows a user to specify a set or range of values, respectively. For example, when requesting for data for a device, one may use the SDK as follows:

```python
iotery.getDeviceDataList(
    opts={
        "dataTypeEnum": {"$in": ["ENUM_1","ENUM_2","ENUM_3"]},
        "timestamp": {"$btwn": [1562759000, 1562759500]},
        "limit": 5
      },
    deviceUuid="a-valid-device-uuid")
```

Refer to the iotery REST API docs to see when options such as `$in` and `$btwn` are available for a given query parameter.

The available resource creation methods are

| getDeviceTypes | `` | [link](https://iotery.io/v1/docs#getDeviceTypes) | Gets all device types |
| getDeviceTypeByUuid | `deviceTypeUuid` | [link](https://iotery.io/v1/docs#getDeviceyTypeByUuid) | Gets a device type by uuid |

### Updating Resources

The generalized syntax for updating resources in iotery.io python sdk looks like:

```python
iotery.methodName(inputParameter="parameter", data={ "data": "variables" })
```

For example, to update a device type, the javascript would look like

```python
updateDeviceType(
  deviceTypeUuid="a-valid-device-type-uuid",
  data={ "name": "My New Name" }
)
```

where `updateDevice` maps to `methodName`, `deviceTypeUuid` maps to `inputParameter`, and `{ "name": "My New Name" }` maps to the dictonary `{data : "variables"}` in the generalized form given above.

The available resource creation methods are

| updateDeviceType | `deviceTypeUuid` | [link](https://iotery.io/v1/docs#updateDeviceType) | Updates a device type by uuid |

### Deleting Resources

The generalized syntax for reading (getting) resources in iotery.io python sdk looks like:

```python
iotery.methodName(inputParameter="parameter", opts={"query":"parameter"})
```

For example, to get a device by it's unique identifier `uuid`, the python would look like

```python
deleteDevice(
  deviceUuid="a-valid-device-uuid",
  opts={ "some": "option" }
)
```

where `deleteDevice` maps to `methodName`, `deviceUuid` maps to `inputParameter`, and `{ "some": "option" }` maps to the dictonary `{"query" : "parameters"}` in the generalized form given above.

The available resource creation methods are

| deleteDeviceType | `deviceTypeUuid` | [link](https://iotery.io/v1/docs#deleteDeviceType) | Deletes a device type by uuid |

## Simple Getting Data Example

```
from iotery_python_server_sdk import Iotery
import json

API_KEY = "MY_TEAM_API_KEY"

DEVICE_UUID = "MY_DEVICE_UUID"
DATA_TYPE_ENUM = "MY_DATA_TYPE_ENUM"

iotery = Iotery(API_KEY)

device_data_list = iotery.getDeviceDataList(
    opts={"dataTypeEnum": DATA_TYPE_ENUM, "limit": 5}, deviceUuid=DEVICE_UUID)

print(json.dumps(device_data_list["results"], indent=2))

```

## Contributing

We welcome contributors and PRs! Let us know if you are interested.
