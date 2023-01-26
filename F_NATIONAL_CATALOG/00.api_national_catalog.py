import json
import sys
import requests
import csv
import datetime
from datetime import date
from requests import RequestException
from json.decoder import JSONDecodeError

base_folder = sys.argv[1]

apikey = sys.argv[2]  # ключ
offset = sys.argv[3]  # смещение

request_headers = {
    "Content-type": "application/json; charset=utf-8"
}

file = open(base_folder + 'national_catalog.csv', 'w', newline='')
writer = csv.writer(file, delimiter=';')

try:
    yesterday = date.today() - datetime.timedelta(days=1)
    url = 'https://апи.национальный-каталог.рф/v4/product-list?apikey={apikey}&limit=1000&offset={offset}&to_date={yesterday} 00:00:00'\
        .format(apikey=apikey, offset=offset, yesterday=yesterday)
    response = requests.get(url, headers=request_headers)
    length = int(json.loads(response.text)['result']['total'])

    while length > 0:
        url = 'https://апи.национальный-каталог.рф/v4/product-list?apikey={apikey}&limit=1000&offset={offset}&to_date={yesterday} 00:00:00'\
            .format(apikey=apikey, offset=offset, yesterday=yesterday)
        response = requests.get(url, headers=request_headers)
        result = json.loads(response.text)['result']['goods']

        for good in result:
            gtin = good['gtin']
            good_name = good['good_name']
            good_status = good['good_status']
            to_date = good['updated_date']

            tnved = ''
            tnved_url = 'https://апи.национальный-каталог.рф/v3/feed-product?apikey={apikey}&gtin={gtin}'\
                .format(apikey=apikey, gtin=str(gtin))
            tnved_response = requests.get(tnved_url, headers=request_headers)
            if str(tnved_response.status_code)[0] in ('4', '5'):
                raise Exception(gtin)
            dicts = json.loads(tnved_response.text)['result'][0]['good_attrs']
            for d in dicts:
                if d['attr_name'] == 'Код ТНВЭД':
                    tnved = d['attr_value']

            writer.writerow([
                gtin,
                good_name,
                tnved,
                good_status,
                to_date
            ])

        offset += 1000
        length -= 1000

except RequestException:
    print('RequestException')
except JSONDecodeError:
    print('JSONDecodeError')
except Exception as e:
    print('Wrong gtin:', e)
finally:
    file.close()
