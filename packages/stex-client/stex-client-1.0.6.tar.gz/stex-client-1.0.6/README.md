# STEX (former Stocks.Exchange) (Python API client)
STEX (former Stocks.Exchange) provides all the core exchange functionality, and additional merchant tools available via the HTTPS API where all returned messages are in JSON. It's much easier to work with the API by using one of the clients provided by STEX, so while this page describes the API in case you want or need to build your own client, the examples use the Python client.
## Requirements
- Python >= 3.5
## Dependent Libraries
- requests
- furl
- pendulum
- python-socketio

## General
The base URL for all the requests other than public methods is 
```
https://api3.stex.com
```

## Getting started
- [Documentation](http://help.stex.com/api-integration).
- [Sandbox API V3](https://apidocs.stex.com).

To get started with the Python API client, here's a snippet for creating a client with existing credentials:
> In order to use the API functions, you must have an API key and API secret, which is generated in the user profile.

## Lists Methods Public Example
- [Sandbox API](https://apidocs.stex.com).
```python
from stex_client.public import Public
public = Public()
public.ping() #https://apidocs.stex.com/#/Public/get_public_ping
public.currencies() #https://apidocs.stex.com/#/Public/get_public_currencies
public.currencies_by_id(1) #https://apidocs.stex.com/#/Public/get_public_currencies__currencyId_
public.markets() #https://apidocs.stex.com/#/Public/get_public_markets
public.pairs_groups() #https://apidocs.stex.com/#/Public/get_public_pairs_groups
public.currency_pairs_list('BTC') #https://apidocs.stex.com/#/Public/get_public_currency_pairs_list__code_
public.pairs_groups_by_id(1) #https://apidocs.stex.com/#/Public/get_public_currency_pairs_group__currencyPairGroupId_
public.currency_pairs_by_id(1) #https://apidocs.stex.com/#/Public/get_public_currency_pairs__currencyPairId_
public.ticker() #https://apidocs.stex.com/#/Public/get_public_ticker
public.ticker_by_currency_pair_id(1) #https://apidocs.stex.com/#/Public/get_public_ticker__currencyPairId_
public.trades_by_currency_pair_id(1, {'limit': 1}) #https://apidocs.stex.com/#/Public/get_public_trades__currencyPairId_
public.orderbook_by_currency_pair_id(1, {'limit_bids': 1, 'limit_asks': 1}) #https://apidocs.stex.com/#/Public/get_public_orderbook__currencyPairId_
public.chart(1, '1D') #https://apidocs.stex.com/#/Public/get_public_chart__currencyPairId___candlesType_

```

## Lists Methods Private Example
- [Sandbox API](https://apidocs.stex.com)
- [How to get the settings](https://help.stex.com/articles/2740368-how-to-connect-to-the-stex-api-v3-using-postman)
```python
from stex_client.private import Private
private = Private({
    'client': {
        'id': '',
        'secret': ''
    },
    'tokenObject': {
        'access_token': '',
        'refresh_token': '',
    },
    'accessTokenUrl': 'https://api3.stex.com/oauth/token',
    'scope': 'trade profile reports withdrawal',
})
private.profile_info()
private.profile_wallets()
private.profile_wallets_by_id(1)
private.post_profile_wallets_by_currency_id(1)
private.profile_deposit_address_by_wallet_id(1)
private.new_deposit_address_by_wallet_id(1)
private.profile_deposits({'limit': 1})
private.profile_deposits_by_id(1)
private.profile_withdrawals({'limit': 1})
private.profile_withdrawals_id(1)
private.create_withdrawal(1, 0.1, 'address', 'additional_address')
private.cancel_withdrawal(1)
private.reports_orders({'limit': 1})
private.reports_orders_id(1)
private.trading_fees_by_pair_id(1)
private.trading_open_orders()
private.trading_cancel_all_open_orders()
private.trading_orders_by_pair_id(1)
private.cancel_trading_orders_by_pair_id(1)
private.create_trading_orders_by_pair_id(1, 'BUY', 1, 1)
private.get_trading_orders_by_id(1)
private.cancel_trading_orders_by_id(1)

```

## Lists Methods WebSocket Example
- [Documentation](https://docs.google.com/document/d/1CaD7qV6UzSJ72DMY0qLHnRgabhadVV0Kxc2_lhEFWKA)
- [How to get the settings](https://help.stex.com/articles/2740368-how-to-connect-to-the-stex-api-v3-using-postman)
```python
from stex_client.wss import WebsocketStex
client = WebsocketStex({
    'client': {
        'id': '',
        'secret': ''
    },
    'tokenObject': {
        'access_token': '',
        'refresh_token': '',
    },
    'accessTokenUrl': 'https://api3.stex.com/oauth/token',
    'scope': 'push',
})
def show(*args):
    print(args)
    
client.subscribe_rate(show)
client.subscribe_order_fill_created(1, show)
client.subscribe_glass_total_changed(1, 'sell', show)
client.subscribe_glass_row_changed(1, 'sell', show)
client.subscribe_best_price_changed(1, 'bid', show)
client.subscribe_candle_changed(1, '1D', show)
client.subscribe_balance_changed(1, show)
client.subscribe_user_order('sell', 1, 1, show)
client.subscribe_user_order_deleted( 1, 1, show)
client.subscribe_user_order_fill( 1, 1, show)
client.subscribe_user_order_fill( 1, 1, show)

```
	