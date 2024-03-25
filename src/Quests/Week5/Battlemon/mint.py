from src.networks import linea_net
from src.logger import cs_logger
from src.Helpers.txnHelper import get_txn_dict
from src.Quests.questHelper import Quest


class Battlemon(Quest):
    title = 'Минтим Battlemon'
    contract_address = linea_net.web3.to_checksum_address('0x578705C60609C9f02d8B7c1d83825E2F031e35AA')
    method_id = '0x6871ee40'

    def build_txn(self, wallet):
        try:
            txn = get_txn_dict(wallet.address, linea_net)
            txn['to'] = self.contract_address
            txn['data'] = self.method_id
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (Battlemon/mint: build_txn) {ex.args}')


battlemon = Battlemon()
