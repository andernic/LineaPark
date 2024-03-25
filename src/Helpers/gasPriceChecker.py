from web3 import Web3
import settings
import time
from src.networks import ethereum_net, linea_net


if settings.gas_price_switch == 1:
    gas_price_limit = settings.gas_price_limit_linea
    net = linea_net
if settings.gas_price_switch == 2:
    gas_price_limit = settings.gas_price_limit_ether
    net = ethereum_net


def check_gas_price_net():
    net.choice_web3()
    gas_price_now = net.get_gas_price_wei()
    settings.gas_price_net = net.web3.from_wei(gas_price_now, 'gWei')


def checking():
    while settings.stop_flag is False:
        check_gas_price_net()
        time.sleep(30)


def check_limit():
    if settings.gas_price_net > gas_price_limit:
        while settings.gas_price_net > gas_price_limit:
            wait_anim('|', settings.gas_price_net)
            time.sleep(0.4)
            wait_anim('/', settings.gas_price_net)
            time.sleep(0.4)
            wait_anim('--', settings.gas_price_net)
            time.sleep(0.4)
            wait_anim('\ ', settings.gas_price_net)
            time.sleep(0.4)


def wait_anim(symbol, gas_price):
    print(f'\rЖдем, цена газа большая: {gas_price} gWei  {symbol} ', end='')
