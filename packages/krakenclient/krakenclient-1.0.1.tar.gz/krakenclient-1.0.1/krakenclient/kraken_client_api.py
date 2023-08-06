import krakenex

# Documentation at: https://www.kraken.com/features/api
public_key = ''
private_key = ''


def set_keys(public, private):
    global public_key
    public_key = public
    global private_key
    private_key = private


def i_need_help():
    print('Kraken Documentation:', 'https://www.kraken.com/features/api')
    print('krakenclient Source Code:', 'https://github.com/ApacheDatastreams/krakenclient')
    print('krakenex Source Code:', 'https://github.com/veox/python3-krakenex')

# Public Market Data Functions -----------------------------------------------------


def get_server_time():
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_public('Time')
    return result


def get_asset_info(info=None, aclass=None, asset=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_public('Assets', {'info': info, 'aclass':aclass, 'asset':asset})
    return result


def get_asset_pairs(info=None, pair=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_public('Assets', {'info': info, 'pair': pair})
    return result


def get_ticker_info(pair):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_public('Ticker', {'pair': pair})
    return result


def get_OHLC_data(pair, interval=None, since=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_public('OHLC', {'pair': pair, 'inverval': interval, 'since': since})
    return result


def get_order_book(pair , count=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_public('Depth', {'pair': pair, 'count':count})
    return result


def get_recent_trades(pair, since=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_public('Trades', {'pair': pair, 'since':since})
    return result


def get_recent_spread_data(pair, since=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_public('Spread', {'pair': pair, 'since':since})
    # Note: returns arrays of [time, bid, ask]
    return result

# Private User Data ------------------------------------


# NOTE: Currently not working
def get_trade_balance(asset, aclass=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('TradeBalance', {'aclass': aclass, 'asset':asset})
    result = kraken.query_private('TradeBalance', {})
    return result


def get_open_orders(trades=None, userref=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    #result = kraken.query_private('OpenOrders', {'trades': trades, 'userref':userref})
    result = kraken.query_private('OpenOrders', {})
    return result


def get_closed_orders(trades=None, userref=None, start=None, end=None, ofs=None, closetime=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('ClosedOrders', {})
    return result


def get_query_orders(txid, trades=None, userref=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('QueryOrders', {'txid': txid})
    return result


def get_trades_history(ofs, type=None, trades=None, start=None, end=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('TradesHistory', {'ofs': ofs})
    return result


def query_trades_info(txid, trades=False):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('QueryTrades', {'txid': txid})
    return result


def get_open_positions(txid, docalcs=False):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('OpenPositions', {'txid': txid, 'docalcs': docalcs})
    return result


def get_ledgers_info(ofs, aclass=None, asset=None, type='all', start=None, end=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('Ledgers', {'ofs': ofs, 'aclass': aclass, 'asset' : asset, 'type' : type,
                                              'start': start, 'end': end})
    return result


def query_ledgers(ids):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('QueryLedgers', {'id': ids})
    return result


def get_trade_volume(pair=None, fee_info=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('TradeVolume', {'pair': pair, 'fee-info': fee_info})
    return result

# Note: I skipped the export reports here


# Private User Trading ------------------------------------
def add_standard_order(pair, type, ordertype, volume, leverage='none', price=None, price2=None,oflags=None,
                       starttm=None, expiretm=None, userref=None, validate=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('AddOrder', {'pair': pair, 'type': type, 'ordertype': ordertype, 'volume': volume,
                                               'leverage': leverage, 'price': price, 'price2': price2, 'oflags': oflags,
                                               'starttm': starttm, 'expiretm': expiretm, 'userref': userref,
                                               'validate': validate})
    return result


def cancel_open_order(txid):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('CancelOrder', {'txid': txid})
    return result

# Private User Funding ------------------------------------


def get_deposit_methods(asset, aclass=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('DepositMethods', {'aclass': aclass, 'asset': asset})
    return result


def get_deposit_addresses(asset, method, aclass=None, new=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('DepositAddresses', {'aclass': aclass, 'asset': asset, 'method': method,
                                                       'new' : new})
    return result


def deposit_status(asset, method, aclass):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('DepositStatus', {'aclass': aclass, 'asset': asset, 'method': method})
    return result


def withdrawal_info(asset, key, amount, aclass=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('WithdrawInfo', {'aclass': aclass, 'asset': asset, 'key': key, 'amount': amount})
    return result


def withdraw_funds(asset, key, amount):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('Withdraw', {'asset': asset, 'key': key, 'amount': amount})
    return result


def recent_withdrawal_status(asset, aclass=None, method=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('WithdrawStatus', {'aclass': aclass, 'asset': asset, 'method': method})
    return result


def cancel_withdrawel(asset, refid, aclass=None):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('WithdrawCancel', {'aclass': aclass, 'asset': asset, 'refid': refid})
    return result


def KrakenTransfer(asset, to_wallet, from_wallet, amount):
    kraken = krakenex.API(key=public_key, secret=private_key)
    result = kraken.query_private('WalletTransfer', {'asset': asset, 'to': to_wallet, 'from': from_wallet, 'amount':
        amount})
    return result
