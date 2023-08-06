This is a wrapper package for Buyproxies.org API.
You can retrive your account's proxies in following formats: 
  - String
  - Python List
  - Json
  
 ### Installation
```sh
$ pip install BuyProxiesAPI
```

### Usage
```python
from buyproxies_api import BuyProxiesAPI

# buyproxies.org API KEY
API_KEY = '021b5584b0c5c4735a9a157169d8c030'

# Proxy Service ID
service_id = 120810

# Initialize the API
proxy_api = BuyProxiesAPI(API_KEY)

# Retrieve proxies as string
proxies_str = proxy_api.get_proxies(service_id, return_as='str')

# Retrieve proxies as Python list
proxies_list = proxy_api.get_proxies(service_id, return_as='list')

# Retrieve proxies as JSON
proxies_json = proxy_api.get_proxies(service_id, return_as='json')
```