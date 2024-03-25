from src.networks import linea_net
from src.logger import cs_logger
from src.Helpers.txnHelper import get_txn_dict
from src.Quests.questHelper import Quest


class BitAvatar(Quest):
    title = 'Делаем Check In в BitAvatar'
    contract_address = linea_net.web3.to_checksum_address('0x37D4BFc8c583d297A0740D734B271eAc9a88aDe4')
    method_id = '0x183ff085'

    def build_txn(self, wallet):
        try:
            txn = get_txn_dict(wallet.address, linea_net)
            txn['to'] = self.contract_address
            txn['data'] = self.method_id
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (BitAvatar/checkIn: build_txn) {ex.args}')


bit_avatar = BitAvatar()
