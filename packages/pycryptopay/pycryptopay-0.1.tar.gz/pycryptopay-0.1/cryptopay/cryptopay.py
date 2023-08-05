import time
from asyncio import gather, get_event_loop, sleep
from inspect import iscoroutinefunction
from threading import Thread

import aiohttp
import requests

from cryptopay.classes import Payment


class Application:
    MAIN_URL = 'http://3.9.215.1:5555'
    DETAILED_PAYMENT_ENDPOINT = '/payment/{payment_id}'
    PAYMENT_ENDPOINT = '/payment'
    PAYMENTS_ENDPOINT = '/payments'
    CURRENCIES_ENDPOINT = '/currencies'

    def __init__(self, token, callback=None, loop=None):
        self.token = token
        self.callback = callback
        self._loop = loop or get_event_loop()
        self._init_callback()

    def _init_callback(self):
        if self.callback:
            if not callable(self.callback):
                raise ValueError('callback must be callable')
            if iscoroutinefunction(self.callback):
                self._loop.create_task(self._check_payments_periodic_async())
                Thread(target=self._loop.run_forever).start()
            else:
                Thread(target=self._check_payments_periodic).start()

    def _process_request(self, *, method: str, endpoint: str, json=None):
        response = getattr(requests, method)(self.MAIN_URL + endpoint, headers={'app_token': self.token}, json=json)
        response.raise_for_status()
        return response.json()

    async def _process_request_async(self, *, method: str, endpoint: str, json=None):
        async with aiohttp.ClientSession() as session:
            resp = await getattr(session, method)(self.MAIN_URL + endpoint, headers={'app_token': self.token}, json=json)
            resp.raise_for_status()
            return await resp.json()

    def _check_payments_periodic(self):
        while True:
            time.sleep(3)
            try:
                payments = self.get_all_payments()
            except:
                continue
            for payment in payments:
                self._handle_payment(payment)

    async def _check_payments_periodic_async(self):
        while True:
            await sleep(3)
            try:
                payments = await self.get_all_payments_async()
            except:
                continue
            tasks = [self._handle_payment_async(payment) for payment in payments]
            await gather(*tasks)


    def _handle_payment(self, payment):
        if 'fixed_amount' not in payment.data:
            return
        if payment.data['fixed_amount'] < payment.amount:
            if 'target_amount' not in payment.data:
                payment.data['donated'] = payment.amount - payment.data['fixed_amount']
            else:
                if payment.amount < payment.data['target_amount']:
                    return
            self._on_success_payment(payment)

    async def _handle_payment_async(self, payment):
        if 'fixed_amount' not in payment.data:
            return
        if payment.data['fixed_amount'] < payment.amount:
            if 'target_amount' not in payment.data:
                payment.data['donated'] = payment.amount - payment.data['fixed_amount']
            else:
                if payment.amount < payment.data['target_amount']:
                    return
            await self._on_success_payment_async(payment)

    def _call_callback(self, payment):
        method_args = self.callback.__code__.co_varnames
        kwargs = {}
        for k, v in payment.data.items():
            if k in method_args:
                kwargs[k] = v
        self.callback(**kwargs)

    async def _call_callback_async(self, payment):
        method_args = self.callback.__code__.co_varnames
        kwargs = {}
        for k, v in payment.data.items():
            if k in method_args:
                kwargs[k] = v
        await self.callback(**kwargs)

    def _on_success_payment(self, payment):
        self._call_callback(payment)
        payment.data['fixed_amount'] = payment.amount
        del payment.data['donated']
        self.update_payment_data(payment.id, payment.data)

    async def _on_success_payment_async(self, payment):
        await self._call_callback_async(payment)
        payment.data['fixed_amount'] = payment.amount
        del payment.data['donated']
        await self.update_payment_data_async(payment.id, payment.data)

    def get_currencies(self):
        """
        Returns list of currencies available for your application type
        """
        return self._process_request(method='get', endpoint=self.CURRENCIES_ENDPOINT)

    async def get_currencies_async(self):
        """
        Returns list of currencies available for your application type in async mode
        """
        return await self._process_request_async(method='get', endpoint=self.CURRENCIES_ENDPOINT)

    def get_payment(self, payment_id: str):
        """
        :param payment_id: payment identifier
        :return: Payment
        """
        response = self._process_request(
            method='get',
            endpoint=self.DETAILED_PAYMENT_ENDPOINT.format(payment_id=payment_id)
        )
        return Payment(**response)

    async def get_payment_async(self, payment_id: str):
        """
        :param payment_id: payment identifier
        :return: Payment
        """
        response = await self._process_request_async(
            method='get',
            endpoint=self.DETAILED_PAYMENT_ENDPOINT.format(payment_id=payment_id)
        )
        return Payment(**response)

    def get_all_payments(self):
        """
        Get all payments bound with your application
        :return:
        """
        response = self._process_request(method='get', endpoint=self.PAYMENTS_ENDPOINT)
        return [Payment(**p) for p in response]

    async def get_all_payments_async(self):
        """
        Get all payments bound with your application async
        :return:
        """
        response = await self._process_request_async(method='get', endpoint=self.PAYMENTS_ENDPOINT)
        return [Payment(**p) for p in response]

    def create_payment(self, symbol, data=None):
        """
        Creating new payment async
        :param symbol: one of supported symbols
        :param data: data to be stored with payment object, dict or None
        :return:
        """
        json = {'symbol': symbol}
        if not data:
            data = {}
        data['fixed_amount'] = 0
        json['data'] = data
        response = self._process_request(method='put', endpoint=self.PAYMENT_ENDPOINT, json=json)
        return Payment(**response)

    async def create_payment_async(self, symbol, data=None):
        """
        Creating new payment async
        :param symbol: one of supported symbols
        :param data: data to be stored with payment object, dict or None
        :return:
        """
        json = {'symbol': symbol}
        if not data:
            data = {}
        data['fixed_amount'] = 0
        json['data'] = data
        response = await self._process_request_async(method='put', endpoint=self.PAYMENT_ENDPOINT, json=json)
        return Payment(**response)

    def update_payment_data(self, payment_id, data):
        """
        Upload new payment data
        :param payment_id: payment identifier
        :param data: dict
        :return: Payment object
        """
        response = self._process_request(
            method='post',
            endpoint=self.PAYMENT_ENDPOINT,
            json={'data': data, 'payment_id': payment_id}
        )
        return Payment(**response)

    async def update_payment_data_async(self, payment_id, data):
        """
        Upload new payment data async
        :param payment_id: payment identifier
        :param data: dict
        :return: Payment object
        """
        response = await self._process_request_async(
            method='post',
            endpoint=self.PAYMENT_ENDPOINT,
            json={'data': data, 'payment_id': payment_id}
        )
        return Payment(**response)
