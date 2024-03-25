import eth_abi
from src.networks import linea_net
from src.logger import cs_logger
from src.Helpers.txnHelper import get_txn_dict
from src.Quests.questHelper import Quest


class AbyssWorld(Quest):
    title = 'Минтим Abyss World Nft'
    contract_address = linea_net.web3.to_checksum_address('0x66Ccc220543B6832f93c2082EDD7be19c21dF6C0')
    method_id = '0xefef39a1'
    txn_value = linea_net.web3.to_wei(0.0001, 'ether')

    def build_txn(self, wallet):
        try:
            txn = get_txn_dict(wallet.address, linea_net, self.txn_value)
            txn['to'] = self.contract_address
            txn['data'] = self.method_id + eth_abi.encode(['uint256'], [1]).hex()
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (AbyssWorld/mint: build_txn) {ex.args}')


abyss_world = AbyssWorld()
