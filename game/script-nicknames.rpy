
default persistent._jn_nicknames_natsuki_allowed = True
default persistent._jn_nicknames_natsuki_current_nickname = "Natsuki"
default persistent._jn_nicknames_natsuki_bad_given_total = 0


default persistent._jn_nicknames_player_allowed = True
default persistent._jn_nicknames_player_current_nickname = persistent.playername
default persistent._jn_nicknames_player_bad_given_total = 0

init python in jn_nicknames:
    from Enum import Enum
    import re
    import store
    import store.jn_globals as jn_globals
    import store.jn_utils as jn_utils

    class NicknameTypes(Enum):
        """
        Identifiers for different nickname types.
        """
        invalid = 1
        loved = 2
        neutral = 3
        disliked = 4
        hated = 5
        profanity = 6
        funny = 7
        nou = 8


    NATSUKI_LOVED_NICKNAME_REGEX = re.compile('|'.join({
        "^amazing$",
        "^angel$",
        "^(babe|baby|babygirl)$",
        "^babycakes$",
        "^beautiful$",
        "^bestgirl$",
        "^betterhalf$",
        "^boo$",
        "^(bunbun|bun-bun|bunny)$",
        "^(butter(cup|scotch))$",
        "^candy$",
        "^cookie$",
        "^cupcake$",
        "^(cutey|cutie|cuteypie|cutiepie)$",
        "^(darlin|darling)$",
        "^(doll|dollface)$",
        "^dove$",
        "^gem$",
        "^gorgeous$",
        "^(heartstring|heart-string|heartthrob|heart-throb)$",
        "^heaven$",
        "^(honey|honeybun)$",
        "^hun$",
        "^ki$",
        "^(kitty|kitten)$",
        "^love$",
        "^mine$",
        "^myflower$",
        "^(mylove|mylovely)$",
        "^myprincess$",
        "^myqueen$",
        "^myrose$",
        "^(nat|natnat|nat-nat)$",
        "^(natsu|natsukitten|natsukitty)$",
        "^(natty|nattykins)$",
        "^number(one|1)$",
        "^precious$",
        "^princess$",
        "^(qt|qtpie)$",
        "^(queen|myqueen)$",
        "^(snooki|snookums)$",
        "^special$",
        "^squeeze$",
        "^(starlight|starshine)$",
        "^su$",
        "^(sugar|sugarlump|sugarplum)$",
        "^'suki$",
        "^suki$",
        "^summer$",
        "^(sunny|sunshine)$",
        "^(sweetcakes|sweetpea|sweetheart|sweetness|sweety)$",
        "^thebest$"
    }), re.IGNORECASE)


    NATSUKI_DISLIKED_NICKNAME_REGEX = re.compile('|'.join({
        "^(dad|daddy)$",
        "^father$",
        "^lily$",
        "^(moni$|moni([ck])a|monikins|monmon|mon-mon)$",
        "^papa$",
        "^(sayo|sayori)$",
        "^(salvato|dansalvato)$",
        "^metaverse$",
        "^yori$",
        "^yuri$",
        "^weeb$",
        "(playboy|playgirl)",
    }), re.IGNORECASE)


    NATSUKI_FUNNY_NICKNAME_REGEX = re.compile('|'.join({
        "^catsuki$",
        "^gorgeous$",
        "^(hot|hotstuff|hottie)$",
        "^nyatsuki$",
        "^mama$",
        "^(mom|mommy|mother)$",
        "^(mum|mummy|maam|ma'am)$",
        "^sexy$",
        "^smol$",
        "^snack$",
    }), re.IGNORECASE)


    NATSUKI_NOU_NICKNAME_REGEX = re.compile('|'.join({
        "^adorkable$",
        "^baka$",
        "^(booplicate|boopli[ck]8|boopliq(ee|e|3|33)b)$",
        "^dummy$",
        "^(q[eaoui]b|q[eaoui][eaoui]b|q[eaoui]b[wq][eaoui]b)$",
        "^(w[eaoui]b|w[eaoui][eaoui]b|w[eaoui]b[wq][eaoui]b)$",
    }), re.IGNORECASE)


    PLAYER_DISLIKED_NICKNAME_REGEX = re.compile('|'.join({
        "^(dad|daddy)$",
        "^father$",
        "^papa$",
        "^(salvato|dansalvato)$",
        "^metaverse$",
        "(playboy|playgirl)",
        "^nerd$",
        "^trash$",
        "^junk$",
    }), re.IGNORECASE)


    PLAYER_FUNNY_NICKNAME_REGEX = re.compile('|'.join({
        "^gorgeous$",
        "^(hot|hotstuff|hottie)$",
        "^(mom|mommy|mother)$",
        "^(mum|mummy|maam|ma'am)$",
        "^mama$",
        "^sexy$",
        "^weeb$",
        "^dork$",
        "^nerd$",
        "^geek$",
        "^girl$",
        "^boy$",
        "thiccsuki"
    }), re.IGNORECASE)

    def getNatsukiNicknameType(nickname):
        """
        Returns the NicknameTypes type for a given string nickname for Natsuki, defaulting to NatsukiNicknameTypes.neutral

        IN:
            nickname - The nickname to test

        OUT:
            NicknameTypes type of the given nickname
        """
        
        if not isinstance(nickname, basestring):
            return NicknameTypes.invalid
        
        else:
            nickname = nickname.lower().replace(" ", "")
            
            if nickname == "":
                return NicknameTypes.invalid
            
            elif re.search(NATSUKI_LOVED_NICKNAME_REGEX, nickname):
                return NicknameTypes.loved
            
            elif re.search(NATSUKI_FUNNY_NICKNAME_REGEX, nickname):
                return NicknameTypes.funny
            
            elif re.search(NATSUKI_DISLIKED_NICKNAME_REGEX, nickname) or jn_utils.getStringContainsLabel(nickname):
                return NicknameTypes.disliked
            
            elif jn_utils.getStringContainsInsult(nickname):
                return NicknameTypes.hated
            
            elif jn_utils.getStringContainsProfanity(nickname):
                return NicknameTypes.profanity
            
            elif re.search(NATSUKI_NOU_NICKNAME_REGEX, nickname):
                return NicknameTypes.nou
            
            else:
                return NicknameTypes.neutral

    def getPlayerNicknameType(nickname):
        """
        Returns the NicknameTypes type for a given string nickname for the player, defaulting to NicknameTypes.neutral

        IN:
            nickname - The nickname to test

        OUT:
            NicknameTypes type of the given nickname
        """
        
        if not isinstance(nickname, basestring):
            return NicknameTypes.invalid
        
        else:
            nickname = nickname.lower().replace(" ", "")
            
            if nickname == "":
                return NicknameTypes.invalid
            
            if re.search(PLAYER_FUNNY_NICKNAME_REGEX, nickname):
                return NicknameTypes.funny
            
            elif re.search(PLAYER_DISLIKED_NICKNAME_REGEX, nickname) or jn_utils.getStringContainsLabel(nickname):
                return NicknameTypes.disliked
            
            elif jn_utils.getStringContainsInsult(nickname):
                return NicknameTypes.hated
            
            elif jn_utils.getStringContainsProfanity(nickname):
                return NicknameTypes.profanity
            
            else:
                return NicknameTypes.neutral
