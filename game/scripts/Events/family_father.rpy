# ============================================================
# family_father.rpy... the player's father on the map (the author, 2026-10-02). shion_family.rpy keeps his phone
# side (his texts, his business trips, the dinners); this file is the man in the apartment.
#
# HIS ROOMS: by weekday / slot (DAD_ROOM_SCHEDULE): the living room, the bedroom, the bathroom (never while a woman
#   of the house is in it: the living room instead), or "out" (away from the apartment, not seen). At work / on a
#   trip he is never home (dad_where). Asleep on the couch after the DAD_DRINKS_NAP-th drink of the day: off scene
#   for the rest of that slot. dad_room() = the room he is in, or None.
# SEEN: his sprite (FAMILY_SPRITES: his own art, NPCs/Man/Dad.png) in the roster of the room he is in (family_on_scene,
#   build_location_roster); "Chat..." lists him (do_talk -> label family_talk). NPC partners never get his sprite.
# TALK (family_talk): chat (his friendship, the first chat of the day), speak well / badly of his wife (his love for
#   her; once a day; when she is in the room she hears it: her love for him follows what he answers, her Love for the
#   player too), give him a drink from the inventory (friendship by the drink's tier; the 3rd of the day puts him to
#   sleep). Each costs a chat.
# STATS: his friendship with the player and his love for his wife (attributes of store.Dad, FAMILY_START), her love
#   for him (girl._love_for_husband, GIRLS_CONFIG "husband_love"). Shown in her card ("HUSBAND"); they pick his
#   lines (FAMILY_TIERS). Game effects (trips, suspicion) come later.
# IN THE ROOM WITH HIS WIFE: nothing of her ladder happens in front of him (husband_in_room, story_act_locked).
# THE FIRST VISIT: a girl of the apartment with "meets_at_home" stays home until he meets her (girl_pre_intro_loc,
#   get_scheduled_location_for; she refuses his invitations, _girl_accepts_invite "not_met"); his first arrival plays
#   her intro with his father in the living room (label _apartment_intro, FAMILY_INTROS).
# ============================================================

init python:

    # Each family member's own art (never a guest sprite: the guests are all free for NPC partners): member gid ->
    # (file, the file's height in pixels). Shown at the height of the guest sprites (NPC_SPRITE_HEIGHT), so the
    # roster slots place him like any NPC. Image "family_sprite_<gid>" (FamilyContact.image_name)
    FAMILY_SPRITES = {"dad": ("images/characters/NPCs/Man/Dad.png", 1376)}
    for _fs_gid, (_fs_file, _fs_height) in FAMILY_SPRITES.items():
        renpy.image("family_sprite_%s" % _fs_gid, Transform(_fs_file, zoom=float(NPC_SPRITE_HEIGHT) / _fs_height))
    FAMILY_START = {"friendship": 300, "love_for_wife": 700, "suspicion": 0}
    FAMILY_STAT_MAX = {"friendship": 1000, "love_for_wife": 1000, "suspicion": 100}
    WIFE_LOVE_START = 400               # her love for her husband when her config has no "husband_love"
    # Tiers of his lines: (minimum, tier), highest first
    FAMILY_TIERS = {
        "friendship": ((500, "high"), (200, "mid"), (0, "low")),
        "love_for_wife": ((700, "high"), (400, "mid"), (0, "low")),
    }

    # His rooms by weekday ((Day - 1) % 7, 0 = Sunday) and slot; "out" = away from the apartment (not seen)
    DAD_ROOM_SCHEDULE = (
        ("apartment_room",   "apartment", "apartment", "apartment_room"),   # Sunday (the dinner in the Evening)
        ("apartment_shower", "out",       "apartment", "apartment_room"),   # Monday
        ("apartment",        "out",       "apartment", "apartment_room"),   # Tuesday
        ("apartment_shower", "out",       "apartment", "apartment_room"),   # Wednesday
        ("apartment",        "out",       "out",       "apartment_room"),   # Thursday (drinks after work)
        ("apartment_shower", "out",       "out",       "apartment_room"),   # Friday (drinks after work)
        ("apartment_room",   "out",       "apartment", "apartment_room"),   # Saturday (golf at Midday)
    )
    DAD_PRIVATE_ROOMS = ("apartment_shower",)   # never in one while a woman of the house is in it

    DAD_CHAT_GAIN = 5                   # friendship, the first chat of the day
    DAD_DRINK_FRIENDSHIP = {"low": 5, "med": 10, "high": 15}
    DAD_DRINKS_NAP = 3                  # the drink of the day that puts him to sleep on the couch

    # ── "She decides for him": the wife overrules her husband in front of the player ──
    # Any of these stats of hers (toward the PLAYER) at its bar: she uses her weight in the house for him.
    # The story caps (story_stat_gain) keep this out of reach on her early steps without a step check here.
    # Used by the errand ask (family_talk) and the dessert run of the Sunday dinner (tester ideas, 2026-10-10).
    FAMILY_OVERRULE_STATS = {"Obed": 700, "Love": 700}

    def family_wife_overrules(girl):
        """She decides for her husband when the player asks for something her husband refused."""
        if girl is None:
            return False
        _hit = next((_s for _s, _v in FAMILY_OVERRULE_STATS.items() if getattr(girl, _s, 0) >= _v), None)
        if _hit:
            print("[FAMILY] %s overrules her husband (%s %d >= %d)" % (
                girl.gid, _hit, getattr(girl, _hit, 0), FAMILY_OVERRULE_STATS[_hit]))
        return _hit is not None

    def family_errand_out(member):
        """He steps out of the apartment for the rest of this time slot (the corner store): dad_room's _here
        override, (day, slot, None) = no room. It expires on its own when the slot turns and his schedule
        takes him back."""
        member._here = (store.Day, store.TimeIndex, None)
        print("[FAMILY] %s runs the errand: out for Day %d slot %d" % (member.gid, store.Day, store.TimeIndex))

    # His answers to the errand ask (label _family_errand). The player's legs are younger: only his wife moves him.
    FAMILY_ERRAND_ASK = _("Hey, could you run down to the corner store and grab us something?")
    FAMILY_ERRAND_REFUSE = [
        _("Ha! You have younger legs than mine, son. You go."),
        _("The couch and I have an agreement. Whatever it is, it can wait."),
        _("Me? Now? The game is on. Ask me at halftime... no, ask me tomorrow."),
    ]
    FAMILY_ERRAND_REFUSE_AGAIN = [
        _("Twice in one day? The store isn't going anywhere, son."),
        _("Again? What did you two do with the last batch?"),
    ]
    FAMILY_ERRAND_OBEY = [
        _("...Alright, alright. Anything for the lady of the house."),
        _("You heard her. Apparently I'm going to the store."),
    ]

    # The street-stand dessert at the Sunday dinner (_apartment_dinner_weekly): his no, and his return
    FAMILY_DESSERT_REFUSE = [
        _("The kitchen is full of dessert, son. Sit down."),
        _("Three blocks for sugar on a Sunday night? Not a chance."),
    ]
    FAMILY_DESSERT_RETURN = [
        _("The front door opens. Your father walks in with a paper box and the face of a man who waited in line."),
        _("Keys, footsteps, and your father appears holding a small paper box like a trophy."),
    ]

    # Departure hints when the father leaves the player's current room (time change at the apartment).
    # Keyed by his NEW room (dad_room() after the change), None = leaving the apartment entirely.
    DAD_DEPARTURE_LINES = {
        "apartment_room": [
            _("I think I'll go read something in the bedroom."),
            _("I'll be in the bedroom if you need anything, son."),
        ],
        "apartment": [
            _("I'll go sit in the living room for a while."),
            _("Let me go see what's on TV."),
        ],
        "apartment_shower": [
            _("Excuse me, I need the bathroom."),
        ],
        None: [
            _("I'm heading out for a while. Need anything from the store?"),
            _("I'll check the market, see if there's anything on sale."),
            _("I need to run a few errands. Back later."),
        ],
    }

    # His small talk: member gid -> friendship tier -> lines
    # His line about his wife's mood when she has a story (docs/plan_story_dynamism.md F4): her step in two bands,
    # read by _family_chat with a small chance. He suspects nothing; the irony IS the line. "%s" = her name
    FAMILY_WIFE_MOOD_LINES = {
        # steps 0-1: the distant wife he knows
        "cold": [
            _("Don't mind %s if she's short with you, son. She's short with everyone. It's how she says hello."),
            _("%s works too much. I keep telling her the world won't collapse without her. She disagrees."),
            _("Twenty years, and I still knock before I ask %s anything. You'll learn the rhythm."),
        ],
        # steps 2-3: the good mood he can't explain
        "warm": [
            _("%s has been in a good mood lately. Whatever you two are doing, keep doing it."),
            _("She hums in the kitchen now. %s! Humming! Must be my new aftershave."),
            _("I'm glad you two finally get along, son. Family should be close."),
        ],
    }

    FAMILY_CHAT_LINES = {
        "dad": {
            "low": [
                _("Hey, kid. School okay? Good. Good."),
                _("You need something? ...No? Alright."),
            ],
            "mid": [
                _("Work is killing me, kid. Enjoy college while it lasts."),
                _("Your stepmother wants to repaint the living room. Again. Don't tell her I said 'again'."),
                _("Your grandfather used to say a man is only as good as his word. I never understood it either."),
            ],
            "high": [
                _("You know, I'm proud of you. I don't say it enough."),
                _("Come by more often. This place feels like a hotel without you."),
                _("If you ever need anything, money, advice, a place to crash... you come to me first."),
            ],
        },
    }

    # Talking about his wife: kind -> his son's line ("%s" = her name), his answer by his love for her, and what she
    # does when she is in the room and hears it ("her_love" = her love for him, "love" = her Love for the player)
    FAMILY_GOSSIP = {
        "praise": {
            "say": _("%s is really something, Dad. You did well."),
            "reply": {
                "high": {"lines": [_("She is, isn't she? I'm a lucky man.")], "love": 15, "friendship": 5},
                "mid": {"lines": [_("She's... intense. But she means well. Most days.")], "love": 15, "friendship": 3},
                "low": {"lines": [_("Hm. If you say so. She hasn't smiled at me in weeks.")], "love": 10, "friendship": 0},
            },
            "hears": {
                "high": {"face": "smug", "lines": [_("Flattery. From both of you. How touching.")], "her_love": 5, "love": 3},
                "mid": {"face": "smug", "lines": [_("Hmph. I'm standing right here, you know.")], "her_love": 3, "love": 3},
                "low": {"face": "normal", "lines": [_("At least one man in this house notices.")], "her_love": 0, "love": 5},
            },
        },
        "badmouth": {
            "say": _("Honestly? %s can be a real nightmare."),
            "reply": {
                "high": {"lines": [_("Watch it. That's my wife you're talking about.")], "love": -5, "friendship": -10},
                "mid": {"lines": [_("...She can be cold, yeah. I've noticed.")], "love": -15, "friendship": 0},
                "low": {"lines": [_("You're telling me. Some days I wonder why I married her.")], "love": -20, "friendship": 5},
            },
            "hears": {
                "high": {"face": "smug", "lines": [_("Thank you, darling. ...And you. We'll talk later.")], "her_love": 10, "love": -10},
                "mid": {"face": "angry", "lines": [_("I'm standing right here. Both of you, remember that.")], "her_love": -10, "love": -10},
                "low": {"face": "angry", "lines": [_("Both of you. Out of my sight.")], "her_love": -25, "love": -5},
            },
        },
    }

    # A drink for him: member gid -> drink tier -> his answer
    FAMILY_DRINK_LINES = {
        "dad": {
            "low": [_("A beer? Sure, why not. Thanks, kid.")],
            "med": [_("The strong stuff on a weekday? Your stepmother would kill me. ...Cheers.")],
            "high": [_("Top shelf! Okay, who did you kill?"), _("The good stuff. You're a better son than I deserve.")],
        },
    }

    # The intro of a girl he meets at his first visit to her home (label _apartment_intro): gid -> parts. Lines as in
    # story_say ((who, line): None narration, "@player", "@husband", her face). "greet" = his greeting she cuts, by slot.
    FAMILY_INTROS = {
        "shion": {
            "open": [
                (None, _("You arrive at your father's apartment. Well, technically your stepmother's, but your father lives here too.")),
            ],
            "greet": {0: _("Good mor..."), 1: _("Good after..."), 2: _("Good eve..."), 3: _("Good eve...")},
            "shout": ("angry", _("TAKE OFF YOUR SHOES! YOU'LL SCRATCH MY FLOOR WITH THOSE GARDENER BOOTS!")),
            "after_shout": [
                ("@player", _("(That's Shion, my stepmother. After my parents split up, my father married her. She's terrible, but rich as fuck. And honestly, I can't blame my father. She's extremely hot.)")),
                ("smug", _("Are you lost, boy? What is it?")),
            ],
            "choices": [
                {"menu": _("I just came to say hi."),
                 "lines": [("annoyed", _("Okay. Hi. Now go study. You have no right to lose that scholarship.")),
                           ("serious", _("That college isn't much to begin with. If you fail, I'll recommend your father send you to the army once and for all."))],
                 "stats": {"Love": -5, "Obed": -5}},
                {"menu": _("I'm broke. I thought I could get some lunch money from you."),
                 "lines": [("angry", _("Are you kidding me? You already get the allowance we send you every week.")),
                           ("serious", _("Start taking care of your money. Do you think you're rich?")),
                           (None, _("She pulls a single dollar from her purse and drops it in your hand.")),
                           ("smug", _("Here. Buy yourself a candy and stay away."))],
                 "stats": {"Love": -10, "Obed": -10}, "cash": 1},
                {"menu": _("I just missed you guys, so I came to see you."),
                 "lines": [("smirk", _("You definitely didn't come here for that."))]},
            ],
            "close": [
                ("@husband", _("Ha! Don't mind her, kid. Make yourself at home. ...Shoes off, though.")),
            ],
        },
    }

    # ── his stats ──
    def family_stat(member, stat):
        _v = getattr(member, stat, None)
        return FAMILY_START.get(stat, 0) if _v is None else int(_v)

    _FAMILY_STAT_COLORS = {"friendship": "#ffc857", "love_for_wife": "#ff6b81"}
    _FAMILY_STAT_YPOS = {"friendship": 0.18, "love_for_wife": 0.23}
    _FAMILY_STAT_LABELS = {"friendship": "Friend", "love_for_wife": "Wife"}

    def family_change(member, stat, amount, why="", show_popup=True):
        _old = family_stat(member, stat)
        _new = max(0, min(FAMILY_STAT_MAX[stat], _old + int(amount)))
        setattr(member, stat, _new)
        _delta = _new - _old
        print("[FAMILY] %s %s %+d -> %d (%s)" % (member.gid, stat, int(amount), _new, why))
        if show_popup and _delta != 0:
            _prefix = "+" if _delta > 0 else "-"
            _tag = "stat_family_%s" % stat
            renpy.show_screen(
                "StatHolder",
                value=abs(int(_delta)),
                prefix=_prefix,
                color=_FAMILY_STAT_COLORS.get(stat, "#ffffff"),
                xpos=0.5,
                ypos=_FAMILY_STAT_YPOS.get(stat, 0.18),
                label_text=_FAMILY_STAT_LABELS.get(stat, stat.replace("_", " ").title()),
                hide_tag=_tag,
                _tag=_tag,
            )
        return _delta

    def family_tier(member, stat):
        _v = family_stat(member, stat)
        return next(_t for _min, _t in FAMILY_TIERS[stat] if _v >= _min)

    def wife_love(girl):
        """Her love for her husband (0-1000)."""
        _v = getattr(girl, "_love_for_husband", None)
        return GIRLS_CONFIG.get(girl.gid, {}).get("husband_love", WIFE_LOVE_START) if _v is None else int(_v)

    def wife_love_change(girl, amount, why="", show_popup=True):
        _old = wife_love(girl)
        girl._love_for_husband = max(0, min(1000, _old + int(amount)))
        _delta = girl._love_for_husband - _old
        print("[FAMILY] %s love for her husband %+d -> %d (%s)" % (girl.gid, int(amount), girl._love_for_husband, why))
        if show_popup and _delta != 0:
            _tag = "stat_family_husband_love"
            renpy.show_screen(
                "StatHolder",
                value=abs(int(_delta)),
                prefix="+" if _delta > 0 else "-",
                color="#ff6b81",
                xpos=0.5,
                ypos=0.28,
                label_text="Husband",
                hide_tag=_tag,
                _tag=_tag,
            )

    def family_wife(member):
        """The girl married to this family member (girl_husband), or None."""
        return next((_g for _g in ALL_GIRLS if girl_husband(_g) is member), None)

    # ── where he is ──
    def dad_room(day=None, ti=None):
        """The room of the apartment his father is in (APARTMENT_ROOMS), or None: at work, on a trip, out, asleep."""
        _dad = store.Dad
        _d = store.Day if day is None else day
        _ti = store.TimeIndex if ti is None else ti
        _here = getattr(_dad, "_here", None)
        if _here and _here[:2] == (_d, _ti):
            return _here[2]
        if dad_where(_d, _ti) != "home" or getattr(_dad, "_nap", None) == (_d, _ti):
            return None
        _room = DAD_ROOM_SCHEDULE[(_d - 1) % 7][_ti]
        if _room not in APARTMENT_ROOMS:
            return None
        if _room in DAD_PRIVATE_ROOMS and any(_g.loc == _room for _g in girls_reachable() if girl_home_loc(_g) in APARTMENT_ROOMS):
            return "apartment"
        return _room

    def family_room(member):
        """The room of the apartment a family member is in, or None."""
        return dad_room() if member is store.Dad else None

    def husband_in_room(girl):
        """Her husband is in the room with them right now: nothing of her ladder happens in front of him."""
        _h = girl_husband(girl)
        return (_h is not None and getattr(girl, "loc", None) == store.CurrentLocation
                and family_room(_h) == store.CurrentLocation)

    def family_on_scene():
        """The family members in the room he is in (the roster shows them, "Chat..." lists them)."""
        if getattr(store, "_in_event", False) or getattr(store, "_in_intro", False):
            return []
        return [_m for _m in family_contacts() if family_room(_m) is not None and family_room(_m) == store.CurrentLocation]

    # ── the first visit ──
    def girl_met_player(girl):
        """He has met her in the game: a girl whose config waits for him at home ("meets_at_home") is met at her intro."""
        if not GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("meets_at_home"):
            return True
        return bool(getattr(girl, "_met_player", False))

    def girl_home_rooms(girl):
        _home = girl_home_loc(girl)
        return APARTMENT_ROOMS if _home in APARTMENT_ROOMS else (_home,)

    def girl_pre_intro_loc(girl, loc):
        """get_scheduled_location_for: until he has met her she stays home."""
        if girl_met_player(girl) or loc in girl_home_rooms(girl) or loc == GIRL_AWAY_LOC:
            return loc
        return girl_home_loc(girl)

    def family_intro_girl():
        """The girl of the father's apartment he has never met (her intro plays at his first visit), or None."""
        return next((_g for _g in girls_reachable() if girl_home_loc(_g) in APARTMENT_ROOMS and not girl_met_player(_g)), None)

    def family_father_sync(why):
        """Load: a save where he already met her (the first dinner, her story, her history) never plays the intro."""
        for _g in ALL_GIRLS:
            if girl_met_player(_g):
                continue
            if (store._family_dinner == "done" or story_step(_g) > 0 or getattr(_g, "_story_seen", None)
                    or sum((getattr(_g, "Sex_acts", None) or {}).values())):
                _g._met_player = True
                # an old save skips the intro, but he heard the marriage there: the chip follows, silently
                if _g.has_trait("married"):
                    _g.flags["discovered_trait_married"] = True
                print("[FAMILY] %s: %s, he already knows her: no intro" % (_g.gid, why))

# ============================================================
# His talk ("Chat..." -> do_talk): chat, his wife, a drink. Each costs a chat
# ============================================================
label family_talk(member):
    python:
        _ft_wife = family_wife(member)
        _ft_wife_name = _ft_wife.Name if _ft_wife else ""
        _ft_gossiped = getattr(member, "_gossip_day", -1) == Day
        _ft_has_drink = player_has_any_drink()
        _ft_did = False
    menu:
        "Chat":
            call _family_chat(member) from _call_family_chat
            $ _ft_did = True
        "{color=#22c55e}Speak well of [_ft_wife_name]{/color}" if _ft_wife and not _ft_gossiped:
            call _family_gossip(member, _ft_wife, "praise") from _call_family_gossip_praise
            $ _ft_did = True
        "{color=#ef4444}Speak badly of [_ft_wife_name]{/color}" if _ft_wife and not _ft_gossiped:
            call _family_gossip(member, _ft_wife, "badmouth") from _call_family_gossip_badmouth
            $ _ft_did = True
        "!disabled![_tr('Talk about her (Already today)')]" if _ft_wife and _ft_gossiped:
            pass
        "{color=#f0d060}Give him a drink...{/color}" if _ft_has_drink:
            call _family_drink(member) from _call_family_drink
            $ _ft_did = getattr(store, "_family_drink_given", False)
        "!disabled![_tr('Give him a drink (No drinks)')]" if not _ft_has_drink:
            pass
        "Ask him to run an errand downstairs":
            call _family_errand(member) from _call_family_errand
            $ _ft_did = True
        "Never mind":
            pass
    if _ft_did:
        call Apply_Time_Cost(TIME_COSTS["chat"]) from _call_Apply_Time_Cost_family_talk
    return

label _family_chat(member):
    python:
        _fc_first = getattr(member, "_chat_day", -1) != Day
        member._chat_day = Day
        _fc_line = renpy.random.choice(FAMILY_CHAT_LINES[member.gid][family_tier(member, "friendship")])
        _fc_args = ()
        # his wife has a story: sometimes he talks about her mood instead, by the band of her step (he suspects nothing)
        _fc_wife = family_wife(member)
        if _fc_wife is not None and story_key(_fc_wife) is not None and renpy.random.random() < 0.35:
            _fc_band = "warm" if story_step(_fc_wife) >= 2 else "cold"
            _fc_line = renpy.random.choice(FAMILY_WIFE_MOOD_LINES[_fc_band])
            _fc_args = (_fc_wife.Name,)
            print("[FAMILY] %s: his line about his wife's mood (%s, her step %d)" % (member.gid, _fc_band, story_step(_fc_wife)))
        if _fc_first:
            family_change(member, "friendship", DAD_CHAT_GAIN, "chat")
    $ renpy.say(Character(member.Name, who_color=member.color), family_fmt(_fc_line, *_fc_args) if _fc_args else _tl(_fc_line))
    return

label _family_gossip(member, wife, kind):
    python:
        member._gossip_day = Day
        _fg = FAMILY_GOSSIP[kind]
        _fg_tier = family_tier(member, "love_for_wife")
        _fg_r = _fg["reply"][_fg_tier]
        _fg_hears = wife.loc == CurrentLocation
        print("[FAMILY] he speaks %s of %s to %s (his love tier %s, she hears %s)" % (kind, wife.gid, member.gid, _fg_tier, _fg_hears))
    $ Say_Player(_tl_fmt(_fg["say"], wife.Name))
    $ renpy.say(Character(member.Name, who_color=member.color), _tl(renpy.random.choice(_fg_r["lines"])))
    python:
        family_change(member, "love_for_wife", _fg_r["love"], kind)
        family_change(member, "friendship", _fg_r["friendship"], kind)
    if _fg_hears:
        python:
            _fg_h = _fg["hears"][_fg_tier]
            wife_love_change(wife, _fg_h["her_love"], "heard " + kind)
        $ set_scene_expression(wife, _fg_h["face"], pose="standing")
        $ Say_Line(wife, renpy.random.choice(_fg_h["lines"]))
        $ Change_Status(wife, "Love", _fg_h["love"])
        $ set_scene_expression(wife, "normal", pose="standing")
    return

label _family_drink(member):
    python:
        store._family_drink_given = False
        _fd_choices = [("%s (%d)" % (_tr(drink_info(_d)["label"]), _c), _d) for _d, _c in player_owned_drinks()]
        _fd_choices.append((_tl(_("Never mind")), None))
        _fd_pick = renpy.display_menu(_fd_choices)
    if _fd_pick is None:
        return
    python:
        store._family_drink_given = True
        player_consume_drink(_fd_pick)
        _fd_tier = drink_tier_of(_fd_pick)
        _fd_prev = getattr(member, "_drinks", None) or (Day, 0)
        _fd_n = (_fd_prev[1] if _fd_prev[0] == Day else 0) + 1
        member._drinks = (Day, _fd_n)
        family_change(member, "friendship", DAD_DRINK_FRIENDSHIP.get(_fd_tier, 5), "drink %s (%d today)" % (_fd_pick, _fd_n))
    $ Say_Player(_("Here. This one's for you."))
    $ renpy.say(Character(member.Name, who_color=member.color), _tl(renpy.random.choice(FAMILY_DRINK_LINES[member.gid][_fd_tier])))
    if _fd_n >= DAD_DRINKS_NAP:
        python:
            member._nap = (Day, TimeIndex)
            print("[FAMILY] %s falls asleep on the couch (drink %d today)" % (member.gid, _fd_n))
        $ Narration(_("Halfway through the glass, your father is snoring on the couch."))
        call Set_Scene(entry=False) from _call_Set_Scene_family_nap
    return

# The errand ask (family_talk): he refuses on his own, always. His wife in the room with her weight in the
# house (family_wife_overrules) decides for him: he goes to the corner store for the rest of this slot
# (family_errand_out), and the apartment is theirs. Once a day; her ladder still rules what happens in it.
label _family_errand(member):
    python:
        _fe_wife = family_wife(member)
        _fe_wife_here = _fe_wife is not None and _fe_wife.loc == CurrentLocation
        _fe_again = getattr(member, "_errand_day", -1) == Day
        _fe_rules = (not _fe_again) and _fe_wife_here and family_wife_overrules(_fe_wife)
        print("[FAMILY] errand ask: %s (wife %s here=%s, asked today=%s, she overrules=%s)" % (
            member.gid, getattr(_fe_wife, "gid", None), _fe_wife_here, _fe_again, _fe_rules))
    $ Say_Player(_tl(FAMILY_ERRAND_ASK))
    if _fe_again:
        $ renpy.say(Character(member.Name, who_color=member.color), _tl(renpy.random.choice(FAMILY_ERRAND_REFUSE_AGAIN)))
        return
    $ renpy.say(Character(member.Name, who_color=member.color), _tl(renpy.random.choice(FAMILY_ERRAND_REFUSE)))
    $ member._errand_day = Day
    if not _fe_rules:
        return
    # she cuts in: her word moves him where the player's couldn't
    $ set_scene_expression(_fe_wife, "normal", pose="standing")
    $ Say_Line(_fe_wife, rod_pick_line(_fe_wife, "family_errand_order"))
    $ renpy.say(Character(member.Name, who_color=member.color), _tl(renpy.random.choice(FAMILY_ERRAND_OBEY)))
    python:
        family_errand_out(member)
        member.hide_sprite()
    $ Narration(_("The front door closes behind him. The apartment is suddenly very quiet."))
    $ set_scene_expression(_fe_wife, "smug", pose="standing")
    $ Say_Line(_fe_wife, rod_pick_line(_fe_wife, "family_errand_alone"))
    $ set_scene_expression(_fe_wife, "normal", pose="standing")
    call Set_Scene(entry=False) from _call_Set_Scene_family_errand
    return

# ============================================================
# His first visit to the apartment: the intro of the girl of the house he has never met, his father in the living
# room with her (Apartment_Arrive). His father stays in the living room for the rest of that slot
# ============================================================
label _apartment_intro(girl):
    python:
        _ai = FAMILY_INTROS.get(girl.gid, {})
        _ai_dad = girl_husband(girl)
        girl.loc = "apartment"
        girl._met_player = True
        # dressed for the place before she is shown: the outfit check of the place (Set_Scene) only runs at the end
        # of the intro, and a save that left her with nothing on (a girl newer than an old save, 2026-10-06) played
        # the whole intro with her naked
        _enforce_location_outfit(girl)
        if _ai_dad is not None:
            _ai_dad._here = (Day, TimeIndex, "apartment")
        store._in_event = True
        print("[FAMILY] first visit: %s's intro (Day %d, slot %d)" % (girl.gid, Day, TimeIndex))
    scene bg apartment
    with fade
    call story_say(girl, _ai.get("open")) from _call_story_say_intro_open
    python:
        if _ai_dad is not None:
            _ai_dad.show_sprite(slot_left)
        set_girl_sprite(girl.gid, pose="standing", at_list=[slot_right])
    with dissolve
    if _ai.get("greet"):
        $ Say_Player(_ai["greet"].get(TimeIndex, _ai["greet"][0]))
    # belt and braces: the pair stays apart for the whole intro (tester 2026-10-11: his sprite sat in
    # front of hers while SHE was the one speaking)
    python:
        if _ai_dad is not None:
            _ai_dad.show_sprite(slot_left)
        set_girl_sprite(girl.gid, pose="standing", at_list=[slot_right])
    if _ai.get("shout"):
        $ set_scene_expression(girl, _ai["shout"][0], pose="standing")
        with vpunch
        $ Say_Line(girl, _ai["shout"][1])
    call story_say(girl, _ai.get("after_shout")) from _call_story_say_intro_after
    # the intro names the marriage ("my father married her"): the Married chip lights here (audit 2026-10-04)
    $ girl.discover("discovered_trait_married") if girl.has_trait("married") else None
    python:
        _ai_pick = renpy.display_menu([(_tl(_c["menu"]), _i) for _i, _c in enumerate(_ai.get("choices", ()))]) if _ai.get("choices") else None
        _ai_c = _ai["choices"][_ai_pick] if _ai_pick is not None else {}
    if _ai_c:
        $ Say_Player(_ai_c["menu"])
        call story_say(girl, _ai_c.get("lines")) from _call_story_say_intro_choice
        python:
            for _st, _amt in sorted(_ai_c.get("stats", {}).items()):
                Change_Status(girl, _st, _amt)
            if _ai_c.get("cash"):
                Player.add_cash(_ai_c["cash"])
            print("[FAMILY] intro: he says %r" % _ai_c["menu"])
    call story_say(girl, [_l for _l in _ai.get("close", ()) if _ai_dad is not None or _l[0] != "@husband"]) from _call_story_say_intro_close
    $ set_scene_expression(girl, "normal", pose="standing")
    $ store._in_event = False
    call Set_Scene(entry=True) from _call_Set_Scene_intro_end
    return
