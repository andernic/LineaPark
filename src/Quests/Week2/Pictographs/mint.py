from src.networks import linea_net
from src.logger import cs_logger
from src.Helpers.txnHelper import get_txn_dict
from src.ABIs import Pictographs_ABI
from src.Quests.questHelper import Quest


class PictographsMint(Quest):
    title = 'Минтим Pictographs Nft'
    contract_address = linea_net.web3.to_checksum_address('0xb18b7847072117AE863f71F9473D555d601Eb537')
    contract = linea_net.get_contract(contract_address, abi=Pictographs_ABI)
    method_id = '0x14f710fe'

    def build_txn(self, wallet):
        try:
            value = self.contract.functions.price().call()
            txn = get_txn_dict(wallet.address, linea_net, value)
            txn['to'] = self.contract_address
            txn['data'] = self.method_id
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (Pictographs/mint: build_txn) {ex.args}')


class PictographsStake(Quest):
    title = 'Стейкаем Pictographs Nft'
    contract_address = linea_net.web3.to_checksum_address('0xb18b7847072117AE863f71F9473D555d601Eb537')
    contract = linea_net.get_contract(contract_address, abi=Pictographs_ABI)
    method_id = '0xa694fc3a'

    def build_txn(self, wallet):
        try:
            nft_id = self.contract.functions.tokenOfOwnerByIndex(wallet.address, 0).call()
            txn_dict = get_txn_dict(wallet.address, linea_net)
            txn = self.contract.functions.stake(
                nft_id
            ).build_transaction(txn_dict)
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (Pictographs/stake: build_txn_stake) {ex.args}')


pictographs_mint = PictographsMint()
pictographs_stake = PictographsStake()
