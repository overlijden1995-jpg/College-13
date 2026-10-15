# ============================================================
# shion_netori.rpy... netori, after her turn (docs/plan_shion.md Fase 6)
#
# A married girl (trait "married") whose husband is a contact of his (GIRLS_CONFIG "husband": the store name of a
# FamilyContact, Shion = "Dad") and who is WILLING (netori_willing: a girl with a story from the step that opens
# "netori", story_steps.rpy; any other girl from NETORI_WILLING_LOVE):
#   THE RING: "On her wedding ring" in his cum menu of the handjob (PlayerCumMenu_Outside_Oral) and of the rimjob
#     (PlayerCumMenu_Hand). Willing: she holds up her hand for it (achievement "till_death"). Not willing yet: he
#     does it anyway and she is furious.
#   THE CALL: in his dorm room at Night, during sex with him, she calls her husband (sub-event "netori_call",
#     SubEvents.rpy) to tell him she is staying at his son's dorm "to help him study". Two beats: he stays still,
#     keeps moving or fucks her hard; every noise is a risk (NETORI_CALL_NOISE). Too much noise and the husband
#     grows suspicious (husband.suspicion) and texts the next morning (DAD_TEXTS "netori_noise"). Once a day.
#     The same label plays the INCOMING call (incoming=True: HE calls HER, the "in_" lines): her later visits
#     to his dorm (stepmom_story.rpy), before she is willing.
#   SHE COMES TO HIS DORM: from FEMDOM_TURN_DORM_STAGE she accepts his phone invitation to his dorm room in the
#     Evening / Night (femdom_turn.rpy, girl_comes_to_his_dorm): the room the call happens in.
# Lines: NETORI_LINES[gid] (her), NETORI_HUSBAND_LINES[husband gid] (him), the ring lines in SCENE_LINES
# ("cum_ring.<scene>.<gid>", "cum_ring_refused.<scene>.<gid>").
# ============================================================

init python:

    NETORI_WILLING_LOVE = 800               # a married girl who is not a canon femdom: willing from this Love
    NETORI_CALL_WEIGHT = 35                 # its weight in the sub-event roll
    NETORI_CALL_NOISE = {"still": 0, "slow": 1, "hard": 3}          # noise of each choice
    NETORI_CALL_LUST = {"still": 2, "slow": 6, "hard": 12}          # her lust from each choice
    NETORI_CALL_HEARD = 3                   # noise from which he hears something (this beat)
    NETORI_CALL_SUSPICION = (0, 0, 5, 10, 20, 30, 40)               # husband suspicion by total noise (0..6)
    NETORI_CALL_TEXT_NOISE = 3              # total noise from which he texts the next morning

    # Her side of it. Face-to-face lines are (face, line).
    NETORI_LINES = {
        "shion": {
            "call_start": [
                ("smirk", _("Don't stop. Just keep quiet for a minute.")),
                ("smug", _("Shh. Stay right where you are. I have a call to make.")),
            ],
            "lie": [
                _("Hi, honey. Don't wait up tonight. I'm staying at your son's dorm."),
                _("Darling, I won't be home tonight. Your son needs my help."),
            ],
            "lie_reason": [
                _("He has an exam coming. I'm helping him study."),
                _("He's so far behind on his studies. Someone has to take him in hand."),
            ],
            "still": [
                _("He's being very... good tonight. Very obedient."),
                _("Oh, he's behaving. For once."),
            ],
            "slow": [
                _("He's... mmh... working very hard tonight..."),
                _("We're going over it... slowly... very thoroughly..."),
            ],
            "hard": [
                _("Ah-! ...No, nothing. I just... stubbed my toe on his desk."),
                _("Nnh-! ...Sorry, honey. His chair is... terrible."),
            ],
            "goodbye": [
                _("Love you too, honey... goodnight."),
                _("Goodnight, darling. Don't wait up."),
            ],
            "goodbye_hard": [
                _("Goodnight... hah... I have to go. Now."),
            ],
            "hang_up": [
                ("sexy", _("Your father says goodnight. ...Now fuck me like he never could.")),
                ("smirk", _("He thinks I'm tutoring you. In a way, I am.")),
                ("smug", _("Good boy. He didn't suspect a thing. ...Don't you dare stop now.")),
            ],
            "hang_up_heard": [
                ("embarrassed", _("You little bastard... he heard that. ...Do it again.")),
                ("annoyed", _("Are you trying to get us caught? ...God, that was hot.")),
            ],
            # HE calls HER (incoming=True): the night she ran from a fight with him to his son's dorm
            "in_call_start": [
                ("serious", _("Not a sound. I mean it.")),
                ("annoyed", _("Don't. Move. It's your father.")),
            ],
            "in_lie": [
                _("I needed some air, honey. I'm just driving around."),
                _("I'm fine. I couldn't sleep, so I went for a drive."),
            ],
            "in_lie_reason": [
                _("Just clearing my head. You know how I get."),
                _("Nothing's wrong. I just needed to be alone for a while."),
            ],
            "in_still": [
                _("No, I'm alone. It's just the radio."),
                _("I'm parked. It's quiet here. I'm fine."),
            ],
            "in_slow": [
                _("I'm... mmh... fine. The road is just... bumpy."),
                _("Nothing, honey... I'm just... tired."),
            ],
            "in_hard": [
                _("Ah-! ...No, it's nothing. A pothole. I hit a pothole."),
                _("Nnh-! ...Sorry. Somebody cut me off."),
            ],
            "in_goodbye": [
                _("I'll be home soon. Go back to sleep."),
                _("Don't wait up, honey. I won't be long."),
            ],
            "in_goodbye_hard": [
                _("I have to go. I'm... driving. Bye."),
            ],
            "in_hang_up": [
                ("embarrassed", _("...If he ever finds out, we're both dead. Don't stop.")),
                ("serious", _("He believed it. Of course he did. He always does.")),
            ],
            "in_hang_up_heard": [
                ("annoyed", _("Are you insane? He almost heard you! ...God. Again.")),
                ("embarrassed", _("You did that on purpose. ...I hate that I liked it.")),
            ],
        },
    }

    # Her husband's side (Character with his name). "%s" in "noise" lines never: plain lines.
    NETORI_HUSBAND_LINES = {
        "dad": {
            "answer": [
                _("Hey, honey! Everything okay?"),
                _("Shion? It's late. Is everything alright?"),
            ],
            "reply_lie": [
                _("That's so sweet of you. I knew you two would get along eventually."),
                _("Really? Thank you, honey. He needs a firm hand."),
            ],
            "noise": [
                _("Honey? What was that?"),
                _("Are you okay? You sound out of breath."),
            ],
            "goodbye": [
                _("Okay, don't stay up too late. Tell him I said good luck. Love you!"),
                _("Alright. Make sure he actually studies. Love you."),
            ],
            "suspicious": [
                _("...Alright. You sound strange tonight, Shion. Call me if you need anything."),
            ],
            # he calls her (incoming=True), the night she stormed out after their fight
            "in_open": [
                _("Honey? Where are you? It's almost midnight."),
                _("Shion? I woke up and you were gone. Where are you?"),
            ],
            "in_reply_lie": [
                _("Okay... I'm sorry about earlier. I shouldn't have said that."),
                _("Alright. Drive safe. I hate it when you go out this late."),
            ],
            "in_goodbye": [
                _("Okay. Come home soon. Love you."),
                _("Alright, alright. Don't stay out too late. Love you."),
            ],
            "in_suspicious": [
                _("...Shion, you sound strange. Where are you, really? ...Fine. Just come home."),
            ],
        },
    }

    # The narration around a call: "" = she calls him, "in_" = he calls her
    NETORI_CALL_NARRATION = {
        "": {
            "start": _("She reaches for her phone, puts it on speaker and dials. It rings twice."),
            "end": _("She hangs up and drops the phone on your bed."),
        },
        "in_": {
            "start": _("Her phone buzzes on your nightstand. She looks at the screen and goes still. It's your father."),
            "end": _("She ends the call and stares at the phone for a long second."),
        },
    }

    def girl_wears_ring(girl):
        """She is married: a wedding ring on her hand."""
        return bool(girl) and girl.has_trait("married")

    def netori_willing(girl):
        """A married girl who betrays her husband WITH him: a girl with a story from the step that opens "netori"
        (story_steps.rpy), any other girl from NETORI_WILLING_LOVE."""
        if not girl_wears_ring(girl):
            return False
        if story_key(girl) is not None:
            return story_act_open(girl, "netori")
        return getattr(girl, "Love", 0) >= NETORI_WILLING_LOVE

    def girl_husband(girl):
        """Her husband, a contact of his (GIRLS_CONFIG "husband": the store name of a FamilyContact), or None."""
        _name = GIRLS_CONFIG.get(getattr(girl, "gid", None), {}).get("husband")
        return getattr(store, _name, None) if _name else None

    def netori_pick(table, key, who):
        _pool = (table.get(who) or {}).get(key) or ()
        return renpy.random.choice(_pool) if _pool else None

    def _se_can_netori_call(girl, scene_type):
        """Sub-event "netori_call": a willing married girl, with a husband to call, in HIS dorm room at Night, once a
        day."""
        return (netori_willing(girl) and girl_husband(girl) is not None and girl.gid in NETORI_LINES
                and store.CurrentLocation == "room" and store.TimeIndex == NIGHT_INDEX
                and getattr(girl, "_netori_call_day", -1) != store.Day)

# Her words when his cum lands on her wedding ring (_netori_ring_cum, _cum_say_line "ring" / "ring_refused")
init 2 python:

    SCENE_LINES.update({
        "cum_ring.hj.shion": [
            _("On the ring... the one your father put on my finger. Good boy."),
            _("Look at it. His ring, your cum. That's what this marriage is now."),
            _("Mmm... I won't even wash it off. He'll never know."),
        ],
        "cum_ring.rj.shion": [
            _("On my ring? ...You filthy boy. I love it."),
            _("His ring, covered in you. Perfect."),
        ],
        "cum_ring_refused.hj.shion": [
            _("My RING?! You little bastard... that was a gift from your father!"),
            _("Get it off! Get it OFF! Do you have any idea what you just did?"),
        ],
        "cum_ring_refused.rj.shion": [
            _("On my ring?! You disgusting... that ring is from your father!"),
            _("You did that on purpose. You'll pay for this, boy. Dearly."),
        ],
    })

# ============================================================
# His cum on her wedding ring (the handjob / rimjob cum menus)
# ============================================================
label _netori_ring_cum(girl, scene_type):
    python:
        _nr_willing = netori_willing(girl)
        print("[NETORI] ring: %s in %s, willing=%s" % (girl.gid, scene_type, _nr_willing))
    call _cum_dispatch_anim(girl, scene_type) from _call__cum_dispatch_anim_ring
    $ process_cum(girl, scene_type, "ring", ["hand"])
    if _nr_willing:
        $ set_scene_expression(girl, "sexy", blush="2")
        $ _cum_say_line(girl, "ring", scene_type)
        $ apply_cum_bonuses(girl, "cum_outside")
        $ Change_Status(girl, "Love", 5)
        $ Change_Status(girl, "Obed", 5)
        $ unlock_achievement("till_death")
    else:
        $ set_scene_expression(girl, "angry")
        $ _cum_say_line(girl, "ring_refused", scene_type)
        $ Change_Status(girl, "Love", -15)
        $ Change_Status(girl, "Inbt", 5)
    return

# ============================================================
# She calls her husband during sex (sub-event "netori_call", SubEvents.rpy)
# ============================================================
label SubEvent_NetoriCall(girl, scene_type, incoming=False):
    python:
        girl._netori_call_day = Day
        _nc_h = girl_husband(girl)
        _nc_who = Character(_nc_h.Name, who_color=_nc_h.color)
        _nc_noise = 0
        _nc_heard = False
        # "in_": HE calls HER (her lines and his are the "in_" keys)
        _nc_k = "in_" if incoming else ""
        print("[NETORI] call: %s %s %s from his dorm (%s, Day %d)" % (girl.gid, "gets a call from" if incoming else "calls", _nc_h.gid, scene_type, Day))
    if incoming:
        $ Narration(NETORI_CALL_NARRATION[_nc_k]["start"])
        python:
            _nc_face, _nc_line = netori_pick(NETORI_LINES, "in_call_start", girl.gid)
        $ set_scene_expression(girl, _nc_face)
        $ Say_Line(girl, _nc_line)
        $ renpy.say(_nc_who, _tl(netori_pick(NETORI_HUSBAND_LINES, "in_open", _nc_h.gid)))
    else:
        python:
            _nc_face, _nc_line = netori_pick(NETORI_LINES, "call_start", girl.gid)
        $ set_scene_expression(girl, _nc_face)
        $ Say_Line(girl, _nc_line)
        $ Narration(NETORI_CALL_NARRATION[_nc_k]["start"])
        $ renpy.say(_nc_who, _tl(netori_pick(NETORI_HUSBAND_LINES, "answer", _nc_h.gid)))
    $ set_scene_expression(girl, "serious" if incoming else "smug")
    $ Say_Line(girl, netori_pick(NETORI_LINES, _nc_k + "lie", girl.gid))
    $ renpy.say(_nc_who, _tl(netori_pick(NETORI_HUSBAND_LINES, _nc_k + "reply_lie", _nc_h.gid)))

    # two beats: he decides how quiet he is
    $ _nc_beat = 0
    while _nc_beat < 2:
        menu:
            "Stay still":
                $ _nc_choice = "still"
            "Keep moving, slowly":
                $ _nc_choice = "slow"
            "Fuck her hard":
                $ _nc_choice = "hard"
        python:
            _nc_noise += NETORI_CALL_NOISE[_nc_choice]
            _girl_lust_gain(girl, NETORI_CALL_LUST[_nc_choice], 2)
            print("[NETORI] call beat %d: %s (noise %d)" % (_nc_beat + 1, _nc_choice, _nc_noise))
        if _nc_choice == "hard":
            $ set_scene_expression(girl, "pleasure_intense", blush="3")
        elif _nc_choice == "slow":
            $ set_scene_expression(girl, "pleasure", blush="2")
        else:
            $ set_scene_expression(girl, "smirk")
        if _nc_beat == 0:
            $ Say_Line(girl, netori_pick(NETORI_LINES, _nc_k + (_nc_choice if _nc_choice != "still" else "lie_reason"), girl.gid))
        else:
            $ Say_Line(girl, netori_pick(NETORI_LINES, _nc_k + _nc_choice, girl.gid))
        if NETORI_CALL_NOISE[_nc_choice] >= NETORI_CALL_HEARD:
            $ _nc_heard = True
            $ renpy.say(_nc_who, _tl(netori_pick(NETORI_HUSBAND_LINES, "noise", _nc_h.gid)))
        $ _nc_beat += 1

    # goodbye
    if _nc_noise >= NETORI_CALL_TEXT_NOISE:
        $ renpy.say(_nc_who, _tl(netori_pick(NETORI_HUSBAND_LINES, _nc_k + "suspicious", _nc_h.gid)))
        $ Say_Line(girl, netori_pick(NETORI_LINES, _nc_k + "goodbye_hard", girl.gid))
    else:
        $ renpy.say(_nc_who, _tl(netori_pick(NETORI_HUSBAND_LINES, _nc_k + "goodbye", _nc_h.gid)))
        $ Say_Line(girl, netori_pick(NETORI_LINES, _nc_k + "goodbye", girl.gid))
    $ Narration(NETORI_CALL_NARRATION[_nc_k]["end"])

    python:
        _nc_susp = NETORI_CALL_SUSPICION[min(_nc_noise, len(NETORI_CALL_SUSPICION) - 1)]
        _nc_h.suspicion = int(getattr(_nc_h, "suspicion", 0) or 0) + _nc_susp
        if _nc_noise >= NETORI_CALL_TEXT_NOISE and _nc_h is store.Dad and store._dad_text_pending is None:
            store._dad_text_pending = "netori_noise"
        print("[NETORI] call over: noise %d, %s suspicion +%d -> %d" % (_nc_noise, _nc_h.gid, _nc_susp, _nc_h.suspicion))
        _nc_face, _nc_line = netori_pick(NETORI_LINES, _nc_k + ("hang_up_heard" if _nc_heard else "hang_up"), girl.gid)
    $ set_scene_expression(girl, _nc_face, blush="2")
    $ Say_Line(girl, _nc_line)
    if incoming:
        # she lied to him with his son inside her, and it did something to her
        $ Change_Status(girl, "Inbt", 5)
    else:
        $ Change_Status(girl, "Love", 5)
        $ unlock_achievement("study_session")
    return
