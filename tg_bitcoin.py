from telegram.ext import Updater, CommandHandler
import requests
import json
import taifex_exchange_rate
import datetime

def output_time(funcname):
    print(datetime.datetime.now(), funcname)

def get_token(botname):
    tgbot = dict()
    with open('bot.json', 'r') as f:
        tgbot = json.load(f)
    return tgbot[botname]

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def help(bot, update):
    msg = u'請參考：\n\n'
    msg += u'/bito\n'
    msg += u'/maicoin\n'
    msg += u'/bfx_iotbtc\n'
    msg += u'/bfx_iotusd\n'
    msg += u'/bfx_iottwd\n'
    msg += u'/iota : 跟/bfx_iottwd 一樣\n'
    msg += u'/bfx_btcusd\n'
    
    update.message.reply_text(msg)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
        
    return False

def get_bito_price(bot, update):
    output_time('get_bito_price')
    URL = 'https://www.bitoex.com/api/v1/get_rate'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    msg = u'BTC/TWD\n\n'
    msg += u'買入：{} TWD\n'.format(price['buy'])
    msg += u'賣出：{} TWD\n'.format(price['sell'])
    
    midprice = (float(price['buy']) + float(price['sell'])) / 2.0
    msg += u'均價：{:.2f} TWD\n'.format(midprice)
    
    update.message.reply_text(msg)
        
def get_maicoin_price(bot, update):
    output_time('get_maicoin_price')
    URL = 'https://api.maicoin.com/v1/prices/twd'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    msg = u'BTC/TWD\n\n'
    msg += u'買入：{} TWD\n'.format(price['buy_price'])
    msg += u'賣出：{} TWD\n'.format(price['sell_price'])
    
    midprice = (float(price['buy_price']) + float(price['sell_price'])) / 2.0
    msg += u'均價：{:.2f} TWD\n'.format(midprice)
    
    update.message.reply_text(msg)

def get_bfx_iotbtc_price(bot, update, args):
    output_time('get_bfx_iotbtc_price')
    URL = 'https://api.bitfinex.com/v1/pubticker/iotbtc'
    res = requests.get(URL)
    price = json.loads(res.text)
	
    times = 1
    if len(args)>0 and is_number(args[0]):
        times = float(args[0])
 	
    last_price = float(price['last_price'])
    total_price = last_price * times
    
    bid = float(price['bid']) * times
    ask = float(price['ask']) * times	    
	
    msg = u'IOTA/BTC\n\n'
    msg += u'單價：{:.6f} BTC\n'.format(last_price)
    msg += u'總價：{:.6f} BTC\n\n'.format(total_price)
    msg += u'買入：{:.6f} BTC\n'.format(bid)
    msg += u'賣出：{:.6f} BTC\n'.format(ask)
    
    update.message.reply_text(msg)

def get_bfx_iotusd_price(bot, update, args):
    output_time('get_bfx_iotusd_price')
    URL = 'https://api.bitfinex.com/v1/pubticker/iotusd'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    times = 1
    if len(args)>0 and is_number(args[0]):
        times = float(args[0])
    
    last_price = float(price['last_price'])
    total_price = last_price * times    
    bid = float(price['bid']) * times
    ask = float(price['ask']) * times	
	
    msg = u'IOTA/USD\n\n'
    msg += u'單價：{:.4f} USD\n'.format(last_price)
    msg += u'總價：{:.4f} USD\n\n'.format(total_price)    
    msg += u'買入：{:.4f} USD\n'.format(bid)
    msg += u'賣出：{:.4f} USD\n'.format(ask)
    
    update.message.reply_text(msg)

def get_bfx_iottwd_price(bot, update, args):
    output_time('get_bfx_iottwd_price')
    URL = 'https://api.bitfinex.com/v1/pubticker/iotusd'
    res = requests.get(URL)
    print(res.text)
    price = json.loads(res.text)
    
    times = 1
    if len(args)>0 and is_number(args[0]):
        times = float(args[0])
    
    rate = taifex_exchange_rate.read_ratefile()
    
    last_price_usd = float(price['last_price'])
    total_price_usd = last_price_usd * times
    total_price_twd = total_price_usd * rate['USD/TWD']
    #bid = float(price['bid']) * rate['USD/TWD'] * times
    #ask = float(price['ask']) * rate['USD/TWD'] * times
    
    msg = u'IOTA/TWD\n\n'
    
    msg += u'單價：{:.4f} USD\n'.format(last_price_usd)
    msg += u'總價：{:.4f} USD\n\n'.format(total_price_usd)
    msg += u'約 {:.0f} TWD\n\n'.format(total_price_twd)
    #msg += u'買入: {}\n'.format(bid)
    #msg += u'賣出: {}\n'.format(ask)
    msg += u'匯率：{}\n\n'.format(rate['USD/TWD'])
    
    update.message.reply_text(msg)

def get_bfx_btcusd_price(bot, update, args):
    output_time('get_bfx_btcusd_price')
    URL = 'https://api.bitfinex.com/v1/pubticker/btcusd'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    times = 1
    if len(args)>0 and is_number(args[0]):
        times = float(args[0])
    
    rate = taifex_exchange_rate.read_ratefile()

    last_price = float(price['last_price'])
    total_price = last_price * times        
    bid = float(price['bid']) * times
    ask = float(price['ask']) * times
    
    msg = u'BTC/USD\n\n'

    msg += u'單價：{:.4f} USD\n'.format(last_price)
    msg += u'總價：{:.4f} USD\n\n'.format(total_price)     
    msg += u'買入：{:.4f} USD\n'.format(bid)
    msg += u'賣出：{:.4f} USD\n'.format(ask)
        
    update.message.reply_text(msg)
    
    
def main():
    updater = Updater(get_token('momo'))
    
    print(updater)
    
    updater.dispatcher.add_handler(CommandHandler('hello', hello))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('bito', get_bito_price))
    updater.dispatcher.add_handler(CommandHandler('maicoin', get_maicoin_price))
    updater.dispatcher.add_handler(CommandHandler('bfx_iotbtc', get_bfx_iotbtc_price, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('bfx_iotusd', get_bfx_iotusd_price, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('bfx_iottwd', get_bfx_iottwd_price, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('iota', get_bfx_iottwd_price, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler('bfx_btcusd', get_bfx_btcusd_price, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()