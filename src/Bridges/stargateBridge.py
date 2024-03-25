import src.ABIs as ABIs
import settings
import datetime
import src.Helpers.helper as helper
import src.Helpers.txnHelper as txnHelper
import random
import src.logger as logger


def get_bridge_fee(wallet, net_src, net_dst):
    try:
        contract = net_src.web3.eth.contract(net_src.web3.to_checksum_address(net_src.router_address),
                                             abi=ABIs.Stargate_router_ABI)
        data = contract.functions.quoteLayerZeroFee(
            net_dst.chain_id_l0, 1, wallet.address, "0x", [0, 0, "0x"]
        ).call()
        return data[0]
    except Exception as ex:
        logger.cs_logger.info(f'Ошибка в (get_bridge_fee): {ex}')


def get_open_balance_eth(wallet, net, gas_price, gas, fee, rem_mult):
    balance_wei = net.get_balance_wei(wallet.address)
    optimism_l1_fee = 0
    open_balance = (balance_wei - (gas_price * gas)) - fee

    if net.name == 'Optimism':
        optimism_l1_fee = int(txnHelper.get_optimism_l1_fee(net, b'') *
                              helper.get_random_value(1.05, 1.10, 2))
        open_balance -= int(optimism_l1_fee * 2.1)

    remains = helper.get_random_value(settings.exc_remains[0], settings.exc_remains[1], settings.rem_digs)
    remains_wei = int(net.web3.to_wei(remains, 'ether') * rem_mult)
    open_balance -= remains_wei

    if open_balance <= 0:
        need_gas = net.web3.from_wei((gas * gas_price) + fee + optimism_l1_fee + remains_wei, 'ether')
        balance = net.web3.from_wei(net.get_balance_wei(wallet.address), 'ether')
        logger.cs_logger.info(f'Недостаточно средств для оплаты транзакции!')
        logger.cs_logger.info(f'Стоимость транзакции: {need_gas}')
        logger.cs_logger.info(f'Баланс кошелька:      {balance}')

    return open_balance


def bridge_eth_build_txn(wallet, net_src, net_dst, value_wei, fee, gas_price, gas):
    try:
        contract = net_src.web3.eth.contract(net_src.web3.to_checksum_address(net_src.router_eth_address),
                                             abi=ABIs.Stargate_router_ETH_ABI)
        nonce = net_src.get_nonce(wallet.address)
        min_amount = value_wei - int(value_wei * settings.slippage)

        dict_txn = {
            'chainId': net_src.chain_id,
            'nonce': nonce,
            'from': wallet.address,
            'value': value_wei + fee,
            'gas': gas,
            'maxFeePerGas': gas_price,
        }

        txn = contract.functions.swapETH(
            net_dst.chain_id_l0, wallet.address, wallet.address, value_wei, min_amount
        ).build_transaction(dict_txn)

        return txn
    except Exception as ex:
        logger.cs_logger.info(f'Ошибка в (bridge_eth_build_txn): {ex}')


def bridge_eth(wallet, net_src, net_dst, all_balance=False):
    try:
        txn_status = False
        rem_mult = 1
        gas_lim = 1
        trying = True
        script_time = datetime.datetime.now().strftime("%d-%m-%y %H:%M")
        logger.cs_logger.info(f'Делаем Stargate бридж ETH из {net_src.name} в {net_dst.name}')

        balance_st_src = net_src.get_balance_wei(wallet.address)
        balance_st_src_eth = net_src.web3.from_wei(balance_st_src, 'ether')

        balance_st_dst = net_dst.get_balance_wei(wallet.address)
        balance_st_dst_eth = net_src.web3.from_wei(balance_st_dst, 'ether')

        while trying is True:
            fee = get_bridge_fee(wallet, net_src, net_dst)
            gas = random.randint(int(net_src.bridge_gas[0] * gas_lim), int(net_src.bridge_gas[1] * gas_lim))

            gp_mult = helper.get_random_value(settings.random_mult[0], settings.random_mult[1], 2)
            gas_price = int(net_src.get_gas_price_wei() * gp_mult)

            open_balance = get_open_balance_eth(wallet, net_src, gas_price, gas, fee, rem_mult)

            if open_balance < 0:
                break

            if all_balance is True:
                bridge_value_wei = open_balance
            else:
                bridge_percent = helper.get_random_value(settings.bridge_sum_percent[0],
                                                         settings.bridge_sum_percent[1],
                                                         settings.bridge_sum_percent_digs)
                bridge_value_eth = helper.trunc_value(
                    net_src.web3.from_wei((open_balance * bridge_percent), 'ether'),
                    settings.bridge_sum_digs[0], settings.bridge_sum_digs[1])

                bridge_value_wei = net_src.web3.to_wei(bridge_value_eth, 'ether')

            txn = bridge_eth_build_txn(wallet, net_src, net_dst, bridge_value_wei, fee, gas_price, gas)
            test = txnHelper.check_estimate_gas(txn, net_src)
            if type(test) is str:
                logger.cs_logger.info(test)
                if 'gas required exceeds allowance' in test:
                    gas_lim += 0.2
                if 'insufficient funds' in test:
                    rem_mult += 0.2
                if 'header not found' in test:
                    helper.delay_sleep(60 * 1, 60 * 3)
                logger.cs_logger.info('Еще одна попытка бриджа')
            else:
                bridge_value_eth = net_src.web3.from_wei(bridge_value_wei, 'ether')
                logger.cs_logger.info(f'Делаем бридж {bridge_value_eth} ETH')
                txn_hash, txn_status = txnHelper.exec_txn(wallet.key, txn, net_src)
                logger.cs_logger.info(f'Hash: {txn_hash}')

                if txn_status is True:
                    trying = False
                    wallet.bridge_sum += bridge_value_eth
                    wallet.wallet_num += 1

                    balance_end_src = net_src.get_balance_wei(wallet.address)
                    balance_end_src_eth = net_src.web3.from_wei(balance_end_src, 'ether')
                    log = logger.LogBridge(wallet.wallet_num, net_src.name, net_dst.name, wallet.address, bridge_value_eth,
                                           txn_hash, balance_st_src_eth, balance_st_dst_eth,
                                           balance_end_src_eth, balance_st_dst_eth)
                    log.write_log(script_time)

                    logger.cs_logger.info('Ожидаем окончание бриджа')
                    balance_end_dst = helper.check_balance_change(wallet, balance_st_dst, net_dst, 60*300)

                    log.balance_to_end = net_src.web3.from_wei(balance_end_dst, 'ether')
                    log.rewrite_log()
                    logger.cs_logger.info('Бридж окончен!')
                else:
                    if 'gas required exceeds allowance' in txn_hash:
                        gas_lim += 0.2
                    if 'insufficient funds for gas' in txn_hash:
                        rem_mult += 0.2
                    if 'header not found' in txn_hash:
                        helper.delay_sleep(60 * 1, 60 * 3)
                    logger.cs_logger.info('Еще одна попытка бриджа')

        return txn_status
    except Exception as ex:
        logger.cs_logger.info(f'Ошибка в (stargateBridge.bridge_eth): {ex}')
        return False
