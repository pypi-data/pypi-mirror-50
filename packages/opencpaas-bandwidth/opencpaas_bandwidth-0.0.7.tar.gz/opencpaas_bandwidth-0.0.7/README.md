# opencpaas-bandwidth

This is the Bandwidth implementation of OpenCpaas.

See our [full documentation]().

## Requirements

- [Python](https://www.python.org/downloads/) 3.5+

## Installation

```python
pip install opencpaas-bandwidth
```

## Testing

Run the following command in the project directory:

```python
python -m unittest discover
```


## Getting Started

### Client Initialization

Begin by initializing a new Bandwidth client. 

```python
from opencpaas_bandwidth import BandwidthClient

auth = 	{
	'api_token': '789',
	'api_secret':'1011',
	'account_id': 'myaccount' ,
	'application_id': 'myapplication',
	'user': 'username',
	'pass': 'password',
	'site_id': '12345' 
	}

client = BandwidthClient(auth)

```

Bandwidth requires several different authorizations in order to perform voice, messaging, or number functions.
In order to initialize a new Bandwidth Client you MUST include an account_id or a CpaasAuthenticationException will be thrown.
