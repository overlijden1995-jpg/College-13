# =========================================================
# PLAYER HANDS (touch overlay)
# =========================================================
image player_hands = _p("Player Hands.png")
image massage_hands = _p("Massage Back.png")

# Ass grab animation: Neutral -> Open -> Grab -> Squeeze -> Grab -> Open -> Neutral (x3)
image massage_ass_grab:
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Neutral.png"
    0.4
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Open.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Grab.png"
    0.4
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Squeeze.png"
    0.5
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Grab.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Open.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Neutral.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Open.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Grab.png"
    0.4
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Squeeze.png"
    0.5
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Grab.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Open.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Neutral.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Open.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Grab.png"
    0.4
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Squeeze.png"
    0.5
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Grab.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Open.png"
    0.3
    "images/characters/Gwen/RCG/Gwen RCG Guy Hand Neutral.png"

transform player_hands_touch_bounce:
    subpixel True
    alpha 0.0
    easein 0.3 alpha 1.0
    block:
        ease 0.6 yoffset 6
        ease 0.6 yoffset -6
        repeat

transform player_hands_fade_out:
    alpha 1.0
    easeout 0.3 alpha 0.0

# Massage hands: circular motion on back
transform massage_hands_back:
    subpixel True
    xalign StageCenter
    yalign 2.0
    alpha 0.0
    easein 0.3 alpha 1.0
    block:
        ease 0.5 xoffset 10 yoffset -5
        ease 0.5 xoffset 5 yoffset 5
        ease 0.5 xoffset -10 yoffset 5
        ease 0.5 xoffset -5 yoffset -5
        repeat

# Massage hands: circular motion on shoulders (higher Y)
transform massage_hands_shoulders:
    subpixel True
    xalign StageCenter
    yalign 2.0
    yoffset -80
    alpha 0.0
    easein 0.3 alpha 1.0
    block:
        ease 0.5 xoffset 8 yoffset -85
        ease 0.5 xoffset 4 yoffset -75
        ease 0.5 xoffset -8 yoffset -75
        ease 0.5 xoffset -4 yoffset -85
        repeat

# Massage hands: circular motion on thighs (much lower Y)
transform massage_hands_thighs:
    subpixel True
    xalign StageCenter
    yalign 2.0
    yoffset 400
    alpha 0.0
    easein 0.3 alpha 1.0
    block:
        ease 0.5 xoffset 12 yoffset 395
        ease 0.5 xoffset 6 yoffset 405
        ease 0.5 xoffset -12 yoffset 405
        ease 0.5 xoffset -6 yoffset 395
        repeat

# Massage ass: circular motion with grab animation
transform massage_ass_motion:
    subpixel True
    xalign StageCenter
    yalign 2.0
    alpha 0.0
    easein 0.3 alpha 1.0
    block:
        ease 0.6 xoffset 8 yoffset -4
        ease 0.6 xoffset 4 yoffset 4
        ease 0.6 xoffset -8 yoffset 4
        ease 0.6 xoffset -4 yoffset -4
        repeat

# The doggy's hand art is FULL SCREEN with the hand baked where it lands (sdg_slap): the circles
# anchor at (0,0), never at the girl slot (_rear_grab_at, scene_config.rpy)
transform massage_ass_motion_dg:
    subpixel True
    pos (0, 0)
    alpha 0.0
    easein 0.3 alpha 1.0
    block:
        ease 0.6 xoffset 8 yoffset -4
        ease 0.6 xoffset 4 yoffset 4
        ease 0.6 xoffset -8 yoffset 4
        ease 0.6 xoffset -4 yoffset -4
        repeat

transform massage_hands_fade_out:
    easeout 0.3 alpha 0.0

# =========================================================
# PER-CHARACTER MASSAGE STRIP PERSONALITY
# =========================================================
# Checked BEFORE the trait cascade (virgin/cute/nerd/hc/bf).
# To add a new character: add a gid entry below. All keys optional.
#   accept: {piece: [lines]} — overrides strip acceptance dialogue
#   pub_suffix: string — appended to accept lines in public
#   pub_deny: [lines] — overrides public denial dialogue
init python:
    MASSAGE_STRIP_PERSONALITY = {
        "tenny": {
            "accept": {
                "top": [_("Anyone could walk in right now... why am I not stopping you?"), _("I should say no... but my body is saying something completely different..."), _("This is so reckless... and I can't believe how much I don't care right now.")],
                "skirt": [_("If someone opens that door... oh god, my heart... but keep going."), _("I'm supposed to be the smart one who thinks things through... clearly not today."), _("Every rational part of me says stop... and I'm ignoring all of it.")],
                "bra": [_("We could get caught any second... why does that make this feel more intense?"), _("I can hear footsteps outside... and I'm still letting you..."), _("My brain is screaming danger but my body won't listen...")],
                "panties": [_("If anyone finds us like this, I'm done... finished... and I still want this..."), _("The risk is insane right now... and I've never felt more alive..."), _("Every second we could get caught... and I'm the one who should know better...")],
            },
            "pub_suffix": _("...and someone could see us any second. That should scare me more than it does."),
            "pub_deny": [_("N-not here! Anyone could... I mean, the RISK is... no. I can't. Not today."), _("I want to, believe me, I WANT to... but my brain is barely winning right now!"), _("Don't look at me like that... I'm already fighting myself to say no!")],
        },
    }

# =========================================================
# MAIN FLIRT ENTRY
# =========================================================
label Flirt_Girl(girl, loc, t_index):

    if not girl:
        "There's no one here to flirt with."
        return

    $ CurrentGirl = girl

    # Repeat-denial check: if she already denied flirting this time slot, penalize
    if was_denied_this_slot(girl, "flirt"):
        $ penalty_for_insistence(girl, "flirt")
        return

    # Player-has-girlfriend gate: she knows you're taken
    python:
        _flirt_player_has_gf = player_has_girlfriend(ALL_GIRLS) and not girl.is_dating_player()
        # Harem exemption: if all GFs accept this girl, skip the GF gate
        if _flirt_player_has_gf:
            _flirt_all_gfs_ok = True
            for _fgf in get_player_girlfriends(ALL_GIRLS):
                if not is_harem_exempt(_fgf, girl):
                    _flirt_all_gfs_ok = False
                    break
            if _flirt_all_gfs_ok:
                _flirt_player_has_gf = False
    if _flirt_player_has_gf:
        python:
            _t = int(girl.Temptation)
            _flirt_is_cheater = girl.has_trait("cheater") if hasattr(girl, "has_trait") else False
        if _t < 2 and not _flirt_is_cheater:
            # Low temptation: she refuses to flirt with someone else's boyfriend
            $ set_scene_expression(girl, "angry")
            python:
                register_denial(girl, "flirt")
                _pgf_line = _player_gf_sex_line(girl, "flirt", False)
                if _pgf_line:
                    Say_Line(girl, _format_partner_line(girl, _pgf_line))
                else:
                    Say_Line(girl, _("You have a girlfriend. Don't flirt with me."))
                provoke(girl, 1)
                Change_Status(girl, "Love", -3)
            $ set_scene_expression(girl, "normal")
            return
        # temptation >= 2 (or cheater): conflicted but lets it through
        $ set_scene_expression(girl, "uncomfortable")
        python:
            _pgf_line = _player_gf_sex_line(girl, "flirt", True)
            if _pgf_line:
                Say_Line(girl, _format_partner_line(girl, _pgf_line))
            provoke(girl, 1)
        $ set_scene_expression(girl, "normal")

    # Boyfriend gate: temptation-based resistance
    if girl.has_npc_partner() and not girl.has_trait("cheater"):
        python:
            _t = int(girl.Temptation)
            # Heat contributes to effective temptation
            if callable(_is_on_cheat_path) and _is_on_cheat_path(girl):
                _t += int(getattr(girl, "_cheat_heat", 0) // 10)
        if _t < 3:
            # Low temptation: she refuses to flirt, temptation rises
            $ set_scene_expression(girl, "serious")
            python:
                register_denial(girl, "flirt")
                Say_Line(girl, _format_partner_line(girl, bf_denial_line(girl, "flirt")))
                _bfh = get_bf_loyalty_hint(girl, False)
                if _bfh:
                    set_scene_expression(girl, "worried")
                    Say_Line(girl, _bfh)
                provoke(girl, 1)
                Change_Status(girl, "Love", -3)
                _notify_cheat_heat(girl, "bf_flirt", False)
            $ set_scene_expression(girl, "normal")
            return
        # temptation >= 3: conflicted but lets it through
        $ set_scene_expression(girl, "uncomfortable")
        python:
            Say_Line(girl, _format_partner_line(girl, bf_denial_line(girl, "flirt")))
            _bfh = get_bf_loyalty_hint(girl, True)
            if _bfh:
                Say_Line(girl, _bfh)
            provoke(girl, 1)
        $ set_scene_expression(girl, "normal")

    # If the player has been spamming flirts and her stats are low,
    # she can get annoyed instead of opening the menu.
    if girl_is_annoyed_by_flirt(girl):
        $ register_denial(girl, "flirt")
        $ _set_standing_arm(girl, 2)
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _("Why are you suddenly trying so hard today?"))
        $ set_scene_expression(girl, "serious")
        $ Say_Line(girl, _("Calm down a little, will you?"))
        $ Change_Status(girl, "Love", -10)
        $ Change_Status(girl, "Obed", -5)
        $ _set_standing_arm(girl, 0)
        $ set_scene_expression(girl, "normal")
        return

    # Story lock gate: her step doesn't open flirting yet (story_steps.rpy). She interrupts before the menu,
    # like the boyfriend gate: no menu, immediate rejection.
    if story_act_locked(girl, "flirt"):
        python:
            register_denial(girl, "flirt")
            _sl_face = "angry" if story_first_step(girl) else "smug"
        $ set_scene_expression(girl, _sl_face)
        python:
            _sl_keys = _story_keys_with_traits(girl, "flirt_story_locked.%s" % story_step_id(girl))
            if husband_in_room(girl):
                _sl_keys = _story_keys_with_traits(girl, "flirt_story_locked_husband.%s" % story_step_id(girl)) + _sl_keys
            _sl_line = story_rod_line(girl, _sl_keys) or _tl(renpy.random.choice(STORY_LOCKED_FALLBACK))
            Say_Line(girl, _sl_line)
        $ set_scene_expression(girl, "normal")
        return

    $ _flirt_did_action = False
    menu:
        "Play Safe...":
            call Flirt_Safe_Menu(girl, loc, t_index) from _call_Flirt_Safe_Menu
            $ _flirt_did_action = _return if _return is not None else True

        "Go Lewd...":
            call Flirt_Lewd_Menu(girl, loc, t_index) from _call_Flirt_Lewd_Menu
            $ _flirt_did_action = _return if _return is not None else True

        "Never mind":
            "You decide to hold back for now."
            return

    if _flirt_did_action:
        # GF witness trigger: if a GF is at the same location and saw the flirt, set open-rel trigger
        python:
            _flirt_witness_gf = None
            for _fwg in get_player_girlfriends(ALL_GIRLS):
                if _fwg.gid == girl.gid:
                    continue
                if _fwg.loc != loc:
                    continue
                if _fwg.has_trait("polyamorous"):
                    _jeal_gain = 0
                elif is_harem_exempt(_fwg, girl):
                    _jeal_gain = 5
                else:
                    _jeal_gain = 30
                if _jeal_gain > 0:
                    Change_Status(_fwg, "Jealousy", _jeal_gain, max_val=1000)
                print("[JEALOUSY] %s +%d from witnessing flirt with %s (now %d)" % (_fwg.gid, _jeal_gain, girl.gid, getattr(_fwg, "Jealousy", 0)))
                if getattr(_fwg, "_open_relationship_consent", False):
                    continue
                if is_harem_exempt(_fwg, girl):
                    continue
                _fwg._gf_open_rel_trigger = {"other_gid": girl.gid, "reason": "flirt"}
                print("[HAREM_TRIGGER] %s witnessed player flirting with %s at %s" % (_fwg.gid, girl.gid, loc))
                if _flirt_witness_gf is None:
                    _flirt_witness_gf = _fwg

        # GF visual reaction to witnessing the flirt
        if _flirt_witness_gf is not None:
            $ set_scene_expression(_flirt_witness_gf, "angry")
            $ Say_Line(_flirt_witness_gf, renpy.random.choice([
                _("Really? Right in front of me?"),
                _("I'm literally right here."),
                _("Am I invisible to you?"),
                _("You're unbelievable."),
            ]))
            $ set_scene_expression(_flirt_witness_gf, "normal")

        # Her own partner on scene: did he see that?
        call _flirt_partner_witness(girl) from _call_flirt_partner_witness

        call Apply_Time_Cost(TIME_COSTS["flirt"]) from _call_Apply_Time_Cost_flirt
    return

# =========================================================
# HER PARTNER IS RIGHT THERE (FLIRT_PARTNER_WATCH, dialogue_bank.rpy)
# =========================================================
# Runs after every flirt that queued itself (flirt_partner_note): her "not with him here!" when he was the
# only reason she said no, then whether he saw it (his reaction, suspicion, friendship, love). At 100 he
# confronts her on the spot and she goes after him (npc_suspicion_confrontation).
default _flirt_partner_pending = None

label _flirt_partner_witness(girl):
    $ _fpw = flirt_partner_take(girl)
    if not _fpw:
        return
    if _fpw["blocked_line"]:
        $ set_scene_expression(girl, "worried")
        $ Say_Line(girl, _fpw["blocked_line"])
    if _fpw["seen"]:
        $ Narration(_fpw["narration"])
        $ Say_Line(_fpw["npc"], _fpw["line"])
        if _fpw["accepted"]:
            $ set_scene_expression(girl, "worried")
        if getattr(_fpw["npc"], "suspicion", 0) >= 100 and not _fpw.get("ntr_boundary"):
            call npc_suspicion_confrontation(_fpw["npc"]) from _call_npc_suspicion_confront_flirt
    elif _fpw["near_miss"]:
        $ Narration(_fpw["near_miss"])
    return

# =========================================================
# SAFE FLIRT MENU
# =========================================================
label Flirt_Safe_Menu(girl, loc, t_index):

    menu:
        "Make a joke":
            call Flirt_Safe_Joke(girl, loc, t_index) from _call_Flirt_Safe_Joke
            return True

        "Compliment Her...":
            call Flirt_Compliment(girl, loc, t_index) from _call_Flirt_Compliment
            return True

        "Hold hands":
            call Flirt_Safe_HoldHands(girl, loc, t_index) from _call_Flirt_Safe_HoldHands
            return True

        "Touch her cheek":
            call Flirt_Safe_TouchCheek(girl, loc, t_index) from _call_Flirt_Safe_TouchCheek
            return True

        "Hug her":
            call Flirt_Safe_Hug(girl, loc, t_index) from _call_Flirt_Safe_Hug
            return True

        "Kiss her cheek":
            call Flirt_Safe_KissCheek(girl, loc, t_index) from _call_Flirt_Safe_KissCheek
            return True

        "Back":
            "You decide not to push it for now."
            return False

label Flirt_Safe_TouchCheek(girl, loc, t_index):
    $ base_result = do_safe_flirt(girl, "touch_cheek")
    $ reaction_mode = get_flirt_reaction_mode_safe(girl, base_result, "touch_cheek")
    $ rod_flirt_say(girl, "safe_touch_cheek", reaction_mode)
    return

label Flirt_Safe_HoldHands(girl, loc, t_index):
    $ base_result = do_safe_flirt(girl, "hold_hands")
    $ reaction_mode = get_flirt_reaction_mode_safe(girl, base_result, "hold_hands")
    $ rod_flirt_say(girl, "safe_hold_hands", reaction_mode)
    return

label Flirt_Safe_Joke(girl, loc, t_index):
    $ base_result = do_safe_flirt(girl, "joke")
    $ reaction_mode = get_flirt_reaction_mode_safe(girl, base_result, "joke")
    $ rod_flirt_say(girl, "safe_joke", reaction_mode)
    return

label Flirt_Safe_KissCheek(girl, loc, t_index):
    $ base_result = do_safe_flirt(girl, "kiss_cheek")
    $ reaction_mode = get_flirt_reaction_mode_safe(girl, base_result, "kiss_cheek")
    $ rod_flirt_say(girl, "safe_kiss_cheek", reaction_mode)
    if base_result == "reject" and girl.has_trait("lesbian"):
        $ Narration(_("A kiss seems to be the last thing she'd ever agree to. Try something else first."))
    return

label Flirt_Safe_StealKiss(girl, loc, t_index):
    $ base_result = do_safe_flirt(girl, "steal_kiss")
    $ reaction_mode = get_flirt_reaction_mode_safe(girl, base_result, "steal_kiss")

    if base_result == "ok":
        call _kiss_accepted(girl, flirt_mode=reaction_mode) from _call_kiss_accepted_flirt
    elif reaction_mode == "story_locked":
        # her step locks the kiss (story_steps.rpy): she stops it, no slap
        $ rod_flirt_say(girl, "safe_steal_kiss", reaction_mode)
    else:
        $ set_scene_expression(girl, "angry")
        # the same selector as every flirt (rod_flirt_line): her own / shared ".player_cheating" etc. pools play here too
        $ Say_Line(girl, rod_flirt_line(girl, "safe_steal_kiss", reaction_mode) or "Back off. I did not say you could do that.")
        call Punch from _call_Punch_1
        $ set_scene_expression(girl, "normal")
        if girl.has_trait("lesbian"):
            $ Narration(_("A kiss seems to be the last thing she'd ever agree to. Try something else first."))

    return

# One accepted kiss outside a sex scene, with everything a kiss sets off: her first kiss (KISS_Launch), temptation,
# cheat heat, a lesbian's first-kiss reaction, the partner who may be watching (_flirt_partner_witness) and the
# guilt scene. Her line during it: `line`, or the steal-kiss flirt reaction (flirt_mode). Used by the flirt and by
# the breath-holding bet (swimming.rpy). The calls keep the flirt's old names: a save made mid-kiss still returns.
label _kiss_accepted(girl, line=None, flirt_mode=None):
    call KISS_Launch(girl) from _call_KISS_Launch
    call KISS_Smooch(girl) from _call_KISS_Smooch
    $ mark_intimacy(girl, "kiss")
    $ sex_accept_with_temptation(girl, "kiss")
    $ _notify_cheat_heat(girl, "kiss", True)
    if not (girl.has_trait("lesbian") and getattr(store, "_kiss_is_first", False)):
        if line:
            $ Say_Line(girl, line)
        elif flirt_mode:
            $ rod_flirt_say(girl, "safe_steal_kiss", flirt_mode)
    call KISS_End(girl) from _call_KISS_End
    if girl.has_trait("lesbian") and getattr(store, "_kiss_is_first", False):
        call _lesbian_first_kiss_reaction(girl) from _call_les_first_kiss_flirt
    # Her partner on scene sees the kiss first: if he confronts her, she is gone before any guilt scene
    call _flirt_partner_witness(girl) from _call_flirt_partner_witness_kiss
    if girl.loc != CurrentLocation:
        $ store._cheat_guilt_pending = False
        return
    if store._cheat_guilt_pending:
        call cheat_guilt_scene(girl) from _call_cheat_guilt_flirt_kiss
    return

label Flirt_Safe_Hug(girl, loc, t_index):
    $ base_result = do_safe_flirt(girl, "hug")
    $ reaction_mode = get_flirt_reaction_mode_safe(girl, base_result, "hug")
    $ rod_flirt_say(girl, "safe_hug", reaction_mode)
    return

label Flirt_Safe_ShoulderMassage(girl, loc, t_index):
    $ base_result = do_safe_flirt(girl, "shoulder_massage")
    $ reaction_mode = get_flirt_reaction_mode_safe(girl, base_result, "shoulder_massage")
    $ rod_flirt_say(girl, "safe_shoulder_massage", reaction_mode)
    return

# =========================================================
# COMPLIMENT FLIRT
# =========================================================
label Flirt_Compliment(girl, loc, t_index):

    if not girl:
        "There's no one here to compliment."
        return

    # Pick three random compliment options from COMPLIMENT_OPTIONS
    python:
        pool = list(COMPLIMENT_OPTIONS)
        # Student-only compliments (school, swimming, gym) don't apply to family-type girls
        _girl_type = GIRLS_CONFIG.get(girl.gid, {}).get("type", "student")
        if _girl_type != "student":
            _student_only = {"class", "class_grades", "dr_skill", "gym_weights"}
            pool = [c for c in pool if c[0] not in _student_only]
        renpy.random.shuffle(pool)

        opt0_key, opt0_text, opt0_kind = pool[0]
        opt1_key, opt1_text, opt1_kind = pool[1]
        opt2_key, opt2_text, opt2_kind = pool[2]
        opt0_text = _tl(opt0_text)
        opt1_text = _tl(opt1_text)
        opt2_text = _tl(opt2_text)

    menu:
        "You think for a moment about what to say..."
        "[opt0_text]":
            $ chosen_key = opt0_key
            $ chosen_kind = opt0_kind
        "[opt1_text]":
            $ chosen_key = opt1_key
            $ chosen_kind = opt1_kind
        "[opt2_text]":
            $ chosen_key = opt2_key
            $ chosen_kind = opt2_kind
        "These are all awful, I can do better...":
            $ Change_Status(girl, "Love", -2)
            $ Change_Status(girl, "Obed", -2)
            "You shake your head and try to come up with something better."
            call Flirt_Compliment(girl, loc, t_index) from _call_Flirt_Compliment_1
            return
        "Never mind":
            "You decide to stay quiet instead."
            return

    # Build a base action key so stats can treat compliments as a type of safe/lewd flirt
    $ action_key_base = "compliment_%s" % chosen_key

    # Track that the player complimented her body part (regardless of outcome)
    if chosen_key == "tits":
        $ girl.RegisterAction("complimented_tits")
    elif chosen_key == "ass":
        $ girl.RegisterAction("complimented_ass")

    if chosen_kind == "safe":
        # Safe compliments use the same comfort logic as other safe flirts
        $ base_result = do_safe_flirt(girl, action_key_base)
        $ reaction_mode = get_flirt_reaction_mode_safe(girl, base_result, action_key_base)
        $ rod_flirt_say(girl, "safe_%s" % action_key_base, reaction_mode)
    else:
        # Lewd compliments use ApprovalCheck-style logic
        $ result = do_lewd_flirt_approval(
            girl,
            action_key_base,
            T=950,
            Type="LI",
            Spread=170,
            Bonus=0,
            Variation=60
        )
        $ reaction_mode = get_flirt_reaction_mode_lewd(girl, result, action_key_base)
        $ rod_flirt_say(girl, "lewd_%s" % action_key_base, reaction_mode)
        if flirt_lewd_slaps(result, reaction_mode):
            call Punch from _call_Punch_2

    return

# =========================================================
# LEWD FLIRT MENU
# =========================================================
label Flirt_Lewd_Menu(girl, loc, t_index):

    menu:
        "Steal a quick kiss":
            call Flirt_Safe_StealKiss(girl, loc, t_index) from _call_Flirt_Safe_StealKiss
            return True

        "Ask for her panties":
            call Flirt_Lewd_AskPanties(girl, loc, t_index) from _call_Flirt_Lewd_AskPanties
            return True

        "Pinch her ass":
            call Flirt_Lewd_PinchAss(girl, loc, t_index) from _call_Flirt_Lewd_PinchAss
            return True

        "Slap her ass":
            call Flirt_Lewd_SlapAss(girl, loc, t_index) from _call_Flirt_Lewd_SlapAss
            return True

        "Grab her ass":
            call Flirt_Lewd_GrabAss(girl, loc, t_index) from _call_Flirt_Lewd_GrabAss
            return True

        "Grab her tits":
            call Flirt_Lewd_GrabTits(girl, loc, t_index) from _call_Flirt_Lewd_GrabTits
            return True

        "Touch her thighs":
            call Flirt_Lewd_TouchThighs(girl, loc, t_index) from _call_Flirt_Lewd_TouchThighs
            return True

        "Touch her tits":
            call Flirt_Lewd_TouchTits(girl, loc, t_index) from _call_Flirt_Lewd_TouchTits
            return True

        "Touch her pussy":
            call Flirt_Lewd_TouchPussy(girl, loc, t_index) from _call_Flirt_Lewd_TouchPussy
            return True

        "Back":
            "Maybe this isn't the right moment for that."
            return False

label Flirt_Lewd_SlapAss(girl, loc, t_index):
    $ slap_crack()
    $ result = do_lewd_flirt_approval(girl, "slap_ass", T=950, Type="OI", Spread=160, Variation=60, Bonus=0)
    $ reaction_mode = get_flirt_reaction_mode_lewd(girl, result, "slap_ass")
    $ rod_flirt_say(girl, "lewd_slap_ass", reaction_mode)
    # the slap landed whatever her answer: her spank record (SubEvents.rpy spank_note), enjoyed when her answer liked it
    $ spank_note(girl, reaction_mode in SPANK_FLIRT_ENJOYED_MODES, "flirt_slap_ass")
    if flirt_lewd_slaps(result, reaction_mode):
        call Punch from _call_Punch_3
    return

label Flirt_Lewd_PinchAss(girl, loc, t_index):
    $ result = do_lewd_flirt_approval(girl, "pinch_ass", T=900, Type="OI", Spread=150, Variation=50, Bonus=0)
    $ reaction_mode = get_flirt_reaction_mode_lewd(girl, result, "pinch_ass")
    $ rod_flirt_say(girl, "lewd_pinch_ass", reaction_mode)
    if flirt_lewd_slaps(result, reaction_mode):
        call Punch from _call_Punch_4
    return

label Flirt_Lewd_GrabTits(girl, loc, t_index):
    $ result = do_lewd_flirt_approval(girl, "grab_tits", T=1000, Type="LOI", Spread=170, Variation=70, Bonus=0)
    $ reaction_mode = get_flirt_reaction_mode_lewd(girl, result, "grab_tits")
    $ rod_flirt_say(girl, "lewd_grab_tits", reaction_mode)
    if flirt_lewd_slaps(result, reaction_mode):
        call Punch from _call_Punch_5
    return

label Flirt_Lewd_GrabAss(girl, loc, t_index):
    $ result = do_lewd_flirt_approval(girl, "grab_ass", T=950, Type="LOI", Spread=160, Variation=60, Bonus=0)
    $ reaction_mode = get_flirt_reaction_mode_lewd(girl, result, "grab_ass")
    $ rod_flirt_say(girl, "lewd_grab_ass", reaction_mode)
    if flirt_lewd_slaps(result, reaction_mode):
        call Punch from _call_Punch_6
    return

label Flirt_Lewd_AskPanties(girl, loc, t_index):
    $ result = do_lewd_flirt_approval(girl, "ask_panties", T=1050, Type="LI", Spread=180, Variation=70, Bonus=0)
    $ reaction_mode = get_flirt_reaction_mode_lewd(girl, result, "ask_panties")
    $ rod_flirt_say(girl, "lewd_ask_panties", reaction_mode)
    if flirt_lewd_slaps(result, reaction_mode):
        call Punch from _call_Punch_7
    return

# =========================================================
# TOUCH actions (with Player Hands overlay)
# =========================================================

label Flirt_Lewd_TouchThighs(girl, loc, t_index):
    $ result = do_lewd_flirt_approval(girl, "touch_thighs", T=900, Type="OI", Spread=150, Variation=50, Bonus=0)
    $ reaction_mode = get_flirt_reaction_mode_lewd(girl, result, "touch_thighs")

    python:
        _slot = getattr(girl, "SpriteLoc", StageCenter)
        if _slot == StageLeft:
            _hand_slot = slot_left
        elif _slot == StageRight:
            _hand_slot = slot_right
        else:
            _hand_slot = slot_center
        renpy.show("player_hands", at_list=[_hand_slot, player_hands_touch_bounce], zorder=10070)

    if result >= 2:
        $ set_scene_expression(girl, "surprised")
        $ rod_flirt_say(girl, "lewd_touch_thighs", reaction_mode)
        pause 1.0
    elif result == 1 or reaction_mode == "commanding_no":
        # a femdom girl never flips him off: she catches his wrist (rod_flirt_say) and sets the rule
        $ set_scene_expression(girl, "angry")
        $ rod_flirt_say(girl, "lewd_touch_thighs", reaction_mode)
    else:
        $ _set_standing_arm(girl, 2)
        $ set_scene_expression(girl, "angry")
        $ rod_flirt_say(girl, "lewd_touch_thighs", reaction_mode)
        $ _set_standing_arm(girl, 0)

    $ renpy.show("player_hands", at_list=[_hand_slot, player_hands_fade_out], zorder=10070)
    pause 0.3
    $ renpy.hide("player_hands")

    if flirt_lewd_slaps(result, reaction_mode):
        call Punch from _call_Punch_touch_thighs

    $ set_scene_expression(girl, "normal")
    return

label Flirt_Lewd_TouchTits(girl, loc, t_index):
    $ result = do_lewd_flirt_approval(girl, "touch_tits", T=1000, Type="LOI", Spread=170, Variation=60, Bonus=0)
    $ reaction_mode = get_flirt_reaction_mode_lewd(girl, result, "touch_tits")

    python:
        _slot = getattr(girl, "SpriteLoc", StageCenter)
        if _slot == StageLeft:
            _hand_slot = slot_left
        elif _slot == StageRight:
            _hand_slot = slot_right
        else:
            _hand_slot = slot_center
        renpy.show("player_hands", at_list=[_hand_slot, player_hands_touch_bounce], zorder=10070)

    if result >= 2:
        $ set_scene_expression(girl, "surprised")
        $ rod_flirt_say(girl, "lewd_touch_tits", reaction_mode)
        pause 1.0
    elif result == 1 or reaction_mode == "commanding_no":
        # a femdom girl never flips him off: she catches his wrist (rod_flirt_say) and sets the rule
        $ set_scene_expression(girl, "angry")
        $ rod_flirt_say(girl, "lewd_touch_tits", reaction_mode)
    else:
        $ _set_standing_arm(girl, 2)
        $ set_scene_expression(girl, "angry")
        $ rod_flirt_say(girl, "lewd_touch_tits", reaction_mode)
        $ _set_standing_arm(girl, 0)

    $ renpy.show("player_hands", at_list=[_hand_slot, player_hands_fade_out], zorder=10070)
    pause 0.3
    $ renpy.hide("player_hands")

    if result >= 2:
        $ set_scene_expression(girl, "sexy")
    elif flirt_lewd_slaps(result, reaction_mode):
        call Punch from _call_Punch_touch_tits
        $ set_scene_expression(girl, "normal")
    else:
        $ set_scene_expression(girl, "normal")

    return

label Flirt_Lewd_TouchPussy(girl, loc, t_index):
    $ result = do_lewd_flirt_approval(girl, "touch_pussy", T=1100, Type="LOI", Spread=180, Variation=70, Bonus=0)
    $ reaction_mode = get_flirt_reaction_mode_lewd(girl, result, "touch_pussy")

    python:
        _slot = getattr(girl, "SpriteLoc", StageCenter)
        if _slot == StageLeft:
            _hand_slot = slot_left
        elif _slot == StageRight:
            _hand_slot = slot_right
        else:
            _hand_slot = slot_center
        renpy.show("player_hands", at_list=[_hand_slot, player_hands_touch_bounce], zorder=10070)

    if result >= 2:
        $ set_scene_expression(girl, "surprised")
        $ rod_flirt_say(girl, "lewd_touch_pussy", reaction_mode)
        pause 1.0
        $ girl.RegisterAction("player_touched_pussy")
        $ Change_Status(girl, "Lust", 15)
    elif result == 1 or reaction_mode == "commanding_no":
        # a femdom girl never flips him off: she catches his wrist (rod_flirt_say) and sets the rule
        $ set_scene_expression(girl, "angry")
        $ rod_flirt_say(girl, "lewd_touch_pussy", reaction_mode)
    else:
        $ _set_standing_arm(girl, 2)
        $ set_scene_expression(girl, "angry")
        $ rod_flirt_say(girl, "lewd_touch_pussy", reaction_mode)
        $ _set_standing_arm(girl, 0)

    $ renpy.show("player_hands", at_list=[_hand_slot, player_hands_fade_out], zorder=10070)
    pause 0.3
    $ renpy.hide("player_hands")

    if result >= 2:
        $ set_scene_expression(girl, "sexy")
    elif flirt_lewd_slaps(result, reaction_mode):
        call Punch from _call_Punch_touch_pussy
        $ set_scene_expression(girl, "normal")
    else:
        $ set_scene_expression(girl, "normal")

    return

# =========================================================
# MASSAGE SYSTEM
# =========================================================
# ============================================================
# SUNSCREEN — Pool-only event, reuses massage sprites/transforms
# ============================================================
label _SunscreenStart(girl, loc, t_index):

    menu:
        "Sure, turn around.":
            $ Change_Status(girl, "Love", 5)
            $ Say_Line(girl, _("Thanks! You're the best."))
        "I'm good, thanks.":
            $ Change_Status(girl, "Obed", 3)
            $ Say_Line(girl, _("Fine... I'll just burn then."))
            return

    # Switch to rear pose (RCG or LD depending on girl)
    python:
        girl._massage_prev_pose = getattr(girl, "default_pose", "standing")
        girl._massage_prev_slot = getattr(girl, "SpriteLoc", StageCenter)
        if not getattr(girl, "_saved_outfit", None):
            girl.SaveOutfit()

        # Stop standing blink and hide standing sprite before switching
        stop_standing_blink(girl)
        hide_girl_sprite(girl)

        store._sunscreen_use_ld = _setup_rear_pose_vars(girl)
        store._sunscreen_top_removed = False

    if store._sunscreen_use_ld == "doggy":
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_sunscreen
    elif store._sunscreen_use_ld == "laying_down":
        call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_sunscreen
    else:
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_sunscreen
    with dissolve

    $ _start_rear_blink(girl)

    call _SunscreenLoop(girl, loc, t_index) from _call_SunscreenLoop

    if store._sunscreen_use_ld == "doggy":
        $ store._dg_massage = False
        call DG_End(girl, dress_up=True) from _call_DG_End_sunscreen
    elif store._sunscreen_use_ld == "laying_down":
        call LD_End(girl, dress_up=True) from _call_LD_End_sunscreen
    else:
        call RCG_End(girl, dress_up=True) from _call_RCG_End_sunscreen
    return

label _SunscreenLoop(girl, loc, t_index):

    while True:
        menu:
            "Rub her shoulders":
                $ renpy.show("massage_hands", at_list=[massage_hands_shoulders], zorder=10070)
                python:
                    _lines = [
                        _("Mmm... make sure you get it everywhere."),
                        _("Your hands are so warm..."),
                        _("That feels nice... don't miss a spot."),
                    ]
                $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                $ Change_Status(girl, "Love", 3)
                $ Change_Status(girl, "Lust", 2)
                $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
                pause 0.3
                $ renpy.hide("massage_hands")

            "Rub her back":
                $ renpy.show("massage_hands", at_list=[massage_hands_back], zorder=10070)
                python:
                    _lines = [
                        _("Yeah, right there... I always miss that part."),
                        _("Mmm... you're being very thorough."),
                        _("Make sure you get the lower back too..."),
                    ]
                $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                $ Change_Status(girl, "Love", 3)
                $ Change_Status(girl, "Lust", 3)
                $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
                pause 0.3
                $ renpy.hide("massage_hands")

            "Ask to remove top" if girl.Chest and not store._sunscreen_top_removed:
                $ Say_Player(_("It would be easier without the top. For better coverage."))
                $ _top_ok = ApprovalCheck(girl=girl, T=300, Type="LI", Spread=100, Variation=50, Action="sunscreen_top")
                if _top_ok >= 2:
                    python:
                        _lines = [
                            _("I guess that makes sense... fine. But ONLY the back."),
                            _("You better not be trying anything... okay, go ahead."),
                            _("Just... don't stare, okay?"),
                        ]
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ girl.clothes["chest"] = None
                    $ girl.clothes_state["chest"] = "full"
                    $ store._sunscreen_top_removed = True
                    if store._sunscreen_use_ld == "doggy":
                        call DG_ApplySpeed(girl, 0) from _call_DG_RefreshClothing_sun_top
                    elif store._sunscreen_use_ld == "laying_down":
                        call LD_ApplySpeed(girl, 0) from _call_LD_RefreshClothing_sun_top
                    else:
                        call RCG_RefreshClothing(girl) from _call_RCG_RefreshClothing_sun_top
                else:
                    python:
                        _lines = [
                            _("Nice try. The top stays on."),
                            _("I KNOW what you're doing. No."),
                            _("Just apply the sunscreen, perv."),
                        ]
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))

            "Rub her thighs":
                $ renpy.show("massage_hands", at_list=[massage_hands_thighs], zorder=10070)
                $ _appr = do_lewd_flirt_approval(girl, "sunscreen_thighs", T=500, Type="LI", Spread=150, Variation=50)
                if _appr >= 3:
                    # Level 3: she enjoys it and wants more
                    python:
                        _lines = [
                            _("Mmm... your hands feel so good on my thighs... don't stop."),
                            _("Higher... just a little higher... you're really good at this."),
                            _("I'm supposed to say stop but... keep going. Please."),
                        ]
                    $ flirt_lewd_react(girl, "sunscreen_thighs", _appr, "lusty", _lines)
                    $ Change_Status(girl, "Lust", 10)
                    $ Change_Status(girl, "Inbt", 5)
                    $ Change_Status(girl, "Love", 2)
                elif _appr == 2:
                    # Level 2: she likes it but pretends she doesn't
                    python:
                        _lines = [
                            _("H-hey... that's not my back... but I guess it needs sunscreen too..."),
                            _("You're getting a little close there... not that it feels bad or anything..."),
                            _("I didn't ask for that... but... fine. Just this once."),
                        ]
                    $ flirt_lewd_react(girl, "sunscreen_thighs", _appr, "embarrassed", _lines)
                    $ Change_Status(girl, "Lust", 6)
                    $ Change_Status(girl, "Inbt", 3)
                else:
                    # Level 1: she hates it and complains
                    python:
                        _lines = [
                            _("I said my BACK! What are you doing?!"),
                            _("Hey! I can do my own legs, thanks!"),
                            _("That's NOT my back and you know it!"),
                        ]
                    $ flirt_lewd_react(girl, "sunscreen_thighs", _appr, "angry", _lines)
                    $ Change_Status(girl, "Love", -2)
                $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
                pause 0.3
                $ renpy.hide("massage_hands")

            "Rub her ass":
                $ _appr = do_lewd_flirt_approval(girl, "sunscreen_ass", T=600, Type="LI", Spread=160, Variation=60)
                if _appr >= 3:
                    # Level 3: she loves it and wants more
                    $ renpy.show(_rear_grab_img(girl, "left"), tag="massage_ass", at_list=_rear_grab_at(girl), zorder=10070)
                    python:
                        _lines = [
                            _("Mmm... you don't have to stop there... grab it harder."),
                            _("That's... not sunscreen anymore, is it? I don't care. Keep going."),
                            _("You have no idea how good that feels... squeeze harder."),
                        ]
                    $ flirt_lewd_react(girl, "sunscreen_ass", _appr, "lusty", _lines)
                    $ Change_Status(girl, "Lust", 15)
                    $ Change_Status(girl, "Inbt", 8)
                    if not femdom_flirt_mode(girl, _appr, "sunscreen_ass"):
                        $ Change_Status(girl, "Obed", 3)
                    $ Change_Status(girl, "Love", 2)
                    $ renpy.show(_rear_grab_img(girl, "left"), tag="massage_ass", at_list=[massage_hands_fade_out], zorder=10070)
                    pause 0.3
                    $ renpy.hide("massage_ass")
                elif _appr == 2:
                    # Level 2: she likes it but tries to deny it
                    $ renpy.show(_rear_grab_img(girl, "left"), tag="massage_ass", at_list=_rear_grab_at(girl), zorder=10070)
                    python:
                        _lines = [
                            _("That is DEFINITELY not my back... but fine. I guess it needs coverage."),
                            _("You're really pushing it... it's not like it feels good or anything..."),
                            _("I should tell you to stop... but... just make sure you cover everywhere."),
                        ]
                    $ flirt_lewd_react(girl, "sunscreen_ass", _appr, "embarrassed", _lines)
                    $ Change_Status(girl, "Lust", 10)
                    $ Change_Status(girl, "Inbt", 5)
                    if not femdom_flirt_mode(girl, _appr, "sunscreen_ass"):
                        $ Change_Status(girl, "Obed", 2)
                    $ renpy.show(_rear_grab_img(girl, "left"), tag="massage_ass", at_list=[massage_hands_fade_out], zorder=10070)
                    pause 0.3
                    $ renpy.hide("massage_ass")
                else:
                    # Level 1: she hates it and complains
                    $ renpy.show(_rear_grab_img(girl, "left"), tag="massage_ass", at_list=_rear_grab_at(girl), zorder=10070)
                    python:
                        _lines = [
                            _("THAT is my ASS, not my back! Hands OFF!"),
                            _("Okay, sunscreen is OVER. You ruined it."),
                            _("I KNEW you'd try something! Don't touch me there!"),
                        ]
                    $ flirt_lewd_react(girl, "sunscreen_ass", _appr, "angry", _lines)
                    $ Change_Status(girl, "Love", -3)
                    $ renpy.show(_rear_grab_img(girl, "left"), tag="massage_ass", at_list=[massage_hands_fade_out], zorder=10070)
                    pause 0.3
                    $ renpy.hide("massage_ass")

            "'Rub' with your dick":
                $ Say_Player(_("I know something that would spread even better..."))
                $ _rub = rub_check(girl)
                if _rub["accepted"]:
                    call start_rub(girl, _rear_pose_for(girl)) from _call_start_rub_sunscreen
                    return
                else:
                    python:
                        _deny = [
                            _("You're disgusting. I asked for SUNSCREEN."),
                            _("And just like that, you ruined a nice moment."),
                            _("I can't believe you just said that."),
                        ]
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _tl(renpy.random.choice(_deny)))
                    $ Change_Status(girl, "Love", -5)
                    return

            "Done":
                python:
                    _lines = [
                        _("Thanks! My back feels protected now."),
                        _("All done? Great, thanks for the help."),
                        _("You're hired as my personal sunscreen applicator."),
                    ]
                $ set_scene_expression(girl, "smile")
                $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                return

# ============================================================
# MASSAGE SYSTEM
# ============================================================
label Flirt_MassageMenu(girl, loc, t_index):

    if getattr(girl, "_last_massage_day", -1) == Day:
        python:
            _cooldown_lines = [
                _("Another massage? I'm still relaxed from the last one."),
                _("I don't need another massage today. Maybe tomorrow."),
                _("My muscles are fine. You already massaged me today."),
            ]
        $ Say_Line(girl, _tl(renpy.random.choice(_cooldown_lines)))
        return

    $ base_result = do_safe_flirt(girl, "shoulder_massage")

    if base_result != "ok":
        $ reaction_mode = get_flirt_reaction_mode_safe(girl, base_result, "shoulder_massage")
        $ rod_flirt_say(girl, "safe_shoulder_massage", reaction_mode)
        call _flirt_partner_witness(girl) from _call_flirt_partner_witness_massage_no
        return

    # She accepts - switch to RCG pose (keep all clothes)
    python:
        girl._massage_prev_pose = getattr(girl, "default_pose", "standing")
        girl._massage_prev_slot = getattr(girl, "SpriteLoc", StageCenter)
        if not getattr(girl, "_saved_outfit", None):
            girl.SaveOutfit()

        # Stop standing blink and hide standing sprite before switching
        stop_standing_blink(girl)
        hide_girl_sprite(girl)

        store._massage_use_ld = _setup_rear_pose_vars(girl)

    if store._massage_use_ld == "doggy":
        call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_massage
    elif store._massage_use_ld == "laying_down":
        call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_massage
    else:
        call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_massage
    with dissolve

    $ _start_rear_blink(girl)

    python:
        if getattr(store, "_massage_partner_present", False):
            _massage_lines = [
                _("Okay, but my %(pl)s is right there. No funny stuff."),
                _("Fine... but %(pn)s is literally right there, so behave."),
                _("A massage? With my %(pl)s here? ...Okay, but keep your hands where they belong."),
            ]
            _m_line = _format_partner_line(girl, renpy.random.choice(_massage_lines))
        else:
            _massage_lines = [
                _("Mmm... okay, that feels nice."),
                _("A massage? Sure, I could use one."),
                _("Alright... don't get any funny ideas though."),
            ]
            _m_line = _tl(renpy.random.choice(_massage_lines))
    $ Say_Line(girl, _m_line)

    # Massage loop
    call _MassageLoop(girl, loc, t_index) from _call_MassageLoop

    $ girl._last_massage_day = Day

    # End - restore standing
    if store._massage_use_ld == "doggy":
        $ store._dg_massage = False
        call DG_End(girl, dress_up=True) from _call_DG_End_massage
    elif store._massage_use_ld == "laying_down":
        call LD_End(girl, dress_up=True) from _call_LD_End_massage
    else:
        call RCG_End(girl, dress_up=True) from _call_RCG_End_massage
    # Her partner on scene: did he see the massage? (standing again, so she can go after him)
    call _flirt_partner_witness(girl) from _call_flirt_partner_witness_massage
    return

label _MassageLoop(girl, loc, t_index):

    $ _massage_count = 0
    # [MASSAGE] rollback after the dick refusal sent a player to the main menu (tester 2026-10-10, not
    # reproduced). A silent main menu = a return on an empty call stack, so the depth is logged at the
    # loop's start and at the refusal: the next log.txt says whether the stack was already short here.
    $ print("[MASSAGE] loop start: %s, return stack depth %d" % (girl.gid, len(renpy.game.context().return_stack)))

    while True:

        # ── Guard: max 7 massage actions ──
        if _massage_count >= 7:
            python:
                _lines = [
                    _("Okay, I think that's enough for now. My body can only take so much."),
                    _("That was a long massage... I'm all loosened up. Let's stop here."),
                    _("Alright, I think you've massaged every inch of me. We're done."),
                ]
            $ set_scene_expression(girl, "smile")
            $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
            return

        # ── Guard: time ran out ──
        if Round >= 100:
            python:
                _lines = [
                    _("It's getting late... we should stop."),
                    _("We've been at this for a while... I should go."),
                    _("Okay, I need to stop. It's late."),
                ]
            $ set_scene_expression(girl, "neutral")
            $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
            return

        menu:
            "Massage her shoulders":
                $ renpy.show("massage_hands", at_list=[massage_hands_shoulders], zorder=10070)
                python:
                    _lines = [
                        _("Mmm... right there. That feels good."),
                        _("You're pretty good at this."),
                        _("I needed this... keep going."),
                    ]
                $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                $ Change_Status(girl, "Love", 1)
                $ Change_Status(girl, "Lust", 1)
                $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
                pause 0.3
                $ renpy.hide("massage_hands")
                $ advance_round(5)
                $ _massage_count += 1

            "Massage her back":
                $ renpy.show("massage_hands", at_list=[massage_hands_back], zorder=10070)
                python:
                    _lines = [
                        _("Ahh... my back is so tense."),
                        _("Lower... yeah, right there."),
                        _("You have strong hands..."),
                    ]
                $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                $ Change_Status(girl, "Love", 1)
                $ Change_Status(girl, "Lust", 2)
                $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
                pause 0.3
                $ renpy.hide("massage_hands")
                $ advance_round(5)
                $ _massage_count += 1

            "Massage her thighs":
                $ renpy.show("massage_hands", at_list=[massage_hands_thighs], zorder=10070)
                python:
                    _r = ApprovalCheck(girl=girl, T=350, Type="LI", Spread=150, Variation=50, ReturnData=True)
                    _appr = 3 if _r["accepted"] and _r.get("value", 0) >= _r.get("threshold", 350) + 80 else (2 if _r["accepted"] else 1)
                if _appr >= 3:
                    python:
                        _lines = [
                            _("Mmm... higher... just a little higher... please."),
                            _("Your hands on my thighs... don't you dare stop."),
                            _("God, that feels amazing... I want more of that."),
                        ]
                    $ set_scene_expression(girl, "lusty")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ Change_Status(girl, "Lust", 6)
                    $ Change_Status(girl, "Inbt", 3)
                    $ Change_Status(girl, "Love", 1)
                elif _appr == 2:
                    python:
                        _lines = [
                            _("H-hey... that's a bit low... but I guess it's fine."),
                            _("My thighs...? I didn't say you could... but don't stop."),
                            _("That's... not where I expected. It's not bad though..."),
                        ]
                    $ set_scene_expression(girl, "embarrassed")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ Change_Status(girl, "Lust", 4)
                    $ Change_Status(girl, "Inbt", 2)
                else:
                    python:
                        _lines = [
                            _("Hey! That's too low! I said massage, not grope!"),
                            _("Watch your hands! That's NOT where I asked!"),
                            _("Okay, that's way too close. Hands up. NOW."),
                        ]
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ Change_Status(girl, "Love", -2)
                $ renpy.show("massage_hands", at_list=[massage_hands_fade_out], zorder=10070)
                pause 0.3
                $ renpy.hide("massage_hands")
                $ advance_round(5)
                $ _massage_count += 1

            "Massage her ass":
                python:
                    _r = ApprovalCheck(girl=girl, T=400, Type="LI", Spread=160, Variation=60, ReturnData=True)
                    _appr = 3 if _r["accepted"] and _r.get("value", 0) >= _r.get("threshold", 400) + 80 else (2 if _r["accepted"] else 1)
                $ _grab_img = _rear_grab_img(girl, "left")
                if _appr >= 3:
                    $ renpy.show(_grab_img, tag="massage_ass", at_list=_rear_grab_at(girl), zorder=10070)
                    python:
                        _lines = [
                            _("Mmm... grab it harder. I don't care anymore."),
                            _("That's not a massage and we both know it... don't stop."),
                            _("You're so bad... but your hands feel so good there."),
                        ]
                    $ set_scene_expression(girl, "lusty")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ Change_Status(girl, "Lust", 8)
                    $ Change_Status(girl, "Inbt", 4)
                    $ Change_Status(girl, "Obed", 2)
                    $ Change_Status(girl, "Love", 1)
                    $ renpy.show(_grab_img, tag="massage_ass", at_list=[massage_hands_fade_out], zorder=10070)
                    pause 0.3
                    $ renpy.hide("massage_ass")
                elif _appr == 2:
                    $ renpy.show(_grab_img, tag="massage_ass", at_list=_rear_grab_at(girl), zorder=10070)
                    python:
                        _lines = [
                            _("That's not a massage anymore... but I'm not complaining."),
                            _("H-hey... you're grabbing, not massaging... it's fine I guess."),
                            _("I should tell you to stop... but it actually feels nice..."),
                        ]
                    $ set_scene_expression(girl, "embarrassed")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ Change_Status(girl, "Lust", 5)
                    $ Change_Status(girl, "Inbt", 3)
                    $ Change_Status(girl, "Obed", 1)
                    $ renpy.show(_grab_img, tag="massage_ass", at_list=[massage_hands_fade_out], zorder=10070)
                    pause 0.3
                    $ renpy.hide("massage_ass")
                else:
                    $ renpy.show(_grab_img, tag="massage_ass", at_list=_rear_grab_at(girl), zorder=10070)
                    python:
                        _lines = [
                            _("HEY! That is NOT a massage! Hands OFF!"),
                            _("I said massage, not grab! Back off!"),
                            _("Get your hands off my ass RIGHT NOW!"),
                        ]
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ Change_Status(girl, "Love", -3)
                    $ renpy.show(_grab_img, tag="massage_ass", at_list=[massage_hands_fade_out], zorder=10070)
                    pause 0.3
                    $ renpy.hide("massage_ass")
                $ advance_round(5)
                $ _massage_count += 1

            "Slap her ass":
                python:
                    _slap_side = renpy.random.choice(["right", "left"])
                    _slap_img = _rear_slap_img(girl, _slap_side)
                    _slap_tf = _rear_slap_tf(girl, _slap_side)

                # the shared crack (slap_crack, SubEvents.rpy; tester 2026-10-10: it was mute here)
                $ slap_crack()
                show expression _slap_img as massage_slap at _slap_tf zorder 10050
                $ renpy.pause(0.08)
                show layer master at bj_slap_shake
                $ renpy.pause(0.40)
                hide massage_slap
                show layer master

                if girl.has_trait("hardcore_sex"):
                    python:
                        _lines = [
                            _("Ooh! I like this kind of massage~"),
                            _("Mmm, do that again! Harder!"),
                            _("Now THAT'S my kind of massage."),
                            _("Again! Don't be gentle!"),
                        ]
                    $ set_scene_expression(girl, "lusty")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ girl.discover("discovered_trait_hardcore_sex")
                    $ Change_Status(girl, "Obed", 2)
                    $ Change_Status(girl, "Inbt", 2)
                    $ girl.Lust = min(100, getattr(girl, "Lust", 0) + 3)
                elif girl.has_trait("cute_sex"):
                    python:
                        _lines = [
                            _("Ow! W-what was that?! This is a massage!"),
                            _("Hey! That hurt! Be gentle with me..."),
                            _("Ow! I said massage, not spank!"),
                        ]
                    $ set_scene_expression(girl, "scared")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ girl.discover("discovered_trait_cute_sex")
                    $ Change_Status(girl, "Love", trait_love_loss(girl, -2))
                    $ Change_Status(girl, "Obed", 1)
                else:
                    python:
                        _lines = [
                            _("Ouch! What was that? This is a massage!"),
                            _("Hey! Watch it! That's not a massage move."),
                            _("Did you just slap my ass?! Seriously?"),
                        ]
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ Change_Status(girl, "Love", trait_love_loss(girl, -1))
                    $ Change_Status(girl, "Obed", 2)
                # her spank record, like every other ass slap (spank_note; the face slaps never come here)
                $ spank_note(girl, girl.has_trait("hardcore_sex"), "massage_slap_ass")
                $ advance_round(1)   # a slap costs what every other slap costs, not a massage step (tester 2026-10-11)
                $ _massage_count += 1

            "'Massage' with your dick":
                $ Say_Player(_("Let me try a different kind of massage..."))
                $ print("[MASSAGE] dick ask: %s, return stack depth %d" % (girl.gid, len(renpy.game.context().return_stack)))
                $ _rub = rub_check(girl)
                if _rub["accepted"]:
                    python:
                        _is_cute = girl.has_trait("cute_sex")
                        _is_hc = girl.has_trait("hardcore_sex")
                        if _is_cute:
                            _lines = [
                                _("W-what is that?! That's not your hands! ...oh god... okay, keep going..."),
                                _("Is that your... that's NOT a massage! ...but it feels warm..."),
                                _("You're rubbing THAT against me?! I... I can't believe I'm letting you..."),
                            ]
                            girl.discover("discovered_trait_cute_sex")
                        elif _is_hc:
                            _lines = [
                                _("Oh, THAT kind of massage? Sure. Go ahead."),
                                _("Finally getting to the real massage, huh? Don't be shy."),
                                _("I was wondering when you'd try this. Go for it."),
                            ]
                            girl.discover("discovered_trait_hardcore_sex")
                        else:
                            _lines = [
                                _("That is definitely not your hand... fine, just rub. Nothing more."),
                                _("You're such a pervert... okay, just rubbing though."),
                                _("I can feel that's not a massage... but okay, don't push it."),
                            ]
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    python:
                        _rub_pose = _rear_pose_for(girl)
                        if _rub_pose == "laying_down":
                            store.laying_rub_mode = True
                            store.laying_started = False
                        else:
                            store.rcg_rub_mode = True
                            store.rcg_started = False
                        session_cum_reset()
                        store._player_exhausted = False
                        store._hate_cum_scene_aborted = False
                        store._condom_removed_midscene = False
                        store._creampie_consent = "denied"
                        store._scene_condom_break = False
                        store._scene_condom_break_believed = False
                        store._player_exposed_this_session = False
                        # Stop massage blink/expression threads before rub starts its own
                        if _rub_pose == "laying_down":
                            store._laying_girl = None
                            renpy.pause(0.3)
                            store._laying_girl = girl
                        else:
                            store._rcg_girl = None
                            renpy.pause(0.3)
                            store._rcg_girl = girl
                    call start_rub(girl, _rub_pose) from _call_start_rub_massage
                    return
                else:
                    python:
                        _lines = [
                            _("WHAT?! No! That is NOT happening! Massage is OVER!"),
                            _("Are you serious?! Put that away! We're done here!"),
                            _("Absolutely NOT! What kind of massage is that?!"),
                        ]
                    $ set_scene_expression(girl, "angry")
                    $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                    $ Change_Status(girl, "Love", -5)
                    $ print("[MASSAGE] dick refused: %s, return stack depth %d (rollback-to-main-menu watch)" % (girl.gid, len(renpy.game.context().return_stack)))
                    return

            "Ask her to undress" if girl.Over or girl.Chest or girl.Legs or girl.Panties or getattr(girl, "Shoes", None):
                call _MassageStripRequest(girl, loc) from _call_MassageStripRequest

            "Stop":
                python:
                    _lines = [
                        _("That was nice. Thanks."),
                        _("Mmm... I feel better. Thank you."),
                        _("Not bad. You can do that again sometime."),
                    ]
                $ set_scene_expression(girl, "smile")
                $ Say_Line(girl, _tl(renpy.random.choice(_lines)))
                return

label _MassageStripRequest(girl, loc):

    python:
        _massage_public = _is_public_location(loc)
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _is_cute = girl.has_trait("cute_sex")
        _is_hc = girl.has_trait("hardcore_sex")
        _is_shy = girl.has_trait("public_shy")
        _is_virgin = girl.has_trait("virgin")
        _is_nerd = girl.has_trait("nerd")
        _msp = MASSAGE_STRIP_PERSONALITY.get(girl.gid)
        _lust = getattr(girl, "Lust", 0)
        _inbt = getattr(girl, "Inbt", 0)
        _obed = getattr(girl, "Obed", 0)

        # What can be removed next (order: over > mid > legs > chest > panties > shoes)
        _strip_piece = None
        _strip_slot = None
        _strip_is_pants = False
        if girl.Over:
            _strip_piece = "top"
            _strip_slot = "over"
        elif girl.Mid:
            _strip_piece = "top"
            _strip_slot = "mid"
        elif girl.Legs:
            _strip_piece = "skirt"
            _strip_slot = "legs"
            _strip_is_pants = _strip_name_for_slot(girl, "skirt") == "pants"
        elif girl.Chest:
            _strip_piece = "bra"
            _strip_slot = "chest"
        elif girl.Panties:
            _strip_piece = "panties"
            _strip_slot = "panties"
        elif getattr(girl, "Shoes", None):
            _strip_piece = "shoes"
            _strip_slot = "shoes"

    if not _strip_piece:
        "She's already completely undressed."
        return

    # Player asks
    if _strip_piece == "top":
        $ Say_Player(_("It would be easier to massage you without your top on..."))
    elif _strip_piece == "skirt":
        if _strip_is_pants:
            $ Say_Player(_("Your pants are getting in the way... can you take them off?"))
        else:
            $ Say_Player(_("Your skirt is getting in the way... can you take it off?"))
    elif _strip_piece == "bra":
        $ Say_Player(_("I can't reach your back properly with this on..."))
    elif _strip_piece == "panties":
        $ Say_Player(_("You'd be more comfortable without those..."))
    elif _strip_piece == "shoes":
        $ Say_Player(_("Let me take those off for you..."))

    # Approval check - harder for intimate pieces, public, shy, virgin, bf
    python:
        _base_t = {"top": 400, "skirt": 500, "bra": 600, "panties": 750, "shoes": 300}
        _t = _base_t.get(_strip_piece, 950)

        # Public penalty
        if _massage_public:
            _t += 200

        # Public shy in public: even harder
        if _massage_public and _is_shy:
            _t += 150

        # Virgin penalty for intimate pieces
        if _is_virgin and _strip_piece in ("bra", "panties"):
            _t += 100

        # Cute sex: more reluctant
        _bonus_mod = 0
        if _is_cute:
            _bonus_mod -= 50
        # Hardcore: easier
        if _is_hc:
            _bonus_mod += 80

        # BF penalty
        _bf_penalty = 0
        if _has_bf:
            _bf_penalty = 100

        _strip_rule = ApprovalRuleFor(girl, "touch_massage", "sex")
        _strip_rule = dict(_strip_rule)
        _strip_rule["T"] = _t
        _strip_rule["Bonus"] = _strip_rule.get("Bonus", 0) - _bf_penalty + _bonus_mod
        _strip_rule["Type"] = "LOI"
        _strip_rule["Spread"] = 170
        _strip_rule["Variation"] = 60

        _strip_result = ApprovalCheck(girl, ReturnData=True, **_strip_rule)

    if _strip_result["accepted"]:
        # She accepts
        python:
            _msp_lines = _msp.get("accept", {}).get(_strip_piece) if _msp else None

            if _msp_lines:
                _accept = list(_msp_lines)
            elif _strip_piece == "top":
                if _is_virgin:
                    _accept = [_("I-I've never undressed for anyone before... okay, just the top..."), _("N-nobody's ever seen me... fine, just for the massage..."), _("This is my first time doing this... don't judge me...")]
                elif _is_cute:
                    _accept = [_("O-okay... but don't stare..."), _("Fine... just for the massage."), _("I guess that makes sense...")]
                elif _is_nerd:
                    _accept = [_("This is NOT in any textbook I've ever read... fine, just the top."), _("If anyone from my study group sees me..."), _("This goes against every rational decision I've ever made...")]
                elif _is_hc:
                    _accept = [_("Sure. Take it off yourself if you want."), _("About time you asked."), _("Go ahead. I don't mind.")]
                elif _has_bf:
                    _accept = [_("My %(pl)s wouldn't like this... but okay, just for the massage."), _("Fine... but this stays between us."), _("I shouldn't... okay, just this once.")]
                else:
                    _accept = [_("Okay... I guess that makes sense."), _("Fine, but only because it's a massage."), _("Alright... don't make it weird.")]
            elif _strip_piece == "skirt":
                if _is_virgin:
                    if _strip_is_pants:
                        _accept = [_("M-my pants too?! This is getting... okay, but please don't look at my..."), _("I've never been this undressed in front of someone..."), _("You promise this is just a massage, right...?")]
                    else:
                        _accept = [_("M-my skirt too?! This is getting... okay, but please don't look at my..."), _("I've never been this undressed in front of someone..."), _("You promise this is just a massage, right...?")]
                elif _is_cute:
                    if _strip_is_pants:
                        _accept = [_("M-my pants...? Okay... just don't look too much..."), _("This is embarrassing... but fine."), _("Promise you'll keep massaging?")]
                    else:
                        _accept = [_("M-my skirt...? Okay... just don't look too much..."), _("This is embarrassing... but fine."), _("Promise you'll keep massaging?")]
                elif _is_nerd:
                    _accept = [_("If anyone walks in, my academic career is over before it started..."), _("I should be studying right now, not... okay, just for the massage."), _("The risk-reward ratio of this is terrible... fine.")]
                elif _is_hc:
                    _accept = [_("Sure. Less clothes, better massage, right?"), _("Take it off. I don't care."), _("Was wondering when you'd ask.")]
                elif _has_bf:
                    _accept = [_("If %(pp)s could see me now... okay, fine."), _("This is so wrong... but the massage feels too good to stop."), _("Just... don't tell anyone.")]
                else:
                    _accept = [_("Okay... but this is just for the massage."), _("Fine... I trust you."), _("Alright, but keep those hands where they should be.")]
            elif _strip_piece == "bra":
                if _is_virgin:
                    _accept = [_("N-no one has ever seen my... okay... just don't stare... please..."), _("I can't believe I'm doing this... my heart is racing..."), _("T-this is the first time anyone... okay, just massage...")]
                elif _is_cute:
                    _accept = [_("M-my bra too?! I... okay... just... be professional..."), _("This is really embarrassing..."), _("D-don't look...")]
                elif _is_nerd:
                    _accept = [_("This is so far from anything I've ever studied..."), _("I'm supposed to be the responsible one... fine."), _("No textbook could have prepared me for this...")]
                elif _is_hc:
                    _accept = [_("Finally. These were getting in the way anyway."), _("Sure. Enjoy the view."), _("About time.")]
                elif _has_bf:
                    _accept = [_("%(Pp)s would lose %(poss)s mind if %(pp)s saw this... fine."), _("I can't believe I'm doing this..."), _("This is wrong on so many levels... okay.")]
                else:
                    _accept = [_("My bra...? That's... okay, fine. Just massage."), _("This is getting a bit much... but okay."), _("Alright, but this doesn't mean anything.")]
            elif _strip_piece == "panties":
                if _is_virgin:
                    _accept = [_("I... nobody has ever seen me completely... my heart won't stop pounding..."), _("I can't believe this is happening... okay... just... be gentle with me..."), _("E-everything off?! I've never been naked in front of... okay... just don't laugh...")]
                elif _is_cute:
                    _accept = [_("E-everything?! I... I can't believe I'm doing this..."), _("O-okay... but you HAVE to keep massaging. No funny business!"), _("This is so embarrassing I could die...")]
                elif _is_nerd:
                    _accept = [_("Every rational thought I have is screaming at me to stop..."), _("If my parents knew what their scholarship money led to..."), _("The statistical probability of getting caught right now is terrifying...")]
                elif _is_hc:
                    _accept = [_("Sure. Like you haven't seen it all before."), _("Panties off. Happy now?"), _("You wanted the full experience? Here.")]
                elif _has_bf:
                    _accept = [_("I'm completely naked in front of someone who isn't my %(pl)s... what am I doing?"), _("If %(pp)s finds out... okay. Just... keep massaging."), _("I've gone too far to stop now...")]
                else:
                    _accept = [_("My panties too? You're really pushing it... fine."), _("I hope you know what you're doing..."), _("Okay, but this is JUST a massage. Clear?")]
            elif _strip_piece == "shoes":
                _accept = [_("Sure, go ahead."), _("Okay. They were getting warm anyway."), _("Fine. More comfortable without them.")]

            if _massage_public:
                if _msp and "pub_suffix" in _msp:
                    _pub_suffix = " " + _msp["pub_suffix"]
                elif _is_nerd and loc in ("classroom", "campus"):
                    _pub_suffix = " " + _("If my professor walks in, I'm DEAD!")
                elif _is_shy:
                    _pub_suffix = " " + _("Oh god, what if someone SEES us?!")
                else:
                    _pub_suffix = " " + _("...and make sure nobody's watching!")
                _accept = [a + _pub_suffix for a in _accept]

        $ set_scene_expression(girl, "shy")
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice(_accept)))
        python:
            # her accept line itself states it: the virgin pool ("I've never undressed for anyone")
            # and the nerd pool (the textbook/study voice). Cute/hardcore pools are tone, no reveal.
            # The chain is virgin > cute > nerd > ... for every piece; girl-specific pools replace them.
            if not _msp_lines and _strip_piece != "shoes" and hasattr(girl, "discover"):
                if _is_virgin:
                    girl.discover("discovered_trait_virgin")
                elif not _is_cute and _is_nerd:
                    girl.discover("discovered_trait_nerd")
        $ girl.Outfit_Change(**{_strip_slot: "none", "pose": _rear_pose_for(girl)})
        if store._massage_use_ld == "doggy":
            call DG_ApplySpeed(girl, 0) from _call_DG_ApplySpeed_massage_strip
        elif store._massage_use_ld == "laying_down":
            call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_massage_strip
        else:
            call RCG_ApplySpeed(girl, 0) from _call_RCG_ApplySpeed_massage_strip

        # Exposure check: only triggers when actually exposed
        # Boobs: both Over AND Chest must be None (some girls have only one)
        # Pussy: Panties must be None (skirt alone doesn't cover)
        python:
            _chest_exposed = not girl.Over and not girl.Mid and not girl.Chest
            _bottom_exposed = not girl.Panties

            store._massage_first_exposure = None
            if _chest_exposed and _strip_piece in ("bra", "top"):
                _exp = girl.RegisterAction("player_saw_boobs")
                if _exp["first_time"]:
                    store._massage_first_exposure = "boobs"
            elif _bottom_exposed and _strip_piece == "panties":
                _exp = girl.RegisterAction("player_saw_pussy")
                if _exp["first_time"]:
                    store._massage_first_exposure = "pussy"

        if getattr(store, "_massage_first_exposure", None):
            call FirstExposureReaction(girl, store._massage_first_exposure) from _call_FirstExposureReaction_massage
            $ store._massage_first_exposure = None

        $ Change_Status(girl, "Inbt", 5)
        $ Change_Status(girl, "Obed", 3)

        if _has_bf:
            $ Change_Status(girl, "Obed", 3)
            $ girl.add_temptation(1)

    else:
        # She refuses
        python:
            if _strip_piece == "top":
                _deny = [_("No way. The massage is fine with my clothes on."), _("I'm not taking that off."), _("Nice try. Keep massaging.")]
            elif _strip_piece == "skirt":
                if _strip_is_pants:
                    _deny = [_("My pants stay on."), _("No. Just massage over the clothes."), _("You wish. Keep going as is.")]
                else:
                    _deny = [_("My skirt stays on."), _("No. Just massage over the clothes."), _("You wish. Keep going as is.")]
            elif _strip_piece == "bra":
                _deny = [_("Absolutely not. You've seen enough."), _("No way. That's too far."), _("The bra stays on. End of discussion.")]
            elif _strip_piece == "panties":
                _deny = [_("Are you KIDDING? No!"), _("Absolutely not! What kind of massage is this?!"), _("NO. That's way too far.")]
            elif _strip_piece == "shoes":
                _deny = [_("No, I'm keeping those on."), _("My shoes stay. Just massage."), _("Leave them. They're fine.")]

            if _massage_public:
                if _msp and "pub_deny" in _msp:
                    _deny = list(_msp["pub_deny"])
                elif _is_nerd and loc in ("classroom", "campus"):
                    _deny = [_("Are you OUT OF YOUR MIND?! My classmates walk by here! My PROFESSOR could come back!"), _("I have a REPUTATION here! I'm not risking my entire academic career!"), _("Do you know how hard I worked to get here?! I'm not throwing it away!")]
                else:
                    _deny = [_("Are you crazy?! We're in PUBLIC! No!"), _("Someone could SEE us! Absolutely not!"), _("Not here! Are you insane?!")]

        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, renpy.random.choice(_deny))

    return
