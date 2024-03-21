import eth_abi

from src.networks import linea_net
from src.logger import cs_logger
from src.Helpers.txnHelper import get_txn_dict
from src.Quests.questHelper import Quest
from src.Quests.Week1.Nidum.sign import request_ops
from src.ABIs import Nouns_ABI


contract_address = linea_net.web3.to_checksum_address('0x9DF3c2C75a92069B99c73bd386961631F143727C')
contract = linea_net.web3.eth.contract(linea_net.web3.to_checksum_address(contract_address),
                                       abi=Nouns_ABI)


class Nouns(Quest):
    title = 'Минтим Nouns'

    def build_txn(self, wallet):
        try:
            currency = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
            txn_dict = get_txn_dict(wallet.address, linea_net)
            txn = contract.functions.claim(
                wallet.address, 0, 1, currency, 0,
                [[eth_abi.encode(['bytes32'], [b''])], 2 ** 256 - 1, 0, currency], b''
            ).build_transaction(txn_dict)
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (Nouns/mint: build_txn) {ex.args}')


nouns_mint = Nouns()