import requests
from src.POH.Trusta.sign import sign_in_message
from src.networks import linea_net
from src.logger import LogProof, cs_logger
from src.Helpers.txnHelper import get_txn_dict, check_estimate_gas, exec_txn
import settings
from src.Helpers.helper import delay_sleep


def get_attest_data_humanity(token_auth):
    url = 'https://mp.trustalabs.ai/accounts/attest_calldata?attest_type=humanity'
    headers = {'Authorization': f'TOKEN {token_auth}', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        res = [r.json()]
        if res[0]['code'] == 0:
            txn_calldata = res[0]['data']
            return txn_calldata


def build_txn(wallet, txn_calldata):
    try:
        txn_data = txn_calldata['calldata']['data']
        value = txn_calldata['calldata']['value']
        txn = get_txn_dict(wallet.address, linea_net, value)
        txn['to'] = linea_net.web3.to_checksum_address('0xb86b3e16b6b960fd822849fd4b4861d73805879b')
        txn['data'] = txn_data
        return txn
    except Exception as ex:
        cs_logger.info(f'Ошибка в (Trusta/attestA: build_txn) {ex.args}')


def attest_a(wallet):
    try:
        cs_logger.info(f'Делаем аттестацию Trusta Group A')
        token_auth = sign_in_message(wallet)
        txn_calldata = get_attest_data_humanity(token_auth)
        score = txn_calldata['message']['score']
        if settings.trusta_a_replace_enable == 0:
            method = txn_calldata['calldata']['data'][0:10]
            if method == '0xecdbb4fd':
                cs_logger.info(f'Аттестация уже пройдена, замена отключена, скипаем')
                log = LogProof(wallet.index, wallet.address, 'Trusta A', 'Уже выполнена', score)
                log.write_log()
                return True
        if score != -1:
            cs_logger.info(f'Score кошелька равен {score}, аттестация не выполняется')
            log = LogProof(wallet.index, wallet.address, 'Trusta A', 'Не выполнялась', score)
            log.write_log()
            return False
        txn = build_txn(wallet, txn_calldata)
        estimate_gas = check_estimate_gas(txn, linea_net)
        if type(estimate_gas) is str:
            cs_logger.info(f'{estimate_gas}')
            return False
        else:
            txn['gas'] = estimate_gas
            txn_hash, txn_status = exec_txn(wallet.key, txn, linea_net)
            cs_logger.info(f'Hash: {txn_hash}')
            wallet.txn_num += 1

            log = LogProof(wallet.index, wallet.address, 'Trusta A', txn_hash, score)
            log.write_log()

            delay_sleep(settings.txn_delay[0], settings.txn_delay[1])
            return True

    except Exception as ex:
        cs_logger.info(f'Ошибка в (Trusta/attestA: attest_a) {ex.args}')


def score_check(wallet):
    try:
        cs_logger.info(f'Проверяем баллы для аттестации Trusta Group A')
        token_auth = sign_in_message(wallet)
        txn_calldata = get_attest_data_humanity(token_auth)
        score = txn_calldata['message']['score']
        log = LogProof(wallet.index, wallet.address, 'Trusta A', 'Предварительная оценка', score)
        log.write_log()
    except Exception as ex:
        cs_logger.info(f'Ошибка в (Trusta/attestA: score_check) {ex.args}')
