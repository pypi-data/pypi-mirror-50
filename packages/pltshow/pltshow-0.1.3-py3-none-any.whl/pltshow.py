# -*- coding: utf-8 -*-
import requests
import pandas

class Client:
    def __init__(self, username = '', password = ''):
        self.session = requests.Session()
        r = self.session.post('http://login.pltshow.com/api/login', json={'username': username, 'password': password})
        if r.status_code < 300:
            r = self.session.get('http://pltshow.com')
        if r.status_code > 300:
            raise Exception('login failed')

    def show(self, chart, df):
        result = self.session.patch('%s/api/charts?name=%s' % ('http://pltshow.com', chart), json={'chart_data': df.to_csv()})
        if result.status_code > 300:
            raise Exception(result.text)
