## swimming.rpy: what swimming does for HIM, and the breath-holding bet at the pool.
## The pool action itself is do_swim (actions.rpy). Author's rules (2026-09-30):
##   - swimming is half a workout: every 2 days in the pool = one gym workout (Max Energy progress AND the
##     weekly minimum); only the first swim of a day counts (PlayerData.register_swim)
##   - Breath, its own stat, trained only by swimming: his arousal builds slower in scenes (add_player_focus)
##   - the bet: a kiss when she would take one from him, money below that; only a girl with a bikini gets in the
##     water (without one she says so, same lines as the swim invite)

# the fraction of an arousal tick Breath left over, carried to the next tick (add_player_focus)
default _focus_carry = 0.0

init python:

    SWIM_DAYS_PER_WORKOUT = 2     # two counted swim days = one gym workout
    SWIM_DAYS_PER_BREATH = 4      # counted swim days per Breath level
    BREATH_MAX = 5
    BREATH_FOCUS_CUT = 0.05       # each Breath level: his arousal builds 5% slower (up to 25%)
    BREATH_BET_CASH = 20          # the money bet when a kiss is not on the table
    BREATH_GIRL_BASE = 1          # her lungs in the contest; a gym rat's are much better
    BREATH_GYM_RAT = 3

    def player_breath_focus_mult():
        """How much of an arousal tick lands, by his Breath (1.0 at 0, 0.75 at BREATH_MAX)."""
        _b = min(BREATH_MAX, max(0, int(getattr(store.Player, "breath", 0))))
        return 1.0 - BREATH_FOCUS_CUT * _b

    # ── Shared by the swim invite and the bet ──
    _SWIM_DECLINE_LINES = [
        _("Maybe later, I'm just relaxing."),
        _("Not right now, thanks."),
        _("I'm good just sunbathing for now."),
    ]
    # she has no bikini: why she can't get in the water (first key that applies)
    _SWIM_NO_BIKINI_LINES = {
        "exhibitionist_late": [
            _("I don't have a bikini... but it's late enough that nobody would care, right?"),
            _("No bikini for me... but honestly, at this hour, I could just go in like this."),
        ],
        "exhibitionist": [
            _("I don't have a bikini either... I'd swim naked, but the lifeguard would kick us out."),
            _("No bikini for me... Too bad I can't just go in naked, the lifeguard is watching."),
        ],
        "poor": [
            _("I don't have a bikini... I can't really afford one right now."),
            _("I wish I could, but I don't have a swimsuit. They're not cheap."),
        ],
        "rich": [
            _("I don't have one with me, actually. I should order one online."),
            _("I forgot to bring a bikini. I'll have to pick one up later."),
        ],
        "_default": [
            _("I don't have a bikini... Maybe some other time."),
            _("I'd love to, but I don't have anything to swim in."),
        ],
    }

    def swim_no_bikini_line(girl):
        """Her line (translated) when she has no bikini to get in the water."""
        if girl.has_trait("exhibitionist"):
            _key = "exhibitionist_late" if store.TimeIndex >= 2 else "exhibitionist"
        elif girl.has_trait("poor"):
            _key = "poor"
        elif girl.has_trait("rich"):
            _key = "rich"
        else:
            _key = "_default"
        return _tl(renpy.random.choice(_SWIM_NO_BIKINI_LINES[_key]))

    def swim_together_ok(girl):
        """She wants to swim with him (the swim invite's check)."""
        return ApprovalCheck(girl=girl, T=200, Type="LI", Spread=100, Variation=50, Action="swim_together") >= 2

    # ── The breath-holding bet ──
    # (expression, line) per moment; "gym_rat" = the sporty girl's own voice, "_default" for everybody else
    _BREATH_BET_LINES = {
        "accept_kiss": {
            "_default": [("smirk", _("A kiss? ...Fine. But you're going to lose.")),
                         ("shy", _("You're on. Don't get your hopes up."))],
            "gym_rat":  [("smirk", _("A kiss? You'll have to beat me first. Good luck with that."))],
        },
        "accept_cash": {
            "_default": [("smirk", _("Easy money. You're on.")),
                         ("happy", _("Deal. Hope you brought your wallet."))],
            "gym_rat":  [("smirk", _("You're betting against me? I'll gladly take that money."))],
        },
        "again": {
            "_default": [("normal", _("Again? My lungs need a break. Tomorrow.")),
                         ("smirk", _("One contest a day. Come back tomorrow."))],
        },
        "win_kiss": {
            "_default": [("shy", _("Fine... a deal's a deal.")),
                         ("shy", _("Okay, you won. Come here."))],
            "gym_rat":  [("smirk", _("Not bad. Alright, you earned it."))],
        },
        "lose_kiss": {
            "_default": [("smirk", _("Guess you'll have to earn that kiss some other way.")),
                         ("happy", _("Ha! No kiss for you."))],
            "gym_rat":  [("smirk", _("Weak lungs. Come back when you can keep up."))],
        },
        "win_cash": {
            "_default": [("annoyed", _("Ugh. Fine, here's your money.")),
                         ("annoyed", _("I can't believe I lost. Take it."))],
            "gym_rat":  [("annoyed", _("...You got lucky. Take it before I change my mind."))],
        },
        "lose_cash": {
            "_default": [("happy", _("Pay up~")),
                         ("smirk", _("Thanks for the donation."))],
            "gym_rat":  [("smirk", _("Told you. Hand it over."))],
        },
        "lose_cash_broke": {
            "_default": [("bemused", _("You're broke? Forget it. Winning is enough."))],
        },
        "tie": {
            "_default": [("surprised", _("A tie? No way. Rematch next time.")),
                         ("happy", _("Nobody wins? That's so lame. Next time."))],
        },
    }
    _BREATH_BET_ASK = [
        _("Bet you can't hold your breath longer than me."),
        _("Breath-holding contest. You and me, right now."),
    ]

    def breath_bet_line(girl, moment):
        """(expression, translated line) for her at this moment of the bet: her gym-rat voice when she has one."""
        _pools = _BREATH_BET_LINES[moment]
        _pool = _pools.get("gym_rat") if girl.has_trait("gym_rat") else None
        if _pool:
            girl.discover("discovered_trait_gym_rat")   # her gym-rat voice in the bet
        _expr, _line = renpy.random.choice(_pool or _pools["_default"])
        return _expr, _tl(_line)

    def breath_bet_say(girl, moment):
        _expr, _line = breath_bet_line(girl, moment)
        set_scene_expression(girl, _expr)
        Say_Line(girl, _line)

    def breath_bet_accepts(girl):
        """She plays: never angry / sad; a gym rat never turns a challenge down; anyone else if she would swim with him."""
        if girl.has_temp_status("angry") or girl.has_temp_status("sad"):
            return False
        return girl.has_trait("gym_rat") or swim_together_ok(girl)

    def breath_bet_kiss_ok(girl):
        """The stake: a kiss when she would take one from him right now, money below that. Never a kiss with her
        partner watching, never from a lesbian before her kiss stage (read-only checks, no side effects)."""
        if flirt_partner_watching(girl) is not None:
            return False
        if _is_lesbian_stage_blocked(girl, "kiss")[0]:
            return False
        return bool(would_accept_action(girl, "kiss").get("accepted"))

    def breath_contest(girl):
        """'win' / 'lose' / 'tie' for him. Him: his Breath (+1 for the athlete trait) + 0..3. Her: BREATH_GIRL_BASE
        (a gym rat BREATH_GYM_RAT) + 0..3."""
        _you = (getattr(store.Player, "breath", 0) + (1 if getattr(store.Player, "player_trait", "") == "athlete" else 0)
                + renpy.random.randint(0, 3))
        _her = (BREATH_GYM_RAT if girl.has_trait("gym_rat") else BREATH_GIRL_BASE) + renpy.random.randint(0, 3)
        _result = "win" if _you > _her else ("lose" if _you < _her else "tie")
        print("[BREATH_BET] %s: him %d vs her %d -> %s" % (girl.gid, _you, _her, _result))
        return _result

# ============================================================
# After a swim: what it did for him (called by do_swim and the bet)
# ============================================================
label _swim_register:
    $ _sw_counted, _sw_energy_up, _sw_breath_up = Player.register_swim()
    if _sw_counted and not getattr(Player, "_swim_tip_shown", False):
        $ Player._swim_tip_shown = True
        # the WHY is in the line (tester 2026-10-10 read it as "two whole days = one workout, really?"):
        # a swim is a third of the time a gym session takes, so half credit per day is the fair trade
        $ Narration(_("Swimming counts too: a swim takes a fraction of a gym session, and every two swim days add up to one full workout."))
    if _sw_energy_up:
        $ Narration(_tl_fmt(_("All those laps are paying off. You feel stronger. {b}Max Energy up!{/b} (Max Energy: %d/5)"), Player.energy_max))
        if Player.energy_max >= 5:
            $ unlock_achievement("max_fit")
    if _sw_breath_up:
        $ Narration(_tl_fmt(_("Holding your breath under water is getting easier. {b}Breath up!{/b} (Breath: %d/%d)"), Player.breath, BREATH_MAX))
    return

# ============================================================
# THE BREATH-HOLDING BET (pool menu)
# ============================================================
label breath_challenge:
    python:
        _bb_here = [_g for _g in ALL_GIRLS if _g.loc == CurrentLocation]
    if not _bb_here:
        return
    if len(_bb_here) == 1:
        $ _bb_girl = _bb_here[0]
    else:
        # a None value would render as an unclickable caption: "Never mind" needs a real value
        $ _bb_girl = renpy.display_menu([(_g.Name, _g) for _g in _bb_here] + [(_("Never mind"), "back")])
    if _bb_girl != "back":
        call breath_challenge_with(_bb_girl) from _call_breath_challenge_with
    return

label breath_challenge_with(girl):
    $ Say_Player(renpy.random.choice(_BREATH_BET_ASK))

    # no bikini: she cannot get in the water (the swim invite's lines)
    if not getattr(girl, "_bikini_unlocked", False):
        $ set_scene_expression(girl, "sad")
        $ Say_Line(girl, swim_no_bikini_line(girl))
        $ set_scene_expression(girl, "normal")
        return

    if getattr(girl, "_breath_challenge_day", -1) == Day:
        $ breath_bet_say(girl, "again")
        $ set_scene_expression(girl, "normal")
        return

    if not breath_bet_accepts(girl):
        $ set_scene_expression(girl, "normal")
        $ Say_Line(girl, _tl(renpy.random.choice(_SWIM_DECLINE_LINES)))
        return

    $ girl._breath_challenge_day = Day
    $ _bb_kiss = breath_bet_kiss_ok(girl)
    if _bb_kiss:
        $ Say_Player(_("If I win, you owe me a kiss."))
        $ breath_bet_say(girl, "accept_kiss")
    else:
        $ Say_Player(_tl_fmt(_("Loser pays $%d."), BREATH_BET_CASH))
        $ breath_bet_say(girl, "accept_cash")

    if getattr(girl, "CurrentOutfitPreset", None) != "pool":
        $ girl.WearPreset("pool", apply_now=True)
        with dissolve

    $ Narration(_("You both take a deep breath and sink under the water."))
    $ _bb_result = breath_contest(girl)
    if _bb_result == "win":
        $ Narration(_("She bursts up first, gasping for air. You win."))
    elif _bb_result == "lose":
        $ Narration(_("Your lungs give out first. You surface, coughing. She wins."))
    else:
        $ Narration(_("You both burst up at the same time."))

    # the stake
    if _bb_result == "tie":
        $ breath_bet_say(girl, "tie")
    elif _bb_kiss and _bb_result == "win":
        $ store._flirt_partner_pending = None
        $ _bb_kiss_line = breath_bet_line(girl, "win_kiss")[1]
        call _kiss_accepted(girl, _bb_kiss_line) from _call_breath_bet_kiss
    elif _bb_kiss:
        $ breath_bet_say(girl, "lose_kiss")
    elif _bb_result == "win":
        $ Player.add_cash(BREATH_BET_CASH)
        $ breath_bet_say(girl, "win_cash")
        $ Narration(_tl_fmt(_("She hands you {b}$%d{/b}."), BREATH_BET_CASH))
    elif Player.spend_cash(BREATH_BET_CASH):
        $ breath_bet_say(girl, "lose_cash")
        $ Narration(_tl_fmt(_("You hand her {b}$%d{/b}."), BREATH_BET_CASH))
    else:
        $ breath_bet_say(girl, "lose_cash_broke")

    # a gym rat respects strength and despises weakness; anyone else just had fun
    python:
        if girl.has_trait("gym_rat"):
            if _bb_result == "win":
                Change_Status(girl, "Love", 3)
                Change_Status(girl, "Obed", 2)
            elif _bb_result == "lose":
                Change_Status(girl, "Love", -2)
        else:
            Change_Status(girl, "Love", 2)
    $ set_scene_expression(girl, "normal")

    # both of them were in the water: it is this day's swim
    call _swim_register from _call_swim_register_bet
    call Apply_Time_Cost(TIME_COSTS["swim"]) from _call_Apply_Time_Cost_breath_bet
    return
