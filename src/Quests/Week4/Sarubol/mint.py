import eth_abi
from src.networks import linea_net
from src.logger import cs_logger
from src.Helpers.txnHelper import get_txn_dict
from src.Quests.questHelper import Quest


class Sarubol(Quest):
    title = 'Минтим Tanukiverse для Sarubol'
    contract_address = linea_net.web3.to_checksum_address('0x47874ff0BEf601D180a8A653A912EBbE03739a1a')
    method_id = '0xefef39a1'
    txn_value = linea_net.web3.to_wei(0.0001, 'ether')

    def build_txn(self, wallet):
        try:
            txn = get_txn_dict(wallet.address, linea_net, self.txn_value)
            txn['to'] = self.contract_address
            txn['data'] = self.method_id + eth_abi.encode(['uint256'], [1]).hex()
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (Sarubol/mint: build_txn) {ex.args}')


sarubol_mint = Sarubol()
