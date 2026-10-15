# ============================================================
# shop.rpy
# Online shop... accessible from the Player Room.
# Extensible via SHOP_CATALOG (add new categories/items here).
# ============================================================

default bk_in_store = False
default bk_current_bg = ""
default bk_was_inside_dressing = False
default bk_companions_accepted = []
default bk_companions_raw = []
default bk_companions = []
default bk_saved_clothes = {}
default bk_had_sex = False
default bk_auto_witness = None
default bk_invite_list = []
default bk_invite_idx = 0
default bk_susp_idx = 0
default bk_react_idx = 0

init python:

    # Drinks come from the central alcohol registry (see alcohol.rpy).
    # Built here so the shop UI stays data-driven and prices never diverge.
    _shop_drink_items = [
        {"id": _did, "label": DRINKS[_did]["label"], "qty": 1, "price": DRINKS[_did]["price"]}
        for _did in DRINK_IDS
    ]

    SHOP_CATALOG = {
        "condoms": {
            "label": _("Condoms"),
            "items": [
                {"id": "condom", "label": _("Condom (x1)"),      "qty": 1, "price": 15},
                {"id": "condom", "label": _("Condom (x6-pack)"), "qty": 6, "price": 75},
            ]
        },
        "drinks": {
            "label": _("Drinks"),
            "items": _shop_drink_items,
        },
        "gifts": {
            "label": _("Gifts"),
            "items": [
                {"id": "chocolate",  "label": _("Chocolate Box"),  "qty": 1, "price": 20},
                {"id": "flowers",    "label": _("Flowers"),        "qty": 1, "price": 30},
                {"id": "perfume",    "label": _("Perfume"),        "qty": 1, "price": 60},
                {"id": "necklace",   "label": _("Necklace"),       "qty": 1, "price": 80},
                {"id": "handbag",    "label": _("Handbag"),        "qty": 1, "price": 100},
                {"id": "ring",       "label": _("Ring"),           "qty": 1, "price": 150},
                {"id": "watch",      "label": _("Designer Watch"), "qty": 1, "price": 500},
                {"id": "jewelry_set","label": _("Jewelry Set"),    "qty": 1, "price": 1000},
            ]
        },
        "gifts_gwen": {
            "label": _("Gifts for Gwen"),
            "items": [
                {"id": "piercing_gwen", "label": _("Nipple Piercings"), "qty": 1, "price": 200},
                {"id": "bikini_gwen",   "label": _("Black Bikini"),     "qty": 1, "price": 350},
            ]
        },
        "gifts_rogue": {
            "label": _("Gifts for Rogue"),
            "items": [
                {"id": "piercing_rogue", "label": _("Nipple Piercings"), "qty": 1, "price": 200},
                {"id": "bikini_rogue",   "label": _("Green Bikini"),     "qty": 1, "price": 350},
            ]
        },
        "gifts_ntw": {
            "label": _("Gifts for Negasonic"),
            "items": [
                {"id": "piercing_ntw", "label": _("Nipple Piercings"), "qty": 1, "price": 200},
                {"id": "bikini_ntw",   "label": _("Pink Bikini"),      "qty": 1, "price": 350},
            ]
        },
        "gifts_tenny": {
            "label": _("Gifts for Tenny"),
            "items": [
                {"id": "piercing_tenny", "label": _("Nipple Piercings"), "qty": 1, "price": 200},
                {"id": "bikini_tenny",   "label": _("Blue Bikini"),      "qty": 1, "price": 350},
            ]
        },
        "gifts_shion": {
            "label": _("Gifts for Shion"),
            "items": [
                {"id": "piercing_shion", "label": _("Nipple Piercings"), "qty": 1, "price": 200},
                {"id": "bikini_shion",   "label": _("Red Bikini"),       "qty": 1, "price": 350},
            ]
        },
        "pharmacy": {
            "label": _("Pharmacy"),
            "items": [
                {"id": "birth_control",      "label": _("Birth Control Pills"),         "qty": 1, "price": 50},
                {"id": "placebo_pills",      "label": _("Sunflower Fertility Shield"),  "qty": 1, "price": 30},
                {"id": "morning_after",      "label": _("Morning After Pill"),          "qty": 1, "price": 100},
                {"id": "fertility_vitamin",  "label": _("Fertility Vitamins"),          "qty": 1, "price": 200},
            ]
        },
    }

    # The "Gifts for <girl>" sections of the phone shop, in order: (SHOP_CATALOG key, gid, accent color).
    # Drawn by one loop (screen phone_shop_screen) and by the phone inventory; a girl whose optional
    # route is off (girl_route_enabled) has no section. A new girl = one row here + her catalog entry.
    PHONE_SHOP_GIRL_SECTIONS = (
        ("gifts_gwen",  "gwen",  "#e040fb"),
        ("gifts_rogue", "rogue", "#c45b7c"),
        ("gifts_ntw",   "ntw",   "#f5c842"),
        ("gifts_tenny", "tenny", "#7ecb8f"),
        ("gifts_shion", "shion", "#c084fc"),
    )

    # Gift stat effects: { item_id: { stat: amount, ... } }
    GIFT_EFFECTS = {
        "chocolate":  {"Love": 5,  "Obed": 5,  "Jealousy": -5},
        "flowers":    {"Love": 10, "Jealousy": -10},
        "perfume":    {"Love": 10, "Inbt": 5,  "Jealousy": -10},
        "necklace":   {"Love": 15, "Jealousy": -15},
        "handbag":   {"Love": 5,  "Inbt": 15,  "Jealousy": -5},
        "ring":       {"Love": 25, "Jealousy": -25},
        "watch":      {"Love": 15, "Obed": 20,  "Jealousy": -15},
        "jewelry_set":{"Love": 30, "Obed": 15, "Inbt": 20, "Jealousy": -30},
        "piercing_gwen": {"Obed": 15},
        "bikini_gwen":   {"Love": 10, "Lust": 5, "Jealousy": -10},
        "piercing_rogue": {"Obed": 15},
        "bikini_rogue":  {"Love": 10, "Lust": 5, "Jealousy": -10},
        "piercing_ntw":  {"Obed": 15},
        "bikini_ntw":    {"Love": 10, "Lust": 5, "Jealousy": -10},
        "piercing_tenny": {"Obed": 15},
        "bikini_tenny":   {"Love": 10, "Lust": 5, "Jealousy": -10},
        "piercing_shion": {"Obed": 15},
        "bikini_shion":   {"Love": 10, "Lust": 5, "Jealousy": -10},
        "blazing_flames":     {"Love": -5,  "Obed": -3},
        "my_hero_college":    {"Love": -5,  "Obed": -3},
        "one_frame_man":      {"Love": -5,  "Obed": -3},
        "supra_marcio_kart":  {"Love": -6,  "Obed": -4},
        "catch_monsters_89":  {"Love": -7,  "Obed": -5},
        "fuckpop_bobblehead": {"Love": -7,  "Obed": -5},
        "fuck_fuck_flush":    {"Love": -6,  "Obed": -4},
        "thisdendo_3ds":      {"Love": -10, "Obed": -8},
    }

    # Lookup: gift_id -> price (built from catalog)
    GIFT_PRICES = {}
    for _cat in SHOP_CATALOG.values():
        for _item in _cat.get("items", []):
            if _item["id"] not in GIFT_PRICES:
                GIFT_PRICES[_item["id"]] = _item["price"]
    GIFT_PRICES.update({
        "blazing_flames": 50, "my_hero_college": 50, "one_frame_man": 50,
        "supra_marcio_kart": 80, "catch_monsters_89": 100,
        "fuckpop_bobblehead": 100, "fuck_fuck_flush": 90, "thisdendo_3ds": 250,
    })

    # NPC gift effects by NPC trait key (base values, scaled by price/100)
    NPC_NERD_GIFT_EFFECTS = {
        "ntr":    {"friendship_with_player": 30, "suspicion": -10},
        "proud":  {"friendship_with_player": 10, "suspicion": -5},
        "normal": {"friendship_with_player": 20, "suspicion": -8},
    }

    NERD_GIFT_CATEGORY = {
        "blazing_flames": "game", "supra_marcio_kart": "game",
        "catch_monsters_89": "game", "thisdendo_3ds": "console",
        "my_hero_college": "manga", "one_frame_man": "manga",
        "fuckpop_bobblehead": "fuckpop",
        "fuck_fuck_flush": "plush",
    }

    NPC_NERD_GIFT_REFUSE = {
        "game": [
            _("Hey, you already gave me one of these! I haven't even finished it yet."),
            _("Dude, I'm still playing the last one you gave me. Slow down!"),
            _("I appreciate it, but I've got this one already. Maybe something different?"),
        ],
        "console": [
            _("Bro... I already have one of these. You gave it to me, remember?"),
            _("I love it, but I don't need two. One is enough!"),
        ],
        "manga": [
            _("I haven't finished reading what you gave me. Isn't this the same edition?"),
            _("Wait, I already have this volume. Did you forget?"),
            _("Same manga? Come on, at least get me the next volume!"),
        ],
        "fuckpop": [
            _("I know FuckPops are never too many, but this one I already have. You gave it to me!"),
            _("Dude, I literally have this exact one on my shelf. You put it there!"),
            _("A duplicate FuckPop? That's not how collecting works, man."),
        ],
        "plush": [
            _("Dude, you already gave me this plush. It's on my bed right now!"),
            _("Same plushie again? I only have so much room on the shelf, man."),
            _("I already have this one. Get me a different plush next time!"),
        ],
    }

    # NPC reaction lines by (trait_key, friendship_tier)
    NPC_NERD_GIFT_REACTIONS = {
        ("ntr", "hostile"): [
            _("Is... IS THAT THE NEW ONE?! HOLY... wait... why are you being nice to me? ...Whatever, I'm taking it."),
            _("NO FUCKING WAY, IS THAT... hold on. What's your angle here? ...Fine. Give it. NOW."),
            _("Dude... DUDE! That's the... okay calm down... I don't even like you but GIVE ME THAT."),
        ],
        ("ntr", "neutral"): [
            _("Wait... WAIT. Is this what I think it is?! ...Okay, you're still weird but THANK YOU."),
            _("BRO! THE LIMITED EDITION?! I... I mean... cool, I guess. ...Who am I kidding, THIS IS AMAZING."),
            _("Holy... you actually got me this? I... okay fine, you're not THAT bad. Sometimes. Rarely. Thanks!"),
        ],
        ("ntr", "friendly"): [
            _("NO WAY! IS THIS WHAT I THINK IT IS?! YOU'RE THE BEST, MAN!"),
            _("DUDE! I've been DYING to get my hands on this! You're a LEGEND!"),
            _("BRO, I could HUG you right now! This is AMAZING!"),
        ],
        ("proud", "hostile"): [
            _("...What is this supposed to be?"),
            _("Games? Really? I don't have time for this."),
            _("...Sure. I'll find a use for it. Maybe as a paperweight."),
        ],
        ("proud", "neutral"): [
            _("Oh, a gift. That's... thoughtful, I suppose. Thanks."),
            _("Hm. I wouldn't have picked this myself, but I appreciate the gesture."),
            _("This isn't really my thing, but... thanks."),
        ],
        ("proud", "friendly"): [
            _("Hm, actually... I've been curious about these. Thanks."),
            _("That's surprisingly considerate of you. I might actually enjoy this."),
            _("You know what, I'll give it a try. Thanks."),
        ],
        ("normal", "hostile"): [
            _("Oh... a gift? I don't know what to say to that."),
            _("That's... unexpected. Fine, I'll take it."),
            _("...Are you trying to bribe me or something?"),
        ],
        ("normal", "neutral"): [
            _("Hey, thanks! I needed something to kill time."),
            _("Oh, cool! I've heard good things about this one."),
            _("Nice! I'll check it out tonight."),
        ],
        ("normal", "friendly"): [
            _("Awesome! You wanna play together sometime?"),
            _("You always know what to get. Thanks, man!"),
            _("Sweet! I'm gonna binge this all weekend."),
        ],
    }

    def _npc_trait_key(npc):
        if npc.has_trait("ntr"):
            return "ntr"
        if npc.has_trait("proud"):
            return "proud"
        return "normal"

    def _npc_friendship_tier_key(npc):
        if npc.is_hostile():
            return "hostile"
        if npc.is_friendly():
            return "friendly"
        return "neutral"

    # ---------------------------------------------------------------- her taste in gifts (personality)
    # (docs/plan_personality_mechanics.md, approved 2026-09-19; no new item). Gift id -> multiplier on top of rich /
    # poor. >= GIFT_TASTE_LOVED she loves it, <= GIFT_TASTE_MEH it is not her thing: she says so (GIFT_TASTE_LINES),
    # always the first time (that reveals the taste on her status screen), then GIFT_TASTE_REPEAT of the times.
    GIRL_GIFT_TASTE = {
        "gwen":  {"necklace": 1.3, "flowers": 0.8, "perfume": 0.8, "handbag": 0.7},
        "rogue": {"flowers": 1.3, "chocolate": 1.3, "watch": 0.8},
        "ntw":   {"watch": 1.3, "chocolate": 1.2, "flowers": 0.5, "perfume": 0.6, "handbag": 0.6},
        "tenny": {"watch": 1.2, "chocolate": 1.2, "necklace": 0.9},
        # only the expensive things; cheap ones are an insult
        "shion": {"watch": 1.3, "jewelry_set": 1.3, "necklace": 1.2, "handbag": 1.2, "chocolate": 0.5, "flowers": 0.6},
    }
    GIFT_TASTE_LOVED = 1.2
    GIFT_TASTE_MEH = 0.8
    GIFT_TASTE_REPEAT = 0.5
    GIFT_TASTE_LINES = {
        "gwen": {
            "loved": [
                ("smile", _("Dark, simple and a little dramatic. You actually get my style.")),
                ("happy", _("Okay, this one I'm actually wearing. Every day.")),
            ],
            "meh": [
                ("bemused", _("It's nice. It's just... not really me.")),
                ("smirk", _("I'll find a place for it. Somewhere dark, where it can think about what it did.")),
            ],
        },
        "rogue": {
            "loved": [
                ("closed_happy", _("Now that's the way to a southern girl's heart, sugar.")),
                ("shy", _("You remembered what I like. Ain't nobody done that in a long time.")),
            ],
            "meh": [
                ("bemused", _("It's real fancy, sugar. Just not much use to a girl who lives by the sun.")),
                ("smile", _("It's pretty. I'll save it for special occasions. The very special ones.")),
            ],
        },
        "ntw": {
            "loved": [
                ("smirk", _("...Okay. That's actually good. Don't let it go to your head.")),
                ("smirk", _("Huh. You actually know what I like. That's new.")),
            ],
            "meh": [
                ("annoyed", _("What am I supposed to do with this?")),
                ("annoyed", _("You've met me, right? Try again.")),
            ],
        },
        "tenny": {
            "loved": [
                ("happy", _("You actually paid attention to what I like. That's rarer than you think.")),
                ("smirk", _("Great choice. Clearly evidence-based.")),
            ],
        },
        "shion": {
            "loved": [
                ("smug", _("Now this is a gift. You're learning what I'm worth.")),
                ("smirk", _("Good taste. I didn't expect that from you.")),
            ],
            "meh": [
                ("disgusted", _("Is this what you give the girls on campus? Take it back.")),
                ("annoyed", _("Cheap. Next time, don't bother.")),
            ],
        },
    }

    def gift_taste(girl, gift_id):
        """Her taste multiplier for this gift (1.0 = no opinion)."""
        return GIRL_GIFT_TASTE.get(getattr(girl, "gid", None), {}).get(gift_id, 1.0)

    GIFT_JEALOUSY_SOOTHE = 30     # a gift to his GIRLFRIEND calms her Jealousy by this much (x2 for one she loves)

    def gift_soothe_jealousy(girl, gift_id, mult=1.0):
        """A gift calms a jealous girlfriend (author 2026-10-04: 'dar presentes deveria diminuir'). Only while
        she is dating him (Jealousy is a girlfriend stat, like its daily decay); a gift she doesn't care for
        (taste <= GIFT_TASTE_MEH) soothes nothing, one she loves soothes double. `mult` = the caller's gift
        multiplier (fatigue of repeated gifts; <= 0 = she disliked the gesture itself: no soothing)."""
        if not (hasattr(girl, "is_dating_player") and girl.is_dating_player()):
            return
        if getattr(girl, "Jealousy", 0) <= 0 or mult <= 0:
            return
        _taste = gift_taste(girl, gift_id)
        if _taste <= GIFT_TASTE_MEH:
            print("[JEALOUSY] %s: gift %s is meh, no soothing" % (girl.gid, gift_id))
            return
        _amt = int(GIFT_JEALOUSY_SOOTHE * (2.0 if _taste >= GIFT_TASTE_LOVED else 1.0) * min(1.0, mult))
        if _amt <= 0:
            return
        Change_Status(girl, "Jealousy", -_amt)
        print("[JEALOUSY] %s: gift %s soothes -%d (now %d)" % (girl.gid, gift_id, _amt, getattr(girl, "Jealousy", 0)))

    def gift_taste_aside(girl, gift_id):
        """(face, line) she adds after her reaction to a gift she loves / doesn't care for, or None. The first time
        reveals that taste (discovered_gift_taste_<gift>: banner + her status screen)."""
        _m = gift_taste(girl, gift_id)
        _kind = "loved" if _m >= GIFT_TASTE_LOVED else ("meh" if _m <= GIFT_TASTE_MEH else None)
        if _kind == "loved":
            unlock_achievement("perfect_gift")
        _pool = GIFT_TASTE_LINES.get(getattr(girl, "gid", None), {}).get(_kind) if _kind else None
        if not _pool:
            return None
        _flag = "discovered_gift_taste_" + gift_id
        if girl.get_flag(_flag) and renpy.random.random() >= GIFT_TASTE_REPEAT:
            return None
        girl.discover(_flag)
        print("[PERSONA] %s: gift %s = %s (x%.2f)" % (girl.gid, gift_id, _kind, _m))
        return renpy.random.choice(_pool)

    def gift_taste_discovered(girl):
        """([gifts she loves], [gifts she doesn't care for]) he already found out, display names."""
        _loved, _meh = [], []
        for _gift, _m in GIRL_GIFT_TASTE.get(getattr(girl, "gid", None), {}).items():
            if not girl.get_flag("discovered_gift_taste_" + _gift):
                continue
            if _m >= GIFT_TASTE_LOVED:
                _loved.append(_tr(GIFT_DISPLAY.get(_gift, _gift)))
            elif _m <= GIFT_TASTE_MEH:
                _meh.append(_tr(GIFT_DISPLAY.get(_gift, _gift)))
        return _loved, _meh

    def get_gift_multiplier(girl, gift_id):
        _price = GIFT_PRICES.get(gift_id, 50)
        if girl.has_trait("rich"):
            _mult = 0.1 + 0.4 * min(1.0, _price / 150.0)
        elif girl.has_trait("poor"):
            _mult = 1.5
        else:
            _mult = 1.0
        return _mult * gift_taste(girl, gift_id)

    # Gift IDs exempt from weekly fatigue (one-time unlocks / customization)
    GIFT_FATIGUE_EXEMPT = set()
    for _gid_key in ("gwen", "rogue", "ntw", "tenny", "shion"):
        GIFT_FATIGUE_EXEMPT.add("piercing_" + _gid_key)
        GIFT_FATIGUE_EXEMPT.add("bikini_" + _gid_key)

    def _gift_weekly_cap(girl):
        """Weekly gift cap: poor girls accept more, rich girls tire faster."""
        if girl.has_trait("poor"):
            return 10
        if girl.has_trait("rich"):
            return 5
        return 7

    def _gift_same_item_max(girl):
        """Same-item cap: poor tolerates more repeats, rich hates them."""
        if girl.has_trait("poor"):
            return 4
        if girl.has_trait("rich"):
            return 2
        return 3

    def _gift_fatigue_cleanup(girl):
        """Remove entries older than 7 days from the gift log."""
        _log = getattr(girl, "_gift_week_log", [])
        _current_day = store.Day
        girl._gift_week_log = [(d, gid) for d, gid in _log if _current_day - d < 7]

    def _gift_week_count(girl):
        """Total non-exempt gifts given this week."""
        _gift_fatigue_cleanup(girl)
        return len(getattr(girl, "_gift_week_log", []))

    def _gift_same_item_count(girl, gift_id):
        """How many times this exact item was given this week."""
        _gift_fatigue_cleanup(girl)
        return sum(1 for d, gid in getattr(girl, "_gift_week_log", []) if gid == gift_id)

    def _gift_fatigue_multiplier(girl, gift_id):
        """Returns stat multiplier based on same-item repetition this week.
        1st: 1.0, 2nd: 0.5, at cap: rejected (0.0).
        Poor: 1.0 / 0.7 / 0.4 / rejected (4th).
        Rich: 1.0 / rejected (2nd)."""
        _count = _gift_same_item_count(girl, gift_id)
        _max = _gift_same_item_max(girl)
        if _count >= _max - 1:
            return 0.0
        if girl.has_trait("poor"):
            return max(0.3, 1.0 - (_count * 0.3))
        if girl.has_trait("rich"):
            return max(0.3, 1.0 - (_count * 0.7))
        return max(0.3, 1.0 - (_count * 0.5))

    def _gift_register(girl, gift_id):
        """Record a gift in the weekly log."""
        if not hasattr(girl, "_gift_week_log"):
            girl._gift_week_log = []
        girl._gift_week_log.append((store.Day, gift_id))

    def _pharmacy_popup(item_label, qty, price):
        # StatHolder shows "[label_text]" (never translated there): _pk_t = the tl pair of a _()-marked label, else _I18N
        renpy.show_screen(
            "StatHolder", value=qty, prefix="+", color="#38bdf8",
            xpos=0.5, ypos=0.35, label_text=_pk_t(item_label),
            hide_tag="stat_pharm_item", _tag="stat_pharm_item",
        )
        renpy.show_screen(
            "StatHolder", value=price, prefix="-", color="#4ade80",
            xpos=0.5, ypos=0.42, label_text="$",
            hide_tag="stat_pharm_cash", _tag="stat_pharm_cash",
        )

    def phone_buy_item(item_id, qty, price):
        """Buy an item from the phone shop UI."""
        if Player.cash >= price:
            Player.spend_cash(price)
            Player.add_item(item_id, qty)
            return True
        return False

    # Display names for inventory UI
    GIFT_DISPLAY = {
        "chocolate": _("Chocolate Box"),
        "flowers":   _("Flowers"),
        "perfume":   _("Perfume"),
        "necklace":  _("Necklace"),
        "handbag":  _("Handbag"),
        "ring":           _("Ring"),
        "watch":          _("Designer Watch"),
        "jewelry_set":    _("Jewelry Set"),
        "piercing_gwen":  _("Nipple Piercings (Gwen)"),
        "bikini_gwen":    _("Black Bikini (Gwen)"),
        "piercing_rogue": _("Nipple Piercings (Rogue)"),
        "bikini_rogue":   _("Green Bikini (Rogue)"),
        "piercing_ntw":   _("Nipple Piercings (Negasonic)"),
        "bikini_ntw":     _("Pink Bikini (Negasonic)"),
        "piercing_tenny": _("Nipple Piercings (Tenny)"),
        "bikini_tenny":   _("Blue Bikini (Tenny)"),
        "piercing_shion": _("Nipple Piercings (Shion)"),
        "bikini_shion":   _("Red Bikini (Shion)"),
        "blazing_flames":       _("Blazing Flames"),
        "my_hero_college":      _("My Hero College"),
        "one_frame_man":        _("One Frame Man"),
        "supra_marcio_kart":    _("Super Shopping Cart"),
        "catch_monsters_89":    _("Catch Monsters 89"),
        "fuckpop_bobblehead":   _("FuckPop Bobblehead"),
        "fuck_fuck_flush":      _("Fuck Fuck Flush"),
        "thisdendo_3ds":        _("Thisdendo 3DS"),
        "birth_control":        _("Birth Control Pills"),
        "placebo_pills":        _("Sunflower Fertility Shield"),
        "morning_after":        _("Morning After Pill"),
        "fertility_vitamin":    _("Fertility Vitamins"),
    }

    NERD_GIFT_IDS = {
        "blazing_flames", "my_hero_college", "one_frame_man",
        "supra_marcio_kart", "catch_monsters_89",
        "fuckpop_bobblehead", "fuck_fuck_flush", "thisdendo_3ds",
    }

    # =============================================================
    # VIDEO SELLING... Pricing System
    # =============================================================

    # Base price by video type (more explicit = more valuable)
    VIDEO_BASE_PRICE = {
        "masturbate": 20,
        "hj":         28,
        "fj":         32,
        "tj":         35,
        "rj":         60,
        "bj":         42,
        "cowgirl":    55,
        "reverse_cowgirl":      55,
        "reverse_cowgirl_anal": 70,
        "doggy":      55,
        "full_nelson": 55,
        "full_nelson_anal": 70,
        "laying_down": 55,
        "laying_anal": 70,
        "anal":       70,
        "creampie":   85,
    }

    VIDEO_TYPE_DISPLAY = {
        "masturbate": "Masturbation",
        "hj":         "Handjob",
        "fj":         "Footjob",
        "tj":         "Titjob",
        "rj":         "Rimjob",
        "bj":         "Blowjob",
        "cowgirl":    "Cowgirl",
        "reverse_cowgirl":      "Reverse Cowgirl",
        "reverse_cowgirl_anal": "Reverse Cowgirl Anal",
        "doggy":      "Doggy Style",
        "full_nelson": "Full Nelson",
        "full_nelson_anal": "Full Nelson Anal",
        "laying_down": "Laying Down",
        "laying_anal": "Laying Down Anal",
        "anal":       "Anal",
        "creampie":   "Creampie",
    }

    SPECIAL_VIDEO_DISPLAY = {
        "virginity":  "LOSING VIRGINITY",
    }

    def video_sell_price(vid):
        """Calculate the sell value of a recorded video."""
        base = VIDEO_BASE_PRICE.get(vid.get("type", "hj"), 40)
        mult = 1.0

        is_secret = not vid.get("consensual", True)
        is_cheating = vid.get("committed", False)

        # Non-consensual (secretly recorded): riskier content
        if is_secret:
            mult += 0.5

        # Girl has a boyfriend (cheating/scandal factor)
        if is_cheating:
            mult += 0.5

        # Both secret AND cheating: extra premium
        if is_secret and is_cheating:
            mult += 0.5

        # Face hidden: less valuable (can't identify her)
        if vid.get("face_hidden", False):
            mult *= 0.65

        # HD quality: TekMix Camera produces better content
        if vid.get("hd", False):
            mult += 0.6

        # Cuckold/threesome: niche fetish content
        if vid.get("cuckold", False):
            mult += 0.7
        elif vid.get("threesome", False):
            mult += 0.5

        return int(base * mult)

    def video_sell_label(vid):
        """Build a display label for a sellable video."""
        girl = GIRL_BY_ID.get(vid.get("girl_gid"))
        name = girl.Name if girl else vid.get("girl_gid", "???")
        vtype = _tr(VIDEO_TYPE_DISPLAY.get(vid.get("type", "?"), vid.get("type", "?")))
        price = video_sell_price(vid)

        tags = []
        if vid.get("hd", False):
            tags.append("HD")
        if not vid.get("consensual", True):
            tags.append(_tr("secret"))
        if vid.get("committed", False):
            tags.append(_tr("cheating"))
        if vid.get("cuckold", False):
            tags.append(_tr("cuckold"))
        elif vid.get("threesome", False):
            tags.append(_tr("threesome"))
        if vid.get("face_hidden", False):
            tags.append(_tr("face hidden"))
        if vid.get("atm", False):
            tags.append(_tr("ATM"))
            vtype += " (ATM)"

        lbl = "%s \u2014 %s \u2014 $%d" % (name, vtype, price)
        if tags:
            lbl += "  (%s)" % ", ".join(tags)
        return lbl

    # =============================================================
    # BIGFANS... Formatting helpers
    # =============================================================

    def bigfans_format_number(n):
        """Format large numbers: 10000 -> '10k', 1500000 -> '1.5m', etc."""
        if n >= 1000000:
            v = n / 1000000.0
            return ("%gm" % round(v, 1)) if v != int(v) else ("%dm" % int(v))
        elif n >= 10000:
            return "%dk" % (n // 1000)
        return str(n)

    # =============================================================
    # BIGFANS... Fan Request System
    # =============================================================

    # Secret girl profiles — the girl is watching her own videos
    BIGFANS_GIRL_PROFILES = {
        "gwen": "JustGwirl",
        "rogue": "SouthernMystery",
        "ntw": "screwuwade",
        "tenny": "SecretRed",
    }

    # Trait-based secret request phrases (written in character, hinting it's HER)
    # Each entry: (phrase, type_required, tag_required)
    # type_required = specific video type or None for any
    # tag_required = "cheating", "public", or None
    _GIRL_SECRET_PHRASES = {
        "cum_slut": [
            (_("uh... do you think you could... finish inside her? like, a lot, multiple times? I'd really like to see that..."), "creampie", None),
            (_("can you fill her up and film it? I want to see every drop... please..."), "creampie", None),
            (_("I just... I need to see what it looks like when someone cums inside. like, raw. no condom. can you do that?"), "creampie", None),
            (_("is it weird that I want to see her swallow? like, all of it? asking for... research purposes..."), "bj", None),
        ],
        "public_fetish": [
            (_("what about doing something in public? I bet the danger makes it SO much hotter... the thrill... I want SO badly for you to do this"), None, "public"),
            (_("imagine getting caught... in the open... that would be insane. can you film something public?"), None, "public"),
            (_("somewhere outside. where anyone could see. PLEASE. I need this."), None, "public"),
        ],
        "hardcore_sex": [
            (_("I want to see you go HARD. like, really rough. don't hold back. she can take it."), "reverse_cowgirl", None),
            (_("grab her, pull her hair, go fast. I want to see her lose control completely."), "reverse_cowgirl", None),
            (_("do it so hard she can't walk straight after. film everything."), "cowgirl", None),
        ],
        "cute_sex": [
            (_("can you be gentle with her? like, slow and sweet? I want to see something romantic for once..."), "cowgirl", None),
            (_("not everything has to be rough... can you film something tender? like you actually care about her?"), None, None),
            (_("hold her hand while you do it. I know that sounds weird. just... please?"), None, None),
        ],
        "camera_lover": [
            (_("she looks SO good on camera. can you get more of her face? she seems to love the attention..."), None, None),
            (_("I think she likes being filmed... can you zoom in on her expressions? she's perfect..."), "bj", None),
            (_("more content with her. she was born for this. every angle, every reaction."), None, None),
        ],
        "loyal": [
            (_("does she... does she have a boyfriend? because I want to see what she does behind his back..."), None, "cheating"),
            (_("she looks like the faithful type. which makes it SO much hotter. get her to cheat on camera."), None, "cheating"),
            (_("I bet her boyfriend thinks she's innocent... show me how wrong he is."), None, "cheating"),
        ],
        "exhibitionist": [
            (_("she clearly loves being seen... give her an audience. film her somewhere public."), None, "public"),
            (_("I can tell she wants people to watch. so let them. film her where anyone could see."), None, "public"),
        ],
        "voyeur": [
            (_("I want to watch her watching someone else. or... watching herself on camera. meta, I know."), None, None),
            (_("film her reaction when she sees herself on screen. I bet she can't look away."), None, None),
        ],
        "nerd": [
            (_("this is purely for academic purposes. I'm studying human arousal responses and I need... visual data. detailed visual data."), None, None),
            (_("hypothetically, if someone wanted to observe the physiological effects of... intimate contact... for a paper... could you film something? asking for a colleague."), None, None),
            (_("I've been analyzing your content from a behavioral science perspective. your subject's involuntary responses are... fascinating. I need more samples."), None, None),
            (_("I read that recording intimate encounters can increase dopamine by 40%. I need to verify. empirically. with your next video. please."), None, None),
        ],
        "_default": [
            (_("I'm a huge fan. can you make something special? anything goes. I'll pay well."), None, None),
            (_("I keep coming back to your page... can you film something new? surprise me."), None, None),
            (_("more content please. you have no idea how much I look forward to your uploads."), None, None),
        ],
    }

    def _generate_girl_secret_request(girl):
        """Create a BigFans request from the girl's secret profile.
        Picks phrases based on her traits. Returns a request dict or None."""
        profile = BIGFANS_GIRL_PROFILES.get(girl.gid)
        if not profile:
            return None

        # Pick trait-based phrase pool (priority order)
        pool = []
        for trait in ("cum_slut", "public_fetish", "hardcore_sex", "cute_sex",
                      "camera_lover", "loyal", "exhibitionist", "voyeur", "nerd"):
            if girl.has_trait(trait) and trait in _GIRL_SECRET_PHRASES:
                pool.extend(_GIRL_SECRET_PHRASES[trait])
        if not pool:
            pool = list(_GIRL_SECRET_PHRASES["_default"])

        phrase, req_type, req_tag = renpy.random.choice(pool)

        if hasattr(girl, "has_npc_partner") and girl.has_npc_partner() and girl.get_flag("partner_is_female"):
            _plbl = girl.partner_label()
            phrase = phrase.replace("boyfriend", _plbl)
            phrase = phrase.replace(_(" his "), _(" her "))
            phrase = phrase.replace(_(" he "), _(" she "))

        req = {}
        if not hasattr(store.Player, "bigfans_next_id"):
            store.Player.bigfans_next_id = 1
        req["id"] = store.Player.bigfans_next_id
        store.Player.bigfans_next_id += 1

        req["fan_name"] = profile
        req["type"] = req_type
        req["girl_gid"] = None  # she doesn't specify the girl (would be too obvious)
        req["secret"] = None
        req["public"] = True if req_tag == "public" else None
        req["cheating"] = True if req_tag == "cheating" else None
        req["_girl_secret"] = girl.gid  # internal flag for tracking

        # Reward — girl requests pay well (she's spending her own money on this)
        base = VIDEO_BASE_PRICE.get(req_type, 50) if req_type else 60
        mult = 1.8  # premium for secret requests
        if req.get("cheating"):
            mult += 0.5
        if req.get("public"):
            mult += 0.3
        req["reward"] = int(base * mult)
        req["min_duration"] = 0

        req["phrase"] = phrase

        req["created_day"] = store.Day
        req["expire_day"] = store.Day + renpy.random.randint(3, 5)
        req["fulfilled"] = False

        return req

    # Supporters / Patrons — always included in fan name pool
    BIGFANS_SUPPORTERS = [
        "Alinmus", "anbogir0", "CavemanJohnson", "Dc4604",
        "DD", "demonsla3r", "elmuchacho", "Erutamni",
        "EthanAdams", "Hunt4Bugs", "Idel66123", "InSync",
        "Jonathan", "Kri", "LavantWilliams", "LOG",
        "Lordathand", "lsaine", "mikeHarder", "NahidHassan",
        "Raincario", "RayTrevy", "Senditexpress", "Steel",
        "Superninja", "TeMechanic04", "Thanatos", "Totempol13",
        "UnusualAlias", "Xevec", "YesNo", "Zerafu",
        "Zetsu",
    ]

    BIGFANS_FAN_NAMES = [
        "3dh", "AaronCrane", "AbsoluteZero777", "AdamEvans",
        "AdorableViking", "Ahri", "Aleks", "AlfieBrooks",
        "AlfonsoSwan-Waterman", "AllenSaylor", "Ameno", "Anonymous",
        "Anthony", "arcodawgs", "Arer", "AriShaffir",
        "arthemios", "asdfasdf", "asharevans", "Aster",
        "Atrineas", "Austinmayer", "BadBait28", "BestGoat",
        "BigRed", "Bill", "Billy", "birb",
        "Blackstatic95.", "Blandon", "Bluebolt", "BobLe",
        "BobParker", "BrandonBailey", "BrandonH.", "BurakDinler",
        "Cakemixgod", "Candyman5700", "CaptainPoncho", "Captainryan117",
        "CharlieHart", "Cheef_Teef", "ChocolaSan", "Chrisblkchris",
        "ChristianAlcantar", "ChristianJakob", "ChristophPanagl", "CJ",
        "Coldheart48", "ColeDelaney", "ColesAsinus", "CommanderAndrew2015",
        "Corvalist", "CorwinFenton", "CptBlitz", "CraigShmelvin",
        "CrimsonRocket", "Cuilean", "d", "Dakon",
        "DamienLeonard", "Danekiller", "Darkosim", "DatDromedary",
        "DavidDavidson", "DavidHill", "DiegoAndrade", "dkyviontucker",
        "Doli", "Domestos2013", "DominicBergeron", "Doug",
        "Drake", "drumSNIPER", "edward1997", "Egmi",
        "Elektrolaus", "Enigma", "EvilTiger", "falloutjunky",
        "FiftyRings", "Firekampfer", "FischerMichael", "Flashborn",
        "FoxyDesu", "FoxyHome", "Friendspeak", "Fritz",
        "Gabriel", "GaetanCrivellari", "gard110", "GinoPrimo",
        "Godeatingyggdreisl", "GoGoGadget", "GoldCookie", "Gray-iwnl-",
        "Greaperassassin", "GreatSun", "GriffinForrest", "Gt_burns",
        "GuanQiangJi", "HairyHal", "HazeEDaze", "HermitGuru",
        "HesuS5", "Hopefullynothing", "HungryCarrot", "HunterHartsell",
        "Hykap", "IanKurrle", "illomen1991", "ILuvGames",
        "Imortald", "IronKing", "IsaacPiper", "Isak",
        "J", "JacobMorris", "JanelleChristmas101", "jaredfromsubway",
        "jasonbaker", "Jasso", "javierdarkuroko", "Jay",
        "JayLother", "JeffersondaSilva", "Jinkiesboy", "JJMC",
        "Jman7753", "JoanJordanaTristany", "John", "JohnGentilini",
        "JohnSmith", "Jon-DavidPepperman", "JosephStalin", "Jsk32",
        "JuanFernandez", "JuicyWaterBomb", "justinnebrigich", "Jynx",
        "K", "Kaida", "kamikamikaze", "KCArnao",
        "Ken", "kenifffff", "KingWebbly", "KirkWilson",
        "Klingetod", "KyleShepherd", "LakrixDevroux", "LazarusDraken",
        "LeeRedding", "liam", "Ligma", "Llord",
        "LMP", "LoganWheeler", "LugDee", "luigid",
        "LukeT", "lummur", "lummy", "LynTel",
        "M", "Mackenzie", "madcreeper", "MarcusSample",
        "Matt", "Mbsheros", "MechaWeeb", "Michael",
        "MichalPeksa", "Monfane", "MONOLITHICC", "Moonseeds",
        "MoonToTheMoon", "Mr.Mann", "Mr.Pillz", "MumEverest",
        "Munity", "Mutant", "N", "Narwing",
        "NateColds", "NathanParks", "Nathum", "NeptuneBlueSoul",
        "NightSky", "NoOne", "nope", "NPC123",
        "NSFWasabi", "Obsolete", "OldMariner", "Omarhashem",
        "OneLonelyBoi", "Onit42", "OnScreenGalaxy", "OrpheusOnFilm",
        "ParkerHughes", "Passerby", "Patreonizer", "Patrick",
        "PB", "PhilChandler", "Pirinaise", "PotofGreed",
        "ProbablyAnonymous", "ProTaco", "PugetDolphin", "pumpkinmeerkat",
        "Raben449", "Raekwon", "Rafz98", "RagnaRock",
        "RancidFish", "RandallDevine", "Rapter0303", "RashidiHenry",
        "Rc", "RedSerpant", "Rhotisserie", "RhysWhite",
        "Rieth", "RoadyRoad", "robertmartin", "RobertoBanales",
        "RomanDean", "RyanG", "Sageoson", "sanscross",
        "SaulParada", "ScarletChaos", "SebastienGre", "SeniorDeer957",
        "SethSalry", "Shawn", "Shep-N7", "SjugduMigFastar",
        "SkitariiRanger", "sloth", "SmellyVirgin", "sn123412",
        "Sounds", "spamfajitas", "Spasticaction", "SPT12",
        "Stardust013", "stella", "StephenGlover", "StephenWeaver",
        "Steve", "SteveCook", "stink", "SubaruHarem",
        "sunburst", "SuperDuck", "TaaviPaas", "TakerPokerus",
        "TallanteKarc", "TCoffin", "TedHaidydei", "teubiont",
        "thatsneakyfkr", "TheChazz", "TheCoverts", "TheCrispyDud",
        "thedawg", "TheEvilDuckLord", "TheFool", "TheGameGuild",
        "TheGoonJr", "ThomasPenner", "ToddGrooby", "TossyHunter",
        "Tranq", "Tre'Rhodeman", "TRlegacy", "Tsuka",
        "turv", "TuVieja", "Tyler", "UlisesRios",
        "Umbros", "UnitSingle", "Unk", "UsefulJk",
        "Vermin", "WallyD", "WantedNewKidD", "Warriolx76",
        "waterboy", "weeabootrash", "wenacomparexdlol", "WesleyWilliams",
        "WhyAmISober", "WillFar", "WilliamBeavis", "WilliamDavis",
        "wing", "Wolf", "WytchDr", "Xyzie",
        "yamirei", "YourLocalSadBoyo", "Youwa", "Zach",
        "ZenTheRat", "Zer0Akira808", "ZeroBlaze", "zeus20010",
        "zolas",
    ] + BIGFANS_SUPPORTERS * 5

    BIGFANS_REQUEST_PHRASES = {
        "hj":         [
            _("I wanna see her hands at work"),

            _("Show me a good handjob vid"),

            _("Need some handwork content asap"),

        ],
        "tj":         [
            _("Titjob content is so rare, hook me up"),

            _("I need a good titjob clip"),

            _("Big fan of titjobs, send one over"),

        ],
        "bj":         [
            _("Blowjob vid pls, the sloppier the better"),

            _("I need some good head content"),

            _("Show me what that mouth can do"),

        ],
        "cowgirl":    [
            _("Cowgirl riding vid, take my money"),

            _("I want to see her ride like a pro"),

            _("Need a cowgirl clip, don't disappoint"),

        ],
        "reverse_cowgirl": [
            _("Reverse cowgirl is the best angle"),

            _("I need a reverse cowgirl vid, that view is everything"),

            _("Show me that reverse cowgirl bounce"),

        ],
        "reverse_cowgirl_anal": [
            _("Reverse cowgirl anal? That view plus the back door, send it"),

            _("I want her riding reverse with it in her ass, premium stuff"),

            _("Reverse cowgirl, back door. Best angle there is for that"),

        ],
        "doggy":      [
            _("Doggy style vid, that's the classic"),

            _("I need a good doggy clip, raw energy"),

            _("Hit it from the back on camera for me"),

        ],
        "anal":       [
            _("Anal content is premium, send it over"),

            _("I need a good anal vid, don't hold back"),

            _("Back door action, that's what I'm here for"),

        ],
        "full_nelson": [
            _("Full nelson vid, I love that position"),

            _("Hold her up and go hard, full nelson style"),

            _("I need some full nelson content, that grip is everything"),

        ],
        "full_nelson_anal": [
            _("Full nelson anal? Now THAT's premium content"),

            _("Hold her up and take the back door, full nelson style"),

            _("Full nelson anal is the ultimate, send it over"),

        ],
        "laying_down": [
            _("Laying down vid, I love that angle"),

            _("I want to see her on her back, nice and slow"),

            _("Lay her down and film it, that position is underrated"),

        ],
        "laying_anal": [
            _("Laying down anal? That's the good stuff"),

            _("On her back, back door. Premium combo right there"),

            _("I need a laying anal vid, don't hold back"),

        ],
        "masturbate": [
            _("Solo content hits different, send one"),

            _("A good masturbation vid would be perfect"),

            _("I just want to see her enjoy herself"),

        ],
        "creampie":   [
            _("Creampie vid... that's the good stuff"),

            _("I need a creampie clip, no pulling out"),

            _("Fill her up on camera, I'll pay extra"),

        ],
        "any_cheating": [
            _("I want something forbidden, cheating content"),

            _("Show me something scandalous, she got a man?"),

            _("Cheating vids hit different, send one over"),

            _("I need that drama... got any cheating content?"),

        ],
        "any_public": [
            _("Public stuff is so risky, I love it"),

            _("Got anything filmed in public? That's my thing"),

            _("I wanna see something outdoors, public vibes"),

            _("Public videos are the best, send one"),

        ],
    }

    def _bigfans_pick_phrase(req):
        """Pick a random flavor phrase for a request, with optional duration/face requirements."""
        vtype = req.get("type")
        if vtype is None:
            variant = req.get("_any_variant", "cheating")
            key = "any_cheating" if variant == "cheating" else "any_public"
            phrases = BIGFANS_REQUEST_PHRASES.get(key, BIGFANS_REQUEST_PHRASES["any_cheating"])
        else:
            phrases = BIGFANS_REQUEST_PHRASES.get(vtype, BIGFANS_REQUEST_PHRASES["masturbate"])
        base = _tl(renpy.random.choice(phrases))
        _min = req.get("min_duration", 0)
        if _min > 0:
            _mins = _min // 60
            _dur_phrases = [
                _(" Make it at least %d minutes though!"),
                _(" But nothing short, at least %d min!"),
                _(" I want a long one, %d+ minutes!"),
                _(" Give me something proper, %d min minimum."),
            ]
            base += _tl(renpy.random.choice(_dur_phrases)) % _mins
        _fp = req.get("face_pref")
        if _fp == "explicit":
            base += _tl(renpy.random.choice([
                _(" I want to see her face clearly!"),

                _(" Make sure her face is visible."),

                _(" No hiding, I want full face."),

            ]))
        elif _fp == "hidden":
            base += _tl(renpy.random.choice([
                _(" The mystery is hotter, keep her face hidden."),

                _(" I like when they hide their face, more anonymous."),

                _(" Face hidden is fine, adds to the thrill."),

            ]))
        if req.get("hd"):
            base += _tl(renpy.random.choice([
                _(" Make it HD quality, none of that blurry phone stuff."),
                _(" High quality only! I want to see every detail."),
                _(" HD or nothing, I'm not paying for potato quality."),
            ]))
        if req.get("cuckold"):
            base += _tl(renpy.random.choice([
                _(" I want to see someone watching. The cuck angle is gold."),
                _(" Make sure the boyfriend is watching. That's the whole point."),
                _(" Cuckold content only. I need the watcher in frame."),
            ]))
        elif req.get("threesome"):
            base += _tl(renpy.random.choice([
                _(" I want a threesome video, another girl involved."),
                _(" Give me one with two girls. That's premium content."),
                _(" Threesome content, I'll pay extra for that."),
            ]))
        return base

    def generate_bigfans_request():
        """Create one random BigFans request dict."""
        req = {}

        # ID (getattr for save compat)
        if not hasattr(store.Player, "bigfans_next_id"):
            store.Player.bigfans_next_id = 1
        req["id"] = store.Player.bigfans_next_id
        store.Player.bigfans_next_id += 1

        # Fan name
        req["fan_name"] = renpy.random.choice(BIGFANS_FAN_NAMES)

        # Type: 70% specific, 15% any+cheating, 15% any+public
        _roll = renpy.random.randint(1, 100)
        if _roll <= 70:
            req["type"] = renpy.random.choice(list(VIDEO_BASE_PRICE.keys()))
        elif _roll <= 85:
            req["type"] = None  # any video — cheating required
            req["_any_variant"] = "cheating"
        else:
            req["type"] = None  # any video — public required
            req["_any_variant"] = "public"

        # Girl: never specified by fans
        req["girl_gid"] = None

        # Tags
        req["secret"] = None
        req["public"] = None

        # Cheating: 25% on specific types, forced on any_cheating
        if req.get("_any_variant") == "cheating":
            req["cheating"] = True
        elif req.get("_any_variant") == "public":
            req["cheating"] = None
            req["public"] = True
        else:
            req["cheating"] = True if renpy.random.randint(1, 100) <= 25 else None
            req["public"] = True if renpy.random.randint(1, 100) <= 15 else None

        # Reward calculation
        if req["type"] is not None:
            base = VIDEO_BASE_PRICE.get(req["type"], 50)
        else:
            base = 50

        mult = 1.0
        if req["cheating"]:
            mult += 0.5
        if req.get("public"):
            mult += 0.3

        # Private request premium (requests always pay more than feed)
        mult += 0.3

        # Face preference: explicit (35%), hidden (15%), any (50%)
        # Doggy is always face-hidden (rear-facing pose), so never request explicit
        _face_roll = renpy.random.randint(1, 100)
        if _face_roll <= 35 and req.get("type") not in ("doggy",):
            req["face_pref"] = "explicit"
            mult += 0.2
        elif _face_roll <= 50:
            req["face_pref"] = "hidden"
        else:
            req["face_pref"] = "any"

        # Duration requirement: 30% chance to want a longer video
        if renpy.random.random() < 0.30:
            _min_dur = renpy.random.choice([180, 240, 300, 360])  # 3, 4, 5, 6 minutes
            req["min_duration"] = _min_dur
            mult += 0.4  # longer videos pay more
        else:
            req["min_duration"] = 0

        # HD requirement: 25% chance if player owns the TekMix Camera
        if Player.has_item("tekmix_camera") and renpy.random.random() < 0.25:
            req["hd"] = True
            mult += 0.3
        else:
            req["hd"] = False

        # Cuckold/threesome requirement: 15% chance if player has such videos
        _player_vids = getattr(store.Player, "recorded_videos", [])
        _has_cuck = any(v.get("cuckold") for v in _player_vids)
        _has_three = any(v.get("threesome") for v in _player_vids)
        if (_has_cuck or _has_three) and renpy.random.random() < 0.15:
            if _has_cuck and _has_three:
                _pick = renpy.random.choice(["cuckold", "threesome"])
                req[_pick] = True
            elif _has_cuck:
                req["cuckold"] = True
            else:
                req["threesome"] = True
            mult += 0.4

        # Supporters pay double
        _is_supporter = req["fan_name"] in BIGFANS_SUPPORTERS
        if _is_supporter:
            mult *= 2.0

        req["reward"] = int(base * mult)

        # Flavor phrase
        req["phrase"] = _bigfans_pick_phrase(req)

        # Expiry: supporters give more time (4-6 days), others 2-4
        req["created_day"] = store.Day
        if _is_supporter:
            req["expire_day"] = store.Day + renpy.random.randint(4, 6)
        else:
            req["expire_day"] = store.Day + renpy.random.randint(2, 4)
        req["fulfilled"] = False

        return req

    def bigfans_daily_refresh():
        """Remove expired/fulfilled requests, generate new ones, cap at 3."""
        if not hasattr(store.Player, "bigfans_requests"):
            store.Player.bigfans_requests = []
        reqs = store.Player.bigfans_requests

        # Remove expired or fulfilled
        reqs = [r for r in reqs if not r["fulfilled"] and r["expire_day"] >= store.Day]
        store.Player.bigfans_requests = reqs

        # Girl secret request: 20% daily chance per girl (if player has videos of her)
        # Only one secret request active at a time per girl
        _active_secret_gids = {r.get("_girl_secret") for r in reqs if r.get("_girl_secret")}
        _player_vids = getattr(store.Player, "recorded_videos", [])
        for _g in girls_reachable():
            if _g.gid in BIGFANS_GIRL_PROFILES and _g.gid not in _active_secret_gids:
                # Must have at least 1 published video of this girl
                _has_vid = any(v.get("girl_gid") == _g.gid and v.get("published", False) for v in _player_vids)
                if _has_vid and renpy.random.random() < 0.20 and len(reqs) < 4:
                    _secret_req = _generate_girl_secret_request(_g)
                    if _secret_req:
                        reqs.append(_secret_req)

        # Generate new requests up to 3 total (not counting girl secrets)
        _normal_reqs = [r for r in reqs if not r.get("_girl_secret")]
        spots = 3 - len(_normal_reqs)
        new_count = 0
        if spots > 0:
            if len(_normal_reqs) == 0:
                # No active requests: always generate at least 1
                new_count = 1
            else:
                # 75% chance of 1 request
                new_count = 1 if renpy.random.randint(1, 100) <= 75 else 0
            for _ in range(new_count):
                reqs.append(generate_bigfans_request())

        return new_count

    # Locations considered "public" for BigFans requests
    def bigfans_video_matches_request(req, vid):
        """Check if a video dict satisfies all criteria of a request."""
        if vid.get("sold", False):
            return False
        if vid.get("published", False):
            return False

        # Type check
        if req["type"] is not None and vid.get("type") != req["type"]:
            return False

        # Girl check
        if req["girl_gid"] is not None and vid.get("girl_gid") != req["girl_gid"]:
            return False

        # Cheating check (committed=True means cheating)
        if req["cheating"] is True and not vid.get("committed", False):
            return False

        # Public check (video must be filmed in a public location)
        if req.get("public") is True and vid.get("location", "room") not in store.PUBLIC_LOCATIONS:
            return False

        # Face preference check
        _face_pref = req.get("face_pref", "any")
        if _face_pref == "explicit" and vid.get("face_hidden", False):
            return False
        if _face_pref == "hidden" and not vid.get("face_hidden", False):
            return False

        # Duration check
        _min_dur = req.get("min_duration", 0)
        if _min_dur > 0:
            _vid_dur = bigfans_video_duration_seconds(vid)
            if _vid_dur < _min_dur:
                return False

        # HD check
        if req.get("hd") and not vid.get("hd", False):
            return False

        # Cuckold/threesome check
        if req.get("cuckold") and not vid.get("cuckold", False):
            return False
        if req.get("threesome") and not vid.get("threesome", False):
            return False

        return True

    def bigfans_fulfill_request(req, vid):
        """Fulfill a request: pay reward, mark both as done."""
        req["fulfilled"] = True
        vid["sold"] = True
        store.Player.add_cash(req["reward"])
        if req.get("_girl_secret"):
            unlock_achievement("secret_admirer")

    def bigfans_request_label(req):
        """Build a short tag line for a request's criteria."""
        if req["type"] is not None:
            lbl = _tr(VIDEO_TYPE_DISPLAY.get(req["type"], req["type"]))
        else:
            lbl = _tr("Any video")

        tags = []
        if req.get("hd"):
            tags.append("HD")
        if req.get("cheating"):
            tags.append(_tr("cheating"))
        if req.get("public"):
            tags.append(_tr("public"))
        if req.get("cuckold"):
            tags.append(_tr("cuckold"))
        elif req.get("threesome"):
            tags.append(_tr("threesome"))
        _fp = req.get("face_pref", "any")
        if _fp == "explicit":
            tags.append(_tr("face visible"))
        elif _fp == "hidden":
            tags.append(_tr("face hidden"))
        _min = req.get("min_duration", 0)
        if _min > 0:
            tags.append("%dm+" % (_min // 60))
        if tags:
            lbl += " (%s)" % ", ".join(tags)

        return lbl

    # =============================================================
    # BIGFANS... Feed & Publishing System
    # =============================================================

    def bigfans_publish_video(vid):
        """Publish a video to the BigFans feed for passive income.
        Returns None so Function() action does not end the interaction."""
        if vid.get("published", False):
            return
        if vid.get("sold", False):
            return

        vid["published"] = True

        if not hasattr(store.Player, "bigfans_published"):
            store.Player.bigfans_published = []
        if not hasattr(store.Player, "bigfans_total_earnings"):
            store.Player.bigfans_total_earnings = 0
        if not hasattr(store.Player, "bigfans_subscribers"):
            store.Player.bigfans_subscribers = 10

        if not hasattr(store.Player, "_bigfans_seq"):
            store.Player._bigfans_seq = 0
        store.Player._bigfans_seq += 1

        entry = {
            "vid": vid,
            "published_day": store.Day,
            "published_seq": store.Player._bigfans_seq,
            "total_views": 0,
            "total_earned": 0,
            "daily_views": 0,
        }
        store.Player.bigfans_published.insert(0, entry)

        # Publishing gains subscribers
        sub_gain = renpy.random.randint(2, 8)
        is_secret = not vid.get("consensual", True)
        is_cheating = vid.get("committed", False)
        if is_secret:
            sub_gain += renpy.random.randint(3, 6)
        if is_cheating:
            sub_gain += renpy.random.randint(2, 5)
        store.Player.bigfans_subscribers += sub_gain

    def bigfans_daily_income():
        """Generate daily views and passive income for all published videos.
        Called once per day (e.g. from daily refresh). Returns total earned today."""
        if not hasattr(store.Player, "bigfans_published"):
            store.Player.bigfans_published = []
        if not hasattr(store.Player, "bigfans_total_earnings"):
            store.Player.bigfans_total_earnings = 0
        if not hasattr(store.Player, "bigfans_subscribers"):
            store.Player.bigfans_subscribers = 10

        subs = store.Player.bigfans_subscribers
        total_today = 0
        published = store.Player.bigfans_published
        num_vids = len(published)

        # View multiplier by content intensity (heavier = more views)
        _VIEW_MULT = {
            "masturbate": 1.0,
            "hj":         1.3,
            "tj":         1.5,
            "bj":         1.8,
            "cowgirl":    2.5,
            "reverse_cowgirl":      2.5,
            "reverse_cowgirl_anal": 3.0,
            "doggy":      2.5,
            "anal":       3.0,
            "full_nelson": 2.5,
            "full_nelson_anal": 3.0,
            "laying_down": 2.5,
            "laying_anal": 3.0,
            "creampie":   3.5,
        }

        # Diversity bonus: unique video types give a small boost
        _unique_types = set(e["vid"].get("type", "hj") for e in published)
        _diversity_mult = 1.0 + (len(_unique_types) - 1) * 0.1  # +10% per unique type

        # Catalog size bonus: gentle scaling, not explosive
        _catalog_mult = 1.0 + min(num_vids, 10) * 0.05  # +5% per vid, cap at +50%

        for entry in published:
            vid = entry["vid"]
            age = store.Day - entry["published_day"]
            vtype = vid.get("type", "hj")

            # Base views: small numbers (15-52 base)
            type_mult = _VIEW_MULT.get(vtype, 1.3)
            base_views = int(15 * type_mult)

            # Subscriber bonus: modest
            sub_views = int(subs * renpy.random.uniform(0.1, 0.3) * type_mult)

            # Freshness: newer videos get more views
            if age <= 1:
                fresh_mult = 1.8
            elif age <= 3:
                fresh_mult = 1.3
            elif age <= 7:
                fresh_mult = 1.0
            else:
                fresh_mult = max(0.3, 0.8 - (age - 7) * 0.05)

            # Scandal bonus
            scandal_mult = 1.0
            if not vid.get("consensual", True):
                scandal_mult += 0.3
            if vid.get("committed", False):
                scandal_mult += 0.2
            if vid.get("cuckold", False):
                scandal_mult += 0.5
            elif vid.get("threesome", False):
                scandal_mult += 0.4
            if vid.get("special") == "virginity":
                scandal_mult += 1.5

            # Face hidden penalty: less engagement
            _face_mult = 0.6 if vid.get("face_hidden", False) else 1.0

            # HD bonus: better quality = more views
            _hd_mult = 1.4 if vid.get("hd", False) else 1.0

            # Random variance
            variance = renpy.random.uniform(0.8, 1.2)

            views = int((base_views + sub_views) * fresh_mult * scandal_mult * _diversity_mult * _catalog_mult * _face_mult * _hd_mult * variance)
            views = max(5, views)

            # Income per view: very low — passive income is supplementary
            # Target: ~$1-5/day per video early, ~$5-15 with many vids
            rate = 0.008 + (type_mult * 0.003)
            income = int(views * renpy.random.uniform(rate * 0.8, rate * 1.2))
            income = max(1, income)

            entry["daily_views"] = views
            entry["total_views"] += views
            entry["total_earned"] += income
            total_today += income

        if total_today > 0:
            store.Player.add_cash(total_today)
            store.Player.bigfans_total_earnings += total_today

        # Track daily earnings history (last 7 days for chart)
        if not hasattr(store.Player, "bigfans_earnings_history"):
            store.Player.bigfans_earnings_history = []
        store.Player.bigfans_earnings_history.append({"day": store.Day, "earned": total_today})
        # Keep only last 7
        if len(store.Player.bigfans_earnings_history) > 7:
            store.Player.bigfans_earnings_history = store.Player.bigfans_earnings_history[-7:]

        # Subscriber growth: slow and steady
        if num_vids > 0:
            store.Player.bigfans_subscribers += renpy.random.randint(0, 1 + min(num_vids, 5))

        return total_today

    def bigfans_unpublish_video(entry):
        """Remove a video from the feed."""
        if not hasattr(store.Player, "bigfans_published"):
            return
        entry["vid"]["published"] = False
        store.Player.bigfans_published.remove(entry)

    # Title templates for published videos — {loc} replaced with location phrase
    _FEED_TITLES = {
        "masturbate": [
            _("Caught her touching herself {loc}"),

            _("Solo session {loc}"),

            _("She couldn't wait... {loc}"),

            _("Private moment {loc}"),

            _("Naughty solo time {loc}"),

            _("When she thinks nobody is watching {loc}"),

            _("Self-love {loc}"),

            _("All alone and loving it {loc}"),

            _("Her fingers know exactly where to go {loc}"),

            _("She moans even when she's alone {loc}"),

            _("Caught on camera before she noticed {loc}"),

            _("She didn't know I was watching {loc}"),

            _("Solo but loud {loc}"),

            _("She finished before I even walked in {loc}"),

        ],
        "hj": [
            _("Giving me a hand {loc}"),

            _("Quick handy {loc}"),

            _("She grabbed it {loc}"),

            _("Handjob session {loc}"),

            _("Her grip is something else {loc}"),

            _("She knows what she's doing {loc}"),

            _("Hands on experience {loc}"),

            _("She couldn't keep her hands off {loc}"),

            _("Two hands and still not enough {loc}"),

            _("She strokes like a pro {loc}"),

            _("Her hand did all the talking {loc}"),

            _("She didn't let go until the job was done {loc}"),

            _("Fastest hands {loc}"),

            _("She grabbed it and wouldn't let go {loc}"),

        ],
        "tj": [
            _("Between her tits {loc}"),

            _("Titjob heaven {loc}"),

            _("She put them to work {loc}"),

            _("Squeezed between {loc}"),

            _("Perfect fit {loc}"),

            _("Those tits are unreal {loc}"),

            _("Sliding between the best pair {loc}"),

            _("She wrapped them around me {loc}"),

            _("Natural pillows {loc}"),

            _("She pressed them together and looked up at me {loc}"),

            _("The best use for those perfect tits {loc}"),

            _("She spit on them and squeezed tighter {loc}"),

            _("Titjob POV you won't forget {loc}"),

            _("Between her tits with eye contact {loc}"),

        ],
        "bj": [
            _("On her knees {loc}"),

            _("She swallowed it all {loc}"),

            _("Sloppy blowjob {loc}"),

            _("Deep throat session {loc}"),

            _("She didn't miss a drop {loc}"),

            _("Mouth game on point {loc}"),

            _("Best head I ever got {loc}"),

            _("She went all the way down {loc}"),

            _("She looked up at me the whole time {loc}"),

            _("Throat so deep she couldn't breathe {loc}"),

            _("She sucks like her life depends on it {loc}"),

            _("Sloppy, wet, and she's loving it {loc}"),

            _("Her lips don't stop until I'm done {loc}"),

            _("She took it so deep her eyes watered {loc}"),

        ],
        "cowgirl": [
            _("She rode me {loc}"),

            _("Cowgirl ride {loc}"),

            _("Bouncing on top {loc}"),

            _("She took control {loc}"),

            _("She wouldn't stop riding {loc}"),

            _("The view from below {loc}"),

            _("Grinding on top {loc}"),

            _("She pinned me down {loc}"),

            _("She rode until her legs gave out {loc}"),

            _("POV of her bouncing on me {loc}"),

            _("She controls the pace and I let her {loc}"),

            _("Best view in the world {loc}"),

            _("She grinds slow then goes full speed {loc}"),

            _("Her hips don't lie {loc}"),

        ],
        "creampie": [
            _("Creampied her {loc}"),

            _("Filled her up {loc}"),

            _("I didn't pull out {loc}"),

            _("Deep inside {loc}"),

            _("No pulling out today {loc}"),

            _("She wanted every drop {loc}"),

            _("Breeding session {loc}"),

            _("Raw and uncut {loc}"),

            _("Overflowing {loc}"),

            _("She told me to pull out. I pushed deeper instead {loc}"),

            _("Full load. Zero regrets {loc}"),

            _("She felt every single drop go inside {loc}"),

            _("The moment I finished inside and she moaned louder {loc}"),

            _("Dripping after I was done {loc}"),

            _("No condom. No pullout. No mercy {loc}"),

            _("She clenched when she felt it coming {loc}"),

            _("I came so deep she gasped {loc}"),

            _("Watch the exact moment I fill her up {loc}"),

            _("She tried to pull away. Too late {loc}"),

            _("Raw finish deep inside {loc}"),

        ],
        "anal": [
            _("She took it in the ass {loc}"),

            _("Anal session {loc}"),

            _("Back door open {loc}"),

            _("She let me hit it from behind... the other hole {loc}"),

            _("Straight to anal. No warm up {loc}"),

            _("She said 'wrong hole'. I said 'right hole' {loc}"),

            _("The tightest fit {loc}"),

            _("She bit the pillow and took every inch {loc}"),

            _("Anal debut {loc}"),

            _("She clenched so hard I almost couldn't move {loc}"),

            _("The forbidden hole {loc}"),

            _("She walked funny the next day {loc}"),

            _("Deep in her ass and she's asking for more {loc}"),

            _("She said she'd never try it. Look at her now {loc}"),

        ],
        "full_nelson": [
            _("Full nelson time {loc}"),

            _("Picked her up and didn't put her down {loc}"),

            _("She lost control of her body {loc}"),

            _("Held in the air and pounded {loc}"),

            _("Full nelson. She couldn't even squirm {loc}"),

            _("She went limp after the first minute {loc}"),

            _("Feet off the ground, eyes rolling back {loc}"),

            _("No escape from this position {loc}"),

            _("She screamed so loud the walls shook {loc}"),

            _("Ragdoll treatment {loc}"),

            _("Suspended and destroyed {loc}"),

            _("She begged to be put down. I went harder {loc}"),

            _("Her legs were shaking before I even started thrusting {loc}"),

            _("Full nelson until she couldn't form words {loc}"),

        ],
    }

    _FEED_LOC_PHRASES = {
        "campus": _("on campus"),
        "room": _("in my room"),
        "pool": _("at the pool"),
        "showers": _("in the showers"),
        "shower": _("in the showers"),
        "gym": _("at the gym"),
        "classroom": _("in the classroom"),
        "gwen_room": _("in her room"),
        "rogue_room": _("in her room"),
        "ntw_room": _("in her room"),
        "tenny_room": _("in her room"),
        "mall": _("at the mall"),
        "restaurant_restroom": _("in the restroom"),
        "dressing_room": _("in the dressing room"),
        "apartment": _("in the apartment"),
        "apartment_room": _("in the bedroom"),
        "apartment_shower": _("in the bathroom"),
    }

    # ── Trait-aware title pools ──
    # Each key is a trait/condition tag. Titles may use {loc}.
    # Checked in priority order; first matching pool wins.
    _FEED_TITLES_TRAIT = {
        # --- Cheating (committed == True) ---
        "cheating": [
            _("She has a boyfriend but she chose me \U0001F608"),

            _("Her boyfriend doesn't know about this \U0001F64A"),

            _("He thinks she's faithful... LOL \U0001F921"),

            _("Cheating on her man {loc} \U0001F525"),

            _("She said she has a boyfriend. I said I don't care \U0001F608"),

            _("Someone's girlfriend is very naughty \U0001F525"),

            _("Sorry bro, she's mine now \U0001F60F"),

            _("While her boyfriend is away... \U0001F440"),

            _("He's texting her during this. She didn't stop \U0001F4F1"),

            _("Her boyfriend has no idea she does this \U0001F92B"),

            _("Taken girl, but she keeps coming back \U0001F501"),

            _("She told him she was studying \U0001F4DA\U0001F608"),

            _("His girl sneaks out to see me every week \U0001F92B"),

            _("She changes my name in her phone to 'Mom' \U0001F4F1\U0001F608"),

            _("She showers before going back to him \U0001F6BF\U0001F92B"),

            _("Her boyfriend liked my post. If only he knew \U0001F4F1\U0001F921"),

            _("She puts his photo face down before we start \U0001F5BC\U0001F608"),

            _("He dropped her off at my place. Thanks bro \U0001F697\U0001F608"),

            _("She wore the necklace he gave her while with me \U0001F4CE\U0001F608"),

            _("Monday is for him. The rest of the week is mine \U0001F4C5\U0001F60F"),

            _("She saves her best outfits for when she visits me \U0001F457\U0001F525"),

            _("He pays for dinner. I get dessert \U0001F370\U0001F608"),

        ],
        # --- Hate cum ---
        "hate_cum": [
            _("She hates cum but I don't care \U0001F608"),

            _("She begged me not to cum on her... oops \U0001F92D"),

            _("She HATES cum but look at that face \U0001F4A6\U0001F624"),

            _("Every drop she didn't want \U0001F4A6"),

            _("She literally gags when she sees cum LOL \U0001F923"),

            _("She told me she hates it. I gave her extra \U0001F608"),

            _("Her face when she realizes I'm about to finish \U0001F631"),

            _("Anti-cum girl vs the inevitable \U0001F4A6\U0001F645"),

            _("She runs but she can't hide from it \U0001F3C3\U0001F4A6"),

            _("She flinches every time I get close to finishing \U0001F631"),

            _("She hates every drop and I love every second \U0001F608\U0001F4A6"),

            _("She made a disgusted face. I kept going. \U0001F92D"),

            _("Her least favorite thing is my favorite thing \U0001F4A6\U0001F608"),

            _("She closes her eyes and prays it's over fast \U0001F64F\U0001F4A6"),

        ],
        # --- Cum slut ---
        "cum_slut": [
            _("She begged for every single drop \U0001F4A6\U0001F60D"),

            _("This girl is ADDICTED to cum \U0001F4A6\U0001F525"),

            _("She won't let me pull out. Ever. \U0001F92F"),

            _("Cum slut paradise \U0001F4A6\U0001F60B"),

            _("She said 'more' after I was already done \U0001F629"),

            _("She gets mad if I waste a single drop \U0001F620\U0001F4A6"),

            _("Watch her face light up when I finish \U0001F929\U0001F4A6"),

            _("She collects it like it's gold \U0001F4B0\U0001F4A6"),

            _("She opens her mouth before I even say I'm close \U0001F4A6\U0001F60B"),

            _("She licks her lips and waits like a good girl \U0001F4A6\U0001F929"),

            _("Three rounds and she still wants more \U0001F4A6\U0001F525"),

            _("She smiled and said 'that's not enough' \U0001F4A6\U0001F608"),

            _("She didn't waste a single drop. Not one. \U0001F4A6\U0001F60D"),

            _("Her favorite dessert \U0001F4A6\U0001F370"),

        ],
        # --- No condom (penetration/creampie only) ---
        "no_condom": [
            _("She told me to use a condom. I came inside \U0001F608"),

            _("Raw every single time and she keeps coming back \U0001F525"),

            _("Condoms? We don't do that here \U0001F6AB\U0001F92B"),

            _("She said 'put on a condom'. I said 'no' \U0001F608"),

            _("No protection, no regrets \U0001F525"),

            _("She made me promise to use one... I lied \U0001F92D"),

            _("Breeding material {loc} \U0001F525"),

            _("Raw and unprotected. Just how she secretly likes it \U0001F92B"),

            _("She brought condoms. I threw them away \U0001F5D1\U0001F608"),

            _("Skin to skin, the way nature intended \U0001F525"),

            _("She stopped asking about condoms after the third time \U0001F92D"),

            _("Condom? Never heard of it \U0001F937\U0001F608"),

            _("She said raw feels different. She's right. \U0001F525"),

            _("I ripped it off halfway through and she didn't complain \U0001F608"),

        ],
        # --- Hardcore sex ---
        "hardcore_sex": [
            _("She likes it ROUGH \U0001F525\U0001F4A5"),

            _("She begged me to go harder \U0001F62C"),

            _("She likes to be slapped in the face when getting fucked \U0001F44B\U0001F525"),

            _("The harder I go, the louder she gets \U0001F525\U0001F50A"),

            _("She doesn't break. I tried. \U0001F608"),

            _("Rough enough to leave marks \U0001F525"),

            _("She said 'don't hold back'. I didn't. \U0001F62C\U0001F4A5"),

            _("This girl can take a pounding {loc} \U0001F4AA"),

            _("She said 'harder' until she couldn't talk anymore \U0001F92B"),

            _("She bruises easy but never complains \U0001F525\U0001F608"),

            _("The neighbors filed a noise complaint \U0001F50A\U0001F525"),

            _("She screamed so loud she lost her voice \U0001F525\U0001F62C"),

            _("Her throat is sore and she's smiling about it \U0001F608"),

            _("She bit the pillow so hard it ripped \U0001F4A5"),

            _("Rough is an understatement {loc} \U0001F525\U0001F62C"),

        ],
        # --- Cute sex ---
        "cute_sex": [
            _("The cutest moans you'll ever hear \U0001F970"),

            _("She gets so shy but doesn't want to stop \U0001F633\U0001F495"),

            _("Gentle with her... she's precious \U0001F49D"),

            _("Those little sounds she makes \U0001F3B5\U0001F970"),

            _("She covers her face but keeps going \U0001F648\U0001F495"),

            _("Adorable AND naughty {loc} \U0001F970\U0001F525"),

            _("She whispers 'be gentle' every time \U0001F92B\U0001F495"),

            _("Soft moans and blushing {loc} \U0001F633"),

            _("She bites her lip and looks away when it feels too good \U0001F633"),

            _("Every little moan sounds like a melody \U0001F3B6\U0001F970"),

            _("She holds my hand during the whole thing \U0001F495"),

            _("So sweet it doesn't even feel like porn {loc} \U0001F970"),

            _("She says 'sorry' when she moans too loud \U0001F633\U0001F495"),

            _("The most gentle girl I've ever been with {loc} \U0001F49D"),

        ],
        # --- Camera hater (secret recording) ---
        "camera_hater": [
            _("She has NO IDEA I'm recording this \U0001F4F7\U0001F92B"),

            _("Secret footage. She would kill me \U0001F4F1\U0001F480"),

            _("Filmed without permission... worth it \U0001F608\U0001F3AC"),

            _("She told me NO cameras. I didn't listen \U0001F4F5\U0001F608"),

            _("Hidden camera footage {loc} \U0001F4F7\U0001F440"),

            _("What she doesn't know won't hurt her \U0001F92B"),

            _("She'd delete this if she knew it existed \U0001F5D1\U0001F92B"),

            _("Top secret recording {loc} \U0001F575"),

            _("Phone propped up where she can't see it \U0001F4F1\U0001F92B"),

            _("She would end me if she finds this video \U0001F480\U0001F608"),

            _("The angle she doesn't know about {loc} \U0001F4F7\U0001F608"),

            _("I told her the camera was off. It wasn't \U0001F92B\U0001F3AC"),

            _("She specifically said no recording. Oops \U0001F608"),

            _("Leaked footage she never approved \U0001F4F7\U0001F525"),

        ],
        # --- Camera lover ---
        "camera_lover": [
            _("She LOVES being on camera \U0001F4F8\U0001F60D"),

            _("She asked ME to record this \U0001F3AC\U0001F525"),

            _("Born to be a star \U00002B50\U0001F4F7"),

            _("She performs better when the camera's on \U0001F3AC\U0001F525"),

            _("POV: she knows you're watching \U0001F440\U0001F609"),

            _("She made sure the angle was perfect \U0001F4F8\U0001F48B"),

            _("Natural in front of the camera {loc} \U0001F3AC\U0001F31F"),

            _("She checked the footage and said 'post it' \U0001F608"),

            _("She held the camera herself for the best angle \U0001F4F8\U0001F525"),

            _("She winks at the camera like a pro \U0001F609\U0001F3AC"),

            _("She asked to see the preview and said 'perfect' \U0001F4F8\U0001F60D"),

            _("Camera on = performance mode activated \U0001F3AC\U0001F525"),

            _("She poses between rounds for the camera \U0001F4F8\U0001F48B"),

            _("She said 'make sure you get my good side' \U0001F4F7\U0001F609"),

        ],
        # --- Public fetish ---
        "public_fetish": [
            _("She WANTED people to see \U0001F440\U0001F525"),

            _("She gets off knowing someone could walk in {loc} \U0001F6AA\U0001F440"),

            _("Exhibition time {loc} \U0001F525\U0001F3AA"),

            _("She picked the riskiest spot on purpose \U0001F608"),

            _("The thrill of getting caught {loc} \U0001F525"),

            _("She dared me to do it {loc} and I didn't hesitate \U0001F4AA"),

            _("Public and proud of it \U0001F3C6\U0001F440"),

            _("She loves an audience \U0001F3AD\U0001F525"),

            _("She gets wetter the more people are around \U0001F440\U0001F525"),

            _("She moaned extra loud so they could hear {loc} \U0001F50A\U0001F608"),

            _("Someone walked by. She smiled and kept going \U0001F6B6\U0001F608"),

            _("The riskier the spot, the harder she comes \U0001F525"),

            _("She left the curtains open on purpose {loc} \U0001F440"),

            _("Almost caught. She loved every second of it \U0001F525\U0001F608"),

        ],
        # --- Public shy ---
        "public_shy": [
            _("She was SO nervous someone would see \U0001F633\U0001F440"),

            _("Shaking with fear AND excitement {loc} \U0001F631\U0001F525"),

            _("She kept looking around scared {loc} \U0001F440\U0001F630"),

            _("Too shy for this but she did it anyway \U0001F633"),

            _("She whispered 'someone's going to see us' \U0001F92B\U0001F631"),

            _("Blushing the entire time {loc} \U0001F633\U0001F495"),

            _("She almost stopped when she heard footsteps \U0001F463\U0001F631"),

            _("Shy girl takes a risk {loc} \U0001F633\U0001F525"),

            _("Her hands were shaking the whole time {loc} \U0001F630"),

            _("She kept saying 'hurry up before someone sees' \U0001F633\U0001F631"),

            _("She covered her mouth to stay quiet {loc} \U0001F92B"),

            _("Terrified of getting caught but too turned on to stop \U0001F633\U0001F525"),

            _("She hid behind me when someone walked past \U0001F631\U0001F648"),

            _("Nervous wreck {loc} but she still finished \U0001F633\U0001F525"),

        ],
        # --- Virgin (from snapshot) ---
        "virgin": [
            _("Her very first time... and I recorded it \U0001F608\U0001F3AC"),

            _("Virgin no more \U0001F525\U0001F51E"),

            _("First time EVER {loc} \U0001F633\U0001F525"),

            _("She was saving herself... not anymore \U0001F608"),

            _("I took it. She let me. \U0001F525"),

            _("Deflowered {loc} \U0001F339\U0001F525"),

            _("She didn't know what to expect. Now she does \U0001F633\U0001F4A5"),

            _("Innocence lost {loc} \U0001F607\U0001F525"),

            _("She was nervous before. Not anymore \U0001F633\U0001F525"),

            _("First timer and she's already hooked \U0001F608"),

            _("She saved herself for someone special. That's me apparently \U0001F60F"),

            _("From virgin to addicted in one night \U0001F525"),

            _("Watch the exact moment she goes from innocent to naughty \U0001F607\U0001F608"),

            _("Her first time ever and she wants to go again already \U0001F633\U0001F525"),

        ],
        # --- Exhibitionist ---
        "exhibitionist": [
            _("She stripped without me even asking \U0001F525"),

            _("She wants the whole world to see \U0001F30D\U0001F440"),

            _("Zero shame. 100% confidence. \U0001F4AA\U0001F525"),

            _("She'd do this on a stage if I let her \U0001F3AD\U0001F525"),

            _("Born exhibitionist {loc} \U0001F440\U0001F60F"),

            _("She doesn't care who's watching \U0001F440\U0001F525"),

            _("The less clothes, the happier she is \U0001F460\U0001F525"),

            _("She told me to leave the door open \U0001F6AA\U0001F608"),

            _("She asked if the camera was on. Then took everything off \U0001F4F7\U0001F525"),

            _("She flashes strangers for fun \U0001F440\U0001F608"),

            _("Clothes are her enemy \U0001F460\U0001F525"),

            _("She walks around naked and dares anyone to stare \U0001F440\U0001F4AA"),

            _("She wanted the window open while we did it \U0001F6AA\U0001F525"),

            _("No shame, no filter, no clothes \U0001F525\U0001F608"),

        ],
        # --- Submissive ---
        "submissive": [
            _("She does whatever I tell her \U0001F608"),

            _("Good girl {loc} \U0001F90D"),

            _("Obedient and eager to please \U0001F90D\U0001F525"),

            _("She asked permission before moaning \U0001F92B\U0001F90D"),

            _("Completely under my control {loc} \U0001F608"),

            _("She lives to serve \U0001F90D\U0001F525"),

            _("I didn't even have to ask twice \U0001F608"),

            _("'Yes sir' is her favorite phrase \U0001F90D"),

            _("She waits on her knees until I tell her what to do \U0001F90D\U0001F608"),

            _("I snapped my fingers and she came running \U0001F90D"),

            _("She thanked me after. Twice. \U0001F90D\U0001F525"),

            _("Trained to perfection {loc} \U0001F90D\U0001F608"),

            _("She doesn't move until I give the command \U0001F90D"),

            _("The most obedient girl you'll ever see \U0001F90D\U0001F525"),

        ],
        # --- Dominant ---
        "dominant": [
            _("She took charge and I let her \U0001F451\U0001F525"),

            _("She told ME what to do \U0001F451"),

            _("I'm just along for the ride \U0001F3A2\U0001F525"),

            _("Alpha female energy {loc} \U0001F451\U0001F525"),

            _("She pinned me down and didn't ask \U0001F608\U0001F451"),

            _("Bossy and I love it \U0001F451\U0001F525"),

            _("She runs the show {loc} \U0001F3AC\U0001F451"),

            _("When SHE decides it's time \U0001F451"),

            _("She pushed my head down and said 'your turn' \U0001F451\U0001F608"),

            _("I tried to switch positions. She said no \U0001F451"),

            _("She grabs what she wants when she wants it \U0001F451\U0001F525"),

            _("I'm her toy and she makes sure I know it \U0001F451\U0001F608"),

            _("She set the rules before we even started \U0001F451"),

            _("She decides when I finish. Not me. \U0001F451\U0001F525"),

        ],

        # ==========================================================
        # TYPE-SPECIFIC trait titles  (key = "trait:vtype")
        # Checked BEFORE the generic trait pool for more variety.
        # ==========================================================

        # ── Cheating × type ──
        "cheating:creampie": [
            _("Creampied someone else's girl \U0001F608\U0001F4A6"),

            _("Her boyfriend uses condoms. I don't. \U0001F92B\U0001F4A6"),

            _("Filled his girlfriend up and sent her home \U0001F608"),

            _("She let me finish inside. He has no clue \U0001F64A\U0001F4A6"),

            _("Breeding another man's girlfriend \U0001F525\U0001F4A6"),

            _("She's going back to him with my cum inside \U0001F92B"),

            _("He kisses her goodnight. If only he knew \U0001F608"),

            _("Raw creampie in someone else's girl {loc} \U0001F525"),

            _("His girlfriend dripping with my cum on the way home \U0001F695\U0001F4A6"),

            _("She texts him 'on my way' while my cum is still inside her \U0001F4F1\U0001F4A6"),

            _("He asked if she had a good day. She had the best day \U0001F92B\U0001F4A6"),

            _("She says 'I love you' to him 10 minutes after I cum inside her \U0001F4F1\U0001F608"),

            _("He thinks the wet spot is from the shower \U0001F6BF\U0001F4A6"),

            _("I fill her up. He cleans up after. Life is good \U0001F608\U0001F4A6"),

            _("She sits on his couch still leaking from me \U0001F6CB\U0001F92B"),

            _("His girlfriend begged me to cum inside. Twice. \U0001F64F\U0001F4A6"),

            _("She wears a sundress to hide the mess I left inside \U0001F457\U0001F4A6"),

            _("Creampie so deep she felt it all the way home \U0001F697\U0001F4A6"),

            _("He buys her flowers. I give her loads \U0001F490\U0001F608"),

            _("She put on fresh panties but they're already ruined \U0001F608\U0001F4A6"),

            _("He holds her hand. I hold her hips while I cum inside \U0001F4A6\U0001F525"),

            _("Another man's girl, another raw creampie \U0001F501\U0001F4A6"),

            _("She swore she'd use protection with me. She lied to herself \U0001F92D\U0001F4A6"),

            _("His girlfriend's favorite position? Whatever makes me cum inside faster \U0001F608"),

        ],
        "cheating:cowgirl": [
            _("His girlfriend riding me like she never rides him \U0001F608"),

            _("She's on top like she owns me. She still has a bf \U0001F92B"),

            _("Taken girl bouncing {loc}. Boyfriend has no idea \U0001F440"),

            _("She rode me until she forgot his name \U0001F525"),

            _("His girl on top of me. Sorry not sorry \U0001F60F"),

            _("She said she never rides him like this \U0001F92D"),

            _("Girlfriend material... just not his anymore \U0001F608"),

            _("She chose to be on top. He doesn't get this treatment \U0001F451"),

            _("She rides me way better than she rides him. Her words \U0001F92D"),

            _("His girlfriend on top grinding like she's single \U0001F525"),

            _("She called me his name once. Then corrected herself and kept riding \U0001F608"),

            _("Her thighs shake for me. He gets the leftovers \U0001F60F"),

            _("Taken girl riding {loc} while his calls go to voicemail \U0001F4F1\U0001F525"),

            _("She put his hoodie on the chair and rode me on his birthday \U0001F382\U0001F608"),

        ],
        "cheating:bj": [
            _("His girlfriend on her knees for someone else \U0001F608"),

            _("She sucks me off then kisses her boyfriend goodbye \U0001F48B\U0001F608"),

            _("His girl gives me head while he's at work \U0001F92B"),

            _("She swallows mine but won't even do it for him \U0001F60F"),

            _("Taken girl on her knees {loc}. He'd lose his mind \U0001F608"),

            _("She deepthroats me then tells him she had a sore throat \U0001F912\U0001F608"),

            _("His girlfriend's mouth is busy with someone else \U0001F525"),

            _("She gives me the blowjob she refuses to give him \U0001F92B\U0001F60F"),

            _("He gets a peck on the cheek. I get this \U0001F48B\U0001F608"),

            _("Boyfriend calls. She answers with her mouth full \U0001F4F1\U0001F608"),

        ],
        "cheating:hj": [
            _("His girlfriend's hands all over me \U0001F608"),

            _("She jerks me off while texting him back \U0001F4F1\U0001F92B"),

            _("Taken girl, magic hands {loc} \U0001F525"),

            _("Her boyfriend's ring on her finger while she strokes me \U0001F48D\U0001F608"),

            _("She uses both hands on me. He gets none \U0001F60F"),

            _("His girl grabbed it like she's been thinking about it all day \U0001F608"),

            _("She has his name tattooed on her wrist. That same hand is on me \U0001F608"),

            _("Her grip gets tighter every time her phone buzzes from him \U0001F4F1\U0001F525"),

            _("She learned this trick on him. Perfected it on me \U0001F60F"),

            _("His girlfriend's hands were made for someone else \U0001F92B\U0001F608"),

        ],
        "cheating:tj": [
            _("His girlfriend's tits wrapped around me \U0001F608"),

            _("She uses her best assets on someone who isn't him \U0001F92B"),

            _("Titjob from a taken girl. He doesn't get this either \U0001F60F"),

            _("His girlfriend's perfect tits {loc}. Sorry bro \U0001F608"),

            _("She squeezed them around me while wearing his necklace \U0001F4CE\U0001F608"),

            _("Between his girlfriend's tits and she's enjoying every second \U0001F525"),

            _("He bought her that push-up bra. I'm the one who benefits \U0001F60F\U0001F608"),

            _("She never does this for him. His loss, my gain \U0001F92B\U0001F525"),

            _("Taken girl's tits around me while he thinks she's at yoga \U0001F9D8\U0001F608"),

            _("Her boyfriend paid for those. I get to enjoy them \U0001F60F\U0001F525"),

        ],
        "cheating:masturbate": [
            _("Caught his girlfriend touching herself thinking about me \U0001F608"),

            _("She was moaning MY name, not his \U0001F92B"),

            _("His girlfriend's solo session... inspired by me \U0001F4F1\U0001F608"),

            _("She sent me this while he was in the next room \U0001F92B\U0001F525"),

            _("Taken girl's private time. He has no idea \U0001F440\U0001F608"),

            _("She records herself for me. He'd never believe it \U0001F4F7\U0001F608"),

            _("She touches herself to our texts. He sleeps next to her \U0001F4F1\U0001F92B"),

            _("His girlfriend gets off thinking about me, not him \U0001F608\U0001F525"),

            _("She finishes to my voice notes while he's at work \U0001F3A7\U0001F92B"),

            _("Taken girl's solo time and it's all about me \U0001F440\U0001F608"),

        ],

        # ── Hate cum × type ──
        "hate_cum:creampie": [
            _("She HATES cum and I came inside anyway \U0001F608\U0001F4A6"),

            _("She begged me to pull out. I didn't. \U0001F92D\U0001F4A6"),

            _("Anti-cum girl gets the full load inside \U0001F631\U0001F4A6"),

            _("She screamed when she felt it inside her \U0001F631"),

            _("She literally cried. I literally don't care \U0001F608\U0001F4A6"),

            _("Worst nightmare for a cum hater \U0001F4A6\U0001F645"),

            _("She said 'anywhere but inside'. Guess where I finished \U0001F608\U0001F4A6"),

            _("She pushed me but I was already done inside \U0001F631\U0001F4A6"),

            _("Her face went from pleasure to horror in 2 seconds \U0001F633\U0001F631"),

            _("She hates cum AND I came inside. Double nightmare \U0001F4A6\U0001F645"),

            _("She felt it and froze. Best reaction video ever \U0001F631\U0001F4F7"),

            _("Cum hater creampied against her will {loc} \U0001F608\U0001F4A6"),

        ],
        "hate_cum:cowgirl": [
            _("She hates cum but she's riding anyway \U0001F633\U0001F525"),

            _("Cum hater on top. Praying I don't finish inside \U0001F64F\U0001F608"),

            _("She rode me and panicked when I got close \U0001F631"),

            _("She tried to jump off before I came. Too late \U0001F92D"),

            _("Riding with fear in her eyes. She knows what's coming \U0001F440\U0001F631"),

            _("She hates it but she still bounces \U0001F633\U0001F525"),

            _("She speeds up then panics when she realizes what that means \U0001F631\U0001F608"),

            _("Cum-hating cowgirl trying to time her escape \U0001F3C3\U0001F4A6"),

            _("On top with one eye on me and one on the exit \U0001F440\U0001F631"),

            _("She rides like she loves it but dreads the ending \U0001F633\U0001F4A6"),

        ],

        # ── Cum slut × type ──
        "cum_slut:creampie": [
            _("She wrapped her legs and wouldn't let me pull out \U0001F4A6\U0001F60D"),

            _("Cum addict demands the creampie \U0001F4A6\U0001F525"),

            _("She said 'inside me, all of it' \U0001F929\U0001F4A6"),

            _("Cum slut gets her favorite filling \U0001F4A6\U0001F60B"),

            _("She moaned 'deeper' right before I came \U0001F4A6\U0001F525"),

            _("She counts the seconds until I fill her up \U0001F4A6\U0001F60D"),

            _("She locked her ankles behind me and said 'don't you dare pull out' \U0001F4A6\U0001F608"),

            _("Three creampies and she's asking for a fourth \U0001F4A6\U0001F929"),

            _("She scoops it back inside when it drips out \U0001F4A6\U0001F60B"),

            _("She checks to make sure nothing leaked out \U0001F4A6\U0001F92B"),

            _("She holds still after so she doesn't waste any \U0001F4A6\U0001F60D"),

            _("Addicted to the feeling of being filled up \U0001F4A6\U0001F525"),

        ],
        "cum_slut:cowgirl": [
            _("She rode me just to milk every drop \U0001F4A6\U0001F60D"),

            _("Cum addict on top. She's not stopping until she gets it \U0001F525"),

            _("She bounces faster when she knows I'm close \U0001F929\U0001F4A6"),

            _("Riding me like she's trying to drain me dry \U0001F4A6\U0001F525"),

            _("She slammed down when I came. On purpose \U0001F608\U0001F4A6"),

            _("On top and in control of every last drop \U0001F4A6\U0001F451"),

            _("She grinds slower to feel every drop fill her up \U0001F929\U0001F4A6"),

            _("Cum addict refuses to get off until she's milked me twice \U0001F4A6\U0001F60D"),

            _("She keeps riding after I finish just to squeeze out more \U0001F4A6\U0001F525"),

            _("On top with one mission: drain every last drop \U0001F4A6\U0001F608"),

        ],

        # ── No condom × type ──
        "no_condom:creampie": [
            _("She said use protection. I came inside raw \U0001F608\U0001F4A6"),

            _("No condom, no pulling out. Full commitment \U0001F525\U0001F4A6"),

            _("She begged for a condom. Got a creampie instead \U0001F92D"),

            _("Raw creampie. She's still processing what happened \U0001F633\U0001F4A6"),

            _("Unprotected and overflowing {loc} \U0001F4A6\U0001F525"),

            _("She asked for a condom three times. I came inside three times \U0001F608"),

            _("She handed me a condom. I handed it back and came inside \U0001F608\U0001F4A6"),

            _("No wrapper, no warning, no pulling out \U0001F525\U0001F4A6"),

            _("She whispered 'at least use a condom'. I whispered 'no' \U0001F92B\U0001F4A6"),

            _("Raw creampie so deep she couldn't stand up after \U0001F633\U0001F4A6"),

            _("She saw me reach for the condom. I reached past it \U0001F608"),

            _("Unprotected creampie and she pretends to be surprised \U0001F92D\U0001F4A6"),

        ],
        "no_condom:cowgirl": [
            _("She's riding raw. No condom. Her choice? Maybe. \U0001F608"),

            _("On top with nothing between us \U0001F525"),

            _("She forgot about the condom when she got on top \U0001F92D"),

            _("Raw riding {loc}. She feels everything \U0001F525"),

            _("No barrier. She bounces and bites her lip \U0001F525"),

            _("She was supposed to grab a condom. She grabbed me instead \U0001F608"),

            _("Unprotected cowgirl. She stopped asking after the first bounce \U0001F92D"),

            _("She rides different when there's nothing between us \U0001F525\U0001F608"),

            _("Raw on top and she's biting her lip harder than usual \U0001F525"),

            _("No condom cowgirl {loc}. She pretends she didn't notice \U0001F92D\U0001F608"),

        ],

        # ── Hardcore × type ──
        "hardcore_sex:creampie": [
            _("Pounded her into the mattress and came inside \U0001F4A5\U0001F4A6"),

            _("Rough creampie. She screamed when I finished \U0001F525\U0001F4A6"),

            _("Hard and raw. Filled her up with no mercy \U0001F608\U0001F4A6"),

            _("She likes it rough AND deep. Full load inside \U0001F4A5\U0001F4A6"),

            _("Destroyed her and then left a gift inside \U0001F608\U0001F4A6"),

            _("She wanted it hard. She got it hard AND full \U0001F525"),

            _("Slapped her while I came inside. She moaned louder \U0001F44B\U0001F4A6"),

            _("Rough pounding ended with the deepest creampie \U0001F4A5\U0001F4A6"),

            _("She screamed the whole time and I filled her up at the end \U0001F525\U0001F4A6"),

            _("Hard enough to leave bruises. Deep enough to overflow \U0001F4A5\U0001F4A6"),

        ],
        "hardcore_sex:cowgirl": [
            _("She slams down so hard the bed might break \U0001F4A5\U0001F525"),

            _("Aggressive rider. She doesn't do gentle \U0001F525\U0001F62C"),

            _("She rides like she's trying to break me \U0001F4A5"),

            _("Rough cowgirl. She bounces hard enough to hurt \U0001F62C\U0001F525"),

            _("Wild ride {loc}. Nothing soft about this \U0001F525"),

            _("She slapped me while bouncing. I didn't complain \U0001F44B\U0001F4A5"),

            _("Rough rider leaves bruises on my chest \U0001F525\U0001F62C"),

            _("The headboard cracked. She kept going \U0001F4A5\U0001F525"),

            _("She rides so hard the whole building can hear it \U0001F50A\U0001F4A5"),

        ],
        "hardcore_sex:bj": [
            _("She likes to choke on the big dick \U0001F346\U0001F525"),

            _("Deep throat until she can't breathe. She loves it \U0001F525\U0001F4A5"),

            _("She gags and keeps going. No quit in this girl \U0001F62C\U0001F525"),

            _("Sloppy, rough, and she's begging for more \U0001F525"),

            _("She grabbed my hips and pulled me deeper into her throat \U0001F4A5"),

            _("She doesn't stop until her eyes are watering \U0001F525\U0001F62C"),

            _("Mascara running, spit everywhere. She's smiling \U0001F62C\U0001F525"),

            _("She chokes herself on it and asks for more \U0001F4A5\U0001F525"),

            _("Rough blowjob. She gagged three times and never stopped \U0001F525\U0001F62C"),

            _("Her throat is sore and she's asking for round two \U0001F4A5\U0001F525"),

        ],

        # ── Cute sex × type ──
        "cute_sex:creampie": [
            _("She blushes even harder when I finish inside \U0001F633\U0001F4A6"),

            _("The cutest gasp when she felt it \U0001F970\U0001F4A6"),

            _("Gentle creampie. She held my hand the whole time \U0001F495\U0001F4A6"),

            _("She hid her face and whispered 'it's warm' \U0001F633\U0001F4A6"),

            _("Soft moan when I came inside. So precious \U0001F970"),

            _("She squeezed my hand when she felt me finish \U0001F495"),

            _("She giggled softly when she felt it fill her up \U0001F970\U0001F4A6"),

            _("The way she looks at me when I finish inside \U0001F633\U0001F495"),

            _("She whispered 'it feels nice' after I came inside \U0001F970"),

            _("She wrapped her arms around me and said 'stay inside' \U0001F495\U0001F4A6"),

        ],
        "cute_sex:cowgirl": [
            _("Shy girl tries riding for the first time \U0001F633\U0001F495"),

            _("She's on top blushing the entire time \U0001F970"),

            _("The cutest cowgirl you'll ever see \U0001F633\U0001F525"),

            _("She hides her face while she bounces \U0001F648\U0001F495"),

            _("Slow and sweet on top {loc} \U0001F970"),

            _("She kept apologizing while riding. Adorable \U0001F633\U0001F970"),

            _("She giggles every time she bounces. So cute \U0001F633\U0001F3B5"),

            _("Gentle cowgirl with the shyest smile on her face \U0001F970\U0001F495"),

            _("She rocks her hips slowly and whispers 'is this good?' \U0001F633\U0001F970"),

            _("The way she looks down at me while riding... precious \U0001F495\U0001F633"),

        ],

        # ── Virgin × type ──
        "virgin:creampie": [
            _("First time ever AND I came inside \U0001F608\U0001F4A6"),

            _("Virgin creampie. She didn't even know what hit her \U0001F633\U0001F4A6"),

            _("Took her virginity and left a gift inside \U0001F608\U0001F4A6"),

            _("Her first time. My cum. Inside. \U0001F525\U0001F4A6"),

            _("She lost her virginity to a raw creampie {loc} \U0001F633"),

            _("First time and no condom. She'll remember this forever \U0001F608"),

            _("She lost her virginity and her first creampie in the same night \U0001F633\U0001F4A6"),

            _("First time sex, first time creampie. Double debut \U0001F525\U0001F4A6"),

            _("She didn't even know what a creampie was until now \U0001F633"),

            _("Virgin to bred in one session {loc} \U0001F608\U0001F4A6"),

        ],
        "virgin:cowgirl": [
            _("Virgin rides for the first time. She's shaking \U0001F633\U0001F525"),

            _("She wanted to be on top for her first time \U0001F633"),

            _("First time cowgirl. She barely knew what to do \U0001F633\U0001F495"),

            _("Virgin on top. You can see the exact moment she loses it \U0001F440\U0001F525"),

            _("She chose to ride for her first time. Bold \U0001F633\U0001F525"),

            _("Awkward first ride. She got better fast \U0001F633\U0001F525"),

            _("She lowered herself slowly. Then couldn't stop \U0001F633\U0001F525"),

            _("First time riding and her legs are already shaking \U0001F633\U0001F4A5"),

            _("Virgin tried cowgirl and now she's obsessed \U0001F633\U0001F525"),

            _("She went from scared to bouncing in 60 seconds \U0001F633\U0001F525"),

        ],

        # ── Camera hater × type ──
        "camera_hater:creampie": [
            _("Secret creampie footage. She has no idea \U0001F4F7\U0001F92B\U0001F4A6"),

            _("Hidden cam caught the whole creampie \U0001F4F1\U0001F4A6"),

            _("She'd kill me if she knew I filmed this part \U0001F480\U0001F4A6"),

            _("Recorded the creampie without her knowing \U0001F92B\U0001F4A6"),

            _("She hates being filmed AND I came inside on camera \U0001F4F5\U0001F4A6"),

            _("Anti-camera girl's creampie going viral \U0001F4F7\U0001F92B\U0001F4A6"),

            _("She banned my camera. I filmed the creampie anyway \U0001F480\U0001F608"),

            _("Hidden angle of her worst nightmare on tape \U0001F575\U0001F4A6"),

            _("She'd burn my phone if she saw this dripping out \U0001F4F1\U0001F92B"),

            _("Camera-shy girl creampied on hidden film {loc} \U0001F4F7\U0001F4A6"),

        ],
        "camera_hater:cowgirl": [
            _("Secret footage of her riding me. She has no idea \U0001F4F7\U0001F92B"),

            _("Hidden cam angle from below while she rides \U0001F4F1\U0001F440"),

            _("She thinks no one will ever see this \U0001F92B\U0001F525"),

            _("Phone under the pillow caught everything \U0001F4F1\U0001F608"),

            _("She scans for cameras before getting on top. She missed mine \U0001F575\U0001F92B"),

            _("Anti-camera girl bouncing on hidden film {loc} \U0001F4F7\U0001F525"),

            _("She'd never ride again if she knew this was online \U0001F480\U0001F4F1"),

            _("Camera-shy cowgirl caught from the angle she didn't check \U0001F92B\U0001F608"),

            _("Her rule: no cameras. My rule: she doesn't get to know \U0001F4F5\U0001F4F7"),

            _("She closed her eyes while riding. Phone recorded everything \U0001F92B\U0001F525"),

        ],
        "camera_hater:masturbate": [
            _("Caught her touching herself. She has NO idea I filmed it \U0001F4F7\U0001F92B"),

            _("Secret footage of her solo session. She'd kill me \U0001F480\U0001F92B"),

            _("She was moaning with her eyes closed. Perfect time to record \U0001F4F1\U0001F608"),

            _("Hidden cam caught her fingers deep inside herself \U0001F92B\U0001F525"),

            _("She locked the door but forgot I had the angle \U0001F4F7\U0001F608"),

            _("Secretly recorded her getting herself off {loc} \U0001F4F1\U0001F92B"),

            _("She thought she was alone. My phone was already recording \U0001F92B\U0001F4F7"),

            _("Spy cam caught every moan of her solo time \U0001F575\U0001F525"),

            _("She finished without ever knowing I was watching and filming \U0001F4F1\U0001F608"),

            _("Her private moment. Now it's everyone's moment \U0001F92B\U0001F525"),

        ],
        "camera_hater:bj": [
            _("Secret blowjob footage. She has no clue \U0001F4F7\U0001F92B"),

            _("She told me no cameras. My phone was already recording her mouth \U0001F4F1\U0001F608"),

            _("Hidden angle caught every inch going in her mouth \U0001F92B\U0001F525"),

            _("She'd end me if she knew this blowjob is on film \U0001F480\U0001F92B"),

            _("Anti-camera girl on her knees on hidden film \U0001F4F5\U0001F4F7"),

            _("She always checks for cameras. She forgot to look up \U0001F575\U0001F92B"),

            _("Camera-shy lips doing camera-worthy things {loc} \U0001F4F1\U0001F608"),

            _("She hates being filmed but her mouth is a star \U0001F480\U0001F525"),

            _("Her biggest rule broken while she was on her knees \U0001F4F7\U0001F92B"),

            _("She made me promise no recording. I had my fingers crossed \U0001F92B\U0001F608"),

        ],
        "camera_hater:hj": [
            _("She didn't know the camera was on while stroking me \U0001F4F7\U0001F92B"),

            _("Secret handjob footage. Her grip on hidden cam \U0001F4F1\U0001F608"),

            _("Filmed her hand on me without her knowing \U0001F92B\U0001F525"),

            _("She bans cameras but her hands are on film anyway \U0001F4F5\U0001F4F7"),

            _("She'd smash my phone if she saw this handjob clip \U0001F480\U0001F92B"),

            _("Anti-camera girl giving the best handjob on hidden film \U0001F4F1\U0001F608"),

            _("She said no photos ever. I got a whole video of her hand \U0001F92B\U0001F525"),

            _("Camera-shy girl, camera-worthy grip {loc} \U0001F4F7\U0001F608"),

            _("She checks for cameras every time. She missed this one \U0001F575\U0001F92B"),

            _("Her one rule is no filming. Oops \U0001F4F5\U0001F608"),

        ],
        "camera_hater:tj": [
            _("She has no idea her tits around my cock are on film \U0001F4F7\U0001F92B"),

            _("Secret titjob footage. She would destroy my phone \U0001F480\U0001F608"),

            _("Hidden cam caught her breasts squeezing every inch \U0001F92B\U0001F525"),

            _("She hates cameras more than anything. Her tits are on film \U0001F4F5\U0001F4F7"),

            _("Anti-camera girl's titjob caught from the perfect angle \U0001F575\U0001F92B"),

            _("She made me swear no filming. I lied. Her tits looked too good \U0001F92B\U0001F608"),

            _("Camera-hating girl with camera-worthy tits {loc} \U0001F4F7\U0001F525"),

            _("She looked down the whole time. Phone was above filming \U0001F480\U0001F4F1"),

            _("She'd throw my phone out the window if she saw this \U0001F4F5\U0001F92B"),

            _("Her biggest fear is being filmed. Her best titjob is now on tape \U0001F4F7\U0001F608"),

        ],

        # ── Secret recording (any girl, non-consensual) ──
        "secret": [
            _("She has NO idea this video exists \U0001F92B\U0001F4F7"),

            _("Secretly recorded {loc}. She never noticed \U0001F4F1\U0001F608"),

            _("Hidden camera footage she'll never find out about \U0001F575\U0001F92B"),

            _("Filmed without her knowing. Pure gold \U0001F4F7\U0001F525"),

            _("She thought it was just us. The camera was rolling \U0001F92B"),

            _("What she doesn't know makes great content \U0001F608\U0001F4F1"),

            _("Secret angle {loc}. She was completely unaware \U0001F4F7\U0001F92B"),

            _("Recorded everything while she had no clue \U0001F575\U0001F525"),

        ],
        "secret:masturbate": [
            _("Caught her playing with herself. She had no idea I was there \U0001F92B\U0001F525"),

            _("I found her touching herself and hit record \U0001F4F1\U0001F608"),

            _("Secret footage of her solo time. Eyes closed, moaning loud \U0001F92B\U0001F525"),

            _("She was fingering herself {loc}. My phone caught everything \U0001F4F7\U0001F608"),

            _("Spy cam caught her mid-orgasm. She never knew \U0001F575\U0001F525"),

            _("She locked the door but I got the angle through the crack \U0001F92B\U0001F4F1"),

            _("Her private moment recorded without her knowing {loc} \U0001F4F7\U0001F92B"),

            _("She was so lost in pleasure she didn't hear me recording \U0001F608\U0001F525"),

            _("Caught her wet and moaning. Phone was already rolling \U0001F4F1\U0001F92B"),

            _("She thought nobody would ever see this. Wrong \U0001F92B\U0001F525"),

            _("Secretly filmed her orgasm face {loc} \U0001F575\U0001F608"),

            _("Hidden footage of her getting herself off alone \U0001F4F7\U0001F92B"),

        ],
        "secret:creampie": [
            _("She didn't know I filmed the creampie leaking out \U0001F92B\U0001F4A6"),

            _("Hidden camera caught every drop going inside her \U0001F4F1\U0001F4A6"),

            _("Secret footage of the moment I filled her up \U0001F92B\U0001F525"),

            _("She has no idea this creampie is on video \U0001F4F7\U0001F4A6"),

            _("Spy cam caught the exact moment I came inside \U0001F575\U0001F4A6"),

            _("She felt it leak out. She didn't feel the camera recording it \U0001F92B\U0001F4F7"),

            _("Hidden angle of the cream dripping out {loc} \U0001F4F1\U0001F4A6"),

            _("Secret creampie footage. She'd lose her mind \U0001F92B\U0001F525"),

            _("Phone caught every drop going in. She caught nothing \U0001F4F7\U0001F4A6"),

            _("She was still shaking when I stopped recording \U0001F92B\U0001F608"),

        ],
        "secret:bj": [
            _("She didn't know I was recording her mouth on me \U0001F92B\U0001F4F7"),

            _("Hidden angle caught her going down on me {loc} \U0001F4F1\U0001F608"),

            _("Secret blowjob footage. She was too focused to notice \U0001F92B\U0001F525"),

            _("Phone was propped up and she never saw it while sucking \U0001F4F7\U0001F608"),

            _("Her lips on camera. She was too busy to look up \U0001F92B\U0001F4F7"),

            _("Secret angle of her head going up and down {loc} \U0001F575\U0001F525"),

            _("She closed her eyes while sucking. Phone recorded it all \U0001F4F1\U0001F92B"),

            _("Hidden cam caught the deepthroat. She never noticed \U0001F4F7\U0001F608"),

            _("Spy footage of her on her knees. She'd freak out \U0001F575\U0001F4F7"),

            _("She was looking up at me, not at the phone behind me \U0001F92B\U0001F525"),

        ],
        "secret:cowgirl": [
            _("She was riding me. Phone was recording under the pillow \U0001F92B\U0001F4F1"),

            _("Secret footage of her bouncing on top. She never noticed \U0001F4F7\U0001F608"),

            _("Hidden cam caught her riding from the perfect angle \U0001F575\U0001F525"),

            _("She closed her eyes while riding. Phone got every bounce \U0001F92B\U0001F525"),

            _("Pillow cam POV of her on top. She was too lost to notice \U0001F4F1\U0001F608"),

            _("She has no idea her cowgirl is going viral \U0001F4F7\U0001F92B"),

            _("Secret ride footage from below. Best angle she'll never see \U0001F575\U0001F525"),

            _("Recorded her on top from a mirror she didn't know about \U0001F92B\U0001F4F7"),

            _("She bounced with her eyes shut. I filmed with mine open \U0001F4F1\U0001F608"),

            _("She was too focused on riding to check for cameras \U0001F92B\U0001F525"),

        ],
        "secret:hj": [
            _("She didn't notice the phone while stroking me \U0001F92B\U0001F4F1"),

            _("Hidden cam caught her hand in action \U0001F4F7\U0001F608"),

            _("Secret handjob footage. She was focused on something else \U0001F92B\U0001F525"),

            _("Phone angled just right to catch every stroke \U0001F4F1\U0001F92B"),

            _("She was looking away. I was recording her grip \U0001F4F7\U0001F608"),

            _("Her hand on me, hidden cam on her. She never saw it \U0001F92B\U0001F525"),

            _("Secret footage of the softest hands doing the dirtiest thing \U0001F575\U0001F4F7"),

            _("She stroked me while I filmed from the side. Not a clue \U0001F4F1\U0001F608"),

            _("Her fingers wrapped around me on hidden camera {loc} \U0001F92B\U0001F525"),

            _("She was watching TV while jerking me off. Phone got it all \U0001F4F7\U0001F92B"),

        ],
        "secret:tj": [
            _("She didn't know I was filming her tits around me \U0001F92B\U0001F4F7"),

            _("Hidden angle of the titjob. She never looked up \U0001F4F1\U0001F608"),

            _("Secret titjob footage {loc} \U0001F575\U0001F525"),

            _("Her tits squeezed around me on hidden camera \U0001F92B\U0001F4F7"),

            _("She was focused on my chest, not the phone filming hers \U0001F4F1\U0001F608"),

            _("Secret angle of her breasts doing all the work \U0001F575\U0001F525"),

            _("She looked down the whole time. Camera caught everything \U0001F92B\U0001F4F7"),

            _("Titjob from above on spy cam. She had no idea \U0001F4F1\U0001F92B"),

            _("Phone balanced on the headboard caught every squeeze \U0001F4F7\U0001F608"),

            _("Her best assets on hidden film {loc} \U0001F575\U0001F525"),

        ],

        # ── Submissive × type ──
        "submissive:cowgirl": [
            _("I told her to ride. She obeyed immediately \U0001F90D\U0001F608"),

            _("She asked permission before getting on top \U0001F90D"),

            _("Good girl riding like she was told \U0001F90D\U0001F525"),

            _("'Can I go faster, sir?' \U0001F90D\U0001F633"),

            _("She checks my face for approval with every bounce \U0001F90D\U0001F633"),

            _("Obedient cowgirl. She matches exactly the pace I set \U0001F90D\U0001F525"),

            _("She stops when I say stop. Rides when I say ride \U0001F90D\U0001F608"),

            _("She whispered 'am I doing good?' while on top \U0001F90D\U0001F633"),

            _("'Tell me how you want me to move, sir' \U0001F90D\U0001F525"),

            _("Good girl on top following every instruction perfectly \U0001F90D\U0001F608"),

        ],
        "submissive:creampie": [
            _("She let me finish inside because I told her to \U0001F90D\U0001F4A6"),

            _("'You can cum wherever you want, sir' \U0001F90D\U0001F4A6"),

            _("Obedient girl takes the creampie without question \U0001F90D\U0001F525"),

            _("She thanked me after I came inside \U0001F90D\U0001F4A6"),

            _("She held still while I filled her up. Good girl \U0001F90D\U0001F4A6"),

            _("'Inside me? Yes sir, whatever you want' \U0001F90D\U0001F525"),

            _("She didn't flinch when I came inside. Just whispered 'thank you' \U0001F90D\U0001F4A6"),

            _("Obedient creampie. She takes what she's given \U0001F90D\U0001F608"),

            _("She spread her legs wider when I said I was close \U0001F90D\U0001F4A6"),

            _("Good girl lets me decide where I finish. Always inside \U0001F90D\U0001F525"),

        ],

        # ── Dominant × type ──
        "dominant:cowgirl": [
            _("She pinned me down and rode until SHE was done \U0001F451\U0001F525"),

            _("She decides the speed, the angle, everything \U0001F451"),

            _("I'm not allowed to move. She handles it \U0001F451\U0001F608"),

            _("She grabbed my wrists and rode harder \U0001F451\U0001F525"),

            _("She grabs my throat while she rides \U0001F525\U0001F4A5"),

            _("She held me down and took what she wanted on top \U0001F451\U0001F608"),

            _("I tried to grab her hips. She slapped my hands away \U0001F451\U0001F525"),

            _("'Lie still. I'll tell you when I'm done' \U0001F451\U0001F608"),

            _("She rides at her own pace. I have no say \U0001F451"),

            _("Alpha cowgirl. She controls every single movement \U0001F451\U0001F525"),

            _("She looked down at me and said 'don't even think about moving' \U0001F451\U0001F608"),

        ],
        "dominant:creampie": [
            _("She locked her legs and made ME cum inside \U0001F451\U0001F4A6"),

            _("I didn't choose to cum inside. She did \U0001F451\U0001F608"),

            _("She decided when, where, and how much \U0001F451\U0001F4A6"),

            _("'You're finishing inside. That's not a request' \U0001F451\U0001F525"),

            _("She pulled me in deeper and said 'now' \U0001F451\U0001F4A6"),

            _("I wasn't ready to cum. She didn't care \U0001F451\U0001F608"),

            _("'Every drop inside me. That's an order' \U0001F451\U0001F4A6"),

            _("She wrapped her legs around me and decided for both of us \U0001F451\U0001F525"),

            _("She grabbed my hips and forced the creampie herself \U0001F451\U0001F4A6"),

            _("I tried to pull out. She said 'absolutely not' \U0001F451\U0001F608"),

        ],

        # ── Anal lover (generic: any anal video, anal creampie included; veteran only) ──
        "anal_lover": [
            _("Anal queen takes it and LOVES every second \U0001F451\U0001F525"),

            _("She begged for it in the ass. Who am I to say no \U0001F608\U0001F525"),

            _("She came harder from anal than most girls do from regular \U0001F4A5\U0001F525"),

            _("Her favorite hole. She said it herself \U0001F608"),

            _("She asked me to skip the foreplay and go straight to her ass \U0001F525"),

            _("Anal addict gets her fix {loc} \U0001F60D\U0001F525"),

            _("She pushed back on every stroke like she couldn't get enough \U0001F525\U0001F4A5"),

            _("She moaned louder from anal than anything else we tried \U0001F525"),

            _("Told her we'd do regular. She said 'put it in my ass instead' \U0001F608"),

            _("She finishes from anal alone. No hands needed \U0001F4A5\U0001F525"),

            _("Her eyes roll back every time. Anal queen for real \U0001F451\U0001F525"),

            _("She rates it 10/10 and wants to go again \U0001F60D\U0001F525"),

        ],

        # ── Anal hater (generic — pain/discomfort) ──
        "anal_hater": [
            _("She HATES anal and she took it anyway \U0001F62C\U0001F525"),

            _("Anti-anal girl gets it in the ass {loc} \U0001F631\U0001F525"),

            _("She said never again. We'll see about that \U0001F608"),

            _("She gripped the sheets the whole time. Not from pleasure \U0001F62C"),

            _("She counted every second until it was over \U0001F631\U0001F525"),

            _("Her worst nightmare in her favorite position \U0001F62C\U0001F608"),

            _("She bit the pillow so hard she almost ripped it \U0001F62C\U0001F525"),

            _("Anal hater took every inch. The face she made is priceless \U0001F631"),

            _("She promised herself never. She lied \U0001F62C\U0001F525"),

            _("You can see the exact moment she regrets everything \U0001F631\U0001F608"),

            _("She survived it. Barely \U0001F62C\U0001F525"),

            _("Anti-anal girl learns the hard way {loc} \U0001F631\U0001F525"),

        ],

        # ── Cuckold (NPC partner watching) ──
        "cuckold": [
            _("She sucks me while the cuckold watches \U0001F440\U0001F608"),

            _("I fucked his girl right in front of him \U0001F608\U0001F525"),

            _("'Your cock is bigger' she says while her boyfriend watches \U0001F92F\U0001F525"),

            _("I filled his girl's pussy in front of him \U0001F4A6\U0001F608"),

            _("He watches me stretch his girlfriend {loc} \U0001F440\U0001F525"),

            _("She moaned MY name while looking at HIM \U0001F608\U0001F92B"),

            _("He held the camera while I destroyed his girl \U0001F4F7\U0001F525"),

            _("She forgot he existed the second I went in \U0001F440\U0001F608"),

            _("He had to watch me make her cum harder than he ever could \U0001F629\U0001F525"),

            _("She looked him in the eyes while riding me \U0001F440\U0001F608"),

            _("His girl begged for more while he just stood there \U0001F92B\U0001F525"),

            _("She screamed louder than she ever did for him \U0001F50A\U0001F608"),

        ],
        "cuckold:bj": [
            _("She sucks me while her boyfriend films it \U0001F4F7\U0001F608"),

            _("His girl's mouth on me. He just watches \U0001F440\U0001F525"),

            _("She deep throats me while looking at her cuck boyfriend \U0001F440\U0001F608"),

            _("He watches his girlfriend gag on a bigger cock \U0001F92F\U0001F525"),

            _("Cuckold's girlfriend gives the sloppiest blowjob while he watches \U0001F4A6\U0001F440"),

            _("She never sucked HIM like this. He can see that now \U0001F608\U0001F92B"),

        ],
        "cuckold:creampie": [
            _("Creampied his girlfriend in front of him \U0001F4A6\U0001F608"),

            _("He watched me cum inside his girl. She didn't stop me \U0001F4A6\U0001F440"),

            _("Cuckold watches the creampie drip out of his girlfriend \U0001F4A6\U0001F629"),

            _("She begged me to cum inside while HE watched \U0001F4A6\U0001F608"),

            _("I filled her up. He watched every drop go in \U0001F4A6\U0001F440"),

            _("She made him clean up after I was done inside her \U0001F4A6\U0001F92F"),

        ],

        # ── Full Nelson position ──
        "full_nelson": [
            _("Held her up and destroyed her. She couldn't escape \U0001F4AA\U0001F525"),

            _("Full nelson. Feet off the ground. Nowhere to run \U0001F525\U0001F608"),

            _("Picked her up and gave her no choice \U0001F4AA\U0001F608"),

            _("She can't move, can't run, can't think \U0001F525\U0001F92F"),

            _("Lifted her off the ground and went deep \U0001F4AA\U0001F525"),

            _("Full nelson so hard her legs went numb \U0001F525\U0001F4A5"),

            _("Held up like a ragdoll. She loved every second \U0001F4AA\U0001F608"),

            _("She screamed louder once her feet left the floor \U0001F50A\U0001F525"),

            _("Gravity does half the work in this position \U0001F4AA\U0001F92F"),

            _("Full nelson bounce until she went limp \U0001F525\U0001F4A5"),

            _("No hands free. Completely at my mercy {loc} \U0001F4AA\U0001F608"),

            _("Held her open for the camera to see everything \U0001F4F7\U0001F525"),

        ],

        # ── Threesome (another girl present) ──
        "threesome": [
            _("Two girls take turns on me. Best night ever \U0001F525\U0001F608"),

            _("My girl brought her friend. Things escalated fast \U0001F440\U0001F525"),

            _("One rides, one watches. Then they switch \U0001F501\U0001F525"),

            _("Two mouths are better than one \U0001F444\U0001F525"),

            _("She invited her roommate to join us \U0001F6CF\U0001F525"),

            _("They competed over who could make me finish first \U0001F3C6\U0001F525"),

            _("One on each side. I didn't last long \U0001F525\U0001F608"),

            _("Her friend 'just wanted to watch'. Didn't last 5 minutes \U0001F440\U0001F525"),

            _("They share everything. Including me \U0001F608\U0001F525"),

            _("Threesome {loc}. They planned this behind my back \U0001F92B\U0001F525"),

            _("She held her friend down while I went in \U0001F525\U0001F608"),

            _("Two college girls, one bed, zero regrets \U0001F393\U0001F525"),

        ],

        # ── Girl recorded (another girl held the camera) ──
        "girl_recorded": [
            _("Her friend filmed everything from the best angle \U0001F4F7\U0001F525"),

            _("She held the camera while her friend got destroyed \U0001F4F7\U0001F608"),

            _("POV from her roommate's phone. She caught everything \U0001F4F1\U0001F440"),

            _("Her friend recorded this and sent it to me after \U0001F4F7\U0001F92B"),

            _("The camerawoman couldn't keep the phone steady \U0001F4F1\U0001F923"),

            _("She volunteered to film. Said she wanted the 'experience' \U0001F4F7\U0001F608"),

            _("Her best friend filmed it. You can hear her gasping \U0001F4F7\U0001F440"),

            _("She directed the whole thing. Natural born filmmaker \U0001F3AC\U0001F525"),

            _("The camera girl kept zooming in on the wrong things \U0001F4F7\U0001F923"),

            _("Filmed by her jealous friend. You can hear the envy \U0001F4F7\U0001F60F"),

            _("Her friend's commentary makes this 10x better \U0001F4F7\U0001F923"),

            _("She held the camera and whispered 'deeper' \U0001F4F7\U0001F525"),

        ],

        # ── Anal hater first (first time filmed — high-priority tag) ──
        "anal_hater_first": [
            _("First anal ends in tears \U0001F62D\U0001F525"),

            _("Uptight anal virgin gets wild ride and loves it \U0001F631\U0001F525"),

            _("Her first time in the ass. The SCREAM \U0001F631\U0001F4A5"),

            _("She swore she'd NEVER do anal. Watch what happens \U0001F608\U0001F525"),

            _("First anal for the girl who said it would never happen \U0001F62C\U0001F525"),

            _("Anti-anal girl loses her anal virginity on camera \U0001F631\U0001F4F7"),

            _("She said 'absolutely never'. Then this happened \U0001F608"),

            _("FIRST TIME ANAL and she can't stop shaking \U0001F62C\U0001F525"),

            _("She begged me to stop. I hadn't even started yet \U0001F631\U0001F608"),

            _("Anal debut for the girl who said it was disgusting \U0001F62C\U0001F525"),

            _("She braced herself like she was going to war \U0001F631\U0001F4A5"),

            _("Her anal virginity taken {loc}. She won't sit down tomorrow \U0001F62C\U0001F608"),

        ],

        # ── Anal lover first (her very first anal: she finds out she loves it; the veteran titles wait) ──
        "anal_lover_first": [
            _("Her first time in the ass and she didn't want it to end \U0001F633\U0001F525"),

            _("She was nervous about her first anal. Then she started pushing back \U0001F633\U0001F4A5"),

            _("First anal ever and she's already hooked \U0001F60D\U0001F525"),

            _("She said 'go slow'. Five minutes later it was 'don't stop' \U0001F633\U0001F608"),

            _("Anal virgin finds out what she's been missing {loc} \U0001F633\U0001F525"),

            _("You can hear the exact moment she realizes she loves it \U0001F62E\U0001F4A5"),

        ],

        # ── Cum slut first (creampie video of her very first load: she finds out she loves it) ──
        "cum_slut_first": [
            _("Her first creampie ever. She didn't expect to love it this much \U0001F633\U0001F4A6"),

            _("First time anyone finished inside her. She's still shaking \U0001F633\U0001F4A6"),

            _("She felt her first creampie and whispered 'oh... wow' \U0001F633\U0001F4A6"),

            _("She'd never had a creampie. Now she can't stop thinking about it \U0001F633\U0001F4A6"),

            _("Her first creampie {loc} and she didn't want me to pull out \U0001F60D\U0001F4A6"),

        ],

        # ── ATM (ass-to-mouth during scene) ──
        "atm": [
            _("Ass to mouth. She didn't even hesitate \U0001F92F\U0001F525"),
            _("Straight from her ass to her lips. She tasted everything \U0001F444\U0001F525"),
            _("ATM on camera. She cleaned every inch \U0001F4F7\U0001F525"),
            _("She went ass to mouth without being asked \U0001F92F\U0001F608"),
            _("From the back door to the front. No complaints \U0001F525\U0001F608"),
            _("She licked it clean after it came out of her ass \U0001F444\U0001F92F"),
            _("She sucked it right after I pulled it out of her ass \U0001F92F\U0001F525"),
            _("Zero hesitation. Ass to mouth like a pro \U0001F444\U0001F608"),
            _("She asked to taste it after anal. I didn't have to say anything \U0001F92F"),
            _("She put it in her mouth still warm from her ass \U0001F444\U0001F525"),
            _("ATM queen. She lives for this \U0001F444\U0001F451"),
            _("She gagged a little from the taste but kept going \U0001F92F\U0001F525"),
        ],

        # ── HD recording (tripod / steady cam) ──
        "hd": [
            _("4K quality. You can see every detail \U0001F4F7\U0001F525"),

            _("HD footage. Crystal clear {loc} \U0001F3AC\U0001F525"),

            _("Tripod setup. Professional grade content \U0001F4F7\U0001F3AC"),

            _("The quality on this one is insane \U0001F4F8\U0001F525"),

            _("Shot in HD. Every moan, every detail captured \U0001F3AC\U0001F4F7"),

            _("Steady cam, perfect angle, zero shaking \U0001F4F7\U0001F44C"),

            _("This is what happens when you set up the tripod first \U0001F4F7\U0001F608"),

            _("Cinema quality. She's the main character \U0001F3AC\U0001F31F"),

            _("Full HD. You can count the goosebumps on her skin \U0001F4F8\U0001F525"),

            _("The tripod was the best investment I ever made \U0001F4F7\U0001F4B0"),

            _("Shot from multiple angles. HD perfection \U0001F3AC\U0001F525"),

            _("You won't find better quality anywhere else \U0001F4F7\U0001F451"),

        ],

        # ── Face hidden (anonymity) ──
        "face_hidden": [
            _("You can't see her face but you can hear everything \U0001F3AD\U0001F525"),

            _("Face hidden. She has a reputation to protect \U0001F3AD\U0001F92B"),

            _("She made me promise to hide her face. Fair enough \U0001F3AD\U0001F608"),

            _("Anonymous but you can tell she's hot from the body alone \U0001F3AD\U0001F525"),

            _("No face, no case. She's safe... for now \U0001F3AD\U0001F92B"),

            _("She covers her face but her moans give her away \U0001F3AD\U0001F50A"),

            _("Identity protected but the body speaks for itself \U0001F3AD\U0001F525"),

            _("She'd die if anyone recognized her from this \U0001F3AD\U0001F631"),

            _("Hidden face, exposed everything else \U0001F3AD\U0001F608"),

            _("Mystery girl {loc}. Guess who she is \U0001F3AD\U0001F50D"),

            _("She insisted on anonymity. The body is too good to hide though \U0001F3AD\U0001F525"),

            _("Face hidden but you can hear her begging for more \U0001F3AD\U0001F92B"),

        ],

        # ── Cuckold × additional types ──
        "cuckold:cowgirl": [
            _("She rides me while her boyfriend watches from the corner \U0001F440\U0001F608"),

            _("His girl on top of me. He can see everything \U0001F440\U0001F525"),

            _("She bounces on me while making eye contact with him \U0001F440\U0001F608"),

            _("Cuckold watches his girlfriend ride another man {loc} \U0001F440\U0001F525"),

            _("She grinds on me while he sits there helpless \U0001F440\U0001F608"),

            _("His girlfriend chose to be on top of me. In front of him \U0001F451\U0001F440"),

            _("She rides harder when she knows he's watching \U0001F440\U0001F525"),

            _("He watched her bounce on me for 20 minutes straight \U0001F440\U0001F608"),

            _("His girl on top, his eyes on us, his world collapsing \U0001F440\U0001F525"),

            _("She looked at him and said 'this is what you wanted' while riding me \U0001F440\U0001F608"),

        ],
        "cuckold:hj": [
            _("She strokes me while her boyfriend watches \U0001F440\U0001F608"),

            _("His girlfriend's hand on me. He can see every stroke \U0001F440\U0001F525"),

            _("Cuckold watches his girl jerk off another man {loc} \U0001F440\U0001F608"),

            _("She grabbed me right in front of him \U0001F440\U0001F525"),

            _("Her boyfriend's eyes on her hand, her hand on me \U0001F440\U0001F608"),

            _("She looked at him while stroking me and smiled \U0001F440\U0001F525"),

        ],
        "cuckold:tj": [
            _("Her tits around me while her boyfriend watches {loc} \U0001F440\U0001F608"),

            _("Cuckold watches his girlfriend's titjob from across the room \U0001F440\U0001F525"),

            _("She squeezed her tits around me while he sat there frozen \U0001F440\U0001F608"),

            _("His girl uses her best assets on me. He can only watch \U0001F440\U0001F525"),

            _("Titjob for the bull while the cuck records \U0001F4F7\U0001F440"),

            _("She spit on her tits and looked at him while wrapping them around me \U0001F440\U0001F608"),

        ],

        # ── Threesome × type ──
        "threesome:cowgirl": [
            _("One rides me while the other sits on my face \U0001F525\U0001F608"),

            _("She rides while her friend coaches from the side \U0001F440\U0001F525"),

            _("Two girls taking turns riding me. I lost track of who was on top \U0001F501\U0001F525"),

            _("She bounces on me while her friend holds the camera \U0001F4F7\U0001F525"),

            _("Her friend guided her onto me. Then wanted a turn too \U0001F525\U0001F608"),

            _("One on top, one making out with me. Best multitasking ever \U0001F525\U0001F48B"),

            _("They argued about who gets to ride first \U0001F451\U0001F525"),

            _("She rode me so good her friend got jealous and pushed her off \U0001F501\U0001F608"),

        ],
        "threesome:bj": [
            _("Two mouths on me at the same time \U0001F444\U0001F525"),

            _("They take turns going down on me. I can't feel my legs \U0001F501\U0001F525"),

            _("Double blowjob. They fight over who goes deeper \U0001F444\U0001F608"),

            _("One sucks while the other licks. Teamwork \U0001F444\U0001F525"),

            _("She showed her friend how it's done. Then they did it together \U0001F444\U0001F608"),

            _("Two tongues, one target. I lasted about 30 seconds \U0001F444\U0001F525"),

            _("They kissed with it between them. I almost died \U0001F48B\U0001F525"),

            _("Tag team blowjob. They high-fived after I finished \U0001F444\U0001F3C6"),

        ],
        "threesome:creampie": [
            _("Creampied one while the other watched up close \U0001F4A6\U0001F440"),

            _("Two girls, one creampie. The other one wants next \U0001F4A6\U0001F525"),

            _("I came inside her while her friend held her legs open \U0001F4A6\U0001F608"),

            _("Her friend scooped it out and tasted it \U0001F4A6\U0001F444"),

            _("They both wanted the creampie. I had to pick one \U0001F4A6\U0001F525"),

            _("Creampied them both. Same night. No regrets \U0001F4A6\U0001F608"),

            _("She watched the cream drip out of her friend and said 'my turn' \U0001F4A6\U0001F440"),

            _("Two girls competing for the load. Only one can win \U0001F4A6\U0001F3C6"),

        ],

        # ── Full Nelson × type ──
        "full_nelson:creampie": [
            _("Full nelson creampie. She couldn't escape even if she wanted to \U0001F4AA\U0001F4A6"),

            _("Held her up and came deep inside. Gravity did the rest \U0001F4AA\U0001F4A6"),

            _("She felt every drop while suspended in the air \U0001F4AA\U0001F4A6"),

            _("Full nelson position + raw creampie = her new favorite thing \U0001F4AA\U0001F525"),

            _("Came inside her while her feet dangled off the ground \U0001F4AA\U0001F4A6"),

            _("She tried to squirm when she felt it coming. Couldn't move. Too late \U0001F4AA\U0001F608"),

            _("Full nelson creampie from above. Gravity pushed it deeper \U0001F4AA\U0001F4A6"),

            _("Held her open and filled her up. She went limp after \U0001F4AA\U0001F525"),

        ],

        # ── Cheating × full nelson ──
        "cheating:full_nelson": [
            _("His girlfriend in full nelson. She can't call him for help \U0001F4AA\U0001F608"),

            _("Someone's girl getting the full nelson treatment \U0001F4AA\U0001F92B"),

            _("Her boyfriend never picks her up like this. I do \U0001F4AA\U0001F60F"),

            _("Taken girl lifted off the ground and destroyed \U0001F4AA\U0001F525"),

            _("She moaned his name by accident. I went harder \U0001F4AA\U0001F608"),

            _("Full nelson on another man's girlfriend {loc} \U0001F4AA\U0001F92B"),

            _("His girl held up in the air, completely helpless, loving every second \U0001F4AA\U0001F608"),

            _("He's at work. She's off the ground. Sorry bro \U0001F4AA\U0001F60F"),

        ],

        # ── Cum slut × bj ──
        "cum_slut:bj": [
            _("She begged me to finish in her mouth \U0001F4A6\U0001F60D"),

            _("Cum addict gives the sloppiest blowjob just to get the reward \U0001F4A6\U0001F444"),

            _("She sucked harder the closer I got \U0001F4A6\U0001F525"),

            _("She opened wide and caught every single drop \U0001F4A6\U0001F60B"),

            _("She swallowed without being asked. Twice \U0001F4A6\U0001F929"),

            _("She got mad when a drop landed on her chin instead of her tongue \U0001F4A6\U0001F620"),

            _("She held me in her mouth until she got every last drop \U0001F4A6\U0001F60D"),

            _("Her eyes lit up when she tasted it \U0001F4A6\U0001F929"),

            _("She asked for seconds before I even recovered \U0001F4A6\U0001F525"),

            _("Cum slut on her knees. Her favorite position for her favorite snack \U0001F4A6\U0001F60B"),

        ],

        # ── Hate cum × bj ──
        "hate_cum:bj": [
            _("She hates cum but still got on her knees \U0001F631\U0001F444"),

            _("The panic in her eyes when she felt me getting close \U0001F631\U0001F525"),

            _("She tried to pull away at the last second. Didn't make it \U0001F631\U0001F4A6"),

            _("Anti-cum girl sucking with anxiety in her eyes \U0001F631\U0001F444"),

            _("She gagged before I even finished. Not from the depth \U0001F631\U0001F92D"),

            _("She spit it out immediately. Her face was priceless \U0001F631\U0001F4A6"),

            _("She closed her mouth the second I said I was close \U0001F631\U0001F645"),

            _("Cum hater blowjob. She flinches every time I twitch \U0001F631\U0001F444"),

            _("She held her breath through the whole ending \U0001F631\U0001F4A6"),

            _("The fastest head turn I've ever seen when I said 'I'm close' \U0001F631\U0001F3C3"),

        ],

        # ── Hardcore × tj ──
        "hardcore_sex:tj": [
            _("She squeezes hard enough to leave marks on her own tits \U0001F525\U0001F4A5"),

            _("Rough titjob. She likes when I thrust between them \U0001F525\U0001F62C"),

            _("She presses so hard her knuckles turn white \U0001F4A5\U0001F525"),

            _("Aggressive titjob. She spit on them and went harder \U0001F525\U0001F4A5"),

            _("She slaps her own tits between strokes {loc} \U0001F525\U0001F44B"),

            _("Rough enough to leave her chest red \U0001F525\U0001F4A5"),

            _("She likes the titjob messy, loud, and rough \U0001F525\U0001F62C"),

            _("She presses them so tight I can barely move. She loves the struggle \U0001F4A5\U0001F525"),

        ],

        # ── Cute sex × bj ──
        "cute_sex:bj": [
            _("She looks up at me with those eyes while sucking \U0001F633\U0001F970"),

            _("The shyest blowjob you'll ever see. She keeps blushing \U0001F633\U0001F495"),

            _("She covers her face with one hand while sucking with the other \U0001F648\U0001F970"),

            _("She whispered 'sorry' when she gagged. Adorable \U0001F633\U0001F495"),

            _("She takes it slow and gentle. Every lick is careful \U0001F970\U0001F444"),

            _("She giggles between sucks. I can't handle it \U0001F633\U0001F3B5"),

            _("The way she holds it with both hands like it's precious \U0001F970\U0001F495"),

            _("She blushes harder every time she goes deeper \U0001F633\U0001F970"),

        ],

        # ── Camera lover × cowgirl ──
        "camera_lover:cowgirl": [
            _("She adjusted the camera angle before getting on top \U0001F4F8\U0001F525"),

            _("She rides while looking directly at the lens \U0001F4F8\U0001F609"),

            _("She picked cowgirl because 'it looks best on camera' \U0001F4F8\U0001F608"),

            _("Camera-loving cowgirl. She checks the preview between bounces \U0001F4F8\U0001F525"),

            _("She flips her hair for the camera while riding \U0001F4F8\U0001F48B"),

            _("She asked me to hold the phone steady while she rides \U0001F4F8\U0001F525"),

            _("Natural performer on top. She was born for this angle \U0001F4F8\U0001F31F"),

            _("She winks at the camera every time she bottoms out \U0001F4F8\U0001F609"),

        ],

        # ── Camera lover × creampie ──
        "camera_lover:creampie": [
            _("She spread herself open so the camera could see the creampie \U0001F4F8\U0001F4A6"),

            _("She held the camera to film it dripping out \U0001F4F8\U0001F4A6"),

            _("Camera lover demanded a close-up of the creampie \U0001F4F8\U0001F525"),

            _("She posed for the camera with the cream still inside \U0001F4F8\U0001F4A6"),

            _("She wanted the money shot on film. Got exactly what she asked for \U0001F4F8\U0001F608"),

            _("She asked me to zoom in when I finished inside \U0001F4F8\U0001F4A6"),

            _("She checked the footage and said 'you can see everything. Perfect' \U0001F4F8\U0001F60D"),

            _("She directed the whole creampie like a pro filmmaker \U0001F4F8\U0001F3AC"),

        ],

        # ── Camera lover × bj ──
        "camera_lover:bj": [
            _("She held the camera while going down on me. Selfie angle \U0001F4F8\U0001F444"),

            _("She winked at the lens with my cock in her mouth \U0001F4F8\U0001F609"),

            _("Camera lover gives the most photogenic blowjob \U0001F4F8\U0001F525"),

            _("She looked at the camera, not me, the whole time \U0001F4F8\U0001F444"),

            _("She paused mid-blowjob to check if the angle was good \U0001F4F8\U0001F608"),

            _("She asked for a retake because her lipstick smudged \U0001F4F8\U0001F484"),

            _("She sucked it like she knew millions would watch \U0001F4F8\U0001F31F"),

            _("Born performer. She gives head for the camera, not for me \U0001F4F8\U0001F3AC"),

        ],

        # ── Submissive × bj ──
        "submissive:bj": [
            _("She waits on her knees until I tell her to start \U0001F90D\U0001F444"),

            _("'Can I suck it now, sir?' \U0001F90D\U0001F633"),

            _("Obedient girl on her knees. She doesn't move until I say so \U0001F90D\U0001F608"),

            _("She asked permission before swallowing \U0001F90D\U0001F4A6"),

            _("Good girl takes it as deep as I tell her to \U0001F90D\U0001F525"),

            _("She froze when I said 'stop'. Perfect obedience \U0001F90D\U0001F444"),

            _("'Am I doing it right, sir?' Best blowjob I've ever had \U0001F90D\U0001F608"),

            _("She opens her mouth on command and doesn't close it until I'm done \U0001F90D\U0001F525"),

        ],

        # ── Dominant × bj ──
        "dominant:bj": [
            _("She pushed my head back and said 'let me handle this' \U0001F451\U0001F444"),

            _("She decides the pace, the depth, everything \U0001F451\U0001F525"),

            _("She grabbed it and went down on HER terms \U0001F451\U0001F608"),

            _("She teases me and stops when SHE wants. Not when I beg \U0001F451\U0001F444"),

            _("I tried to push her head. She slapped my hand away \U0001F451\U0001F525"),

            _("She stops right before I finish just to watch me suffer \U0001F451\U0001F608"),

            _("'You'll finish when I let you' \U0001F451\U0001F444"),

            _("She controls the blowjob like she owns it. Because she does \U0001F451\U0001F525"),

        ],

        # ── Public fetish × cowgirl ──
        "public_fetish:cowgirl": [
            _("She rode me {loc} hoping someone would walk by \U0001F440\U0001F525"),

            _("Public cowgirl. She picked the riskiest bench on campus \U0001F440\U0001F608"),

            _("She bounced louder when she heard footsteps nearby \U0001F440\U0001F525"),

            _("Public rider. She came harder knowing someone saw \U0001F440\U0001F608"),

            _("She chose to ride me outside because 'the thrill is different' \U0001F440\U0001F525"),

            _("On top of me {loc} with zero care about who sees \U0001F440\U0001F608"),

            _("She smiled when someone gasped at us {loc} \U0001F440\U0001F525"),

            _("Public fetish girl picks the most exposed spot to ride \U0001F440\U0001F608"),

        ],

        # ── Exhibitionist × cowgirl ──
        "exhibitionist:cowgirl": [
            _("She stripped down and got on top without checking if anyone was around \U0001F440\U0001F525"),

            _("Naked cowgirl {loc}. She wants the world to see \U0001F30D\U0001F525"),

            _("She rides with the curtains open and the lights on \U0001F440\U0001F608"),

            _("Exhibitionist on top. She waves at people who stare \U0001F440\U0001F525"),

            _("She took everything off before getting on top. Everything \U0001F460\U0001F525"),

            _("She bounces on me facing the window on purpose \U0001F440\U0001F608"),

            _("Naked, on top, no shame. Just how she likes it \U0001F525\U0001F60F"),

            _("She left the door unlocked while riding. On purpose \U0001F6AA\U0001F525"),

        ],

        # ── Face hidden × cowgirl ──
        "face_hidden:cowgirl": [
            _("She rides with a mask on. Body says it all though \U0001F3AD\U0001F525"),

            _("Anonymous cowgirl. You can't see her face but you can see the bounce \U0001F3AD\U0001F608"),

            _("Face hidden but her moans while riding gave her away \U0001F3AD\U0001F50A"),

            _("She rides me facing away so the camera never catches her face \U0001F3AD\U0001F525"),

            _("Mystery rider {loc}. Who is she? \U0001F3AD\U0001F50D"),

            _("Anonymous on top. Her body is the only ID you need \U0001F3AD\U0001F525"),

            _("She covered her face with a pillow while riding me. Smart girl \U0001F3AD\U0001F608"),

            _("Face hidden cowgirl. But those hips don't lie \U0001F3AD\U0001F525"),

        ],

        # ── Face hidden × creampie ──
        "face_hidden:creampie": [
            _("Anonymous creampie. She doesn't want you to know who she is \U0001F3AD\U0001F4A6"),

            _("You can't see her face but you can see the cream dripping out \U0001F3AD\U0001F4A6"),

            _("Face hidden but the creampie is in full view \U0001F3AD\U0001F525"),

            _("She hid her face the whole time. The creampie is the star of the show \U0001F3AD\U0001F4A6"),

            _("Anonymous girl gets filled up {loc} \U0001F3AD\U0001F4A6"),

            _("No face shown. But the sounds she made when I came inside... \U0001F3AD\U0001F4A6"),

            _("She covered her face and whispered 'don't show anyone' as I finished inside \U0001F3AD\U0001F92B"),

            _("Mystery girl creampied {loc}. Guess who \U0001F3AD\U0001F4A6"),

        ],

        # ── Face hidden × bj ──
        "face_hidden:bj": [
            _("You can hear the sloppy sounds but can't see who it is \U0001F3AD\U0001F444"),

            _("Anonymous blowjob. She made sure her face wasn't in frame \U0001F3AD\U0001F92B"),

            _("Face hidden but her mouth game speaks for itself \U0001F3AD\U0001F525"),

            _("She went down on me with her hair covering her face \U0001F3AD\U0001F444"),

            _("Mystery lips on me {loc}. No face, just talent \U0001F3AD\U0001F525"),

            _("She sucked me off anonymously. Smart AND skilled \U0001F3AD\U0001F608"),

            _("Face hidden blowjob. The sounds are enough \U0001F3AD\U0001F50A"),

            _("Anonymous head from a girl who clearly knows what she's doing \U0001F3AD\U0001F444"),

        ],

        # ── HD × cowgirl ──
        "hd:cowgirl": [
            _("4K cowgirl. Every bounce in crystal clear detail \U0001F4F7\U0001F525"),

            _("Tripod caught every second of her riding in HD \U0001F4F7\U0001F3AC"),

            _("HD from below. Best angle, best quality \U0001F4F7\U0001F525"),

            _("She rides in 4K. You can see every detail of her body \U0001F4F7\U0001F608"),

            _("The tripod made this cowgirl video look professional \U0001F4F7\U0001F31F"),

            _("HD bounce compilation. Every frame is perfect \U0001F4F7\U0001F525"),

            _("Crystal clear footage of her on top {loc} \U0001F4F7\U0001F3AC"),

            _("4K cowgirl POV. The quality upgrade is insane \U0001F4F7\U0001F525"),

        ],

        # ── HD × creampie ──
        "hd:creampie": [
            _("4K creampie. You can see every drop go inside \U0001F4F7\U0001F4A6"),

            _("HD close-up of the cream dripping out \U0001F4F7\U0001F4A6"),

            _("Tripod caught the exact moment I finished inside. Crystal clear \U0001F4F7\U0001F525"),

            _("The creampie in 4K is a different experience \U0001F4F7\U0001F4A6"),

            _("HD footage of every drop filling her up \U0001F4F7\U0001F4A6"),

            _("You can see the goosebumps on her skin when I came inside. 4K is something else \U0001F4F7\U0001F525"),

            _("Professional quality creampie footage {loc} \U0001F4F7\U0001F3AC"),

            _("The drip in full HD. Worth every pixel \U0001F4F7\U0001F4A6"),

        ],

        # ── Anal lover × creampie ──
        "anal_lover:creampie": [
            _("Anal creampie for the girl who begged for it \U0001F4A6\U0001F525"),

            _("She wanted it in her ass AND she wanted me to finish there too \U0001F4A6\U0001F60D"),

            _("Anal queen gets her favorite filling in her favorite hole \U0001F4A6\U0001F451"),

            _("She pushed back harder when she felt me getting close in her ass \U0001F4A6\U0001F525"),

            _("Anal creampie and she moaned louder than ever \U0001F4A6\U0001F4A5"),

            _("She held still so she could feel every drop go in her ass \U0001F4A6\U0001F60D"),

            _("Anal addict gets the ultimate reward \U0001F4A6\U0001F525"),

            _("She clenched when I came in her ass and said 'don't pull out yet' \U0001F4A6\U0001F608"),

        ],

        # ── Anal hater × creampie ──
        "anal_hater:creampie": [
            _("Anti-anal girl gets a creampie in the worst possible hole \U0001F631\U0001F4A6"),

            _("She hates anal AND I came inside her ass. Double nightmare \U0001F631\U0001F4A6"),

            _("She screamed louder when she felt it filling up her ass \U0001F631\U0001F525"),

            _("Anal hater creampied in the ass against her will {loc} \U0001F631\U0001F4A6"),

            _("She tried to push me out when she felt it coming. Couldn't \U0001F631\U0001F4A6"),

            _("The LOOK on her face when she felt the warm load in her ass \U0001F631\U0001F608"),

            _("She hates the hole, hates the filling, still took both \U0001F631\U0001F4A6"),

            _("Anal hater gets the full experience in the hole she despises most \U0001F631\U0001F525"),

        ],

        # ── Cheating × anal ──
        "cheating:anal": [
            _("His girlfriend takes it in the ass for someone else \U0001F608\U0001F525"),

            _("She won't do anal for her boyfriend. But she does it for me \U0001F60F\U0001F525"),

            _("Anal with someone else's girl {loc} \U0001F608\U0001F92B"),

            _("She said her boyfriend never gets this hole. I got it on the first try \U0001F60F"),

            _("His girlfriend's ass belongs to me now \U0001F608\U0001F525"),

            _("She does things for me she'd never do for him. Anal is one of them \U0001F92B\U0001F608"),

            _("His girl screamed my name while I was in her ass \U0001F608\U0001F525"),

            _("Taken girl gives up her last hole to someone who isn't her boyfriend \U0001F60F\U0001F525"),

        ],

        # ── Threesome × hj ──
        "threesome:hj": [
            _("Four hands on me at the same time. I can't think straight \U0001F525\U0001F608"),

            _("They take turns stroking. One fast, one slow. I'm losing my mind \U0001F501\U0001F525"),

            _("One hand from each girl. Perfect teamwork \U0001F525\U0001F3C6"),

            _("Her friend joined in with her hand. They giggled the whole time \U0001F525\U0001F608"),

            _("They compete over who has the better grip \U0001F525\U0001F451"),

            _("Double handjob. I didn't last three minutes \U0001F525\U0001F608"),

        ],

        # ── Threesome × tj ──
        "threesome:tj": [
            _("Four tits around me at the same time. Heaven \U0001F525\U0001F608"),

            _("They pressed their tits together with me in the middle \U0001F525\U0001F4A5"),

            _("Double titjob. I'm sandwiched between four of the best \U0001F525\U0001F608"),

            _("She and her friend squeezed me between their chests. I saw stars \U0001F525\U0001F31F"),

            _("They argued about whose tits are better. I said 'let me test both' \U0001F525\U0001F451"),

            _("Sliding between two pairs of tits at once. Unreal \U0001F525\U0001F608"),

        ],

        # ── Public shy × cowgirl ──
        "public_shy:cowgirl": [
            _("She rode me shaking with fear someone would see {loc} \U0001F633\U0001F525"),

            _("Shy girl on top {loc}. She kept looking over her shoulder \U0001F633\U0001F440"),

            _("She whispered 'we're going to get caught' while still bouncing \U0001F633\U0001F631"),

            _("Nervous cowgirl. She rides fast because she wants to finish before anyone sees \U0001F633\U0001F525"),

            _("She almost stopped when she heard a door open. Almost \U0001F633\U0001F631"),

            _("Shy girl on top trying to stay quiet {loc}. She failed \U0001F633\U0001F50A"),

            _("She covered her mouth with one hand while riding to muffle the moans \U0001F633\U0001F92B"),

            _("Terrified of getting caught on top of me but too turned on to stop \U0001F633\U0001F525"),

        ],

        # ── Exhibitionist × bj ──
        "exhibitionist:bj": [
            _("She got on her knees in public and didn't care who saw \U0001F440\U0001F444"),

            _("Exhibitionist blowjob. She wants an audience \U0001F440\U0001F525"),

            _("She sucked me off with the door wide open \U0001F6AA\U0001F444"),

            _("She gave me head where anyone could walk by. On purpose \U0001F440\U0001F608"),

            _("Zero shame. She got on her knees {loc} like it was nothing \U0001F440\U0001F525"),

            _("She made eye contact with a stranger while going down on me \U0001F440\U0001F608"),

            _("Born exhibitionist. She sucks louder when people are nearby \U0001F50A\U0001F444"),

            _("She blew me by the window so the neighbors could watch \U0001F440\U0001F525"),

        ],
    }

    # Priority order for trait title selection
    _FEED_TRAIT_PRIORITY = [
        "cuckold", "threesome", "girl_recorded", "cheating", "virgin", "anal_hater_first", "anal_lover_first", "cum_slut_first",
        "full_nelson", "atm", "no_condom", "hate_cum", "cum_slut",
        "anal_lover", "anal_hater",
        "hardcore_sex", "camera_hater", "secret", "face_hidden", "camera_lover", "public_fetish",
        "public_shy", "exhibitionist", "cute_sex", "submissive", "dominant", "hd",
    ]

    def _get_vid_trait_tags(vid):
        """Determine which trait tags apply to a video for title selection."""
        tags = []
        girl = GIRL_BY_ID.get(vid.get("girl_gid", ""))
        vtype = vid.get("type", "hj")
        _pen_types = {"cowgirl", "reverse_cowgirl", "reverse_cowgirl_anal", "doggy", "anal", "creampie"}

        # Cheating
        if vid.get("committed", False):
            tags.append("cheating")

        # Virgin (from snapshot or special tag)
        snap = vid.get("snapshot", {})
        if (snap.get("was_virgin", False) and vtype in _pen_types) or vid.get("special") == "virginity":
            tags.append("virgin")

        # No condom (penetration only)
        if vtype in _pen_types and vid.get("condom") is False:
            tags.append("no_condom")

        # Cuckold (NPC partner watching)
        if vid.get("cuckold", False):
            tags.append("cuckold")

        # Threesome (another girl present)
        if vid.get("threesome", False):
            tags.append("threesome")

        # Girl recording (another girl held the camera)
        if vid.get("recorder_gid") and vid.get("recorder_gid") in [g.gid for g in store.ALL_GIRLS]:
            tags.append("girl_recorded")

        # Full Nelson position
        if vtype in ("full_nelson", "full_nelson_anal"):
            tags.append("full_nelson")

        # Laying Down position
        if vtype in ("laying_down", "laying_anal"):
            tags.append("laying_down")

        # ATM tag from recording metadata
        if vid.get("atm"):
            tags.append("atm")

        # HD recording
        if vid.get("hd", False):
            tags.append("hd")

        # Face hidden
        if vid.get("face_hidden", False):
            tags.append("face_hidden")

        if girl is None:
            return tags

        # Trait checks on the girl
        _ht = getattr(girl, "has_trait", None)
        if not _ht:
            return tags

        # Eager traits at the stage she was at when it was shot (snapshot; an older video: her stage now). Still
        # discovering one: never its veteran titles, only "<trait>_first" on her very first time
        _disc = _vid_snap(vid, "discovering")
        if _disc is None:
            _disc = trait_discovery_state(girl)
        _anal_vid = vtype in _ANAL_SCENE_TYPES or (vtype == "creampie" and vid.get("anal_creampie", False))

        if _ht("hate_cum"):
            tags.append("hate_cum")
        if _ht("cum_slut"):
            if "cum_slut" not in _disc:
                tags.append("cum_slut")
            elif _disc["cum_slut"] == "first" and vtype == "creampie" and vid.get("reaction") in ("loved", "accepted"):
                tags.append("cum_slut_first")   # the load is in this video and she wanted it
        if _ht("hardcore_sex") and "hardcore_sex" not in _disc:
            tags.append("hardcore_sex")
        if _ht("cute_sex"):
            tags.append("cute_sex")
        # Secret recording: always tag non-consensual videos
        if not vid.get("consensual", True):
            tags.append("secret")
            if _ht("camera_hater"):
                tags.append("camera_hater")
        if _ht("camera_lover"):
            tags.append("camera_lover")
        if _ht("public_fetish"):
            tags.append("public_fetish")
        if _ht("public_shy"):
            tags.append("public_shy")
        if _ht("exhibitionist"):
            tags.append("exhibitionist")
        if _ht("anal_lover") and _anal_vid:
            if "anal_lover" not in _disc:
                tags.append("anal_lover")
            elif _disc["anal_lover"] == "first":
                tags.append("anal_lover_first")
        if _ht("anal_hater") and _anal_vid:
            tags.append("anal_hater")
            _sa = getattr(girl, "Sex_acts", {}) or {}
            if _sa.get("anal", 0) <= 1:
                tags.append("anal_hater_first")
        if _ht("submissive"):
            tags.append("submissive")
        # the title pools say "dominant", the trait is femdom (no trait was ever called "dominant"); still finding out
        # she likes giving orders: not yet
        if _ht("femdom") and "femdom" not in _disc:
            tags.append("dominant")

        return tags

    def bigfans_feed_title(entry):
        """Build a creative title for a published video.
        Prefers trait-specific clickbait titles when available."""
        vid = entry["vid"]
        vtype = vid.get("type", "hj")
        # RCG/doggy share cowgirl video titles for now; her ass in the reverse cowgirl shares the anal ones
        if vtype in ("reverse_cowgirl", "doggy"):
            vtype = "cowgirl"
        elif vtype == "reverse_cowgirl_anal":
            vtype = "anal"
        loc = vid.get("location", "room")
        loc_phrase = _tl(_FEED_LOC_PHRASES.get(loc, "somewhere private"))
        _is_virginity = vid.get("special") == "virginity"

        # Deterministic seed for stable title across sessions
        _seed = hash((vid.get("girl_gid", ""), vtype, loc, entry.get("published_day", 0)))

        # Try trait-specific titles first (pick based on seed for variety)
        _tags = _get_vid_trait_tags(vid)
        if _tags:
            _ordered = [t for t in _FEED_TRAIT_PRIORITY if t in _tags]
            if _ordered:
                # Virginity videos ALWAYS use "virgin" tag — it's rare, unique content
                if _is_virginity and "virgin" in _ordered:
                    _pick_tag = "virgin"
                else:
                    _pick_tag = _ordered[_seed % len(_ordered)]
                # Prefer type-specific pool (e.g. "cheating:reverse_cowgirl") over generic
                _type_key = _pick_tag + ":" + vtype
                _pool = _FEED_TITLES_TRAIT.get(_type_key) or _FEED_TITLES_TRAIT.get(_pick_tag, [])
                if _pool:
                    title = _tl(_pool[_seed % len(_pool)])
                    title = title.replace("{loc}", loc_phrase)
                    if _pick_tag == "cheating":
                        _bf_girl = GIRL_BY_ID.get(vid.get("girl_gid"))
                        if _bf_girl and hasattr(_bf_girl, "get_flag"):
                            # a girlfriend: the shared word swap of the language (cheat_guilt), + the titles' own slang
                            title = _cheat_gf_sub(_bf_girl, title)
                            if _bf_girl.get_flag("partner_is_female") and not renpy.game.preferences.language:
                                for _old, _new in [(" bro", " sis"), ("her man", "her woman")]:
                                    title = title.replace(_old, _new)
                            # Russian declines her partner: its titles carry the case keys
                            if "%(" in title:
                                title = fmt_safe(title, partner_fmt(_bf_girl))
                    if _is_virginity:
                        return "\U0001F534 RARE: " + title
                    return title

        # Fallback to generic type-based titles
        templates = _FEED_TITLES.get(vtype, [_("Hot video {loc}")])
        title = _tl(templates[_seed % len(templates)])
        return title.replace("{loc}", loc_phrase)

    def bigfans_feed_label(entry):
        """Build display label for a published video."""
        vid = entry["vid"]
        girl = GIRL_BY_ID.get(vid.get("girl_gid"))
        name = girl.Name if girl else vid.get("girl_gid", "???")
        color = girl.color if girl and hasattr(girl, "color") else "#e2e8f0"
        _special = vid.get("special")
        if _special:
            vtype = _tr(SPECIAL_VIDEO_DISPLAY.get(_special, VIDEO_TYPE_DISPLAY.get(vid.get("type", "?"), vid.get("type", "?"))))
        else:
            vtype = _tr(VIDEO_TYPE_DISPLAY.get(vid.get("type", "?"), vid.get("type", "?")))
        return "{color=%s}%s{/color} - %s" % (color, name, vtype)

    def bigfans_video_duration(entry):
        """Return duration string. Uses recorded seconds if available, else deterministic random."""
        vid = entry["vid"]
        _dur = vid.get("duration_seconds", 0)
        if _dur <= 0:
            _ticks = vid.get("duration_ticks", 0)
            if _ticks > 0:
                _seed = hash((vid.get("girl_gid", ""), vid.get("type", "")))
                _dur = _ticks * (25 + (_seed % 11))
        if _dur > 0:
            _total_secs = int(_dur)
            minutes = _total_secs // 60
            seconds = _total_secs % 60
        else:
            _seed = hash((vid.get("girl_gid", ""), vid.get("type", ""), vid.get("location", ""), entry.get("published_day", 0)))
            minutes = (_seed % 4)
            seconds = (_seed // 4) % 50 + 10
        return "%d:%02d" % (minutes, seconds)

    def bigfans_video_duration_seconds(vid):
        """Return total duration in seconds for matching against requests."""
        _dur = vid.get("duration_seconds", 0)
        if _dur <= 0:
            _ticks = vid.get("duration_ticks", 0)
            if _ticks > 0:
                _seed = hash((vid.get("girl_gid", ""), vid.get("type", "")))
                _dur = _ticks * (25 + (_seed % 11))
        if _dur > 0:
            return int(_dur)
        return renpy.random.randint(60, 180)

    def _recording_current_duration():
        """Return (minutes, seconds) for the current recording overlay."""
        _total = int(getattr(store, "_recording_seconds", 0.0))
        return (_total // 60, _total % 60)

    def recording_tick(rounds=1):
        """Add recording time based on rounds spent. Rate varies per recording for natural-looking durations."""
        if getattr(store, "_recording_active", False):
            _rate = getattr(store, "_recording_sec_rate", 0.0)
            if _rate <= 0:
                _vids = getattr(store.Player, "recorded_videos", [])
                if _vids:
                    _v = _vids[-1]
                    _seed = hash((_v.get("girl_gid", ""), _v.get("type", ""), len(_vids)))
                    _rate = 3.5 + (_seed % 40) / 10.0
                else:
                    _rate = 5.0
                store._recording_sec_rate = _rate
            store._recording_seconds = getattr(store, "_recording_seconds", 0.0) + (rounds * _rate)

    def _get_recording_stopper_name():
        """Get the name of whoever is holding the camera, or None if it's the player."""
        _wgid = getattr(store, "_recording_watcher_gid", None)
        if not _wgid:
            return None
        _wg = store.GIRL_BY_ID.get(_wgid)
        if _wg:
            return _wg.Name
        _npc = getattr(store, "_ntr_watching_npc", None)
        if _npc and hasattr(_npc, "Name"):
            return _npc.Name
        return None

    def finalize_recording():
        """Save duration to the last recorded video and stop recording."""
        if getattr(store, "_recording_active", False):
            _secs = getattr(store, "_recording_seconds", 0.0)
            _vids = getattr(store.Player, "recorded_videos", [])
            if _vids:
                _vids[-1]["duration_seconds"] = max(30, int(_secs))
                if getattr(store, "_recording_had_atm", False):
                    _vids[-1]["atm"] = True
                    store._recording_had_atm = False
            _watcher_gid = getattr(store, "_recording_watcher_gid", None)
            if _watcher_gid and _watcher_gid in [g.gid for g in store.ALL_GIRLS]:
                _wg = store.GIRL_BY_ID.get(_watcher_gid)
                if _wg:
                    sprite_state.setdefault(_wg.Id, {})["arm_pos"] = 0
                    _wr_at = sprite_state.get(_wg.Id, {}).get("_last_at_list", [slot_right])
                    set_girl_sprite(_wg.gid, pose="standing", at_list=_wr_at)
            store._recording_active = False
            store._recording_girl = None
            store._recording_seconds = 0.0
            store._recording_sec_rate = 0.0
            store._recording_face_locked = False
            store._player_hand_disabled = None
            store._recording_watcher_gid = None
            if renpy.get_screen("recording_overlay"):
                renpy.hide_screen("recording_overlay")
        # A pending ATM mark never outlives its scene. Without an active recording it stayed True and the NEXT
        # recorded video, whatever it showed, got the "atm" tag (BigFans caption + video reactions).
        if getattr(store, "_recording_had_atm", False):
            print("[ATM] finalize_recording: pending ATM mark dropped, no active recording")
            store._recording_had_atm = False

# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
label shop_online:
    $ Narration(_("You grab your laptop and open the browser. Time to restock."))
    jump shop_online_loop

# ------------------------------------------------------------
# Main shop loop... category selection
# ------------------------------------------------------------
label shop_online_loop:

    menu:
        "Condoms":
            call shop_protection from _call_shop_protection
            jump shop_online_loop

        "Drinks":
            call shop_drinks from _call_shop_drinks
            jump shop_online_loop

        "Gifts":
            call shop_gifts from _call_shop_gifts
            jump shop_online_loop

        "Close store":
            $ Narration(_("You close the tab and put the laptop away."))
            return

# ------------------------------------------------------------
# Condoms section
# ------------------------------------------------------------
label shop_protection:

    $ Narration(_("Condoms. You have [Player.get_item_count('condom')] condom(s) in stock."))

    menu:

        "Condom... $15 (x1)" if Player.cash >= 15:
            $ Player.spend_cash(15)
            $ Player.add_item("condom", 1)
            $ Narration(_("Ordered. 1 condom on the way. Balance: $[Player.cash]."))
            return

        "!disabled!Condom... $15 (x1)  (Need $[15 - Player.cash] more)" if Player.cash < 15:
            return

        "Condom... $75 (x6)" if Player.cash >= 75:
            $ Player.spend_cash(75)
            $ Player.add_item("condom", 6)
            $ Narration(_("Ordered. 6-pack of condoms on the way. Balance: $[Player.cash]."))
            return

        "!disabled!Condom... $75 (x6)  (Need $[75 - Player.cash] more)" if Player.cash < 75:
            return

        "Back":
            return

# ------------------------------------------------------------
# Pharmacy (Mall) — in-store condom shop
# ------------------------------------------------------------
default _pharmacy_visited = False

label pharmacy_shop:
    scene bg pharmacy with dissolve
    python:
        _pharm_clerk = Character(_("Clerk"), color="#66cc99")
        # Show girls that followed the player to the mall
        _pharm_girls = [g for g in Party if g.loc == "mall"]
        _pharm_slots = [slot_right, slot_center, slot_left]
        for _phi, _phg in enumerate(_pharm_girls[:3]):
            set_girl_sprite(_phg.gid, pose="standing", at_list=[_pharm_slots[_phi]])

    if not _pharmacy_visited:
        $ Say_Player(_("(This place seems to have good prices. Without paying shipping and app fees, I think I can save here, even if it takes a bit more time...)"))
        $ Say_Player(_("(Migraine pills... Mouthwash... Condoms! And... Japanese... Condoms? What the hell is that?)"))
        $ Narration(_("The clerk notices you staring at the Japanese condoms."))
        $ _pharm_clerk(_("Hey, welcome. Those just came in as an import. They're a bit pricier, but supposedly they're much thinner, or something like that."))
        $ _pharm_clerk(_("Except I think this batch might be defective, we've had some complaints..."))
        $ Say_Player(_("Complaints? Not thin enough?"))
        $ _pharm_clerk(_("Actually, I think they're way thinner than normal and it ended up compromising the durability a bit."))
        $ _pharm_clerk(_("We just didn't send them all back because plenty of people keep buying them anyway, go figure..."))
        $ Say_Player(_("Got it. Thanks for the heads up."))
        $ Say_Player(_("(I think I know exactly why people buy those... Well, I'll look into it later.)"))
        # Pregnancy system on: the clerk also introduces the pills and the fertility vitamins
        if store._pregnancy_mode != "off":
            $ Say_Player(_("Sunflower Fertility Shield? What is that?"))
            $ _pharm_clerk(_("Ah, that's a kind of birth control pill based on alternative medicine. You know, regular pills are full of hormones and can be pretty invasive. These are made from sunflower seeds, so they're gentler on women."))
            $ Say_Player(_("And they probably don't work."))
            $ _pharm_clerk(_("Well... maybe... But those over there definitely work. Male fertility pills. All kinds of natural stuff to boost sperm health."))
            $ Say_Player(_("People actually buy those?"))
            $ _pharm_clerk(_("Of course! They raise the chance of getting your partner pregnant by up to 200 percent. Great for couples who want to plan their kids for the right time."))
            $ Say_Player(_("(Well... who knows, maybe one day...)"))
        $ store._pharmacy_visited = True
    else:
        $ _pharm_clerk(_("Welcome!"))

    while True:
        menu:
            "Condom (x1)... $10" if Player.cash >= 10:
                $ Player.spend_cash(10)
                $ Player.add_item("condom", 1)
                $ _pharmacy_popup("Condom", 1, 10)

            "!disabled!Condom (x1)... $10" if Player.cash < 10:
                return

            "Condom (x6)... $50" if Player.cash >= 50:
                $ Player.spend_cash(50)
                $ Player.add_item("condom", 6)
                $ _pharmacy_popup("Condom", 6, 50)

            "!disabled!Condom (x6)... $50" if Player.cash < 50:
                return

            "Condom (x10)... $75" if Player.cash >= 75:
                $ Player.spend_cash(75)
                $ Player.add_item("condom", 10)
                $ _pharmacy_popup("Condom", 10, 75)

            "!disabled!Condom (x10)... $75" if Player.cash < 75:
                return

            "Japanese Condom (x1)... $50" if Player.cash >= 50:
                $ Player.spend_cash(50)
                $ Player.add_item("japanese_condom", 1)
                $ _pharmacy_popup("JP Condom", 1, 50)

            "!disabled!Japanese Condom (x1)... $50" if Player.cash < 50:
                return

            "Japanese Condom (x6)... $250" if Player.cash >= 250:
                $ Player.spend_cash(250)
                $ Player.add_item("japanese_condom", 6)
                $ _pharmacy_popup("JP Condom", 6, 250)

            "!disabled!Japanese Condom (x6)... $250" if Player.cash < 250:
                return

            "Birth Control Pills... $50" if Player.cash >= 50 and store._pregnancy_mode != "off":
                $ Player.spend_cash(50)
                $ Player.add_item("birth_control", 1)
                $ _pharmacy_popup("Birth Control Pills", 1, 50)

            "!disabled!Birth Control Pills... $50" if Player.cash < 50 and store._pregnancy_mode != "off":
                pass

            "Sunflower Fertility Shield... $30" if Player.cash >= 30 and store._pregnancy_mode != "off":
                $ Player.spend_cash(30)
                $ Player.add_item("placebo_pills", 1)
                $ _pharmacy_popup("Sunflower Fertility Shield", 1, 30)

            "!disabled!Sunflower Fertility Shield... $30" if Player.cash < 30 and store._pregnancy_mode != "off":
                pass

            "Morning After Pill... $100" if Player.cash >= 100 and store._pregnancy_mode != "off":
                $ Player.spend_cash(100)
                $ Player.add_item("morning_after", 1)
                $ _pharmacy_popup("Morning After Pill", 1, 100)

            "!disabled!Morning After Pill... $100" if Player.cash < 100 and store._pregnancy_mode != "off":
                pass

            "Fertility Vitamins... $200" if Player.cash >= 200 and store._pregnancy_mode != "off":
                python:
                    # the purchase IS the 7-day buff ("You swallow the pills"): no inventory item left behind
                    Player.spend_cash(200)
                    store._player_fertility_vitamin_active = True
                    store._player_fertility_vitamin_days = _FERT_VITAMIN_DAYS
                    _pharmacy_popup("Fertility Vitamins", 1, 200)
                    print("[PREGNANCY] fertility vitamin purchased, %d days active (x%s)" % (_FERT_VITAMIN_DAYS, _FERT_VITAMIN_MULT))
                "You swallow the pills and feel... more potent. They'll last for a week."

            "!disabled!Fertility Vitamins... $200" if Player.cash < 200 and store._pregnancy_mode != "off":
                pass

            "Leave":
                call Set_Scene(entry=True) from _call_Set_Scene_pharmacy_back
                return

# ------------------------------------------------------------
# Geek Store (Mall)
# ------------------------------------------------------------

default _electronics_visited = False

label electronics_store:
    scene bg electronics_store with dissolve
    python:
        _elec_clerk = Character(_("Clerk"), color="#ff9900")
        _elec_girls = [g for g in Party if g.loc == "mall"]
        if len(_elec_girls) == 1:
            set_girl_sprite(_elec_girls[0].gid, pose="standing", at_list=[slot_right])
        elif len(_elec_girls) >= 2:
            set_girl_sprite(_elec_girls[0].gid, pose="standing", at_list=[slot_center])
            set_girl_sprite(_elec_girls[1].gid, pose="standing", at_list=[slot_right])

    if not _electronics_visited:
        $ _elec_clerk(_("Hey, welcome, welcome my super friendo! I've got games, consoles, manga! Everything for the traditional, rustic, macho man!"))
        $ _elec_clerk(_("I can't believe you still don't have a camcorder! Phones are low quality, check out the world's best-selling new camcorder! Buy a tripod too and record your tekatuk dances in high quality!"))
        $ Say_Player(_("What the f... Ok, I'll be quick with the shopping."))
        $ store._electronics_visited = True
    else:
        $ _elec_clerk(_("Welcome back, friendo!"))

    while True:
        menu:
            # ── Buy-once items ──
            "{color=#e0a030}Tripod{/color}... $100" if Player.cash >= 100 and not Player.has_item("tripod"):
                $ Player.spend_cash(100)
                $ Player.add_item("tripod", 1)
                $ _pharmacy_popup("Tripod", 1, 100)

            "!disabled!{color=#e0a030}Tripod{/color}... $100 {size=18}(owned){/size}" if Player.has_item("tripod"):
                pass

            "!disabled!{color=#e0a030}Tripod{/color}... $100" if Player.cash < 100 and not Player.has_item("tripod"):
                pass

            "TekMix HD 5.2K 9in1 Camera... $500" if Player.cash >= 500 and not Player.has_item("tekmix_camera"):
                $ Player.spend_cash(500)
                $ Player.add_item("tekmix_camera", 1)
                $ _pharmacy_popup(_("TekMix Camera"), 1, 500)

            "!disabled!TekMix HD 5.2K 9in1 Camera... $500 {size=18}(owned){/size}" if Player.has_item("tekmix_camera"):
                pass

            "!disabled!TekMix HD 5.2K 9in1 Camera... $500" if Player.cash < 500 and not Player.has_item("tekmix_camera"):
                pass

            # ── Gifts (repeatable, cheap to expensive) ──
            "Blazing Flames With No Monetary Value... $50" if Player.cash >= 50:
                $ Player.spend_cash(50)
                $ Player.add_item("blazing_flames", 1)
                $ _pharmacy_popup(_("Blazing Flames"), 1, 50)

            "!disabled!Blazing Flames With No Monetary Value... $50" if Player.cash < 50:
                pass

            "My Hero College Manga... $50" if Player.cash >= 50:
                $ Player.spend_cash(50)
                $ Player.add_item("my_hero_college", 1)
                $ _pharmacy_popup(_("My Hero College"), 1, 50)

            "!disabled!My Hero College Manga... $50" if Player.cash < 50:
                pass

            "One Frame Man Manga... $50" if Player.cash >= 50:
                $ Player.spend_cash(50)
                $ Player.add_item("one_frame_man", 1)
                $ _pharmacy_popup(_("One Frame Man"), 1, 50)

            "!disabled!One Frame Man Manga... $50" if Player.cash < 50:
                pass

            "Super Shopping Cart... $80" if Player.cash >= 80:
                $ Player.spend_cash(80)
                $ Player.add_item("supra_marcio_kart", 1)
                $ _pharmacy_popup(_("Super Shopping Cart"), 1, 80)

            "!disabled!Super Shopping Cart... $80" if Player.cash < 80:
                pass

            "Catch Monsters With Balls 89 - Drunk-Tank-Pink Version... $100" if Player.cash >= 100:
                $ Player.spend_cash(100)
                $ Player.add_item("catch_monsters_89", 1)
                $ _pharmacy_popup(_("Catch Monsters 89"), 1, 100)

            "!disabled!Catch Monsters With Balls 89 - Drunk-Tank-Pink Version... $100" if Player.cash < 100:
                pass

            "FuckPop Bobblehead... $100" if Player.cash >= 100:
                $ Player.spend_cash(100)
                $ Player.add_item("fuckpop_bobblehead", 1)
                $ _pharmacy_popup(_("FuckPop Bobblehead"), 1, 100)

            "!disabled!FuckPop Bobblehead... $100" if Player.cash < 100:
                pass

            "Fuck Fuck Flush... $90" if Player.cash >= 90:
                $ Player.spend_cash(90)
                $ Player.add_item("fuck_fuck_flush", 1)
                $ _pharmacy_popup(_("Fuck Fuck Flush"), 1, 90)

            "!disabled!Fuck Fuck Flush... $90" if Player.cash < 90:
                pass

            "Thisdendo 3DS Console... $250" if Player.cash >= 250:
                $ Player.spend_cash(250)
                $ Player.add_item("thisdendo_3ds", 1)
                $ _pharmacy_popup(_("Thisdendo 3DS"), 1, 250)

            "!disabled!Thisdendo 3DS Console... $250" if Player.cash < 250:
                pass

            "Leave":
                call Set_Scene(entry=True) from _call_Set_Scene_electronics_back
                return

# ------------------------------------------------------------
# Bikini Store (Mall) — in-store bikini shop
# ------------------------------------------------------------

init python:
    BIKINI_STORE_ITEMS = {
        "gwen": [
            {"id": "bikini_gwen", "label": "Black Bikini", "price": 200},
        ],
        "rogue": [
            {"id": "bikini_rogue", "label": "Green Bikini", "price": 200},
        ],
        "ntw": [
            {"id": "bikini_ntw", "label": "Pink Bikini", "price": 200},
        ],
        "tenny": [
            {"id": "bikini_tenny", "label": "Blue Bikini", "price": 200},
        ],
        "shion": [
            {"id": "bikini_shion", "label": "Red Bikini", "price": 200},
        ],
    }

    def _bikini_girl_all_bought(gid):
        items = BIKINI_STORE_ITEMS.get(gid, [])
        return all(_is_unique_gift_purchased(it["id"]) for it in items)

    def _bikini_girl_has_available(gid):
        items = BIKINI_STORE_ITEMS.get(gid, [])
        return any(not _is_unique_gift_purchased(it["id"]) for it in items)

    def _dressing_strip_all(girl, delay=0.4):
        """Strip all clothing slots with pauses. Reusable."""
        print("[DRESSING_STRIP] girl=%s clothes_before=%s" % (girl.gid, dict(girl.clothes)))
        for _slot in ("over", "mid", "skirt", "chest", "panties"):
            _item = girl.clothes.get(_slot)
            if _item:
                print("[DRESSING_STRIP] stripping %s=%s" % (_slot, _item))
                cloth_strip(girl, _slot)
                renpy.pause(delay)
            else:
                print("[DRESSING_STRIP] skip %s (empty: %r)" % (_slot, _item))
        print("[DRESSING_STRIP] clothes_after=%s" % dict(girl.clothes))

    def _dressing_dress_outfit(girl, outfit, delay=0.4):
        """Dress girl in an outfit dict {slot: item_code}. Reusable."""
        for _slot in ("panties", "chest", "mid", "skirt", "over"):
            _item = outfit.get(_slot)
            if _item:
                cloth_dress(girl, _slot, _item)
                renpy.pause(delay)

    def _bikini_item_ids(girl):
        """HER closet's bikini item ids (chest, bottom), read from the clothing registry: Tenny owns the
        blue set, Shion's bottom is "bikini_bottom". Never a gid check: the registry decides."""
        _reg = CLOTHING_REGISTRY.get(girl.gid, {})
        _top = next((_i for _i in ("bikini_top", "blue_bikini_top") if _i in _reg), "bikini_top")
        _bot = next((_i for _i in ("bikini_panties", "bikini_bottom", "blue_bikini_bottom") if _i in _reg), "bikini_panties")
        return _top, _bot

    def _dressing_dress_bikini(girl, delay=0.4):
        """Dress girl in bikini. Reusable."""
        _bk_top, _bk_pan = _bikini_item_ids(girl)
        cloth_dress(girl, "panties", _bk_pan)
        renpy.pause(delay)
        cloth_dress(girl, "chest", _bk_top)
        renpy.pause(delay)

    # ── Dressing room dialogue pools (trait-keyed) ──
    _BK_DRESSING_LINES = {
        "invite": {
            "exhibitionist": [
                _("Come in! I don't care if anyone sees."),
                _("Get in here! I love being watched."),
            ],
            "bf": [
                _("Quick, come in... but keep quiet. If %s finds out..."),
            ],
            "shy": [
                _("Come in... just don't stare too much, ok?"),
            ],
            "public_fetish": [
                _("Come in... I kinda like the idea of someone watching."),
            ],
            "default": [
                _("Come in here with me, quick. Nobody's looking."),
            ],
        },
        "wait": {
            "bf": [
                _("I'll go change. Stay right there, what if %s shows up?"),
            ],
            "shy": [
                _("I'm going to change... please don't peek!"),
            ],
            "default": [
                _("Ok, I'll go change. Wait here!"),
            ],
        },
        "refuse": {
            "bf": [
                _("Are you crazy?! What if %s comes in here?!"),
            ],
            "shy": [
                _("No! I can't have you watching me change!"),
            ],
            "default": [
                _("What?! No! Stay here!"),
            ],
        },
        "yield": {
            "bf": [
                _("Fine... but if %s finds out, it's your fault."),
            ],
            "shy": [
                _("I... ok... just don't stare too much..."),
            ],
            "default": [
                _("Oh... Fine then..."),
            ],
        },
    }

    def _bk_pick_line(girl, category):
        pool = _BK_DRESSING_LINES[category]
        if "exhibitionist" in girl.traits and "exhibitionist" in pool:
            lines = pool["exhibitionist"]
        elif girl.has_npc_partner() and "bf" in pool:
            lines = pool["bf"]
        elif "public_shy" in girl.traits and "shy" in pool:
            lines = pool["shy"]
        elif "public_fetish" in girl.traits and "public_fetish" in pool:
            lines = pool["public_fetish"]
        else:
            lines = pool["default"]
        line = _(renpy.random.choice(lines))
        if girl.has_npc_partner() and "%s" in line:
            line = _tl(line) % girl.partner_label()      # translated BEFORE the label goes in (else the lookup misses)
        return line

    def _bk_calc_dressing_scenario(girl):
        _saw_body = (girl.HasSeen("player_saw_pussy") and girl.HasSeen("player_saw_boobs"))
        # acts only: positions are preferences, a cowgirl scene would count twice
        _total = sum(_v for _k, _v in girl.Sex_acts.items() if _k not in _SEX_POSITION_KEYS)
        _loi = girl.Love + girl.Obed + girl.Inbt
        _has_bf = girl.has_npc_partner()
        _is_shy = "public_shy" in girl.traits
        _is_pf = "public_fetish" in girl.traits

        # Exhibitionist always invites
        if "exhibitionist" in girl.traits:
            return "invite"

        # Invite check (requires saw_body, uses combined LOI). Act counts: SEX_HISTORY_THRESHOLDS
        _inv_acts = SEX_HISTORY_THRESHOLDS["dressing_invite_acts"]
        if _saw_body:
            if _is_pf and _has_bf:
                if _loi >= 600 or _total >= _inv_acts["pf_bf"]:
                    return "invite"
            elif _is_pf:
                if _loi >= 500 or _total >= _inv_acts["pf"]:
                    return "invite"
            elif _is_shy and _has_bf:
                if _loi >= 1100 and _total >= _inv_acts["shy_bf"]:
                    return "invite"
            elif _has_bf:
                if _loi >= 800 or _total >= _inv_acts["bf"]:
                    return "invite"
            elif _is_shy:
                if _loi >= 900 and _total >= _inv_acts["shy"]:
                    return "invite"
            else:
                if _loi >= 650 or _total >= _inv_acts["default"]:
                    return "invite"

        # Obed force check
        if _is_shy and _has_bf:
            _obed_t = 850
        elif _has_bf:
            _obed_t = 750
        elif _is_shy:
            _obed_t = 800
        else:
            _obed_t = 600

        if girl.Obed >= _obed_t:
            return "obed"

        return "wait"

    def _bk_detect_companions(target, girls_here):
        companions = []
        blockers = []
        print("[BIKINI_COMP] target=%s, girls_here=%s" % (target.gid, [g.gid for g in girls_here]))
        for g in girls_here:
            if g.gid == target.gid:
                print("[BIKINI_COMP]   skip %s (is target)" % g.gid)
                continue
            _dating = g.is_dating_player()
            _harem = is_harem_exempt(g, target)
            _poly = g.has_trait("polyamorous")
            _ps = getattr(g, "Player_status", "none")
            _ha = getattr(g, "harem_accepted", set()) or set()
            print("[BIKINI_COMP]   %s: dating=%s(status=%s) harem_exempt=%s(accepted=%s) poly=%s" % (g.gid, _dating, _ps, _harem, _ha, _poly))
            if _dating and not (_harem or _poly):
                blockers.append(("gf", g))
                print("[BIKINI_COMP]   → BLOCKER (gf)")
            else:
                companions.append(("girl", g))
                print("[BIKINI_COMP]   → companion")
        if target.has_npc_partner():
            _npc = get_npc_partner_for(target)
            if _npc and getattr(_npc, "loc", "") == "mall":
                if not getattr(target, "_ntr_boundary_discovered", False):
                    blockers.append(("npc", _npc))
                elif getattr(_npc, "_ntr_boundary_level", 1) >= 2:
                    companions.append(("npc", _npc))
                else:
                    blockers.append(("npc", _npc))
        return companions, blockers

    def _bk_will_volunteer(comp_type, obj):
        if comp_type == "npc":
            return True
        g = obj
        if g.has_trait("exhibitionist") or g.has_trait("voyeur"):
            return renpy.random.random() < 0.8
        if g.has_trait("public_fetish"):
            return renpy.random.random() < 0.7
        if getattr(g, "Lust", 0) >= 50:
            return renpy.random.random() < 0.6
        if g.has_trait("public_shy"):
            return renpy.random.random() < 0.1
        return renpy.random.random() < 0.3

label bikini_store:
    $ store.bk_in_store = True
    $ store.bk_current_bg = "bg bikini_shop"
    $ debug_log("[BIKINI_ENTRY] bk_in_store SET to True. bk_current_bg=bg bikini_shop")
    scene bg bikini_shop with dissolve
    python:
        store._npc_on_scene = None
        _bikini_clerk = Character(_("Attendant"), color="#f472b6")
        _bikini_girls_here = [g for g in Party if g.loc == "mall"]
        _bk_entry_slots = [slot_right, slot_center, slot_left]
        for _bk_i, _bk_g in enumerate(_bikini_girls_here[:3]):
            set_girl_sprite(_bk_g.gid, pose="standing", at_list=[_bk_entry_slots[_bk_i]])

    $ _bikini_clerk(_("Welcome! Looking for something special?"))

    if _bikini_girls_here:
        call _bikini_store_accompanied(_bikini_girls_here) from _call_bikini_store_accompanied
    else:
        call _bikini_store_solo from _call_bikini_store_solo

    $ store.bk_in_store = False
    call Set_Scene(entry=True) from _call_Set_Scene_bikini_back
    return

# ─── SOLO PATH: buy as gift (simple purchase) ───
label _bikini_store_solo:
    $ store.bk_in_store = True
    while True:
        python:
            _bk_girl_menu = []
            for _bg in ALL_GIRLS:
                if _bg.gid not in BIKINI_STORE_ITEMS:
                    continue
                if not girl_route_enabled(_bg):
                    # her optional route is off: she does not exist in this run (no gift row)
                    continue
                if _bikini_girl_all_bought(_bg.gid):
                    _bk_girl_menu.append(("!disabled!" + _tl(_("Gift for %s... (All purchased)")) % _bg.Name, None))
                else:
                    _bk_girl_menu.append((_tl(_("Gift for %s...")) % _bg.Name, _bg.gid))
            _bk_girl_menu.append((_tl(_("Leave")), "leave"))
            _bk_pick = renpy.display_menu(_bk_girl_menu)

        if _bk_pick == "leave" or _bk_pick is None:
            return
        else:
            call _bikini_store_solo_items(_bk_pick) from _call_bikini_store_solo_items
    return

label _bikini_store_solo_items(gid):
    while True:
        python:
            _bk_items_menu = []
            for _bit in BIKINI_STORE_ITEMS.get(gid, []):
                _bit_bought = _is_unique_gift_purchased(_bit["id"])
                _bit_label = _tr(_bit["label"])
                if _bit_bought:
                    _bk_items_menu.append(("!disabled!" + _tl(_("%s (Purchased)")) % _bit_label, None))
                elif Player.cash < _bit["price"]:
                    _bk_items_menu.append(("!disabled!" + "%s... $%d" % (_bit_label, _bit["price"]), None))
                else:
                    _bk_items_menu.append(("%s... $%d" % (_bit_label, _bit["price"]), _bit["id"]))
            _bk_items_menu.append((_("Back"), "back"))
            _bk_item_pick = renpy.display_menu(_bk_items_menu)

        if _bk_item_pick == "back" or _bk_item_pick is None:
            return
        else:
            call _bikini_store_buy_solo(_bk_item_pick) from _call_bikini_store_buy_solo
    return

label _bikini_store_buy_solo(item_id):
    python:
        _bk_item = None
        for _gid_key, _items_list in BIKINI_STORE_ITEMS.items():
            for _it in _items_list:
                if _it["id"] == item_id:
                    _bk_item = _it
                    break
            if _bk_item:
                break
        _bk_price = _bk_item["price"]
        _bk_label = _bk_item["label"]
    if Player.cash < _bk_price:
        $ Say_Player(_("(I don't have enough money for that...)"))
        return
    $ Player.spend_cash(_bk_price)
    $ Player.add_item(item_id, 1)
    python:
        if not hasattr(store.Player, "_unique_gifts_purchased"):
            store.Player._unique_gifts_purchased = set()
        store.Player._unique_gifts_purchased.add(item_id)
    $ _pharmacy_popup(_bk_label, 1, _bk_price)
    $ Say_Player(_("(Nice. I'll give this to her later.)"))
    return

# ─── ACCOMPANIED PATH: dressing room experience ───
label _bikini_store_accompanied(girls_here):
    $ store.bk_in_store = True
    while True:
        python:
            _bk_girl_menu = []
            for _bg in girls_here:
                if _bg.gid not in BIKINI_STORE_ITEMS:
                    continue
                if _bikini_girl_all_bought(_bg.gid):
                    _bk_girl_menu.append(("!disabled!" + _tl(_("Gift for %s... (All purchased)")) % _bg.Name, None))
                else:
                    _bk_girl_menu.append((_tl(_("Gift for %s...")) % _bg.Name, _bg.gid))
            _bk_girl_menu.append((_tl(_("Leave")), "leave"))
            _bk_pick = renpy.display_menu(_bk_girl_menu)

        if _bk_pick == "leave" or _bk_pick is None:
            return
        else:
            $ _bk_girl = GIRL_BY_ID[_bk_pick]

            python:
                store.bk_companions_raw, _bk_blockers = _bk_detect_companions(_bk_girl, girls_here)
                store.bk_companions = []

            $ print("[BIKINI_FLOW] blockers=%d companions=%d" % (len(_bk_blockers), len(store.bk_companions_raw)))
            if _bk_blockers:
                python:
                    _bl_type, _bl_obj = _bk_blockers[0]
                    print("[BIKINI_FLOW] blocker type=%s obj=%s" % (_bl_type, getattr(_bl_obj, 'gid', getattr(_bl_obj, 'name', '?'))))
                if _bl_type == "gf":
                    $ set_scene_expression(_bl_obj, "angry")
                    $ Say_Line(_bl_obj, _("You're going to buy HER a bikini? Right in front of me?"))
                    $ set_scene_expression(_bl_obj, "normal")
                elif _bl_type == "npc":
                    python:
                        _bl_npc_char = Character(_bl_obj.name)
                    $ _bl_npc_char(_("Hey... what are you doing buying my girlfriend a bikini?"))
            else:
                call _bikini_store_acc_items(_bk_girl) from _call_bikini_store_acc_items
                if _bk_girl.has_temp_status("angry"):
                    return
    return

label _bikini_store_acc_items(girl):
    $ store.bk_in_store = True
    while True:
        python:
            _bk_items_menu = []
            for _bit in BIKINI_STORE_ITEMS.get(girl.gid, []):
                _bit_bought = _is_unique_gift_purchased(_bit["id"])
                _bit_label = _tr(_bit["label"])
                if _bit_bought:
                    _bk_items_menu.append(("!disabled!" + _tl(_("%s (Purchased)")) % _bit_label, None))
                elif Player.cash < _bit["price"]:
                    _bk_items_menu.append(("!disabled!" + "%s... $%d" % (_bit_label, _bit["price"]), None))
                else:
                    _bk_items_menu.append(("%s... $%d" % (_bit_label, _bit["price"]), _bit["id"]))
            _bk_items_menu.append((_("Back"), "back"))
            _bk_item_pick = renpy.display_menu(_bk_items_menu)

        if _bk_item_pick == "back" or _bk_item_pick is None:
            return
        else:
            call _bikini_store_try_on(girl, _bk_item_pick) from _call_bikini_store_try_on
            if girl.has_temp_status("angry"):
                return
    return

# Stat check → dressing room scene
label _bikini_store_try_on(girl, item_id):
    $ store.bk_in_store = True
    # Combined stat check: Love + Obed + Inbt must reach threshold
    if girl.Love + girl.Obed + girl.Inbt < 300:
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _("No thanks... I don't want you buying me something like that."))
        $ set_scene_expression(girl, "normal")
        return

    # She accepts — find the item data
    python:
        _bk_item = None
        for _it in BIKINI_STORE_ITEMS.get(girl.gid, []):
            if _it["id"] == item_id:
                _bk_item = _it
                break
        _bk_price = _bk_item["price"]

    $ set_scene_expression(girl, "happy")
    $ Say_Line(girl, _("Oh, really? You want to get that for me? Sure, let me try it on!"))

    # Companion invite/volunteer phase
    python:
        if not hasattr(store, "bk_companions"):
            store.bk_companions = []
        store.bk_companions_accepted = []

    if getattr(store, "bk_companions_raw", []):
        python:
            store.bk_invite_list = list(store.bk_companions_raw)
            store.bk_invite_idx = 0

        while store.bk_invite_idx < len(store.bk_invite_list):
            python:
                _ct, _co = store.bk_invite_list[store.bk_invite_idx]
                store.bk_invite_idx += 1
            if _ct == "npc":
                python:
                    _bk_comp_char = Character(_co.name)
                $ _bk_comp_char(_("I'd like to see her try it on... can I come along?"))
                python:
                    _bk_invite_pick = renpy.display_menu([
                        (_("Let him come"), "yes"),
                        (_("No, wait here"), "no"),
                    ])
                if _bk_invite_pick == "yes":
                    $ store.bk_companions_accepted.append(("npc", _co))
                    $ print("[BIKINI] NPC %s accepted as companion" % _co.name)
            else:
                python:
                    _bk_invite_pick = renpy.display_menu([
                        (_tl(_("Invite %s to come along")) % _co.Name, "invite"),
                        (_("Don't invite her"), "skip"),
                    ])
                if _bk_invite_pick == "invite":
                    $ store.bk_companions_accepted.append(("girl", _co))
                    $ set_scene_expression(_co, "happy")
                    $ Say_Line(_co, _("Sure, I'll come watch!"))
                else:
                    if _bk_will_volunteer("girl", _co):
                        $ set_scene_expression(_co, "smirk")
                        $ Say_Line(_co, _("Hey, can I come too? I want to see!"))
                        python:
                            _bk_vol_pick = renpy.display_menu([
                                (_("Sure, come along"), "yes"),
                                (_("No, stay here"), "no"),
                            ])
                        if _bk_vol_pick == "yes":
                            $ store.bk_companions_accepted.append(("girl", _co))
                        else:
                            $ set_scene_expression(_co, "sad")
                            $ Say_Line(_co, _("Fine..."))
                            $ set_scene_expression(_co, "normal")

    $ print("[BIKINI] Companions accepted: %d" % len(store.bk_companions_accepted))

    # Go to dressing room area
    $ store.bk_current_bg = "bg dressing_room_outside"
    scene bg dressing_room_outside with dissolve
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])

    # Position accepted companions
    if getattr(store, "bk_companions_accepted", []):
        python:
            _bk_comp_slots = [slot_right, slot_left]
            for _ci, (_ct2, _co2) in enumerate(store.bk_companions_accepted):
                if _ct2 == "girl" and _ci < len(_bk_comp_slots):
                    set_girl_sprite(_co2.gid, pose="standing", at_list=[_bk_comp_slots[_ci]])

    # Determine scenario via trait-aware logic
    $ _bk_scenario = _bk_calc_dressing_scenario(girl)

    if _bk_scenario == "invite":
        call _bikini_dressing_invite(girl) from _call_bikini_dressing_invite
    elif _bk_scenario == "obed":
        call _bikini_dressing_obed(girl) from _call_bikini_dressing_obed
    else:
        call _bikini_dressing_wait(girl) from _call_bikini_dressing_wait

    # Achievement: entered dressing room with her
    if store.bk_was_inside_dressing:
        $ unlock_achievement("fashion_stylist")

    # Opinion menu (restores clothes internally)
    call _bikini_store_opinion(girl) from _call_bikini_store_opinion

    if girl.has_temp_status("angry"):
        return

    # Post-sex suspicion: companions who stayed outside ask why it took so long
    if getattr(store, "bk_had_sex", False):
        python:
            _bk_outside_comps = [c for c in getattr(store, "bk_companions_raw", []) if c not in getattr(store, "bk_companions_accepted", [])]
        if _bk_outside_comps:
            $ store.bk_current_bg = "bg dressing_room_outside"
            scene bg dressing_room_outside with dissolve
            $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])
            python:
                store.bk_susp_idx = 0
            while store.bk_susp_idx < len(_bk_outside_comps):
                python:
                    _oc_type, _oc_obj = _bk_outside_comps[store.bk_susp_idx]
                    store.bk_susp_idx += 1
                if _oc_type == "girl":
                    $ set_girl_sprite(_oc_obj.gid, pose="standing", at_list=[slot_right])
                    $ set_scene_expression(_oc_obj, "sly")
                    $ Say_Line(_oc_obj, _("What took you two so long in there?"))
                    $ set_scene_expression(girl, "shy")
                    $ Say_Line(girl, _("Nothing! I was just... trying things on."))
                    $ set_scene_expression(_oc_obj, "smug")
                    $ Say_Line(_oc_obj, _("Uh-huh. Sure you were."))
                    $ set_scene_expression(_oc_obj, "normal")
                    $ hide_girl_sprite(_oc_obj)
                elif _oc_type == "npc":
                    python:
                        _oc_npc_char = Character(_oc_obj.name)
                    $ _oc_npc_char(_("You guys were in there for a while..."))
                    $ set_scene_expression(girl, "shy")
                    $ Say_Line(girl, _("Sorry, it took a while to find the right fit."))

    # Back to shop — reposition ALL girls that are here
    $ store.bk_current_bg = "bg bikini_shop"
    scene bg bikini_shop with dissolve
    python:
        _bk_back_slots = [slot_right, slot_center, slot_left]
        for _bk_bi, _bk_bg in enumerate(store._bikini_girls_here[:3]):
            set_girl_sprite(_bk_bg.gid, pose="standing", at_list=[_bk_back_slots[_bk_bi]])
            set_scene_expression(_bk_bg, "normal")

    # Purchase decision
    call _bikini_store_purchase(girl, item_id, _bk_price) from _call_bikini_store_purchase
    return

# ─── Scenario 3: She invites player inside ───
label _bikini_dressing_invite(girl):
    $ store.bk_was_inside_dressing = True
    python:
        _bk_line = _bk_pick_line(girl, "invite")
        _bk_expr = "smug" if "exhibitionist" in girl.traits or "public_fetish" in girl.traits else "shy"
    $ set_scene_expression(girl, _bk_expr)
    $ Say_Line(girl, _bk_line)

    $ store.bk_current_bg = "bg dressing_room"
    scene bg dressing_room with dissolve
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])

    # Reposition companions inside
    if getattr(store, "bk_companions_accepted", []):
        python:
            _bk_inside_slots = [slot_right, slot_left]
            for _ci3, (_ct3, _co3) in enumerate(store.bk_companions_accepted):
                if _ct3 == "girl" and _ci3 < len(_bk_inside_slots):
                    set_girl_sprite(_co3.gid, pose="standing", at_list=[_bk_inside_slots[_ci3]])
                    set_scene_expression(_co3, "smirk")

    python:
        store.bk_saved_clothes = dict(girl.clothes)

    $ set_scene_expression(girl, "shy")
    $ print("[BIKINI_TRYON] about to strip girl=%s id=%s clothes=%s" % (girl.Name, id(girl), dict(girl.clothes)))
    $ _dressing_strip_all(girl)
    $ print("[BIKINI_TRYON] after strip, before dress: clothes=%s" % dict(girl.clothes))
    $ _dressing_dress_bikini(girl)
    $ print("[BIKINI_TRYON] after dress: clothes=%s" % dict(girl.clothes))

    # Companion reaction to seeing her in bikini
    if getattr(store, "bk_companions_accepted", []):
        python:
            store.bk_react_idx = 0
        while store.bk_react_idx < len(store.bk_companions_accepted):
            python:
                _ct4, _co4 = store.bk_companions_accepted[store.bk_react_idx]
                store.bk_react_idx += 1
            if _ct4 == "girl":
                $ set_scene_expression(_co4, "happy")
                $ Say_Line(_co4, _("Wow, that looks amazing on you!"))
            elif _ct4 == "npc":
                python:
                    _bk_npc_react = Character(_co4.name)
                $ _bk_npc_react(_("Wow... you look great."))

    $ set_scene_expression(girl, "smug")
    $ Say_Line(girl, _("So... what do you think?"))
    return

# ─── Scenario 2: She says wait, player can insist (fails) ───
label _bikini_dressing_wait(girl):
    python:
        _bk_line = _bk_pick_line(girl, "wait")
    $ set_scene_expression(girl, "normal")
    $ Say_Line(girl, _bk_line)

    python:
        store.bk_saved_clothes = dict(girl.clothes)
        _bk_wait_menu = [
            (_("Wait for her"), "wait"),
            (_("No way, I want to see everything!"), "insist"),
        ]
        _bk_wait_pick = renpy.display_menu(_bk_wait_menu)

    if _bk_wait_pick == "insist":
        python:
            _bk_refuse = _bk_pick_line(girl, "refuse")
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _bk_refuse)
        $ Change_Status(girl, "Love", -10)
        $ Change_Status(girl, "Obed", -5)
    else:
        $ Change_Status(girl, "Love", 5)

    # Either way: she goes alone (outside dressing)
    $ store.bk_was_inside_dressing = False
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[slide_out_right])
    $ renpy.pause(0.5)
    $ renpy.hide(girl.Id)

    $ Narration(_("You wait a few minutes..."))

    python:
        _bk_chest, _bk_pan = _bikini_item_ids(girl)
        girl.clothes = {"over": None, "mid": None, "chest": _bk_chest, "skirt": None, "panties": _bk_pan, "shoes": None}
        girl.clothes_state = {"over": "full", "mid": "full", "chest": "full", "skirt": "full", "panties": "full", "shoes": "full"}
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[slide_in_right])
    $ renpy.pause(0.5)
    $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])
    $ set_scene_expression(girl, "shy")
    $ Say_Line(girl, _("So... what do you think?"))
    return

# ─── Obed sub-scenario: she says wait, player can force entry ───
label _bikini_dressing_obed(girl):
    python:
        _bk_line = _bk_pick_line(girl, "wait")
    $ set_scene_expression(girl, "normal")
    $ Say_Line(girl, _bk_line)

    python:
        store.bk_saved_clothes = dict(girl.clothes)
        _bk_obed_menu = [
            (_("Wait for her"), "wait"),
            (_("No way, I want to see everything!"), "force"),
        ]
        _bk_obed_pick = renpy.display_menu(_bk_obed_menu)

    if _bk_obed_pick == "force":
        python:
            _bk_yield = _bk_pick_line(girl, "yield")
        $ set_scene_expression(girl, "shy")
        $ Say_Line(girl, _bk_yield)
        $ Change_Status(girl, "Obed", 10)

        # Player enters with her
        $ store.bk_was_inside_dressing = True
        $ store.bk_current_bg = "bg dressing_room"
        scene bg dressing_room with dissolve
        $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])

        # Reposition companions inside
        if getattr(store, "bk_companions_accepted", []):
            python:
                _bk_inside_slots2 = [slot_right, slot_left]
                for _ci5, (_ct5, _co5) in enumerate(store.bk_companions_accepted):
                    if _ct5 == "girl" and _ci5 < len(_bk_inside_slots2):
                        set_girl_sprite(_co5.gid, pose="standing", at_list=[_bk_inside_slots2[_ci5]])
                        set_scene_expression(_co5, "surprised")

        $ set_scene_expression(girl, "shy")
        $ _dressing_strip_all(girl)
        $ _dressing_dress_bikini(girl)

        $ set_scene_expression(girl, "shy")
        $ Say_Line(girl, _("So... what do you think?"))
    else:
        # Player waits outside
        $ Change_Status(girl, "Love", 5)
        $ store.bk_was_inside_dressing = False

        $ set_girl_sprite(girl.gid, pose="standing", at_list=[slide_out_right])
        $ renpy.pause(0.5)
        $ renpy.hide(girl.Id)

        $ Narration(_("You wait a few minutes..."))

        python:
            _bk_chest, _bk_pan = _bikini_item_ids(girl)
            girl.clothes = {"over": None, "mid": None, "chest": _bk_chest, "skirt": None, "panties": _bk_pan, "shoes": None}
            girl.clothes_state = {"over": "full", "mid": "full", "chest": "full", "skirt": "full", "panties": "full", "shoes": "full"}
        $ set_girl_sprite(girl.gid, pose="standing", at_list=[slide_in_right])
        $ renpy.pause(0.5)
        $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])
        $ set_scene_expression(girl, "shy")
        $ Say_Line(girl, _("So... what do you think?"))
    return

# ─── Opinion menu (shared by inside/outside paths) ───
label _bikini_store_opinion(girl):
    $ store.bk_in_store = True
    python:
        _bk_opinion_menu = [
            (_("It looks great on you!"), "good"),
            (_("I think we should get an even smaller one..."), "smaller"),
            (_("I think we should try another one."), "another"),
        ]
        _bk_opinion = renpy.display_menu(_bk_opinion_menu)

    if _bk_opinion == "good":
        $ set_scene_expression(girl, "happy")
        $ Say_Line(girl, _("Really? Thank you! I love it!"))
        $ Change_Status(girl, "Love", 10)
    elif _bk_opinion == "smaller":
        $ set_scene_expression(girl, "shy")
        $ Say_Line(girl, _("Smaller?! You're so bold..."))
        $ Change_Status(girl, "Obed", 5)
        $ Change_Status(girl, "Inbt", 5)
        $ Say_Line(girl, _("They don't have another one in my size, though."))
    elif _bk_opinion == "another":
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _("Another one? But I liked this one..."))
        $ Change_Status(girl, "Love", -5)
        $ Change_Status(girl, "Obed", 5)
        $ Say_Line(girl, _("They don't have anything else in my size anyway."))

    # After opinion: offer to have fun (only when inside dressing room)
    if store.bk_was_inside_dressing:
        python:
            _bk_fun_menu = [
                (_("Have some fun"), "fun"),
                (_("Let's go"), "leave"),
            ]
            _bk_fun_pick = renpy.display_menu(_bk_fun_menu)
        if _bk_fun_pick == "fun":
            $ unlock_achievement("fitting_fun")
            $ _bk_saved_loc = store.CurrentLocation
            $ store.CurrentLocation = "dressing_room"

            # Set up companion flags for sex scene
            python:
                store.bk_had_sex = True
                _bk_girl_comps = [c for c in getattr(store, "bk_companions_accepted", []) if c[0] == "girl"]
                _bk_npc_comps = [c for c in getattr(store, "bk_companions_accepted", []) if c[0] == "npc"]

                if _bk_girl_comps:
                    store.bk_auto_witness = _bk_girl_comps[0][1]
                    debug_log("[BIKINI] Auto-witness set: %s" % store.bk_auto_witness.gid)
                else:
                    store.bk_auto_witness = None

                if _bk_npc_comps:
                    store._ntr_partner_watching = True
                    store._ntr_watching_npc = _bk_npc_comps[0][1]
                    debug_log("[BIKINI] NTR watching set: %s" % store._ntr_watching_npc.name)

            call sex_menu(girl, "dressing_room", store.TimeIndex) from _call_sex_menu_bikini
            $ store.CurrentLocation = _bk_saved_loc
            $ store.bk_auto_witness = None
            if girl.has_temp_status("angry"):
                $ store.bk_in_store = False
                scene bg mall with dissolve
                $ store.CurrentLocation = "mall"
                return
            $ store.bk_current_bg = "bg dressing_room"
            scene bg dressing_room with dissolve
            $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])
            python:
                _bk_girl_comps_post = [c[1] for c in getattr(store, "bk_companions_accepted", []) if c[0] == "girl" and c[1] is not girl]
                for _bk_comp in _bk_girl_comps_post:
                    set_girl_sprite(_bk_comp.gid, pose="standing", at_list=[slot_right])
        else:
            $ store.bk_had_sex = False
    else:
        $ store.bk_had_sex = False

    # She changes back — inside dressing room: visual dress-up; outside: slide out/in
    $ _bk_saved = store.bk_saved_clothes

    if store.bk_was_inside_dressing:
        $ _dressing_strip_all(girl)
        $ _dressing_dress_outfit(girl, _bk_saved)
        $ set_scene_expression(girl, "normal")
    else:
        $ set_girl_sprite(girl.gid, pose="standing", at_list=[slide_out_right])
        $ renpy.pause(0.5)
        $ renpy.hide(girl.Id)
        $ Narration(_("..."))
        python:
            for _slot, _item in _bk_saved.items():
                girl.clothes[_slot] = _item
                girl.clothes_state[_slot] = "full"
        $ set_girl_sprite(girl.gid, pose="standing", at_list=[slide_in_right])
        $ renpy.pause(0.5)
        $ set_girl_sprite(girl.gid, pose="standing", at_list=[slot_center])
        $ set_scene_expression(girl, "normal")
        $ Say_Line(girl, _("Done. Shall we go?"))
    return

# ─── Final purchase decision (back in shop) ───
label _bikini_store_purchase(girl, item_id, price):
    python:
        _bk_buy_menu = [
            ("%s - $%d" % (_tl(_("Buy it for her")), price), "buy"),
            (_("Actually, never mind."), "skip"),
        ]
        _bk_decision = renpy.display_menu(_bk_buy_menu)

    if _bk_decision == "buy":
        if Player.cash < price:
            $ Say_Player(_("(I don't have enough money for that...)"))
            return
        $ Player.spend_cash(price)
        python:
            if not hasattr(store.Player, "_unique_gifts_purchased"):
                store.Player._unique_gifts_purchased = set()
            store.Player._unique_gifts_purchased.add(item_id)
            _bk_label = ""
            for _it in BIKINI_STORE_ITEMS.get(girl.gid, []):
                if _it["id"] == item_id:
                    _bk_label = _it["label"]
                    break
            girl._bikini_unlocked = True
            _effects = GIFT_EFFECTS.get(item_id, {})
            _gift_mult = get_gift_multiplier(girl, item_id)
            for _stat, _amt in _effects.items():
                Change_Status(girl, _stat, int(_amt * _gift_mult))
            _erode_bf_loyalty(girl, "gift", item_id)
            girl._total_gifts_value = getattr(girl, "_total_gifts_value", 0) + GIFT_PRICES.get(item_id, 0)
            _update_financial_attitude(girl)
            girl.RegisterAction("gift_given")
        $ _pharmacy_popup(_bk_label, 1, price)
        $ set_scene_expression(girl, "happy")
        $ Say_Line(girl, _("Thank you so much! I'll wear it just for you."))
    else:
        $ set_scene_expression(girl, "sad")
        $ Say_Line(girl, _("Oh... okay then."))
        $ Change_Status(girl, "Love", -5)
        $ Change_Status(girl, "Obed", 3)
    return

# ------------------------------------------------------------
# Drinks section
# ------------------------------------------------------------
label shop_drinks:

    $ _own_drinks = Player.get_item_count("drinks")
    $ Narration(_("Drinks for a night in. You have [_own_drinks] bottle(s). Balance: $[Player.cash]."))

    menu:

        "Bottle of Drinks... $40" if Player.cash >= 40:
            $ Player.spend_cash(40)
            $ Player.add_item("drinks", 1)
            $ Narration(_("Ordered. 1 bottle on the way. Balance: $[Player.cash]."))
            return

        "!disabled!Bottle of Drinks... $40  (Need $[40 - Player.cash] more)" if Player.cash < 40:
            return

        "Back":
            return

# ------------------------------------------------------------
# Gifts section
# ------------------------------------------------------------
label shop_gifts:

    $ Narration(_("Gifts. Perfect for making a good impression. Balance: $[Player.cash]."))

    python:
        _gift_items = SHOP_CATALOG["gifts"]["items"]
        _gift_choices = []
        for _gi in _gift_items:
            _owned = Player.get_item_count(_gi["id"])
            _lbl = "%s - $%d" % (_tl(_gi["label"]), _gi["price"])
            if _owned > 0:
                _lbl += "  (%s: %d)" % (_tl(_("own")), _owned)
            if Player.cash >= _gi["price"]:
                _gift_choices.append((_lbl, _gi))
            else:
                _gift_choices.append(("!disabled!" + _lbl, None))
        # None-valued items render as unclickable captions, so Back needs a real sentinel
        _gift_choices.append((_("Back"), "__back__"))
        _picked = renpy.display_menu(_gift_choices)
        if _picked == "__back__":
            _picked = None

    if _picked is not None:
        python:
            Player.spend_cash(_picked["price"])
            Player.add_item(_picked["id"], _picked["qty"])
            Narration(_tl(_("Ordered. %s on the way. Balance: $%d.")) % (_tl(_picked["label"]), Player.cash))

    return

# ------------------------------------------------------------
# Girl-specific gifts (piercings, accessories)
# ------------------------------------------------------------
label shop_girl_gifts(catalog_key):

    python:
        _cat = SHOP_CATALOG.get(catalog_key, {})
        _items = _cat.get("items", [])
        _cat_label = _tl(_cat.get("label", _("Special Gifts")))

    $ Narration(_("[_cat_label]. Balance: $[Player.cash]."))

    python:
        _choices = []
        for _gi in _items:
            _item_id = _gi["id"]
            _owned = Player.get_item_count(_item_id)
            _lbl = "%s - $%d" % (_tl(_gi["label"]), _gi["price"])

            # Check if piercing already applied or pending
            _already_applied = False
            if _item_id.startswith("piercing_"):
                _p_gid = _item_id.replace("piercing_", "")
                _p_girl = GIRL_BY_ID.get(_p_gid)
                if _p_girl and (getattr(_p_girl, "Piercing", False) or getattr(_p_girl, "_piercing_pending", False)):
                    _already_applied = True
            elif _item_id.startswith("bikini_"):
                _b_gid = _item_id.replace("bikini_", "")
                _b_girl = GIRL_BY_ID.get(_b_gid)
                if _b_girl and getattr(_b_girl, "_bikini_unlocked", False):
                    _already_applied = True

            if _already_applied:
                _choices.append(("!disabled!" + _lbl + "  (%s)" % _tl(_("already wearing")), None))
            elif _owned > 0:
                _choices.append(("!disabled!" + _lbl + "  (%s)" % _tl(_("owned")), None))
            elif Player.cash >= _gi["price"]:
                _choices.append((_lbl, _gi))
            else:
                _choices.append(("!disabled!" + _lbl, None))
        # None-valued items render as unclickable captions, so Back needs a real sentinel
        _choices.append((_("Back"), "__back__"))
        _picked = renpy.display_menu(_choices)
        if _picked == "__back__":
            _picked = None

    if _picked is not None:
        python:
            Player.spend_cash(_picked["price"])
            Player.add_item(_picked["id"], _picked["qty"])
            Narration(_tl(_("Ordered. %s on the way. Balance: $%d.")) % (_tl(_picked["label"]), Player.cash))

    return

# ============================================================
# Sell Videos Online
# ============================================================
label sell_videos:

    python:
        _vids = getattr(store.Player, "recorded_videos", [])
        _unsold = [v for v in _vids if not v.get("sold", False)]

    if not _unsold:
        "You don't have any unsold videos."
        $ _phone_restore_others()
        return

    $ Narration(_("You open an anonymous upload site. Time to cash in. Balance: $[Player.cash]."))

    label .sell_loop:

    python:
        _vids = getattr(store.Player, "recorded_videos", [])
        _unsold = [v for v in _vids if not v.get("sold", False)]
        _sell_choices = []
        for _sv in _unsold:
            _lbl = video_sell_label(_sv)
            _sell_choices.append((_lbl, _sv))
        # None-valued items render as unclickable captions, so Back needs a real sentinel
        _sell_choices.append(("Back", "__back__"))
        _chosen_vid = renpy.display_menu(_sell_choices)
        if _chosen_vid == "__back__":
            _chosen_vid = None

    if _chosen_vid is None:
        $ _phone_restore_others()
        return

    python:
        _price = video_sell_price(_chosen_vid)
        _chosen_vid["sold"] = True
        Player.add_cash(_price)

    $ Narration(_("Video uploaded anonymously. You earned $[_price]. Balance: $[Player.cash]."))

    # Check if more unsold videos remain
    python:
        _remaining = sum(1 for v in store.Player.recorded_videos if not v.get("sold", False))

    if _remaining > 0:
        jump .sell_loop

    "No more unsold videos."
    $ _phone_restore_others()
    return
