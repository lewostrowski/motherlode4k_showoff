import requests
import json
import pandas as pd
from math import floor, ceil
from datetime import datetime, timedelta
from .data_manager import DataManager


class GetMarketInfo(DataManager):
    def __init__(self, coin, db):
        super().__init__(db)
        self.coin = coin

    def _request_guardian(self, mode):
        try:
            df = self.query(f'select distinct timestamp from price_{mode}_{self.coin} where coin="{self.coin}"')
            date_max = df['timestamp'].max()
            current_date = datetime.now()

            if mode == 'history':
                date_diff = current_date - datetime.strptime(date_max, '%Y-%m-%d')
                fetch_new_data = True if date_diff.days > 1 else False

            elif mode == 'now':
                date_diff = current_date - datetime.strptime(date_max, '%Y-%m-%d %H:%M:%S')
                fetch_new_data = True if date_diff.seconds > 3600 else False

            return fetch_new_data

        except:
            return True

    def _get_coin_id(self):
        return self.query(f'select cmc_coin_id from coin_info where coin_symbol="{self.coin}"').values[0][0]

    def historical(self):
        if self._request_guardian('history'):
            date_end = datetime.now()

            try:
                in_db = self.query(f'select distinct timestamp from price_history_{self.coin} where coin="{self.coin}"')

                try:
                    date_max = datetime.strptime(in_db['timestamp'].max(), '%Y-%m-%d')
                except:
                    date_max = datetime.strptime(in_db['timestamp'].max(), '%Y-%m-%d %H:%M:%S')

                date_start = date_max - timedelta(days=2)

            except:
                date_start = date_end.replace(month=date_end.month - 2)

            unix_start = floor(datetime.timestamp(date_start))
            unix_end = ceil(datetime.timestamp(date_end))

            base_url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?'
            coin_id = 'id=' + str(self._get_coin_id())
            timestamp = f'timeStart={unix_start}&timeEnd={unix_end}'

            full_url = base_url + coin_id + '&convertId=2781&' + timestamp
            result = requests.get(full_url)
            market_data = json.loads(result.content)

            df = pd.DataFrame()
            quotes = market_data['data']['quotes']
            for i in range(0, len(quotes)):
                row = pd.DataFrame.from_records([quotes[i].get('quote')])
                row['coin'] = self.coin
                row['timestamp'] = pd.to_datetime(row['timestamp'], yearfirst=True).dt.strftime('%Y-%m-%d')
                row = row.assign(average=lambda x: (x['high'] + x['low']) / 2)
                df = pd.concat([df, row])

            try:
                df = df.loc[df['timestamp'].isin(set(in_db['timestamp']) is False)]
            except:
                pass

            self.save_table(df, f'price_history_{self.coin}')

    def last_week(self):
        if self._request_guardian('now'):
            base_url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail/chart?'
            coin_id = 'id=' + str(self._get_coin_id())
            full_url = base_url + coin_id + '&range=7D'

            result = requests.get(full_url)
            market_data = json.loads(result.content)

            df = pd.DataFrame()
            points = market_data['data']['points']
            for date in points:
                values = points[date].get('v')
                row = {
                    'timestamp': [datetime.fromtimestamp(int(date))],  # unix
                    'price_usd': [values[0]],
                    'price_btc': [values[3]],
                    'volume': [values[1]],
                    'coin': [self.coin]
                }
                row = pd.DataFrame(row)
                df = pd.concat([df, row])

            self.save_table(df, f'price_now_{self.coin}', 'replace')
