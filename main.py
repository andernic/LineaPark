import src.Helpers.helper as helper
import src.networks as nt
import settings
import random
import src.logger as logger
import src.Exchanges.okxOperations as okxOp
import src.Helpers.gasPriceChecker as gPC
import src.Helpers.userHelper as userHelper
from threading import Thread
import src.Bridges.stargateBridge as stargateBridge
from src.Swaps.swapOps import swap_usdc_remains
from src.Quests.questHelper import get_modules_list
from src.Quests.questOps import quest_ops
from src.POH.proofOps import proof_op


logger.create_xml()
settings.last_row = logger.get_last_row_overall('Overall')
settings.last_row_poh = logger.get_last_row_overall('POH attestations')
wallets = helper.read_wallets()
net_src = nt.arbitrum_net


def main():
    op = 0
    if settings.wallet_mode == 2:
        random.shuffle(wallets)
    for wallet in wallets:
        op += 1
        balance_st = nt.linea_net.web3.from_wei(nt.linea_net.get_balance_wei(wallet.address), 'ether')
        logger.cs_logger.info(f'')
        logger.cs_logger.info(
            f'№ {op} ({wallet.wallet_num})  Адрес: {wallet.address}  Биржа: {wallet.exchange_address}')
        script_time = helper.get_curr_time()

        # Вывод с биржи
        if settings.exc_withdraw == 1:
            rc = 1
            while int(rc) > 0:
                res, rc = okxOp.withdraw(wallet, nt.linea_net)
                if int(rc) > 0:
                    logger.cs_logger.info(f'{res}')
                    logger.cs_logger.info(f'Доп попытка вывода')

        balance_end = nt.linea_net.web3.from_wei(nt.linea_net.get_balance_wei(wallet.address), 'ether')
        nonce = nt.linea_net.get_nonce(wallet.address)
        logger.write_overall(wallet, balance_st, balance_end, script_time, nonce)

        modules = get_modules_list()
        quest_ops(wallet, modules)

        # Свапаем остатки USDC на эфир после всех операций, если нужно
        gPC.check_limit()
        swap_usdc_remains(wallet)

        # Транзакции POH
        proof_op(wallet)

        balance_end = nt.linea_net.web3.from_wei(nt.linea_net.get_balance_wei(wallet.address), 'ether')
        nonce = nt.linea_net.get_nonce(wallet.address)
        logger.write_overall(wallet, balance_st, balance_end, script_time, nonce)

        # Депозит на биржу или бридж
        if settings.exc_deposit == 1:
            if settings.switch_bridge_exc == 0:
                # Трансфер средств на адрес биржи в Linea
                okxOp.deposit(wallet, nt.linea_net)
                balance_end = nt.linea_net.web3.from_wei(nt.linea_net.get_balance_wei(wallet.address), 'ether')
                nonce = nt.linea_net.get_nonce(wallet.address)
                logger.rewrite_overall(wallet, balance_end, nonce)

            if settings.switch_bridge_exc == 1:
                # Делаем бридж в Arbitrum или Optimism
                net_src = helper.choice_net(nt.networks, random.choice(settings.net_bridge))
                result = stargateBridge.bridge_eth(wallet, nt.linea_net, net_src, True)

                if result is True:
                    balance_end = nt.linea_net.web3.from_wei(nt.linea_net.get_balance_wei(wallet.address), 'ether')
                    nonce = nt.linea_net.get_nonce(wallet.address)
                    logger.rewrite_overall(wallet, balance_end, nonce)
                    # Трансфер средств на адрес биржи в Arbitrum или Optimism
                    okxOp.deposit(wallet, net_src)
                    logger.rewrite_overall(wallet, balance_end, nonce)
                else:
                    logger.cs_logger.info(f'Бридж не удался')

        helper.delay_sleep(settings.wallet_delay[0], settings.wallet_delay[1])


#'''
logger.cs_logger.info(f'Найдено кошельков: {len(wallets)}')
userHelper.get_info(wallets)
if settings.start_flag is True:
    gPC.check_gas_price_net()
    check_thread = Thread(target=gPC.checking, args=(), daemon=True)
    main_thread = Thread(target=main, args=())
    check_thread.start()
    main_thread.start()
    main_thread.join()
    logger.cs_logger.info(f'Нажмите Enter для выхода')
    input()
    logger.cs_logger.info(f'Выход...')
#'''
