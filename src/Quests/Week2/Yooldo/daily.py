from src.Helpers.txnHelper import get_txn_dict
from src.networks import linea_net
from src.logger import cs_logger
from src.Quests.questHelper import Quest


class YooldoDaily(Quest):
    title = 'Делаем Daily Stand-Up'
    contract_address = linea_net.web3.to_checksum_address('0x63ce21bd9af8cc603322cb025f26db567de8102b')
    method_id = '0xfb89f3b1'
    txn_value = linea_net.web3.to_wei(0.0001, 'ether')

    def build_txn(self, wallet):
        try:
            txn = get_txn_dict(wallet.address, linea_net, self.txn_value)
            txn['to'] = self.contract_address
            txn['data'] = self.method_id
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (Yooldo/daily: build_txn) {ex.args}')


yooldo_daily = YooldoDaily()
