from src.networks import linea_net
from src.logger import cs_logger
from src.Helpers.txnHelper import get_txn_dict
from src.ABIs import Omnisea_ABI
from src.Quests.questHelper import Quest


class Omnisea(Quest):
    title = 'Минтим Omnisea Nft'
    contract_address = linea_net.web3.to_checksum_address('0xecbEE1a087aA83Db1fCC6C2C5eFFC30BCb191589')
    contract = linea_net.get_contract(contract_address, abi=Omnisea_ABI)
    method_id = '0xf648253d'
    nft_address = '0x0dE240B2A3634fCD72919eB591A7207bDdef03cd'

    def build_txn(self, wallet):
        try:
            value = self.contract.functions.fixedFee().call()
            txn_dict = get_txn_dict(wallet.address, linea_net, value)
            txn = self.contract.functions.mint(
                [wallet.address, self.nft_address, 1, [], 1, b'']
            ).build_transaction(txn_dict)
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (Omnisea/mint: build_txn) {ex.args}')


omnisea = Omnisea()
