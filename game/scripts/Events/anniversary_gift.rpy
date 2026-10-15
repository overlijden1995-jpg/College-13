# ============================================
# ANNIVERSARY GIFT: Scripted NTR Event
# One-time cutscene: exhibitionist+cheater girl
# manipulates player through escalating sex
# while NPC partner watches.
# ============================================

default _ag_done = False
default _ag_scheduled_day = -1
default _ag_girl_gid = None
default _ag_cooldown_until = -1
default _time_locked = False

init python:

    # ── Daily morning check (called from _per_day_cleanup) ──

    def _ag_daily_check():
        print("[AG] _ag_daily_check called. done=%s scheduled=%s Day=%s" % (store._ag_done, store._ag_scheduled_day, store.Day))
        if store._ag_done:
            print("[AG] BLOCKED: _ag_done is True")
            return
        if 0 < store._ag_scheduled_day < store.Day:
            # the scheduled day passed without the event firing (he was not alone in his room): it stayed
            # "scheduled" forever and the gift could never happen again (same fix as _bet_daily_check)
            print("[AG] scheduled day %d missed, unscheduling" % store._ag_scheduled_day)
            store._ag_scheduled_day = -1
            store._ag_girl_gid = None
        if store._ag_scheduled_day > 0:
            print("[AG] BLOCKED: already scheduled day=%s" % store._ag_scheduled_day)
            return
        if store.Day < 7:
            print("[AG] BLOCKED: Day %s < 7" % store.Day)
            return
        if store._ag_cooldown_until > 0 and store.Day < store._ag_cooldown_until:
            print("[AG] BLOCKED: cooldown until day %s" % store._ag_cooldown_until)
            return

        for girl in ALL_GIRLS:
            print("[AG] Checking %s: traits=%s partner=%s Sex_acts=%s" % (girl.gid, list(girl.traits), girl.has_npc_partner(), dict(girl.Sex_acts)))
            if girl_is_away(girl):
                print("[AG] %s SKIP: away (giving birth)" % girl.gid)
                continue
            if not girl.has_trait("exhibitionist"):
                print("[AG] %s SKIP: no exhibitionist" % girl.gid)
                continue
            if not girl.has_trait("cheater"):
                print("[AG] %s SKIP: no cheater" % girl.gid)
                continue
            if not girl.has_npc_partner():
                print("[AG] %s SKIP: no npc partner" % girl.gid)
                continue
            _npc = get_npc_partner_for(girl)
            if _npc is None:
                print("[AG] %s SKIP: get_npc_partner_for returned None" % girl.gid)
                continue
            if girl.has_trait("virgin"):
                print("[AG] %s SKIP: still a virgin" % girl.gid)
                continue
            _has_sex = girl_had_sex(girl)
            if not _has_sex:
                print("[AG] %s SKIP: no vaginal sex with player" % girl.gid)
                continue
            _score = ApprovalCheck(girl, T=1150, Type="LOI", Spread=170, Variation=0, Check=True, Location="room")
            if _score < 1150:
                print("[AG] %s SKIP: score %s < 1150" % (girl.gid, _score))
                continue

            store._ag_scheduled_day = store.Day
            store._ag_girl_gid = girl.gid
            print("[AG] Scheduled for today. Girl=%s Day=%d score=%s" % (girl.gid, store.Day, _score))
            return

    # ── Dialogue pools ──

    _AG_DIALOGUE = {
        "arrival": {
            "girl_intro_1": [
                _("Hey, [Player.Name]. My %(pl)s agreed to give me a little anniversary gift and I want your help."),
                _("Hey, [Player.Name]! So, my %(pl)s is letting me get a massage as an anniversary gift and I need your help."),
            ],
            "girl_intro_2": [
                _("I love massages, but %(pp)s doesn't enjoy giving them much, so %(pp)s let me have one. But %(pp)s wants to watch to make sure I'll be safe, okay?"),
                _("%(Pp)s doesn't like giving massages, so %(pp)s said someone else could do it. %(Pp)s just wants to watch and make sure everything's fine."),
            ],
            "npc_demand": [
                _("JUST a massage! No funny business!"),
                _("ONLY a massage, understand?! Nothing more!"),
            ],
            "player_accept": [
                _("Uh? Well... sure. I guess."),
            ],
            "narration_npc_anxious": [
                _("You look at [_ag_npc.name]. %(Pp)s seems anxious."),
            ],
            "narration_girl_position": [
                _("[_ag_girl.Name] positions herself for the massage."),
            ],
            "girl_ready": [
                _("Ready, you can start!"),
            ],
        },
        "massage_1": {
            "girl": [
                _("Mmm... yeah, right there. You're pretty good at this."),
                _("Ooh... that feels nice. Keep going."),
                _("A little harder... more pressure... yeah, like that."),
            ],
        },
        "strip": {
            "girl_ask": [
                _("Hey, [_ag_npc.name]. It feels so good... Is it okay if I take my clothes off? The skin contact will feel so much better."),
                _("Mmm, [_ag_npc.name]... this is amazing. Can I take off my clothes? It'll feel way better on bare skin."),
            ],
            "npc_accept": [
                _("The... the clothes...? I... yes, okay..."),
                _("Take off your... I... fine, okay..."),
            ],
            "narration": [
                _("She's completely naked now."),
            ],
        },
        "massage_2": {
            "girl": [
                _("God... your hands feel amazing without the clothes in the way..."),
                _("Mmm... lower... yeah, right there..."),
                _("So much better like this, don't you think?"),
            ],
        },
        "rub": {
            "narration_bulge": [
                _("[_ag_girl.Name] looks at your crotch. She clearly notices the bulge."),
            ],
            "girl_request": [
                _("Baby... I'd like to be massaged somewhere else... He has something so big... Can I rub just a little bit? Just to feel better."),
                _("Babe... I want a different kind of massage... He's so big down there... Can I just grind on it a little? Just to feel good."),
            ],
            "npc_accept": [
                _("Just... Just rub? But... He... He needs to promise not to go in... You need to remember you are mine..."),
            ],
            "girl_reassure": [
                _("Of course babe... It is just to feel good, he is helping us in the anniversary only."),
            ],
            "narration_unzip": [
                _("She opens your fly and positions herself."),
            ],
            "girl_tease": [
                _("Just... rubbing... A huge cock, so close to my little pussy..."),
                _("Mmm... it feels so good to grind on it... just a little more..."),
            ],
            "npc_worried": [
                _("That's... that's not just rubbing anymore..."),
            ],
        },
        "tip": {
            "girl_ask": [
                _("Oh... [_ag_npc.name]... Can he just put the tip? Just a little bit, [Player.Name] will behave, it is just so I can feel him better... I'm so wet."),
            ],
            "npc_deny": [
                _("No babe... That... That would be too far... It is... Dangerous."),
            ],
            "girl_convince": [
                _("No baby, it is just the tip. Just a little bit inside, he won't push it further..."),
            ],
            "narration_insert": [
                _("[_ag_girl.Name] puts her hands between her legs and positions your cock inside her."),
            ],
            "narration_npc_frozen": [
                _("[_ag_npc.name] is frozen, eyes wide open, mouth hanging slightly."),
            ],
            "girl_continue": [
                _("Mmm... just the tip... it barely counts..."),
                _("See? Nothing is happening. Everything's fine, right [_ag_npc.name]?"),
            ],
            "npc_breaking": [
                _("I... I can't look away... why can't I look away..."),
            ],
        },
        "condom_sex": {
            "girl_ahegao_moan": [
                _("Ahhh... mmm... aaahh..."),
            ],
            "girl_extra_moan": [
                _("Mmmm... ahh... it feels so good... I want more..."),
            ],
            "girl_beg": [
                _("Everything... I want everything... Please baby, just a little, I need to feel it."),
                _("All of it... I want all of it... Please babe, just a little more, I need to feel him."),
            ],
            "npc_condom": [
                _("I... my... yes, okay. But with a condom, [Player.Name]. Use this one. Be careful."),
                _("I... fine... okay. But put a condom on, [Player.Name]. Take this. Be careful."),
            ],
            "narration_condom_handoff": [
                _("You take the condom from %(poss)s hand. %(Pp)s is shaking."),
            ],
            "girl_moan_speed2": [
                _("Ahhh... yes... I can feel it even with the condom... so deep..."),
                _("Mmm... so good... harder, [Player.Name]... don't stop..."),
            ],
            "girl_speed": [
                _("Faster... go faster... oh God, yes..."),
                _("Don't slow down... keep going... harder..."),
            ],
            "gf_npc_demand": [
                _("Fine. But he has to pull out, [Player.Name]. You hear me? Don't you dare finish inside her."),
                _("Okay... but you better pull out, [Player.Name]. Promise me. Not inside her."),
            ],
            "gf_narration_demand": [
                _("%(Pp)s stares at you, shaking. %(Pp)s means it."),
            ],
            "gf_girl_moan": [
                _("Ahhh... yes... I can feel everything... so deep..."),
            ],
        },
        "raw": {
            "girl_remove": [
                _("I can't take it anymore... I want it without a condom, I need to feel his skin in my pussy. I'll make him pull out before he cums, I promise."),
                _("I can't handle this anymore... I want it raw, I need to feel him inside me for real. I'll make sure he pulls out, I promise."),
            ],
            "gf_girl_break_promise": [
                _("Don't pull out... forget the promise... I want to feel everything, I need him to fill me up."),
                _("Screw pulling out... I don't care anymore... don't stop, I want it all inside me."),
            ],
            "narration_npc": [
                _("[_ag_npc.name] has %(poss)s hands inside %(poss)s pants, clearly sweating."),
            ],
            "girl_dirty": [
                _("Fuck, yes, like that, faster. He's all inside my pussy babe, he's fucking me so hard."),
                _("Oh God yes, like that, faster. He's deep in my pussy babe, he's pounding me hard."),
            ],
            "npc_command": [
                _("[_ag_girl.Name]! I'm going crazy, but this is so good! [Player.Name], FASTER! FUCK HER HARD!"),
                _("[_ag_girl.Name]! I'm losing my mind, but it feels so good! [Player.Name], HARDER! DON'T STOP!"),
            ],
            "girl_speed3": [
                _("Oh fuck... he's so deep... I can't... I can't stop..."),
                _("Harder... please... I'm going to lose my mind..."),
            ],
        },
        "creampie": {
            "player": [
                _("I... I'm going to cum, I can't hold it anymore."),
            ],
            "girl_inside": [
                _("Inside! Fill me with cum, cum everything inside me!"),
                _("Inside! Don't pull out! Fill me up, I want every drop!"),
            ],
            "narration": [
                _("You can't think anymore and just let go."),
            ],
            "girl_feel_cum": [
                _("Babe... I can feel all his cum in my pussy... it's flooding..."),
                _("[_ag_npc.name]... he came so much inside me... I can feel it all..."),
            ],
        },
        "post": {
            "girl_show": [
                _("Look, baby. He filled my pussy with cum after fucking it... It's dripping, that's how full he left my little pussy..."),
                _("Look at this, babe. He came inside my pussy and filled it up... It's dripping out, that's how much he left in me..."),
            ],
            "narration_npc": [
                _("You look at [_ag_npc.name]. You realize you weren't the only one who came watching this."),
            ],
            "girl_dismiss": [
                _("Thanks, [Player.Name]. Now, can you give us some alone time? %(Pp)s has a little cleanup job to do on me."),
                _("Thank you, [Player.Name]. Now please, give us some privacy. %(Pp)s needs to take care of a little cleaning down here."),
            ],
        },
    }


# ── Check label (called from Wait label) ──

label anniversary_gift_check:
    if _ag_done:
        return
    if _ag_scheduled_day != Day:
        return
    if _ag_girl_gid is None:
        return
    if CurrentLocation != "room":
        return
    if len(Party) > 0 or any(getattr(g, "loc", None) == "room" for g in ALL_GIRLS):
        return

    python:
        _ag_girl = GIRL_BY_ID.get(store._ag_girl_gid)
        if _ag_girl is None:
            store._ag_done = True
        elif girl_is_away(_ag_girl):
            # she cannot text "come to my room" from her parents' place: back to the scheduler for later
            print("[AG] %s is away: unscheduled, can be scheduled again when she is back" % _ag_girl.gid)
            store._ag_scheduled_day = -1
            store._ag_girl_gid = None
    if _ag_done or _ag_girl_gid is None:
        return

    python:
        _ag_npc = get_npc_partner_for(_ag_girl)
        if _ag_npc is None:
            store._ag_done = True
    if _ag_done:
        return

    # ── Phone notification ──
    play sound "audio/Notification.mp3" noloop
    "Your phone buzzes. Someone sent you a message."

    # ── Open phone chat with typing animation ──
    $ phone_add_msg(_ag_girl.gid, _ag_girl.gid, None, "typing")
    call screen phone_chat_screen(_ag_girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(_ag_girl.gid)
        if _t and _t[-1].get("type") == "typing":
            _t.pop()
        _ag_invite_msg = _format_partner_line(_ag_girl, _tl(_("Hey, come to my room. I want to give my %(pl)s an anniversary gift.")))
        phone_add_msg(_ag_girl.gid, _ag_girl.gid, _ag_invite_msg)

    $ phone_add_msg(_ag_girl.gid, _ag_girl.gid, None, "typing")
    call screen phone_chat_screen(_ag_girl, auto_close=renpy.random.uniform(0.8, 1.4), choices=[])
    python:
        _t = phone_get_msgs(_ag_girl.gid)
        if _t and _t[-1].get("type") == "typing":
            _t.pop()
        phone_add_msg(_ag_girl.gid, _ag_girl.gid, _tl(_("I need your help with something special. Trust me, you'll like it.")))

    # ── Accept / Decline choices on the phone ──
    python:
        _ag_phone_choices = [
            (_tl(_("Sure, I'll be right there.")), "accept"),
            (_tl(_("Not interested.")), "decline"),
        ]
    call screen phone_chat_screen(_ag_girl, choices=_ag_phone_choices)
    $ _ag_pick = _return

    if _ag_pick == "accept":
        $ phone_add_msg(_ag_girl.gid, "player", _tl(_("Sure, I'll be right there.")))
        $ phone_add_msg(_ag_girl.gid, _ag_girl.gid, _tl(_("Perfect! Door's unlocked. Come whenever you're ready.")))
        call screen phone_chat_screen(_ag_girl, choices=[])

        # Fade to black then navigate
        scene black
        with fade
        "You head to [_ag_girl.Name]'s room."
        python:
            _ag_room = girl_home_loc(store._ag_girl_gid)
            navigate_to(_ag_room, None)
        call Set_Scene(entry=False) from _call_ag_set_scene
        call anniversary_gift_event from _call_anniversary_gift_event
    else:
        $ phone_add_msg(_ag_girl.gid, "player", _tl(_("Not interested.")))
        call _phone_typing(_ag_girl) from _typing_ag_decline
        $ phone_add_msg(_ag_girl.gid, _ag_girl.gid, _tl(_("Wow. Okay then. Your loss.")))
        call screen phone_chat_screen(_ag_girl, auto_close=1.0, choices=[])

        python:
            Change_Status(_ag_girl, "Love", -10)
            Change_Status(_ag_girl, "Obed", 5)
            store._ag_cooldown_until = store.Day + renpy.random.randint(7, 14)
            store._ag_scheduled_day = -1
            print("[AG] Player declined. Love -10, Obed +5. Cooldown until day %d." % store._ag_cooldown_until)
    return


# ── Main event ──

label anniversary_gift_event:
    python:
        _ag_girl = GIRL_BY_ID.get(store._ag_girl_gid)
        _ag_npc = get_npc_partner_for(_ag_girl)
        _ag_npc_is_gf = _ag_girl.get_flag("partner_is_female")
        store._scene_restricted = True
        time_lock()
        session_cum_reset()
        store._ntr_partner_watching = True
        store._ntr_watching_npc = _ag_npc
        store._player_exhausted = False
        store._hate_cum_scene_aborted = False
        store._condom_removed_midscene = False
        store._creampie_consent = False
        store._player_exposed_this_session = False
        print("[AG] Event starting. Girl=%s NPC=%s npc_is_gf=%s" % (_ag_girl.gid, _ag_npc.name, _ag_npc_is_gf))

    call _ag_phase_arrival from _call_ag_arrival
    call _ag_phase_massage_1 from _call_ag_massage_1
    call _ag_phase_strip from _call_ag_strip
    call _ag_phase_massage_2 from _call_ag_massage_2
    call _ag_phase_rub from _call_ag_rub
    call _ag_phase_tip from _call_ag_tip
    call _ag_phase_condom_sex from _call_ag_condom
    call _ag_phase_raw from _call_ag_raw
    call _ag_phase_creampie from _call_ag_creampie
    call _ag_phase_post from _call_ag_post
    call _ag_cleanup from _call_ag_cleanup
    return


# ── Phase 1: Arrival ──

label _ag_phase_arrival:
    $ print("[AG] Phase 1: Arrival")

    # Show NPC in the room
    $ _ag_npc.show_sprite(slot_right)

    # Girl intro (split into 2 bubbles with expression change)
    $ set_scene_expression(_ag_girl, "smile")
    python:
        _line = _format_partner_line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["arrival"]["girl_intro_1"])))
    $ Say_Line(_ag_girl, _line)

    $ set_scene_expression(_ag_girl, "normal")
    python:
        _line = _format_partner_line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["arrival"]["girl_intro_2"])))
    $ Say_Line(_ag_girl, _line)

    # NPC demands
    $ Say_Line(_ag_npc, _tl(renpy.random.choice(_AG_DIALOGUE["arrival"]["npc_demand"])))

    # Player accepts (with player name shown)
    $ Say_Player(_tl(_AG_DIALOGUE["arrival"]["player_accept"][0]))

    # NPC is anxious
    python:
        _line = _format_partner_line(_ag_girl, _tl(_AG_DIALOGUE["arrival"]["narration_npc_anxious"][0]))
    $ renpy.say(None, _line)

    # Girl positions herself
    $ renpy.say(None, _tl(_AG_DIALOGUE["arrival"]["narration_girl_position"][0]))

    return


# ── Phase 2: Massage 1 (clothed, 3 ticks) ──

label _ag_phase_massage_1:
    $ print("[AG] Phase 2: Massage 1 (clothed)")

    python:
        _ag_girl._massage_prev_pose = getattr(_ag_girl, "default_pose", "standing")
        _ag_girl._massage_prev_slot = getattr(_ag_girl, "SpriteLoc", StageCenter)
        _ag_girl.SaveOutfit()
        stop_standing_blink(_ag_girl)
        hide_girl_sprite(_ag_girl)

        # the anniversary stays an LD / RCG event (its massage escalates into the full scene, 20+
        # boolean branches below): a doggy-solo girl (mast_pose "doggy") can't reach it today, she
        # has no NPC partner. _setup_rear_pose_vars returns the pose KIND since 2026-10-11.
        store._ag_use_ld = (_setup_rear_pose_vars(_ag_girl) == "laying_down")

    if store._ag_use_ld:
        call LD_ApplySpeed(_ag_girl, 0) from _call_ag_ld_0
    else:
        call RCG_ApplySpeed(_ag_girl, 0) from _call_ag_rcg_0

    # Re-show NPC above RCG layers so they stay visible
    $ renpy.show(_ag_npc.image_name(), tag=_ag_npc.image_tag(), at_list=[slot_right], zorder=10090)

    # Girl is now in position
    $ set_scene_expression(_ag_girl, "smile")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["arrival"]["girl_ready"][0]))

    # Tick 1: shoulders
    $ set_scene_expression(_ag_girl, "happy")
    $ renpy.show("massage_hands", at_list=[massage_hands_shoulders], zorder=10070)
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["massage_1"]["girl"][0]))
    $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
    $ renpy.pause(0.3)
    $ renpy.hide("massage_hands")

    # Tick 2: back
    $ set_scene_expression(_ag_girl, "sexy")
    $ renpy.show("massage_hands", at_list=[massage_hands_back], zorder=10070)
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["massage_1"]["girl"][1]))
    $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
    $ renpy.pause(0.3)
    $ renpy.hide("massage_hands")

    # Tick 3: shoulders
    $ set_scene_expression(_ag_girl, "lipbite")
    $ renpy.show("massage_hands", at_list=[massage_hands_shoulders], zorder=10070)
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["massage_1"]["girl"][2]))
    $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
    $ renpy.pause(0.3)
    $ renpy.hide("massage_hands")

    $ _ag_girl.Lust = min(100, _ag_girl.Lust + 5)

    return


# ── Phase 3: Strip ──

label _ag_phase_strip:
    $ print("[AG] Phase 3: Strip")

    $ set_scene_expression(_ag_girl, "smirk")
    $ Say_Line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["strip"]["girl_ask"])))

    $ Say_Line(_ag_npc, _tl(renpy.random.choice(_AG_DIALOGUE["strip"]["npc_accept"])))

    python:
        for _slot in ("over", "mid", "chest", "skirt", "panties", "shoes"):
            if _ag_girl.clothes.get(_slot):
                _ag_girl.clothes[_slot] = None
                _ag_girl.clothes_state[_slot] = "full"

    if store._ag_use_ld:
        call LD_ApplySpeed(_ag_girl, 0) from _call_ag_ld_strip
    else:
        call RCG_ApplySpeed(_ag_girl, 0) from _call_ag_rcg_strip

    $ renpy.say(None, _tl(_AG_DIALOGUE["strip"]["narration"][0]))

    $ _ag_girl.Lust = min(100, _ag_girl.Lust + 5)

    return


# ── Phase 4: Massage 2 (naked, 3 ticks) ──

label _ag_phase_massage_2:
    $ print("[AG] Phase 4: Massage 2 (naked)")

    # Tick 1: back
    $ set_scene_expression(_ag_girl, "sexy")
    $ renpy.show("massage_hands", at_list=[massage_hands_back], zorder=10070)
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["massage_2"]["girl"][0]))
    $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
    $ renpy.pause(0.3)
    $ renpy.hide("massage_hands")

    # Tick 2: thighs
    $ set_scene_expression(_ag_girl, "lipbite")
    $ renpy.show("massage_hands", at_list=[massage_hands_thighs], zorder=10070)
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["massage_2"]["girl"][1]))
    $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
    $ renpy.pause(0.3)
    $ renpy.hide("massage_hands")

    # Tick 3: back
    $ set_scene_expression(_ag_girl, "kissing")
    $ renpy.show("massage_hands", at_list=[massage_hands_back], zorder=10070)
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["massage_2"]["girl"][2]))
    $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
    $ renpy.pause(0.3)
    $ renpy.hide("massage_hands")

    $ _ag_girl.Lust = min(100, _ag_girl.Lust + 10)

    return


# ── Phase 5: Rub (extended) ──

label _ag_phase_rub:
    $ print("[AG] Phase 5: Rub")

    # Narration: girl feels player's bulge
    $ set_scene_expression(_ag_girl, "surprised")
    $ renpy.say(None, _tl(_AG_DIALOGUE["rub"]["narration_bulge"][0]))

    $ set_scene_expression(_ag_girl, "lipbite")
    $ Say_Line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["rub"]["girl_request"])))

    $ Say_Line(_ag_npc, _tl(renpy.random.choice(_AG_DIALOGUE["rub"]["npc_accept"])))

    # Girl reassures NPC
    $ set_scene_expression(_ag_girl, "smile")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["rub"]["girl_reassure"][0]))

    # Narration: she unzips
    $ renpy.say(None, _tl(_AG_DIALOGUE["rub"]["narration_unzip"][0]))

    python:
        if store._ag_use_ld:
            store.laying_rub_mode = True
            store.laying_speed = 1
        else:
            store.rcg_rub_mode = True
            store.rcg_speed = 1

    if store._ag_use_ld:
        call LD_ApplySpeed(_ag_girl, 1) from _call_ag_ld_rub
    else:
        call RCG_ApplySpeed(_ag_girl, 1) from _call_ag_rcg_rub

    $ set_scene_expression(_ag_girl, "lipbite")
    $ renpy.pause(2.0)

    # Girl teases NPC while grinding
    $ set_scene_expression(_ag_girl, "kissing")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["rub"]["girl_tease"][0]))

    $ renpy.pause(1.5)

    $ set_scene_expression(_ag_girl, "lipbite")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["rub"]["girl_tease"][1]))

    # NPC realizes
    $ Say_Line(_ag_npc, _tl(_AG_DIALOGUE["rub"]["npc_worried"][0]))

    # Speed 2: grinding intensifies before tip request
    if store._ag_use_ld:
        call LD_ApplySpeed(_ag_girl, 2) from _call_ag_ld_rub_2
    else:
        call RCG_ApplySpeed(_ag_girl, 2) from _call_ag_rcg_rub_2

    $ set_scene_expression(_ag_girl, "moaning")
    $ renpy.pause(2.0)

    $ _ag_girl.Lust = min(100, _ag_girl.Lust + 10)
    $ mark_intimacy(_ag_girl, "rub")

    return


# ── Phase 6: Tip (extended) ──

label _ag_phase_tip:
    $ print("[AG] Phase 6: Tip")

    # Girl asks NPC for permission
    $ set_scene_expression(_ag_girl, "lipbite")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["tip"]["girl_ask"][0]))

    # NPC denies
    $ Say_Line(_ag_npc, _tl(_AG_DIALOGUE["tip"]["npc_deny"][0]))

    # Girl convinces
    $ set_scene_expression(_ag_girl, "kissing")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["tip"]["girl_convince"][0]))

    # Narration: she inserts
    $ renpy.say(None, _tl(_AG_DIALOGUE["tip"]["narration_insert"][0]))

    python:
        if store._ag_use_ld:
            store.laying_tip_mode = True
            store.laying_rub_mode = False
            store.laying_started = True
        else:
            store.rcg_tip_mode = True
            store.rcg_rub_mode = False
            store.rcg_started = True

    if store._ag_use_ld:
        call LD_ApplySpeed(_ag_girl, 1) from _call_ag_ld_tip
    else:
        call RCG_ApplySpeed(_ag_girl, 1) from _call_ag_rcg_tip

    # NPC frozen
    $ renpy.say(None, _tl(_AG_DIALOGUE["tip"]["narration_npc_frozen"][0]))

    $ set_scene_expression(_ag_girl, "lipbite")
    $ renpy.pause(2.0)

    # Girl continues teasing
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["tip"]["girl_continue"][0]))

    $ renpy.pause(2.0)

    $ set_scene_expression(_ag_girl, "kissing")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["tip"]["girl_continue"][1]))

    # NPC breaking
    $ Say_Line(_ag_npc, _tl(_AG_DIALOGUE["tip"]["npc_breaking"][0]))

    $ _ag_girl.Lust = min(100, _ag_girl.Lust + 10)
    $ mark_intimacy(_ag_girl, "tip")

    return


# ── Phase 7: Condom sex ──

label _ag_phase_condom_sex:
    $ print("[AG] Phase 7: Condom sex (gf=%s)" % _ag_npc_is_gf)

    # Ahegao moan before begging
    $ set_scene_expression(_ag_girl, "ahegao")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["condom_sex"]["girl_ahegao_moan"][0]))

    # Extra moan building up
    $ set_scene_expression(_ag_girl, "lipbite")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["condom_sex"]["girl_extra_moan"][0]))

    $ set_scene_expression(_ag_girl, "kissing")
    $ Say_Line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["condom_sex"]["girl_beg"])))

    # NPC condition: BF hands a condom, GF demands pull-out promise
    if _ag_npc_is_gf:
        $ Say_Line(_ag_npc, _tl(renpy.random.choice(_AG_DIALOGUE["condom_sex"]["gf_npc_demand"])))
        python:
            _line = _format_partner_line(_ag_girl, _tl(_AG_DIALOGUE["condom_sex"]["gf_narration_demand"][0]))
        $ renpy.say(None, _line)
    else:
        $ Say_Line(_ag_npc, _tl(renpy.random.choice(_AG_DIALOGUE["condom_sex"]["npc_condom"])))
        python:
            _line = _format_partner_line(_ag_girl, _tl(_AG_DIALOGUE["condom_sex"]["narration_condom_handoff"][0]))
        $ renpy.say(None, _line)

    # ── Transition from tip to full sex ──
    if _ag_npc_is_gf:
        # GF path: no condom, just go from tip to full penetration
        if store._ag_use_ld:
            python:
                store.laying_tip_mode = False
            call LD_PenisEnterAnim(_ag_girl) from _call_ag_ld_gf_enter
            call LD_ApplySpeed(_ag_girl, 1) from _call_ag_ld_sex_1
        else:
            python:
                store.rcg_tip_mode = False
            call RCG_PenisEnterAnim(_ag_girl) from _call_ag_gf_enter
            call RCG_ApplySpeed(_ag_girl, 1) from _call_ag_rcg_sex_1
    else:
        # BF path: condom equip animation (penis slides out, comes back with condom)
        if store._ag_use_ld:
            python:
                store.condom_active = True
                store.laying_tip_mode = False
            call LD_PenisEnterAnim(_ag_girl) from _call_ag_ld_condom_equip
            call LD_ApplySpeed(_ag_girl, 1) from _call_ag_ld_sex_1b
        else:
            python:
                _pen_img = "%s rcg_penis" % _ag_girl.gid
                renpy.show(_pen_img, tag="rcg_penis", at_list=[rcg_penis_slide_out], zorder=10060)
            $ renpy.pause(0.5)
            python:
                renpy.hide("rcg_penis")
                store.condom_active = True
                store.rcg_tip_mode = False
            call RCG_PenisEnterAnim(_ag_girl) from _call_ag_condom_equip
            call RCG_ApplySpeed(_ag_girl, 1) from _call_ag_rcg_sex_1b
    $ renpy.pause(3.0)

    # Speed 2 - extended with moaning lines
    if store._ag_use_ld:
        call LD_ApplySpeed(_ag_girl, 2) from _call_ag_ld_sex_2
    else:
        call RCG_ApplySpeed(_ag_girl, 2) from _call_ag_rcg_sex_2

    $ set_scene_expression(_ag_girl, "moaning")
    if _ag_npc_is_gf:
        $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["condom_sex"]["gf_girl_moan"][0]))
    else:
        $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["condom_sex"]["girl_moan_speed2"][0]))

    $ renpy.pause(2.0)

    $ set_scene_expression(_ag_girl, "ahegao")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["condom_sex"]["girl_moan_speed2"][1]))

    $ renpy.pause(2.0)

    $ set_scene_expression(_ag_girl, "moaning")
    $ Say_Line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["condom_sex"]["girl_speed"])))

    $ _ag_girl.Lust = min(100, _ag_girl.Lust + 15)
    # Full vaginal sex happened: the ACT first ("sex" is the flag every check reads), then the position
    $ mark_intimacy(_ag_girl, "sex")
    $ mark_intimacy(_ag_girl, "laying_down" if store._ag_use_ld else "reverse_cowgirl")

    return


# ── Phase 8: Raw sex ──

label _ag_phase_raw:
    $ print("[AG] Phase 8: Raw sex (gf=%s)" % _ag_npc_is_gf)

    $ set_scene_expression(_ag_girl, "moaning")
    if _ag_npc_is_gf:
        # GF path: girl breaks the pull-out promise (already raw, no condom to remove)
        $ Say_Line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["raw"]["gf_girl_break_promise"])))
    else:
        $ Say_Line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["raw"]["girl_remove"])))

    # NPC narration (hands in pants) — %(poss)s handles gender automatically
    python:
        _line = _format_partner_line(_ag_girl, _tl(_AG_DIALOGUE["raw"]["narration_npc"][0]))
    $ renpy.say(None, _line)

    if _ag_npc_is_gf:
        # GF path: already raw, just increase speed
        if store._ag_use_ld:
            call LD_ApplySpeed(_ag_girl, 2) from _call_ag_ld_raw_2
        else:
            call RCG_ApplySpeed(_ag_girl, 2) from _call_ag_rcg_raw_2
    else:
        # BF path: condom removal animation
        $ _on_condom_removed(_ag_girl, skip_hide=True, force=True)
        if store._ag_use_ld:
            call LD_CondomRemoveAnim(_ag_girl) from _call_ag_ld_condom_remove
            call LD_ApplySpeed(_ag_girl, 2) from _call_ag_ld_raw_2b
        else:
            call RCG_CondomRemoveAnim(_ag_girl) from _call_ag_condom_remove
            call RCG_ApplySpeed(_ag_girl, 2) from _call_ag_rcg_raw_2b
    $ renpy.pause(2.0)

    # Girl dirty talk
    $ set_scene_expression(_ag_girl, "ahegao")
    $ Say_Line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["raw"]["girl_dirty"])))

    # NPC gets turned on, commands player
    $ Say_Line(_ag_npc, _tl(renpy.random.choice(_AG_DIALOGUE["raw"]["npc_command"])))

    # Speed 3 - extended with more dialogue
    if store._ag_use_ld:
        call LD_ApplySpeed(_ag_girl, 3) from _call_ag_ld_raw_3
    else:
        call RCG_ApplySpeed(_ag_girl, 3) from _call_ag_rcg_raw_3
    $ renpy.pause(2.0)

    $ set_scene_expression(_ag_girl, "ahegao")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["raw"]["girl_speed3"][0]))

    $ renpy.pause(2.0)

    $ set_scene_expression(_ag_girl, "moaning")
    $ Say_Line(_ag_girl, _tl(_AG_DIALOGUE["raw"]["girl_speed3"][1]))

    $ renpy.pause(2.0)

    $ _ag_girl.Lust = min(100, _ag_girl.Lust + 15)

    return


# ── Phase 9: Creampie ──

label _ag_phase_creampie:
    $ print("[AG] Phase 9: Creampie")

    # Player can't hold it (with player name shown)
    $ Say_Player(_tl(_AG_DIALOGUE["creampie"]["player"][0]))

    # Girl demands inside
    $ set_scene_expression(_ag_girl, "ahegao")
    $ Say_Line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["creampie"]["girl_inside"])))

    # Narration
    $ renpy.say(None, _tl(_AG_DIALOGUE["creampie"]["narration"][0]))

    # Girl orgasm
    $ _ag_girl.Lust = 100

    # ── Cum animation: speed 4, pulsing, screen shake ──
    if store._ag_use_ld:
        call LD_CumAnim(_ag_girl) from _call_ag_ld_cum_anim
    else:
        call RCG_CumAnim(_ag_girl) from _call_ag_cum_anim

    # Track cum
    $ process_cum(_ag_girl, "laying_down" if store._ag_use_ld else "reverse_cowgirl", "inside")

    # Still moment - girl feels the cum flooding
    if store._ag_use_ld:
        $ store.laying_speed = 0
        call LD_ApplySpeed(_ag_girl, 0) from _call_ag_ld_still
    else:
        $ store.rcg_speed = 0
        call RCG_ApplySpeed(_ag_girl, 0) from _call_ag_rcg_still

    $ set_scene_expression(_ag_girl, "pleasure")
    $ Say_Line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["creampie"]["girl_feel_cum"])))

    $ renpy.pause(2.0)

    # Now show the results: Arms 2 + Dripping Cum 2
    python:
        store._session_cum["inside"] = 2
        if store._ag_use_ld:
            store._ld_arm_variant = 2
        else:
            store.rcg_arms_pose = 2
    if store._ag_use_ld:
        call LD_ApplySpeed(_ag_girl, 0) from _call_ag_ld_post_cum
    else:
        call RCG_ApplySpeed(_ag_girl, 0) from _call_ag_rcg_post_cum

    return


# ── Phase 10: Post-scene (still in RCG, then standing) ──

label _ag_phase_post:
    $ print("[AG] Phase 10: Post-scene")

    # ── Still in RCG with Arms 2 + Dripping Cum 2 ──
    $ set_scene_expression(_ag_girl, "smirk")
    $ Say_Line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["post"]["girl_show"])))

    $ renpy.say(None, _tl(_AG_DIALOGUE["post"]["narration_npc"][0]))

    # ── Transition to standing (naked) ──
    if store._ag_use_ld:
        call LD_End(_ag_girl, dress_up=False) from _call_ag_ld_end
    else:
        call RCG_End(_ag_girl, dress_up=False) from _call_ag_rcg_end

    # End's scene_full_cleanup restores outfit - strip again for naked standing
    python:
        for _s in ("over", "mid", "chest", "skirt", "panties", "shoes"):
            _ag_girl.clothes[_s] = None
            _ag_girl.clothes_state[_s] = "full"
        _ag_girl.Cum = ["dripping"]
        _set_standing_arm(_ag_girl, 1)
        print("[AG] Standing: naked + dripping cum")

    # Re-show NPC at normal zorder for standing scene
    $ _ag_npc.show_sprite(slot_right)

    $ set_scene_expression(_ag_girl, "smile")
    python:
        _line = _format_partner_line(_ag_girl, _tl(renpy.random.choice(_AG_DIALOGUE["post"]["girl_dismiss"])))
    $ Say_Line(_ag_girl, _line)

    return


# ── Cleanup ──

label _ag_cleanup:
    $ print("[AG] Cleanup")

    python:
        Change_Status(_ag_girl, "Love", 20)
        Change_Status(_ag_girl, "Obed", 15)
        Change_Status(_ag_girl, "Inbt", 10)

        _ag_npc._ntr_boundary_level = 4
        _ag_girl._ntr_boundary_level = 4
        _ag_npc._ntr_boundary_bar = 0
        _ag_girl._ntr_boundary_bar = 0
        # he gives up every limit here: the same achievement as filling his trust bar to the top
        unlock_achievement("full_access")
        _ag_npc.change_friendship(50)

        if callable(globals().get("_ntr_is_hostile_mode", None)) and _ntr_is_hostile_mode(_ag_npc):
            _ag_npc._ntr_hostile_surrendered = True

        _ntr_save_state(_ag_npc, _ag_girl)
        _ag_girl._ntr_levelup_pending = True
        _ntr_process_levelup_next_day(_ag_girl)

        store._ag_done = True
        store._ag_scheduled_day = -1

        unlock_achievement("femdom_cuckold")

        time_unlock()
        store._scene_restricted = False
        store._ntr_partner_watching = False
        store._ntr_watching_npc = None

        _ag_girl.Cum = []
        _ag_npc.hide_sprite()

        print("[AG] Event complete. Girl=%s, Love+20, Obed+15, Inbt+10, NPC boundary=4, friendship+50, levelup_pending=True" % _ag_girl.gid)

    scene black
    with fade
    "You get dressed and leave."
    $ navigate_to("campus", None)
    call Set_Scene(entry=True) from _call_ag_set_scene_exit

    if getattr(_ag_girl, "_ntr_activation_msg_pending", False):
        python:
            _ag_girl._ntr_boundary_discovered = True
            _ag_girl._ntr_activation_msg_pending = False
            _ag_girl._ntr_activation_msg_list = []
            _ag_girl._ntr_activation_msg_npc_id = None
        "Well... [_ag_npc.name] watched the whole thing. And didn't stop it."

    return


# ============================================
# QA TEST: renpy.jump("qa_anniversary_gift")
# Full flow: setup -> phone message -> accept/decline -> event -> results
# ============================================

label qa_anniversary_gift:
    scene black

    # ── Setup: ensure girl has all required conditions ──
    python:
        _qa_ag_girl = None
        for _g in ALL_GIRLS:
            if _g in ALL_GIRLS:
                _qa_ag_girl = _g
                break

        if _qa_ag_girl is None:
            renpy.say(None, "No girl found for testing.")
            renpy.jump("main_loop")

        _qa_ag_girl.traits.add("exhibitionist")
        _qa_ag_girl.traits.add("cheater")

        _qa_ag_girl.Sex_acts["sex"] = max(_qa_ag_girl.Sex_acts.get("sex", 0), 1)
        _qa_ag_girl.Sex_acts["reverse_cowgirl"] = max(_qa_ag_girl.Sex_acts.get("reverse_cowgirl", 0), 1)

        if not _qa_ag_girl.has_npc_partner():
            # NEW partner: set_npc_partner() wipes the per-partner mirrors and creates the NPC itself
            _qa_ag_girl.set_npc_partner(_qa_ag_girl.npc_partner_canonical_id("male"), gender="male")
        _qa_ag_npc = get_npc_partner_for(_qa_ag_girl)
        print("[QA_AG] %s: test partner = %s" % (_qa_ag_girl.gid, getattr(_qa_ag_npc, "name", None)))

        _qa_ag_npc._ntr_active = True
        _qa_ag_npc._ntr_boundary_level = 2
        _qa_ag_npc._ntr_boundary_bar = 0
        _qa_ag_npc.friendship_with_player = 500
        _qa_ag_npc.love_for_girl = 750
        _ntr_save_state(_qa_ag_npc, _qa_ag_girl)

        _qa_ag_love_before = _qa_ag_girl.Love
        _qa_ag_obed_before = _qa_ag_girl.Obed
        _qa_ag_inbt_before = _qa_ag_girl.Inbt
        _qa_ag_friend_before = _qa_ag_npc.friendship_with_player
        _qa_ag_boundary_before = _qa_ag_npc._ntr_boundary_level

        store._ag_done = False
        store._ag_scheduled_day = -1
        store._ag_girl_gid = None
        store._ag_cooldown_until = -1

        print("[QA_AG] Setup done: girl=%s npc=%s" % (_qa_ag_girl.gid, _qa_ag_npc.name))

    "[_qa_ag_girl.Name] configured: exhibitionist + cheater, NPC [_qa_ag_npc.Name] with NTR active."
    "Stats before: Love=[_qa_ag_love_before], Obed=[_qa_ag_obed_before], Inbt=[_qa_ag_inbt_before]"
    "NPC before: boundary=[_qa_ag_boundary_before], friendship=[_qa_ag_friend_before]"

    # ── Step 1: Schedule the event for today ──
    python:
        _ag_daily_check()
        print("[QA_AG] Daily check fired. scheduled_day=%s girl=%s" % (store._ag_scheduled_day, store._ag_girl_gid))

    if _ag_scheduled_day < 0:
        "ERROR: Daily check did not schedule the event. Check conditions."
        return

    # ── Step 2: Fire check (phone opens, girl texts, accept/decline) ──
    call anniversary_gift_check from _call_qa_ag_check

    # ── Step 3: Results ──
    jump qa_anniversary_gift.results


label .results:
    python:
        _qa_r_girl = GIRL_BY_ID.get(store._ag_girl_gid) or _qa_ag_girl
        _qa_r_npc = get_npc_partner_for(_qa_r_girl)
        _qa_r_love = _qa_r_girl.Love
        _qa_r_obed = _qa_r_girl.Obed
        _qa_r_inbt = _qa_r_girl.Inbt
        _qa_r_boundary = getattr(_qa_r_npc, "_ntr_boundary_level", -1) if _qa_r_npc else -1
        _qa_r_friend = getattr(_qa_r_npc, "friendship_with_player", -1) if _qa_r_npc else -1
        _qa_r_done = store._ag_done
        _qa_r_ach = is_achievement_unlocked("femdom_cuckold")
        _qa_r_cum = str(_qa_r_girl.Cum) if hasattr(_qa_r_girl, "Cum") else "[]"
        _qa_r_locked = getattr(store, "_time_locked", False)

    "== RESULTS =="
    "Girl: Love [_qa_ag_love_before]->[_qa_r_love], Obed [_qa_ag_obed_before]->[_qa_r_obed], Inbt [_qa_ag_inbt_before]->[_qa_r_inbt]"
    "NPC: boundary [_qa_ag_boundary_before]->[_qa_r_boundary], friendship [_qa_ag_friend_before]->[_qa_r_friend]"
    "Event done: [_qa_r_done] | Achievement unlocked: [_qa_r_ach]"
    "Cum state: [_qa_r_cum]"
    "Time locked (should be False): [_qa_r_locked]"

    menu:
        "Run again (full reset)":
            python:
                store._ag_done = False
                store._ag_scheduled_day = -1
                store._ag_girl_gid = None
                store._ag_cooldown_until = -1
            jump qa_anniversary_gift
        "Done":
            return
