from src.Helpers.txnHelper import exec_txn, check_estimate_gas, get_txn_dict, approve_amount
from src.Quests.questHelper import Quest
from src.networks import linea_net
from src.logger import cs_logger
from src.Helpers.helper import delay_sleep, get_random_value
import settings
import eth_abi
from src.Swaps.tokens import USDC_token, contract_USDC, TROB_token
from src.Swaps.iZUMiSwapUSDC import swap_eth_to_usdc
from src.Swaps.swapHelper import get_eth_value
from src.Helpers.txnChecker import get_txn_list_from_address, check_txn_existence


class YooldoSwap(Quest):
    title = 'Делаем Yooldo свап USDC на TROB'
    contract_address = linea_net.web3.to_checksum_address('0x6c5f2ce8ab5d6341ba9563c82ca7fa6fa0c35161')
    method_id = '0x0c0a7630'

    def build_txn_swap(self, wallet, usdc_value):
        try:
            txn = get_txn_dict(wallet.address, linea_net)
            txn['to'] = self.contract_address
            txn['data'] = self.method_id + eth_abi.encode(['address', 'address', 'uint256'],
                                                          [USDC_token.address, TROB_token.address, usdc_value]).hex()
            txn['gas'] = 200000
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (Yooldo/trobSwap: build_txn) {ex.args}')

    def run_quest(self, wallet):
        try:
            cs_logger.info(f'{self.title}')
            if settings.check_txn_existence_enable == 1:
                txn_list = get_txn_list_from_address(wallet.address, 2000)
                txn_check = check_txn_existence(wallet.address, txn_list, self.contract_address, self.method_id)
                if txn_check is not None:
                    cs_logger.info(f'Данная транзакция уже выполнялась')
                    return True
            usdc_balance = contract_USDC.functions.balanceOf(wallet.address).call()
            if usdc_balance < int(0.01 * 10 ** 6):
                eth_value = get_eth_value(settings.usdc_limits)
                swap_eth_to_usdc(wallet, eth_value)
                usdc_swap_balance = contract_USDC.functions.balanceOf(wallet.address).call()
            else:
                usdc_swap_balance = int(get_random_value(settings.usdc_limits[0], settings.usdc_limits[1], 2) * 10 ** 6)
                if usdc_balance < usdc_swap_balance:
                    usdc_swap_balance = usdc_balance
            usdc_value = (usdc_swap_balance // 10 ** 4) * 10 ** 4
            if usdc_value <= 9999:
                return False
            cs_logger.info(f'Сумма свапа {(usdc_value / 10 ** 6)} USDC')
            approve_amount(wallet.key, wallet.address, self.contract_address, contract_USDC, linea_net,
                           usdc_value, usdc_value)
            txn = self.build_txn_swap(wallet, usdc_value)
            estimate_gas = check_estimate_gas(txn, linea_net)
            if type(estimate_gas) is str:
                cs_logger.info(f'{estimate_gas}')
                return False
            else:
                txn['gas'] = estimate_gas
                txn_hash, txn_status = exec_txn(wallet.key, txn, linea_net)
                cs_logger.info(f'Hash: {txn_hash}')

                wallet.txn_num += 1
                delay_sleep(settings.txn_delay[0], settings.txn_delay[1])
                return True

        except Exception as ex:
            cs_logger.info(f'Ошибка в (Yooldo/trobSwap: run_quest) {ex.args}')


yooldo_trob_swap = YooldoSwap()
