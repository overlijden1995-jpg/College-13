# ============================================================
# VIRGINITY LOSS EVENT
# Called when a virgin girl has penetrative sex for the first time.
# Receives: girl (Girl instance), position ("cowgirl" or "reverse_cowgirl")
# ============================================================

# --- Virginity blood screen tint (subtle dark red flash) ---
image virgin_blood_tint = Solid("#8B0000", xsize=1920, ysize=1080)

transform _virgin_blood_tint:
    alpha 0.0
    linear 0.3 alpha 0.15
    pause 1.5
    linear 0.8 alpha 0.0

# --- One-shot impact transforms (single thrust, NO repeat) ---

# RCG butt: two slow deep thrusts, then hold at deepest
# Applied to butt_gap, butt_top, thigh_highs, panties, skirt
transform _vdg_impact_butt:
    yoffset 0
    ease 0.8 yoffset 60
    ease 0.8 yoffset 0
    easein 0.6 yoffset 60

# RCG body: same rhythm but less distance (body moves less than butt)
transform _vdg_impact_body:
    yoffset 0
    ease 0.8 yoffset 40
    ease 0.8 yoffset 0
    easein 0.6 yoffset 40

# RCG penis: two matching thrusts forward
transform _vdg_impact_penis:
    subpixel True
    anchor (0.5, 1.0)
    xpos 0.5
    ypos 1.0
    xoffset 0
    yoffset 156
    ease 0.8 yoffset 88
    ease 0.8 yoffset 156
    easein 0.6 yoffset 88

# Cowgirl: two slow descents (girl sits down deeper), then hold
# yoffset 30 = top, 160 = deep
transform _vcg_impact_slot:
    subpixel True
    anchor (0.5, 1.0)
    xalign StageCenter
    yalign 2.0
    yoffset 30
    ease 0.8 yoffset 160
    ease 0.8 yoffset 30
    easein 0.6 yoffset 160

label virgin_first_time(girl, position):

    $ debug_log("[DEBUG] virgin_first_time CALLED: girl=%s position=%s" % (girl.gid, position))

    python:
        _rec_active = getattr(store, "_recording_active", False)
        _is_cute = girl.has_trait("cute_sex")
        _is_hardcore = girl.has_trait("hardcore_sex")
        _is_lesbian = girl.has_trait("lesbian")
        _is_cheat = _is_on_cheat_path(girl)
        _cheat_path = getattr(girl, "_cheat_escalation_path", 0) if _is_cheat else 0
        _has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
        _is_loyal = girl.has_trait("loyal")
        _is_cum_slut = girl.has_trait("cum_slut")
        _is_exhibitionist = girl.has_trait("exhibitionist")
        _is_dating = girl.is_dating_player()

    # ==========================================================
    # 0. DIRECT SEX OPENING -- she accepted without going through tip
    # Plays when _virgin_direct_sex is set (high stats skipped the
    # virgin gate). Especially impactful when she hasn't done other
    # acts -- rewards the player for reaching this rare scenario.
    # ==========================================================
    python:
        _virgin_direct = getattr(store, "_virgin_direct_sex", False)
        store._virgin_direct_sex = False  # consume flag

    if _virgin_direct:
        python:
            _flags = getattr(girl, "intimacy_flags", set()) or set()
            _no_kiss = "kiss" not in _flags
            _no_touch = "touch" not in _flags
            _no_hj = "hj" not in _flags and "tj" not in _flags and "bj" not in _flags

            if _no_kiss and _no_touch and _no_hj:
                unlock_achievement("speedrun")

            # Tier 1: never kissed + never touched -- maximum impact
            if _no_kiss and _no_touch and _has_bf:
                if _is_hardcore:
                    _vd_pool = [
                        _("I've never kissed you. Never let you touch me. And I'm about to let you take my virginity before my own {hint}%(pl)s{/hint}. Fuck it. I want this."),

                        _("My {hint}%(pl)s{/hint} has been waiting for this for months... and I'm giving it to a man I've never even kissed. I don't care anymore. Take me."),

                    ]
                elif _is_cute:
                    _vd_pool = [
                        _("W-we've never even kissed... I've never let anyone touch me... and I'm giving my virginity to someone who isn't my {hint}%(pl)s{/hint}? What is happening to me..."),

                        _("I don't understand... we never held hands, never kissed... and now I'm about to lose my virginity to you instead of my {hint}%(pl)s{/hint}... my heart won't stop racing..."),

                    ]
                else:
                    _vd_pool = [
                        _("I can't believe this is happening... we never even kissed, and I'm about to give you something my {hint}%(pl)s{/hint} has been waiting for. I must be losing my mind."),

                        _("We skipped everything... the kissing, the touching, all of it... and here I am, about to lose my virginity to someone who isn't my {hint}%(pl)s{/hint}."),

                    ]
            elif _no_kiss and _no_touch:
                if _is_hardcore:
                    _vd_pool = [
                        _("We've never kissed. Never touched. And I'm about to let you inside me for the first time. No buildup. No foreplay. Just raw need."),
                        _("I don't need kisses. I don't need touching. I just need you to fuck me. Right now. Even if it's my first time."),
                    ]
                elif _is_cute:
                    _vd_pool = [
                        _("I c-can't believe I'm letting you do this... we've never even kissed... never held hands... and I'm so wet I can barely think..."),
                        _("We skipped everything... the hand-holding, the kissing, all of it... and my body is saying yes before my brain catches up..."),
                    ]
                else:
                    _vd_pool = [
                        _("I can't believe I'm letting you fuck me like this... we've never even kissed, but I'm so wet..."),
                        _("We never kissed, never touched... and I'm about to let you take my virginity. What is wrong with me?"),
                    ]
            # Tier 2: never kissed but has touched
            elif _no_kiss:
                _vd_pool = [
                    _("You haven't even kissed me yet... and I'm letting you be my first? This is insane..."),
                    _("I've never felt your lips on mine... but I'm about to feel you inside me for the first time. How did we get here?"),
                ]
            # Tier 3: has kissed but skipped everything else
            elif _no_hj and _no_touch:
                _vd_pool = [
                    _("All we've done is kiss... and now I'm giving you my virginity? We skipped so many steps..."),
                    _("From a kiss to... this? I've never done anything else with you, and I'm already about to lose my virginity..."),
                ]
            # Tier 4: has done some stuff -- still impressive but less extreme
            elif _has_bf:
                _vd_pool = [
                    _("I was saving this for my {hint}%(pl)s{/hint}... but I want you. I want YOU to be my first."),

                    _("My {hint}%(pl)s{/hint} thought %(pp)s'd be my first... %(pp)s was wrong. You are. Right now."),

                ]
            else:
                _vd_pool = [
                    _("I'm really doing this... giving you my virginity. No tip first, no easing in... just... you."),
                    _("I don't need to go slow. I don't need the tip first. I want all of you. Even if it's my first time."),
                ]

            if _is_lesbian and getattr(store, "_coercion_type", None) == "blackmail":
                _vd_pool = [
                    _("I can't believe this is happening... a man is about to take my virginity. Because I know what happens if I say no."),
                    _("My first time was supposed to be with a woman I love. Not a man who has videos of me."),
                ]
            elif _is_lesbian and getattr(store, "_coercion_type", None) == "financial":
                _vd_pool = [
                    _("I can't believe I'm doing this... selling my virginity to a man. For money."),
                    _("My first time was supposed to be with a woman I love. Not a man who paid for it."),
                ]
            elif _is_lesbian:
                _vd_pool = [
                    _("I can't believe a man is about to take my virginity... this was never supposed to happen."),
                    _("My first time was supposed to be with a woman I love. Not like this."),
                ]

        if _is_lesbian:
            $ set_scene_expression(girl, "scared")
        else:
            $ set_scene_expression(girl, "pleasure")
        $ Say_Line(girl, _format_partner_line(girl, _tl(renpy.random.choice(_vd_pool))))

    # ==========================================================
    # 1. OPENING -- nervous realisation (only when NOT direct sex)
    # Skipped for direct path: Section 0 already establishes
    # she knows it's her first time.
    # ==========================================================
    if not _virgin_direct:
        python:
            _vft_nervous = {
                "lesbian_blackmail": [
                    _("I can't believe a man is about to take my virginity... because of what you have on me."),
                    _("This is not how my first time was supposed to go... not with a man. Not like this."),
                    _("You know I'm a lesbian... you know I don't want this. But you also know I can't say no. Not with those recordings."),
                ],
                "lesbian_financial": [
                    _("I can't believe I'm about to lose my virginity to a man... for money."),
                    _("This is not how my first time was supposed to go... not with a man. Not for cash."),
                    _("You know I'm a lesbian... you know I don't want this. But the money... I need it."),
                ],
                "lesbian": [
                    _("I can't believe a man is about to take my virginity... this was never supposed to happen."),
                    _("This is not how my first time was supposed to go... not with a man. Not like this."),
                    _("You know I'm a lesbian... you know I don't want this. But somehow I can't say no."),
                ],
                "cute_sex": [
                    _("W-wait... go slow, okay? This is my first time..."),
                    _("I've never done this before... please be gentle with me."),
                    _("I'm really nervous... promise me you'll be careful?"),
                ],
                "hardcore_sex": [
                    _("This is my first time... but don't hold back."),
                    _("I've never done this, but... I don't want you to go easy on me."),
                    _("It's my first time. I'm scared, but I want it real."),
                ],
                "loyal": [
                    _("I was saving this... but I want it to be with you."),
                    _("I've never let anyone do this before... you're the first."),
                    _("I chose you for my first time. Don't make me regret it."),
                ],
                "camera_hater": [
                    _("This is my first time... and if you DARE record this, I'll never speak to you again."),
                    _("I'm a virgin... please don't film this. This is private."),
                ],
                "camera_lover": [
                    _("My first time... I actually want this on camera. Is that weird?"),
                    _("I've been saving this... and I want to remember every second. Film it."),
                ],
                "hate_cum": [
                    _("I'm a virgin... and please... please be clean about this."),
                    _("It's my first time... just promise me you'll be careful with... the mess."),
                ],
                "public_fetish": [
                    _("I'm losing my virginity... somewhere anyone could catch us. Oh god..."),
                    _("My first time... and the thrill of being caught is making it even more intense."),
                ],
                "_default": [
                    _("Wait... I should tell you... this is my first time."),
                    _("I've never done this before... be careful with me, okay?"),
                    _("I'm a virgin... I don't really know what to expect."),
                ],
            }
            _line = None
            _vft_matched_trait = None
            for _t in ("lesbian", "cute_sex", "hardcore_sex", "loyal", "camera_hater", "camera_lover", "hate_cum", "public_fetish"):
                if _t == "camera_lover" and not _rec_active:
                    continue
                if girl.has_trait(_t):
                    _lookup_key = _t
                    if _t == "lesbian":
                        _ct = getattr(store, "_coercion_type", None)
                        if _ct == "blackmail":
                            _lookup_key = "lesbian_blackmail"
                        elif _ct == "financial":
                            _lookup_key = "lesbian_financial"
                    _line = renpy.random.choice(_vft_nervous[_lookup_key])
                    _vft_matched_trait = _t
                    break
            if _line is None:
                _line = renpy.random.choice(_vft_nervous["_default"])

        if _is_lesbian:
            $ set_scene_expression(girl, "scared")
        else:
            $ set_scene_expression(girl, "nervous", blush="1")
        $ Say_Line(girl, _line)
        if _vft_matched_trait:
            $ girl.discover("discovered_trait_%s" % _vft_matched_trait)

    # ==========================================================
    # 2. PLAYER CHOICE -- gentle or push through
    # ==========================================================
    menu:
        "Go slow and be gentle":
            $ _virgin_approach = "gentle"
            $ Say_Player(_("I'll take it slow. Tell me if it hurts."))
            python:
                if _is_lesbian:
                    _line = renpy.random.choice([_("...At least you're not being rough about it. That doesn't make this right."), _("...Fine. Slowly then. Just get it over with.")])
                elif _is_cute:
                    _line = renpy.random.choice([_("Thank you... that means everything to me."), _("You're so sweet... okay, I'm ready."), _("I feel safe with you. Go ahead... slowly.")])
                elif _is_hardcore:
                    _line = renpy.random.choice([_("...Fine. But once I'm used to it, don't hold back."), _("Okay... but I won't need you to be gentle for long.")])
                else:
                    _line = renpy.random.choice([_("Thank you... okay. I trust you."), _("That makes me feel better. I'm ready."), _("Okay... just go slow at first.")])
            if _is_lesbian:
                $ set_scene_expression(girl, "sad")
            else:
                $ set_scene_expression(girl, "happy")
            $ Say_Line(girl, _line)

        "Don't worry, you'll get used to it":
            $ _virgin_approach = "push"
            $ Say_Player(_("Relax. You'll get used to it."))
            python:
                if _is_lesbian and getattr(store, "_coercion_type", None) == "blackmail":
                    _line = renpy.random.choice([_("Of course you wouldn't care enough to be gentle... you already don't care that I'm a lesbian."), _("You don't even care that this is my first time... why would you? You have the videos, that's all that matters to you.")])
                elif _is_lesbian and getattr(store, "_coercion_type", None) == "financial":
                    _line = renpy.random.choice([_("Of course you wouldn't care enough to be gentle... you already don't care that I'm a lesbian."), _("You don't even care that this is my first time... why would you? You're paying, so nothing else matters.")])
                elif _is_lesbian:
                    _line = renpy.random.choice([_("Of course you wouldn't care enough to be gentle... you already don't care that I'm a lesbian."), _("You don't even care that this is my first time... why would you? I'm just a conquest to you.")])
                elif _is_cute:
                    _line = renpy.random.choice([_("W-wait, that's too fast! Slow down!"), _("Ow! I said be careful!")])
                elif _is_hardcore:
                    _line = renpy.random.choice([_("Ngh... okay. I can take it."), _("It hurts, but... don't stop.")])
                else:
                    _line = renpy.random.choice([_("Ah! That... that stings a little..."), _("Ow... okay, okay... just give me a second.")])
            $ set_scene_expression(girl, "grimace")
            $ Say_Line(girl, _line)

    # ==========================================================
    # 3. CAMERA -- offer to record BEFORE penetration
    # ==========================================================
    if not getattr(store, "_recording_active", False):
        python:
            _cam_lover = girl.has_trait("camera_lover")
            _cam_hater = girl.has_trait("camera_hater")

        if _cam_lover:
            $ Say_Line(girl, _("Wait... are you recording this? You SHOULD be. My first time deserves to be on camera."))
            menu:
                "Record her first time":
                    python:
                        store._recording_active = True
                        store._recording_girl = girl
                        store._player_hand_disabled = renpy.random.choice(["left", "right"])
                        _pen = scene_type_is_penetration(position)
                        vid = {
                            "girl_gid": girl.gid,
                            "type": position,
                            "location": CurrentLocation,
                            "committed": girl.has_npc_partner(),
                            "consensual": True,
                            "special": "virginity",
                            "hd": Player.has_item("tekmix_camera"),
                            "snapshot": _make_vid_snapshot(girl),
                        }
                        if _pen:
                            vid["condom"] = bool(store.condom_active)
                        _tag_coercion_on_vid(vid)
                        store.Player.recorded_videos.append(vid)
                        renpy.show_screen("recording_overlay")
                    $ Say_Line(girl, renpy.random.choice([_("Yes! Get every second of this. My first time on camera..."), _("Good. I want to watch this later. Every single second.")]))
                    if girl.has_trait("camera_lover"):
                        $ girl.discover("discovered_trait_camera_lover")
                "Maybe later":
                    $ Say_Line(girl, _("Your loss... this was a once in a lifetime moment."))
        elif not _cam_hater:
            menu:
                "Record her first time":
                    $ _rec_ok = recording_consent_check(girl, position)
                    if _rec_ok["result"] == "accepted":
                        python:
                            if _is_cute:
                                _cam_line = renpy.random.choice([_("You want to film this?! I... I guess... since it's my first time..."), _("A video of my first time? That's so embarrassing... but okay.")])
                            elif _is_hardcore:
                                _cam_line = renpy.random.choice([_("Film it. I want proof of how good my first time was."), _("Go ahead. Record everything. I'm not shy.")])
                            elif _has_bf:
                                _cam_line = _format_partner_line(girl, renpy.random.choice([_("You want VIDEO of this?! If my {hint}%(pl)s{/hint} ever finds out... ugh, fine. Just don't show anyone."), _("A recording of me cheating AND losing my virginity? You're insane. ...Do it.")]))
                            else:
                                _cam_line = renpy.random.choice([_("You want to record my first time? ...Okay. But only because it's special."), _("A video? I... sure. I want to remember this too.")])
                        $ Say_Line(girl, _cam_line)
                        python:
                            store._recording_active = True
                            store._recording_girl = girl
                            store._recording_face_locked = False
                            store._player_hand_disabled = renpy.random.choice(["left", "right"])
                            _pen = scene_type_is_penetration(position)
                            vid = {
                                "girl_gid": girl.gid,
                                "type": position,
                                "location": CurrentLocation,
                                "committed": girl.has_npc_partner(),
                                "consensual": True,
                                "face_hidden": bool(getattr(store, "hiding_face", False)),
                                "special": "virginity",
                                "hd": Player.has_item("tekmix_camera"),
                                "snapshot": _make_vid_snapshot(girl),
                            }
                            if _pen:
                                vid["condom"] = bool(store.condom_active)
                            _tag_coercion_on_vid(vid)
                            store.Player.recorded_videos.append(vid)
                            renpy.show_screen("recording_overlay")
                    elif _rec_ok["result"] == "face_hidden_only":
                        # She agrees ONLY with her face out of the shot (same tier 2 as every other recording)
                        if position in ("cowgirl", "reverse_cowgirl", "laying_down"):
                            call _apply_hide_face(girl, position) from _call_hide_face_virgin_rec
                        $ set_scene_expression(girl, "uncomfortable")
                        $ Say_Line(girl, _pick_recording_line(girl, "face_hidden_accept"))
                        python:
                            store._recording_active = True
                            store._recording_girl = girl
                            store._recording_face_locked = True
                            store._player_hand_disabled = renpy.random.choice(["left", "right"])
                            _pen = scene_type_is_penetration(position)
                            vid = {
                                "girl_gid": girl.gid,
                                "type": position,
                                "location": CurrentLocation,
                                "committed": girl.has_npc_partner(),
                                "consensual": True,
                                "reluctant": True,
                                "face_hidden": True,
                                "special": "virginity",
                                "hd": Player.has_item("tekmix_camera"),
                                "snapshot": _make_vid_snapshot(girl),
                            }
                            if _pen:
                                vid["condom"] = bool(store.condom_active)
                            _tag_coercion_on_vid(vid)
                            store.Player.recorded_videos.append(vid)
                            renpy.show_screen("recording_overlay")
                            print("[VIRGIN] recording tier=face_hidden_only position=%s hiding_face=%s" % (position, getattr(store, "hiding_face", False)))
                    else:
                        python:
                            if _is_cute:
                                _cam_deny = renpy.random.choice([_("No! Please don't film this... this is too personal."), _("My first time is NOT going on camera. No way.")])
                            elif _has_bf:
                                _cam_deny = _format_partner_line(girl, renpy.random.choice([_("Are you INSANE? Film me losing my virginity to someone who isn't my {hint}%(pl)s{/hint}? Absolutely not."), _("No! If my {hint}%(pl)s{/hint} ever saw that... no. No recording.")]))
                            else:
                                _cam_deny = renpy.random.choice([_("No... this is too intimate for a camera."), _("I don't want my first time recorded. This is just for us.")])
                        $ Say_Line(girl, _cam_deny)
                "Keep going":
                    pass

    # ==========================================================
    # 4. PENETRATION BEGINS -- ApplySpeed(1)
    # Direct path: no "I want more than just the tip" (she was
    # taken directly, not via tip-first). Normal path: she went
    # through tip and is asking for more.
    # ==========================================================
    if not _virgin_direct:
        $ Say_Line(girl, _("I want more... more than just the tip."))

    python:
        _started_map = {"reverse_cowgirl": "rcg_started", "cowgirl": "cowgirl_started", "doggy": "doggy_started", "full_nelson": "fn_started", "laying_down": "laying_started"}
        _sv = _started_map.get(position)
        if _sv:
            setattr(store, _sv, True)
        if position == "laying_down":
            store._ld_had_pussy = True
            girl._ld_after_pussy = True
    if position == "cowgirl":
        call CG_PenisEnterAnim(girl) from _call_CG_PenisEnterAnim_vir
    call _cum_dispatch_apply_speed(girl, position, speed=1) from _call_vir_s1_as

    python:
        state = sprite_state.setdefault(girl.Id, {})
        state["mouth"] = "mouth_open_teeth"
        state["eyes"] = "eyes_squint_big"

    pause 1.5
    $ Say_Line(girl, renpy.random.choice([_("Oh my god, I can feel it... it's so big!"), _("I can feel it going in... oh god..."), _("It's... it's stretching me... I can feel everything...")]))

    if _is_lesbian and getattr(store, "_coercion_type", None) == "blackmail":
        $ set_scene_expression(girl, "grimace")
        $ Say_Line(girl, renpy.random.choice([_("I can feel a man inside me for the first time... this was never supposed to happen."), _("This is wrong... everything about this is wrong. But I know what you'll do if I stop."), _("A man... inside me... I never wanted this. You know I never wanted this.")]))
    elif _is_lesbian:
        $ set_scene_expression(girl, "grimace")
        $ Say_Line(girl, renpy.random.choice([_("I can feel a man inside me for the first time... this was never supposed to happen."), _("This is wrong... everything about this is wrong. But I don't have a choice."), _("A man... inside me... I never wanted this. You know I never wanted this.")]))
    elif _is_cute:
        $ set_scene_expression(girl, "grimace")
        $ Say_Line(girl, renpy.random.choice([_("Stop! Take it out, it's hurting!"), _("Wait, wait, wait! It hurts too much!"), _("Ow! Please, slow down... it really hurts!")]))
        $ Say_Player(_("Shh, it's okay... you'll get used to it. Just breathe."))
    elif _is_hardcore:
        $ set_scene_expression(girl, "pleasure")
        $ Say_Line(girl, renpy.random.choice([_("More. MORE! I need more, push it in!"), _("Don't stop now! Keep going deeper!"), _("Yes! I can feel it... give me all of it!")]))
    else:
        $ Say_Line(girl, renpy.random.choice([_("It hurts... but don't stop. Keep going."), _("I can take it... just go slow."), _("Ahhh... okay... okay, keep going.")]))

    # ==========================================================
    # 5. BLOOD EFFECT (optional, player toggle)
    # Shown at speed 1 -- blood appears at first penetration.
    # ==========================================================
    if store.virginity_blood and position != "laying_down":
        show virgin_blood_tint at _virgin_blood_tint zorder 11000
    if store.virginity_blood:
        python:
            if _is_lesbian:
                _blood_pool = [
                    _("...I'm bleeding. A man made me bleed."),
                    _("There's blood... this is really happening. A man is taking my virginity."),
                ]
            elif _is_cute:
                _blood_pool = [
                    _("Is that... am I bleeding?! Oh no..."),
                    _("There's blood... is that normal? Please tell me that's normal..."),
                    _("I'm bleeding... it hurts so much..."),
                ]
            elif _is_hardcore:
                _blood_pool = [
                    _("I'm bleeding... good. Now I know it was real."),
                    _("Blood... that means you really took it. All of it."),
                    _("There's blood... I don't care. Keep going."),
                ]
            else:
                _blood_pool = [
                    _("I think I'm bleeding a little... is that normal?"),
                    _("There's... blood. My first time really is gone, isn't it?"),
                    _("Oh... I'm bleeding. It really happened."),
                ]
        $ set_scene_expression(girl, "nervous" if not _is_lesbian else "scared")
        $ Say_Line(girl, _tl(renpy.random.choice(_blood_pool)))
        if _virgin_approach == "gentle":
            $ Say_Player(_("It's normal for the first time. It'll stop soon. Are you okay?"))
            if _is_lesbian:
                $ Say_Line(girl, _("Do I look okay to you?"))
            elif _is_cute:
                $ Say_Line(girl, renpy.random.choice([_("I... I think so. Just... hold me for a second."), _("Y-yeah... just don't move yet, please...")]))
            else:
                $ Say_Line(girl, renpy.random.choice([_("Yeah... I'm fine. Just surprised."), _("I'm okay. It stings, but I can take it.")]))
        else:
            $ Say_Player(_("It's normal. You'll be fine."))
            if _is_lesbian:
                $ Say_Line(girl, _("Of course you don't care."))
            elif _is_cute:
                $ Say_Line(girl, renpy.random.choice([_("Easy for you to say... you're not the one bleeding!"), _("It hurts! Can you at least slow down?!")]))
            else:
                $ Say_Line(girl, renpy.random.choice([_("...Fine. Just keep going."), _("I know... I just didn't expect it to actually bleed.")]))

    # ==========================================================
    # 6. FULL DEPTH -- ApplySpeed(2) + impact animation
    # ==========================================================
    call _cum_dispatch_apply_speed(girl, position, speed=2) from _call_vir_depth_as

    python:
        state["mouth"] = "mouth_sch"
        state["eyes"] = "eyes_squint_big"
        state["brows"] = "brows_surprised"

    pause 2.0

    # --- IMPACT: single thrust (one-shot, no repeat) ---
    python:
        state["mouth"] = "mouth_tongue" if _is_hardcore else "mouth_serious"
        state["eyes"] = "eyes_surprised" if _is_hardcore else "eyes_squint_big"
        state["brows"] = "brows_surprised"

    if position == "reverse_cowgirl":
        # Override body + butt layers + clothing + penis with two-thrust animation
        python:
            _slot_at = [rcg_slot_speed2]
            _vdg_off = _gsc(girl.gid, "slot_offset", None, "rcg")
            if _vdg_off:
                _slot_at.append(getattr(store, _vdg_off))
            _butt_at = _slot_at + [_vdg_impact_butt]

            # Body (layeredimage): less movement than butt
            _body_at = _slot_at + [_vdg_impact_body]
            _vdg_attrs = _build_rcg_attributes(girl)
            _vdg_img = "%s rcg %s" % (girl.gid, " ".join(_vdg_attrs))
            renpy.show(_vdg_img, tag=girl.gid, at_list=_body_at, zorder=9980)

            # Arms 2 standalone (follows body, not butt)
            if store.rcg_arms_pose == 2:
                _arms2_ls = "%s rcg_arms_ls_2" % girl.gid
                _arms2_img = _arms2_ls if girl.Over == "long_shirt" and renpy.has_image(_arms2_ls, exact=True) else "%s rcg_arms_2" % girl.gid
                renpy.show(_arms2_img, tag="rcg_arms2", at_list=_body_at, zorder=10050)

            # Butt gap
            renpy.show("%s rcg_butt_gap" % girl.gid, tag="rcg_butt_gap", at_list=_butt_at, zorder=9960)
            # Butt top
            _bt_img = {
                "butt_top_1": "%s rcg_butt_top_1" % girl.gid,
                "butt_top_2": "%s rcg_butt_top_2" % girl.gid,
                "butt_top_3": "%s rcg_butt_top_3" % girl.gid,
            }.get(store.rcg_butt_state)
            if _bt_img:
                renpy.show(_bt_img, tag="rcg_butt_top", at_list=_butt_at, zorder=10005)
            # Thigh highs
            if getattr(girl, "Shoes", None):
                renpy.show("%s rcg_thigh_highs" % girl.gid, tag="rcg_thigh_highs", at_list=_butt_at, zorder=9968)
            # Panties (if displaced)
            _pan_item = girl.Panties
            _pan_state = girl.clothes_state.get("panties", "full") if hasattr(girl, "clothes_state") else "full"
            if _pan_item:
                _pan_img = "%s rcg_panties_%s_%s" % (girl.gid, _pan_item, _pan_state)
                _pan_z = 9969 if _pan_state == "down" else 10006
                renpy.show(_pan_img, tag="rcg_panties", at_list=_butt_at, zorder=_pan_z)
                # Side bottom: follows butt movement (not penis)
                _pan_sb = "%s rcg_panties_%s_side_bottom" % (girl.gid, _pan_item)
                if _pan_state == "side" and renpy.has_image(_pan_sb):
                    renpy.show(_pan_sb, tag="rcg_panties_side_bottom", at_list=_butt_at, zorder=9965)
            # Skirt
            if girl.Legs:
                _skirt_state = girl.clothes_state.get("skirt", "full")
                _skirt_tag_name = "rcg_skirt_up" if _skirt_state == "up" else "rcg_skirt"
                renpy.show("%s %s" % (girl.gid, _skirt_tag_name), tag="rcg_skirt", at_list=_butt_at, zorder=10007)
            # Blush
            renpy.show("%s rcg_butt_blush" % girl.gid, tag="rcg_butt_blush", at_list=_butt_at, zorder=10008)

            # Grab hands (synced with butt)
            if store.rcg_grab:
                _hand_disabled = getattr(store, "_player_hand_disabled", None)
                _slap_hide = getattr(store, "_slap_hide_hand", None)
                _gb_left = "%s rcg_grab_butt_left" % girl.gid
                if renpy.has_image(_gb_left):
                    for _side in ("left", "right"):
                        _gb_img = "%s rcg_grab_butt_%s" % (girl.gid, _side)
                        _gb_tag = "rcg_grab_%s" % _side
                        if _hand_disabled != _side and _slap_hide != _side and renpy.has_image(_gb_img):
                            renpy.show(_gb_img, tag=_gb_tag, at_list=_butt_at, zorder=10050)
                        else:
                            renpy.hide(_gb_tag)
                else:
                    _gb_img = "%s rcg_grab_butt" % girl.gid
                    if renpy.has_image(_gb_img):
                        renpy.show(_gb_img, tag="rcg_grab_left", at_list=_butt_at, zorder=10050)
                    renpy.hide("rcg_grab_right")

            # Crop top (follows body movement)
            _crop_top_img = "%s rcg_crop_top" % girl.gid
            if renpy.has_image(_crop_top_img, exact=True):
                _vdg_attrs = _build_rcg_attributes(girl) if callable(_build_rcg_attributes) else ""
                if isinstance(_vdg_attrs, list):
                    _vdg_attrs = " ".join(_vdg_attrs)
                if "torso_chest_corset" in _vdg_attrs:
                    renpy.show(_crop_top_img, tag="rcg_crop_top", at_list=_body_at, zorder=10051)

            # Bikini top (same pattern)
            _bikini_top_img = "%s rcg_bikini_top" % girl.gid
            if renpy.has_image(_bikini_top_img, exact=True) and "torso_chest_bikini_top" in _vdg_attrs:
                renpy.show(_bikini_top_img, tag="rcg_bikini_top", at_list=_body_at, zorder=10051)

            # Penis: matching two-thrust forward
            _pen_at = [_vdg_impact_penis]
            _vdg_off = _gsc(girl.gid, "slot_offset", None, "rcg")
            if _vdg_off:
                _pen_at.append(getattr(store, _vdg_off))
            renpy.show("%s rcg_penis" % girl.gid, tag="rcg_penis", at_list=_pen_at, zorder=9970)
            if store.condom_active:
                renpy.show("rcg_condom", tag="rcg_condom", at_list=_pen_at, zorder=9970)

        # Wait for two thrusts (0.8 + 0.8 + 0.6 = 2.2s)
        pause 2.2
        # Screen shake on final impact
        with vpunch
        # Hold at deepest position -- she needs time to process
        $ Say_Line(girl, renpy.random.choice([_("Oh my god... it's so deep... wait... let me get used to this..."), _("It's all the way in... don't move... just... let me breathe..."), _("I can feel everything... just stay like that... let me adjust...")]))
        # Return to speed 2
        $ rcg_speed = 2
        call RCG_ApplySpeed(girl, 2) from _call_RCG_ApplySpeed_vir_post
    elif position == "cowgirl":
        # Override ALL cowgirl layers with two-descent one-shot
        python:
            store._cg_impact_active = True
            _tf = [_vcg_impact_slot]

            print("[VIR_CG] === VIRGINITY COWGIRL IMPACT START gid=%s ===" % girl.gid)
            print("[VIR_CG] Clothing: Chest=%s ChestUp=%s Over=%s Legs=%s Panties=%s" % (girl.Chest, girl.ChestUp, getattr(girl, "Over", None), girl.Legs, getattr(girl, "Panties", None)))
            print("[VIR_CG] PantiesState=%s" % girl.clothes_state.get("panties", "full"))

            # Main layeredimage (body + head + arms + clothing)
            attrs = _build_cowgirl_attributes(girl)
            img_name = "%s cowgirl" % girl.gid
            if attrs:
                img_name += " " + " ".join(attrs)
            print("[VIR_CG] LAYEREDIMAGE: img_name='%s' attrs=%s has_image=%s" % (img_name, attrs, renpy.has_image(img_name)))
            try:
                renpy.show(img_name, tag=girl.gid, at_list=_tf, zorder=9980)
                print("[VIR_CG] LAYEREDIMAGE: show OK")
            except Exception as _e:
                print("[VIR_CG] LAYEREDIMAGE: show FAILED: %s" % _e)

            # Legs bottom
            _lb_img = "%s cowgirl_legs_bottom" % girl.gid
            _lb_exists = renpy.has_image(_lb_img)
            print("[VIR_CG] LEGS_BOTTOM: img='%s' exists=%s" % (_lb_img, _lb_exists))
            if _lb_exists:
                renpy.show(_lb_img, tag="cowgirl_legs_bottom", at_list=_tf, zorder=9965)
                print("[VIR_CG] LEGS_BOTTOM: show OK")
            else:
                renpy.hide("cowgirl_legs_bottom")
                print("[VIR_CG] LEGS_BOTTOM: HIDDEN (no image)")

            # Skirt bottom
            _skirt_bottom_img = "%s cowgirl_skirt_bottom" % girl.gid
            _sb_show = girl.Legs and renpy.has_image(_skirt_bottom_img)
            print("[VIR_CG] SKIRT_BOTTOM: img='%s' Legs=%s has_image=%s showing=%s" % (_skirt_bottom_img, girl.Legs, renpy.has_image(_skirt_bottom_img), _sb_show))
            if _sb_show:
                renpy.show(_skirt_bottom_img, tag="cowgirl_skirt_bottom", at_list=_tf, zorder=9960)

            # Boobs + nipples
            _boob_img = "%s cowgirl_boobs_naked" % girl.gid
            _nip_img = "%s cowgirl_nipples" % girl.gid
            print("[VIR_CG] BOOBS: img='%s' exists=%s" % (_boob_img, renpy.has_image(_boob_img)))
            print("[VIR_CG] NIPPLES: img='%s' exists=%s" % (_nip_img, renpy.has_image(_nip_img)))
            if renpy.has_image(_boob_img):
                renpy.show(_boob_img, tag="cowgirl_boobs", at_list=_tf, zorder=9982)
            if renpy.has_image(_nip_img):
                renpy.show(_nip_img, tag="cowgirl_nipples", at_list=_tf, zorder=9983)

            # Corset (if present)
            _chest_item = girl.Chest
            if _chest_item == "corset":
                _chest_cfg = CLOTHING_REGISTRY.get(girl.gid, {}).get("corset", {})
                if "cowgirl" in _chest_cfg.get("poses", {}):
                    if not girl.ChestUp:
                        renpy.show("%s cowgirl_corset" % girl.gid, tag="cowgirl_corset", at_list=_tf, zorder=9985)
                        renpy.show("%s cowgirl_corset_up" % girl.gid, tag="cowgirl_corset_up", at_list=_tf, zorder=9984)
                    else:
                        renpy.show("%s cowgirl_corset_up" % girl.gid, tag="cowgirl_corset_up", at_list=_tf, zorder=9985)
            elif _chest_item and _chest_item != "corset":
                _ct_img = "%s cowgirl_%s" % (girl.gid, _chest_item)
                _ct_up_img = "%s cowgirl_%s_up" % (girl.gid, _chest_item)
                if not girl.ChestUp and renpy.has_image(_ct_img):
                    renpy.show(_ct_img, tag="cowgirl_chest_top", at_list=_tf, zorder=9985)
                elif girl.ChestUp and renpy.has_image(_ct_up_img):
                    renpy.show(_ct_up_img, tag="cowgirl_chest_top", at_list=_tf, zorder=9988)

            # Chest fixed layer (crop_top_fixed / shirt bottom)
            _chest_item = girl.Chest if hasattr(girl, "Chest") else None
            if _chest_item and _chest_item != "corset":
                _ct_fixed_img = "%s cowgirl_%s_fixed" % (girl.gid, _chest_item)
                if renpy.has_image(_ct_fixed_img):
                    _ct_fixed_z = 9984 if girl.gid == "ntw" else 9981
                    renpy.show(_ct_fixed_img, tag="cowgirl_chest_fixed", at_list=_tf, zorder=_ct_fixed_z)

            # Panties side bottom
            _pan_item = getattr(girl, "Panties", None)
            _pan_state = girl.clothes_state.get("panties", "full") if hasattr(girl, "clothes_state") else "full"
            if _pan_item and _pan_state in ("side", "down"):
                _psb = "%s cowgirl_bikini_panties_side_bottom" % girl.gid if _pan_item == "bikini_panties" else "%s cowgirl_panties_side_bottom" % girl.gid
                print("[VIR_CG] PANTIES_BOTTOM: img='%s' exists=%s" % (_psb, renpy.has_image(_psb)))
                if renpy.has_image(_psb):
                    renpy.show(_psb, tag="cowgirl_panties_side_bottom", at_list=_tf, zorder=9968)

            # Cum layers
            _tummy_img = "%s cowgirl_tummy_cum" % girl.gid
            print("[VIR_CG] TUMMY_CUM: img='%s' exists=%s" % (_tummy_img, renpy.has_image(_tummy_img)))
            if renpy.has_image(_tummy_img):
                renpy.show(_tummy_img, tag="cowgirl_tummy_cum", at_list=_tf, zorder=9988)

            # Guy
            _guy_img = "%s cowgirl_guy" % girl.gid
            print("[VIR_CG] GUY: img='%s' exists=%s" % (_guy_img, renpy.has_image(_guy_img)))
            if renpy.has_image(_guy_img):
                renpy.show(_guy_img, tag="cowgirl_guy", at_list=_tf, zorder=9970)

            # Guy squeeze
            if getattr(store, "cowgirl_guy_touch", None) == "grab_tits":
                for _side in ("left", "right"):
                    _sq = "%s cowgirl_guy_squeeze_%s" % (girl.gid, _side)
                    if renpy.has_image(_sq):
                        renpy.show(_sq, tag="cowgirl_guy_squeeze_%s" % _side, at_list=_tf, zorder=10050)

            print("[VIR_CG] === VIRGINITY COWGIRL IMPACT END ===")

        # Wait for two descents (0.8 + 0.8 + 0.6 = 2.2s)
        pause 2.2
        # Screen shake on final impact
        with vpunch
        # Hold -- she needs time to process
        $ Say_Line(girl, renpy.random.choice([_("Oh my god... it's so deep... wait... let me get used to this..."), _("It's all the way in... don't move... just... let me breathe..."), _("I can feel everything... just stay like that... let me adjust...")]))
        # Return to speed 2
        $ store._cg_impact_active = False
        $ cowgirl_speed = 2
        call COWGIRL_ApplySpeed(girl, 2) from _call_COWGIRL_ApplySpeed_vir_post
    elif position == "doggy":
        # Doggy impact: screen shake + hold at speed 2
        pause 1.5
        with vpunch
        $ Say_Line(girl, renpy.random.choice([_("Oh my god... it's so deep... wait... let me get used to this..."), _("It's all the way in... don't move... just... let me breathe..."), _("I can feel everything... just stay like that... let me adjust...")]))
        $ doggy_speed = 2
        call DG_ApplySpeed(girl, 2) from _call_DG_ApplySpeed_vir_post
    elif position == "full_nelson":
        pause 1.5
        with vpunch
        $ Say_Line(girl, renpy.random.choice([_("Oh my god... it's so deep... wait... let me get used to this..."), _("It's all the way in... don't move... just... let me breathe..."), _("I can feel everything... just stay like that... let me adjust...")]))
        $ fn_speed = 2
        call FN_ApplySpeed(girl, 2) from _call_FN_ApplySpeed_vir_post
    elif position == "laying_down":
        pause 1.5
        $ laying_speed = 0
        call LD_ApplySpeed(girl, 0) from _call_LD_ApplySpeed_vir_freeze
        python:
            _pen_z = _ld_pen_z()
            _pen_img = "tenny laying_penis"
            if store.condom_active:
                _ci = _condom_img_tag("ld_condom")
                _pw = Fixed(renpy.displayable(_pen_img), renpy.displayable(_ci), fit_first=True)
                renpy.show("ld_penis_combined", what=_pw, tag="ld_penis", at_list=[ld_penis_virgin_hold], zorder=_pen_z)
            else:
                renpy.show(_pen_img, tag="ld_penis", at_list=[ld_penis_virgin_hold], zorder=_pen_z)
            if store.virginity_blood:
                _bp_img = girl.gid + " laying_blood_penis"
                if renpy.has_image(_bp_img, exact=True):
                    renpy.show(_bp_img, tag="ld_blood_penis", at_list=[ld_penis_virgin_hold], zorder=_pen_z + 1)
                    store._ld_blood_active = True
        with vpunch
        $ Say_Line(girl, renpy.random.choice([_("Oh my god... it's so deep... wait... let me get used to this..."), _("It's all the way in... don't move... just... let me breathe..."), _("I can feel everything... just stay like that... let me adjust...")]))
        $ laying_speed = 2
        call LD_ApplySpeed(girl, 2) from _call_LD_ApplySpeed_vir_post
        python:
            _pen_z = _ld_pen_z()
            _pen_img = "tenny laying_penis"
            if store.condom_active:
                _ci = _condom_img_tag("ld_condom")
                _pw = Fixed(renpy.displayable(_pen_img), renpy.displayable(_ci), fit_first=True)
                renpy.show("ld_penis_combined", what=_pw, tag="ld_penis", at_list=[ld_penis_virgin_resume], zorder=_pen_z)
            else:
                renpy.show(_pen_img, tag="ld_penis", at_list=[ld_penis_virgin_resume], zorder=_pen_z)
            if store._ld_blood_active:
                _bp_img = girl.gid + " laying_blood_penis"
                renpy.show(_bp_img, tag="ld_blood_penis", at_list=[ld_penis_virgin_resume], zorder=_pen_z + 1)

    # ==========================================================
    # 7. VIRGINITY LOST -- flag + reactions
    # ==========================================================
    python:
        lose_virginity(girl, position=position)

        if _virgin_approach == "gentle":
            Change_Status(girl, "Love", renpy.random.randint(15, 25))
            Change_Status(girl, "Inbt", renpy.random.randint(5, 10))
        else:
            Change_Status(girl, "Love", renpy.random.randint(-10, -5))
            Change_Status(girl, "Obed", renpy.random.randint(10, 15))
            Change_Status(girl, "Inbt", renpy.random.randint(8, 15))

        _girl_lust_gain(girl, 20)

        if getattr(store, "_recording_active", False):
            unlock_achievement("directors_cut")

    # Virginity loss reaction (priority: cheat > loyal+bf > trait-specific > default)
    if _is_cheat and _cheat_path == 1:
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("Someone else took my virginity... and it wasn't %(po)s. I can never take this back."), _("My %(pl)s was supposed to be my first... but you... you took it. And I let you.")])))
    elif _is_cheat and _cheat_path == 2:
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("I was saving this to give %(po)s when I was ready... but you took it first. And I wanted you to."), _("%(Pp)s doesn't know I was a virgin... and now %(pp)s'll never get to be my first. You are.")])))
    elif _is_cheat and _cheat_path == 3:
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("I lost my virginity as revenge... but it felt too good to be just revenge."), _("I wanted to get back at %(po)s by giving this to someone else... and I don't regret it.")])))
    elif _is_loyal and _has_bf:
        $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([_("I was saving myself for %(po)s... and I gave it to you instead. What have I done..."), _("My %(pl)s was supposed to be my first... I loved %(po)s. But I chose you. I can't undo this."), _("I broke every promise I ever made to %(po)s... and the worst part is I don't regret it.")])))
    elif _is_cum_slut:
        $ Say_Line(girl, renpy.random.choice([_("Oh god... so THIS is what it feels like raw... I've been missing out my whole life..."), _("I can feel everything... every inch... I never want to go back to not knowing this."), _("My first time and I already know I'm addicted... I need more of this.")]))
        $ girl.discover("discovered_trait_cum_slut")
    elif _is_exhibitionist and store._crowd_level > 0:
        $ Say_Line(girl, renpy.random.choice([_("I just lost my virginity somewhere anyone could see... and that makes it even hotter."), _("My first time, in public... if anyone saw that... oh god, why does that excite me?"), _("I can't believe I did this here... anyone could have watched me lose my virginity...")]))
        $ girl.discover("discovered_trait_exhibitionist")
    elif _is_lesbian and getattr(store, "_coercion_type", None) == "blackmail":
        $ Say_Line(girl, renpy.random.choice([_("I lost my virginity to a man... because of a recording. Not because I wanted it. Never because I wanted it."), _("My first time... stolen by a man with a camera and no conscience. I'll never forgive you for this."), _("You used a video to take my virginity. I hope you're proud of yourself.")]))
    elif _is_lesbian and getattr(store, "_coercion_type", None) == "financial":
        $ Say_Line(girl, renpy.random.choice([_("I sold my virginity to a man... I can never take that back."), _("A man paid to take my first time. What does that make me..."), _("My virginity had a price tag. And I let you pay it.")]))
    elif _is_lesbian:
        $ Say_Line(girl, renpy.random.choice([_("A man took my virginity. I'm still a lesbian. That hasn't changed. But I can never undo what just happened."), _("I let a man be my first... I don't even know what I'm feeling right now."), _("My first time was with a man... my body wanted it even if my head is screaming.")]))
    elif _is_dating:
        $ Say_Line(girl, renpy.random.choice([_("I gave my first time to my boyfriend... that feels right. I'm glad it was you."), _("You're my first... and I wanted it to be you. I don't regret anything."), _("I chose you for this. My boyfriend, my first... it's perfect.")]))
    else:
        $ Say_Line(girl, renpy.random.choice([_("I can't believe I just did that... my first time. It's gone."), _("So that's what it feels like... I'm not a virgin anymore."), _("You were my first... I'll never forget this.")]))

    if position == "laying_down" and store.virginity_blood:
        $ store._virgin_blood_postscene = True

    # ==========================================================
    # 8. AFTERMATH -- resume to normal sex
    # ==========================================================
    if _is_lesbian and getattr(store, "_coercion_type", None) in ("blackmail", "financial"):
        $ Say_Line(girl, renpy.random.choice([_("...Just do what you have to do. The sooner this is over, the sooner I can forget it happened."), _("...I don't want to talk. Just move. Get it over with."), _("...You got what you wanted. A lesbian's virginity. Happy? Just finish.")]))
    elif _is_lesbian:
        $ Say_Line(girl, renpy.random.choice([_("...I can't believe I let this happen. Just... keep going. Don't make it weird."), _("...My body is responding to a man. I hate that. But don't stop."), _("...This doesn't change who I am. It doesn't. Just... move.")]))
    elif _is_hardcore:
        $ Say_Line(girl, renpy.random.choice([_("Move. I felt it... Hard now!"), _("Don't just sit there! Fuck me! For real this time!"), _("I felt everything. Now stop being gentle and MOVE.")]))
    elif _is_cute:
        $ Say_Line(girl, renpy.random.choice([_("It still hurts... but... it's getting good..."), _("Don't stop... the pain is turning into something else..."), _("It's weird... it hurt so much but now I... I don't want you to stop.")]))

    # Speed already at 2 from post-impact ApplySpeed, just return
    $ print("[VIRGIN] virgin_first_time RETURNING to caller. position=%s exhausted=%s force_end=%s deny_kick=%s" % (position, getattr(store, "_player_exhausted", False), getattr(store, "_scene_force_end", False), getattr(store, "_deny_kick", False)))
    return
