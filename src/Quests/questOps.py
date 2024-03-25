import settings
from src.logger import cs_logger
from src.Quests.Week2.Yooldo.daily import yooldo_daily
from src.Quests.Week2.Yooldo.trobSwap import yooldo_trob_swap
from src.Quests.Week2.Pictographs.mint import pictographs_mint, pictographs_stake
from src.Quests.Week2.AbyssWorld.mint import abyss_world
from src.Quests.Week2.Omnisea.mint import omnisea
from src.Quests.Week1.GamerBoom.mint import gamer_boom_mint
from src.Quests.Week1.GamerBoom.proof import gamer_boom_proof
from src.Quests.Week3.AsMatch.mint import as_match_mint
from src.Helpers.gasPriceChecker import check_limit
from src.Quests.Week3.Dmail.sendMail import dmail_send
from src.Quests.Week3.ReadOn.curate import read_on_curate
from src.Quests.Week3.SendingMe.abuse import sending_me
from src.Quests.Week3.Gamic.swap import gamic_swap
from src.Quests.Week3.BitAvatar.checkIn import bit_avatar
from src.Quests.Week1.TownStory.mint import town_story
from src.Quests.Week4.Sarubol.mint import sarubol_mint
from src.Quests.Week4.Zypher.start import zypher
from src.Quests.Week1.Nidum.mint import nidum_mint
from src.Quests.Week4.LuckyCat.mint import lucky_cat
from src.Quests.Week5.Battlemon.mint import battlemon
from src.Quests.Week5.OmniZone.mint import omni_zone
from src.Quests.Week5.Nouns.mint import nouns_mint


def quest_ops(wallet, modules):
    for module in modules:

        if module == 'yooldo':
            cs_logger.info(f'    ***   Модуль Yooldo   ***   ')
            if settings.daily_switch == 1:
                check_limit()
                yooldo_daily.running(wallet)

            if settings.trob_swap_switch == 1:
                check_limit()
                yooldo_trob_swap.running(wallet)

        if module == 'pictographs':
            cs_logger.info(f'    ***   Модуль Pictographs   ***   ')
            if settings.pictographs_mint_switch == 1:
                check_limit()
                pictographs_mint.running(wallet)
            if settings.pictographs_stake_switch == 1:
                check_limit()
                pictographs_stake.running(wallet)

        if module == 'abyss':
            cs_logger.info(f'    ***   Модуль Abyss World   ***   ')
            check_limit()
            abyss_world.running(wallet)

        if module == 'omnisea':
            cs_logger.info(f'    ***   Модуль Omnisea  ***   ')
            check_limit()
            omnisea.running(wallet)

        if module == 'gamerboom':
            cs_logger.info(f'    ***   Модуль GamerBoom  ***   ')
            if settings.gamer_boom_proof_switch == 1:
                check_limit()
                gamer_boom_proof.running(wallet)
            if settings.gamer_boom_mint_switch == 1:
                check_limit()
                gamer_boom_mint.running(wallet)

        if module == 'dmail':
            cs_logger.info(f'    ***   Модуль Dmail  ***   ')
            check_limit()
            dmail_send.running(wallet)

        if module == 'asmatch':
            cs_logger.info(f'    ***   Модуль AsMatch  ***   ')
            check_limit()
            as_match_mint.running(wallet)

        if module == 'readon':
            cs_logger.info(f'    ***   Модуль ReadOn  ***   ')
            check_limit()
            read_on_curate.running(wallet)

        if module == 'sendingme':
            cs_logger.info(f'    ***   Модуль SendingMe  ***   ')
            check_limit()
            sending_me.running(wallet)

        if module == 'gamic':
            cs_logger.info(f'    ***   Модуль Gamic  ***   ')
            check_limit()
            gamic_swap.running(wallet)

        if module == 'bitavatar':
            cs_logger.info(f'    ***   Модуль BitAvatar  ***   ')
            check_limit()
            bit_avatar.running(wallet)

        if module == 'townstory':
            cs_logger.info(f'    ***   Модуль TownStory  ***   ')
            check_limit()
            town_story.running(wallet)

        if module == 'sarubol':
            cs_logger.info(f'    ***   Модуль Sarubol  ***   ')
            check_limit()
            sarubol_mint.running(wallet)

        if module == 'zypher2048':
            cs_logger.info(f'    ***   Модуль Zypher 2048  ***   ')
            check_limit()
            zypher.running(wallet)

        if module == 'nidum':
            cs_logger.info(f'    ***   Модуль Nidum Mint  ***   ')
            check_limit()
            nidum_mint.running(wallet)

        if module == 'luckycat':
            cs_logger.info(f'    ***   Модуль LuckyCat Mint  ***   ')
            check_limit()
            lucky_cat.running(wallet)

        if module == 'battlemon':
            cs_logger.info(f'    ***   Модуль Battlemon Mint  ***   ')
            check_limit()
            battlemon.running(wallet)

        if module == 'omnizone':
            cs_logger.info(f'    ***   Модуль OmniZone Mint  ***   ')
            check_limit()
            omni_zone.running(wallet)

        if module == 'nouns':
            cs_logger.info(f'    ***   Модуль Nouns Mint  ***   ')
            check_limit()
            nouns_mint.running(wallet)
