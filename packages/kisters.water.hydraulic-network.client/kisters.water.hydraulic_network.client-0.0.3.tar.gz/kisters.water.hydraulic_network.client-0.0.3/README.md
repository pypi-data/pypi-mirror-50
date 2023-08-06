# Hydraulic Network Client Library

This library allows connections to remote hydraulic network REST servers. It
supports authentication with OpenID Connect.

## Installation

Install with `pip`.

```bash
> python -m pip install kisters.water.hydraulic_network.client
```


## Example Usage

### Simple Case

```python
from kisters.water.hydraulic_network.client import Network, RESTClient

network = Network(
    "my-network",
    client=RESTClient(url="http://127.0.0.1:80/")
)
```

### Auth Case

```python
from kisters.water.hydraulic_network.client import (
    Network,
    OpenIDConnect,
    RESTClient,
)

authentication = OpenIDConnect(
    issuer_url="https://keycloak.water.kisters.de/auth/realms/kisters",
    client_id="jesse-test",
    client_secret="c4b0f70d-d2e6-497f-b11c-d49fe806c29b",
)
client = RESTClient(url="http://127.0.0.1:80/", authentication=authentication)
network = Network("my-network", client=client)
```
