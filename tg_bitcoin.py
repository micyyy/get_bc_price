from telegram.ext import Updater, CommandHandler
import requests
import json
import taifex_exchange_rate

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
    
    update.message.reply_text(msg)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
        
    return False

def get_bito_price(bot, update):
    URL = 'https://www.bitoex.com/api/v1/get_rate'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    msg = u'BTC/TWD\n\n'
    msg += u'買入: {}\n'.format(price['buy'])
    msg += u'賣出: {}\n'.format(price['sell'])
    
    update.message.reply_text(msg)
        
def get_maicoin_price(bot, update):
    URL = 'https://api.maicoin.com/v1/prices/twd'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    msg = u'BTC/TWD\n\n'
    msg += u'買入: {}\n'.format(price['buy_price'])
    msg += u'賣出: {}\n'.format(price['sell_price'])
    
    update.message.reply_text(msg)

def get_bfx_iotbtc_price(bot, update, args):
    URL = 'https://api.bitfinex.com/v1/pubticker/iotbtc'
    res = requests.get(URL)
    price = json.loads(res.text)
	
    times = 1
    if len(args)>0 and is_number(args[0]):
        times = float(args[0])
 	
    bid = float(price['bid']) * times
    ask = float(price['ask']) * times	    
	
    msg = u'IOTA/BTC\n\n'
    msg += u'買入: {}\n'.format(bid)
    msg += u'賣出: {}\n'.format(ask)
    
    update.message.reply_text(msg)

def get_bfx_iotusd_price(bot, update, args):
    URL = 'https://api.bitfinex.com/v1/pubticker/iotusd'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    times = 1
    if len(args)>0 and is_number(args[0]):
        times = float(args[0])
    
    bid = float(price['bid']) * times
    ask = float(price['ask']) * times	
	
    msg = u'IOTA/USD\n\n'
    msg += u'買入: {}\n'.format(bid)
    msg += u'賣出: {}\n'.format(ask)
    
    update.message.reply_text(msg)

def get_bfx_iottwd_price(bot, update, args):
    URL = 'https://api.bitfinex.com/v1/pubticker/iotusd'
    res = requests.get(URL)
    price = json.loads(res.text)
    
    times = 1
    if len(args)>0 and is_number(args[0]):
        times = float(args[0])
    
    rate = taifex_exchange_rate.read_ratefile()
    bid = float(price['bid']) * rate['USD/TWD'] * times
    ask = float(price['ask']) * rate['USD/TWD'] * times
    
    msg = u'IOTA/TWD\n\n'
    msg += u'買入: {}\n'.format(bid)
    msg += u'賣出: {}\n'.format(ask)
    msg += u'匯率: {}\n'.format(rate['USD/TWD'])
    
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

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()