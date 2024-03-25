from src.networks import linea_net
from src.logger import cs_logger
from src.Helpers.txnHelper import get_txn_dict
from src.Quests.questHelper import Quest


class LuckyCat(Quest):
    title = 'Минтим LuckyCat'
    contract_address = linea_net.web3.to_checksum_address('0xc577018b3518cD7763D143d7699B280d6E50fdb6')
    method_id = '0x70245bdc'

    def build_txn(self, wallet):
        try:
            txn = get_txn_dict(wallet.address, linea_net)
            txn['to'] = self.contract_address
            txn['data'] = self.method_id
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (LuckyCat/mint: build_txn) {ex.args}')


lucky_cat = LuckyCat()
