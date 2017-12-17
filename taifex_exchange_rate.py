import csv
import requests
import json

def get_rate():
    url = 'http://www.taifex.com.tw/data_gov/taifex_open_data.asp?data_name=DailyForeignExchangeRates'

    with requests.Session() as s:
        download = s.get(url)
        
        decoded_content = download.content.decode('Big5')
        
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        
        rate = list(my_list[-2])
        
        return rate

def write_ratefile(rate):
    jdict = dict()
    jdict['DATE'] = rate[0]
    jdict['USD/TWD'] = float(rate[1])
    
    with open('rate.json', 'w') as f:
        json.dump(jdict, f)

def read_ratefile(): 
    jdict = dict()
    
    with open('rate.json', 'r') as f:
        jdict = json.load(f)
    
    return jdict

if __name__ == '__main__':
    rate = get_rate()
    write_ratefile(rate)
    #jdict = read_ratefile()
    #print(jdict)
