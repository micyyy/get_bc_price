import csv
import requests

def get_rate():
    url = 'http://www.taifex.com.tw/data_gov/taifex_open_data.asp?data_name=DailyForeignExchangeRates'

    with requests.Session() as s:
        download = s.get(url)
        
        decoded_content = download.content.decode('Big5')
        
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        
        rate = list(my_list[-2])
        
        return rate[1]

if __name__ == '__main__':
    rate = get_rate()
    print(rate)