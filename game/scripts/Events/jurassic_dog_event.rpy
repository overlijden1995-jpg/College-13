# ============================================================
# JURASSIC DOG — C. Johnson first meeting + van menu
# Fires the first time the player enters campus while the
# van is present (Mon/Wed/Fri, Morning or Midday).
# ============================================================

# ── Check (called from Campus_Entry, after Set_Scene) ──

label cjohnson_check:

    if _met_cjohnson:
        return

    # Van schedule: Mon/Wed/Fri, Morning or Midday
    $ _cj_weekday = (Day - 1) % 7
    if _cj_weekday not in (1, 3, 5) or TimeIndex not in (0, 1):
        return

    call cjohnson_first_meeting from _call_cjohnson_first_meeting
    return

# ── First meeting event ─────────────────────────────────────

label cjohnson_first_meeting:

    # _in_event hides the van overlay (clickable van + "start his quest" pulse) while he introduces himself;
    # _met_cjohnson is only set at the end, or the pulse would already fire during this first talk.
    $ store._in_event = True
    $ debug_log("[EVENT] cjohnson_first_meeting triggered (Day %d, TimeIndex %d)" % (Day, TimeIndex))

    # Clear all characters from the scene during this event
    python:
        for _g in ALL_GIRLS:
            if _g.loc == "campus":
                _g.loc = girl_home_loc(_g)
            hide_girl_sprite(_g)
        for _nh in NPC_PARTNERS.values():
            _nh.hide_sprite()
            if _nh.loc == "campus":
                _nh.loc = GIRL_ROOMS.get(getattr(_nh, "girl_gid", ""), "room")
        store._npc_on_scene = None
        store.CurrentGirl = None

    "You notice an unusual van parked on the campus lawn. The smell coming from it is incredible, but the man running the grill looks like he has more body hair than a mammoth."

    "You walk over to check out the menu."

    CJohnsonChar "Hey kiddo! How you doing? Welcome, welcome. You want how many hot dog?"

    "He certainly has a unique way of conjugating verbs. He's wearing an orange apron with black triangles."

    PlayerChar "Hey, nothing for now. Just wanted to check out the prices. Money's a bit tight."

    CJohnsonChar "If money tight, can work with me. My helper Bell... he no can work every day. Need someone to help at grill sometimes and put together the hot dogs."

    PlayerChar "Hmm... could be an honest way to make a living... Do you pay well?"

    CJohnsonChar "Is hot dog, little buddy. Me do this for love... and for seeing the beautiful women on campus. Especially that new professor lady."

    PlayerChar "At least how much do you pay for my time?"

    CJohnsonChar "If you work morning... me have breakfast hot dog, much better than those horrible egg tacos... and afternoon, me pay 100. If only afternoon, me pay 50."

    PlayerChar "Alright, I might help you out sometimes."

    CJohnsonChar "Come when you want. Me like your face. You attract pretty women and sell much sausage."

    CJohnsonChar "Come eat hot dog sometimes. Recover energy and give strength to kiss pretty girls."

    $ Player.discover("johnson_hotdog_energy")

    "You head back to the center of campus."

    $ store._met_cjohnson = True
    $ store._in_event = False
    return

# ── Van click menu ──────────────────────────────────────────

label jurassic_dog_menu:

    if not _met_cjohnson:
        "The hairy man behind the grill seems busy. Maybe another time."
        return

    if not store._cj_shady_intro:
        call cjohnson_shady_intro from _call_cjohnson_shady_intro

    # "life too short for just one girl": only for a player with exactly ONE girlfriend. Already poly
    # (2+ girlfriends or a harem accepted): the hint is moot, mark it seen without playing it.
    $ _cj_gfs = get_player_girlfriends(ALL_GIRLS)
    if not store._cj_harem_hint and (len(_cj_gfs) >= 2 or getattr(store, "relationship_mode", "mono") == "poly"):
        $ store._cj_harem_hint = True
        $ debug_log("[EVENT] cjohnson_harem_hint skipped, player already poly (gfs=%d)" % len(_cj_gfs))
    elif not store._cj_harem_hint and len(_cj_gfs) == 1:
        call cjohnson_harem_hint from _call_cjohnson_harem_hint

    $ _cj_can_talk = (_cj_last_talk_day != Day)
    $ print("[CJ] van menu: last_talk_day=%s Day=%s can_talk=%s" % (_cj_last_talk_day, Day, _cj_can_talk))

    menu:
        "Talk to C. Johnson" if _cj_can_talk:
            call jd_talk from _call_jd_talk

        "!disabled!Talk to C. Johnson (already talked today)" if not _cj_can_talk:
            pass

        "Buy Hot Dog ($20)" if Player.cash >= 20:
            $ Player.spend_cash(20)
            $ Player.change_energy(1)
            $ Player._hotdog_count = getattr(Player, "_hotdog_count", 0) + 1
            "You grab a hot dog from the Jurassic Dog. It's surprisingly delicious. {b}Energy +1{/b}."

        "!disabled!Buy Hot Dog (need $20)" if Player.cash < 20:
            pass

        "Work the shift":
            call jd_work from _call_jd_work

        "Suspicious Items" if store._cj_shady_intro:
            call cj_suspicious_items from _call_cj_suspicious_items

        "Leave":
            pass

    return

# ── Work shift ──────────────────────────────────────────────

label jd_work:

    if is_exam_slot(Day, EXAM_TIME_INDEX):
        CJohnsonChar "You no have exam today, little buddy? Me need you focused and in university with good grades! Come back next week."
        return

    $ _jd_pay = 100 if TimeIndex == 0 else 50

    python:
        _evening_idx = TIME_NAMES.index("Evening")
        _slots = _evening_idx - store.TimeIndex
        store.Round = 0
        store.LastPresentGirls = [g for g in ALL_GIRLS if g.loc == store.CurrentLocation]
        for _i in range(_slots):
            advance_time(1)

    python:
        _jd_work_lines = [
            _("You spend the shift assembling hot dogs and handling an uncomfortable amount of sausages for the campus crowd."),
            _("You spend the shift flipping 'mammoth burgers' for the campus crowd. Whatever that means, they taste surprisingly good."),
            _("You spend the shift cleaning the grill and restocking all the condiments. C. Johnson is very particular about his mustard-to-ketchup ratio."),
        ]
        _jd_work_line = _tl(renpy.random.choice(_jd_work_lines))

    $ Player.cash += _jd_pay
    "[_jd_work_line] C. Johnson hands you {b}$[_jd_pay]{/b}."

    "It's now Evening."

    call Wait from _call_Wait_jd
    call Set_Scene(entry=True) from _call_Set_Scene_jd_work

    return

# ── Talk to C. Johnson ──────────────────────────────────────
# One talk per day. All lines (generic + contextual tips) in
# one pool. If the random pick is a tip, unlock achievement.
# ────────────────────────────────────────────────────────────

init python:
    _CJ_GIRL_DESC = {
        "gwen": "blue hair girl",
        "rogue": "white and black hair girl",
        "ntw": "punk hair girl",
        "tenny": "redhead girl",
    }

    # Translation extraction markers (never runs, just for generate_translate)
    if False:
        _("blue hair girl")
        _("white and black hair girl")
        _("punk hair girl")
        _("redhead girl")
        _("that girl")

label jd_talk:

    $ store._cj_last_talk_day = Day

    python:
        # (line, is_tip, discovery_key)
        _jd_pool = []

        # ── Generic lines (not tips) ──
        _jd_pool.append((_("This place good, but too many skinny young women. Need more professors, with big bodies. Older women is what good in the world."), False, None))
        _jd_pool.append((_("Me hear skinny girl talking about you earlier. Not sure if she hate you or like you. Hard to tell from the words."), False, None))
        _jd_pool.append((_("Gothic girl give me scare. She give me static shock when me try to hand her hot dog. Me would not touch her if me was you."), False, None))
        _jd_pool.append((_("Colorful hair girl very crazy. She talk to herself like she on a reality show."), False, None))
        _jd_pool.append((_("Remember to use gym. Lift hard rock, sad voice go byebye."), False, None))
        _jd_pool.append((_("Study, little buddy. High grades and you can buy a lot of hot dog in the future."), False, None))
        _jd_pool.append((_("Me love warm nights. Perfect for swim under moonlight."), False, None))

        # ── Contextual tips (hidden hints) ──

        # NPC partner suspicious of player
        for _nh in NPC_PARTNERS.values():
            if getattr(_nh, "suspicion", 0) >= 30:
                _jd_pool.append((_("Other students talk about you playing with more than one girl. Here, take this club and bonk them on the head for being gossips."), True, "johnson_npc_suspicious"))
                break

        # Player broke up with someone
        if any(getattr(g, "is_ex_of_player", lambda: False)() for g in ALL_GIRLS):
            _jd_pool.append((_("Me hear you end relationship. No be sad, that happen to everyone. Here, eat hot dog, on the house."), True, "johnson_breakup"))

        # Caught in public act
        if any(getattr(g, "GetActionCount", lambda k: 0)("caught_public_sex") > 0 for g in ALL_GIRLS):
            _jd_pool.append((_("Me hear thing from very angry professor about you today. Well done, you really know how to handle sausage, huahuahuahua."), True, "johnson_caught_public"))

        # Player attractiveness (hidden stat)
        _attr = getattr(Player, "attractiveness", 50)
        if _attr >= 60:
            _jd_pool.append((_("Many girl talk about you. You lucky, friend, enjoy the youth!"), True, "johnson_attractive"))
        elif _attr < 30:
            _jd_pool.append((_("Me only see you with those weird nerds who play fairy game. Do not let the ugly bring you down, friend! Together we stronger."), True, "johnson_unattractive"))

        # Lesbian girl ceding (hidden stat)
        for _g in ALL_GIRLS:
            if _g.has_trait("lesbian") and lesbian_openness(_g) >= 50:
                _gdesc = _tl(_CJ_GIRL_DESC.get(_g.gid, _("that girl")))   # _() on a variable is identity: the piece stayed English inside a translated line
                _jd_pool.append((_tl(_("Me notice something about %s lately. She say she no like men, but she walk different now. Eyes tell different story.")) % _gdesc, True, "johnson_lesbian_%s" % _g.gid))
                break

        # NPC hostile to player
        for _nh in NPC_PARTNERS.values():
            if _nh.is_hostile():
                _gdesc = _tl(_CJ_GIRL_DESC.get(getattr(_nh, "girl_gid", ""), _("that girl")))
                _ga = "a" if getattr(_nh, "gender", "male") == "female" else "o"
                _pp = _tl(_("She")) if getattr(_nh, "gender", "male") == "female" else _tl(_("He"))
                _jd_pool.append((_tl(_("Partner of %(gdesc)s look very angry at you yesterday. %(pp)s kick trash can when you walk by. Watch your back, little buddy.")) % {"gdesc": _gdesc, "pp": _pp, "ga": _ga}, True, "johnson_npc_hostile_%s" % getattr(_nh, "girl_gid", "")))
                break

        # NPC partner traits (ntr / proud)
        for _nh in NPC_PARTNERS.values():
            _gdesc = _tl(_CJ_GIRL_DESC.get(getattr(_nh, "girl_gid", ""), _("that girl")))
            _jf = getattr(_nh, "gender", "male") == "female"
            # Johnson's words: %(pp)s = "Girl" / "Boy", %(po)s = his / her (the possessive), the rest from gender_fmt
            _jfmt = gender_fmt(_jf)
            _jfmt.update(partner_label_fmt(_jf))
            _jfmt.update({"pp": _tl(_("Girl")) if _jf else _tl(_("Boy")), "po": _jfmt["poss"], "gdesc": _gdesc})
            if _nh.has_trait("ntr"):
                _jd_pool.append((_tl(_("%(pp)s %(pl)s of %(gdesc)s be very strange. Ask me if me ever think about being with committed girls.")) % _jfmt, True, "johnson_npc_ntr_%s" % getattr(_nh, "girl_gid", "")))
                break
            elif _nh.has_trait("proud"):
                _jd_pool.append((_tl(_("%(pp)s %(pl)s of %(gdesc)s very angry! %(pp)s look at %(po)s partner funny and get furious and throw hot dog at me.")) % _jfmt, True, "johnson_npc_proud_%s" % getattr(_nh, "girl_gid", "")))
                break

        # He is a father (children.rpy): one child / children with several girls. Work is how the bills get paid.
        _jd_mothers = len([_jm for _jm in player_mothers() if child_support_due(_jm) > 0])     # a child her partner raises is a secret, and costs him nothing
        if _jd_mothers == 1:
            _jd_pool.append((_("Me hear you is papa now, little buddy! Baby cost many green papers. Work shift with CJ, me pay good."), True, "johnson_father_one"))
        elif _jd_mothers > 1:
            _jd_pool.append((_("Me hear you have many baby now, with many mama. You very busy sausage, huahuahuahua. Green papers fly away every week, yes? Come work with CJ."), True, "johnson_father_many"))

        # Player has given gifts to at least one girl
        if any(getattr(g, "_total_gifts_value", 0) > 0 for g in ALL_GIRLS):
            _jd_pool.append((_("Women very greedy these days. Me think if you give enough gifts and show you have money, some even do things for cash."), True, "johnson_financial_gifts"))

        # Prefer undiscovered tips; a tip he already told once is SPENT. Re-picking old tips kept the
        # one-shot news ("you is papa now!") coming back day after day and starved his generic small
        # talk forever (tester 2026-10-10). Nothing new to tell = he talks like always.
        _jd_tips = [x for x in _jd_pool if x[1]]
        _jd_new_tips = [x for x in _jd_tips if x[2] and not Player.has_discovery(x[2])]
        if _jd_new_tips:
            _jd_pick = renpy.random.choice(_jd_new_tips)
        else:
            _jd_generics = [x for x in _jd_pool if not x[1]]
            _jd_pick = renpy.random.choice(_jd_generics or _jd_pool)
        _jd_talk_line = _tl(_jd_pick[0])
        _jd_is_tip = _jd_pick[1]
        _jd_discover_key = _jd_pick[2]

    CJohnsonChar "[_jd_talk_line]"

    if _jd_is_tip:
        $ unlock_achievement("jurassic_help")
    if _jd_discover_key:
        $ Player.discover(_jd_discover_key)

    return

# ── CJ Shady Intro ─────────────────────────────────────────

label cjohnson_shady_intro:

    $ store._cj_shady_intro = True
    $ debug_log("[EVENT] cjohnson_shady_intro triggered (Day %d)" % Day)

    "You notice C. Johnson loading heavy boxes into his van."

    PlayerChar "Hey, CJ. Need a hand?"

    CJohnsonChar "NO! HELP NO NEED! Oops, is you little buddy. Of course, help me here."

    "You hear a crack in your back as you try to lift the boxes."

    PlayerChar "Damn, what do you have in here? Rocks?"

    CJohnsonChar "Yes, there have rock collection mine. But take other ones, they lighter. Hot dog not giving so much money, me need side business. Got rare things from my friend who wear dress at other college."

    PlayerChar "Rare? What kind?"

    CJohnsonChar "Look little buddy, world is hard, some decisions made on impulse charge child support. If want to make change, talk to me."

    PlayerChar "I didn't understand a word of that."

    CJohnsonChar "5 thousand green papers and kaboom, no more kid, nobody remember nothing."

    PlayerChar "What?!"

    CJohnsonChar "Me have other suspicious things soon. Trust me. You understand when older."

    "You decide to leave CJ alone. Apparently he now has items that change decisions that should be permanent in the real world."

    "Also saves you from starting a new save file. Very useful."

    return

# ── Harem hint (one-shot, after player starts dating) ──────

label cjohnson_harem_hint:

    $ debug_log("[EVENT] cjohnson_harem_hint triggered (Day %d)" % Day)

    CJohnsonChar "Hey little buddy. Here, take hot dog. Me find out you got girl. Many congratulation."

    CJohnsonChar "But you know, life too short for just one girl. If want another, me think you can. Talk to girlfriend, me sure they would like have someone like you!"

    menu:
        "Thanks, CJ!":
            pass

        "What do you mean? Explain!":
            CJohnsonChar "Heh, me understand everything about women. Young people today weak, call it open relationship. But only for them, you smart and never share."

            CJohnsonChar "Talk to girlfriend to see if she okay with it, make things easier. Or go straight and ask other girl to be girlfriend, they sort it out."

            CJohnsonChar "You too busy with hot dog to worry about this."

            menu:
                "Thanks, CJ!":
                    pass

    $ store._cj_harem_hint = True
    $ debug_log("[EVENT] _cj_harem_hint = True")

    return

# ── Suspicious Items Menu ───────────────────────────────────

label cj_suspicious_items:

    python:
        _cj_girls_with_kids = player_mothers()
        _cj_has_baby_eraser = len(_cj_girls_with_kids) > 0

    CJohnsonChar "Ah, little buddy want the special menu. What you need?"

    menu:
        "Baby Eraser ($5000)" if _cj_has_baby_eraser:
            call cj_baby_eraser from _call_cj_baby_eraser

        "!disabled!Baby Eraser (no one has children)" if not _cj_has_baby_eraser:
            pass

        "Girls Tracker ($500)" if not Player.has_item("girls_tracker"):
            call cj_girls_tracker from _call_cj_girls_tracker

        "!disabled!Girls Tracker (owned)" if Player.has_item("girls_tracker"):
            pass

        "Y.U.Z.U. Trait Discover ($1500)" if not _yuzu_purchased:
            call cj_yuzu_trait_discover from _call_cj_yuzu_trait_discover

        "!disabled!Y.U.Z.U. Trait Discover (owned)" if _yuzu_purchased:
            pass

        "Instant Pregnancy Test ($100)" if _pregnancy_mode != "off" and not Player.has_item("instant_preg_test"):
            call cj_instant_preg_test from _call_cj_instant_preg_test

        "!disabled!Instant Pregnancy Test (owned)" if _pregnancy_mode != "off" and Player.has_item("instant_preg_test"):
            pass

        # pregnancy turned off at game start: the test could never do anything
        "!disabled!Instant Pregnancy Test (pregnancy disabled)" if _pregnancy_mode == "off":
            pass

        "Leave":
            CJohnsonChar "Come back when you need something, little buddy."

    return

# ── Instant Pregnancy Test ─────────────────────────────────

label cj_instant_preg_test:

    CJohnsonChar "Yes, friend! At the level of tiny cells. If you have this, you know right away if girl got pregnant!"

    CJohnsonChar "100 green papers. You want?"

    if Player.cash < 100:
        PlayerChar "I don't have enough money right now."
        CJohnsonChar "Okay. You come back when pocket is full, little buddy."
        return

    menu:
        "Buy it ($100)":
            $ Player.spend_cash(100)
            $ Player.add_item("instant_preg_test", 1)
            CJohnsonChar "Done. Now when you do the thing... if baby start, you see special animation. Science is beautiful, little buddy."

        "No thanks":
            CJohnsonChar "Okay. You come back when curiosity win, little buddy."

    return

# ── Baby Eraser ─────────────────────────────────────────────

label cj_baby_eraser:

    CJohnsonChar "Ah, you want the baby go-away thing. Which pretty lady need to forget?"

    python:
        _cj_girl_choices = [(_g.Name, _g.gid) for _g in player_mothers()]

    menu:
        "[_cj_girl_choices[0][0]]" if len(_cj_girl_choices) >= 1:
            $ _cj_target_gid = _cj_girl_choices[0][1]
        "[_cj_girl_choices[1][0]]" if len(_cj_girl_choices) >= 2:
            $ _cj_target_gid = _cj_girl_choices[1][1]
        "[_cj_girl_choices[2][0]]" if len(_cj_girl_choices) >= 3:
            $ _cj_target_gid = _cj_girl_choices[2][1]
        "[_cj_girl_choices[3][0]]" if len(_cj_girl_choices) >= 4:
            $ _cj_target_gid = _cj_girl_choices[3][1]
        "Never mind":
            CJohnsonChar "Okay, you think about it."
            return

    python:
        _cj_target_girl = None
        for _g in ALL_GIRLS:
            if _g.gid == _cj_target_gid:
                _cj_target_girl = _g
                break

    CJohnsonChar "5 thousand green papers, little buddy. No refund, no receipt, no questions."

    if Player.cash < 5000:
        PlayerChar "I don't have that kind of money right now."
        CJohnsonChar "You come back when pocket is full, little buddy."
        return

    menu:
        "Pay $5000":
            pass
        "Never mind":
            CJohnsonChar "You come back when you ready."
            return

    $ Player.cash -= 5000

    CJohnsonChar "Here, take this."

    "CJ hands you... a coat hanger tied to a watch with twine."

    PlayerChar "What the hell is this?"

    CJohnsonChar "Is Baby Eraser. Very advanced technology. You press button on watch and point at direction of pretty lady. Poof. She no remember baby, no remember nothing. Like time travel but cheap."

    PlayerChar "This can't possibly work."

    CJohnsonChar "5 thousand green papers say it work. Trust CJ."

    "You press the button on the watch. The coat hanger vibrates slightly."

    "Nothing seems to happen."

    CJohnsonChar "Is done. She no remember nothing now. Magic of science."

    PlayerChar "There's no way that actually..."

    CJohnsonChar "You go check. CJ never lie. Well, CJ sometimes lie. But not about this."

    "Against all logic, you have a feeling he might be right."

    python:
        if _cj_target_girl:
            # ONE wipe (children.rpy): child state, his discovery answer, the paternity claim, the procedure,
            # what the other girls hold about her pregnancy. It used to reset three attributes and leave the rest.
            _cj_cleared = children_forget(_cj_target_girl, "baby_eraser")
            debug_log("[CJ] Baby Eraser used on %s, cleared: %s" % (_cj_target_girl.gid, _cj_cleared))

    return

# ── Girls Tracker ──────────────────────────────────────────

label cj_girls_tracker:

    CJohnsonChar "I also have tracker. Very useful, save time walking around looking for little girlfriends."

    CJohnsonChar "500 green papers. You want?"

    if Player.cash < 500:
        PlayerChar "I don't have enough money right now."
        CJohnsonChar "You come back when pocket is full, little buddy."
        return

    menu:
        "Buy it ($500)":
            $ Player.spend_cash(500)
            $ Player.add_item("girls_tracker", 1)
            CJohnsonChar "Done. Check contact screen on your phone. Magic device tell where girl is."

        "No thanks":
            CJohnsonChar "Okay. You come back when legs get tired, little buddy."

    return

# ── Y.U.Z.U. Trait Discover ───────────────────────────────
# The report is a snapshot of the purchase (CJ: "If trait change later, report no update"). Girls: the
# discovered_trait_* flags it sets. NPC partners: _yuzu_npc_report, yuzu_npc_key() -> his / her traits at the
# purchase, read by the phone NPC status (yuzu_npc_report_traits): a partner met later is not in it.
# None = a save that bought the report before the snapshot existed: the phone keeps the live traits there.

default _yuzu_npc_report = None

init python:

    def yuzu_npc_key(npc):
        """An NPC partner in the report: her gid + the partner's name (saved on the girl, never given to a new
        partner, kept by an ex who comes back)."""
        return "%s|%s" % (getattr(npc, "girl_gid", ""), getattr(npc, "name", ""))

    def yuzu_npc_snapshot():
        """Every NPC partner as the report sees him / her at the purchase: {yuzu_npc_key: sorted traits}."""
        _snap = {}
        for _g in ALL_GIRLS:
            _npc = get_npc_partner_for(_g)
            if _npc is not None:
                _snap[yuzu_npc_key(_npc)] = sorted(_npc.traits)
        print("[YUZU] report snapshot of the NPC partners: %s" % (_snap or "none"))
        return _snap

    def yuzu_npc_report_traits(npc):
        """The traits the Y.U.Z.U. report holds for this NPC partner, or None when it does not cover him / her
        (not bought, or a partner met after the purchase)."""
        if not getattr(store, "_yuzu_purchased", False):
            return None
        _report = getattr(store, "_yuzu_npc_report", None)
        if _report is None:
            return set(getattr(npc, "traits", None) or ())   # bought before the snapshot existed: live, as before
        _traits = _report.get(yuzu_npc_key(npc))
        return None if _traits is None else set(_traits)

label cj_yuzu_trait_discover:

    if not store._cj_yuzu_intro:

        PlayerChar "YUZU... What is this? What does the acronym stand for? And what does it do?"

        CJohnsonChar "No idea. Me just sell. Hackerman friend anomalous. Check data of people and give you report. Very good. Me increase hot dog profit 400%%."

        PlayerChar "Report? What do you mean?"

        CJohnsonChar "Tell you Traits of people from College. The College Traits! Work very good!"

        $ store._cj_yuzu_intro = True

    CJohnsonChar "1500 green papers for full report. You want?"

    if Player.cash < 1500:
        PlayerChar "I don't have enough money right now."
        CJohnsonChar "You come back when pocket is full, little buddy."
        return

    menu:
        "Buy it ($1500)":
            pass

        "No thanks":
            CJohnsonChar "Okay. Curiosity always win, little buddy. You come back."
            return

    $ Player.spend_cash(1500)

    python:
        _yuzu_all_trait_keys = list(TRAIT_HINT_DISPLAY.keys()) + [
            "experienced", "has_boyfriend", "has_girlfriend",
        ]
        for _yg in ALL_GIRLS:
            for _yt in _yuzu_all_trait_keys:
                if _yg.has_trait(_yt):
                    _yg.flags["discovered_trait_" + _yt] = True
            if _yg.has_npc_partner():
                _yg.flags["discovered_has_partner"] = True
        # the NPC partners as they are NOW: the report never updates (CJ below)
        store._yuzu_npc_report = yuzu_npc_snapshot()

        store._yuzu_purchased = True
        debug_log("[CJ] Y.U.Z.U. purchased — all girl traits + NPC traits revealed")

    $ renpy.music.play("audio/Information.mp3", channel="notify_sfx", loop=False)
    show screen discovery_banner(girl_name="Y.U.Z.U.", info_text=_tl(_("Report Received")) + "\n" + _tl(_("Traits updated for all contacts")), name_color="#00ff88")

    CJohnsonChar "Done. Check phone. All information there now. Hackerman friend very good."

    CJohnsonChar "If trait change later, report no update. But what is there now, is correct. Trust CJ."

    return
