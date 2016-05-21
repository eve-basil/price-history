import datetime

date_time_1999 = datetime.datetime.utcfromtimestamp(946684799)
date_time_2001 = datetime.datetime.utcfromtimestamp(978310923)
date_time_2012_may = datetime.datetime.utcfromtimestamp(1336197305)
date_time_2012_jun = datetime.datetime.utcfromtimestamp(1339869960)

fixtures = [{'type_id': 100, 'system_id': 22, 'buy_avg': 45.12,
             'buy_min': 39.83, 'buy_max': 51.36, 'buy_stddev': 2.93,
             'buy_median': 47.04, 'sell_avg': 96.82, 'sell_min': 72.44,
             'sell_max': 142.25, 'sell_stddev': 3.07, 'sell_median': 98.36,
             'recorded_at': date_time_1999, 'updated_at': date_time_1999},
            {'type_id': 100, 'system_id': 22, 'buy_avg': 46.46,
             'buy_min': 40.03, 'buy_max': 54.82, 'buy_stddev': 2.19,
             'buy_median': 41.89, 'sell_avg': 98.21, 'sell_min': 74.30,
             'sell_max': 149.81, 'sell_stddev': 3.32, 'sell_median': 94.15,
             'recorded_at': date_time_2001, 'updated_at': date_time_2001},
            {'type_id': 102, 'system_id': 22, 'buy_avg': 7.07,
             'buy_min': 5.98, 'buy_max': 9.1, 'buy_stddev': 0.11,
             'buy_median': 7.50, 'sell_avg': 9.44, 'sell_min': 8.95,
             'sell_max': 10.17, 'sell_stddev': 0.20, 'sell_median': 9.84,
             'recorded_at': date_time_2001, 'updated_at': date_time_2001}]
