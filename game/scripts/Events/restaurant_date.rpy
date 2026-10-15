# ============================================================
# RESTAURANT DATE SYSTEM
# Event-based: invite via phone → meet at Evening → restaurant
# ============================================================

define WaitressChar = Character(_("Waitress"), color="#c8a2c8")

default _restaurant_day = -1
default _restaurant_mode = "solo"
default _restaurant_girls = []
default _restaurant_bonus = 0
default _restaurant_orders = {}
default _restaurant_turn = 0
default _rest_score = 0
default _rest_compliments_used = []
default _rest_food_prefs = {}
default _restaurant_bg = None
default _restaurant_invite_state = {}
default _rest_attention = {}

transform _rest_slide_under_table:
    xalign StageCenter
    yalign 2.0
    yoffset 0
    linear 0.6 yoffset 700

transform _rest_slide_back_up:
    xalign StageCenter
    yalign 2.0
    yoffset 700
    linear 0.6 yoffset 0

transform _rest_exit_left:
    xalign StageCenter
    yalign 2.0
    ease 0.8 xalign -0.3

transform _rest_enter_from_left:
    xalign -0.3
    yalign 2.0
    ease 0.8 xalign StageCenter

transform _rest_slide_under_table_left:
    xalign StageLeft
    yalign 2.0
    yoffset 0
    linear 0.6 yoffset 700

transform _rest_slide_back_up_left:
    xalign StageLeft
    yalign 2.0
    yoffset 700
    linear 0.6 yoffset 0

transform _rest_exit_right:
    xalign StageCenter
    yalign 2.0
    ease 0.8 xalign 1.3

transform _rest_enter_from_right:
    xalign 1.3
    yalign 2.0
    ease 0.8 xalign StageCenter

transform _rest_exit_left_from_left:
    xalign StageLeft
    yalign 2.0
    ease 0.8 xalign -0.3

transform _rest_enter_from_left_to_left:
    xalign -0.3
    yalign 2.0
    ease 0.8 xalign StageLeft

transform _rest_tease_slide_down:
    xalign StageCenter
    yalign 2.0
    yoffset 0
    linear 0.4 yoffset 120

transform _rest_tease_slide_up:
    xalign StageCenter
    yalign 2.0
    yoffset 120
    linear 0.4 yoffset 0

transform _rest_tease_slide_down_left:
    xalign StageLeft
    yalign 2.0
    yoffset 0
    linear 0.4 yoffset 120

transform _rest_tease_slide_up_left:
    xalign StageLeft
    yalign 2.0
    yoffset 120
    linear 0.4 yoffset 0

init python:

    # ── Gate Thresholds ────────────────────────────────────
    RESTAURANT_GATES = {
        "solo_love": 250,
        "group_love": 150,
        "bf_loyalty_block_solo": 700,
        "bf_loyalty_block_group": 900,
        "lesbian_obed_solo": 300,
        "lesbian_obed_group": 150,
        "lesbian_proof_solo": 20,
        "lesbian_proof_group": 10,
        "girl_like_min": 300,
        "ask_pay_obed": 600,
        "plus1_girl_like_romantic": 550,
        "plus1_girl_like_friends": 300,
        "plus1_gf_extra": 100,
        "surprise_girl_like": 350,
        "surprise_gf_girl_like": 500,
        "surprise_gf_obed_override": 500,
        "refused_love_penalty": -15,
        "surprise_love_penalty": -10,
    }

    RESTAURANT_TRAIT_MODS = {
        "loyal": 150,
        "cheater": -100,
        "public_shy": 50,
        "exhibitionist": -50,
    }

    # ── Menu Items (food only) ─────────────────────────────
    RESTAURANT_MENU = {
        "steak":   {"price": 40, "label": _("Steak"),   "quality": 3},
        "pasta":   {"price": 25, "label": _("Pasta"),   "quality": 2},
        "chicken": {"price": 18, "label": _("Chicken"), "quality": 2},
        "salad":   {"price": 12, "label": _("Salad"),   "quality": 1},
    }

    # ── Payment Outcomes ───────────────────────────────────
    RESTAURANT_PAYMENT = {
        "player_pays": {"Love": 5},
        "split":       {},
        "ask_her":     {"Love": -10, "Obed": 3},
        "ask_rich":    {"Love": -5, "Obed": 3},
        "ask_poor":    {"Love": -25},
        "ask_witness": {"Love": -5},
        "cant_afford": {"Love": -15},
    }

    # ── Date Outcome Thresholds (score 0-10) ──────────────
    RESTAURANT_OUTCOMES = {"good": 7, "medium": 4}

    def _gs_meets_threshold(g):
        hist = _sleepover_history_level(g)
        bonus = [0, 50, 150, 250][min(hist, 3)]
        return (g.Love + bonus) >= 300

    # ── Date Events (fire after interactions, before payment) ──
    # Each entry: (label_suffix, base_pct, condition_func)
    # Final pct = base + modifiers from stats/traits/experience
    RESTAURANT_EVENTS = [
        ("event_bj_waitress", 8, lambda g: g.Sex_acts.get("bj", 0) > 0 and (not _is_on_cheat_path(g) or _cheat_can_sex(g))),
        ("event_bj_peek", 8, lambda g: g.Sex_acts.get("bj", 0) > 0 and (not _is_on_cheat_path(g) or _cheat_can_sex(g))),
        ("event_restroom", 8, lambda g: g.Sex_acts.get("bj", 0) > 0 and (not _is_on_cheat_path(g) or _cheat_can_sex(g))),
        ("event_footjob_tease", 8, lambda g: g.Sex_acts.get("tj", 0) > 0 and (not _is_on_cheat_path(g) or _cheat_can_sex(g))),
    ]

    def _rest_solo_modifier(girl, lbl):
        mod = 0
        mod += girl.Lust // 25
        if girl.Love >= 700:
            mod += 2
        elif girl.Love >= 400:
            mod += 1
        if girl.has_trait("public_fetish"):
            mod += 4
        if girl.has_trait("public_shy"):
            mod -= 4
        if girl.has_trait("exhibitionist"):
            mod += 2
        if girl.has_trait("hardcore_sex") and lbl in ("event_restroom", "event_bj_waitress"):
            mod += 2
        if lbl in ("event_bj_waitress", "event_bj_peek", "event_restroom"):
            bj_ct = girl.Sex_acts.get("bj", 0)
            if bj_ct >= 5:
                mod += 3
            elif bj_ct >= 3:
                mod += 1
        elif lbl == "event_footjob_tease":
            tj_ct = girl.Sex_acts.get("tj", 0)
            if tj_ct >= 4:
                mod += 2
            elif tj_ct >= 2:
                mod += 1
        return mod

    def _rest_pick_event(girl):
        """Roll for a random solo date event. Returns label suffix or None."""
        available = []
        for lbl, base_pct, cond in RESTAURANT_EVENTS:
            if cond(girl):
                pct = max(3, base_pct + _rest_solo_modifier(girl, lbl))
                available.append((lbl, pct))
                print("[RESTAURANT] Solo candidate %s: %d%% for %s" % (lbl, pct, girl.gid))
        if not available:
            return None
        roll = renpy.random.randint(1, 100)
        acc = 0
        for lbl, pct in available:
            acc += pct
            if roll <= acc:
                print("[RESTAURANT] Solo event picked: %s (roll=%d)" % (lbl, roll))
                return lbl
        print("[RESTAURANT] No solo event triggered (roll=%d, total_pct=%d)" % (roll, acc))
        return None

    # ── Group Date Events (2 girls) ──────────────────────
    # condition_func(girls) receives the full list
    # double_footjob/double_bj: blocked when GF present
    # sneaky_bj: allowed with GF (only group event that is)
    RESTAURANT_EVENTS_GROUP = [
        ("event_double_footjob", 8, lambda gs: (
            any(g.Sex_acts.get("tj", 0) > 0 and not g.has_trait("lesbian") for g in gs)
            and not any(g.is_dating_player() and not all(is_harem_exempt(g, o) for o in gs if o is not g) for g in gs)
            and all(not _is_on_cheat_path(g) or _cheat_can_sex(g) for g in gs)
        )),
        ("event_double_bj", 8, lambda gs: (
            any(g.Sex_acts.get("bj", 0) > 0 and not g.has_trait("lesbian") for g in gs)
            and not any(g.is_dating_player() and not all(is_harem_exempt(g, o) for o in gs if o is not g) for g in gs)
            and all(not _is_on_cheat_path(g) or _cheat_can_sex(g) for g in gs)
        )),
        ("event_sneaky_bj", 8, lambda gs: (
            any(g.Sex_acts.get("bj", 0) > 0 and not g.has_trait("lesbian") for g in gs)
            and all(not _is_on_cheat_path(g) or _cheat_can_sex(g) for g in gs)
        )),
    ]

    def _rest_group_modifier(girls, lbl):
        mod = 0
        for g in girls:
            mod += g.Lust // 30
            if g.Love >= 700:
                mod += 1
            if g.has_trait("public_fetish"):
                mod += 3
            if g.has_trait("public_shy"):
                mod -= 3
            if g.has_trait("exhibitionist"):
                mod += 1
            if g.has_trait("voyeur") and lbl in ("event_double_footjob", "event_double_bj"):
                mod += 2
        if lbl == "event_sneaky_bj":
            gf = next((g for g in girls if g.is_dating_player()), None)
            if gf:
                non_gf = [g for g in girls if g != gf]
                if non_gf and non_gf[0].has_trait("cheater"):
                    mod += 5
            elif any(g.has_trait("cheater") for g in girls):
                mod += 3
        if lbl == "event_double_bj" and any(g.Sex_acts.get("bj", 0) >= 5 for g in girls):
            mod += 2
        if lbl == "event_double_footjob" and any(g.Sex_acts.get("tj", 0) >= 3 for g in girls):
            mod += 2
        return mod

    def _rest_pick_group_event(girls):
        """Roll for a random group date event. Returns label suffix or None."""
        available = []
        for lbl, base_pct, cond in RESTAURANT_EVENTS_GROUP:
            if cond(girls):
                pct = max(3, base_pct + _rest_group_modifier(girls, lbl))
                available.append((lbl, pct))
                print("[RESTAURANT] Group candidate %s: %d%%" % (lbl, pct))
        if not available:
            return None
        roll = renpy.random.randint(1, 100)
        acc = 0
        for lbl, pct in available:
            acc += pct
            if roll <= acc:
                print("[RESTAURANT] Group event picked: %s (roll=%d)" % (lbl, roll))
                return lbl
        print("[RESTAURANT] No group event triggered (roll=%d, total_pct=%d)" % (roll, acc))
        return None

    # ── Attention / Jealousy (2-girl dates) ─────────────
    def _rest_check_jealousy(girls, attention):
        if len(girls) < 2:
            return (None, "none")
        g1, g2 = girls[0], girls[1]
        a1 = attention.get(g1.gid, 0)
        a2 = attention.get(g2.gid, 0)
        if a1 == a2:
            return (None, "none")
        neglected = g2 if a1 > a2 else g1
        favored = g1 if a1 > a2 else g2
        imbalance = abs(a1 - a2)
        tolerance = 2
        like = int(neglected.Girl_like.get(favored.gid, 500))
        if like >= 750:
            tolerance += 1
        if like < 250:
            tolerance -= 1
        if neglected.is_dating_player() and not (neglected.has_trait("polyamorous") or is_harem_exempt(neglected, favored)):
            tolerance -= 1
        if neglected.has_trait("loyal"):
            tolerance -= 1
        if neglected.has_trait("cheater"):
            tolerance += 1
        tolerance = max(1, tolerance)
        if imbalance >= tolerance + 1:
            return (neglected, "angry")
        elif imbalance >= tolerance:
            return (neglected, "mild")
        return (None, "none")

    # ═══════════════════════════════════════════════════════
    # FOOD PREFERENCE SYSTEM
    # Each girl: 1 favorite, 1 hated, rest neutral
    # Randomized once per playthrough
    # ═══════════════════════════════════════════════════════

    def _rest_init_food_prefs():
        """Sync food preferences dict from Girl attributes (old-save compat)."""
        if store._rest_food_prefs:
            return
        for _g in ALL_GIRLS:
            _fav = getattr(_g, "FavoriteDish", None)
            _hate = getattr(_g, "HatedDish", None)
            if _fav and _hate:
                store._rest_food_prefs[_g.gid] = {"loves": _fav, "hates": _hate}
            else:
                roll_girl_tastes(_g, drink=False)          # an old save that never rolled them: the ONE roll (characters_stats)
                store._rest_food_prefs[_g.gid] = {"loves": _g.FavoriteDish, "hates": _g.HatedDish}
            debug_log("[RESTAURANT] %s food prefs: loves=%s hates=%s" % (_g.gid, store._rest_food_prefs[_g.gid]["loves"], store._rest_food_prefs[_g.gid]["hates"]))

    def _rest_food_reaction(girl, food_item):
        """Returns 'loves', 'hates', or 'neutral' for a food item."""
        _fav = getattr(girl, "FavoriteDish", None)
        _hate = getattr(girl, "HatedDish", None)
        if _fav and _hate:
            if food_item == _fav:
                return "loves"
            elif food_item == _hate:
                return "hates"
            return "neutral"
        prefs = store._rest_food_prefs.get(girl.gid, {})
        if food_item == prefs.get("loves"):
            return "loves"
        elif food_item == prefs.get("hates"):
            return "hates"
        return "neutral"

    # ── Food Hint Pools (girl reacts to player's order) ───
    _REST_FOOD_HINTS = {
        "steak": {
            "loves": [
                _("Ooh, steak? That's my favorite too. Great taste."),
                _("I love a good steak. You and me think alike."),
                _("A man who orders steak. I already like you more."),
                _("Yes! Steak is the only right answer here."),
            ],
            "hates": [
                _("Red meat? I can't handle that... I prefer lighter food."),
                _("Steak is a bit too heavy for me, but you enjoy it."),
                _("I'll pass on the red meat, but you go ahead."),
                _("Not my thing, but at least you know what you want."),
            ],
            "neutral": [
                _("Nice pick. Can't go wrong with steak."),
                _("Solid choice."),
                _("Steak it is. Pretty safe bet."),
                _("Good pick. I was thinking about that too."),
            ],
        },
        "pasta": {
            "loves": [
                _("Pasta! Carbonara is always a great decision."),
                _("I could eat pasta every single day. Good choice."),
                _("Now you're speaking my language. Pasta is life."),
                _("Great minds think alike. Pasta all the way."),
            ],
            "hates": [
                _("Pasta always makes me feel so bloated... not for me."),
                _("I'm not really a pasta person, but go for it."),
                _("Too heavy for me. I need something lighter."),
                _("Carbs at night? Brave choice. Not for me though."),
            ],
            "neutral": [
                _("Classic choice. Can't go wrong."),
                _("Sounds good!"),
                _("Pasta is always a decent option."),
                _("Not bad. Simple and filling."),
            ],
        },
        "chicken": {
            "loves": [
                _("Chicken! I love it. Always a safe bet."),
                _("Good choice. I'm a chicken girl myself."),
                _("Chicken is underrated. Great pick."),
                _("I was hoping you'd pick that. Love chicken."),
            ],
            "hates": [
                _("I've been off chicken lately... something about the texture."),
                _("Chicken? Eh... I prefer other things. But you do you."),
                _("Not my favorite. I find it kind of bland."),
                _("Chicken again? I had it yesterday. But sure."),
            ],
            "neutral": [
                _("Nice, classic dinner choice."),
                _("That works. Simple and good."),
                _("Can't really go wrong with chicken."),
                _("Reasonable choice. Plays it safe."),
            ],
        },
        "salad": {
            "loves": [
                _("Oh, I love a good salad. Fresh and light!"),
                _("Salad? Me too! Healthy and delicious."),
                _("Smart choice. Light and refreshing."),
                _("I respect that. Keeping it healthy."),
            ],
            "hates": [
                _("Salad? That's not really dinner to me..."),
                _("I need something more filling than salad, personally."),
                _("A salad? For dinner? That's bold."),
                _("I'd be starving after a salad. But hey, your call."),
            ],
            "neutral": [
                _("Going healthy tonight? Nice."),
                _("Light dinner, huh? Not bad."),
                _("Salad works. Nothing wrong with that."),
                _("Interesting pick. Not what I expected."),
            ],
        },
    }

    # ── Girl reacts to player ordering for her ────────────
    _REST_ORDER_FOR_HER = {
        "loves": [
            _("You know me so well! That's exactly what I wanted."),
            _("How did you know? That's my favorite!"),
        ],
        "hates": [
            _("Oh... that's... not really my thing."),
            _("I appreciate the thought, but I don't like that..."),
        ],
        "neutral": [
            _("Sure, that works for me."),
            _("Sounds good. Thanks for ordering."),
        ],
    }

    _REST_LET_HER_CHOOSE = [
        _("I'll have the %s, please."),
        _("Hmm... I'll go with the %s."),
    ]

    # ═══════════════════════════════════════════════════════
    # COMPLIMENT SYSTEM (uses COMPLIMENT_OPTIONS from dialogue_bank)
    # ═══════════════════════════════════════════════════════

    _REST_COMPLIMENT_REACT = {
        "liked": [
            _("Aw... that's really sweet. Thank you."),
            _("Stop it... you're making me blush."),
            _("That means a lot. Really."),
        ],
        "neutral": [
            _("Oh... thanks, I guess."),
            _("That's nice of you."),
            _("Hmm, sure. Thanks."),
        ],
        "disliked": [
            _("That's a bit much..."),
            _("I don't really know how to respond to that."),
            _("Can we just eat? That was weird."),
        ],
    }

    def _rest_compliment_result(girl, kind):
        """Returns 'liked' (+2), 'neutral' (0), or 'disliked' (-1) based on compliment kind."""
        love = getattr(girl, "Love", 0)
        lust = getattr(girl, "Lust", 0)
        tempt = getattr(girl, "Temptation", 0)

        if kind == "safe":
            if love >= 300:
                return "liked"
            elif love < 100:
                return "disliked"
            return "neutral"
        else:  # lewd
            if love >= 500 or lust >= 40 or tempt >= 5:
                return "liked"
            elif love < 200:
                return "disliked"
            return "neutral"

    _REST_COMPLIMENT_SCORES = {"liked": 2, "neutral": 0, "disliked": -1}

    # ═══════════════════════════════════════════════════════
    # OTHER DIALOGUE POOLS
    # ═══════════════════════════════════════════════════════

    _REST_INVITE_ACCEPT = [
        _("Sure! I'd love to."),
        _("Sounds nice. What time?"),
        _("Dinner? Yeah, I'm in!"),
        _("Ooh, fancy. Pick me up later?"),
    ]

    _REST_INVITE_DECLINE = [
        _("Dinner? I don't think so... not tonight."),
        _("Sorry, I'm not really up for it."),
        _("Maybe some other time?"),
    ]

    _REST_INVITE_BF_DECLINE = [
        _("I can't... my %s would find out."),
        _("That's too risky. %s might see us."),
        _("I shouldn't... you know I'm with someone."),
    ]

    _REST_INVITE_FRIENDS_ACCEPT = [
        _("As friends? Sure, I could eat."),
        _("Okay, just dinner. Nothing weird."),
        _("I guess that's fine. I am hungry."),
    ]

    _REST_INVITE_FRIENDS_DECLINE = [
        _("Even as friends... I don't think so."),
        _("No, sorry. Not today."),
    ]

    _REST_INVITE_ACCEPT_ADD = [
        _("Sounds fun! Count me in."),
        _("Dinner with you guys? Sure!"),
        _("Yeah, I could go for that. See you tonight!"),
    ]

    _REST_INVITE_ADD_DECLINE = [
        _("Thanks, but I'm busy tonight."),
        _("I'll pass on dinner. Have fun though!"),
        _("Not tonight, maybe next time."),
    ]

    _REST_ARRIVAL = [
        _("Hey! Glad you could make it."),
        _("There you are. Ready to go?"),
        _("I'm starving. Let's go!"),
    ]

    # ── Double Date: +1 Mention ──────────────────────────
    _REST_PLUS1_ACCEPT = [
        _("Sure, I don't mind! Bring her along."),
        _("Yeah, she's cool. The more the merrier."),
        _("That's fine with me. Could be fun!"),
    ]

    _REST_PLUS1_REFUSE = [
        _("I'd rather it just be us tonight."),
        _("Hmm... I'm not really in the mood for a group thing."),
        _("Can we just keep it between you and me?"),
    ]

    _REST_PLUS1_DISAPPOINTED = [
        _("Oh... I thought it was going to be just us."),
        _("Wait, you want to bring someone else? I thought this was a date."),
        _("Really? I was kind of looking forward to it being just you and me."),
    ]

    _REST_PLUS1_ROMANTIC_ACCEPT = [
        _("I guess that's fine... if you want."),
        _("Sure, whatever. Bring her along."),
        _("Okay... I guess it could still be fun."),
    ]

    # ── Double Date: Campus Surprise ─────────────────────
    _REST_SURPRISE_OK = [
        _("Oh, %s is here too? That's cool, I don't mind."),
        _("Hey, %s! Didn't know you were coming. Fun!"),
    ]

    _REST_SURPRISE_CANCEL = [
        _("Wait... %s is coming too? Nobody told me about this."),
        _("I didn't sign up for this. I'm going back to my room."),
    ]

    _REST_SURPRISE_CANCEL_GF = [
        _("You invited another girl without telling me? Seriously?"),
        _("I'm your girlfriend. You should have asked me first."),
    ]

    _REST_BETRAYAL_CANCEL = [
        _("I told you I didn't want her here. I'm leaving."),
        _("Are you serious right now? I said no. Forget dinner."),
        _("You did this on purpose. I'm done."),
    ]

    _REST_SOLO_FALLBACK = [
        _("Well... looks like it's just us then."),
        _("I guess she didn't want to stay. More food for us?"),
    ]

    _REST_CHAT_REACT = [
        _("Ha, that's funny. Tell me more."),
        _("Really? I didn't know that about you."),
        _("I'm having a good time tonight."),
    ]

    _REST_JEALOUSY_MILD = [
        _("Am I invisible or something?"),
        _("Hey, I'm here too, you know."),
        _("You've been ignoring me this whole time."),
    ]

    _REST_JEALOUSY_ANGRY = [
        _("Fine, I'll just sit here then."),
        _("Why did you even invite me if you're only going to talk to her?"),
        _("This is getting awkward. You clearly prefer her company."),
    ]

    _REST_FJ_STOP = [
        _("Stop that. This isn't the place for this."),
        _("Seriously? Cut it out, both of you."),
        _("That's disgusting. Stop it right now."),
    ]

    # ── FJ Watch Reactions (trait-specific) ──
    _REST_FJ_WATCH_LESBIAN = [
        _("This is so wrong... but I can't look away."),
        _("I don't want any part of this. But... wow."),
        _("You two are disgusting. ...Don't stop on my account."),
    ]

    _REST_FJ_WATCH_SHY = [
        _("Oh my god, we're in PUBLIC! What if someone sees?!"),
        _("I can't believe you're doing this here..."),
        _("This is insane. We're in a restaurant!"),
    ]

    _REST_FJ_WATCH_VOYEUR = [
        _("Oh, don't mind me. I'm enjoying the show."),
        _("Mm. Interesting technique."),
        _("Keep going. I'm just... taking notes."),
    ]

    _REST_FJ_WATCH_DEFAULT = [
        _("You two are insane..."),
        _("I can't believe this is happening right now."),
        _("Seriously? Under the table? In a restaurant?"),
    ]

    def _rest_fj_pick_watch_line(girl):
        """Pick a trait-specific watch line and expression for the FJ observer."""
        if girl.has_trait("lesbian"):
            return renpy.random.choice(_REST_FJ_WATCH_LESBIAN), "uncomfortable", True
        elif girl.has_trait("public_shy"):
            return renpy.random.choice(_REST_FJ_WATCH_SHY), "shy", True
        elif girl.has_trait("voyeur"):
            return renpy.random.choice(_REST_FJ_WATCH_VOYEUR), "smug", False
        else:
            return renpy.random.choice(_REST_FJ_WATCH_DEFAULT), "uncomfortable", True

    # ── BJ Watch Reactions (trait-specific) ──
    _REST_BJ_WATCH_LESBIAN = [
        _("She's... under the table? With a guy? I can't even process this."),
        _("I would never do that. But she looks like she's having fun..."),
        _("This is humiliating to watch. ...So why can't I stop?"),
    ]

    _REST_BJ_WATCH_SHY = [
        _("She just went UNDER THE TABLE?! In a restaurant?!"),
        _("Oh my god... I can hear it... please tell me no one else can."),
        _("I'm going to pretend I don't know what's happening down there."),
    ]

    _REST_BJ_WATCH_VOYEUR = [
        _("Well, someone's hungry for dessert."),
        _("Lucky girl. Getting the best seat in the house."),
        _("Don't rush her. I want to see how long you last."),
    ]

    _REST_BJ_WATCH_DEFAULT = [
        _("She really just... went under the table. Okay then."),
        _("I'm just going to drink my wine and pretend this is normal."),
        _("You two have zero shame. Zero."),
    ]

    _REST_BJ_WATCH_GF = [
        _("Wait... is she doing what I think she's doing? Under there?"),
        _("I'll just... sit here. And not think about what's happening."),
        _("Your girlfriend is bold. I'll give her that."),
    ]

    _REST_BJ_JOIN = [
        _("Move over. There's room for two down there."),
        _("If she's going down... I'm not staying up here alone."),
        _("I can't just sit here and watch. Let me help."),
    ]

    _REST_BJ_STOP = [
        _("Are you serious right now? She's under the table in a RESTAURANT?"),
        _("No. Stop. Both of you. This is disgusting."),
        _("I'm not sitting here while she does THAT. Get her up."),
    ]

    def _rest_bj_pick_watch_line(girl, is_gf_scene):
        """Pick a trait-specific watch line and expression for the BJ observer."""
        if is_gf_scene:
            return renpy.random.choice(_REST_BJ_WATCH_GF), "uncomfortable", True
        elif girl.has_trait("lesbian"):
            return renpy.random.choice(_REST_BJ_WATCH_LESBIAN), "uncomfortable", True
        elif girl.has_trait("public_shy"):
            return renpy.random.choice(_REST_BJ_WATCH_SHY), "shy", True
        elif girl.has_trait("voyeur"):
            return renpy.random.choice(_REST_BJ_WATCH_VOYEUR), "smug", False
        else:
            return renpy.random.choice(_REST_BJ_WATCH_DEFAULT), "uncomfortable", True

    # ── Sneaky BJ: Girl B excuse lines when Girl A returns ──
    _REST_SNEAKY_EXCUSE_MOUTH = [
        _("Oops, I got some sauce on me. This pasta sauce is really thick."),
        _("Ugh, I spilled my drink. That pina colada was really good though."),
        _("Stupid straw splashed on me. These cocktails are messy."),
    ]

    _REST_SNEAKY_EXCUSE_FACE = [
        _("I... uh... the dessert cream splashed on me. It's nothing."),
        _("The waiter bumped into me and... sauce went everywhere. It's fine."),
        _("I sneezed while eating. It's just... food. Don't worry about it."),
    ]

    _REST_SNEAKY_FACE_NOTICED = [
        _("What is THAT on your face?! That's not sauce..."),
        _("Why is there... oh my god. Is that what I think it is?"),
        _("Your face... that's not food. What happened while I was gone?"),
    ]

    _REST_SNEAKY_FACE_NOTICED_GF = [
        _("What the HELL is on her face?! What did you do while I was in the bathroom?!"),
        _("That's not sauce. I know what that is. What's going on here?"),
        _("I was gone for two minutes and she has... THAT on her face?! Are you kidding me?!"),
    ]

    _REST_SNEAKY_MOUTH_NOTICED = [
        _("Your lips look... weird. Are you sure that's just a drink?"),
        _("There's something on the corner of your mouth... what is that?"),
    ]

    _REST_SNEAKY_MOUTH_NOT_NOTICED = [
        _("Okay, I'm back. What did I miss?"),
        _("Sorry about that. So, where were we?"),
        _("Found my phone! Now, what were you two talking about?"),
    ]

    # ── Sneaky BJ: Cleanup narration by trait and cum type ──
    _REST_SNEAKY_CLEANUP = {
        ("face", "cum_slut"): [
            _("%s scoops the mess off her cheek with her finger and licks it clean, smiling."),
            _("%s wipes her face with her finger and puts it in her mouth, savoring every drop."),
        ],
        ("face", "hate_cum"): [
            _("%s grabs a napkin and scrubs her face furiously, barely hiding her disgust."),
            _("%s frantically wipes her face with a napkin, grimacing the entire time."),
        ],
        ("face", "public_shy"): [
            _("%s blushes deeply and nervously dabs at her face with a napkin, avoiding eye contact."),
        ],
        ("face", "default"): [
            _("%s grabs a napkin and quickly wipes her face clean."),
            _("%s wipes her face with a napkin and checks her reflection in a spoon."),
        ],
        ("mouth", "cum_slut"): [
            _("%s runs her tongue across her lips and swallows the rest with a satisfied look."),
            _("%s licks the corner of her mouth, savoring the taste."),
        ],
        ("mouth", "hate_cum"): [
            _("%s grabs her drink and takes a long sip, grimacing as she washes the taste away."),
            _("%s reaches for her water and rinses her mouth, trying to mask her discomfort."),
        ],
        ("mouth", "public_shy"): [
            _("%s swallows nervously and takes a long sip of her drink to wash it down, face bright red."),
        ],
        ("mouth", "default"): [
            _("%s dabs at her lips with a napkin and takes a sip of her drink."),
            _("%s wipes her mouth with a napkin, acting like nothing happened."),
        ],
    }

    def _rest_sneaky_cleanup(girl, cum_type):
        trait_key = "default"
        for tk in ("cum_slut", "hate_cum", "public_shy"):
            if girl.has_trait(tk):
                trait_key = tk
                break
        key = (cum_type, trait_key)
        lines = _REST_SNEAKY_CLEANUP.get(key, _REST_SNEAKY_CLEANUP[(cum_type, "default")])
        line = _tl(renpy.random.choice(lines)) % girl.Name
        if trait_key == "cum_slut":
            expr, blush = "smug", 1
        elif trait_key == "hate_cum":
            expr, blush = "uncomfortable", 0
        elif trait_key == "public_shy":
            expr, blush = "shy", 2
        else:
            expr, blush = "normal", 0
        return line, expr, blush

    _REST_PAY_THANKS = [
        _("Thank you! That's really generous."),
        _("Aw, you didn't have to. Thanks."),
    ]

    _REST_PAY_SPLIT = [
        _("Fair enough. I'll cover my part."),
        _("Sure, that works."),
    ]

    _REST_PAY_UPSET = [
        _("Seriously? You're asking ME to pay?"),
        _("Wow. Classy."),
    ]

    _REST_PAY_RICH = [
        _("Fine. I'll get it. But don't make this a habit."),
        _("You're lucky I can afford it. Next time, bring your wallet."),
    ]

    _REST_PAY_POOR = [
        _("I... I was saving that money for the whole week."),
        _("Do you know how hard I worked for this? That was everything I had."),
    ]

    _REST_GOODBYE_GOOD = [
        _("I had an amazing time tonight."),
        _("We should do this again. Soon."),
        _("Tonight was really special."),
    ]

    _REST_GOODBYE_MED = [
        _("That was nice. Thanks for dinner."),
        _("See you around. Good night."),
    ]

    _REST_GOODBYE_OKAY = [
        _("Not bad for a weeknight dinner. Good night."),
        _("Thanks for dinner. See you tomorrow."),
        _("That was chill. Good night."),
    ]

    _REST_GOODBYE_BAD = [
        _("Well... that was something. Good night."),
        _("I think I'm just going to go. Bye."),
    ]

    # ── Afterglow Config ──────────────────────────────────
    # Tier 0=bad, 1=ok (score>=medium), 2=great (score>=good)
    _AFTERGLOW_LOVE = {0: -5, 1: 3, 2: 5}
    _AFTERGLOW_TEMPT = {0: 0, 1: 1, 2: 2}
    _AFTERGLOW_HEAT = {0: 0, 1: 5, 2: 15}
    _AFTERGLOW_BONUS = {0: 0, 1: 30, 2: 60}

    # ── Post-Date Reaction Lines (trait-aware) ────────────
    _REST_REACTION_LINES = {
        "has_bf_good": [
            _("My %(pl)s never takes me anywhere this nice..."),
            _("I haven't felt this way in a long time. Not with %(po)s, at least."),
            _("Tonight made me realize what I've been missing."),
        ],
        "has_bf_medium": [
            _("That was nice. I needed a night out."),
            _("Thanks for tonight. It was a good change of pace."),
        ],
        "has_bf_okay": [
            _("I needed a night away from all that. Thanks."),
            _("Good food, good company. Can't complain."),
        ],
        "has_bf_bad": [
            _("Well... at least my %(pl)s would have picked a better place."),
        ],
        "lesbian_good": [
            _("I... didn't expect tonight to feel like this. With a guy."),
            _("You're... different from what I expected. I'll give you that."),
            _("Don't let this go to your head, but... that was nice."),
        ],
        "lesbian_medium": [
            _("That was... okay. For hanging out with a guy, I mean."),
            _("Not terrible, I guess. Don't read too much into it."),
        ],
        "lesbian_okay": [
            _("Alright, that wasn't bad. For a dinner with a guy."),
        ],
        "lesbian_bad": [
            _("Yeah... this is why I don't date guys."),
        ],
        "friend_good": [
            _("We should do this more often. I had a lot of fun."),
            _("I'm glad we're friends. Tonight was great."),
        ],
        "friend_medium": [
            _("That was a nice dinner. Good company."),
        ],
        "friend_okay": [
            _("We should grab food again sometime."),
        ],
        "solo_good": [
            _("Tonight was really special. I feel... different around you."),
            _("I keep thinking about how good tonight felt."),
            _("You really know how to make a girl feel special."),
        ],
        "solo_medium": [
            _("That was fun. We should do it again sometime."),
            _("Thanks for tonight. It was a nice evening."),
        ],
        "solo_okay": [
            _("The food was good, at least."),
            _("Maybe next time we can talk more."),
        ],
    }

    def _rest_get_reaction_context(girl, tier):
        """Determine which reaction pool to use based on girl traits, Love, and score tier."""
        _is_okay = (tier == 0 and store._rest_score >= 2)
        if tier >= 2:
            _quality = "good"
        elif tier >= 1:
            _quality = "medium"
        elif _is_okay:
            _quality = "okay"
        else:
            _quality = "bad"

        _is_friend = (girl.Love < 300 and not girl.is_dating_player())

        if girl.has_trait("lesbian"):
            if _quality == "bad" and _is_friend:
                return "lesbian_okay"
            return "lesbian_" + _quality
        if girl.has_npc_partner():
            if _quality == "bad" and _is_friend:
                return "has_bf_okay"
            return "has_bf_" + _quality
        if _is_friend or store._restaurant_mode == "group":
            return "friend_" + _quality if _quality != "bad" else "friend_okay"
        return "solo_" + _quality if _quality != "bad" else None

    # ═══════════════════════════════════════════════════════
    # HELPER FUNCTIONS
    # ═══════════════════════════════════════════════════════

    def restaurant_can_invite():
        """Check if dinner invite is available today (first or second girl).
        Invites only allowed before Evening (Morning/Midday) so the date
        triggers naturally when Evening begins."""
        if store.TimeIndex >= 2:
            return False
        if getattr(store, "_restaurant_day", -1) != store.Day:
            return True
        return len(store._restaurant_girls) == 1

    def restaurant_too_late():
        if getattr(store, "_restaurant_day", -1) == store.Day:
            return False
        return store.TimeIndex >= 2

    def restaurant_story_locked(girl, mode="solo"):
        """Her story locks this dinner, whatever her stats: the romantic date is the act "date" (the stepmom's
        last step), the friends dinner the act "outing" (going out with him). The decline sites speak her
        refusal with story_locked_line (never the generic pools)."""
        return story_act_locked(girl, "date" if mode == "solo" else "outing")

    def restaurant_girl_accepts(girl, mode="solo", other_girl=None):
        """Unified acceptance check for solo (romantic) and group (friends)."""
        if girl_is_away(girl):   # at her parents' giving birth: no dinner, whoever asks and however
            debug_log("[RESTAURANT] %s declines: away (giving birth)" % girl.gid)
            return False
        if restaurant_story_locked(girl, mode):
            debug_log("[RESTAURANT] %s declines: her story locks the %s dinner (step %s)" % (
                girl.gid, mode, story_step_id(girl)))
            return False
        love = getattr(girl, "Love", 0)
        obed = getattr(girl, "Obed", 0)

        base_gate = RESTAURANT_GATES["solo_love"] if mode == "solo" else RESTAURANT_GATES["group_love"]
        for trait, mod in RESTAURANT_TRAIT_MODS.items():
            if trait in ("public_shy", "exhibitionist"):
                if girl.has_trait(trait):
                    base_gate += mod
            else:
                if girl.has_trait(trait) and girl.has_npc_partner():
                    base_gate += mod
        base_gate = max(50, base_gate)

        if girl.has_npc_partner():
            bf_loy = getattr(girl, "bf_loyalty", 0)
            _loy_key = "bf_loyalty_block_solo" if mode == "solo" else "bf_loyalty_block_group"
            _has_cheated = getattr(girl, "CheatMaxTier", 0) > 0
            _willing = getattr(girl, "CheatAttitude", 3) >= 5
            if bf_loy >= RESTAURANT_GATES[_loy_key] and not girl.has_trait("cheater") and not _has_cheated and not _willing:
                debug_log("[RESTAURANT] %s DECLINED (bf_loyalty %d >= %d [%s], no cheat history/attitude)" % (girl.gid, bf_loy, RESTAURANT_GATES[_loy_key], mode))
                return False

        if girl.has_trait("lesbian"):
            _obed_key = "lesbian_obed_solo" if mode == "solo" else "lesbian_obed_group"
            _proof_key = "lesbian_proof_solo" if mode == "solo" else "lesbian_proof_group"
            proof = lesbian_openness(girl)
            if obed < RESTAURANT_GATES[_obed_key] and proof < RESTAURANT_GATES[_proof_key]:
                debug_log("[RESTAURANT] %s DECLINED (lesbian, obed %d < %d, openness %d < %d [%s])" % (girl.gid, obed, RESTAURANT_GATES[_obed_key], proof, RESTAURANT_GATES[_proof_key], mode))
                return False

        if mode == "group" and other_girl:
            like = int(girl.Girl_like.get(other_girl.gid, 500))
            if like < RESTAURANT_GATES["girl_like_min"]:
                debug_log("[RESTAURANT] %s DECLINED (Girl_like for %s = %d < %d)" % (girl.gid, other_girl.gid, like, RESTAURANT_GATES["girl_like_min"]))
                return False
            _ensure_girl_knowledge(girl)
            if girl.knows_with_player.get(other_girl.gid):
                if girl.is_dating_player() and not girl.has_trait("cheater") and not (girl.has_trait("polyamorous") or is_harem_exempt(girl, other_girl)):
                    debug_log("[RESTAURANT] %s DECLINED (jealous of %s with player)" % (girl.gid, other_girl.gid))
                    return False

        result = love >= base_gate or obed >= base_gate
        debug_log("[RESTAURANT] %s accept=%s mode=%s (Love=%d Obed=%d gate=%d)" % (girl.gid, result, mode, love, obed, base_gate))
        return result

    def restaurant_calc_bill(orders):
        """Sum total cost from orders dict: {gid_or_player: menu_key}."""
        total = 0
        for key, item in orders.items():
            total += RESTAURANT_MENU.get(item, {}).get("price", 0)
        return total

    def _rest_add_score(points, reason=""):
        """Add points to date score, clamped 0-10."""
        _old = store._rest_score
        store._rest_score = max(0, min(10, store._rest_score + points))
        _tag = " (%s)" % reason if reason else ""
        print("[DATE SCORE] %+d%s | %d -> %d/10" % (points, _tag, _old, store._rest_score))

    def _rest_cleanup_vars():
        """Reset all restaurant tracking variables."""
        for _pg in getattr(store, "_restaurant_girls", []):
            _pg.loc = GIRLS_CONFIG.get(_pg.gid, {}).get("home", "campus")
            _pg.WearPreset("casual", apply_now=False)
        store._restaurant_day = -1
        store._restaurant_girls = []
        store._restaurant_orders = {}
        store._restaurant_bonus = 0
        store._restaurant_turn = 0
        store._rest_compliments_used = []
        store._restaurant_bg = None
        store._restaurant_invite_state = {}
        store._rest_attention = {}
        store._rest_date_girl = None
        store._in_event = False
        store._in_sandbox = True
        debug_log("[STATE] _in_event = False, _in_sandbox = True (restaurant cleanup)")

    # ═══════════════════════════════════════════════════════
    # DOUBLE DATE HELPERS
    # ═══════════════════════════════════════════════════════

    def restaurant_girl_already_invited(girl):
        # only TODAY's invite counts (a stale list from a cancelled group must not block)
        return getattr(store, "_restaurant_day", -1) == store.Day and girl in store._restaurant_girls

    def restaurant_dinner_full():
        return getattr(store, "_restaurant_day", -1) == store.Day and len(store._restaurant_girls) >= 2

    def restaurant_group_blocked(girl):
        # a taken girl will not join a GROUP dinner (hers or the invited girl's partner would hear of it)
        if getattr(store, "_restaurant_day", -1) != store.Day or not store._restaurant_girls:
            return False
        if girl.has_npc_partner():
            return True
        for g in store._restaurant_girls:
            if g.has_npc_partner():
                return True
        return False

    def _restaurant_init_invite(girl, source, warned_gid=None):
        store._restaurant_invite_state[girl.gid] = {
            "warned_about": warned_gid,
            "refused_plus1": None,
            "source": source,
        }
        debug_log("[RESTAURANT] Invite state for %s: source=%s warned=%s" % (girl.gid, source, warned_gid))

    def restaurant_plus1_check(girl, other_girl, mode="solo"):
        like = int(girl.Girl_like.get(other_girl.gid, 500))
        _key = "plus1_girl_like_romantic" if mode == "solo" else "plus1_girl_like_friends"
        threshold = RESTAURANT_GATES[_key]
        if girl.is_dating_player():
            threshold += RESTAURANT_GATES["plus1_gf_extra"]
        result = "accept" if like >= threshold else "refuse"
        debug_log("[RESTAURANT] +1 check: %s about %s mode=%s (like=%d threshold=%d) -> %s" % (girl.gid, other_girl.gid, mode, like, threshold, result))
        return result

    def restaurant_surprise_check(girl, other_girl):
        inv = store._restaurant_invite_state.get(girl.gid, {})

        if inv.get("refused_plus1") == other_girl.gid:
            debug_log("[RESTAURANT] Surprise: %s CANCEL (betrayal, refused %s)" % (girl.gid, other_girl.gid))
            return "cancel"

        if inv.get("warned_about") == other_girl.gid:
            debug_log("[RESTAURANT] Surprise: %s OK (warned about %s)" % (girl.gid, other_girl.gid))
            return "ok"

        like = int(girl.Girl_like.get(other_girl.gid, 500))

        if girl.is_dating_player():
            gf_threshold = RESTAURANT_GATES["surprise_gf_girl_like"]
            obed_override = RESTAURANT_GATES["surprise_gf_obed_override"]
            if like >= gf_threshold or girl.Obed >= obed_override:
                debug_log("[RESTAURANT] Surprise: %s (GF) OK (like=%d or Obed=%d)" % (girl.gid, like, girl.Obed))
                return "ok"
            debug_log("[RESTAURANT] Surprise: %s (GF) CANCEL (like=%d < %d, Obed=%d < %d)" % (girl.gid, like, gf_threshold, girl.Obed, obed_override))
            return "cancel"

        threshold = RESTAURANT_GATES["surprise_girl_like"]
        if like >= threshold:
            debug_log("[RESTAURANT] Surprise: %s OK (like=%d >= %d)" % (girl.gid, like, threshold))
            return "ok"
        debug_log("[RESTAURANT] Surprise: %s CANCEL (like=%d < %d)" % (girl.gid, like, threshold))
        return "cancel"

    def restaurant_get_other_girls(exclude_girl):
        result = []
        for g in ALL_GIRLS:
            if g.gid == exclude_girl.gid:
                continue
            if g in store._restaurant_girls:
                continue
            if not getattr(g, "enabled", True):
                continue
            if girl_is_away(g):
                continue
            result.append(g)
        return result

    def _rest_invite_reply(girl, accepted):
        """Her text answer to a phone dinner invite: accept pool, the "away" line (she is at her parents'
        giving birth), or the decline pool."""
        if accepted:
            return _tl(renpy.random.choice(_REST_INVITE_ACCEPT))
        if girl_is_away(girl):
            return _tl(renpy.random.choice(FOLLOW_INVITE_DECLINE["away"]))
        return _tl(renpy.random.choice(_REST_INVITE_DECLINE))


# ============================================================
# INVITATION LABELS
# ============================================================

# ── In-person invite (from talk_to_her_menu) ──
label restaurant_send_invite_inperson(girl):
    python:
        _rest_is_adding = (store._restaurant_day == store.Day and len(store._restaurant_girls) == 1)

    if _rest_is_adding:
        jump .inperson_add_second

    # ── First invite ──
    "You want to go to dinner with me tonight?"
    python:
        _rest_accepts = restaurant_girl_accepts(girl, "solo")

    if _rest_accepts:
        $ set_scene_expression(girl, "surprised")
        $ Say_Line(girl, _tl(renpy.random.choice(_REST_INVITE_ACCEPT)))
        $ set_scene_expression(girl, "happy")
        python:
            store._restaurant_day = store.Day
            store._restaurant_mode = "solo"
            store._restaurant_girls = [girl]
            _restaurant_init_invite(girl, "inperson")
            debug_log("[RESTAURANT] In-person solo date scheduled with %s" % girl.gid)

        $ _rest_others = [g for g in restaurant_get_other_girls(girl) if not restaurant_group_blocked(g)]
        if _rest_others:
            call .inperson_plus1_ask(girl, _rest_others, "solo") from _call_rest_inperson_plus1

        "She accepted. You'll meet up this evening."
    else:
        python:
            if restaurant_story_locked(girl, "solo"):
                # her story's no, in the voice of her step (never the generic decline)
                _rest_line = story_locked_line(girl, "date")
            elif girl.has_npc_partner() and getattr(girl, "bf_loyalty", 0) >= RESTAURANT_GATES.get("bf_loyalty_block_solo", 700):
                _npc = get_npc_partner_for(girl)
                _pl = getattr(_npc, "name", "them") if _npc else "them"
                _rest_line = _tl(renpy.random.choice(_REST_INVITE_BF_DECLINE))
                if "%s" in _rest_line:
                    _rest_line = _rest_line % _pl
            else:
                _rest_line = _tl(renpy.random.choice(_REST_INVITE_DECLINE))
        $ set_scene_expression(girl, "uncomfortable")
        $ Say_Line(girl, _rest_line)

        menu:
            "What about just as friends? No pressure.":
                "What about just as friends? No pressure."
                python:
                    _rest_friends_ok = restaurant_girl_accepts(girl, "group")
                if _rest_friends_ok:
                    $ set_scene_expression(girl, "normal")
                    $ Say_Line(girl, _tl(renpy.random.choice(_REST_INVITE_FRIENDS_ACCEPT)))
                    $ set_scene_expression(girl, "happy")
                    python:
                        store._restaurant_day = store.Day
                        store._restaurant_mode = "group"
                        store._restaurant_girls = [girl]
                        _restaurant_init_invite(girl, "inperson")
                        debug_log("[RESTAURANT] In-person friends dinner with %s (fallback)" % girl.gid)

                    $ _rest_others = [g for g in restaurant_get_other_girls(girl) if not restaurant_group_blocked(g)]
                    if _rest_others:
                        call .inperson_plus1_ask(girl, _rest_others, "group") from _call_rest_inperson_plus1_friends

                    "She agreed. You'll meet up this evening."
                else:
                    $ set_scene_expression(girl, "sad")
                    if restaurant_story_locked(girl, "group"):
                        $ Say_Line(girl, story_locked_line(girl, "outing"))
                    else:
                        $ Say_Line(girl, _tl(renpy.random.choice(_REST_INVITE_FRIENDS_DECLINE)))
            "Okay, never mind.":
                $ set_scene_expression(girl, "normal")
    return

    # ── Adding second girl to existing dinner (in-person) ──
    label .inperson_add_second:
        python:
            _rest_first = store._restaurant_girls[0]
            _rest_add_ok = restaurant_girl_accepts(girl, "group", _rest_first)
        PlayerChar "I'm having dinner with [_rest_first.Name] tonight. Want to come?"
        if _rest_add_ok:
            $ set_scene_expression(girl, "surprised")
            $ Say_Line(girl, _tl(renpy.random.choice(_REST_INVITE_ACCEPT_ADD)))
            $ set_scene_expression(girl, "happy")
            python:
                store._restaurant_girls.append(girl)
                store._restaurant_mode = "group"
                _restaurant_init_invite(girl, "inperson")
                debug_log("[RESTAURANT] In-person +1: %s added to dinner with %s" % (girl.gid, _rest_first.gid))
            "She accepted. You'll all meet up this evening."
        else:
            $ set_scene_expression(girl, "uncomfortable")
            if restaurant_story_locked(girl, "group"):
                $ Say_Line(girl, story_locked_line(girl, "outing"))
            else:
                $ Say_Line(girl, _tl(renpy.random.choice(_REST_INVITE_ADD_DECLINE)))
        return

    # ── +1 mention sub-flow (in-person) ──
    label .inperson_plus1_ask(girl, others, mode="solo"):
        python:
            _rest_p1_choices = []
            for _og in others:
                _rest_p1_choices.append((_og.Name, _og))
            # None-valued items render as unclickable captions, so the decline option needs a real sentinel
            _rest_p1_choices.append((_tl(_("No, just us tonight.")), "__none__"))
            _rest_plus1_target = renpy.display_menu(_rest_p1_choices)
            if _rest_plus1_target == "__none__":
                _rest_plus1_target = None

        if _rest_plus1_target is None:
            return

        "Would you mind if [_rest_plus1_target.Name] comes too?"

        python:
            _rest_p1_result = restaurant_plus1_check(girl, _rest_plus1_target, mode)
            store._restaurant_invite_state[girl.gid]["asked_plus1"] = True

        if mode == "solo":
            $ set_scene_expression(girl, "sad")
            $ Say_Line(girl, _tl(renpy.random.choice(_REST_PLUS1_DISAPPOINTED)))
            if _rest_p1_result == "accept":
                $ store._restaurant_invite_state[girl.gid]["warned_about"] = _rest_plus1_target.gid
                $ set_scene_expression(girl, "uncomfortable")
                $ Say_Line(girl, _tl(renpy.random.choice(_REST_PLUS1_ROMANTIC_ACCEPT)))
                $ set_scene_expression(girl, "normal")
            else:
                $ store._restaurant_invite_state[girl.gid]["refused_plus1"] = _rest_plus1_target.gid
                $ set_scene_expression(girl, "uncomfortable")
                $ Say_Line(girl, _tl(renpy.random.choice(_REST_PLUS1_REFUSE)))
                $ set_scene_expression(girl, "normal")
        else:
            if _rest_p1_result == "accept":
                $ store._restaurant_invite_state[girl.gid]["warned_about"] = _rest_plus1_target.gid
                $ set_scene_expression(girl, "happy")
                $ Say_Line(girl, _tl(renpy.random.choice(_REST_PLUS1_ACCEPT)))
                $ set_scene_expression(girl, "normal")
            else:
                $ store._restaurant_invite_state[girl.gid]["refused_plus1"] = _rest_plus1_target.gid
                $ set_scene_expression(girl, "uncomfortable")
                $ Say_Line(girl, _tl(renpy.random.choice(_REST_PLUS1_REFUSE)))
                $ set_scene_expression(girl, "normal")
        return


# ── Phone solo invite ──
label restaurant_send_solo_invite(girl):
    python:
        _rest_is_adding = (store._restaurant_day == store.Day and len(store._restaurant_girls) == 1)

    if _rest_is_adding:
        jump .phone_add_second

    # ── First invite ──
    python:
        phone_add_msg(girl.gid, "player", _tl(_("Hey, want to go to dinner with me tonight?")))
    call _phone_typing(girl) from _typing_rest_solo

    python:
        _rest_accepts = restaurant_girl_accepts(girl, "solo")

    if _rest_accepts:
        python:
            _rest_line = _tl(renpy.random.choice(_REST_INVITE_ACCEPT))
            phone_add_msg(girl.gid, girl.gid, _rest_line)
            phone_add_msg(girl.gid, "system", _tl(_("Dinner date scheduled for tonight!")), "system")
            store._restaurant_day = store.Day
            store._restaurant_mode = "solo"
            store._restaurant_girls = [girl]
            _restaurant_init_invite(girl, "phone")
            debug_log("[RESTAURANT] Solo date scheduled with %s" % girl.gid)
        return

    # ── She declined — show response + fallback choices on phone ──
    python:
        if restaurant_story_locked(girl, "solo"):
            # her story's no, in the voice of her step (never the generic decline)
            _rest_line = _tl(story_locked_line(girl, "date"))
        elif girl.has_npc_partner() and getattr(girl, "bf_loyalty", 0) >= RESTAURANT_GATES.get("bf_loyalty_block_solo", 700):
            _npc = get_npc_partner_for(girl)
            _pl = getattr(_npc, "name", "them") if _npc else "them"
            _rest_line = _tl(renpy.random.choice(_REST_INVITE_BF_DECLINE))
            if "%s" in _rest_line:
                _rest_line = _rest_line % _pl
        else:
            _rest_line = _tl(renpy.random.choice(_REST_INVITE_DECLINE))
        phone_add_msg(girl.gid, girl.gid, _rest_line)

    $ _rest_fallback = [(_("What about just as friends?"), "friends"), (_("Never mind"), "nevermind")]
    call screen phone_chat_screen(girl, choices=_rest_fallback)
    $ _rest_fb_pick = _return

    if _rest_fb_pick == "friends":
        python:
            phone_add_msg(girl.gid, "player", _tl(_("What about just as friends? No pressure.")))
        call _phone_typing(girl) from _typing_rest_friends
        python:
            _rest_friends_ok = restaurant_girl_accepts(girl, "group")
        if _rest_friends_ok:
            python:
                _rest_line = _tl(renpy.random.choice(_REST_INVITE_FRIENDS_ACCEPT))
                phone_add_msg(girl.gid, girl.gid, _rest_line)
                phone_add_msg(girl.gid, "system", _tl(_("Dinner scheduled for tonight (as friends).")), "system")
                store._restaurant_day = store.Day
                store._restaurant_mode = "group"
                store._restaurant_girls = [girl]
                _restaurant_init_invite(girl, "phone")
                debug_log("[RESTAURANT] Friends dinner scheduled with %s (fallback)" % girl.gid)
        else:
            python:
                if restaurant_story_locked(girl, "group"):
                    _rest_line = _tl(story_locked_line(girl, "outing"))
                else:
                    _rest_line = _tl(renpy.random.choice(_REST_INVITE_FRIENDS_DECLINE))
                phone_add_msg(girl.gid, girl.gid, _rest_line)
    else:
        python:
            phone_add_msg(girl.gid, "player", _tl(_("Okay, no worries.")))
    return

    # ── Adding second girl to existing dinner (phone) ──
    label .phone_add_second:
        python:
            _rest_first = store._restaurant_girls[0]
            phone_add_msg(girl.gid, "player", _tl(_("Hey! I'm having dinner with %s tonight, want to join?")) % _rest_first.Name)
        call _phone_typing(girl) from _typing_rest_add_second

        python:
            _rest_add_ok = restaurant_girl_accepts(girl, "group", _rest_first)

        if _rest_add_ok:
            python:
                _rest_line = _tl(renpy.random.choice(_REST_INVITE_ACCEPT_ADD))
                phone_add_msg(girl.gid, girl.gid, _rest_line)
                phone_add_msg(girl.gid, "system", _tl(_("She's joining dinner tonight!")), "system")
                store._restaurant_girls.append(girl)
                store._restaurant_mode = "group"
                _restaurant_init_invite(girl, "phone")
                debug_log("[RESTAURANT] Phone +1: %s added to dinner with %s" % (girl.gid, _rest_first.gid))
        else:
            python:
                if restaurant_story_locked(girl, "group"):
                    _rest_line = _tl(story_locked_line(girl, "outing"))
                else:
                    _rest_line = _tl(renpy.random.choice(_REST_INVITE_ADD_DECLINE))
                phone_add_msg(girl.gid, girl.gid, _rest_line)
        return

    # ── +1 mention sub-flow (phone) ──
    label .phone_plus1_ask(girl, others, mode="solo"):
        python:
            _rest_p1_choices = []
            for _og in others:
                _rest_p1_choices.append((_og.Name, _og))
            # None-valued items render as unclickable captions, so the decline option needs a real sentinel
            _rest_p1_choices.append((_tl(_("No, just us tonight.")), "__none__"))
            _rest_plus1_target = renpy.display_menu(_rest_p1_choices)
            if _rest_plus1_target == "__none__":
                _rest_plus1_target = None

        if _rest_plus1_target is None:
            return

        python:
            phone_add_msg(girl.gid, "player", _tl(_("Would you mind if %s comes too?")) % _rest_plus1_target.Name)
        call _phone_typing(girl) from _typing_rest_plus1

        python:
            _rest_p1_result = restaurant_plus1_check(girl, _rest_plus1_target, mode)
            store._restaurant_invite_state[girl.gid]["asked_plus1"] = True

        if mode == "solo":
            python:
                _rest_line = _tl(renpy.random.choice(_REST_PLUS1_DISAPPOINTED))
                phone_add_msg(girl.gid, girl.gid, _rest_line)
            if _rest_p1_result == "accept":
                python:
                    store._restaurant_invite_state[girl.gid]["warned_about"] = _rest_plus1_target.gid
                    _rest_line = _tl(renpy.random.choice(_REST_PLUS1_ROMANTIC_ACCEPT))
                    phone_add_msg(girl.gid, girl.gid, _rest_line)
            else:
                python:
                    store._restaurant_invite_state[girl.gid]["refused_plus1"] = _rest_plus1_target.gid
                    _rest_line = _tl(renpy.random.choice(_REST_PLUS1_REFUSE))
                    phone_add_msg(girl.gid, girl.gid, _rest_line)
        else:
            if _rest_p1_result == "accept":
                python:
                    store._restaurant_invite_state[girl.gid]["warned_about"] = _rest_plus1_target.gid
                    _rest_line = _tl(renpy.random.choice(_REST_PLUS1_ACCEPT))
                    phone_add_msg(girl.gid, girl.gid, _rest_line)
            else:
                python:
                    store._restaurant_invite_state[girl.gid]["refused_plus1"] = _rest_plus1_target.gid
                    _rest_line = _tl(renpy.random.choice(_REST_PLUS1_REFUSE))
                    phone_add_msg(girl.gid, girl.gid, _rest_line)
        return

    # ── Invite +1 girl directly (auto-sent after girl A agrees) ──
    label .phone_invite_plus1(first_girl, target_girl):
        python:
            phone_add_msg(target_girl.gid, "player", _tl(_("Hey! I invited %s for dinner tonight. Want to come too? It'll be fun.")) % first_girl.Name)
        call _phone_typing(target_girl) from _typing_rest_invite_p1

        python:
            _rest_p1_add_ok = restaurant_girl_accepts(target_girl, "group", first_girl)

        if _rest_p1_add_ok:
            python:
                _rest_line = _tl(renpy.random.choice(_REST_INVITE_ACCEPT_ADD))
                phone_add_msg(target_girl.gid, target_girl.gid, _rest_line)
                phone_add_msg(target_girl.gid, "system", _tl(_("She's joining dinner tonight!")), "system")
                store._restaurant_girls.append(target_girl)
                _restaurant_init_invite(target_girl, "phone")
                store._restaurant_invite_state[target_girl.gid]["warned_about"] = first_girl.gid
                debug_log("[RESTAURANT] Auto +1 invite: %s accepted (first=%s)" % (target_girl.gid, first_girl.gid))
        else:
            python:
                if restaurant_story_locked(target_girl, "group"):
                    _rest_line = _tl(story_locked_line(target_girl, "outing"))
                else:
                    _rest_line = _tl(renpy.random.choice(_REST_INVITE_ADD_DECLINE))
                phone_add_msg(target_girl.gid, target_girl.gid, _rest_line)
                store._restaurant_mode = "solo" if len(store._restaurant_girls) == 1 else "group"
                debug_log("[RESTAURANT] Auto +1 invite: %s declined" % target_girl.gid)
        return


label restaurant_send_group_invite(group):
    python:
        _rest_members = group["members"]
        _rest_g = []
        for _rgid in _rest_members:
            _rg = GIRL_BY_ID.get(_rgid)
            if _rg:
                _rest_g.append(_rg)

        if len(_rest_g) < 2:
            phone_group_add_msg(group["id"], "system", _("You need 2 members in the group for a dinner."), "system")
            renpy.jump("restaurant_send_group_invite.done")

        _rest_ga = _rest_g[0]
        _rest_gb = _rest_g[1]

        phone_group_add_msg(group["id"], "player",
            _tl(_("Hey girls! Want to grab dinner tonight? My treat.")), "text")

    call screen phone_group_chat_screen(group, auto_close=0.6)

    $ phone_group_add_msg(group["id"], _rest_ga.gid, None, "typing")
    call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.0, 1.8))
    python:
        _g_msgs = phone_group_get_msgs(group["id"])
        if _g_msgs and _g_msgs[-1].get("type") == "typing":
            _g_msgs.pop()
        _rest_a_ok = restaurant_girl_accepts(_rest_ga, "group", _rest_gb)
        _rest_a_line = _rest_invite_reply(_rest_ga, _rest_a_ok)
        phone_group_add_msg(group["id"], _rest_ga.gid, _rest_a_line, "text")
    call screen phone_group_chat_screen(group, auto_close=0.5)

    $ phone_group_add_msg(group["id"], _rest_gb.gid, None, "typing")
    call screen phone_group_chat_screen(group, auto_close=renpy.random.uniform(1.0, 1.8))
    python:
        _g_msgs = phone_group_get_msgs(group["id"])
        if _g_msgs and _g_msgs[-1].get("type") == "typing":
            _g_msgs.pop()
        _rest_b_ok = restaurant_girl_accepts(_rest_gb, "group", _rest_ga)
        _rest_b_line = _rest_invite_reply(_rest_gb, _rest_b_ok)
        phone_group_add_msg(group["id"], _rest_gb.gid, _rest_b_line, "text")
    call screen phone_group_chat_screen(group, auto_close=0.5)

    python:
        _rest_accepted = []
        if _rest_a_ok:
            _rest_accepted.append(_rest_ga)
        if _rest_b_ok:
            _rest_accepted.append(_rest_gb)

        if len(_rest_accepted) < 2:
            if len(_rest_accepted) == 0:
                phone_group_add_msg(group["id"], "system", _("Nobody's free tonight. Dinner cancelled."), "system")
            else:
                phone_group_add_msg(group["id"], "system",
                    _tl(_("Only %s accepted. You need both for a group dinner.")) % _rest_accepted[0].Name, "system")
            store._restaurant_day = -1
            store._restaurant_girls = []          # a dead group invite must not keep blocking the day
        else:
            store._restaurant_day = store.Day
            store._restaurant_mode = "group"
            store._restaurant_girls = _rest_accepted
            _restaurant_init_invite(_rest_ga, "group", warned_gid=_rest_gb.gid)
            _restaurant_init_invite(_rest_gb, "group", warned_gid=_rest_ga.gid)
            phone_group_add_msg(group["id"], "player", _tl(_("Awesome! See you tonight!")), "text")
            phone_group_add_msg(group["id"], "system", _("Dinner scheduled for tonight!"), "system")
            debug_log("[RESTAURANT] Group dinner scheduled: %s + %s" % (_rest_ga.gid, _rest_gb.gid))

    call screen phone_group_chat_screen(group, auto_close=0.8)

    label .done:
        return


# ============================================================
# EVENING CHECK: Called from Wait label
# ============================================================

label restaurant_date_check:
    if _restaurant_day != Day:
        return
    if TimeIndex != 2:
        return
    if not _restaurant_girls:
        $ store._restaurant_day = -1
        return

    if CurrentLocation != "campus":
        $ Narration(_tl(_("You remember you have dinner plans tonight. You should head to campus.")))
        $ navigate_to("campus", None)
        call Set_Scene(entry=False) from _call_rest_set_scene_nav

    call restaurant_date_event from _call_restaurant_date_event
    return


# ============================================================
# MAIN EVENT
# ============================================================

label restaurant_date_event:
    $ store._in_event = True
    $ store._in_sandbox = False
    $ debug_log("[RESTAURANT] Event starting. Mode=%s Girls=%s" % (_restaurant_mode, [g.gid for g in _restaurant_girls]))

    python:
        store._restaurant_bonus = 0
        store._restaurant_orders = {}
        store._restaurant_turn = 0
        store._rest_score = 0
        store._rest_compliments_used = []
        _rest_init_food_prefs()
        for _dg in _restaurant_girls:
            print("[DATE START] %s | Love=%d Lust=%d Tempt=%d | FavDish=%s HateDish=%s" % (_dg.gid, _dg.Love, _dg.Lust, _dg.Temptation, getattr(_dg, "FavoriteDish", "?"), getattr(_dg, "HatedDish", "?")))
            print("[DATE START] %s | Compliment thresholds: safe liked>=300 disliked<100 | lewd liked>=(Love500/Lust40/Tempt5) disliked<200" % _dg.gid)


    # Ensure date girls wear casual (not pool bikini from schedule)
    python:
        for _rg in _restaurant_girls:
            _rg.WearPreset("casual", apply_now=False)

    # Show campus evening BG + girl sprites for meeting
    $ store._restaurant_bg = "bg campus_evening"
    scene bg campus_evening
    with fade
    pause 0.3

    python:
        if len(_restaurant_girls) == 1:
            set_girl_sprite(_restaurant_girls[0].gid, pose="standing", at_list=[slot_center])
            set_scene_expression(_restaurant_girls[0], "happy")
        else:
            set_girl_sprite(_restaurant_girls[0].gid, pose="standing", at_list=[slot_left])
            set_girl_sprite(_restaurant_girls[1].gid, pose="standing", at_list=[slot_center])
            set_scene_expression(_restaurant_girls[0], "happy")
            set_scene_expression(_restaurant_girls[1], "happy")

    if len(_restaurant_girls) == 1:
        $ _rg = _restaurant_girls[0]
        $ Narration(_tl(_("That evening, you meet %s at the campus entrance.")) % _rg.Name)
        $ Say_Line(_rg, _tl(renpy.random.choice(_REST_ARRIVAL)))
    elif len(_restaurant_girls) == 2:
        call .campus_arrival_check from _call_rest_campus_check

        if not _restaurant_girls:
            $ Narration(_tl(_("Both of them left. Dinner is off tonight.")))
            jump .ending_cleanup
        elif len(_restaurant_girls) == 1:
            python:
                store._restaurant_mode = "solo"
                _rg = _restaurant_girls[0]
            $ Say_Line(_rg, _tl(renpy.random.choice(_REST_SOLO_FALLBACK)))

    $ Narration(_tl(_("You walk together to the restaurant.")))

    # Transition to restaurant BG + re-show sprites
    $ store._restaurant_bg = "bg restaurant"
    scene bg restaurant
    with fade
    show restaurant_table zorder 10
    pause 0.3

    python:
        if len(_restaurant_girls) == 1:
            set_girl_sprite(_restaurant_girls[0].gid, pose="standing", at_list=[slot_center])
            set_scene_expression(_restaurant_girls[0], "happy")
        else:
            set_girl_sprite(_restaurant_girls[0].gid, pose="standing", at_list=[slot_left])
            set_girl_sprite(_restaurant_girls[1].gid, pose="standing", at_list=[slot_center])
            set_scene_expression(_restaurant_girls[0], "happy")
            set_scene_expression(_restaurant_girls[1], "happy")

    $ Narration(_tl(_("You settle into your seats and open the menu.")))
    jump .ordering

    # ── CAMPUS ARRIVAL CHECK (double date) ──────────────
    label .campus_arrival_check:
        python:
            _ca_ga = _restaurant_girls[0]
            _ca_gb = _restaurant_girls[1]
            _ca_a_result = restaurant_surprise_check(_ca_ga, _ca_gb)
            _ca_b_result = restaurant_surprise_check(_ca_gb, _ca_ga)
            debug_log("[RESTAURANT] Campus check: %s=%s, %s=%s" % (_ca_ga.gid, _ca_a_result, _ca_gb.gid, _ca_b_result))

        $ Narration(_tl(_("That evening, you meet %s and %s at the campus entrance.")) % (_ca_ga.Name, _ca_gb.Name))

        # ── Girl A reaction ──
        if _ca_a_result == "cancel":
            python:
                _ca_a_inv = store._restaurant_invite_state.get(_ca_ga.gid, {})
                _ca_a_betrayed = (_ca_a_inv.get("refused_plus1") == _ca_gb.gid)
                _ca_a_is_gf = _ca_ga.is_dating_player()

            if _ca_a_betrayed:
                $ set_scene_expression(_ca_ga, "angry")
                $ Say_Line(_ca_ga, _tl(renpy.random.choice(_REST_BETRAYAL_CANCEL)))
                $ Change_Status(_ca_ga, "Love", RESTAURANT_GATES["refused_love_penalty"])
            elif _ca_a_is_gf:
                $ set_scene_expression(_ca_ga, "angry")
                $ Say_Line(_ca_ga, _tl(renpy.random.choice(_REST_SURPRISE_CANCEL_GF)))
                $ Change_Status(_ca_ga, "Love", RESTAURANT_GATES["surprise_love_penalty"])
            else:
                $ set_scene_expression(_ca_ga, "uncomfortable")
                $ Say_Line(_ca_ga, _tl(renpy.random.choice(_REST_SURPRISE_CANCEL)) % _ca_gb.Name)
                $ Change_Status(_ca_ga, "Love", RESTAURANT_GATES["surprise_love_penalty"])
            $ renpy.hide(_ca_ga.gid)
        elif _ca_a_result == "ok":
            python:
                _ca_a_inv = store._restaurant_invite_state.get(_ca_ga.gid, {})
                _ca_a_was_warned = (_ca_a_inv.get("warned_about") == _ca_gb.gid)
            if not _ca_a_was_warned:
                $ Say_Line(_ca_ga, _tl(renpy.random.choice(_REST_SURPRISE_OK)) % _ca_gb.Name)

        # ── Girl B reaction ──
        if _ca_b_result == "cancel":
            python:
                _ca_b_inv = store._restaurant_invite_state.get(_ca_gb.gid, {})
                _ca_b_betrayed = (_ca_b_inv.get("refused_plus1") == _ca_ga.gid)
                _ca_b_is_gf = _ca_gb.is_dating_player()

            if _ca_b_betrayed:
                $ set_scene_expression(_ca_gb, "angry")
                $ Say_Line(_ca_gb, _tl(renpy.random.choice(_REST_BETRAYAL_CANCEL)))
                $ Change_Status(_ca_gb, "Love", RESTAURANT_GATES["refused_love_penalty"])
            elif _ca_b_is_gf:
                $ set_scene_expression(_ca_gb, "angry")
                $ Say_Line(_ca_gb, _tl(renpy.random.choice(_REST_SURPRISE_CANCEL_GF)))
                $ Change_Status(_ca_gb, "Love", RESTAURANT_GATES["surprise_love_penalty"])
            else:
                $ set_scene_expression(_ca_gb, "uncomfortable")
                $ Say_Line(_ca_gb, _tl(renpy.random.choice(_REST_SURPRISE_CANCEL)) % _ca_ga.Name)
                $ Change_Status(_ca_gb, "Love", RESTAURANT_GATES["surprise_love_penalty"])
            $ renpy.hide(_ca_gb.gid)
        elif _ca_b_result == "ok":
            python:
                _ca_b_inv = store._restaurant_invite_state.get(_ca_gb.gid, {})
                _ca_b_was_warned = (_ca_b_inv.get("warned_about") == _ca_ga.gid)
            if not _ca_b_was_warned:
                $ Say_Line(_ca_gb, _tl(renpy.random.choice(_REST_SURPRISE_OK)) % _ca_ga.Name)

        # ── Update girls list based on who stayed ──
        python:
            _ca_stayed = []
            if _ca_a_result == "ok":
                _ca_stayed.append(_ca_ga)
            if _ca_b_result == "ok":
                _ca_stayed.append(_ca_gb)
            store._restaurant_girls = _ca_stayed
            debug_log("[RESTAURANT] Campus result: %d girl(s) stayed" % len(_ca_stayed))

            if len(_ca_stayed) == 1:
                set_girl_sprite(_ca_stayed[0].gid, pose="standing", at_list=[slot_center])
                set_scene_expression(_ca_stayed[0], "happy")
        return

    # ── ORDERING STEP 1: Player picks their food ──────────
    label .ordering:
        $ _rg = _restaurant_girls[0]
        $ Narration(_tl(_("What will you order?")))

        python:
            _lbl_steak = _tl(_("Steak"))
            _lbl_pasta = _tl(_("Pasta"))
            _lbl_chicken = _tl(_("Chicken"))
            _lbl_salad = _tl(_("Salad"))
            _pr_steak = RESTAURANT_MENU["steak"]["price"]
            _pr_pasta = RESTAURANT_MENU["pasta"]["price"]
            _pr_chicken = RESTAURANT_MENU["chicken"]["price"]
            _pr_salad = RESTAURANT_MENU["salad"]["price"]

        menu:
            "[_lbl_steak] ($[_pr_steak])" if Player.cash >= _pr_steak:
                $ _restaurant_orders["player"] = "steak"
            "[_lbl_pasta] ($[_pr_pasta])" if Player.cash >= _pr_pasta:
                $ _restaurant_orders["player"] = "pasta"
            "[_lbl_chicken] ($[_pr_chicken])" if Player.cash >= _pr_chicken:
                $ _restaurant_orders["player"] = "chicken"
            "[_lbl_salad] ($[_pr_salad])" if Player.cash >= _pr_salad:
                $ _restaurant_orders["player"] = "salad"

        # Each girl reacts to player's choice (hint about her preferences)
        $ _player_food = _restaurant_orders["player"]
        $ _rest_hint_idx = 0
        $ _rest_last_hint = ""
        jump .player_food_reaction

    label .player_food_reaction:
        python:
            _rg = _restaurant_girls[_rest_hint_idx]
            _hint_reaction = _rest_food_reaction(_rg, _player_food)
            _hint_pool = list(_REST_FOOD_HINTS[_player_food][_hint_reaction])
            if _rest_last_hint in _hint_pool and len(_hint_pool) > 1:
                _hint_pool.remove(_rest_last_hint)
            _rest_last_hint = renpy.random.choice(_hint_pool)
            _hint_line = _tl(_rest_last_hint)
            print("[DATE DEBUG] Player ordered '%s' -> %s reaction='%s' (her fav='%s' hate='%s')" % (_player_food, _rg.gid, _hint_reaction, getattr(_rg, "FavoriteDish", "?"), getattr(_rg, "HatedDish", "?")))
            if _hint_reaction == "loves":
                _rest_add_score(1, "player food = her fav")
                _rg.discover("discovered_fav_dish")

        if _hint_reaction == "loves":
            $ set_scene_expression(_rg, "happy")
        elif _hint_reaction == "hates":
            $ set_scene_expression(_rg, "sad")
        else:
            $ set_scene_expression(_rg, "normal")

        $ Say_Line(_rg, _hint_line)
        $ set_scene_expression(_rg, "normal")

        $ _rest_hint_idx += 1
        if _rest_hint_idx < len(_restaurant_girls):
            jump .player_food_reaction

        $ _rest_order_idx = 0
        jump .order_for_girl

    # ── ORDERING STEP 2: Order for each girl ──────────────
    label .order_for_girl:
        python:
            _rg = _restaurant_girls[_rest_order_idx]

        if _rest_order_idx == 0:
            $ Narration(_tl(_("Now, for %s...")) % _rg.Name)
        else:
            $ Narration(_tl(_("And for %s...")) % _rg.Name)

        python:
            _order_tpl = _tl(_("Order %s for %s"))
            _lbl_steak = _tl(_("Steak"))
            _lbl_pasta = _tl(_("Pasta"))
            _lbl_chicken = _tl(_("Chicken"))
            _lbl_salad = _tl(_("Salad"))
            _lbl_let_choose = _tl(_("Let %s choose")) % _rg.Name
            _pr_steak = RESTAURANT_MENU["steak"]["price"]
            _pr_pasta = RESTAURANT_MENU["pasta"]["price"]
            _pr_chicken = RESTAURANT_MENU["chicken"]["price"]
            _pr_salad = RESTAURANT_MENU["salad"]["price"]
            _menu_steak = (_order_tpl % (_lbl_steak, _rg.Name)) + " ($%d)" % _pr_steak
            _menu_pasta = (_order_tpl % (_lbl_pasta, _rg.Name)) + " ($%d)" % _pr_pasta
            _menu_chicken = (_order_tpl % (_lbl_chicken, _rg.Name)) + " ($%d)" % _pr_chicken
            _menu_salad = (_order_tpl % (_lbl_salad, _rg.Name)) + " ($%d)" % _pr_salad

        menu:
            "[_menu_steak]":
                python:
                    _restaurant_orders[_rg.gid] = "steak"
                    _her_reaction = _rest_food_reaction(_rg, "steak")
            "[_menu_pasta]":
                python:
                    _restaurant_orders[_rg.gid] = "pasta"
                    _her_reaction = _rest_food_reaction(_rg, "pasta")
            "[_menu_chicken]":
                python:
                    _restaurant_orders[_rg.gid] = "chicken"
                    _her_reaction = _rest_food_reaction(_rg, "chicken")
            "[_menu_salad]":
                python:
                    _restaurant_orders[_rg.gid] = "salad"
                    _her_reaction = _rest_food_reaction(_rg, "salad")
            "[_lbl_let_choose]":
                python:
                    _her_reaction = "let_choose"
                    _her_fav = getattr(_rg, "FavoriteDish", None) or store._rest_food_prefs.get(_rg.gid, {}).get("loves", "steak")
                    _restaurant_orders[_rg.gid] = _her_fav

        # Girl reacts to the order decision
        $ print("[DATE DEBUG] Ordered '%s' for %s -> reaction='%s' (her fav='%s' hate='%s')" % (_restaurant_orders.get(_rg.gid, "?"), _rg.gid, _her_reaction, getattr(_rg, "FavoriteDish", "?"), getattr(_rg, "HatedDish", "?")))
        if _her_reaction == "let_choose":
            python:
                _her_fav_label = _tl(RESTAURANT_MENU[_her_fav]["label"])
                _choose_line = _tl(renpy.random.choice(_REST_LET_HER_CHOOSE)) % _her_fav_label
                _rest_add_score(1, "let her choose")
                _rg.discover("discovered_fav_dish")
            $ set_scene_expression(_rg, "happy")
            $ Say_Line(_rg, _choose_line)
        elif _her_reaction == "loves":
            $ set_scene_expression(_rg, "surprised")
            $ Say_Line(_rg, _tl(renpy.random.choice(_REST_ORDER_FOR_HER["loves"])))
            $ set_scene_expression(_rg, "happy")
            $ _rest_add_score(2, "ordered her fav for her")
            $ _rg.discover("discovered_fav_dish")
        elif _her_reaction == "hates":
            $ set_scene_expression(_rg, "sad")
            $ Say_Line(_rg, _tl(renpy.random.choice(_REST_ORDER_FOR_HER["hates"])))
            $ _rest_add_score(-1, "ordered her hated dish")
        else:
            $ set_scene_expression(_rg, "normal")
            $ Say_Line(_rg, _tl(renpy.random.choice(_REST_ORDER_FOR_HER["neutral"])))
            $ _rest_add_score(1, "ordered neutral dish for her")

        $ set_scene_expression(_rg, "normal")
        $ _rest_order_idx += 1
        if _rest_order_idx < len(_restaurant_girls):
            jump .order_for_girl

        $ Narration(_tl(_("The food arrives. You start eating and talking.")))

        if len(_restaurant_girls) >= 2:
            python:
                for _ag in _restaurant_girls:
                    store._rest_attention[_ag.gid] = 0

        jump .interaction_loop

    # ── INTERACTION LOOP (3 turns) ────────────────────────
    label .interaction_loop:
        if _restaurant_turn >= 3:
            python:
                if len(_restaurant_girls) == 1:
                    _rest_event = _rest_pick_event(_restaurant_girls[0])
                else:
                    _rest_event = _rest_pick_group_event(_restaurant_girls)
            if _rest_event:
                $ debug_log("[RESTAURANT] Event fired: %s" % _rest_event)
                $ unlock_achievement("hot_date")
                $ renpy.jump("restaurant_date_event." + _rest_event)
            jump .payment

        $ _restaurant_turn += 1

        if len(_restaurant_girls) >= 2:
            python:
                _rg1 = _restaurant_girls[0]
                _rg2 = _restaurant_girls[1]
                _lbl_chat1 = _tl(_("Chat with %s")) % _rg1.Name
                _lbl_chat2 = _tl(_("Chat with %s")) % _rg2.Name
                _lbl_comp1 = _tl(_("Compliment %s")) % _rg1.Name
                _lbl_comp2 = _tl(_("Compliment %s")) % _rg2.Name
                _avail_comps = [(k, t, kind) for k, t, kind in COMPLIMENT_OPTIONS if k not in _rest_compliments_used]
                _has_compliments = len(_avail_comps) > 0
                _lbl_silence = _tl(_("Eat in silence"))

            menu:
                "[_lbl_chat1]":
                    $ _rest_target = _rg1
                    jump .do_chat
                "[_lbl_chat2]":
                    $ _rest_target = _rg2
                    jump .do_chat
                "[_lbl_comp1]" if _has_compliments:
                    $ _rest_target = _rg1
                    jump .compliment_menu
                "[_lbl_comp2]" if _has_compliments:
                    $ _rest_target = _rg2
                    jump .compliment_menu
                "[_lbl_silence]":
                    $ print("[DATE DEBUG] Ate in silence (turn %d/3, no score)" % _restaurant_turn)
                    $ Narration(_tl(_("You eat in comfortable silence for a while.")))

        else:
            python:
                _rest_target = _restaurant_girls[0]
                _avail_comps = [(k, t, kind) for k, t, kind in COMPLIMENT_OPTIONS if k not in _rest_compliments_used]
                _has_compliments = len(_avail_comps) > 0
                _lbl_chat = _tl(_("Chat"))
                _lbl_compliment = _tl(_("Compliment her"))
                _lbl_silence = _tl(_("Eat in silence"))

            menu:
                "[_lbl_chat]":
                    jump .do_chat
                "[_lbl_compliment]" if _has_compliments:
                    jump .compliment_menu
                "[_lbl_silence]":
                    $ print("[DATE DEBUG] Ate in silence (turn %d/3, no score)" % _restaurant_turn)
                    $ Narration(_tl(_("You eat in comfortable silence for a while.")))
                    $ set_scene_expression(_rest_target, "normal")

        jump .interaction_loop

    # ── CHAT ACTION ───────────────────────────────────────
    label .do_chat:
        $ print("[DATE DEBUG] Chat with %s (turn %d/3)" % (_rest_target.gid, _restaurant_turn))
        $ set_scene_expression(_rest_target, "laugh")
        $ Say_Line(_rest_target, _tl(renpy.random.choice(_REST_CHAT_REACT)))
        $ set_scene_expression(_rest_target, "happy")
        $ _rest_add_score(1, "chat")
        $ Change_Status(_rest_target, "Love", renpy.random.randint(2, 3))
        jump .post_interaction

    # ── COMPLIMENT SUB-MENU ───────────────────────────────
    label .compliment_menu:
        python:
            _avail_comps = [(k, t, kind) for k, t, kind in COMPLIMENT_OPTIONS if k not in _rest_compliments_used]
            renpy.random.shuffle(_avail_comps)
            _comp_pool = _avail_comps[:3]
            _opt0_key, _opt0_text, _opt0_kind = _comp_pool[0]
            _opt0_label = _tl(_opt0_text)
            if len(_comp_pool) >= 2:
                _opt1_key, _opt1_text, _opt1_kind = _comp_pool[1]
                _opt1_label = _tl(_opt1_text)
            else:
                _opt1_key = None
                _opt1_label = ""
            if len(_comp_pool) >= 3:
                _opt2_key, _opt2_text, _opt2_kind = _comp_pool[2]
                _opt2_label = _tl(_opt2_text)
            else:
                _opt2_key = None
                _opt2_label = ""

        menu:
            "[_opt0_label]":
                $ _rest_comp_key = _opt0_key
                $ _rest_comp_kind = _opt0_kind
            "[_opt1_label]" if _opt1_key:
                $ _rest_comp_key = _opt1_key
                $ _rest_comp_kind = _opt1_kind
            "[_opt2_label]" if _opt2_key:
                $ _rest_comp_key = _opt2_key
                $ _rest_comp_kind = _opt2_kind

        python:
            _rest_compliments_used.append(_rest_comp_key)
            _comp_result = _rest_compliment_result(_rest_target, _rest_comp_kind)
            _comp_score = _REST_COMPLIMENT_SCORES[_comp_result]
            print("[DATE DEBUG] Compliment '%s' (kind=%s) on %s -> result='%s' score=%+d | Love=%d Lust=%d Tempt=%d" % (_rest_comp_key, _rest_comp_kind, _rest_target.gid, _comp_result, _comp_score, _rest_target.Love, _rest_target.Lust, _rest_target.Temptation))
            _rest_add_score(_comp_score, "compliment %s" % _comp_result)

        if _comp_result == "liked":
            $ set_scene_expression(_rest_target, "happy", blush=1)
            $ Say_Line(_rest_target, _tl(renpy.random.choice(_REST_COMPLIMENT_REACT["liked"])))
            $ set_scene_expression(_rest_target, "shy", blush=1)
            $ Change_Status(_rest_target, "Love", renpy.random.randint(3, 6))
        elif _comp_result == "neutral":
            $ set_scene_expression(_rest_target, "smile")
            $ Say_Line(_rest_target, _tl(renpy.random.choice(_REST_COMPLIMENT_REACT["neutral"])))
            $ set_scene_expression(_rest_target, "normal")
            $ Change_Status(_rest_target, "Love", 1)
        else:
            $ set_scene_expression(_rest_target, "uncomfortable")
            $ Say_Line(_rest_target, _tl(renpy.random.choice(_REST_COMPLIMENT_REACT["disliked"])))
            $ set_scene_expression(_rest_target, "normal")
            $ Change_Status(_rest_target, "Love", -2)

        jump .post_interaction

    # ── POST-INTERACTION CHECK (attention + jealousy) ─────
    label .post_interaction:
        if len(_restaurant_girls) >= 2:
            $ store._rest_attention[_rest_target.gid] = store._rest_attention.get(_rest_target.gid, 0) + 1

            python:
                _jeal_girl, _jeal_level = _rest_check_jealousy(_restaurant_girls, _rest_attention)

            if _jeal_level == "mild":
                $ set_scene_expression(_jeal_girl, "sad")
                $ Say_Line(_jeal_girl, _tl(renpy.random.choice(_REST_JEALOUSY_MILD)))
                $ set_scene_expression(_jeal_girl, "normal")
            elif _jeal_level == "angry":
                $ set_scene_expression(_jeal_girl, "angry")
                $ Say_Line(_jeal_girl, _tl(renpy.random.choice(_REST_JEALOUSY_ANGRY)))
                $ set_scene_expression(_jeal_girl, "uncomfortable")
                $ _rest_add_score(-1, "jealousy angry")
                $ Change_Status(_jeal_girl, "Love", -3)

        jump .interaction_loop

    # ══════════════════════════════════════════════════════
    # DATE EVENT: UNDER-TABLE BJ (shared intro)
    # ══════════════════════════════════════════════════════
    label .event_bj_intro:
        $ _rg = _restaurant_girls[0]
        $ set_scene_expression(_rg, "shy", blush=1)
        $ Say_Line(_rg, _tl(_("Hold still... I want to try something.")))
        $ Narration(_tl(_("She glances around the restaurant, then slips under the table.")))
        $ renpy.show(_rg.gid, at_list=[_rest_slide_under_table])
        pause 0.6
        $ renpy.hide(_rg.gid)
        $ Narration(_tl(_("You feel her hands sliding up your thighs.")))
        pause 0.3
        $ Narration(_tl(_("Fingers undo your zipper.")))
        return

    # ── VARIANT 1: Waitress arrives (narration only) ──────
    label .event_bj_waitress:
        $ _rg = _restaurant_girls[0]
        $ debug_log("[RESTAURANT] Event BJ Waitress triggered for %s" % _rg.gid)
        call .event_bj_intro from _call_rest_bj_intro_w

        $ Narration(_tl(_("A waitress approaches your table with a smile.")))
        pause 0.3
        $ WaitressChar(_tl(_("Is everything alright, sir? Can I get you anything else?")))

        $ Player.Focus = 20

        $ Narration(_tl(_("You try to keep a straight face as her tongue works underneath.")))
        $ add_player_focus(15)

        $ PlayerChar(_tl(_("Y-yes, everything's fine. Just the check, please.")))
        $ add_player_focus(15)

        $ Narration(_tl(_("The waitress tilts her head.")))
        $ WaitressChar(_tl(_("Are you sure? You look a little flushed.")))
        $ add_player_focus(15)

        $ Narration(_tl(_("Under the table, she speeds up. Your knuckles go white gripping the tablecloth.")))
        $ add_player_focus(15)

        $ PlayerChar(_tl(_("I'm... I'm fine. Really.")))
        $ Narration(_tl(_("You force a smile.")))
        $ add_player_focus(10)

        $ Narration(_tl(_("The waitress nods slowly.")))
        $ WaitressChar(_tl(_("Alright... I'll bring the check.")))
        $ add_player_focus(10)

        if Player.Focus >= 100:
            $ Narration(_tl(_("The moment she turns away, you lose it.")))
            call HardPunch from _call_rest_bj_punch1
            $ Narration(_tl(_("You grip the edge of the table. Cold sweat runs down your temple.")))
        else:
            $ Player.Focus = 100
            $ Narration(_tl(_("She's barely two steps away when it hits you.")))
            call HardPunch from _call_rest_bj_punch2
            $ Narration(_tl(_("You bite down hard, staring at the ceiling.")))

        pause 0.5
        $ Narration(_tl(_("Under the table, she swallows. Then giggles.")))

        # Girl slides back up
        pause 0.3
        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[_rest_slide_back_up])
        pause 0.6
        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])
        $ set_scene_expression(_rg, "smug", blush=1)
        $ Say_Line(_rg, _tl(_("Loved the dessert. Hope there's more next time.")))
        $ set_scene_expression(_rg, "happy")

        # Stats
        python:
            Player.Focus = 0
            _rg.RegisterAction("bj")
            _rest_add_score(2, "event: BJ waitress")
            Change_Status(_rg, "Love", 5)
            Change_Status(_rg, "Obed", 10)
            _girl_lust_gain(_rg, 10, 0)
            debug_log("[RESTAURANT] BJ waitress variant complete")

        jump .payment

    # ── VARIANT 2: Player peeks under tablecloth (visual BJ) ──
    label .event_bj_peek:
        $ _rg = _restaurant_girls[0]
        $ debug_log("[RESTAURANT] Event BJ Peek triggered for %s" % _rg.gid)
        call .event_bj_intro from _call_rest_bj_intro_p

        $ Narration(_tl(_("You can't resist. You lift the edge of the tablecloth to peek.")))
        $ unlock_achievement("hidden_menu")
        pause 0.3

        scene bg restaurant_under_table
        # Launch restricted BJ scene
        python:
            store._scene_restricted = True
            store._interruption_happened = True
            store._witness_check_done = True
            session_cum_reset()
            Player.Focus = 20

        call BJ_Launch(_rg) from _call_rest_bj_launch
        call BJ_ControlMenu(_rg) from _call_rest_bj_control
        call BJ_End(_rg, dress_up=False) from _call_BJ_End_rest_bj
        python:
            _bj_angry_abort = getattr(store, "_scene_angry_abort", False)
            store._scene_restricted = False
            store._scene_angry_abort = False
            store._player_exhausted = False
            store._interruption_happened = False
            store._witness_check_done = False
            _bj_cum_result = "none"
            if store._session_cum.get("mouth", 0) > 0:
                _bj_cum_result = "mouth"
            elif store._session_cum.get("face", 0) > 0:
                _bj_cum_result = "face"
            elif store._session_cum.get("outside", 0) > 0:
                _bj_cum_result = "outside"

        # Return to restaurant view
        $ store._restaurant_bg = "bg restaurant"
        scene bg restaurant
        with fade
        show restaurant_table zorder 10
        pause 0.2

        if _bj_angry_abort:
            # Girl comes back up angry, date score zeroed
            $ set_girl_sprite(_rg.gid, pose="standing", at_list=[_rest_slide_back_up])
            pause 0.6
            $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])
            $ set_scene_expression(_rg, "angry")
            $ Narration(_tl(_("She crawls back up, visibly furious. The rest of dinner is painfully silent.")))
            python:
                _rg.RegisterAction("bj")
                store._rest_score = 0
                debug_log("[RESTAURANT] BJ peek angry abort. Score zeroed.")
            jump .payment

        # Narration based on cum result
        if _bj_cum_result == "mouth":
            $ Narration(_tl(_("She swallows and wipes the corner of her lips with her thumb.")))
        elif _bj_cum_result == "face":
            $ Narration(_tl(_("She grabs a napkin from under the table and cleans her face.")))
        elif _bj_cum_result == "outside":
            $ Narration(_tl(_("She grabs a napkin and wipes herself clean before coming back up.")))
        else:
            $ Narration(_tl(_("She tucks you back in and straightens the tablecloth.")))

        # Girl slides back up
        pause 0.2
        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[_rest_slide_back_up])
        pause 0.6
        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])

        # Dialogue based on cum result
        if _bj_cum_result == "mouth":
            $ set_scene_expression(_rg, "smug", blush=1)
            $ Say_Line(_rg, _tl(_("Loved the dessert. Hope there's more next time.")))
        elif _bj_cum_result == "face":
            $ set_scene_expression(_rg, "shy", blush=1)
            $ Say_Line(_rg, _tl(_("You could have warned me...")))
        elif _bj_cum_result == "outside":
            $ set_scene_expression(_rg, "smug", blush=1)
            $ Say_Line(_rg, _tl(_("Good thing these napkins are thick.")))
        else:
            $ set_scene_expression(_rg, "normal")
            $ Say_Line(_rg, _tl(_("What? Changed your mind?")))
        $ set_scene_expression(_rg, "happy")

        # Stats
        python:
            _rg.RegisterAction("bj")
            _rest_add_score(2, "event: BJ peek")
            Change_Status(_rg, "Love", 5)
            Change_Status(_rg, "Obed", 10)
            debug_log("[RESTAURANT] BJ peek variant complete. Cum: %s" % _bj_cum_result)

        jump .payment

    # ══════════════════════════════════════════════════════
    # DATE EVENT: RESTROOM QUICKIE
    # Triggers if girl has had sex before + is aroused.
    # Direct BJ or Sex (no sex_menu). 1 cum = scene end.
    # ══════════════════════════════════════════════════════
    label .event_restroom:
        $ _rg = _restaurant_girls[0]
        $ debug_log("[RESTAURANT] Event Restroom triggered for %s" % _rg.gid)

        $ set_scene_expression(_rg, "lipbite", blush=1)
        $ Say_Line(_rg, _tl(_("It's going to take a while to get home, isn't it...")))
        $ set_scene_expression(_rg, "lusty", blush=1)
        $ Say_Line(_rg, _tl(_("Wait a minute and come to the restroom.")))

        # Girl slides left and exits
        $ renpy.show(_rg.gid, at_list=[_rest_exit_left])
        pause 0.8
        $ renpy.hide(_rg.gid)

        $ Narration(_tl(_("You follow her instructions.")))

        # Scene change to restroom
        $ store._restaurant_bg = "bg restaurant_restroom"
        scene bg restaurant_restroom
        with fade
        pause 0.3

        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])
        $ set_scene_expression(_rg, "lusty", blush=1)

        $ Narration(_tl(_("She locks the door behind you.")))
        $ unlock_achievement("restroom_break")
        $ Say_Line(_rg, _tl(_("We have to be quick...")))

        # Setup restricted scene
        python:
            store._scene_restricted = True
            store.door_locked = True
            store._rest_saved_location = store.CurrentLocation
            store.CurrentLocation = "restaurant_restroom"
            store._interruption_happened = True
            store._witness_check_done = True
            store._npc_witness_check_done = True
            session_cum_reset()
            store.Player.Focus = 20

        $ _rest_choice = None
        $ _rest_pos = None

        menu:
            "Blowjob":
                $ _rest_choice = "bj"
            "Sex":
                $ _rest_choice = "sex"

        # ── BJ PATH ──
        if _rest_choice == "bj":
            call start_scene(_rg, "bj") from _call_rest_room_bj

        # ── SEX PATH ──
        elif _rest_choice == "sex":
            $ _pen = sex_penetration_check(_rg, skip_insistence=True)
            if _pen["accepted"]:
                # Build valid positions (no anal)
                python:
                    _rest_positions = []
                    if girl_has_pose(_rg, "reverse_cowgirl"):
                        _rest_positions.append("reverse_cowgirl")
                    if girl_has_pose(_rg, "cowgirl"):
                        _rest_positions.append("cowgirl")
                    if girl_has_pose(_rg, "doggy"):
                        _rest_positions.append("doggy")
                    if girl_has_pose(_rg, "laying_down"):
                        _rest_positions.append("laying_down")

                if len(_rest_positions) == 1:
                    $ _rest_pos = _rest_positions[0]
                else:
                    menu:
                        "Reverse Cowgirl" if "reverse_cowgirl" in _rest_positions:
                            $ _rest_pos = "reverse_cowgirl"
                        "Cowgirl" if "cowgirl" in _rest_positions:
                            $ _rest_pos = "cowgirl"
                        "Doggy" if "doggy" in _rest_positions:
                            $ _rest_pos = "doggy"
                        "Laying Down" if "laying_down" in _rest_positions:
                            $ _rest_pos = "laying_down"

                call condom_check(_rg, _pen["condom_required"], _pen["raw_outcome"]) from _call_rest_room_condom

                if not store.condom_denied:
                    call start_scene(_rg, "sex", _rest_pos) from _call_rest_room_sex
                else:
                    $ Say_Line(_rg, _tl(_("...Forget it then. Let's go back.")))
            else:
                # Denied sex — offer BJ as fallback with specific reason
                if _rg.has_trait("virgin"):
                    $ Say_Line(_rg, _tl(_("My first time is not going to be in a bathroom. No way.")))
                else:
                    python:
                        _rest_reasons = _pen["result"].get("reasons", [])
                        _rest_loc_issue = "semi_public_pressure" in _rest_reasons or "public_pressure" in _rest_reasons
                        _rest_cheat = _pen["result"].get("is_cheating", False)
                        _rest_has_bf = _rg.has_trait("has_boyfriend") or _rg.has_trait("has_girlfriend")
                        _rest_loyal = _rg.has_trait("loyal")
                        _rest_shy = _rg.has_trait("public_shy")

                        if _rest_loc_issue and _rest_cheat and _rest_has_bf:
                            _rest_deny_pool = [
                                _("Here?! No way. And I have %(pn)s... I can't do this."),
                                _("In a public restroom AND cheating on %(pn)s? No. Just no."),
                            ]
                        elif _rest_loc_issue and _rest_shy:
                            _rest_deny_pool = [
                                _("Not here... someone could walk in at any moment."),
                                _("I can't do that in a place like this. Anyone could hear us."),
                            ]
                        elif _rest_loc_issue:
                            _rest_deny_pool = [
                                _("Here? No... this isn't the place for that."),
                                _("I don't think I can do that here... not like this."),
                            ]
                        elif _rest_cheat and _rest_has_bf and _rest_loyal:
                            _rest_deny_pool = [
                                _("I can't... I have %(pn)s. This is already going too far."),
                                _("No... %(pn)s would never forgive me. I can't go that far."),
                            ]
                        elif _rest_cheat and _rest_has_bf:
                            _rest_deny_pool = [
                                _("I don't think I can go that far... I still have %(pn)s."),
                            ]
                        else:
                            _rest_deny_pool = [
                                _("I don't think I'm ready for that..."),
                                _("Can we take things slower? That's too much right now."),
                            ]
                        _rest_deny = _format_partner_line(_rg, renpy.random.choice(_rest_deny_pool))
                    $ Say_Line(_rg, _rest_deny)
                menu:
                    "Go for a blowjob instead":
                        call start_scene(_rg, "bj") from _call_rest_room_bj_fb
                    "Forget it":
                        pass

        # ── COMMON CLEANUP ──
        python:
            _rest_angry_abort = getattr(store, "_scene_angry_abort", False)
            store._scene_restricted = False
            store._scene_angry_abort = False
            store._player_exhausted = False
            store.door_locked = False
            store._interruption_happened = False
            store._witness_check_done = False
            store._npc_witness_check_done = False
            store.CurrentLocation = store._rest_saved_location

        if _rest_angry_abort:
            $ store._restaurant_bg = "bg restaurant"
            scene bg restaurant
            with fade
            show restaurant_table zorder 10
            pause 0.2
            $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])
            $ set_scene_expression(_rg, "angry")
            $ Narration(_tl(_("You walk back to the table separately. She refuses to look at you for the rest of dinner.")))
            python:
                store._rest_score = 0
                debug_log("[RESTAURANT] Restroom angry abort. Score zeroed.")
            jump .payment

        $ Narration(_tl(_("You decide to finish before drawing too much attention.")))

        # Girl is already standing from start_scene cleanup; just fix position/expression
        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])

        if _rg.has_trait("public_fetish") or _rg.Inbt >= 500:
            $ set_scene_expression(_rg, "smug", blush=1)
            $ Say_Line(_rg, _tl(_("Let's go back together. Who cares if they notice.")))
        else:
            $ set_scene_expression(_rg, "lusty", blush=1)
            $ Say_Line(_rg, _tl(_("Ok, I'll go first. Wait a bit and go back to the table.")))

        $ set_scene_expression(_rg, "happy")

        python:
            _rest_add_score(2, "event: restroom")
            Change_Status(_rg, "Love", 5)
            debug_log("[RESTAURANT] Restroom event complete")

        # Return to restaurant — girl slides back in from the left
        $ store._restaurant_bg = "bg restaurant"
        scene bg restaurant
        with fade
        show restaurant_table zorder 10
        pause 0.2
        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[_rest_enter_from_left])
        $ set_scene_expression(_rg, "happy")
        pause 0.8
        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])

        jump .payment

    # ══════════════════════════════════════════════════════
    # DATE EVENT: FOOTJOB TEASE
    # Light tease under the table. Builds Focus to 90.
    # ══════════════════════════════════════════════════════
    label .event_footjob_tease:
        $ _rg = _restaurant_girls[0]
        $ debug_log("[RESTAURANT] Event Footjob Tease triggered for %s" % _rg.gid)

        $ set_scene_expression(_rg, "smug")

        # Girl slides down slightly in her seat
        $ renpy.show(_rg.gid, at_list=[_rest_tease_slide_down])
        pause 0.4

        $ Narration(_tl(_("You feel something caressing your groin under the table.")))
        $ Player.Focus = max(Player.Focus, 30)
        pause 0.3
        $ Narration(_tl(_("%s starts stroking your crotch with her bare feet.")) % _rg.Name)
        $ Player.Focus = max(Player.Focus, 50)

        if _rg.has_trait("public_fetish") or _rg.Inbt >= 500:
            $ set_scene_expression(_rg, "lusty", blush=1)
            $ Say_Line(_rg, _tl(_("Take it out. I want more.")))
            $ Narration(_tl(_("You unzip and expose yourself under the table.")))
            $ Player.Focus = max(Player.Focus, 70)

        $ Narration(_tl(_("Her toes wrap around you, sliding up and down slowly.")))
        $ Player.Focus = max(Player.Focus, 70)
        pause 0.3
        $ Narration(_tl(_("She keeps going, pressing her sole against you with each stroke.")))
        $ Player.Focus = max(Player.Focus, 90)

        $ set_scene_expression(_rg, "smug", blush=1)
        $ Say_Line(_rg, _tl(_("Just a free sample of what we'll have later.")))

        # Girl slides back to initial position
        $ renpy.show(_rg.gid, at_list=[_rest_tease_slide_up])
        pause 0.4
        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])
        $ set_scene_expression(_rg, "happy")

        python:
            _rest_add_score(1, "event: footjob tease")
            _girl_lust_gain(_rg, 5, 0)
            Change_Status(_rg, "Love", 3)
            debug_log("[RESTAURANT] Footjob tease complete. Focus=%d" % Player.Focus)

        jump .payment

    # ══════════════════════════════════════════════════════
    # GROUP EVENT: DOUBLE FOOTJOB
    # ══════════════════════════════════════════════════════
    label .event_double_footjob:
        python:
            _fj_candidates = [g for g in _restaurant_girls if g.Sex_acts.get("tj", 0) > 0 and not g.has_trait("lesbian")]
            if len(_fj_candidates) >= 2:
                _fj_init = next((g for g in _fj_candidates if g.has_trait("public_fetish")), _fj_candidates[0])
            else:
                _fj_init = _fj_candidates[0]
            _fj_other = [g for g in _restaurant_girls if g != _fj_init][0]
            _fj_init_is_left = (_restaurant_girls[0] == _fj_init)
            _fj_init_slot = slot_left if _fj_init_is_left else slot_center
            _fj_other_slot = slot_center if _fj_init_is_left else slot_left
            _fj_init_slide_down = _rest_tease_slide_down_left if _fj_init_is_left else _rest_tease_slide_down
            _fj_init_slide_up = _rest_tease_slide_up_left if _fj_init_is_left else _rest_tease_slide_up
            _fj_other_slide_down = _rest_tease_slide_down if _fj_init_is_left else _rest_tease_slide_down_left
            _fj_other_slide_up = _rest_tease_slide_up if _fj_init_is_left else _rest_tease_slide_up_left
            debug_log("[RESTAURANT] Double footjob: initiator=%s (left=%s), other=%s" % (_fj_init.gid, _fj_init_is_left, _fj_other.gid))

        $ set_scene_expression(_fj_init, "smug")

        $ renpy.show(_fj_init.gid, at_list=[_fj_init_slide_down])
        pause 0.4

        $ Narration(_tl(_("You feel something brush against your leg under the table.")))
        $ Player.Focus = max(Player.Focus, 30)
        pause 0.3
        $ Narration(_tl(_("%s starts stroking your crotch with her bare feet.")) % _fj_init.Name)
        $ Player.Focus = max(Player.Focus, 50)

        if _fj_init.has_trait("public_fetish") or _fj_init.Inbt >= 500:
            $ set_scene_expression(_fj_init, "lusty", blush=1)
            $ Say_Line(_fj_init, _tl(_("Take it out. I want more.")))
            $ Narration(_tl(_("You unzip and expose yourself under the table.")))
            $ Player.Focus = max(Player.Focus, 70)

        $ Narration(_tl(_("Her toes wrap around you, sliding up and down slowly.")))
        $ Player.Focus = max(Player.Focus, 70)
        pause 0.3

        # ── Roll: does the other girl notice? ──
        python:
            _fj_debug_force = getattr(store, "_debug_fj_force", "")
            _fj_notice_chance = 40
            _fj_attn_init = _rest_attention.get(_fj_init.gid, 0)
            _fj_attn_other = _rest_attention.get(_fj_other.gid, 0)
            if _fj_attn_other < _fj_attn_init:
                _fj_notice_chance += 20
            if _fj_other.has_trait("public_fetish"):
                _fj_notice_chance += 20
            if _fj_other.has_trait("voyeur"):
                _fj_notice_chance += 15
            if _fj_other.Inbt >= 400:
                _fj_notice_chance += 10
            if _fj_debug_force:
                _fj_noticed = True
                debug_log("[RESTAURANT] Double FJ: DEBUG FORCE=%s" % _fj_debug_force)
            else:
                _fj_noticed = renpy.random.randint(1, 100) <= _fj_notice_chance
            debug_log("[RESTAURANT] Double FJ: other notice chance=%d, noticed=%s" % (_fj_notice_chance, _fj_noticed))

        if _fj_noticed:
            # Other girl notices something is off
            $ set_scene_expression(_fj_other, "surprised")
            $ Say_Line(_fj_other, _tl(_("Wait... what's going on under there?")))

            $ set_scene_expression(_fj_init, "smug", blush=1)
            $ Say_Line(_fj_init, _tl(_("Nothing you can't join in on.")))
            $ Narration(_tl(_("%s keeps her eyes on both of you, watching the movements under the tablecloth.")) % _fj_other.Name)

            # ── Determine reaction: join / ignore / stop ──
            python:
                if _fj_debug_force in ("join", "ignore", "stop"):
                    _fj_reaction = _fj_debug_force
                    debug_log("[RESTAURANT] Double FJ: DEBUG forced reaction=%s" % _fj_reaction)
                else:
                    _fj_like = int(_fj_other.Girl_like.get(_fj_init.gid, 500))
                    _fj_is_gf = _fj_other.is_dating_player()
                    _fj_jeal_girl, _fj_jeal_level = _rest_check_jealousy(_restaurant_girls, _rest_attention)
                    _fj_has_skills = (
                        _fj_other.Sex_acts.get("tj", 0) > 0
                        or _fj_other.Inbt >= 400
                        or _fj_other.has_trait("public_fetish")
                    )
                    _fj_is_lesbian = _fj_other.has_trait("lesbian")
                    _fj_is_voyeur = _fj_other.has_trait("voyeur")
                    if _fj_is_lesbian:
                        _fj_reaction = "ignore"
                    elif _fj_is_gf or (_fj_jeal_level == "angry" and _fj_like < 400):
                        _fj_reaction = "stop"
                    elif _fj_like < 250:
                        _fj_reaction = "stop" if not _fj_is_voyeur else "ignore"
                    elif _fj_has_skills and _fj_like >= 400 and _fj_jeal_level != "angry":
                        _fj_reaction = "join"
                    else:
                        _fj_reaction = "ignore"
                    debug_log("[RESTAURANT] Double FJ: reaction=%s (like=%d, gf=%s, jeal=%s, skills=%s, lesbian=%s, voyeur=%s)" % (_fj_reaction, _fj_like, _fj_is_gf, _fj_jeal_level, _fj_has_skills, _fj_is_lesbian, _fj_is_voyeur))

            if _fj_reaction == "join":
                $ Narration(_tl(_("%s watches for a moment, biting her lip.")) % _fj_other.Name)
                $ set_scene_expression(_fj_other, "shy", blush=1)
                $ Say_Line(_fj_other, _tl(_("I can't believe we're doing this here...")))

                $ renpy.show(_fj_other.gid, at_list=[_fj_other_slide_down])
                pause 0.4

                $ Narration(_tl(_("You feel a second pair of feet join in. Both of them are working you under the table.")))
                $ Player.Focus = max(Player.Focus, 90)
                pause 0.3

                $ set_scene_expression(_fj_init, "lusty", blush=1)
                $ Say_Line(_fj_init, _tl(_("See? Much better with two.")))

                $ Narration(_tl(_("Their feet intertwine around you, taking turns stroking.")))
                $ Player.Focus = max(Player.Focus, 100)
                pause 0.3

                $ set_scene_expression(_fj_other, "lusty", blush=1)
                $ Say_Line(_fj_other, _tl(_("Don't you dare finish here.")))

                $ renpy.show(_fj_other.gid, at_list=[_fj_other_slide_up])
                pause 0.3
                $ renpy.show(_fj_init.gid, at_list=[_fj_init_slide_up])
                pause 0.4

                $ set_girl_sprite(_fj_init.gid, pose="standing", at_list=[_fj_init_slot])
                $ set_girl_sprite(_fj_other.gid, pose="standing", at_list=[_fj_other_slot])
                $ set_scene_expression(_fj_init, "happy")
                $ set_scene_expression(_fj_other, "shy", blush=1)

                python:
                    _rest_add_score(2, "event: double footjob both")
                    _girl_lust_gain(_fj_init, 5, 0)
                    _girl_lust_gain(_fj_other, 5, 0)
                    Change_Status(_fj_init, "Love", 3)
                    Change_Status(_fj_other, "Love", 3)
                    debug_log("[RESTAURANT] Double footjob: BOTH joined. Focus=%d" % Player.Focus)

            elif _fj_reaction == "stop":
                $ Narration(_tl(_("%s stares at the table in disbelief, her expression shifting to disgust.")) % _fj_other.Name)
                $ set_scene_expression(_fj_other, "angry")
                $ Say_Line(_fj_other, _tl(renpy.random.choice(_REST_FJ_STOP)))
                $ set_scene_expression(_fj_init, "surprised")

                $ renpy.show(_fj_init.gid, at_list=[_fj_init_slide_up])
                pause 0.4
                $ set_girl_sprite(_fj_init.gid, pose="standing", at_list=[_fj_init_slot])
                $ set_scene_expression(_fj_init, "uncomfortable")
                $ set_scene_expression(_fj_other, "uncomfortable")

                python:
                    _rest_add_score(-1, "event: footjob other stopped")
                    Change_Status(_fj_other, "Love", -5)
                    debug_log("[RESTAURANT] Double footjob: other demanded stop. Focus=%d" % Player.Focus)

            else:
                # ignore — she noticed but doesn't join or stop
                python:
                    _fj_watch_line, _fj_watch_expr, _fj_watch_blush = _rest_fj_pick_watch_line(_fj_other)
                    debug_log("[RESTAURANT] Double FJ: watch line expr=%s blush=%s" % (_fj_watch_expr, _fj_watch_blush))
                $ set_scene_expression(_fj_other, _fj_watch_expr, blush=int(_fj_watch_blush))
                $ Say_Line(_fj_other, _tl(_fj_watch_line))

                if _fj_other.has_trait("voyeur"):
                    $ set_scene_expression(_fj_other, "smug")
                    $ Narration(_tl(_("She leans back in her chair, watching openly with a faint smile.")))
                else:
                    $ set_scene_expression(_fj_other, "looking_left")
                    $ Narration(_tl(_("She crosses her arms and looks away, but keeps stealing glances at the table.")))
                $ Narration(_tl(_("She keeps going, pressing her sole against you with each stroke.")))
                $ Player.Focus = max(Player.Focus, 90)

                $ set_scene_expression(_fj_init, "smug", blush=1)
                $ Say_Line(_fj_init, _tl(_("Just a free sample of what we'll have later.")))

                $ renpy.show(_fj_init.gid, at_list=[_fj_init_slide_up])
                pause 0.4
                $ set_girl_sprite(_fj_init.gid, pose="standing", at_list=[_fj_init_slot])
                $ set_scene_expression(_fj_init, "happy")

                python:
                    _rest_add_score(1, "event: footjob other ignored")
                    _girl_lust_gain(_fj_init, 5, 0)
                    Change_Status(_fj_init, "Love", 3)
                    debug_log("[RESTAURANT] Double footjob: other noticed, ignored. Focus=%d" % Player.Focus)

        else:
            # Other girl doesn't notice - she's on her phone
            python:
                sprite_state[_fj_other.gid]["arm_pos"] = 3
                set_girl_sprite(_fj_other.gid, pose="standing", at_list=[_fj_other_slot])
            $ set_scene_expression(_fj_other, "looking_down")
            $ Narration(_tl(_("%s is scrolling through her phone, completely oblivious to what's happening under the table.")) % _fj_other.Name)

            $ Narration(_tl(_("%s keeps going, pressing her sole against you with each stroke.")) % _fj_init.Name)
            $ Player.Focus = max(Player.Focus, 90)

            $ set_scene_expression(_fj_init, "smug", blush=1)
            $ Say_Line(_fj_init, _tl(_("Just a free sample of what we'll have later.")))

            $ renpy.show(_fj_init.gid, at_list=[_fj_init_slide_up])
            pause 0.4
            $ set_girl_sprite(_fj_init.gid, pose="standing", at_list=[_fj_init_slot])
            $ set_scene_expression(_fj_init, "happy")

            python:
                sprite_state[_fj_other.gid]["arm_pos"] = 0
                set_girl_sprite(_fj_other.gid, pose="standing", at_list=[_fj_other_slot])
            $ set_scene_expression(_fj_other, "normal")

            python:
                _rest_add_score(1, "event: footjob other unaware")
                _girl_lust_gain(_fj_init, 5, 0)
                Change_Status(_fj_init, "Love", 3)
                debug_log("[RESTAURANT] Double footjob: other didn't notice. Focus=%d" % Player.Focus)

        jump .payment

    # ══════════════════════════════════════════════════════
    # GROUP EVENT: DOUBLE BJ
    # One girl slides under the table for BJ. Other always notices.
    # If GF present: only GF initiates, other watches.
    # If no GF: other can join (double BJ) or watch/stop.
    # Lesbian never initiates or joins.
    # ══════════════════════════════════════════════════════
    label .event_double_bj:
        python:
            _bj_gf = next((g for g in _restaurant_girls if g.is_dating_player()), None)
            if _bj_gf is not None:
                _bj_init = _bj_gf
            else:
                _bj_candidates = [g for g in _restaurant_girls if g.Sex_acts.get("bj", 0) > 0 and not g.has_trait("lesbian")]
                _bj_init = next((g for g in _bj_candidates if g.has_trait("public_fetish")), _bj_candidates[0])
            _bj_other = [g for g in _restaurant_girls if g != _bj_init][0]
            _bj_is_gf_scene = _bj_gf is not None
            _bj_init_is_left = (_restaurant_girls[0] == _bj_init)
            _bj_init_slot = slot_left if _bj_init_is_left else slot_center
            _bj_other_slot = slot_center if _bj_init_is_left else slot_left
            _bj_init_slide_under = _rest_slide_under_table_left if _bj_init_is_left else _rest_slide_under_table
            _bj_init_slide_back = _rest_slide_back_up_left if _bj_init_is_left else _rest_slide_back_up
            _bj_other_slide_under = _rest_slide_under_table if _bj_init_is_left else _rest_slide_under_table_left
            _bj_other_slide_back = _rest_slide_back_up if _bj_init_is_left else _rest_slide_back_up_left
            debug_log("[RESTAURANT] Double BJ: initiator=%s (gf_scene=%s, left=%s), other=%s" % (_bj_init.gid, _bj_is_gf_scene, _bj_init_is_left, _bj_other.gid))

        # ── Initiator slides under ──
        $ set_scene_expression(_bj_init, "shy", blush=1)
        $ Say_Line(_bj_init, _tl(_("I'm going to do something crazy. Don't freak out.")))
        $ Narration(_tl(_("She glances around, then disappears under the tablecloth.")))
        $ renpy.show(_bj_init.gid, at_list=[_bj_init_slide_under])
        pause 0.6
        $ renpy.hide(_bj_init.gid)

        $ Narration(_tl(_("You feel hands on your thighs. Fingers undo your zipper.")))
        pause 0.3
        $ Narration(_tl(_("Her lips wrap around you under the table.")))
        $ Player.Focus = max(Player.Focus, 40)
        pause 0.3

        # ── Other girl always notices ──
        $ set_scene_expression(_bj_other, "surprised")
        $ Say_Line(_bj_other, _tl(_("Wait... where did she go? What's happening under the table?")))
        pause 0.3

        $ Narration(_tl(_("%s stares at the tablecloth, then at your face. She puts two and two together.")) % _bj_other.Name)
        $ set_scene_expression(_bj_other, "surprised", blush=1)

        # ── Determine reaction ──
        python:
            _bj_debug_force = getattr(store, "_debug_bj_force", "")
            if _bj_debug_force in ("join", "ignore", "stop"):
                _bj_reaction = _bj_debug_force
                debug_log("[RESTAURANT] Double BJ: DEBUG forced reaction=%s" % _bj_reaction)
            elif _bj_is_gf_scene:
                _bj_reaction = "ignore"
                debug_log("[RESTAURANT] Double BJ: GF scene, other forced to watch")
            elif _bj_other.has_trait("lesbian"):
                _bj_reaction = "ignore"
                debug_log("[RESTAURANT] Double BJ: other is lesbian, forced to watch")
            else:
                _bj_like = int(_bj_other.Girl_like.get(_bj_init.gid, 500))
                _bj_is_other_gf = _bj_other.is_dating_player()
                _bj_jeal_girl, _bj_jeal_level = _rest_check_jealousy(_restaurant_girls, _rest_attention)
                _bj_has_skills = (
                    _bj_other.Sex_acts.get("bj", 0) > 0
                    or _bj_other.Inbt >= 400
                    or _bj_other.has_trait("public_fetish")
                )
                _bj_is_voyeur = _bj_other.has_trait("voyeur")
                if _bj_is_other_gf or (_bj_jeal_level == "angry" and _bj_like < 400):
                    _bj_reaction = "stop"
                elif _bj_like < 250:
                    _bj_reaction = "stop" if not _bj_is_voyeur else "ignore"
                elif _bj_has_skills and _bj_like >= 400 and _bj_jeal_level != "angry":
                    _bj_reaction = "join"
                else:
                    _bj_reaction = "ignore"
                debug_log("[RESTAURANT] Double BJ: reaction=%s (like=%d, gf=%s, jeal=%s, skills=%s, voyeur=%s)" % (_bj_reaction, _bj_like, _bj_is_other_gf, _bj_jeal_level, _bj_has_skills, _bj_is_voyeur))

        # ── JOIN: other slides under too → double BJ ──
        if _bj_reaction == "join":
            $ set_scene_expression(_bj_other, "shy", blush=1)
            $ Say_Line(_bj_other, _tl(renpy.random.choice(_REST_BJ_JOIN)))
            $ Narration(_tl(_("%s slips under the tablecloth too.")) % _bj_other.Name)

            $ renpy.show(_bj_other.gid, at_list=[_bj_other_slide_under])
            pause 0.6
            $ renpy.hide(_bj_other.gid)

            $ unlock_achievement("double_trouble")
            $ Narration(_tl(_("Two mouths. Two tongues. Both of them working you at once under the table.")))
            $ Player.Focus = max(Player.Focus, 70)
            pause 0.3

            $ Narration(_tl(_("They take turns. One licks while the other sucks. You grip the edge of the table.")))
            $ Player.Focus = max(Player.Focus, 90)
            pause 0.3

            $ Narration(_tl(_("Your knuckles go white. The tablecloth trembles.")))
            $ Player.Focus = 100
            call HardPunch from _call_rest_dbj_punch_join
            pause 0.3

            $ Narration(_tl(_("Under the table, they both giggle. You hear them licking you clean.")))
            pause 0.5

            # Both slide back up
            $ set_girl_sprite(_bj_init.gid, pose="standing", at_list=[_bj_init_slide_back])
            $ set_girl_sprite(_bj_other.gid, pose="standing", at_list=[_bj_other_slide_back])
            pause 0.6
            $ set_girl_sprite(_bj_init.gid, pose="standing", at_list=[_bj_init_slot])
            $ set_girl_sprite(_bj_other.gid, pose="standing", at_list=[_bj_other_slot])

            $ set_scene_expression(_bj_init, "smug", blush=1)
            $ set_scene_expression(_bj_other, "shy", blush=1)
            $ Say_Line(_bj_init, _tl(_("Told you it was worth going under.")))
            $ Say_Line(_bj_other, _tl(_("I can't believe I just did that...")))

            python:
                Player.Focus = 0
                _bj_init.RegisterAction("bj")
                _bj_other.RegisterAction("bj")
                _rest_add_score(3, "event: double BJ both")
                Change_Status(_bj_init, "Love", 5)
                Change_Status(_bj_other, "Love", 5)
                Change_Status(_bj_init, "Obed", 10)
                Change_Status(_bj_other, "Obed", 10)
                _girl_lust_gain(_bj_init, 10, 0)
                _girl_lust_gain(_bj_other, 10, 0)
                debug_log("[RESTAURANT] Double BJ: BOTH joined. Focus=%d" % Player.Focus)

        # ── STOP: other demands they stop ──
        elif _bj_reaction == "stop":
            $ set_scene_expression(_bj_other, "angry")
            $ Say_Line(_bj_other, _tl(renpy.random.choice(_REST_BJ_STOP)))

            $ Narration(_tl(_("She bangs on the table.")))
            pause 0.3
            $ Narration(_tl(_("%s crawls back up from under the table, flustered.")) % _bj_init.Name)

            $ set_girl_sprite(_bj_init.gid, pose="standing", at_list=[_bj_init_slide_back])
            pause 0.6
            $ set_girl_sprite(_bj_init.gid, pose="standing", at_list=[_bj_init_slot])

            $ set_scene_expression(_bj_init, "uncomfortable", blush=1)
            $ set_scene_expression(_bj_other, "uncomfortable")

            python:
                Player.Focus = 0
                _rest_add_score(-2, "event: double BJ other stopped")
                Change_Status(_bj_other, "Love", -5)
                debug_log("[RESTAURANT] Double BJ: other demanded stop. Focus=%d" % Player.Focus)

        # ── IGNORE: other watches (trait-specific) ──
        else:
            python:
                _bj_watch_line, _bj_watch_expr, _bj_watch_blush = _rest_bj_pick_watch_line(_bj_other, _bj_is_gf_scene)
                debug_log("[RESTAURANT] Double BJ: watch line expr=%s blush=%s gf_scene=%s" % (_bj_watch_expr, _bj_watch_blush, _bj_is_gf_scene))
            $ set_scene_expression(_bj_other, _bj_watch_expr, blush=int(_bj_watch_blush))
            $ Say_Line(_bj_other, _tl(_bj_watch_line))

            if _bj_other.has_trait("voyeur"):
                $ set_scene_expression(_bj_other, "smug")
                $ Narration(_tl(_("She leans back, watching your reactions with amusement.")))
            else:
                $ set_scene_expression(_bj_other, "looking_left")
                $ Narration(_tl(_("She sips her drink, trying to look anywhere but at the tablecloth.")))

            # BJ continues to climax
            $ Narration(_tl(_("Under the table, she takes you deeper. Your breath catches.")))
            $ Player.Focus = max(Player.Focus, 70)
            pause 0.3

            $ Narration(_tl(_("You grab the edge of the table. She doesn't slow down.")))
            $ Player.Focus = max(Player.Focus, 90)
            pause 0.3

            $ Narration(_tl(_("Your vision blurs. The table shakes.")))
            $ Player.Focus = 100
            call HardPunch from _call_rest_dbj_punch_watch
            pause 0.3

            $ Narration(_tl(_("Under the table, she swallows everything. Then wipes her mouth.")))
            pause 0.5

            # Initiator slides back up
            $ set_girl_sprite(_bj_init.gid, pose="standing", at_list=[_bj_init_slide_back])
            pause 0.6
            $ set_girl_sprite(_bj_init.gid, pose="standing", at_list=[_bj_init_slot])

            $ set_scene_expression(_bj_init, "smug", blush=1)
            $ Say_Line(_bj_init, _tl(_("Dessert was delicious.")))
            $ set_scene_expression(_bj_init, "happy")

            python:
                Player.Focus = 0
                _bj_init.RegisterAction("bj")
                _rest_add_score(2, "event: double BJ other watched")
                Change_Status(_bj_init, "Love", 5)
                Change_Status(_bj_init, "Obed", 10)
                _girl_lust_gain(_bj_init, 10, 0)
                debug_log("[RESTAURANT] Double BJ: other watched. Focus=%d" % Player.Focus)

        jump .payment

    # ══════════════════════════════════════════════════════
    # GROUP EVENT: SNEAKY BJ
    # Girl A goes to bathroom. Girl B sneaks under table for BJ.
    # Girl A returns, suspicious. Leaves again (forgot phone).
    # Player cums. Girl B slides back up with cum visible.
    # Girl A returns and may notice.
    # ══════════════════════════════════════════════════════
    label .event_sneaky_bj:
        python:
            _sbj_candidates = [g for g in _restaurant_girls if g.Sex_acts.get("bj", 0) > 0 and not g.has_trait("lesbian")]
            _sbj_gf = next((g for g in _restaurant_girls if g.is_dating_player()), None)
            if _sbj_gf:
                _sbj_non_gf_cands = [g for g in _sbj_candidates if g != _sbj_gf]
                if _sbj_non_gf_cands:
                    if _sbj_gf in _sbj_candidates and _sbj_gf.has_trait("cheater"):
                        _sbj_sneaker = _sbj_gf if renpy.random.randint(1, 100) <= 25 else _sbj_non_gf_cands[0]
                    else:
                        _sbj_sneaker = _sbj_non_gf_cands[0]
                else:
                    _sbj_sneaker = _sbj_gf
            else:
                _sbj_sneaker = (
                    next((g for g in _sbj_candidates if g.has_trait("cheater")), None)
                    or next((g for g in _sbj_candidates if g.has_trait("public_fetish")), None)
                    or _sbj_candidates[0]
                )
            _sbj_away = [g for g in _restaurant_girls if g != _sbj_sneaker][0]
            _sbj_sneaker_is_left = (_restaurant_girls[0] == _sbj_sneaker)
            _sbj_sneaker_slot = slot_left if _sbj_sneaker_is_left else slot_center
            _sbj_away_slot = slot_center if _sbj_sneaker_is_left else slot_left
            _sbj_away_slide_under = _rest_slide_under_table if not _sbj_sneaker_is_left else _rest_slide_under_table_left
            _sbj_sneaker_slide_under = _rest_slide_under_table_left if _sbj_sneaker_is_left else _rest_slide_under_table
            _sbj_sneaker_slide_back = _rest_slide_back_up_left if _sbj_sneaker_is_left else _rest_slide_back_up
            _sbj_away_exit = _rest_exit_right if _sbj_sneaker_is_left else _rest_exit_left_from_left
            _sbj_away_enter = _rest_enter_from_right if _sbj_sneaker_is_left else _rest_enter_from_left_to_left
            _sbj_is_gf_away = _sbj_away.is_dating_player()
            debug_log("[RESTAURANT] Sneaky BJ: sneaker=%s, away=%s (gf_away=%s)" % (_sbj_sneaker.gid, _sbj_away.gid, _sbj_is_gf_away))

        # ── 1. Girl A excuses herself to the bathroom ──
        $ set_scene_expression(_sbj_away, "normal")
        $ Say_Line(_sbj_away, _tl(_("Excuse me, I need to use the restroom. Be right back.")))
        $ set_scene_expression(_sbj_away, "happy")

        $ renpy.show(_sbj_away.gid, at_list=[_sbj_away_exit])
        pause 0.8
        $ renpy.hide(_sbj_away.gid)
        pause 0.3

        # ── 2. Girl B gets an idea, slides under table ──
        $ set_scene_expression(_sbj_sneaker, "smug", blush=1)
        $ Say_Line(_sbj_sneaker, _tl(_("Now that she's gone... I've been wanting to do this all night.")))

        $ Narration(_tl(_("Before you can say anything, she ducks under the tablecloth.")))
        $ renpy.show(_sbj_sneaker.gid, at_list=[_sbj_sneaker_slide_under])
        pause 0.6
        $ renpy.hide(_sbj_sneaker.gid)

        $ Narration(_tl(_("You feel her hands sliding up your legs. She unzips you.")))
        pause 0.3
        $ Narration(_tl(_("Her mouth wraps around you. Warm, wet, and deliberate.")))
        $ Player.Focus = max(Player.Focus, 40)
        pause 0.3

        # ── 3. Girl A returns, asks about Girl B ──
        $ set_girl_sprite(_sbj_away.gid, pose="standing", at_list=[_sbj_away_enter])
        pause 0.8
        $ set_girl_sprite(_sbj_away.gid, pose="standing", at_list=[_sbj_away_slot])

        $ set_scene_expression(_sbj_away, "surprised")
        $ Say_Line(_sbj_away, _tl(_("Hey, where did %s go?")) % _sbj_sneaker.Name)
        $ add_player_focus(10)

        $ PlayerChar(_tl(_("Oh, she went outside to take a phone call.")))
        $ set_scene_expression(_sbj_away, "normal")
        $ Say_Line(_sbj_away, _tl(_("Hm, okay.")))
        pause 0.3

        # ── 4. Girl A talks, then remembers her phone ──
        $ set_scene_expression(_sbj_away, "happy")
        $ Say_Line(_sbj_away, _tl(_("Well, as I was saying, I think this semester is going to be...")))
        $ add_player_focus(15)
        pause 0.3

        $ set_scene_expression(_sbj_away, "surprised")
        $ Say_Line(_sbj_away, _tl(_("Oh, crap. I left my phone on the bathroom sink. Hold on, I'll be right back!")))

        # ── 5. Girl A leaves again ──
        $ renpy.show(_sbj_away.gid, at_list=[_sbj_away_exit])
        pause 0.8
        $ renpy.hide(_sbj_away.gid)

        # ── 6. Player cums — face or mouth ──
        $ Narration(_tl(_("The moment she's out of sight, the pace under the table doubles.")))
        $ add_player_focus(20)
        pause 0.3
        $ Narration(_tl(_("You can't hold back anymore.")))
        $ Player.Focus = 100
        call HardPunch from _call_rest_sbj_punch
        pause 0.3

        python:
            _sbj_cum_type = renpy.random.choice(["face", "mouth"])
            _sbj_sneaker.Cum = [_sbj_cum_type]
            debug_log("[RESTAURANT] Sneaky BJ: cum_type=%s" % _sbj_cum_type)

        if _sbj_cum_type == "face":
            $ Narration(_tl(_("You pull back at the last second. It hits her face.")))
        else:
            $ Narration(_tl(_("She takes it all in her mouth, swallowing most of it.")))
        pause 0.3

        $ Narration(_tl(_("She giggles under the table, then scrambles to get back in her seat.")))
        pause 0.3

        # ── Girl B slides back up with cum visible ──
        $ set_girl_sprite(_sbj_sneaker.gid, pose="standing", at_list=[_sbj_sneaker_slide_back])
        pause 0.6
        $ set_girl_sprite(_sbj_sneaker.gid, pose="standing", at_list=[_sbj_sneaker_slot])
        $ set_scene_expression(_sbj_sneaker, "smug", blush=1)
        pause 0.3

        # ── 7. Girl A returns and notices (or not) ──
        $ set_girl_sprite(_sbj_away.gid, pose="standing", at_list=[_sbj_away_enter])
        pause 0.8
        $ set_girl_sprite(_sbj_away.gid, pose="standing", at_list=[_sbj_away_slot])

        $ set_scene_expression(_sbj_away, "happy")
        $ Say_Line(_sbj_away, _tl(_("Found it! Okay, I'm back for real this time.")))
        pause 0.3

        if _sbj_cum_type == "face":
            # Face cum: ALWAYS noticed
            $ set_scene_expression(_sbj_away, "surprised")
            $ Narration(_tl(_("%s looks at %s and freezes.")) % (_sbj_away.Name, _sbj_sneaker.Name))
            pause 0.3

            if _sbj_is_gf_away:
                $ set_scene_expression(_sbj_away, "angry")
                $ Say_Line(_sbj_away, _tl(renpy.random.choice(_REST_SNEAKY_FACE_NOTICED_GF)))
                $ set_scene_expression(_sbj_sneaker, "surprised")
                $ Say_Line(_sbj_sneaker, _tl(renpy.random.choice(_REST_SNEAKY_EXCUSE_FACE)))
                $ set_scene_expression(_sbj_away, "sad")
                $ Say_Line(_sbj_away, _tl(_("I don't believe you. Something happened.")))

                python:
                    Change_Status(_sbj_away, "Love", -10)
                    if hasattr(_sbj_away, "bf_loyalty"):
                        _sbj_away.bf_loyalty = max(0, _sbj_away.bf_loyalty - 30)
                    debug_log("[RESTAURANT] Sneaky BJ: GF noticed face cum, trust hit")
            else:
                $ set_scene_expression(_sbj_away, "surprised")
                $ Say_Line(_sbj_away, _tl(renpy.random.choice(_REST_SNEAKY_FACE_NOTICED)))
                $ set_scene_expression(_sbj_sneaker, "uncomfortable", blush=1)
                $ Say_Line(_sbj_sneaker, _tl(renpy.random.choice(_REST_SNEAKY_EXCUSE_FACE)))
                $ set_scene_expression(_sbj_away, "uncomfortable")
                $ Say_Line(_sbj_away, _tl(_("That doesn't look like food to me...")))

                python:
                    Change_Status(_sbj_away, "Love", -3)
                    debug_log("[RESTAURANT] Sneaky BJ: other noticed face cum")

        else:
            # Mouth cum: chance to not be noticed
            python:
                _sbj_mouth_noticed = renpy.random.randint(1, 100) <= 30
                debug_log("[RESTAURANT] Sneaky BJ: mouth cum noticed=%s" % _sbj_mouth_noticed)

            if _sbj_mouth_noticed:
                $ set_scene_expression(_sbj_away, "surprised")
                $ Narration(_tl(_("%s squints at %s's lips.")) % (_sbj_away.Name, _sbj_sneaker.Name))

                if _sbj_is_gf_away:
                    $ set_scene_expression(_sbj_away, "uncomfortable")
                    $ Say_Line(_sbj_away, _tl(renpy.random.choice(_REST_SNEAKY_MOUTH_NOTICED)))
                    $ set_scene_expression(_sbj_sneaker, "shy", blush=1)
                    $ Say_Line(_sbj_sneaker, _tl(renpy.random.choice(_REST_SNEAKY_EXCUSE_MOUTH)))
                    $ set_scene_expression(_sbj_away, "uncomfortable")
                    $ Say_Line(_sbj_away, _tl(_("Hmm... if you say so.")))

                    python:
                        Change_Status(_sbj_away, "Love", -3)
                        if hasattr(_sbj_away, "bf_loyalty"):
                            _sbj_away.bf_loyalty = max(0, _sbj_away.bf_loyalty - 10)
                        debug_log("[RESTAURANT] Sneaky BJ: GF noticed mouth cum, mild suspicion")
                else:
                    $ set_scene_expression(_sbj_away, "uncomfortable")
                    $ Say_Line(_sbj_away, _tl(renpy.random.choice(_REST_SNEAKY_MOUTH_NOTICED)))
                    $ set_scene_expression(_sbj_sneaker, "shy", blush=1)
                    $ Say_Line(_sbj_sneaker, _tl(renpy.random.choice(_REST_SNEAKY_EXCUSE_MOUTH)))
                    $ set_scene_expression(_sbj_away, "normal")
                    $ Say_Line(_sbj_away, _tl(_("Sure... just wipe it off.")))
            else:
                # Not noticed
                $ set_scene_expression(_sbj_away, "happy")
                $ Say_Line(_sbj_away, _tl(renpy.random.choice(_REST_SNEAKY_MOUTH_NOT_NOTICED)))
                $ set_scene_expression(_sbj_sneaker, "happy")

        # ── Girl B cleans up ──
        python:
            _sbj_cleanup_line, _sbj_cleanup_expr, _sbj_cleanup_blush = _rest_sneaky_cleanup(_sbj_sneaker, _sbj_cum_type)
        $ set_scene_expression(_sbj_sneaker, _sbj_cleanup_expr, blush=_sbj_cleanup_blush)
        $ Narration(_tl(_sbj_cleanup_line))
        pause 0.3

        # ── Clear cum and stats ──
        python:
            _sbj_sneaker.Cum = []
            _sbj_sneaker._mouth_cum_persist = False
            set_girl_sprite(_sbj_sneaker.gid, pose="standing", at_list=[_sbj_sneaker_slot])
            Player.Focus = 0
            _sbj_sneaker.RegisterAction("bj")
            _rest_add_score(2, "event: sneaky BJ")
            Change_Status(_sbj_sneaker, "Love", 5)
            Change_Status(_sbj_sneaker, "Obed", 10)
            _girl_lust_gain(_sbj_sneaker, 10, 0)
            debug_log("[RESTAURANT] Sneaky BJ complete. cum_type=%s" % _sbj_cum_type)

        jump .payment

    # ── PAYMENT ───────────────────────────────────────────
    label .payment:
        $ _rest_bill = restaurant_calc_bill(_restaurant_orders)
        $ Narration(_tl(_("The bill arrives. Total: $%d.")) % _rest_bill)

    label .payment_menu:
        python:
            _rg = _restaurant_girls[0]
            _can_pay = Player.cash >= _rest_bill
            _player_share = RESTAURANT_MENU.get(_restaurant_orders.get("player", "salad"), {}).get("price", 12)
            _can_split = Player.cash >= _player_share
            _pay_text = _tl(_("Pay for everyone")) + " ($%d)" % _rest_bill
            _split_text = _tl(_("Suggest splitting the bill"))
            if _can_pay:
                _lbl_pay_all = _pay_text
            else:
                _lbl_pay_all = "{color=#888}" + _pay_text + "{/color}"
            if _can_split:
                _lbl_split = _split_text
            else:
                _lbl_split = "{color=#888}" + _split_text + "{/color}"
            if len(_restaurant_girls) >= 2:
                _lbl_ask_her = _tl(_("Ask one of them to pay"))
            else:
                _lbl_ask_her = _tl(_("Ask her to pay"))

        menu:
            "[_lbl_pay_all]":
                if _can_pay:
                    $ Player.spend_cash(_rest_bill)
                    python:
                        for _pg in _restaurant_girls:
                            Change_Status(_pg, "Love", RESTAURANT_PAYMENT["player_pays"]["Love"])
                    $ _rest_add_score(1, "player paid")
                    $ set_scene_expression(_rg, "happy")
                    $ Say_Line(_rg, _tl(renpy.random.choice(_REST_PAY_THANKS)))
                    $ set_scene_expression(_rg, "closed_happy")
                else:
                    $ Narration(_tl(_("You check your wallet... not enough to cover everyone.")))
                    jump .payment_menu

            "[_lbl_split]":
                if _can_split:
                    $ Player.spend_cash(_player_share)
                    $ print("[DATE DEBUG] Split bill (no score change)")
                    $ set_scene_expression(_rg, "normal")
                    $ Say_Line(_rg, _tl(renpy.random.choice(_REST_PAY_SPLIT)))
                else:
                    $ Narration(_tl(_("You can't even cover your own share.")))
                    jump .payment_menu

            "[_lbl_ask_her]":
                jump .ask_who_pays

        jump .ending

    label .ask_who_pays:
        if len(_restaurant_girls) >= 2:
            $ Narration(_tl(_("Who should cover the bill?")))
            python:
                _lbl_ask_g0 = _restaurant_girls[0].Name
                _lbl_ask_g1 = _restaurant_girls[1].Name
            menu:
                "[_lbl_ask_g0]":
                    $ _pay_girl = _restaurant_girls[0]
                "[_lbl_ask_g1]":
                    $ _pay_girl = _restaurant_girls[1]
        else:
            $ _pay_girl = _restaurant_girls[0]

        python:
            _pay_key = "ask_rich" if _pay_girl.has_trait("rich") else ("ask_poor" if _pay_girl.has_trait("poor") else "ask_her")
            debug_log("[RESTAURANT] Ask to pay: %s (trait_key=%s)" % (_pay_girl.gid, _pay_key))

        if _pay_girl.has_trait("rich"):
            $ set_scene_expression(_pay_girl, "smug")
            $ Narration(_tl(_("%s pulls out her wallet with a sigh, dropping enough cash on the table without looking at you.")) % _pay_girl.Name)
            $ Say_Line(_pay_girl, _tl(renpy.random.choice(_REST_PAY_RICH)))
            $ set_scene_expression(_pay_girl, "looking_left")
            $ _rest_add_score(-1, "asked rich girl to pay")
            python:
                Change_Status(_pay_girl, "Love", RESTAURANT_PAYMENT["ask_rich"]["Love"])
                Change_Status(_pay_girl, "Obed", RESTAURANT_PAYMENT["ask_rich"]["Obed"])
                for _pg in _restaurant_girls:
                    if _pg != _pay_girl:
                        Change_Status(_pg, "Love", RESTAURANT_PAYMENT["ask_witness"]["Love"])

        elif _pay_girl.has_trait("poor"):
            $ set_scene_expression(_pay_girl, "sad")
            $ Narration(_tl(_("%s slowly reaches for her wallet, her hands trembling as she counts what she has.")) % _pay_girl.Name)
            $ Say_Line(_pay_girl, _tl(renpy.random.choice(_REST_PAY_POOR)))
            $ set_scene_expression(_pay_girl, "uncomfortable")
            $ _rest_add_score(-2, "asked poor girl to pay")
            python:
                Change_Status(_pay_girl, "Love", RESTAURANT_PAYMENT["ask_poor"]["Love"])
                for _pg in _restaurant_girls:
                    if _pg != _pay_girl:
                        Change_Status(_pg, "Love", RESTAURANT_PAYMENT["ask_witness"]["Love"])

        else:
            $ set_scene_expression(_pay_girl, "surprised")
            $ Say_Line(_pay_girl, _tl(renpy.random.choice(_REST_PAY_UPSET)))
            $ set_scene_expression(_pay_girl, "uncomfortable")
            $ _rest_add_score(-1, "asked her to pay")
            python:
                Change_Status(_pay_girl, "Love", RESTAURANT_PAYMENT["ask_her"]["Love"])
                Change_Status(_pay_girl, "Obed", RESTAURANT_PAYMENT["ask_her"]["Obed"])
                for _pg in _restaurant_girls:
                    if _pg != _pay_girl:
                        Change_Status(_pg, "Love", RESTAURANT_PAYMENT["ask_witness"]["Love"])

        jump .ending

    # ── ENDING ────────────────────────────────────────────
    label .ending:
        $ print("[DATE FINAL] ===== SCORE: %d/10 ===== (good=%d, medium=%d) result=%s" % (_rest_score, RESTAURANT_OUTCOMES["good"], RESTAURANT_OUTCOMES["medium"], "GOOD" if _rest_score >= RESTAURANT_OUTCOMES["good"] else ("MEDIUM" if _rest_score >= RESTAURANT_OUTCOMES["medium"] else "BAD")))

        # Advance to night before showing campus
        $ advance_time(1)

        # Return to campus night with girl sprites
        $ store._restaurant_bg = "bg campus_night"
        scene bg campus_night
        with fade
        pause 0.2

        python:
            if len(_restaurant_girls) == 1:
                set_girl_sprite(_restaurant_girls[0].gid, pose="standing", at_list=[slot_center])
            else:
                set_girl_sprite(_restaurant_girls[0].gid, pose="standing", at_list=[slot_left])
                set_girl_sprite(_restaurant_girls[1].gid, pose="standing", at_list=[slot_center])

        $ Narration(_tl(_("You leave the restaurant and walk back towards campus.")))

        $ _rg = _restaurant_girls[0]

        if _rest_score >= RESTAURANT_OUTCOMES["good"]:
            $ set_scene_expression(_rg, "happy")
            $ Say_Line(_rg, _tl(renpy.random.choice(_REST_GOODBYE_GOOD)))
            $ set_scene_expression(_rg, "closed_happy")
        elif _rest_score >= RESTAURANT_OUTCOMES["medium"]:
            $ set_scene_expression(_rg, "normal")
            $ Say_Line(_rg, _tl(renpy.random.choice(_REST_GOODBYE_MED)))
        elif _rest_score >= 2:
            $ set_scene_expression(_rg, "normal")
            $ Say_Line(_rg, _tl(renpy.random.choice(_REST_GOODBYE_OKAY)))
        else:
            $ set_scene_expression(_rg, "sad")
            $ Say_Line(_rg, _tl(renpy.random.choice(_REST_GOODBYE_BAD)))

        # ── Afterglow: apply buff + trait-aware reaction ──
        python:
            if _rest_score >= RESTAURANT_OUTCOMES["good"]:
                _glow_tier = 2
            elif _rest_score >= RESTAURANT_OUTCOMES["medium"]:
                _glow_tier = 1
            else:
                _glow_tier = 0
            _is_okay = (_glow_tier == 0 and _rest_score >= 2)
            for _eg in _restaurant_girls:
                _eg._date_afterglow = _glow_tier
                if _glow_tier > 0:
                    _eg.set_temp_status("date_afterglow", days=1)
                if _is_okay:
                    Change_Status(_eg, "Love", 1)
                else:
                    Change_Status(_eg, "Love", _AFTERGLOW_LOVE[_glow_tier])
                Change_Status(_eg, "Temptation", _AFTERGLOW_TEMPT[_glow_tier])
                if _eg.has_npc_partner() and _glow_tier > 0:
                    _eg._cheat_heat = min(100, getattr(_eg, "_cheat_heat", 0) + _AFTERGLOW_HEAT[_glow_tier])

            _reaction_ctx = _rest_get_reaction_context(_rg, _glow_tier)
            _reaction_pool = _REST_REACTION_LINES.get(_reaction_ctx, []) if _reaction_ctx else []
            debug_log("[RESTAURANT] Afterglow tier=%d ctx=%s heat_gain=%d" % (_glow_tier, str(_reaction_ctx), _AFTERGLOW_HEAT[_glow_tier]))

        if _reaction_pool:
            $ Say_Line(_rg, _format_partner_line(_rg, renpy.random.choice(_reaction_pool)))


        # ── End-of-date menu: group vs solo ──
        if len(_restaurant_girls) >= 2:
            jump .ending_group_menu

    label .ending_solo_menu:
        python:
            _rg = _restaurant_girls[0]
            _lbl_kiss = _tl(_("Ask for a goodbye kiss"))
            _lbl_invite = _tl(_("Invite her to your room"))
            _lbl_walk = _tl(_("Walk her to her room"))
            _lbl_end = _tl(_("Say goodnight"))

        menu:
            "[_lbl_kiss]":
                jump .ending_kiss
            "[_lbl_invite]":
                jump .ending_invite
            "[_lbl_walk]":
                jump .ending_walk
            "[_lbl_end]":
                jump .ending_end

    # ── KISS GOODBYE ─────────────────────────────────────
    label .ending_kiss:
        $ _rg = _restaurant_girls[0]

        # Her story locks the kiss (a girl with a ladder, the act "kiss" above her step): her no in the voice
        # of her step, whatever her Love / Lust. story_lock_result prints the [STORY] log.
        if story_lock_result(_rg, "kiss") is not None:
            $ set_scene_expression(_rg, "normal")
            $ Say_Line(_rg, story_locked_line(_rg, "kiss"))
            jump .ending_cleanup

        python:
            _kiss_accepted = _rg.Love >= 400 or (_rg.Lust >= 40 and _rest_score >= 7)

        if _kiss_accepted:
            $ set_scene_expression(_rg, "shy", blush=1)
            call KISS_Launch(_rg) from _call_rest_kiss_launch
            call KISS_Smooch(_rg) from _call_rest_kiss_smooch
            $ mark_intimacy(_rg, "kiss")
            $ sex_accept_with_temptation(_rg, "kiss")
            $ _notify_cheat_heat(_rg, "kiss", True)
            call KISS_End(_rg) from _call_rest_kiss_end
            $ Change_Status(_rg, "Love", 5)
            if store._cheat_guilt_pending:
                $ _rest_cleanup_vars()
                call cheat_guilt_scene(_rg) from _call_cheat_guilt_rest_kiss
                return
            $ set_scene_expression(_rg, "happy")
            $ Say_Line(_rg, _tl(_("See you tomorrow. Good night.")))
        elif _rest_score < RESTAURANT_OUTCOMES["medium"]:
            $ set_scene_expression(_rg, "uncomfortable")
            $ Say_Line(_rg, _tl(_("Hmm... no. Maybe if the next date goes better, we'll see.")))
            $ set_scene_expression(_rg, "normal")
            $ Change_Status(_rg, "Love", -3)
        else:
            $ set_scene_expression(_rg, "uncomfortable")
            $ Say_Line(_rg, _tl(_("I... not yet. But I had a good time tonight.")))
            $ set_scene_expression(_rg, "normal")
            $ Change_Status(_rg, "Love", -2)

        jump .ending_cleanup

    # ── INVITE TO PLAYER ROOM ────────────────────────────
    label .ending_invite:
        $ _rg = _restaurant_girls[0]

        python:
            _invite_accepted = (_rg.Love >= 600 or _rg.Lust >= 60) and _rest_score >= 7

        if _invite_accepted:
            $ set_scene_expression(_rg, "shy", blush=1)
            $ Say_Line(_rg, _tl(_("Your room? I... okay. Lead the way.")))
            $ Change_Status(_rg, "Love", 5)

            scene bg room_night
            with fade
            pause 0.2
            $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])
            $ set_scene_expression(_rg, "shy", blush=1)
            $ store.CurrentLocation = "room"
            $ store._npc_on_scene = None

            python:
                _lbl_move = _tl(_("Make a move"))
                _lbl_sleep = _tl(_("Just go to sleep"))

            $ store._rest_date_girl = _rg
            menu:
                "[_lbl_move]":
                    $ store._in_event = False
                    $ store._in_sandbox = True
                    $ store._restaurant_bg = None
                    call sex_menu(_rg, "room", store.TimeIndex) from _call_rest_invite_sex
                    jump .ending_post_sleep
                "[_lbl_sleep]":
                    jump .ending_post_sleep
        elif _rest_score < RESTAURANT_OUTCOMES["medium"]:
            $ set_scene_expression(_rg, "uncomfortable")
            $ Say_Line(_rg, _tl(_("Err... no. Maybe on a better date next time, if there is one.")))
            $ set_scene_expression(_rg, "normal")
            $ Change_Status(_rg, "Love", -5)
        else:
            $ set_scene_expression(_rg, "uncomfortable")
            $ Say_Line(_rg, _tl(_("I don't think I'm ready for that... but tonight was nice.")))
            $ set_scene_expression(_rg, "normal")
            $ Change_Status(_rg, "Love", -3)

        jump .ending_cleanup

    # ── WALK HER TO HER ROOM ─────────────────────────────
    label .ending_walk:
        $ _rg = _restaurant_girls[0]

        if _rest_score < RESTAURANT_OUTCOMES["medium"]:
            $ set_scene_expression(_rg, "normal")
            $ Say_Line(_rg, _tl(_("I'll manage on my own. Good night.")))
            $ Change_Status(_rg, "Love", -2)
            jump .ending_cleanup

        $ set_scene_expression(_rg, "happy")
        $ Say_Line(_rg, _tl(_("That's sweet. Yeah, walk with me.")))

        python:
            _her_room = girl_home_loc(_rg)
            _her_bg = _BG_VARIANTS.get(_her_room, {}).get(3, _BG_DEFAULTS.get(_her_room, "bg room_night"))
            store._restaurant_bg = _her_bg
            _walk_npc = get_npc_partner_for(_rg) if _rg.has_npc_partner() else None
            _npc_in_room = _walk_npc and getattr(_walk_npc, "loc", None) == _her_room

        scene expression _her_bg
        with fade
        pause 0.2
        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])

        $ Narration(_tl(_("You walk her to her door.")))

        # ── NPC partner is in the room ──
        if _npc_in_room:
            $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_left])
            $ _walk_npc.show_sprite(slot_right)
            $ _npc_name = _walk_npc.Name
            $ _pname = store.Player.Name

            python:
                _walk_susp = getattr(_walk_npc, "suspicion", 0)
                _walk_love = getattr(_walk_npc, "love_for_girl", 750)
                _ws = "high" if _walk_susp >= 60 else ("mid" if _walk_susp >= 30 else "low")
                _wl = "high" if _walk_love >= 700 else ("mid" if _walk_love >= 400 else "low")
                debug_log("[RESTAURANT] NPC encounter: susp=%d(%s) love=%d(%s)" % (_walk_susp, _ws, _walk_love, _wl))

                _WALK_NARRATION = {
                    "low":  _("Her partner is already inside. %s looks up as the door opens."),
                    "mid":  _("Her partner is already inside. %s watches you both carefully as you walk in."),
                    "high": _("Her partner is already inside. %s's expression darkens the moment he sees you together."),
                }
                _WALK_GIRL_EXPR = {"low": "surprised", "mid": "worried", "high": "uncomfortable"}
                _WALK_GIRL_LINE = {
                    "low":  _("Oh... hey. I didn't expect you to be here."),
                    "mid":  _("Oh... hey. You're still up?"),
                    "high": _("Oh... hey..."),
                }
                _WALK_NPC_QUESTION = {
                    "low":  _("Hey, %s. And %s? Where were you two?"),
                    "mid":  _("Hey, %s... And %s? Where were you two?"),
                    "high": _("%s. Where were you? And why is he here?"),
                }
                _WALK_CLASS_RESP = {
                    ("low", "high"):  _("Oh, okay. That makes sense."),
                    ("low", "mid"):   _("Hm. Alright."),
                    ("low", "low"):   _("Sure. Whatever."),
                    ("mid", "high"):  _("Class? At this hour? ...Fine, if you say so."),
                    ("mid", "mid"):   _("Class? Sure."),
                    ("mid", "low"):   _("Class. Right."),
                    ("high", "high"): _("Class? I want to believe you. I really do."),
                    ("high", "mid"):  _("Class? You think I'm stupid?"),
                    ("high", "low"):  _("Class. Sure. I don't even care anymore."),
                }
                _WALK_WALKING_RESP = {
                    ("low", "high"):  _("Walking around? Hm. Alright then."),
                    ("low", "mid"):   _("Walking around? Okay."),
                    ("low", "low"):   _("Whatever."),
                    ("mid", "high"):  _("Walking around... at this hour? Come on."),
                    ("mid", "mid"):   _("Walking around... at this hour? Right."),
                    ("mid", "low"):   _("Walking around. At night. Sure."),
                    ("high", "high"): _("Walking around? At night? With him? Come on, %s."),
                    ("high", "mid"):  _("Walking around? At night? With him? Really?"),
                    ("high", "low"):  _("Walking around with him. At night. Yeah. Whatever."),
                }
                _WALK_DINNER_RESP = {
                    ("low", "high"):  _("Dinner? That's... thoughtful of you, I guess."),
                    ("low", "mid"):   _("Dinner? Okay then."),
                    ("low", "low"):   _("Dinner. Hm."),
                    ("mid", "high"):  _("Dinner? Just the two of you? I don't love that."),
                    ("mid", "mid"):   _("Dinner? Just the two of you? ...I see."),
                    ("mid", "low"):   _("Dinner together. Great."),
                    ("high", "high"): _("Dinner. Alone. With another guy. And you didn't think to tell me?"),
                    ("high", "mid"):  _("Dinner with him? You're not even trying to hide it anymore."),
                    ("high", "low"):  _("Dinner with him. Of course. Do what you want."),
                }

            $ set_scene_expression(_rg, _WALK_GIRL_EXPR[_ws])
            $ Narration(_tl(_WALK_NARRATION[_ws]) % _npc_name)
            $ Say_Line(_rg, _WALK_GIRL_LINE[_ws])

            python:
                if _ws == "high":
                    _npc_q = _tl(_WALK_NPC_QUESTION[_ws]) % _rg.Name
                else:
                    _npc_q = _tl(_WALK_NPC_QUESTION[_ws]) % (_rg.Name, _pname)
            $ Say_Line(_walk_npc, _npc_q)

            python:
                _lbl_class = _tl(_("We had class running late"))
                _lbl_walking = _tl(_("We were just walking around"))
                _lbl_dinner = _tl(_("I took her to dinner, she deserves it"))

            menu:
                "[_lbl_class]":
                    $ Say_Player(_("We had class running late"))
                    $ set_scene_expression(_rg, "normal")
                    $ Say_Line(_walk_npc, _WALK_CLASS_RESP[(_ws, _wl)])
                    $ Change_NPC_Status(_walk_npc, "friendship_with_player", 5)
                    $ Change_NPC_Status(_walk_npc, "suspicion", 5)
                    $ Change_Status(_rg, "Love", 3)
                    python:
                        _rg.bf_loyalty = min(1000, getattr(_rg, "bf_loyalty", 500) + 10)
                        debug_log("[RESTAURANT] NPC excuse=class, friendship+5, suspicion+5, loyalty+10")

                "[_lbl_walking]":
                    $ Say_Player(_("We were just walking around"))
                    $ set_scene_expression(_rg, "looking_left")
                    python:
                        _walk_resp = _WALK_WALKING_RESP[(_ws, _wl)]
                        if "%s" in _walk_resp:
                            _walk_resp = _tl(_walk_resp) % _rg.Name
                    $ Say_Line(_walk_npc, _walk_resp)
                    $ Change_NPC_Status(_walk_npc, "friendship_with_player", -10)
                    $ Change_NPC_Status(_walk_npc, "suspicion", 15)
                    $ Change_Status(_rg, "Obed", 5)
                    $ debug_log("[RESTAURANT] NPC excuse=walking, friendship-10, suspicion+15, obed+5")

                "[_lbl_dinner]":
                    $ Say_Player(_("I took her to dinner, she deserves it"))
                    $ set_scene_expression(_rg, "embarrassed", blush=1)
                    $ Say_Line(_walk_npc, _WALK_DINNER_RESP[(_ws, _wl)])
                    $ Change_NPC_Status(_walk_npc, "friendship_with_player", -30)
                    $ Change_NPC_Status(_walk_npc, "suspicion", 30)
                    $ Change_NPC_Status(_walk_npc, "love_for_girl", -20)
                    $ Change_Status(_rg, "Obed", 20)
                    $ Change_Status(_rg, "Love", 10)
                    $ debug_log("[RESTAURANT] NPC excuse=dinner, friendship-30, suspicion+30, love-20, obed+20, love+10")

            $ set_scene_expression(_rg, "uncomfortable")
            $ Say_Player(_("Well... good night."))
            $ _walk_npc.hide_sprite()
            jump .ending_cleanup

        # ── Normal flow (no NPC in room) ──
        python:
            _door_kiss = _rg.Love >= 400 or _rg.Lust >= 40
            _door_sex = (_rg.Love >= 500 or _rg.Lust >= 50) and _rest_score >= 7

        if not _door_kiss:
            $ set_scene_expression(_rg, "normal")
            $ Say_Line(_rg, _tl(_("Well... good night. Thanks for dinner.")))
            $ Change_Status(_rg, "Love", 3)
        else:
            $ set_scene_expression(_rg, "shy", blush=1)
            call KISS_Launch(_rg) from _call_rest_walk_kiss_launch
            call KISS_Smooch(_rg) from _call_rest_walk_kiss_smooch
            $ mark_intimacy(_rg, "kiss")
            $ sex_accept_with_temptation(_rg, "kiss")
            $ _notify_cheat_heat(_rg, "kiss", True)
            call KISS_End(_rg) from _call_rest_walk_kiss_end
            $ Change_Status(_rg, "Love", 5)
            if store._cheat_guilt_pending:
                $ _rest_cleanup_vars()
                call cheat_guilt_scene(_rg) from _call_cheat_guilt_rest_walk_kiss
                return

            if _door_sex:
                $ set_scene_expression(_rg, "shy", blush=1)
                $ Say_Line(_rg, _tl(_("Do you... want to come in?")))

                python:
                    _lbl_yes = _tl(_("Go inside"))
                    _lbl_no = _tl(_("Kiss her goodnight and leave"))

                menu:
                    "[_lbl_yes]":
                        $ store.CurrentLocation = _her_room

                        python:
                            _lbl_move = _tl(_("Make a move"))
                            _lbl_sleep = _tl(_("Just go to sleep"))

                        $ store._rest_date_girl = _rg
                        menu:
                            "[_lbl_move]":
                                $ store._in_event = False
                                $ store._in_sandbox = True
                                $ store._restaurant_bg = None
                                call sex_menu(_rg, _her_room, store.TimeIndex) from _call_rest_walk_sex
                                jump .ending_post_sleep
                            "[_lbl_sleep]":
                                jump .ending_post_sleep
                    "[_lbl_no]":
                        $ set_scene_expression(_rg, "happy")
                        $ Say_Line(_rg, _tl(_("Good night. I had a great time.")))

        jump .ending_cleanup

    # ── JUST END THE DATE ─────────────────────────────────
    label .ending_end:
        $ _rg = _restaurant_girls[0]

        if _rest_score >= RESTAURANT_OUTCOMES["good"]:
            $ set_scene_expression(_rg, "surprised")
            $ Say_Line(_rg, _tl(_("You don't want to walk me home?")))

            python:
                _lbl_actually = _tl(_("Actually, yeah. Let me walk you."))
                _lbl_no_gn = _tl(_("No, good night."))

            menu:
                "[_lbl_actually]":
                    jump .ending_walk
                "[_lbl_no_gn]":
                    $ set_scene_expression(_rg, "normal")
                    $ Say_Line(_rg, _tl(_("Oh... okay. Good night then.")))
                    $ Change_Status(_rg, "Love", -3)

        elif _rest_score < RESTAURANT_OUTCOMES["medium"]:
            $ set_scene_expression(_rg, "normal")
            $ Say_Line(_rg, _tl(_("Yeah... good night.")))
            $ Change_Status(_rg, "Love", -5)
        else:
            $ set_scene_expression(_rg, "normal")
            $ Say_Line(_rg, _tl(_("Good night! See you around.")))

        jump .ending_cleanup

    # ── GROUP ENDING MENU (2 girls) ──────────────────────
    label .ending_group_menu:
        python:
            _eg0 = _restaurant_girls[0]
            _eg1 = _restaurant_girls[1]
            _eg_like = min(int(_eg0.Girl_like.get(_eg1.gid, 500)), int(_eg1.Girl_like.get(_eg0.gid, 500)))
            _can_invite_both = (
                _rest_score >= 6
                and (_eg0.Love >= 400 or _eg0.Lust >= 40)
                and (_eg1.Love >= 400 or _eg1.Lust >= 40)
                and _eg_like >= 400
            )
            _can_walk_g0 = _rest_score >= 4 and _eg0.Love >= 200
            _can_walk_g1 = _rest_score >= 4 and _eg1.Love >= 200
            _gray_score = _tl(_("date not that good"))
            _gray_stats = _tl(_("not interested enough"))
            _gray_like = _tl(_("they're not comfortable enough"))

            _lbl_gn_both = _tl(_("Say goodnight and head to your room"))

            _invite_text = _tl(_("Take both to your room"))
            if _can_invite_both:
                _lbl_invite_both = _invite_text
            else:
                if _rest_score < 6:
                    _hint = _gray_score
                elif _eg_like < 400:
                    _hint = _gray_like
                else:
                    _hint = _gray_stats
                _lbl_invite_both = "{color=#888}" + _invite_text + " (" + _hint + "){/color}"

            _walk_g0_text = _tl(_("Go to %s's room alone")) % _eg0.Name
            if _can_walk_g0:
                _lbl_walk_g0 = _walk_g0_text
            else:
                _hint = _gray_score if _rest_score < 4 else _gray_stats
                _lbl_walk_g0 = "{color=#888}" + _walk_g0_text + " (" + _hint + "){/color}"

            _walk_g1_text = _tl(_("Go to %s's room alone")) % _eg1.Name
            if _can_walk_g1:
                _lbl_walk_g1 = _walk_g1_text
            else:
                _hint = _gray_score if _rest_score < 4 else _gray_stats
                _lbl_walk_g1 = "{color=#888}" + _walk_g1_text + " (" + _hint + "){/color}"

            debug_log("[RESTAURANT] Group menu: invite_both=%s (like=%d), walk_g0=%s, walk_g1=%s, score=%d" % (_can_invite_both, _eg_like, _can_walk_g0, _can_walk_g1, _rest_score))

        menu:
            "[_lbl_gn_both]":
                jump .ending_group_goodnight
            "[_lbl_invite_both]":
                if _can_invite_both:
                    jump .ending_group_invite
                else:
                    jump .ending_group_menu
            "[_lbl_walk_g0]":
                if _can_walk_g0:
                    $ _end_target = _eg0
                    $ _end_other = _eg1
                    jump .ending_group_walk_solo
                else:
                    jump .ending_group_menu
            "[_lbl_walk_g1]":
                if _can_walk_g1:
                    $ _end_target = _eg1
                    $ _end_other = _eg0
                    jump .ending_group_walk_solo
                else:
                    jump .ending_group_menu

    # ── GROUP GOODNIGHT ───────────────────────────────────
    label .ending_group_goodnight:
        $ _eg0 = _restaurant_girls[0]
        $ _eg1 = _restaurant_girls[1]

        if _rest_score >= RESTAURANT_OUTCOMES["good"]:
            $ set_scene_expression(_eg0, "happy")
            $ Say_Line(_eg0, _tl(renpy.random.choice(_REST_GOODBYE_GOOD)))
            $ set_scene_expression(_eg1, "happy")
            $ Say_Line(_eg1, _tl(_("Agreed! Good night.")))
        elif _rest_score >= RESTAURANT_OUTCOMES["medium"]:
            $ set_scene_expression(_eg0, "normal")
            $ Say_Line(_eg0, _tl(renpy.random.choice(_REST_GOODBYE_MED)))
            $ set_scene_expression(_eg1, "normal")
        elif _rest_score >= 2:
            $ set_scene_expression(_eg0, "normal")
            $ Say_Line(_eg0, _tl(renpy.random.choice(_REST_GOODBYE_OKAY)))
            $ set_scene_expression(_eg1, "normal")
        else:
            $ set_scene_expression(_eg0, "sad")
            $ Say_Line(_eg0, _tl(renpy.random.choice(_REST_GOODBYE_BAD)))
            $ set_scene_expression(_eg1, "looking_left")

        jump .ending_cleanup

    # ── GROUP INVITE BOTH TO PLAYER ROOM ──────────────────
    label .ending_group_invite:
        $ _eg0 = _restaurant_girls[0]
        $ _eg1 = _restaurant_girls[1]

        python:
            _invite_accepted = (
                (_eg0.Love >= 600 or _eg0.Lust >= 60)
                and (_eg1.Love >= 600 or _eg1.Lust >= 60)
                and _rest_score >= 8
            )
            debug_log("[RESTAURANT] Group invite: accepted=%s (g0 L=%d Lu=%d, g1 L=%d Lu=%d)" % (_invite_accepted, _eg0.Love, _eg0.Lust, _eg1.Love, _eg1.Lust))

        if _invite_accepted:
            $ set_scene_expression(_eg0, "shy", blush=1)
            $ Say_Line(_eg0, _tl(_("Both of us? That's... bold.")))
            $ set_scene_expression(_eg1, "shy", blush=1)
            $ Say_Line(_eg1, _tl(_("I... okay. This should be interesting.")))

            scene bg room_night
            with fade
            pause 0.2
            python:
                set_girl_sprite(_eg0.gid, pose="standing", at_list=[slot_left])
                set_girl_sprite(_eg1.gid, pose="standing", at_list=[slot_center])
                store.CurrentLocation = "room"
                store._npc_on_scene = None
                _lbl_move_g0 = _tl(_("Make a move on %s")) % _eg0.Name
                _lbl_move_g1 = _tl(_("Make a move on %s")) % _eg1.Name
                _lbl_sleep = _tl(_("Just go to sleep"))

            menu:
                "[_lbl_move_g0]":
                    $ _end_target = _eg0
                    $ _end_other = _eg1
                    jump .ending_group_room_sex
                "[_lbl_move_g1]":
                    $ _end_target = _eg1
                    $ _end_other = _eg0
                    jump .ending_group_room_sex
                "[_lbl_sleep]":
                    jump .ending_group_sleep
        else:
            $ set_scene_expression(_eg0, "uncomfortable")
            $ Say_Line(_eg0, _tl(_("That's... a lot to ask. I'll pass.")))
            $ set_scene_expression(_eg1, "uncomfortable")
            python:
                Change_Status(_eg0, "Love", -3)
                Change_Status(_eg1, "Love", -3)

        jump .ending_cleanup

    # ── GROUP ROOM SEX (threesome — other girl watches, switch available) ───
    label .ending_group_room_sex:
        $ set_scene_expression(_end_other, "shy")
        $ set_scene_expression(_end_target, "shy", blush=1)
        $ set_girl_sprite(_end_target.gid, pose="standing", at_list=[slot_center])
        $ set_girl_sprite(_end_other.gid, pose="standing", at_list=[slot_right])

        # Set up threesome: other girl watches, must be invited before switch
        python:
            if not getattr(_end_other, "_saved_outfit", None):
                _end_other.SaveOutfit()
            store._threesome_mode = True
            store._threesome_participants = set([_end_target.gid, _end_other.gid])
            unlock_achievement("the_3_way")
            store._witness_girl = _end_other
            store._witness_watching = True
            store._witness_join_available = False
            store._witness_check_done = False
            debug_log("[RESTAURANT] Threesome setup: target=%s watcher=%s (invite required)" % (_end_target.gid, _end_other.gid))

        $ store._in_event = False
        $ store._in_sandbox = True
        $ store._restaurant_bg = None
        call sex_menu(_end_target, "room", store.TimeIndex) from _call_rest_group_room_sex

        jump .ending_group_sleep

    # ── GROUP WALK TO ONE GIRL'S ROOM ─────────────────────
    label .ending_group_walk_solo:
        $ set_scene_expression(_end_other, "normal")
        $ Say_Line(_end_other, _tl(_("Have fun, you two. Good night!")))
        $ renpy.hide(_end_other.gid)
        python:
            _end_other.loc = girl_home_loc(_end_other)
            _end_other.WearPreset("casual", apply_now=False)

        $ _rg = _end_target
        $ set_scene_expression(_rg, "happy")
        $ Say_Line(_rg, _tl(_("That's sweet. Yeah, walk with me.")))

        python:
            _her_room = girl_home_loc(_rg)
            _her_bg = _BG_VARIANTS.get(_her_room, {}).get(3, _BG_DEFAULTS.get(_her_room, "bg room_night"))
            store._restaurant_bg = _her_bg

        scene expression _her_bg
        with fade
        pause 0.2
        $ set_girl_sprite(_rg.gid, pose="standing", at_list=[slot_center])

        $ Narration(_tl(_("You walk her to her door.")))

        python:
            _door_kiss = _rg.Love >= 400 or _rg.Lust >= 40
            _door_sex = (_rg.Love >= 500 or _rg.Lust >= 50) and _rest_score >= 7

        if not _door_kiss:
            $ set_scene_expression(_rg, "normal")
            $ Say_Line(_rg, _tl(_("Well... good night. Thanks for dinner.")))
            $ Change_Status(_rg, "Love", 3)
        else:
            $ set_scene_expression(_rg, "shy", blush=1)
            call KISS_Launch(_rg) from _call_rest_grp_walk_kiss_launch
            call KISS_Smooch(_rg) from _call_rest_grp_walk_kiss_smooch
            $ mark_intimacy(_rg, "kiss")
            $ sex_accept_with_temptation(_rg, "kiss")
            $ _notify_cheat_heat(_rg, "kiss", True)
            call KISS_End(_rg) from _call_rest_grp_walk_kiss_end
            $ Change_Status(_rg, "Love", 5)
            if store._cheat_guilt_pending:
                $ _rest_cleanup_vars()
                call cheat_guilt_scene(_rg) from _call_cheat_guilt_rest_grp_kiss
                return

            if _door_sex:
                $ set_scene_expression(_rg, "shy", blush=1)
                $ Say_Line(_rg, _tl(_("Do you... want to come in?")))

                python:
                    _lbl_yes = _tl(_("Go inside"))
                    _lbl_no = _tl(_("Kiss her goodnight and leave"))

                menu:
                    "[_lbl_yes]":
                        $ store.CurrentLocation = _her_room
                        python:
                            store._restaurant_girls = [_rg]
                            _lbl_move = _tl(_("Make a move"))
                            _lbl_sleep = _tl(_("Just go to sleep"))
                        menu:
                            "[_lbl_move]":
                                $ store._in_event = False
                                $ store._in_sandbox = True
                                $ store._restaurant_bg = None
                                call sex_menu(_rg, _her_room, store.TimeIndex) from _call_rest_grp_walk_sex
                                jump .ending_post_sleep
                            "[_lbl_sleep]":
                                jump .ending_post_sleep
                    "[_lbl_no]":
                        $ set_scene_expression(_rg, "happy")
                        $ Say_Line(_rg, _tl(_("Good night. I had a great time.")))

        jump .ending_cleanup

    # ── GROUP SLEEP — both girls may sleep with player ──────
    label .ending_group_sleep:
        python:
            _gs_g0 = _restaurant_girls[0]
            _gs_g1 = _restaurant_girls[1]
            _gs_gf = next((g for g in _restaurant_girls if g.is_dating_player()), None)
            _gs_non_gf = next((g for g in _restaurant_girls if g != _gs_gf), None) if _gs_gf else None
            _gs_jealous, _gs_jealous_lvl = _rest_check_jealousy(_restaurant_girls, _rest_attention)

            _gs_g0_ok = _gs_meets_threshold(_gs_g0)
            _gs_g1_ok = _gs_meets_threshold(_gs_g1)
            _gs_gf_ok = _gs_meets_threshold(_gs_gf) if _gs_gf else False

            _gs_both_sleep = False
            _gs_solo_girl = None
            _gs_kicked = None
            _gs_kick_reason = None

        # ── GF blocks the other girl (unless harem-exempt) ──
        if _gs_gf and _gs_non_gf and not (is_harem_exempt(_gs_gf, _gs_non_gf) or _gs_gf.has_trait("polyamorous")):
            if _gs_gf_ok:
                $ set_scene_expression(_gs_gf, "uncomfortable")
                $ Say_Line(_gs_gf, _tl(_("I think it's best if it's just us tonight.")))

                $ set_scene_expression(_gs_non_gf, "normal")
                $ Say_Line(_gs_non_gf, _tl(_("Right... I'll head back. Good night, you two.")))
                python:
                    _gs_kicked = _gs_non_gf
                    _gs_kick_reason = "gf_blocks"
                    _gs_solo_girl = _gs_gf
                    hide_girl_sprite(_gs_non_gf)
                    _gs_non_gf.loc = girl_home_loc(_gs_non_gf)
                    _gs_non_gf.WearPreset("casual", apply_now=False)
                    debug_log("[RESTAURANT] Group sleep: GF %s blocks %s" % (_gs_gf.gid, _gs_non_gf.gid))
            else:
                python:
                    _gs_solo_girl = None
                    debug_log("[RESTAURANT] Group sleep: GF %s too low status to stay" % _gs_gf.gid)

        # ── Jealousy: angry girl leaves ──
        elif _gs_jealous and _gs_jealous_lvl == "angry":
            $ _gs_other_j = [g for g in _restaurant_girls if g != _gs_jealous][0]
            $ set_scene_expression(_gs_jealous, "angry")
            $ Say_Line(_gs_jealous, _tl(_("You know what? I'm going back to my room. Enjoy your night.")))
            python:
                _gs_kicked = _gs_jealous
                _gs_kick_reason = "jealous"
                Change_Status(_gs_jealous, "Love", -5)
                hide_girl_sprite(_gs_jealous)
                _gs_jealous.loc = girl_home_loc(_gs_jealous)
                _gs_jealous.WearPreset("casual", apply_now=False)
                debug_log("[RESTAURANT] Group sleep: %s left angry (jealous)" % _gs_jealous.gid)
            if _gs_meets_threshold(_gs_other_j):
                $ _gs_solo_girl = _gs_other_j
                $ set_scene_expression(_gs_other_j, "uncomfortable")
                $ Say_Line(_gs_other_j, _tl(_("That was awkward... let's just get some rest.")))

        # ── Mild jealousy: she stays but is cold ──
        elif _gs_jealous and _gs_jealous_lvl == "mild" and _gs_g0_ok and _gs_g1_ok:
            $ _gs_both_sleep = True
            $ set_scene_expression(_gs_jealous, "looking_left")
            python:
                Change_Status(_gs_jealous, "Love", -2)
                debug_log("[RESTAURANT] Group sleep: both stay, %s mildly jealous" % _gs_jealous.gid)

        # ── No GF, no jealousy: both can stay if thresholds met ──
        elif _gs_g0_ok and _gs_g1_ok:
            $ _gs_both_sleep = True
            python:
                debug_log("[RESTAURANT] Group sleep: both girls stay")

        # ── Only one meets threshold ──
        elif _gs_g0_ok:
            $ _gs_solo_girl = _gs_g0
            $ set_scene_expression(_gs_g1, "normal")
            $ Say_Line(_gs_g1, _tl(_("I should probably head back. Good night!")))
            python:
                hide_girl_sprite(_gs_g1)
                _gs_g1.loc = girl_home_loc(_gs_g1)
                _gs_g1.WearPreset("casual", apply_now=False)

        elif _gs_g1_ok:
            $ _gs_solo_girl = _gs_g1
            $ set_scene_expression(_gs_g0, "normal")
            $ Say_Line(_gs_g0, _tl(_("I should probably head back. Good night!")))
            python:
                hide_girl_sprite(_gs_g0)
                _gs_g0.loc = girl_home_loc(_gs_g0)
                _gs_g0.WearPreset("casual", apply_now=False)

        # ── Both sleep together ──
        if _gs_both_sleep:
            python:
                for _gsg in _restaurant_girls:
                    _gsg.RegisterAction("slept_together")
                    _gsg._slept_with_player_tonight = True
                    Change_Status(_gsg, "Love", 8)

            $ Narration(_tl(_("The three of you settle in. It's a tight fit, but no one seems to mind.")))

            if _gs_jealous and _gs_jealous_lvl == "mild":
                $ _gs_other_j = [g for g in _restaurant_girls if g != _gs_jealous][0]
                $ set_scene_expression(_gs_other_j, "happy")
                $ Say_Line(_gs_other_j, _tl(_("This is nice.")))
                $ set_scene_expression(_gs_jealous, "normal")
                $ Say_Line(_gs_jealous, _tl(_("...Goodnight.")))
            else:
                $ set_scene_expression(_gs_g0, "happy")
                $ Say_Line(_gs_g0, _tl(_("Goodnight, everyone.")))
                $ set_scene_expression(_gs_g1, "happy")
                $ Say_Line(_gs_g1, _tl(_("Night~")))

            # Day advance (mirrors sleepover .accept_sleepover logic)
            python:
                store._restaurant_day = -1
                store._restaurant_girls = []
                store._restaurant_orders = {}
                store._restaurant_bonus = 0
                store._restaurant_turn = 0
                store._rest_compliments_used = []
                store._rest_attention = {}
                store._restaurant_bg = None
                store._in_event = False
                store._in_sandbox = True

            $ LastPresentGirls = [g for g in ALL_GIRLS if g.loc == CurrentLocation]
            $ Party = []
            $ Player.recharge_energy()
            # ONE central new-day routine (system_time.rpy: start_next_day_manually -> _per_day_cleanup).
            $ start_next_day_manually()

            python:
                # a girl who went into labor overnight is gone (girl_is_away): never pin her to the bed
                _gs_left = [g for g in (_gs_g0, _gs_g1) if girl_is_away(g)]
                for _gs_g in [_gs_g0, _gs_g1]:
                    if _gs_g not in _gs_left:
                        _gs_g.loc = CurrentLocation
                for _gs_g in [_gs_g0, _gs_g1]:
                    _gs_npc = get_npc_partner_for(_gs_g) if (hasattr(_gs_g, "has_npc_partner") and _gs_g.has_npc_partner()) else None
                    if _gs_npc and getattr(_gs_npc, "loc", None) == CurrentLocation:
                        _gs_npc.loc = "campus"

            scene black
            with fade
            pause 0.8

            # ── Morning: wake up with both ──
            call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_gs_wakeup

            if _gs_left:
                # she went into labor overnight. This path returns INTO label Wait, whose step 5c2 plays the
                # birth event (and anything else this rollover made pending) right away.
                if len(_gs_left) == 2:
                    $ Narration(_tl(_("You wake up alone. The bed is already cold.")))
                else:
                    $ Narration(_tl(_("You open your eyes. One side of the bed is empty and already cold.")))
                return

            if getattr(store, "_pregnancy_discovery_pending", None) in (_gs_g0.gid, _gs_g1.gid):
                # her pregnancy discovery is due this morning: that event OPENS with him waking up to an empty
                # bed, so it replaces the morning chatter (label Wait step 5c2 plays it)
                $ print("[RESTAURANT] group sleep: pregnancy discovery due (%s), morning chatter skipped" % store._pregnancy_discovery_pending)
                return

            $ Narration(_tl(_("You open your eyes. Both of them are still here.")))

            python:
                _gs_high_love = any(g.Love >= 600 for g in [_gs_g0, _gs_g1])
                _gs_high_hist = any(_sleepover_history_level(g) >= 2 for g in [_gs_g0, _gs_g1])

            if _gs_high_love and _gs_high_hist:
                $ set_scene_expression(_gs_g0, "happy")
                $ Say_Line(_gs_g0, _tl(_("Morning... that was actually really nice.")))
                $ set_scene_expression(_gs_g1, "shy", blush=1)
                $ Say_Line(_gs_g1, _tl(_("I can't believe we all slept in the same bed.")))
            else:
                $ set_scene_expression(_gs_g0, "normal")
                $ Say_Line(_gs_g0, _tl(_("Good morning.")))
                $ set_scene_expression(_gs_g1, "normal")
                $ Say_Line(_gs_g1, _tl(_("Morning... that was... different.")))

            return

        # ── Solo sleep: one girl stays, use normal sleepover ──
        elif _gs_solo_girl:
            $ _rg = _gs_solo_girl
            $ store._restaurant_girls = [_rg]
            jump .ending_post_sleep

        # ── Neither stays: both go home ──
        else:
            python:
                for _gsg in _restaurant_girls:
                    _gsg.loc = girl_home_loc(_gsg)
                    _gsg.WearPreset("casual", apply_now=False)
                    hide_girl_sprite(_gsg)
                debug_log("[RESTAURANT] Group sleep: neither meets threshold, both leave")
            jump .ending_cleanup

    # ── POST-SEX/SLEEP — standard sleepover + day advance ──
    label .ending_post_sleep:
        if not _restaurant_girls and not getattr(store, "_rest_date_girl", None):
            jump .ending_cleanup
        $ _rg = _restaurant_girls[0] if _restaurant_girls else store._rest_date_girl
        $ _rg.loc = store.CurrentLocation

        # Send second girl home if still present (from threesome / group room)
        if len(_restaurant_girls) > 1:
            python:
                _rest_other = _restaurant_girls[1]
                _rest_other_visible = renpy.showing(_rest_other.gid)
            if _rest_other_visible:
                $ set_scene_expression(_rest_other, "normal")
                $ Say_Line(_rest_other, _tl(_("I'll head back to my room. Good night.")))
                python:
                    _rest_other.loc = girl_home_loc(_rest_other)
                    hide_girl_sprite(_rest_other)

        python:
            store._restaurant_day = -1
            store._restaurant_girls = []
            store._restaurant_orders = {}
            store._restaurant_bonus = 0
            store._restaurant_turn = 0
            store._rest_compliments_used = []
            store._rest_attention = {}
            store._restaurant_bg = None
            store._in_event = False
            store._in_sandbox = True
            debug_log("[STATE] Post-date sleep. Location=%s" % store.CurrentLocation)

        $ _day_before_sleep = Day
        call sleepover_offer(_rg) from _call_rest_sleepover
        if Day == _day_before_sleep:
            call do_sleep from _call_rest_do_sleep
            call Set_Scene(entry=True) from _call_rest_set_scene_postsleep
        return

    # ── CLEANUP ───────────────────────────────────────────
    label .ending_cleanup:
        $ _rest_cleanup_vars()
        $ navigate_to("campus", None)
        call Set_Scene(entry=True) from _call_rest_set_scene_end
        return
