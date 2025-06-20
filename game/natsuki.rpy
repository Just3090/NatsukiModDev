default persistent._jn_player_confession_accepted = False
default persistent._jn_player_confession_day_month = None
default persistent._jn_natsuki_birthday_known = False

init python:
    import codecs
    import datetime
    import store.jn_desk_items as jn_desk_items
    import store.jn_outfits as jn_outfits

    class Natsuki(object):
        """
        Qeeb class for handling actions related to Natsuki such as affinity checks/gains/losses, clothing, etc.

        NNNNNNXK0OOKXNXXKKK0000O00KKKKK000OO0Okxooooodoollccc:;;:ok000000K00000OOO00Kkl::oxkxl,,:oOK00KKKKKK
        NNNNNNNK00XXXXKK000000000O00KK0000O00000KKKKKKKKK0000OOkxddk0000000K00000OOOOkxxo:cdkko:,ckKOk0KKKKK
        NNNNNNX0KXXKKKKKKKXKK0000KKKXXKKKK00KKKKKKKK000000000KKKKKKKKKK00OO00000000OOkxxOkoccdkd:ckKOdkKKKKK
        NNNXX00KXXXXXXXXXXKKKKKKKKKKKKKKKKKKKKKKKKKKK0000000000KKKKKKKKKK0000000K000OOkkk00kl:oxddOKkox0KKKK
        XXXXK0KXNNNNNXXXKKXXXKKKKKKKKKKKKKKKKKKKKKKKKK000000000000KKKXXKKKKK00000000000OOOO0Oo:cok0OoldkKKKK
        XXXXXNNNNNX00KKKKXXKK0KKKKKKKKKKKKKKKKKKKKKKKK0K0000KK000000KKXKKKKK0KK0000O0000OOkOOOo;o0Oxoodx0KK0
        XKXXNNXKOxdxOK0KXXK00KKKKKKKKKKKKKKKKKKKKKKKKKKK000000KK000O00KXKK00KK00KK000OOOOOOOkkxxkxddxxxOKKK0
        XXNXKkdlclk0000KXK00KKKKKKKKKKKKKKKKKK000KKKKKKKKK0000KK0KKOkkKXKKK00KKKKK00K00OOOOOkxxkd:lxxxk0KK00
        XXXOocccdOK000KK00KKKK000KKKKKKKKKKKKK00000KKK0KKKKK000KKK00Okk00000000K0KKK00000OkkkkOkxodkxxO0KK00
        XKKkcclx0000000OOKXXK000KKKKKKKKKKKKKK00000KKKK0KKKK00000K0OKKkxk0K00OO0000K00KK000OOOOOkkkkxk0K0000
        XK0xclkK0OOOO0OO0KKK0O0KKKKKKKKKKKKKKK000KKKKKKKKKKK00KKKKKOOK0kxxOKK0OOO0K00K00K0000OOOOkxxk0000OOk
        KK0dlkK0OOOOOOkO0KKOk0KKKKKK000KKKKKK000K0KK0KKK00KK00KKKXKkxO0Okdx0KK0OkO0K0000KKK000OOOOkO000OOkdl
        K0OxkK0OOOOOOkk0KK0kOKKKKKKK00000KKKK000KKKKKKKKKKK00KXXXKkdxO00kxdk00K0kxk00K00K00K0000OO00Okxdolll
        K0O0KKkkOOkkkkO0KOkk0XXKKKK0OO0KKKKKK00KKKKKKKK0KKK00KXK0kdxkk00kxkkO000OxxkO0K0K00K0OOOOkkxollllood
        000KXOkkOOkkxxO00kkO0KXXXXK0OOKKK0KKK0KKKKKKKKKKXK0O0KKOkddkOkO0kOK0OO00OkxxxO00K0K00OOOkkkxdoodxxxx
        000XKkkOOkkxxxkOOkkO00KKXNN0k0KKKKKXKKKKXXKKXXXNX0kk000kxdx0KOOOk0NX0OOOOkxxxxk00KK00000000OOxxxkkkk
        00KX0kkOOkxxxxkkkkkOO0K0KKX0kKNXXNXXXXNNNKKXXKKK0xdk0Okxddk00kxdx0KK0OOkkkxkOkxk0KK00000K000Okxxxkkk
        00KKOkOOkxxxdxxxxxkOOO00KK0OkKXKKXKKKKKXK0KKKK0OxxxkxxdddkKXXOdx0NNNXK0kxdx0XKOxxOKKK0OO0K000Okxxkkk
        O0KKkxOOkxxddxxxxxkOkkO0000kk0KK0000KK0000KKK0OkdddddxxxkKNNNOdONNNNNXK0xoOXNNX0kk0KKKOO0KK00OkxdkOk
        k0KKkxOOkxxddxxdxxkkkkkO00Okk00Oxk0KK0000KKK0Okddxxddddx0XNNXkOXNNNNNNXX0x0NNNNNKOO0K00kO0000Oxxdx00
        k0XKkkOOkxxddxxddxkkkkkkOOkxkO0d;:dO0O000K00OxxdddddddxOKNNNXKXNNNNNNNXXXOKNNNNNNKO0KK0kO0000kodddO0
        x0XXOkOOkxxddxxddxxkxxxkkkxdkkko,,;:ok0K00OkxxdddooodxOKNNNNNNNXXXNNXNNNNNNNNNNNNX0O000kk0000kooddkO
        k0NXOkOOOkxddxxddxxxxxxxkxddkkOk::ol:;coxxkxxxdoooldxk0XXXNNXXXXXNNXX0Okxdollodk0XX0000xdO00OxlldxxO
        OKNX0kO0Okxddxxddxxxxxxxxxddk00Oc;dkdl;'';coxdooddxkOOKKKXXXXXX0koc:;'...  'cl::oKNK00Odok00kdllxkxk
        OKNXKkk0Okxdddddddddxxxxxdllddoc;',:;;;,,,cdooxxkOOOOKXXXXXKKkl,. .....''..'xNXOOXNX0Okolk0kxdookOkx
        OKNXKOkO0Oxodddddddddxxxd:,,;;:c;',lddddodxooxOOOOOOKNNNNNNXk:.'cxOl''',',clo0WNXNNX0kxllxkxdkxd00kx
        xKNXXOkO00kdodddoodoodddol;,;cdxd;,okkxxxxdxkOOOOO0KXNNNNNNXxco0NNOc:c:'':xOx0NNNNNX0xocldxdkOkO00kd
        xKXKX0kkO0Oxoodooooollodddoc;,;ldc'cddxkkkOOOOOO0KKXNNNNNNNNX0KNWNOlokOxxOXKOKNNNNNXkoocldxk00000Odo
        OXX0KKOxkOOkolooolllldxdddxxdl:,,,.,lxkkOOOOOO00KXXNNNNNNNNNNNNNNNNKkxOKK0OOKNNNNNNKxooclxk000000koo
        OX0OKK0xxkOOkoooocldxxddxxxxxxxo:,;cdxkOOOO0000KXNNNNNNNNNNNNNNNNNNNNK0OOO0KXNXXXXXkdxolxO0000000xod
        0Xkx0KKkdxkOOkdolodxdddxxxxxxxdlccodxkkOOO0000KXXNNNNNNNNNNNNNNNNNNNNNNNNXXXXXXXXX0kOxok00000000Odlx
        0KkxOKK0xdxkOkxddooddxxxxxxxdlccllooxkOO00000KXNNNNNNNNNNNNNNNNNNNNNNNXXXXXKKKKKKXKKOdk00OO00000kodO
        0OxxOKK0Oxddxxdooodddddddddlc:;,'...';lk0000KXNNNNNNNNNNNNNNNNNNNNNNXXXXXXKKKKKKKXXKkk0Okk000000kdOK
        OxxxkKK00xdddooodxddddddolc:,..........;dO0KKXNNNNNNNNNNNNNNNNNNNNNXXXXXXXKKKKKKXXK0O0kxx0000O0OkOK0
        xxxxk00Okdlcldxxdddddolccc:...cl:......';d0KXNNNNNNNNNNNNNNNNNNNNNXXXXXXXXXXXXXXXX0O00kxk000OOOO00Ox
        xxxddkOkkxooxxxdddolc:clol,.'dOk:..''';lco0XXNNNNNNNNNNNNNNNNNNNNNXXXXXXXXXXXXXXXK0KK0kxO00OkkkOkddo
        dddddk0OOkkkxxdollccllolodc.;xOOko:,':odldKNNNNNNNNNNNNNNNNNNNNNNNXXXXXXXXXXXXXXXXXXKOdxO0Okkxdddddd
        ddddoxkkkxxdol:;;cllodxdddo:;lxOO0OxdddxkKXNNNNNXXXXNNNNNNNNNNNNNNNNXXXXXXXXNNNNNNNKOodk00OOkxxkxdoo
        doodddxxxdl::::;;:cllodxxxdooodkO00KK00KXNNNNNNXK00KXNNNNNNNNNNNNNNNNNNNNNNNNNNNNXKkooxO0Okxdxxxolod
        ooooodxOkkdcccc:;::ccloodxxdllldkO000KKXXXNNNNNNNXXXNNNNNNNNNNNNNNNNNNNNNNNNNNNNX0xooxOOkxooxxdllddx
        oooloodOK0koccc:;::c::cloddxxdodxkO0KKXXXXNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNKkoodxkOxxdooodOxlldx
        lllclolkKKOdllcc::cccc:ccloooddxxxxxk0KXXXNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNXOdoodxkkkxddxdlxK0olxx
        cclcllcd0K0kolllc:cccccccccccccllllcok0XXXNNNNNNNNNNNNNNNNXXXXNNNNNNNNNNNNNX0xooodxxxkkkkkkkOKX0ddkx
        ccccllclkXKOdllllcccllllcclllllllcccclx0XNNNNNWWWWWNNNNNNXXXXXNNNNNNNNNNNNKxoloodxxxkkkkkO0KXXK0xdxk
        ccccclccdKXKkoooollllllllllllloooollllllx0NNWWWWWWWWNNNNNNNNNNNNNNNNNNNX0xlcloodkkkkkkO0KXNNXKKOddxx
        :::::lcclkXK0kdooooooooooooolllooddddxkkxkO0KXNWWWWWWNNNNNNNNNNNNNNNNXKOxc;clodxkO00KXNNNNNNWXKkoddx
        ;::::cc::lOXK0OxdddddddodddxxddodxxxxxkOkdocclodxkkOO0KKXXXXKKKKKKKK00OkxolxO0KXXNNWWWWWWWWWWXOolddd
        ;:::cccccclOX0kkkxddddddddodxOOOO000Oxdllc::;;;,,'',,;::ccccc::cdO00OxoooxXWWWWWWNNNWWWWWWWWXklldddd
        ::::ccccccclk0kddxxddddddddddxkO00Okxollcc::;;;;,,,,,,,,,,,,,,,lOKOxolddo0NWWWWWNNNNNNNWWNXkoloddddo
        ::::cccccccclxkxddddxxdddxxdxkkOOOxoollccc::::;;,;;;,,,,,,,,,,;d0xccldkodKWWWWWWNNNNNNNWN0oclddddddo
        """
        
        
        _m1_natsuki__is_in_conversation = False
        
        
        _m1_natsuki__is_in_game = False
        
        
        _m1_natsuki__last_topic_call = datetime.datetime.now()
        _m1_natsuki__last_idle_call = datetime.datetime.now()
        _m1_natsuki__last_menu_call = datetime.datetime.now()
        
        _m1_natsuki__capped_aff_dates = list()
        
        
        
        _desk_left = [Null(), None]
        _desk_centre = [Null(), None]
        _desk_right = [Null(), None]
        
        
        
        _is_reading_to_right = False
        
        
        _is_force_quit_attempt = None
        
        @staticmethod
        def setDeskItem(item, desk_slot=None):
            """
            Sets a desk item for Natsuki's desk, and updates her current sprite.

            IN:
                - item - Can be one of:
                    - JNDeskItem instance, in which case an Image displayable is created from the image_path attribute
                    - str file path to image, in which case an Image displayable is created from it
                    - A Ren'Py displayable (Image, etc.), which is used directly
                - desk_slot - Optional JNDeskSlots slot to use for the item (left, centre or right), if item is not JNDeskItem, or None
            """
            if isinstance(item, jn_desk_items.JNDeskItem):
                image = Image(item.image_path)
                desk_slot = item.desk_slot
                reference_name = item.reference_name
            
            elif isinstance(item, basestring):
                image = Image(item)
                reference_name = "unknown"
            
            else:
                image = item
                reference_name = "unknown"
            
            if desk_slot == jn_desk_items.JNDeskSlots.left:
                Natsuki._desk_left = [image, reference_name]
            
            elif desk_slot == jn_desk_items.JNDeskSlots.centre:
                Natsuki._desk_centre = [image, reference_name]
            
            elif desk_slot == jn_desk_items.JNDeskSlots.right:
                Natsuki._desk_right = [image, reference_name]
            
            else:
                jn_utils.log("Cannot assign item to desk slot {0} as the slot does not exist.".format(desk_slot))
        
        @staticmethod
        def getDeskItemReferenceName(desk_slot):
            """
            Gets the reference name of the desk item for Natsuki's desk given a specific slot.
            To get the displayable item for rendering in a specific slot, use getDeskItemDisplayable instead.

            IN:
                - desk_slot - JNDeskSlots slot to return an item for (left, centre or right)

            OUT:
                - str reference name for the desk item, or None
            """
            if desk_slot == jn_desk_items.JNDeskSlots.left:
                return Natsuki._desk_left[1]
            
            elif desk_slot == jn_desk_items.JNDeskSlots.centre:
                return Natsuki._desk_centre[1]
            
            elif desk_slot == jn_desk_items.JNDeskSlots.right:
                return Natsuki._desk_right[1]
            
            else:
                jn_utils.log("Cannot get reference name for desk slot {0} as the slot does not exist.".format(desk_slot))
        
        @staticmethod
        def getDeskItemDisplayable(st, at, desk_slot):
            """
            Gets a desk item displayable for Natsuki's desk given a specific slot.
            To get the name of an item in a specific slot, use getDeskItemReferenceName instead.

            IN:
                - desk_slot - JNDeskSlots slot to return an displayable for (left, centre or right)
            """
            if desk_slot == jn_desk_items.JNDeskSlots.left:
                return Natsuki._desk_left[0], None
            
            elif desk_slot == jn_desk_items.JNDeskSlots.centre:
                return Natsuki._desk_centre[0], None
            
            elif desk_slot == jn_desk_items.JNDeskSlots.right:
                return Natsuki._desk_right[0], None
            
            else:
                jn_utils.log("Cannot get displayable for desk slot {0} as the slot does not exist.".format(desk_slot))
        
        @staticmethod
        def clearDeskItem(desk_slot):
            """
            Removes a desk item from Natsuki's desk given a specific slot.

            IN:
                - desk_slot - JNDeskSlots slot of the desk to clear (left, centre or right)
            """
            if desk_slot == jn_desk_items.JNDeskSlots.left:
                Natsuki._desk_left = [Null(), None]
            
            elif desk_slot == jn_desk_items.JNDeskSlots.centre:
                Natsuki._desk_centre = [Null(), None]
            
            elif desk_slot == jn_desk_items.JNDeskSlots.right:
                Natsuki._desk_right = [Null(), None]
            
            else:
                jn_utils.log("Cannot clear desk slot {0} as the slot does not exist.".format(desk_slot))
        
        @staticmethod 
        def clearDesk():
            """
            Completely clears Natsuki's desk.
            """
            Natsuki._desk_left = [Null(), None]
            Natsuki._desk_centre = [Null(), None]
            Natsuki._desk_right = [Null(), None]
        
        @staticmethod
        def getDeskSlotClear(desk_slot):
            """
            Returns the state of the desk for the given slot, based on if a displayable is present.

            IN:
                - desk_slot - JNDeskSlots slot of the desk to clear (left, centre or right)
            OUT:
                - True if the slot is clear/unoccupied, otherwise False
            """
            if desk_slot == jn_desk_items.JNDeskSlots.left:
                return isinstance(Natsuki._desk_left[0], Null)
            
            elif desk_slot == jn_desk_items.JNDeskSlots.centre:
                return isinstance(Natsuki._desk_centre[0], Null)
            
            elif desk_slot == jn_desk_items.JNDeskSlots.right:
                return isinstance(Natsuki._desk_right[0], Null)
            
            return False
        
        
        
        
        _outfit = None
        
        @staticmethod
        def getOutfitName():
            """
            Returns the reference name of the outfit Natsuki is currently wearing.
            """
            return Natsuki._outfit.reference_name
        
        @staticmethod
        def getOutfit():
            """
            Gets the JNOutfit Natsuki is currently wearing.
            """
            return Natsuki._outfit
        
        @staticmethod
        def setOutfit(outfit, persist=True):
            """
            Assigns the specified jn_outfits.JNOutfit outfit to Natsuki.

            IN:
                - outfit - The jn_outfits.JNOutfit outfit for Natsuki to wear.
                - persist - True if the outfit should be remembered so Natsuki will be wearing it on next boot
            """
            outfit.accessory = jn_outfits.getWearable("jn_none") if not outfit.accessory else outfit.accessory
            outfit.eyewear = jn_outfits.getWearable("jn_none") if not outfit.eyewear else outfit.eyewear
            outfit.headgear = jn_outfits.getWearable("jn_none") if not outfit.headgear else outfit.headgear
            outfit.necklace = jn_outfits.getWearable("jn_none") if not outfit.necklace else outfit.necklace
            outfit.facewear = jn_outfits.getWearable("jn_none") if not outfit.facewear else outfit.facewear
            outfit.back = jn_outfits.getWearable("jn_none") if not outfit.back else outfit.back
            
            Natsuki._outfit = outfit
            
            if persist:
                store.persistent.jn_natsuki_outfit_on_quit = Natsuki._outfit.reference_name
        
        @staticmethod
        def isWearingOutfit(reference_name):
            """
            Returns True if Natsuki is wearing the specified outfit, otherwise False.

            IN: 
                - reference_name - outfit reference name to check if Natsuki is wearing

            OUT:
                - True if Natsuki is wearing the specified outfit, otherwise False
            """
            return Natsuki._outfit.reference_name == reference_name
        
        @staticmethod
        def isWearingClothes(reference_name):
            """
            Returns True if Natsuki is wearing the specified clothes, otherwise False.

            IN: 
                - reference_name - The clothes reference name to check if Natsuki is wearing

            OUT:
                - True if Natsuki is wearing the specified clothes, otherwise False
            """
            return Natsuki._outfit.clothes.reference_name == reference_name
        
        @staticmethod
        def isWearingHairstyle(reference_name):
            """
            Returns True if Natsuki is wearing the specified hairstyle, otherwise False.

            IN: 
                - reference_name - The hairstyle reference name to check if Natsuki is wearing

            OUT:
                - True if Natsuki is wearing the specified hairstyle, otherwise False
            """
            return Natsuki._outfit.hairstyle.reference_name == reference_name
        
        @staticmethod
        def isWearingAccessory(reference_name):
            """
            Returns True if Natsuki is wearing the specified accessory, otherwise False.

            IN: 
                - reference_name - The accessory reference name to check if Natsuki is wearing

            OUT:
                - True if Natsuki is wearing the specified accessory, otherwise False
            """
            return Natsuki._outfit.accessory.reference_name == reference_name
        
        @staticmethod
        def isWearingEyewear(reference_name):
            """
            Returns True if Natsuki is wearing the specified eyewear, otherwise False.

            IN: 
                - reference_name - The eyewear reference name to check if Natsuki is wearing

            OUT:
                - True if Natsuki is wearing the specified eyewear, otherwise False
            """
            return Natsuki._outfit.eyewear.reference_name == reference_name
        
        @staticmethod
        def isWearingHeadgear(reference_name):
            """
            Returns True if Natsuki is wearing the specified headgear, otherwise False.

            IN: 
                - reference_name - The headgear reference name to check if Natsuki is wearing

            OUT:
                - True if Natsuki is wearing the specified headgear, otherwise False
            """
            return Natsuki._outfit.headgear.reference_name == reference_name
        
        @staticmethod
        def isWearingNecklace(reference_name):
            """
            Returns True if Natsuki is wearing the specified necklace, otherwise False.

            IN: 
                - reference_name - The necklace reference name to check if Natsuki is wearing

            OUT:
                - True if Natsuki is wearing the specified necklace, otherwise False
            """
            return Natsuki._outfit.necklace.reference_name == reference_name
        
        @staticmethod
        def isWearingFacewear(reference_name):
            """
            Returns True if Natsuki is wearing the specified facewear, otherwise False.

            IN: 
                - reference_name - The facewear reference name to check if Natsuki is wearing

            OUT:
                - True if Natsuki is wearing the specified facewear, otherwise False
            """
            return Natsuki._outfit.facewear.reference_name == reference_name
        
        @staticmethod
        def isWearingBack(reference_name):
            """
            Returns True if Natsuki is wearing the specified back item, otherwise False.

            IN: 
                - reference_name - The back item reference name to check if Natsuki is wearing

            OUT:
                - True if Natsuki is wearing the specified back item, otherwise False
            """
            return Natsuki._outfit.back.reference_name == reference_name
        
        
        
        @staticmethod
        def getIdleImageTagsForAffinity():
            """
            Returns the idle image tags/name for Natsuki based on her current affinity state.

            OUT:
                - String image tags/name
            """
            if Natsuki.isEnamored(higher=True):
                return "natsuki idle enamored"
            
            elif Natsuki.isAffectionate(higher=True):
                return "natsuki idle affectionate"
            
            elif Natsuki.isHappy(higher=True):
                return "natsuki idle happy"
            
            elif Natsuki.isNormal(higher=True):
                return "natsuki idle normal"
            
            elif Natsuki.isDistressed(higher=True):
                return "natsuki idle distressed"
            
            else:
                return "natsuki idle ruined"
        
        @staticmethod
        def calculatedAffinityGain(base=1, bypass=False):
            """
            Adds a calculated amount to affinity, based on the player's relationship with Natsuki and daily cap state.

            NOTE:
                If the player has not confessed to Natsuki via the talk_i_love_you topic, further affinity gain is not possible
                until the confession has been made! This is to prevent players having Natsuki tell them she loves them unwarranted
                by accidentally crossing the boundary into LOVE.

            IN:
                - base - The base amount to use for the calculation
                - bypass - If the daily cap should be bypassed for things like one-time gifts, events, etc.
            """
            base = 10 if base > 10 else base
            to_add = base * jn_affinity.getRelationshipLengthMultiplier()
            if (
                not persistent._jn_player_confession_accepted 
                and (persistent.affinity + to_add) > (jn_affinity.AFF_THRESHOLD_LOVE -1)
            ):
                
                persistent.affinity = jn_affinity.AFF_THRESHOLD_LOVE -1
                jn_utils.log(bytes.fromhex("416666696e69747920626c6f636b6564202d20434e21").decode("utf-8"))
                return
            
            if bypass and persistent._affinity_daily_bypasses > 0:
                
                persistent.affinity += to_add
                persistent._affinity_daily_bypasses -= 1
                jn_utils.log(bytes.fromhex("416666696e6974792b20284229").decode("utf-8"))
            
            elif persistent.affinity_daily_gain > 0:
                
                persistent.affinity_daily_gain -= to_add
                persistent.affinity += to_add
                
                if persistent.affinity_daily_gain < 0:
                    persistent.affinity_daily_gain = 0
                
                jn_utils.log(bytes.fromhex("416666696e6974792b").decode("utf-8"))
            
            else:
                Natsuki.writeCap()
        
        @staticmethod
        def calculatedAffinityLoss(base=1):
            """
            Subtracts a calculated amount from affinity, based on the player's relationship with Natsuki.

            IN:
                - base - The base amount to use for the calculation
            """
            persistent.affinity -= base * jn_affinity.getRelationshipLengthMultiplier()
            jn_utils.log(bytes.fromhex("416666696e6974792d").decode("utf-8"))
        
        @staticmethod
        def percentageAffinityGain(percentage_gain):
            """
            Adds a percentage amount to affinity, with the percentage based on the existing affinity value.
            This bypasses the usual check, so this should only be used for one-off big gains.

            NOTE:
                If the player has not confessed to Natsuki via the talk_i_love_you topic, further affinity gain is not possible
                until the confession has been made! This is to prevent players having Natsuki tell them she loves them unwarranted
                by accidentally crossing the boundary into LOVE.

            IN:
                - percentage_gain - The integer percentage the affinity should increase by
            """
            percentage_gain = 10 if percentage_gain > 10 else percentage_gain
            to_add = persistent.affinity * (float(percentage_gain) / 100)
            if (not persistent._jn_player_confession_accepted and (persistent.affinity + to_add) > (jn_affinity.AFF_THRESHOLD_LOVE -1)):
                
                persistent.affinity = jn_affinity.AFF_THRESHOLD_LOVE -1
                jn_utils.log(bytes.fromhex("416666696e69747920626c6f636b6564202d20434e21").decode("utf-8"))
            
            else:
                persistent.affinity += to_add
                jn_utils.log(bytes.fromhex("416666696e6974792b").decode("utf-8"))
        
        @staticmethod
        def percentageAffinityLoss(percentage_loss):
            """
            Subtracts a percentage amount to affinity, with the percentage based on the existing affinity value.

            IN:
                - percentage_loss - The integer percentage the affinity should decrease by
            """
            if persistent.affinity == 0:
                persistent.affinity -= (float(percentage_loss) / 10)
            
            else:
                persistent.affinity -= abs(persistent.affinity * (float(percentage_loss) / 100))
            
            jn_utils.log(bytes.fromhex("416666696e6974792d").decode("utf-8"))
        
        @staticmethod
        def checkResetDailies():
            """
            Resets the daily affinity cap, if 24 hours has elapsed.
            """
            current_date = datetime.datetime.now() 
            if current_date in Natsuki._m1_natsuki__capped_aff_dates:
                return
            
            if not persistent.affinity_gain_reset_date:
                persistent.affinity_gain_reset_date = current_date
            
            elif current_date.day is not persistent.affinity_gain_reset_date.day:
                persistent.affinity_daily_gain = 5 * jn_affinity.getRelationshipLengthMultiplier()
                persistent.affinity_gain_reset_date = current_date
                persistent._affinity_daily_bypasses = 5
                persistent._jn_daily_joke_given = False
                jn_utils.log(bytes.fromhex("4461696c7920616666696e697479206361702072657365743b206e6577206361702069733a").decode("utf-8") + str(persistent.affinity_daily_gain))
        
        @staticmethod
        def writeCap():
            jn_utils.log(bytes.fromhex("4461696c7920616666696e69747920636170207265616368656421").decode("utf-8"))
            if not datetime.datetime.today().isoformat() in Natsuki._m1_natsuki__capped_aff_dates:
                Natsuki._m1_natsuki__capped_aff_dates.append(datetime.datetime.today().isoformat())
        
        @staticmethod
        def _m1_natsuki__isStateGreaterThan(aff_state):
            """
            Internal method to check if Natsuki's current affinity state is greater than the given amount
            """
            return jn_affinity._isAffStateWithinRange(
                Natsuki._getAffinityState(),
                (aff_state, None)
            )
        
        @staticmethod
        def _m1_natsuki__isStateLessThan(aff_state):
            """
            Internal method to check if Natsuki's current affinity state is less than or equal to the given amount
            """
            return jn_affinity._isAffStateWithinRange(
                Natsuki._getAffinityState(),
                (None, aff_state)
            )
        
        @staticmethod
        def _m1_natsuki__isAff(aff_state, higher=False, lower=False):
            """
            Internal comparison to check if Natsuki's current affection matches the given state,
            or is lower/higher as specified by arguments

            IN:
                aff_state - The affection state to check if Natsuki is at
                higher - bool, if Natsuki's affection can be greater than the current state
                    (Default: False)
                lower - bool, if Natsuki's affection can be less than the current state
                    (Default: False)
            """
            
            
            if higher and lower:
                return True
            
            if higher:
                return Natsuki._m1_natsuki__isStateGreaterThan(aff_state)
            
            elif lower:
                return Natsuki._m1_natsuki__isStateLessThan(aff_state)
            
            return Natsuki._getAffinityState() == aff_state
        
        
        @staticmethod
        def isRuined(higher=False, lower=False):
            """
            Checks if Natsuki's affection state is ruined, or is lower/higher as specified by arguments

            IN:
                higher - bool, if Natsuki's affection can be greater than the current state
                    (Default: False)
                lower - bool, if Natsuki's affection can be less than the current state
                    (Default: False)
            """
            return Natsuki._m1_natsuki__isAff(jn_affinity.RUINED, higher, lower)
        
        @staticmethod
        def isBroken(higher=False, lower=False):
            """
            Checks if Natsuki's affection state is broken, or is lower/higher as specified by arguments

            IN:
                higher - bool, if Natsuki's affection can be greater than the current state
                    (Default: False)
                lower - bool, if Natsuki's affection can be less than the current state
                    (Default: False)
            """
            return Natsuki._m1_natsuki__isAff(jn_affinity.BROKEN, higher, lower)
        
        @staticmethod
        def isDistressed(higher=False, lower=False):
            """
            Checks if Natsuki's affection state is distressed, or is lower/higher as specified by arguments

            IN:
                higher - bool, if Natsuki's affection can be greater than the current state
                    (Default: False)
                lower - bool, if Natsuki's affection can be less than the current state
                    (Default: False)
            """
            return Natsuki._m1_natsuki__isAff(jn_affinity.DISTRESSED, higher, lower)
        
        @staticmethod
        def isUpset(higher=False, lower=False):
            """
            Checks if Natsuki's affection state is upset, or is lower/higher as specified by arguments

            IN:
                higher - bool, if Natsuki's affection can be greater than the current state
                    (Default: False)
                lower - bool, if Natsuki's affection can be less than the current state
                    (Default: False)
            """
            return Natsuki._m1_natsuki__isAff(jn_affinity.UPSET, higher, lower)
        
        @staticmethod
        def isNormal(higher=False, lower=False):
            """
            Checks if Natsuki's affection state is normal, or is lower/higher as specified by arguments

            IN:
                higher - bool, if Natsuki's affection can be greater than the current state
                    (Default: False)
                lower - bool, if Natsuki's affection can be less than the current state
                    (Default: False)
            """
            return Natsuki._m1_natsuki__isAff(jn_affinity.NORMAL, higher, lower)
        
        @staticmethod
        def isHappy(higher=False, lower=False):
            """
            Checks if Natsuki's affection state is happy, or is lower/higher as specified by arguments

            IN:
                higher - bool, if Natsuki's affection can be greater than the current state
                    (Default: False)
                lower - bool, if Natsuki's affection can be less than the current state
                    (Default: False)
            """
            return Natsuki._m1_natsuki__isAff(jn_affinity.HAPPY, higher, lower)
        
        @staticmethod
        def isAffectionate(higher=False, lower=False):
            """
            Checks if Natsuki's affection state is affectionate, or is lower/higher as specified by arguments

            IN:
                higher - bool, if Natsuki's affection can be greater than the current state
                    (Default: False)
                lower - bool, if Natsuki's affection can be less than the current state
                    (Default: False)
            """
            return Natsuki._m1_natsuki__isAff(jn_affinity.AFFECTIONATE, higher, lower)
        
        @staticmethod
        def isEnamored(higher=False, lower=False):
            """
            Checks if Natsuki's affection state is enamored, or is lower/higher as specified by arguments

            IN:
                higher - bool, if Natsuki's affection can be greater than the current state
                    (Default: False)
                lower - bool, if Natsuki's affection can be less than the current state
                    (Default: False)
            """
            return Natsuki._m1_natsuki__isAff(jn_affinity.ENAMORED, higher, lower)
        
        @staticmethod
        def isLove(higher=False, lower=False):
            """
            Checks if Natsuki's affection state is love, or is lower/higher as specified by arguments

            IN:
                higher - bool, if Natsuki's affection can be greater than the current state
                    (Default: False)
                lower - bool, if Natsuki's affection can be less than the current state
                    (Default: False)
            """
            return Natsuki._m1_natsuki__isAff(jn_affinity.LOVE, higher, lower)
        
        @staticmethod
        def _getAffinityState():
            """
                returns current affinity state

                states:
                    RUINED = 1
                    BROKEN = 2
                    DISTRESSED = 3
                    UPSET = 4
                    NORMAL = 5
                    HAPPY = 6
                    AFFECTIONATE = 7
                    ENAMORED = 8
                    LOVE = 9

                OUT:
                    current affinity state
            """
            
            i = 1
            for threshold in [
                jn_affinity.AFF_THRESHOLD_LOVE,
                jn_affinity.AFF_THRESHOLD_ENAMORED,
                jn_affinity.AFF_THRESHOLD_AFFECTIONATE,
                jn_affinity.AFF_THRESHOLD_HAPPY,
                jn_affinity.AFF_THRESHOLD_NORMAL,
                jn_affinity.AFF_THRESHOLD_UPSET,
                jn_affinity.AFF_THRESHOLD_DISTRESSED,
                jn_affinity.AFF_THRESHOLD_BROKEN,
                jn_affinity.AFF_THRESHOLD_RUINED
            ]:
                
                
                if jn_affinity._compareAffThresholds(persistent.affinity, threshold) >= 0:
                    return jn_affinity._AFF_STATE_ORDER[-i]
                
                
                if threshold == jn_affinity.AFF_THRESHOLD_RUINED:
                    return jn_affinity._AFF_STATE_ORDER[0]
                
                i += 1
        
        def _getAffinityTierName():
            affinity_state = Natsuki._getAffinityState()
            if affinity_state == jn_affinity.ENAMORED:
                return "LOVE"
            
            elif affinity_state == jn_affinity.ENAMORED:
                return "ENAMORED"
            
            elif affinity_state == jn_affinity.AFFECTIONATE:
                return "AFFECTIONATE"
            
            elif affinity_state == jn_affinity.HAPPY:
                return "HAPPY"
            
            elif affinity_state == jn_affinity.NORMAL:
                return "NORMAL"
            
            elif affinity_state == jn_affinity.UPSET:
                return "UPSET"
            
            elif affinity_state == jn_affinity.DISTRESSED:
                return "DISTRESSED"
            
            elif affinity_state == jn_affinity.BROKEN:
                return "BROKEN"
            
            elif affinity_state == jn_affinity.RUINED:
                return "RUINED"
            
            else:
                store.jn_utils.log(
                    message="Unable to get tier name for affinity {0}; affinity_state was {1}".format(
                        store.persistent.affinity,
                        Natsuki._getAffinityState()
                    ),
                    logseverity=store.jn_utils.SEVERITY_WARN
                )
                return "UNKNOWN"
        
        
        
        @staticmethod
        def getForceQuitAttempt():
            """
            Gets the force quit attempt state.
            If True, the player attempted a force quit in this session that wasn't backed out of.
            """
            return Natsuki._is_force_quit_attempt
        
        @staticmethod
        def setForceQuitAttempt(force_quit):
            """
            Sets the force quit attempt state.

            IN:
                - force_quit - The bool force quit attempt state to set
            """
            Natsuki._is_force_quit_attempt = force_quit
        
        @staticmethod
        def addApology(apology_type):
            """
            Adds a new apology possiblity to the list of pending apologies.
            If the apology type is already present in the list, ignore it.

            IN:
                apology_type - The jn_apologies.ApologyTypes type to add.
            """
            if not isinstance(apology_type, int) and not isinstance(apology_type, jn_apologies.ApologyTypes):
                raise TypeError("apology_type must be of types int or jn_apologies.ApologyTypes")
            
            if not int(apology_type) in store.persistent._jn_player_pending_apologies:
                store.persistent._jn_player_pending_apologies.append(int(apology_type))
        
        @staticmethod
        def getQuitApology():
            """
            Gets the jn_apologies.ApologyTypes type to be checked on loading the game after quitting, or None if not set.
            """
            return jn_apologies.ApologyTypes(store.persistent._jn_player_apology_type_on_quit) if store.persistent._jn_player_apology_type_on_quit is not None else None
        
        @staticmethod
        def setQuitApology(apology_type):
            """
            Sets the jn_apologies.ApologyTypes type to be checked on loading the game after quitting.

            IN:
                apology_type - The jn_apologies.ApologyTypes type to add.
            """
            if not isinstance(apology_type, int) and not isinstance(apology_type, jn_apologies.ApologyTypes):
                raise TypeError("apology_type must be of types int or jn_apologies.ApologyTypes")
            
            store.persistent._jn_player_apology_type_on_quit = int(apology_type)
        
        @staticmethod
        def clearQuitApology():
            """
            Clears the quit apology type to be checked on loading the game after quitting.
            """
            store.persistent._jn_player_apology_type_on_quit = None
        
        @staticmethod
        def removeApology(apology_type):
            """
            Removes an apology from the list of pending apologies, if it exists.

            IN:
                apology_type - The jn_apologies.ApologyTypes type to add.
            """
            if not isinstance(apology_type, int) and not isinstance(apology_type, jn_apologies.ApologyTypes):
                raise TypeError("apology_type must be of types int or jn_apologies.ApologyTypes")
            
            if int(apology_type) in store.persistent._jn_player_pending_apologies:
                store.persistent._jn_player_pending_apologies.remove(int(apology_type))
        
        @staticmethod
        def setInConversation(is_in_conversation):
            """
            Marks Natsuki as being in a conversation with the player, or another dialogue flow.
            While in conversation, the hotkey buttons are disabled.

            IN:
                - is_in_conversation - The bool in conversation flag to set
                - reset_calls - bool whether to reset the idle and topic calls, preventing an immediate topic or idle call
            """
            if not isinstance(is_in_conversation, bool):
                raise TypeError("is_in_conversation must be of type bool")
            
            Natsuki._m1_natsuki__is_in_conversation = is_in_conversation
        
        @staticmethod
        def setInGame(is_in_game):
            """
            Marks Natsuki as being in a game with the player.
            While in a game, the player is marked as a cheater if they force quit, and can later apologize for it.

            IN:
                - is_in_game - The bool in game flag to set
                - reset_calls - bool whether to reset the idle and topic calls, preventing an immediate topic or idle call
            """
            if not isinstance(is_in_game, bool):
                raise TypeError("is_in_game must be of type bool")
            
            Natsuki._m1_natsuki__is_in_game = is_in_game
        
        @staticmethod
        def isInConversation():
            """
            Gets whether Natsuki is or is not currently in a conversation.
            While in conversation, the hotkey buttons are disabled.
            
            OUT:
                - True if in conversation, otherwise False
            """
            return Natsuki._m1_natsuki__is_in_conversation
        
        @staticmethod
        def isInGame():
            """
            Gets whether Natsuki is or is not currently playing a game.
            While in a game, the player is marked as a cheater if they force quit, and can later apologize for it.
            
            OUT:
                - True if in game, otherwise False
            """
            return Natsuki._m1_natsuki__is_in_game
        
        @staticmethod
        def getLastTopicCall():
            """
            Gets the time of the last topic call.
            """
            return Natsuki._m1_natsuki__last_topic_call
        
        @staticmethod
        def getLastIdleCall():
            """
            Gets the time of the last idle call.
            """
            return Natsuki._m1_natsuki__last_idle_call
        
        @staticmethod
        def getLastMenuCall():
            """
            Gets the time of the last menu call.
            """
            return Natsuki._m1_natsuki__last_menu_call
        
        @staticmethod
        def resetLastTopicCall():
            """
            Sets the time of the last topic call to the current time.
            """
            Natsuki._m1_natsuki__last_topic_call = datetime.datetime.now()
        
        @staticmethod
        def resetLastIdleCall():
            """
            Sets the time of the last idle call to the current time.
            """
            Natsuki._m1_natsuki__last_idle_call = datetime.datetime.now()
        
        @staticmethod
        def resetLastMenuCall():
            """
            Sets the time of the last menu call to the current time.
            """
            Natsuki._m1_natsuki__last_menu_call = datetime.datetime.now()
        
        @staticmethod
        def getMouseIsLeft():
            """
            Returns True if the mouse is to the left of Natsuki, otherwise False. Note this only accounts for Natsuki being centred!
            """
            current_mouse_pos = renpy.get_mouse_pos()[0]
            return current_mouse_pos > 0 and current_mouse_pos < 520
        
        @staticmethod
        def getMouseIsRight():
            """
            Returns True if the mouse is to the right of Natsuki, otherwise False. Note this only accounts for Natsuki being centred!
            """
            current_mouse_pos = renpy.get_mouse_pos()[0]
            return current_mouse_pos > 760
        
        @staticmethod
        def getMouseIsAbove():
            """
            Returns True if the mouse is above Natsuki, otherwise False. Note this only accounts for Natsuki being centred!
            """
            current_mouse_pos = renpy.get_mouse_pos()[1]
            return current_mouse_pos < 220
        
        @staticmethod
        def getMouseIsBelow():
            """
            Returns True if the mouse is below Natsuki, otherwise False. Note this only accounts for Natsuki being centred!
            """
            current_mouse_pos = renpy.get_mouse_pos()[1]
            return current_mouse_pos > 370
        
        @staticmethod
        def getIsReadingToRight():
            """
            Returns True if Natsuki's current reading direction for books is from left to right, otherwise False.
            """
            return Natsuki._is_reading_to_right
        
        @staticmethod
        def setIsReadingToRight(is_reading_from_right):
            """
            Sets Natsuki's current reading direction for right/left.
            For a traditional (Western) book read from left to right, this should be True.
            For a manga volume read from right to left, this should be False.

            IN:
                - is_reading_from_right - bool reading from right value to set
            """
            Natsuki._is_reading_to_right = is_reading_from_right
