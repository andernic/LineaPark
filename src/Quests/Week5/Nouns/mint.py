import eth_abi
from src.networks import linea_net
from src.logger import cs_logger
from src.Helpers.txnHelper import get_txn_dict
from src.Quests.questHelper import Quest
from src.ABIs import Nouns_ABI


class Nouns(Quest):
    title = 'Минтим Nouns'
    contract_address = linea_net.web3.to_checksum_address('0x9DF3c2C75a92069B99c73bd386961631F143727C')
    method_id = '0x57bc3d78'
    contract = linea_net.get_contract(contract_address, abi=Nouns_ABI)
    currency = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

    def build_txn(self, wallet):
        try:
            txn_dict = get_txn_dict(wallet.address, linea_net)
            txn = self.contract.functions.claim(
                wallet.address, 0, 1, self.currency, 0,
                [[eth_abi.encode(['bytes32'], [b''])], 2 ** 256 - 1, 0, self.currency], b''
            ).build_transaction(txn_dict)
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (Nouns/mint: build_txn) {ex.args}')


nouns_mint = Nouns()
