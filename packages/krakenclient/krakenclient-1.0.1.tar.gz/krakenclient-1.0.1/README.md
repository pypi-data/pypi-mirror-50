# krakenclient: Python API client for Kraken (built on krakenex)

## Installation
```sh
pip3 install krakenclient
```

## Usage
```python
import krakenclient.kraken_client_api as krakenclient

# How to access order book data 
xrp_order_book = krakenclient.get_order_book(pair='XRPUSD')
print(xrp_order_book)

# How to perform account operations
krakenclient.set_keys(public='your_public_key', private='your_private_key')  # Set your api keys to perform account operations
trade_balance = krakenclient.get_trade_balance(asset='XRPUSD')
print(trade_balance)

# Need help? 
krakenclient.i_need_help()

```


## Dependencies
- [Python 3](https://www.python.org/)
- [krakenex](https://github.com/veox/python3-krakenex): 2.1.0

## Disclaimer
We are not affiliated with Kraken and this is a third-party implementation.