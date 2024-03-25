from src.networks import linea_net
from src.ABIs import ERC20_ABI
from web3 import Web3


class Token(object):
    def __init__(self, token_name, token_address):
        self.name = token_name
        self.address = token_address


USDC_token = Token(
    'USDC',
    '0x176211869cA2b568f2A7D4EE941E073a821EE1ff'
)
contract_USDC = linea_net.get_contract(Web3.to_checksum_address(USDC_token.address), abi=ERC20_ABI)

wETH_token = Token(
    'wETH',
    '0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f'
)
contract_wETH = linea_net.get_contract(Web3.to_checksum_address(wETH_token.address), abi=ERC20_ABI)

TROB_token = Token(
    'TROB',
    '0xc04513e23Efe2Cbfcb633D1994304dDb68DF7dCd'
)
