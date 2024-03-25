import settings
import eth_abi
import math
import time
from src.networks import linea_net
from src.Swaps.tokens import contract_USDC, wETH_token, USDC_token
import src.logger as logger
from src.ABIs import iZUMi_Swap_ABI
from src.Helpers.txnHelper import check_estimate_gas, get_txn_dict, exec_txn, approve_amount
from src.Helpers.helper import get_curr_time, delay_sleep, get_price


swap_contract_address = '0x032b241De86a8660f1Ae0691a4760B426EA246d7'

contract_swap = linea_net.get_contract(linea_net.web3.to_checksum_address(swap_contract_address), abi=iZUMi_Swap_ABI)
pool_address = '0x0A3BB08b3a15A19b4De82F8AcFc862606FB69A2D'


def build_txn_swap_in(wallet, value_eth):
    try:
        contract = contract_swap
        slippage = settings.slippage_USDC
        price = get_price('ETH')

        value_wei = linea_net.web3.to_wei(value_eth, 'ether')
        token_out_wei = int(float(value_eth) * price * (10 ** 6))
        min_output = int(token_out_wei * (1 - slippage))

        dict_transaction = get_txn_dict(wallet.address, linea_net, value_wei)

        deadline = math.ceil(time.time()) + 30 * 60
        usdc_address = USDC_token.address
        weth_address = wETH_token.address

        path_str = (weth_address.removeprefix('0x') + '000bb8' + usdc_address.removeprefix('0x'))
        path = bytes.fromhex(path_str)

        contract_code = eth_abi.encode(
            ['bytes', 'address',  'uint256', 'uint256', 'uint256'],
            [path, wallet.address, value_wei, min_output, deadline]
        )
        txn_code_hex = '75ceafe6' + '0000000000000000000000000000000000000000000000000000000000000020' + contract_code.hex()
        txn_code = bytes.fromhex(txn_code_hex)
        ref = bytes.fromhex('12210e8a')

        txn_swap = contract.functions.multicall(
            [txn_code, ref]
        ).build_transaction(dict_transaction)

        return txn_swap
    except Exception as ex:
        logger.cs_logger.info(f'Ошибка в (iZUMiSwapUSDC: build_txn_swap_in) {ex.args}')


def build_txn_swap_out(wallet, value_token_wei):
    try:
        slippage = settings.slippage_USDC
        price = get_price('ETH')
        contract = contract_swap

        ether_out = value_token_wei / price / 10 ** 6
        min_output = int(linea_net.web3.to_wei(ether_out * (1 - slippage), 'ether'))

        dict_transaction = get_txn_dict(wallet.address, linea_net)

        zero_address = '0x0000000000000000000000000000000000000000'
        deadline = math.ceil(time.time()) + 20 * 60
        usdc_address = USDC_token.address
        weth_address = wETH_token.address

        path_str = (usdc_address.removeprefix('0x') + '000bb8' + weth_address.removeprefix('0x'))
        path = bytes.fromhex(path_str)

        contract_code = eth_abi.encode(
            ['bytes', 'address', 'uint256', 'uint256', 'uint256'],
            [path, zero_address, value_token_wei, min_output, deadline]
        )
        txn_code_hex = '75ceafe6' + '0000000000000000000000000000000000000000000000000000000000000020' + contract_code.hex()
        txn_code = bytes.fromhex(txn_code_hex)

        address_code = eth_abi.encode(['uint256', 'address'], [0, wallet.address])
        ref = bytes.fromhex('49404b7c' + address_code.hex())

        txn_swap = contract.functions.multicall(
            [txn_code, ref]
        ).build_transaction(dict_transaction)

        return txn_swap
    except Exception as ex:
        logger.cs_logger.info(f'Ошибка в (iZUMiSwapUSDC: build_txn_swap_out) {ex.args}')


def swap_eth_to_usdc(wallet, swap_value_eth):
    try:
        key = wallet.key
        address = wallet.address
        script_time = get_curr_time()

        logger.cs_logger.info(f'#   Свапаем {swap_value_eth} ETH через iZUMiSwap')
        balance_start_eth = linea_net.web3.from_wei(linea_net.get_balance_wei(address), 'ether')
        balance_start_token = contract_USDC.functions.balanceOf(address).call() / 10 ** 6

        txn_swap = build_txn_swap_in(wallet, swap_value_eth)
        estimate_gas = check_estimate_gas(txn_swap, linea_net)
        if type(estimate_gas) is str:
            logger.cs_logger.info(f'{estimate_gas}')
            return False
        else:
            txn_swap['gas'] = estimate_gas
            txn_hash, txn_status = exec_txn(key, txn_swap, linea_net)
            logger.cs_logger.info(f'Hash: {txn_hash}')
            delay_sleep(settings.txn_delay[0], settings.txn_delay[1])

            wallet.txn_num += 1
            balance_end_eth = linea_net.web3.from_wei(linea_net.get_balance_wei(address), 'ether')
            balance_end_token = contract_USDC.functions.balanceOf(address).call() / 10 ** 6

            log = logger.LogSwap(wallet.wallet_num, wallet.txn_num, address, 'iZUMi', swap_value_eth,
                                 txn_hash, balance_start_eth, balance_end_eth, balance_start_token, balance_end_token)
            log.write_log(1, script_time)
            return True
    except Exception as ex:
        logger.cs_logger.info(f'Ошибка в (iZUMiSwapUSDC: swap_ETH_to_USDC), {ex.args}')
        return False


def swap_usdc_to_eth(wallet, value_token_wei):
    try:
        key = wallet.key
        address = wallet.address
        script_time = get_curr_time()
        if value_token_wei != 0:
            logger.cs_logger.info(f'#   Свапаем {value_token_wei / 10 ** 6} USDC через iZUMiSwap')
            balance_start_eth = linea_net.web3.from_wei(linea_net.get_balance_wei(address), 'ether')
            balance_start_token = contract_USDC.functions.balanceOf(address).call() / 10 ** 6

            approve_amount(key, address, swap_contract_address, contract_USDC, linea_net, value_token_wei)
            txn_swap = build_txn_swap_out(wallet, value_token_wei)
            estimate_gas = check_estimate_gas(txn_swap, linea_net)
            if type(estimate_gas) is str:
                logger.cs_logger.info(f'{estimate_gas}')
                return False
            else:
                txn_swap['gas'] = estimate_gas
                txn_hash, txn_status = exec_txn(key, txn_swap, linea_net)
                logger.cs_logger.info(f'Hash: {txn_hash}')
                delay_sleep(settings.txn_delay[0], settings.txn_delay[1])

                wallet.txn_num += 1
                balance_end_eth = linea_net.web3.from_wei(linea_net.get_balance_wei(address), 'ether')
                balance_end_token = contract_USDC.functions.balanceOf(address).call() / 10 ** 6
                log = logger.LogSwap(wallet.wallet_num, wallet.txn_num, address, 'iZUMi',
                                     value_token_wei / 10 ** 6, txn_hash,
                                     balance_start_eth, balance_end_eth, balance_start_token, balance_end_token)
                log.write_log(2, script_time)
                return True
        else:
            logger.cs_logger.info(f'Баланс USDC равен 0')
            return True
    except Exception as ex:
        logger.cs_logger.info(f'Ошибка в (iZUMiSwapUSDC: swap_USDC_to_ETH), {ex.args}')
        return False
