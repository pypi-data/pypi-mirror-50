# opencpaas-twilio

This is the Twilio implementation of OpenCpaas.

See our [full documentation]().

## Requirements

- [Python](https://www.python.org/downloads/) 3.5+

## Installation

```python
pip install opencpaas-twilio
```

## Testing

Run the following command in the project directory:

```python
python -m unittest discover
```
	
## Getting Started

### Client Initialization

Begin by initializing a new Twilio client. 

```python
from opencpaas_twilio import TwilioClient

auth = 	{
      'account_sid': "12345"
      'auth_token': "678910"
	}

client = TwilioClient(auth)

```

In order to initialize a new Twilio Client you MUST include an account_sid and auth_token a CpaasAuthenticationException will be thrown.
