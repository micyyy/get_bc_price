from telegram.ext import Updater, CommandHandler
import requests
import json
import getrate

TOKEN = '285343903:AAEwfcjZ7Qsj5ngj3nZC8yCbTmJM74Zf4BQ'

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def get_bito_price(bot, update):
    URL = 'https://www.bitoex.com/api/v1/get_rate'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    msg = 'BTC/TWD\n\n'
    #msg = 'TimeStamp:{}\n\n'.format(price['timestamp'])
    msg += 'Buy: {}\n'.format(price['buy'])
    msg += 'Sell: {}\n'.format(price['sell'])
    
    update.message.reply_text(msg)
        
def get_maicoin_price(bot, update):
    URL = 'https://api.maicoin.com/v1/prices/twd'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    msg = 'BTC/TWD\n\n'
    #msg = 'TimeStamp:{}\n\n'.format(price['timestamp'])
    msg += 'Buy: {}\n'.format(price['buy_price'])
    msg += 'Sell: {}\n'.format(price['sell_price'])
    
    update.message.reply_text(msg)

def get_bfx_iotbtc_price(bot, update):
    URL = 'https://api.bitfinex.com/v1/pubticker/iotbtc'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    msg = 'IOTA/BTC\n\n'
    #msg = 'TimeStamp:{}\n\n'.format(price['timestamp'])
    msg += 'Buy: {}\n'.format(price['bid'])
    msg += 'Sell: {}\n'.format(price['ask'])
    
    update.message.reply_text(msg)

def get_bfx_iotusd_price(bot, update):
    URL = 'https://api.bitfinex.com/v1/pubticker/iotusd'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    msg = 'IOTA/USD\n\n'
    #msg = 'TimeStamp:{}\n\n'.format(price['timestamp'])
    msg += 'Buy: {}\n'.format(price['bid'])
    msg += 'Sell: {}\n'.format(price['ask'])
    
    update.message.reply_text(msg)

def get_bfx_iottwd_price(bot, update, args):
    URL = 'https://api.bitfinex.com/v1/pubticker/iotusd'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    if len(args) <= 0:
        times = 1
    else:
        times = float(args[0])
    
    currency = 29.992
    bid = float(price['bid']) * currency * times
    ask = float(price['ask']) * currency * times
    
    #print(times, currency, bid, ask)
    
    msg = 'IOTA/TWD\n\n'
    msg += 'Buy: {}\n'.format(bid)
    msg += 'Sell: {}\n'.format(ask)
    msg += 'rate: {}\n'.format(currency)
    
    update.message.reply_text(msg)
    
def main():
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('bito', get_bito_price))
    updater.dispatcher.add_handler(CommandHandler('maicoin', get_maicoin_price))
    updater.dispatcher.add_handler(CommandHandler('bfx_iotbtc', get_bfx_iotbtc_price))
    updater.dispatcher.add_handler(CommandHandler('bfx_iotusd', get_bfx_iotusd_price))
    updater.dispatcher.add_handler(CommandHandler('bfx_iottwd', get_bfx_iottwd_price, pass_args=True))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()