from .http import Http

class RestService(object):
    def __init__(self, auth, url = 'https://api.novadax.com'):
        self._http = Http(url, auth)

    def list_symbol_trades(self, symbol, limit = 100):
        return self._http.get('/v1/symbols/{}/trades'.format(symbol), {
            'limit': limit
        })

    def list_orders(self, symbol, status = None, from_id = None, to_id = None, limit = 100):
        return self._http.get_with_auth('/v1/orders', {
            'symbol': symbol,
            'status': status,
            'from': from_id,
            'to': to_id,
            'limit': limit
        })

    def place_order(self, symbol, _type, side, price = None, amount = None, value = None):
        return self._http.post_with_auth('/v1/orders', {}, {
            'symbol': symbol,
            'type': _type,
            'side': side,
            'price': price,
            'amount': amount,
            'value': value
        })

    def batch_cancel_order(self, ids):
        return self._http.post_with_auth('/v1/orders/batchCancel', {}, ids)

    def cancle_order(self, id):
        return self._http.post_with_auth('/v1/orders/{}/cancel'.format(id))

    def query_order(self, id):
        return self._http.get_with_auth('/v1/orders/{}'.format(id))

    def batch_query_order(self, order_ids):
        return self._http.get_with_auth('/v1/orders/batchList', {
            'orderIds': ','.join(order_ids)
        })

    def query_order_fills(self, id):
        return self._http.get_with_auth('/v1/orders/{}/fill'.format(id))