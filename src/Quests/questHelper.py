from random import shuffle
from src.networks import linea_net
import settings
from src.logger import cs_logger
from src.Helpers.txnHelper import check_estimate_gas, exec_txn, get_txn_dict
from src.Helpers.helper import delay_sleep
from src.Helpers.txnChecker import get_txn_list_from_address, check_txn_existence


class Quest(object):
    title = 'Выполняем квестик'
    contract_address = 'Адрес контракта'
    method_id = '0xМетодКонтракта'
    txn_value = 0

    def build_txn(self, wallet):
        try:
            txn = get_txn_dict(wallet.address, linea_net, self.txn_value)
            txn['to'] = self.contract_address
            txn['data'] = self.method_id
            return txn
        except Exception as ex:
            cs_logger.info(f'Ошибка в (Quest: build_txn) {ex.args}')

    def run_quest(self, wallet):
        try:
            cs_logger.info(f'{self.title}')
            if settings.check_txn_existence_enable == 1:
                txn_list = get_txn_list_from_address(wallet.address, 2000)
                txn_check = check_txn_existence(wallet.address, txn_list, self.contract_address, self.method_id)
                if txn_check is not None:
                    cs_logger.info(f'Данная транзакция уже выполнялась')
                    return True
            txn = self.build_txn(wallet)
            estimate_gas = check_estimate_gas(txn, linea_net)
            if type(estimate_gas) is str:
                cs_logger.info(f'{estimate_gas}')
                return False
            else:
                txn['gas'] = estimate_gas
                txn_hash, txn_status = exec_txn(wallet.key, txn, linea_net)
                cs_logger.info(f'Hash: {txn_hash}')

                wallet.txn_num += 1
                delay_sleep(settings.txn_delay[0], settings.txn_delay[1])
                return True

        except Exception as ex:
            cs_logger.info(f'Ошибка в (questHelper: run_quest) {ex.args}')

    def running(self, wallet):
        attempt = 1
        txn_status = False
        while txn_status is False and attempt < 4:
            cs_logger.info(f' // Попытка №: {attempt}')
            txn_status = self.run_quest(wallet)
            attempt += 1
            if txn_status is False:
                delay_sleep(settings.try_delay[0], settings.try_delay[1])


def get_modules_list():
    modules = list()
    # Операции
    if settings.week_1_enable == 1:
        if settings.gamer_boom_enable == 1:
            modules.append('gamerboom')
            shuffle(modules)

        if settings.nidum_mint_switch == 1:
            modules.append('nidum')
            shuffle(modules)

        if settings.town_story_switch == 1:
            modules.append('townstory')
            shuffle(modules)

    if settings.week_2_enable == 1:
        if settings.yooldo_enable == 1:
            modules.append('yooldo')
            shuffle(modules)

        if settings.pictographs_enable == 1:
            modules.append('pictographs')
            shuffle(modules)

        if settings.abyss_world_mint_switch == 1:
            modules.append('abyss')
            shuffle(modules)

        if settings.omnisea_mint_switch == 1:
            modules.append('omnisea')
            shuffle(modules)

    if settings.week_3_enable == 1:
        if settings.dmail_switch == 1:
            modules.append('dmail')
            shuffle(modules)

        if settings.as_match_mint_switch == 1:
            modules.append('asmatch')
            shuffle(modules)

        if settings.read_on_switch == 1:
            modules.append('readon')
            shuffle(modules)

        if settings.sending_me_switch == 1:
            modules.append('sendingme')
            shuffle(modules)

        if settings.gamic_switch == 1:
            modules.append('gamic')
            shuffle(modules)

        if settings.bit_avatar_switch == 1:
            modules.append('bitavatar')
            shuffle(modules)

    if settings.week_4_enable == 1:
        if settings.sarubol_mint_switch == 1:
            modules.append('sarubol')
            shuffle(modules)

        if settings.zypher_2048_switch == 1:
            modules.append('zypher2048')
            shuffle(modules)

        if settings.lucky_cat_switch == 1:
            modules.append('luckycat')
            shuffle(modules)

    if settings.week_5_enable == 1:
        if settings.battlemon_switch == 1:
            modules.append('battlemon')
            shuffle(modules)

        if settings.omni_zone_switch == 1:
            modules.append('omnizone')
            shuffle(modules)

        if settings.nouns_swich == 1:
            modules.append('nouns')
            shuffle(modules)

    return modules
