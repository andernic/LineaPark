import settings
import settings as stgs
import src.logger as logger
from src.networks import ethereum_net, linea_net


def get_info(wallets):
    logger.cs_logger.info(f'Цена газа в Ethereum: {ethereum_net.web3.from_wei(ethereum_net.get_gas_price_wei(), "gWei")} gWei')
    logger.cs_logger.info(f'Цена газа в Linea: {linea_net.web3.from_wei(linea_net.get_gas_price_wei(), "gWei")} gWei')
    if stgs.exc_withdraw == 1:
        logger.cs_logger.info(f'Вывод с биржи в сеть включен!')
        if stgs.exc_mode == 1:
            logger.cs_logger.info(f'Выводим {stgs.exc_percent[0]*100} - {stgs.exc_percent[1]*100} % от баланса')
        if stgs.exc_mode == 2:
            logger.cs_logger.info(f'Выводим весь доступный баланс')
        if stgs.exc_mode == 3:
            logger.cs_logger.info(f'Выводим сумму от {stgs.exc_sum[0]} до {stgs.exc_sum[1]} ETH')

    else:
        logger.cs_logger.info(f'Вывод с биржи в сеть отключен!')

    if stgs.exc_deposit == 1:
        logger.cs_logger.info(f'Депозит на адрес биржи включен!')
        if stgs.switch_bridge_exc == 0:
            logger.cs_logger.info(f'Депозит на биржу осуществляется из Linea!')
        if stgs.switch_bridge_exc == 1:
            logger.cs_logger.info(f'Депозит на биржу осуществляется из Arbitrum!')
    else:
        logger.cs_logger.info(f'Депозит на адрес биржи отключен!')

    if stgs.eth_swap_switch == 1:
        logger.cs_logger.info(f'Свапаем ETH на сумму: {stgs.usdc_limits[0]} - {stgs.usdc_limits[1]} USDC '
                              f'| slippage= {settings.slippage_USDC * 100.0} % ')

    logger.cs_logger.info(f'Задержки между кошельками: от {stgs.wallet_delay[0]} до {stgs.wallet_delay[1]} сек')
    logger.cs_logger.info(f'Задержки между транзакциями: от {stgs.txn_delay[0]} до {stgs.txn_delay[1]} сек')
    logger.cs_logger.info(f'Задержки после бриджа: от {stgs.bridge_delay[0]} до {stgs.bridge_delay[1]} сек')

    if stgs.usdc_swap_switch == 1:
        logger.cs_logger.info('Свап остатков USDC на эфир после операций Включен ✅')
    else:
        logger.cs_logger.info('Свап остатков USDC на эфир после операций Отключен')

    if stgs.poh_enable == 1:
        logger.cs_logger.info(' 🔔 Транзакции POH Включены')

        if stgs.trusta_a_switch == 1:
            logger.cs_logger.info(' - Модуль POH Trusta Group A Включен ✅')
        else:
            logger.cs_logger.info(' - Модуль POH Trusta Group A Отключен')

        if stgs.trusta_b_switch == 1:
            logger.cs_logger.info(' - Модуль POH Trusta Group B Включен ✅')
        else:
            logger.cs_logger.info(' - Модуль POH Trusta Group B Отключен')

        if stgs.ruby_switch == 1:
            logger.cs_logger.info(' - Модуль POH RubyScore Group B Включен ✅')
        else:
            logger.cs_logger.info(' - Модуль POH RubyScore Group B Отключен')

    if stgs.poh_enable == 2:
        logger.cs_logger.info(' 🔔 Проверка Score POH Включена ✅')
    if stgs.poh_enable == 0:
        logger.cs_logger.info(' 🔔 Транзакции POH Отключены')

    if stgs.week_1_enable == 1:
        logger.cs_logger.info(' ⭐ Активные Квесты Week 1 ')
        if stgs.gamer_boom_enable == 1:
            logger.cs_logger.info(' Квест GamerBoom Включен ')
            if stgs.gamer_boom_proof_switch == 1:
                logger.cs_logger.info(' - Модуль GamerBoom Proof Включен ✅')
            else:
                logger.cs_logger.info(' - Модуль GamerBoom Proof Отключен')

            if stgs.gamer_boom_mint_switch == 1:
                logger.cs_logger.info(' - Модуль GamerBoom Mint Включен ✅')
            else:
                logger.cs_logger.info(' - Модуль GamerBoom Mint Отключен')
        else:
            logger.cs_logger.info(' Квест GamerBoom Отключены')

        if stgs.nidum_mint_switch == 1:
            logger.cs_logger.info(' Модуль Nidum Nft Включен ✅')
        else:
            logger.cs_logger.info(' Модуль Nidum Nft Отключен')

        if stgs.town_story_switch == 1:
            logger.cs_logger.info(' Модуль Town Story Включен ✅')
        else:
            logger.cs_logger.info(' Модуль Town Story Отключен')

    if stgs.week_2_enable == 1:
        logger.cs_logger.info(' ⭐ Активные Квесты Week 2 ')
        if stgs.yooldo_enable == 1:
            logger.cs_logger.info(' Квест Yooldo Включен ')
            if stgs.daily_switch == 1:
                logger.cs_logger.info(' - Модуль Yooldo Daily Stand-Up Включен ✅')
            else:
                logger.cs_logger.info(' - Модуль Yooldo Daily Stand-Up Отключен')

            if stgs.trob_swap_switch == 1:
                logger.cs_logger.info(' - Модуль Yooldo TROB swap Включен ✅')
            else:
                logger.cs_logger.info(' - Модуль Yooldo TROB swap Отключен')
        else:
            logger.cs_logger.info(' Квест Yooldo Отключены')

        if stgs.pictographs_enable == 1:
            logger.cs_logger.info(' Квест Pictographs Включен ')
            if stgs.pictographs_mint_switch == 1:
                logger.cs_logger.info(' - Модуль Pictographs Mint Включен ✅')
            else:
                logger.cs_logger.info(' - Модуль Pictographs Mint Отключен')

            if stgs.pictographs_stake_switch == 1:
                logger.cs_logger.info(' - Модуль Pictographs Stake Включен ✅')
            else:
                logger.cs_logger.info(' - Модуль Pictographs Stake Отключен')
        else:
            logger.cs_logger.info(' Квесты Pictographs Отключены')

        if stgs.abyss_world_mint_switch == 1:
            logger.cs_logger.info(' Модуль Abyss World Включен ✅')
        else:
            logger.cs_logger.info(' Модуль Abyss World Отключен')

        if stgs.omnisea_mint_switch == 1:
            logger.cs_logger.info(' Модуль Satoshi Universe Omnisea Включен ✅')
        else:
            logger.cs_logger.info(' Модуль Satoshi Universe Omnisea Отключен')

    if stgs.week_3_enable == 1:
        logger.cs_logger.info(' ⭐ Активные Квесты Week 3 ')
        if stgs.dmail_switch == 1:
            logger.cs_logger.info(' Модуль Dmail Включен ✅')
        else:
            logger.cs_logger.info(' Модуль Dmail Отключен')

        if stgs.as_match_mint_switch == 1:
            logger.cs_logger.info(' Модуль AsMatch Включен ✅')
        else:
            logger.cs_logger.info(' Модуль AsMatch Отключен')

        if stgs.read_on_switch == 1:
            logger.cs_logger.info(' Модуль ReadOn Включен ✅')
        else:
            logger.cs_logger.info(' Модуль ReadOn Отключен')

        if stgs.sending_me_switch == 1:
            logger.cs_logger.info(' Модуль SendingMe Включен ✅')
        else:
            logger.cs_logger.info(' Модуль SendingMe Отключен')

        if stgs.gamic_switch == 1:
            logger.cs_logger.info(' Модуль Gamic Включен ✅')
        else:
            logger.cs_logger.info(' Модуль Gamic Отключен')

        if stgs.bit_avatar_switch == 1:
            logger.cs_logger.info(' Модуль BitAvatar Включен ✅')
        else:
            logger.cs_logger.info(' Модуль BitAvatar Отключен')

    if stgs.week_4_enable == 1:
        logger.cs_logger.info(' ⭐ Активные Квесты Week 4 ')
        if stgs.sarubol_mint_switch == 1:
            logger.cs_logger.info(' Модуль Sarubol Включен ✅')
        else:
            logger.cs_logger.info(' Модуль Sarubol Отключен')

        if stgs.zypher_2048_switch == 1:
            logger.cs_logger.info(' Модуль Zypher 2048 Включен ✅')
        else:
            logger.cs_logger.info(' Модуль Zypher 2048 Отключен')

        if stgs.lucky_cat_switch == 1:
            logger.cs_logger.info(' Модуль LuckyCat Включен ✅')
        else:
            logger.cs_logger.info(' Модуль LuckyCat Отключен')

    if stgs.week_5_enable == 1:
        logger.cs_logger.info(' ⭐ Активные Квесты Week 5 ')
        if stgs.battlemon_switch == 1:
            logger.cs_logger.info(' Модуль Battlemon Включен ✅')
        else:
            logger.cs_logger.info(' Модуль Battlemon Отключен')

        if stgs.omni_zone_switch == 1:
            logger.cs_logger.info(' Модуль OmniZone Включен ✅')
        else:
            logger.cs_logger.info(' Модуль OmniZone Отключен')

        if stgs.nouns_swich == 1:
            logger.cs_logger.info(' Модуль Nouns Включен ✅')
        else:
            logger.cs_logger.info(' Модуль Nouns Отключен')

    logger.cs_logger.info('📜 Список обнаруженных адресов кошельков -- адресов бирж')
    for wallet in wallets:
        logger.cs_logger.info(f'№ {wallet.wallet_num} | {wallet.address} -- {wallet.exchange_address}')

    while True:
        logger.cs_logger.info(f'Подтвердить? Y/N: ')
        answer = input('')
        if answer.lower() == 'y':
            stgs.start_flag = True
            break
        if answer.lower() == 'n':
            break
