import requests
from src.POH.Ruby.sign import sign_in_message
from src.networks import linea_net
from src.logger import LogProof, cs_logger
from src.Helpers.txnHelper import get_txn_dict, check_estimate_gas, exec_txn
import settings
from src.Helpers.helper import delay_sleep
from src.ABIs import RubyScore_ABI


contract_address = linea_net.web3.to_checksum_address('0xB9cC0Bb020cF55197C4C3d826AC87CAdba51f272')
contract = linea_net.get_contract(linea_net.web3.to_checksum_address(contract_address), abi=RubyScore_ABI)


def check_attest(wallet, token_auth):
    url = f'https://rubyscore.io/api/attestation/check?wallet={wallet.address}&project=linea'
    headers = {'Authorization': f'Bearer {token_auth}', 'Accept': 'application/json'}
    r = requests.post(url, headers=headers)
    if r.status_code == 200:
        res = [r.json()]
        attest_count = res[0]['result']['count']
        return attest_count


def get_score(wallet, token_auth):
    url = f'https://rubyscore.io/api/profile/{wallet.address}/score'
    headers = {'Authorization': f'Bearer {token_auth}', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        res = [r.json()]
        linea_score = res[0]['result']['linea']['score']
        return linea_score


def get_attest_data(token_auth):
    url = 'https://rubyscore.io/api/attestation/claim?project=linea'
    headers = {'Authorization': f'Bearer {token_auth}', 'Accept': 'application/json'}
    r = requests.post(url, headers=headers)
    if r.status_code == 200:
        res = [r.json()]
        txn_calldata = res[0]['result']
        return txn_calldata


def build_txn(wallet, txn_calldata):
    try:
        schema_id = bytes.fromhex(txn_calldata['attestationParams']['schemaId'].removeprefix('0x'))
        expiration_date = int(txn_calldata['attestationParams']['expirationDate'])
        subject = bytes.fromhex(txn_calldata['attestationParams']['subject'].removeprefix('0x').removeprefix('0x'))
        attestation_data = bytes.fromhex(txn_calldata['attestationParams']['attestationData'].removeprefix('0x'))
        signature = bytes.fromhex(txn_calldata['signature'].removeprefix('0x'))
        value = linea_net.web3.to_wei(0.0005, 'ether')
        txn_dict = get_txn_dict(wallet.address, linea_net, value)
        txn = contract.functions.attestRubyscore(
            [schema_id, expiration_date, subject, attestation_data], [signature]
        ).build_transaction(txn_dict)
        return txn
    except Exception as ex:
        cs_logger.info(f'Ошибка в (Ruby/attest: build_txn) {ex.args}')


def attest_ruby(wallet):
    try:
        cs_logger.info(f'Делаем аттестацию RubyScore Group B')
        token_auth = sign_in_message(wallet)
        score = get_score(wallet, token_auth)
        attest_count = check_attest(wallet, token_auth)
        if settings.ruby_replace_enable == 0:
            if attest_count != 0:
                cs_logger.info(f'Аттестация уже пройдена, замена отключена, скипаем')
                log = LogProof(wallet.index, wallet.address, 'RubyScore', 'Уже выполнена', score)
                log.write_log()
                return True
        txn_calldata = get_attest_data(token_auth)
        if score < 15:
            cs_logger.info(f'Score кошелька равен {score}, аттестация не выполняется')
            log = LogProof(wallet.index, wallet.address, 'RubyScore', 'Не выполнялась', score)
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

            log = LogProof(wallet.index, wallet.address, 'RubyScore', txn_hash, score)
            log.write_log()

            delay_sleep(settings.txn_delay[0], settings.txn_delay[1])
            return True

    except Exception as ex:
        cs_logger.info(f'Ошибка в (Ruby/attest: attest) {ex.args}')


def score_check(wallet):
    try:
        cs_logger.info(f'Проверяем баллы для аттестации RubyScore Group B')
        token_auth = sign_in_message(wallet)
        score = get_score(wallet, token_auth)
        log = LogProof(wallet.index, wallet.address, 'RubyScore', 'Предварительная оценка', score)
        log.write_log()
    except Exception as ex:
        cs_logger.info(f'Ошибка в (Ruby/attest: score_check) {ex.args}')
