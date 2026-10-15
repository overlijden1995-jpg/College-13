# ============================================================
# SLEEPOVER SYSTEM
# Sleep together when it's Night and player is in a girl's room
# or a girl is in the player's room.
# ============================================================

init python:

    def _sleepover_history_level(girl):
        """Return 0-3 based on sexual/intimate history with the player."""
        sa = getattr(girl, "Sex_acts", {})
        total_sex = girl_act_counts(girl)[0]   # "sex" + "anal" scenes; positions are preferences, not acts
        total_oral = sum(sa.get(k, 0) for k in ("bj", "hj", "tj"))
        kissed = sa.get("kiss", 0)

        _t = SEX_HISTORY_THRESHOLDS
        if total_sex >= _t["sleepover_very_intimate_sex"]:
            return 3   # very intimate
        if total_sex >= _t["sleepover_intimate_sex"] or total_oral >= _t["sleepover_intimate_oral"]:
            return 2   # had sex or lots of oral
        if total_oral >= 1 or kissed >= 3:
            return 1   # some intimacy
        return 0       # barely anything

    def _sleepover_can_happen(girl):
        """Check if sleepover conditions are met (Evening or Night)."""
        if TimeIndex < NIGHT_INDEX - 1:
            return False
        loc = CurrentLocation
        her_room = GIRL_ROOMS.get(girl.gid, "")
        if loc == "room" and girl.loc == "room":
            return True   # girl is in player's room
        if loc == her_room and girl.loc == her_room:
            return True   # player is in her room
        return False

    def _sleepover_eligible_girls():
        """Return all girls that pass sleepover conditions AND minimum Love check."""
        result = []
        for g in ALL_GIRLS:
            if not _sleepover_can_happen(g):
                continue
            _hist = _sleepover_history_level(g)
            _bonus = [0, 50, 150, 250][min(_hist, 3)]
            _eff = g.Love + _bonus
            if _eff >= 300:
                result.append(g)
        return result

    def _sleepover_pair_compatible(g1, g2):
        """Check if two girls can sleep together with the player.
        Returns (compatible, reason_string)."""
        like_1to2 = g1.get_like_for(g2.gid)
        like_2to1 = g2.get_like_for(g1.gid)
        min_like = min(like_1to2, like_2to1)

        j1_ok = getattr(g1, "Jealousy", 0) < 600 or g1.has_trait("polyamorous") or is_harem_exempt(g1, g2)
        j2_ok = getattr(g2, "Jealousy", 0) < 600 or g2.has_trait("polyamorous") or is_harem_exempt(g2, g1)

        if min_like < 300:
            _low = g1 if like_1to2 < like_2to1 else g2
            return (False, _tl(_("%s doesn't like %s enough")) % (_low.Name, g2.Name if _low == g1 else g1.Name))
        if not j1_ok:
            return (False, _tl(_("%s is too jealous right now")) % g1.Name)
        if not j2_ok:
            return (False, _tl(_("%s is too jealous right now")) % g2.Name)
        return (True, "")

# ============================================================
# PERMANENT SLEEP ARRANGEMENT — "Ask her to sleep in your room"
# ============================================================
# Girl with _sleeps_in_player_room = True auto-moves to "room"
# every Night via update_all_girls_locations_for_time hook.

init python:

    def _sleep_arrange_check(girl):
        """Check if girl would accept a permanent sleep arrangement.
        Returns (accepted, reason_key)."""
        # A married girl sleeps at home, in her own bed (her nights with him are her story's to give: the
        # stepmom's step 3 visits). Never a permanent arrangement, whatever her stats.
        if girl.has_trait("married"):
            return (False, "married")

        if girl.is_dating_player():
            if girl.Love >= 200:
                return (True, "dating")
            return (False, "dating_low_love")

        _hist = _sleepover_history_level(girl)
        _bonus = [0, 50, 150, 250][min(_hist, 3)]
        _eff = girl.Love + _bonus

        if _eff < 400:
            return (False, "low_love")

        if hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            _t = int(girl.Temptation)
            _cheat_ok = girl.has_trait("cheater") or _t >= 4 or girl.Obed >= 500
            if not _cheat_ok:
                return (False, "has_partner")

        if girl.has_trait("lesbian") and girl.Obed < 500:
            return (False, "lesbian")

        return (True, "ok")

    def _sleep_arrange_can_tonight(girl):
        """Check if a girl with the arrangement can actually come tonight."""
        if girl_away_reason(girl):
            return False
        if hasattr(girl, "has_temp_status") and (girl.has_temp_status("angry") or girl.has_temp_status("sad")):
            return False
        if getattr(girl, "_giving_birth", False):
            return False
        return True

label _ask_sleep_arrangement(girl):
    python:
        _sa_ok, _sa_reason = _sleep_arrange_check(girl)

    if _sa_ok:
        $ set_scene_expression(girl, "happy")
        if girl.is_dating_player():
            $ Say_Line(girl, renpy.random.choice([
                _("Of course! I'd love that."),
                _("You don't even have to ask. I'll be there."),
                _("Finally! I was hoping you'd ask."),
            ]))
        elif hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
                _("That's risky... but okay. I'll sneak in when %(pp)s is not around."),
                _("If %(pp)s finds out, we're both dead. But... yeah, I'll come."),
            ])))
        else:
            $ Say_Line(girl, renpy.random.choice([
                _("Sure, I don't mind. Your room is comfy anyway."),
                _("Okay... but don't get any ideas. Or do. Whatever."),
                _("Alright. I'll start coming over at night."),
            ]))
        $ girl._sleeps_in_player_room = True
        $ set_scene_expression(girl, "normal")
        $ print("[SLEEP_ARRANGE] %s accepted permanent sleep arrangement" % girl.gid)
    else:
        if _sa_reason == "low_love":
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, renpy.random.choice([
                _("We're not that close yet. Maybe someday."),
                _("I appreciate the offer, but... not yet."),
            ]))
        elif _sa_reason == "married":
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, renpy.random.choice([
                _("I'm married. I sleep at home, in my own bed. Don't ask me that again."),
                _("Every night? I have a husband and a house. The answer is no."),
            ]))
        elif _sa_reason == "has_partner":
            $ set_scene_expression(girl, "worried")
            $ Say_Line(girl, _format_partner_line(girl, renpy.random.choice([
                _("I can't do that. %(Pp)s would notice if I'm gone every night."),
                _("That's way too risky. %(Pp)s would find out."),
            ])))
        elif _sa_reason == "lesbian":
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, renpy.random.choice([
                _("Sleep in a guy's room every night? No thanks."),
                _("I don't think that's a good idea."),
            ]))
        elif _sa_reason == "dating_low_love":
            $ set_scene_expression(girl, "uncomfortable")
            $ Say_Line(girl, renpy.random.choice([
                _("I'm not ready for that yet. Give me some time."),
                _("Let's take things slower, okay?"),
            ]))
        else:
            $ set_scene_expression(girl, "serious")
            $ Say_Line(girl, _("I don't think so."))
        $ set_scene_expression(girl, "normal")
        $ print("[SLEEP_ARRANGE] %s refused (%s)" % (girl.gid, _sa_reason))
    return

label _cancel_sleep_arrangement(girl):
    $ set_scene_expression(girl, "serious")
    $ Say_Line(girl, renpy.random.choice([
        _("Oh... okay. I'll go back to my room then."),
        _("If that's what you want. Fine."),
        _("Alright, I'll stop coming over."),
    ]))
    $ girl._sleeps_in_player_room = False
    $ set_scene_expression(girl, "normal")
    $ print("[SLEEP_ARRANGE] %s cancelled permanent sleep arrangement" % girl.gid)
    return

# ============================================================
# SLEEPOVER OFFER — called from location_menu
# ============================================================

label sleepover_offer(girl):

    if TimeIndex < NIGHT_INDEX - 1:
        $ print("[SLEEPOVER] sleepover_offer called too early (TimeIndex=%d), aborting" % TimeIndex)
        return

    # A married girl of a story (her husband is a FamilyContact: girl_husband) only turns a night into
    # a sleepover when he is AWAY on a trip (plan_shion_agency F3): any other night she is home before
    # he wakes, whatever her step. Her line, then the normal night goes on.
    python:
        _so_husband = girl_husband(girl) if callable(globals().get("girl_husband", None)) else None
        _so_husband_home = _so_husband is not None and not (callable(globals().get("story_husband_on_trip", None)) and story_husband_on_trip(girl))
    if _so_husband_home:
        $ print("[SLEEPOVER] %s declines the whole night: her husband is not on a trip" % girl.gid)
        $ set_scene_expression(girl, "normal", pose="standing")
        $ Say_Line(girl, rod_pick_line(girl, "sleepover_husband_home"))
        return

    $ _so_in_her_room = (CurrentLocation == GIRL_ROOMS.get(girl.gid, ""))

    # ----- NPC PARTNER IN THE ROOM: immediate block -----
    if _so_in_her_room:
        python:
            _so_npc = get_npc_partner_for(girl) if (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()) else None
            _so_npc_here = _so_npc and getattr(_so_npc, "loc", None) == CurrentLocation
        if _so_npc_here:
            $ Say_Line(girl, _tl(_("%s is here, are you crazy? We'll see each other tomorrow.")) % _so_npc.Name)
            $ Narration(_("You can't sleep here with her partner in the room."))
            $ navigate_to("campus", None)
            call Set_Scene(entry=True) from _call_Set_Scene_so_npc_block
            return

    $ _so_love = girl.Love
    $ _so_obed = girl.Obed
    $ _so_inbt = girl.Inbt
    $ _so_lust = girl.Lust
    $ _so_hist = _sleepover_history_level(girl)
    # Sexual history lowers thresholds: +0/+50/+150/+250 for hist 0/1/2/3
    $ _so_hist_bonus = [0, 50, 150, 250][min(_so_hist, 3)]
    $ _so_eff_love = _so_love + _so_hist_bonus
    $ _so_in_player_room = (CurrentLocation == "room")
    $ _so_dating = hasattr(girl, "is_dating_player") and girl.is_dating_player()
    $ _so_has_bf = hasattr(girl, "has_npc_partner") and girl.has_npc_partner()
    $ _so_player_has_gf = False

    # Check if player is dating someone ELSE (skip if harem-exempt)
    python:
        if not is_player_harem_exempt(girl):
            for _og in ALL_GIRLS:
                if _og.gid != girl.gid and hasattr(_og, "is_dating_player") and _og.is_dating_player():
                    _so_player_has_gf = True
                    break

    # ----- LOW STATUS: just says goodnight -----
    if _so_eff_love < 300:

        if _so_in_her_room:
            $ Say_Line(girl, _tl(_("It's getting late... you should probably head back to your room.")))
            "You say goodnight and leave."
            $ navigate_to("campus", None)
            call Set_Scene(entry=True) from _call_Set_Scene_so_leave_low
        else:
            $ Say_Line(girl, _tl(_("I should get going. Goodnight, [Player.Name].")))
            "She waves and heads out."
            $ girl.loc = girl_home_loc(girl)

        return

    # ----- MEDIUM STATUS: player can ask -----
    if _so_eff_love < 600:

        if _so_in_her_room:
            $ Say_Line(girl, _tl(_("Well, it's getting pretty late...")))

            menu:
                "Can I crash here tonight?":
                    jump .ask_stay_her_room
                "You're right. Goodnight.":
                    $ Say_Line(girl, _tl(_("Goodnight, [Player.Name].")))
                    $ navigate_to("campus", None)
                    call Set_Scene(entry=True) from _call_Set_Scene_so_leave_med_her
                    return

        else:
            $ Say_Line(girl, _tl(_("I should head back to my room...")))

            menu:
                "Why don't you stay here tonight?":
                    jump .ask_stay_player_room
                "Okay, goodnight.":
                    $ Say_Line(girl, _tl(_("Goodnight!")))
                    $ girl.loc = girl_home_loc(girl)
                    return

    # ----- HIGH STATUS (600+): she suggests -----
    else:

        # --- She has a BF: she brings it up naturally, doesn't suggest ---
        if _so_has_bf:
            if _so_in_her_room:
                if _so_hist >= 2:
                    $ Say_Line(girl, _tl(_("It's late... I'd ask you to stay, but my %s would kill me.")) % girl.partner_label())
                else:
                    $ Say_Line(girl, _tl(_("It's getting late. You should probably go... my %s wouldn't like you staying over.")) % girl.partner_label())

                menu:
                    "We've done way worse together. This is just sleeping." if _so_hist >= 2:
                        if _so_eff_love >= 400 or _so_obed >= 300:
                            $ Say_Line(girl, _tl(_("...You have a point. Fine. But JUST sleeping.")))
                            jump .accept_sleepover
                        else:
                            $ Say_Line(girl, _tl(_("That's... that doesn't make it better!")))
                            jump .refuse_and_leave

                    "It's just sleeping. Nothing wrong with that." if _so_hist >= 1 and _so_hist < 2:
                        if _so_eff_love >= 450 or _so_obed >= 350:
                            $ Say_Line(girl, _tl(_("I guess... okay. But nothing weird.")))
                            jump .accept_sleepover
                        else:
                            $ Say_Line(girl, _tl(_("I still don't think it's a good idea.")))
                            jump .refuse_and_leave

                    "You're right. Goodnight.":
                        $ Say_Line(girl, _tl(_("Thanks for understanding. Goodnight.")))
                        $ Change_Status(girl, "Love", 5)
                        $ navigate_to("campus", None)
                        call Set_Scene(entry=True) from _call_Set_Scene_so_leave_high_bf_her
                        return

            else:
                if _so_hist >= 2:
                    $ Say_Line(girl, _tl(_("I should go... I mean, I'd stay, but my %s would lose it.")) % girl.partner_label())
                else:
                    $ Say_Line(girl, _tl(_("It's late. I need to go back... my %s wouldn't be okay with me sleeping here.")) % girl.partner_label())

                menu:
                    "We've done way worse together. This is just sleeping." if _so_hist >= 2:
                        if _so_eff_love >= 400 or _so_obed >= 300:
                            $ Say_Line(girl, _tl(_("...You have a point. Fine. But JUST sleeping.")))
                            jump .accept_sleepover
                        else:
                            $ Say_Line(girl, _tl(_("That's... that doesn't make it better!")))
                            jump .refuse_and_leave

                    "It's just sleeping. Nothing wrong with that." if _so_hist >= 1 and _so_hist < 2:
                        if _so_eff_love >= 450 or _so_obed >= 350:
                            $ Say_Line(girl, _tl(_("I guess... okay. But nothing weird.")))
                            jump .accept_sleepover
                        else:
                            $ Say_Line(girl, _tl(_("I still don't think it's a good idea.")))
                            jump .refuse_and_leave

                    "You're right. Goodnight.":
                        $ Say_Line(girl, _tl(_("Goodnight, [Player.Name].")))
                        $ Change_Status(girl, "Love", 5)
                        $ girl.loc = girl_home_loc(girl)
                        return

        # --- No BF: she suggests freely ---
        else:
            if _so_in_her_room:
                if _so_hist >= 2:
                    $ Say_Line(girl, _tl(_("It's late... you could just stay here tonight, you know.")))
                else:
                    $ Say_Line(girl, _tl(_("It's getting late. Do you... want to stay over?")))

                menu:
                    "I'd love that.":
                        if _so_player_has_gf and not _so_dating:
                            jump .player_gf_concern
                        jump .accept_sleepover
                    "I should head back.":
                        $ Say_Line(girl, _tl(_("Oh... okay. Goodnight then.")))
                        $ Change_Status(girl, "Love", -5)
                        $ navigate_to("campus", None)
                        call Set_Scene(entry=True) from _call_Set_Scene_so_leave_high_her
                        return

            else:
                if _so_hist >= 2:
                    $ Say_Line(girl, _tl(_("I don't really feel like walking back... can I just sleep here?")))
                else:
                    $ Say_Line(girl, _tl(_("It's so late... would it be weird if I stayed?")))

                menu:
                    "Of course you can stay.":
                        if _so_player_has_gf and not _so_dating:
                            jump .player_gf_concern
                        jump .accept_sleepover
                    "It's probably best if you go.":
                        $ Say_Line(girl, _tl(_("Right... goodnight, [Player.Name].")))
                        $ Change_Status(girl, "Love", -5)
                        $ girl.loc = girl_home_loc(girl)
                        return

    # ---- PLAYER ASKS TO STAY (her room, medium status) ----
    label .ask_stay_her_room:

        # Boyfriend concern — she brings it up naturally
        if _so_has_bf:
            if _so_hist >= 2:
                $ Say_Line(girl, _tl(_("I mean... my %s would freak out. But we've done worse, so...")) % girl.partner_label())
                if _so_eff_love >= 400 or _so_obed >= 300:
                    $ Say_Line(girl, _tl(_("...Fine. But JUST sleeping.")))
                    jump .accept_sleepover
                else:
                    $ Say_Line(girl, _tl(_("No, I really can't. Sorry.")))
                    jump .refuse_and_leave
            elif _so_hist >= 1:
                $ Say_Line(girl, _tl(_("My %s wouldn't like that at all...")) % girl.partner_label())
                if _so_eff_love >= 450 or _so_obed >= 350:
                    $ Say_Line(girl, _tl(_("But... I guess it's just sleeping. Okay.")))
                    jump .accept_sleepover
                else:
                    $ Say_Line(girl, _tl(_("I don't think that's a good idea.")))
                    jump .refuse_and_leave
            else:
                $ Say_Line(girl, _tl(_("I have a %s... I really can't let you stay. Sorry.")) % girl.partner_label())
                jump .refuse_and_leave

        # Player's girlfriend concern
        if _so_player_has_gf and not _so_dating:
            jump .player_gf_concern

        if _so_eff_love >= 450 or _so_obed >= 200:
            $ Say_Line(girl, _tl(_("I... sure. But just sleeping, okay?")))
            jump .accept_sleepover
        else:
            $ Say_Line(girl, _tl(_("I don't think that's a good idea...")))
            "She doesn't seem comfortable with the idea."
            $ navigate_to("campus", None)
            call Set_Scene(entry=True) from _call_Set_Scene_so_reject_her
            return

    # ---- PLAYER ASKS HER TO STAY (player room, medium status) ----
    label .ask_stay_player_room:

        # Boyfriend concern — she brings it up naturally
        if _so_has_bf:
            if _so_hist >= 2:
                $ Say_Line(girl, _tl(_("My %s would lose it... but honestly, we've done worse.")) % girl.partner_label())
                if _so_eff_love >= 400 or _so_obed >= 300:
                    $ Say_Line(girl, _tl(_("Okay, fine. But just sleeping.")))
                    jump .accept_sleepover
                else:
                    $ Say_Line(girl, _tl(_("No... I shouldn't. Goodnight.")))
                    jump .refuse_and_leave
            elif _so_hist >= 1:
                $ Say_Line(girl, _tl(_("I have a %s, [Player.Name]... sleeping here is a bad look.")) % girl.partner_label())
                if _so_eff_love >= 450 or _so_obed >= 350:
                    $ Say_Line(girl, _tl(_("...But it IS just sleeping. Fine.")))
                    jump .accept_sleepover
                else:
                    $ Say_Line(girl, _tl(_("I should go. Goodnight.")))
                    jump .refuse_and_leave
            else:
                $ Say_Line(girl, _tl(_("I can't stay here... I have a %s. Sorry.")) % girl.partner_label())
                jump .refuse_and_leave

        # Player's girlfriend concern
        if _so_player_has_gf and not _so_dating:
            jump .player_gf_concern

        if _so_eff_love >= 450 or _so_obed >= 400:
            $ Say_Line(girl, _tl(_("Okay... but don't get any ideas.")))
            jump .accept_sleepover
        else:
            $ Say_Line(girl, _tl(_("I... I shouldn't. Goodnight.")))
            $ girl.loc = girl_home_loc(girl)
            return

    # ============================================================
    # PLAYER'S GIRLFRIEND CONCERN MINI-EVENT
    # ============================================================
    label .player_gf_concern:

        $ Say_Line(girl, _tl(_("Aren't you dating someone? She wouldn't like this...")))

        if _so_hist >= 2:
            menu:
                "We've already done much worse together. This is innocent.":
                    if _so_eff_love >= 350:
                        $ Say_Line(girl, _tl(_("Hah... I guess you're right. Okay, just sleeping though.")))
                        jump .accept_sleepover
                    else:
                        $ Say_Line(girl, _tl(_("Still... I'd feel weird about it.")))
                        jump .refuse_and_leave

                "You're right, bad idea.":
                    $ Say_Line(girl, _tl(_("Probably for the best.")))
                    jump .refuse_and_leave

        elif _so_hist >= 1:
            menu:
                "She doesn't need to know. It's just sleeping.":
                    if _so_eff_love >= 400 and _so_obed >= 250:
                        $ Say_Line(girl, _tl(_("...Fine. But if she finds out, I had nothing to do with it.")))
                        jump .accept_sleepover
                    else:
                        $ Say_Line(girl, _tl(_("No, I don't want to be part of that.")))
                        jump .refuse_and_leave

                "Yeah, you're right.":
                    $ Say_Line(girl, _tl(_("Goodnight.")))
                    jump .refuse_and_leave

        else:
            $ Say_Line(girl, _tl(_("Yeah no, I'm not doing that. Goodnight.")))
            jump .refuse_and_leave

    # ============================================================
    # REFUSE AND LEAVE
    # ============================================================
    label .refuse_and_leave:

        if _so_in_her_room:
            "You say goodnight and head out."
            $ navigate_to("campus", None)
            call Set_Scene(entry=True) from _call_Set_Scene_so_refuse
        else:
            "She heads back to her room."
            $ girl.loc = girl_home_loc(girl)

        return

    # ============================================================
    # ACCEPT SLEEPOVER — both sleep, wake up together
    # ============================================================
    label .accept_sleepover:

        # NPC partner awareness: evening warnings on consecutive nights AWAY from home. In her own room she IS
        # home: the streak is broken and nobody comes "looking for her" (no warning, no morning visit).
        if _so_in_her_room:
            $ girl._sleepover_consecutive = 0
            $ print("[SLEEPOVER] %s sleeps in her own room: partner awareness skipped, nights-away streak reset" % girl.gid)
        elif hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            call _sleepover_partner_check(girl) from _call_so_partner_check
            if _return:
                jump .refuse_and_leave

        $ girl.RegisterAction("slept_together")
        $ girl._slept_with_player_tonight = True
        $ girl._pre_sleep_lust = girl.Lust
        $ _so_times_slept = girl.GetActionCount("slept_together")
        $ Change_Status(girl, "Love", 10)
        if CurrentLocation == "room":
            $ consecutive_room_sleeps += 1

        if _so_in_her_room:
            "You settle in. [girl.Name] gets comfortable on the other side of the bed."
        else:
            "She grabs a pillow and settles in. You both lie down."

        if _so_love >= 600 and _so_hist >= 1:
            $ Say_Line(girl, _tl(_("Goodnight, [Player.Name].")))
            "She scoots a little closer before closing her eyes."
        else:
            $ Say_Line(girl, _tl(_("Goodnight.")))
            "She turns to her side, pulling the blanket over herself."

        # ----- ACTUAL SLEEP: advance to next day -----
        $ LastPresentGirls = [g for g in ALL_GIRLS if g.loc == CurrentLocation]
        $ Party = []
        $ Player.recharge_energy()

        # ONE central new-day routine (system_time.rpy: start_next_day_manually -> _per_day_cleanup). The
        # hand-copied block that lived here never ran the pregnancy tick, the suspicion decay, the schedulers...
        $ start_next_day_manually()

        # She went into labor overnight (pregnancy tick of the rollover): she is gone when he wakes up, and the
        # birth event in label Wait tells the rest. No wake-up scene, no morning BJ.
        if girl_is_away(girl):
            scene black
            with fade
            pause 0.8
            "You wake up alone. Her side of the bed is already cold."
            if _so_in_her_room:
                # he cannot stay alone in her room (same rule as every other branch of this label)
                $ navigate_to("campus", None)
            jump .wake_up_run_day

        # Keep this girl in the same room as the player for the morning
        $ girl.loc = CurrentLocation

        # Her pregnancy discovery is due this morning (pregnancy tick of the rollover). That event OPENS with him
        # waking up to an empty, still warm bed (_disc_slept branch of _pregnancy_discovery), so it replaces
        # the wake-up scene and the morning BJ: label Wait plays it.
        if getattr(store, "_pregnancy_discovery_pending", None) == girl.gid:
            $ print("[SLEEPOVER] %s: pregnancy discovery due this morning, wake-up scene skipped" % girl.gid)
            scene black
            with fade
            pause 0.8
            jump .wake_up_run_day

        # Move NPC partner away so they don't appear in the morning scene
        python:
            _so_npc_wake = get_npc_partner_for(girl) if (hasattr(girl, "has_npc_partner") and girl.has_npc_partner()) else None
            if _so_npc_wake and getattr(_so_npc_wake, "loc", None) == CurrentLocation:
                _so_npc_wake.loc = "campus"

        scene black
        with fade
        pause 0.8

        # ----- MORNING: wake up together -----
        jump .wake_up_together

    # ============================================================
    # WAKE UP TOGETHER
    # ============================================================
    label .wake_up_together:

        # ── Morning BJ Event Check ──
        # A femdom veteran who can wakes him by sitting on his face instead (morning_bj.rpy, MORNING_WAKE_VARIANTS):
        # the variant is picked once, then judged, rolled and played as that one.
        python:
            print("[MORNING_BJ] wake_up_together check: girl=%s" % girl.Name)
            _mbj_variant = _morning_wake_variant(girl)
            _mbj_elig = _morning_bj_eligible(girl, _mbj_variant)
            if _mbj_elig:
                _mbj_roll_result = _morning_bj_roll(girl, _mbj_variant)
                print("[MORNING_BJ] roll for %s (%s): %s" % (girl.Name, _mbj_variant, _mbj_roll_result))
                _mbj_ok = _mbj_roll_result
            else:
                _mbj_ok = False
                print("[MORNING_BJ] %s not eligible (%s), skipping roll" % (girl.Name, _mbj_variant))
        if _mbj_ok:
            if _mbj_variant == "face_sit":
                call morning_face_sit_solo(girl) from _call_morning_face_sit_solo
            else:
                call morning_bj_solo(girl) from _call_morning_bj_solo
            jump .wake_up_solo_done

        # Refresh scene — show the room with the girl
        call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_so_wakeup

        "You open your eyes. Morning sunlight filters in."

        # ----- VERY HIGH STATUS + LOTS OF HISTORY -----
        if _so_love >= 800 and _so_hist >= 3:

            $ _wakeup_roll = renpy.random.randint(1, 3)

            if _wakeup_roll == 1:
                # She suggests fun
                $ Say_Line(girl, _tl(_("Mmm... good morning.")))
                "She stretches lazily, her body pressing against yours."
                $ Say_Line(girl, _tl(_("You know... we're already in bed. Why not make the most of it?")))

                menu:
                    "I like the way you think.":
                        $ Say_Line(girl, _tl(_("I thought you might~")))
                        $ Change_Status(girl, "Love", 10)
                        $ Change_Status(girl, "Lust", 15, max_val=100)
                        $ _scene_exit_flags_reset()
                        call sex_menu(girl, CurrentLocation, TimeIndex) from _call_sex_menu_so_morning

                    "As tempting as that is... maybe later.":
                        $ Say_Line(girl, _tl(_("Your loss~ ...just kidding. Good morning, [Player.Name].")))
                        $ Change_Status(girl, "Love", 5)

            elif _wakeup_roll == 2:
                # Cuddly morning
                $ Say_Line(girl, _tl(_("Hey... I slept really well.")))
                "She leans her head on your shoulder."
                $ Say_Line(girl, _tl(_("Can we just stay like this for a bit?")))

                menu:
                    "Of course.":
                        "You lie there together for a while. It feels nice."
                        $ Change_Status(girl, "Love", 15)

                    "We should get moving.":
                        $ Say_Line(girl, _tl(_("Mm, I guess you're right...")))
                        $ Change_Status(girl, "Love", 3)

            else:
                # Playful morning
                $ Say_Line(girl, _tl(_("Morning, sleepyhead~")))
                "She's already awake, watching you with a smile."

                menu:
                    "Good morning, beautiful.":
                        $ Say_Line(girl, _tl(_("Smooth talker.")))
                        "She blushes and looks away, smiling."
                        $ Change_Status(girl, "Love", 10)

                    "How long have you been staring at me?":
                        $ Say_Line(girl, _tl(_("I wasn't staring! ...Okay, maybe a little.")))
                        $ Change_Status(girl, "Love", 8)

        # ----- HIGH STATUS (600-799) -----
        elif _so_love >= 600:

            $ Say_Line(girl, _tl(_("Good morning, [Player.Name].")))
            "She smiles softly at you."

            menu:
                "Morning. Sleep well?":
                    $ Say_Line(girl, _tl(_("Mhm. Better than usual, actually.")))
                    $ Change_Status(girl, "Love", 8)

                "You look cute when you just woke up.":
                    $ Say_Line(girl, _tl(_("S-shut up... I look like a mess.")))
                    "She tries to fix her hair, but she's smiling."
                    $ Change_Status(girl, "Love", 12)

                "We should do this more often.":
                    if _so_hist >= 2:
                        $ Say_Line(girl, _tl(_("I wouldn't mind that at all.")))
                    else:
                        $ Say_Line(girl, _tl(_("Maybe... yeah. Maybe we should.")))
                    $ Change_Status(girl, "Love", 10)

        # ----- MEDIUM STATUS (300-599) -----
        elif _so_love >= 300:

            $ Say_Line(girl, _tl(_("Oh... morning.")))
            "She looks a bit awkward but not uncomfortable."

            menu:
                "Morning. Thanks for letting me stay." if _so_in_her_room:
                    $ Say_Line(girl, _tl(_("It was... nice, actually. Don't make it weird.")))
                    $ Change_Status(girl, "Love", 5)

                "Morning. Thanks for staying." if _so_in_player_room:
                    $ Say_Line(girl, _tl(_("Yeah... it was okay, I guess.")))
                    $ Change_Status(girl, "Love", 5)

                "Sleep well?":
                    $ Say_Line(girl, _tl(_("Surprisingly, yeah.")))
                    $ Change_Status(girl, "Love", 5)

                "You know, you talk in your sleep.":
                    $ Say_Line(girl, _tl(_("I do NOT! ...Do I?")))
                    $ Change_Status(girl, "Love", 3)
                    $ Change_Status(girl, "Obed", 3)

        # ----- LOW STATUS (shouldn't normally reach here, but safety) -----
        else:

            $ Say_Line(girl, _tl(_("Huh?! What... oh. Right. We... slept here.")))
            "She looks around, disoriented."
            $ Say_Line(girl, _tl(_("This is so weird... please don't tell anyone.")))

            menu:
                "Your secret is safe with me.":
                    $ Say_Line(girl, _tl(_("...Thanks.")))
                    $ Change_Status(girl, "Love", 3)

                "Relax, it's no big deal.":
                    $ Say_Line(girl, _tl(_("Easy for you to say...")))
                    $ Change_Status(girl, "Obed", 3)

    label .wake_up_solo_done:

        # NPC partner morning visit: after 3+ consecutive nights, the partner shows up
        if getattr(girl, "_sleepover_consecutive", 0) >= 3 and hasattr(girl, "has_npc_partner") and girl.has_npc_partner():
            call _sleepover_npc_morning_visit(girl) from _call_snmv_solo
            if _return:
                # Confrontation happened, girl already left via roster_girl_leaves. Drop her from the night's
                # LastPresentGirls too, or Girl_TimeChange_Handler (in Wait) treats her as still here.
                python:
                    if girl in LastPresentGirls:
                        LastPresentGirls.remove(girl)
                    print("[SLEEPOVER] %s confronted by her partner this morning, dropped from LastPresentGirls (loc=%s)" % (girl.gid, girl.loc))
                jump .wake_up_run_day

        "You both get ready for the day."

        # Move sleepover girl to her scheduled morning location BEFORE Wait.
        # Girl_TimeChange_Handler keeps Love >= 700 girls in the room ("I'll
        # stay here"), trapping the player in an infinite sleep loop.
        python:
            _so_dest = get_scheduled_location_for(girl, Day, TimeIndex)
            girl.loc = _so_dest
            if girl in LastPresentGirls:
                LastPresentGirls.remove(girl)
            hide_girl_sprite(girl)
            print("[SLEEPOVER] %s morning departure -> %s" % (girl.gid, _so_dest))

        if _so_in_her_room:
            "You leave [girl.Name]'s room."
            $ navigate_to("campus", None)

    label .wake_up_run_day hide:

        # Call Wait for generic per-slot logic
        call Wait from _call_Wait_sleepover

        # Refresh the scene
        call Set_Scene(entry=True) from _call_Set_Scene_so_morning

        return

# ============================================================
# MULTI-GIRL SLEEPOVER — when 2+ girls are eligible
# ============================================================

init python:

    _SO_DISMISS_LINES = [
        _("Oh... okay. Goodnight then."),
        _("I guess I'll head back to my room..."),
        _("Fine. See you tomorrow."),
    ]

    _SO_DISMISS_CHOSEN_OTHER = [
        _("So you'd rather sleep with her than me? ...Fine."),
        _("Of course you pick her. Whatever. Goodnight."),
        _("I see how it is. Have a good night."),
    ]

    _SO_DISMISS_ALL_LINES = [
        _("You're kicking us all out? Wow, okay."),
        _("Seriously? Fine. Come on, girls. We know where we're not wanted."),
        _("Well that's rude. Goodnight, I guess."),
    ]

    _SO_DUO_ACCEPT_LINES = [
        _("Wait, both of us? ...This could be interesting."),
        _("A sleepover with the three of us? I'm in."),
        _("Together? I mean... okay, sure. Why not."),
        _("All three of us in one bed? Sounds cozy~"),
        _("Sure, I could use the company tonight."),
        _("This is going to be fun. Let's do it."),
    ]

    _SO_DUO_WAKE_FRIENDLY = [
        _("That was actually really nice. We should do this again."),
        _("I slept so well with you two. This was fun."),
        _("Good morning, you two~"),
    ]

    _SO_DUO_WAKE_TENSE = [
        _("...Did she have to take up so much of the bed?"),
        _("I barely slept. Someone kept hogging the blanket."),
        _("Morning. Can we NOT do this again?"),
    ]

label sleepover_multi(eligible_girls):

    python:
        _sm_girls = eligible_girls
        _sm_count = len(_sm_girls)
        _sm_pairs = []
        if _sm_count >= 2:
            for _i in range(_sm_count):
                for _j in range(_i + 1, _sm_count):
                    _compat, _reason = _sleepover_pair_compatible(_sm_girls[_i], _sm_girls[_j])
                    if _compat:
                        _sm_pairs.append((_sm_girls[_i], _sm_girls[_j]))
        print("[SLEEPOVER_MULTI] %d eligible, %d compatible pairs" % (_sm_count, len(_sm_pairs)))

    $ Narration(_("Multiple girls are here for the night. You can't all share one bed."))

    # Build menu dynamically
    python:
        _sm_menu_items = []
        for _sg in _sm_girls:
            _sm_menu_items.append((_tl(_("Sleep with %s")) % _sg.Name, "solo", _sg, None))
        for _sp in _sm_pairs:
            _sm_menu_items.append((_tl(_("Sleep with %s and %s")) % (_sp[0].Name, _sp[1].Name), "duo", _sp[0], _sp[1]))
        _sm_menu_items.append((_("Send everyone to their rooms"), "dismiss", None, None))

    # Use a fixed menu since Ren'Py menus must be static — dispatch via index
    $ _sm_choice = renpy.display_menu([(_item[0], _idx) for _idx, _item in enumerate(_sm_menu_items)])

    python:
        _sm_selected = _sm_menu_items[_sm_choice]
        _sm_action = _sm_selected[1]
        _sm_girl1 = _sm_selected[2]
        _sm_girl2 = _sm_selected[3]

    if _sm_action == "dismiss":
        jump .dismiss_all

    if _sm_action == "solo":
        jump .pick_solo

    if _sm_action == "duo":
        jump .pick_duo

    return

    # ── DISMISS ALL ──────────────────────────────────
    label .dismiss_all:

        $ _dm_speaker = renpy.random.choice(_sm_girls)
        $ set_scene_expression(_dm_speaker, "sad")
        $ Say_Line(_dm_speaker, renpy.random.choice(_SO_DISMISS_ALL_LINES))

        python:
            for _dg in _sm_girls:
                Change_Status(_dg, "Love", -10)
                Change_Status(_dg, "Obed", 5)
                _dg.loc = girl_home_loc(_dg)
                print("[SLEEPOVER_MULTI] dismissed %s: Love -10, Obed +5" % _dg.gid)

        $ Narration(_("They all leave, looking disappointed."))

        call do_sleep from _call_do_sleep_dismiss_all
        return

    # ── PICK SOLO ────────────────────────────────────
    label .pick_solo:

        python:
            for _sg in _sm_girls:
                if _sg.gid != _sm_girl1.gid:
                    set_scene_expression(_sg, "uncomfortable")
                    Say_Line(_sg, renpy.random.choice(_SO_DISMISS_CHOSEN_OTHER))
                    Change_Status(_sg, "Love", -5)
                    if hasattr(_sg, "is_dating_player") and _sg.is_dating_player():
                        Change_Status(_sg, "Jealousy", 15, show_popup=False)
                    _sg.loc = girl_home_loc(_sg)
                    print("[SLEEPOVER_MULTI] %s sent away: Love -5, Jealousy +15" % _sg.gid)

        $ _day_before_sleepover = Day
        call sleepover_offer(_sm_girl1) from _call_sleepover_offer_multi_solo
        if Day == _day_before_sleepover and CurrentLocation == "room":
            call do_sleep from _call_do_sleep_multi_solo_fallback
        return

    # ── PICK DUO ─────────────────────────────────────
    label .pick_duo:

        # Dismiss girls not in the duo
        python:
            _duo_gids = {_sm_girl1.gid, _sm_girl2.gid}
            for _sg in _sm_girls:
                if _sg.gid not in _duo_gids:
                    set_scene_expression(_sg, "uncomfortable")
                    Say_Line(_sg, renpy.random.choice(_SO_DISMISS_CHOSEN_OTHER))
                    Change_Status(_sg, "Love", -5)
                    if hasattr(_sg, "is_dating_player") and _sg.is_dating_player():
                        Change_Status(_sg, "Jealousy", 15, show_popup=False)
                    _sg.loc = girl_home_loc(_sg)

        # Duo reaction
        python:
            _duo_lines = list(_SO_DUO_ACCEPT_LINES)
            renpy.random.shuffle(_duo_lines)
            _duo_line1 = _duo_lines[0]
            _duo_line2 = _duo_lines[1]
        $ set_scene_expression(_sm_girl1, "surprised")
        $ Say_Line(_sm_girl1, _duo_line1)
        $ set_scene_expression(_sm_girl2, "happy")
        $ Say_Line(_sm_girl2, _duo_line2)

        jump .accept_sleepover_duo

    # ── DUO ACCEPT & SLEEP ──────────────────────────
    label .accept_sleepover_duo:

        # NPC partner awareness: evening warnings on consecutive nights (either girl)
        $ store._so_duo_abort = False
        if hasattr(_sm_girl1, "has_npc_partner") and _sm_girl1.has_npc_partner():
            call _sleepover_partner_check(_sm_girl1) from _call_so_pc_duo1
            if _return:
                $ store._so_duo_abort = True
        if not store._so_duo_abort and hasattr(_sm_girl2, "has_npc_partner") and _sm_girl2.has_npc_partner():
            call _sleepover_partner_check(_sm_girl2) from _call_so_pc_duo2
            if _return:
                $ store._so_duo_abort = True
        if store._so_duo_abort:
            "With that, the sleepover is off for tonight."
            python:
                for _sg in [_sm_girl1, _sm_girl2]:
                    _sg.loc = girl_home_loc(_sg)
                    hide_girl_sprite(_sg)
            return

        python:
            _sm_girl1.RegisterAction("slept_together")
            _sm_girl1._slept_with_player_tonight = True
            _sm_girl1._pre_sleep_lust = _sm_girl1.Lust
            Change_Status(_sm_girl1, "Love", 10)
            _sm_girl2.RegisterAction("slept_together")
            _sm_girl2._slept_with_player_tonight = True
            _sm_girl2._pre_sleep_lust = _sm_girl2.Lust
            Change_Status(_sm_girl2, "Love", 10)

        $ Narration(_("[_sm_girl1.Name] takes one side, [_sm_girl2.Name] takes the other. You settle in between them."))

        python:
            _duo_like = min(_sm_girl1.get_like_for(_sm_girl2.gid), _sm_girl2.get_like_for(_sm_girl1.gid))
        if _duo_like >= 500:
            $ Say_Line(_sm_girl1, _tl(_("This is actually kinda nice.")))
            $ Say_Line(_sm_girl2, _tl(_("Goodnight, you two.")))
        else:
            $ Say_Line(_sm_girl1, _tl(_("Don't hog the blanket.")))
            $ Say_Line(_sm_girl2, _tl(_("...Goodnight.")))

        # ----- ACTUAL SLEEP: advance to next day -----
        $ LastPresentGirls = [g for g in ALL_GIRLS if g.loc == CurrentLocation]
        $ Party = []
        $ Player.recharge_energy()

        # ONE central new-day routine (system_time.rpy: start_next_day_manually -> _per_day_cleanup). The
        # hand-copied block that lived here never ran the pregnancy tick, the suspicion decay, the schedulers...
        $ start_next_day_manually()

        # One of them went into labor overnight: she is gone, and the two-girl morning scene is skipped
        # (the birth event in label Wait tells the rest).
        if girl_is_away(_sm_girl1) or girl_is_away(_sm_girl2):
            python:
                for _dg in [_sm_girl1, _sm_girl2]:
                    if not girl_is_away(_dg):
                        _dg.loc = CurrentLocation
            scene black
            with fade
            pause 0.8
            if girl_is_away(_sm_girl1) and girl_is_away(_sm_girl2):
                "You wake up alone. The bed is already cold."
            else:
                "You wake up to find one side of the bed empty and already cold."
            jump .wake_up_duo_run_day

        # Keep both girls in the room for morning
        $ _sm_girl1.loc = CurrentLocation
        $ _sm_girl2.loc = CurrentLocation

        # One of them has her pregnancy discovery due this morning: that event opens with him waking up to an
        # empty bed (_pregnancy_discovery), so it replaces the two-girl morning scene. label Wait plays it.
        if getattr(store, "_pregnancy_discovery_pending", None) in (_sm_girl1.gid, _sm_girl2.gid):
            $ print("[SLEEPOVER] duo: pregnancy discovery due this morning (%s), wake-up scene skipped" % store._pregnancy_discovery_pending)
            scene black
            with fade
            pause 0.8
            jump .wake_up_duo_run_day

        # Move NPC partners away
        python:
            for _dg in [_sm_girl1, _sm_girl2]:
                _so_npc_w = get_npc_partner_for(_dg) if (hasattr(_dg, "has_npc_partner") and _dg.has_npc_partner()) else None
                if _so_npc_w and getattr(_so_npc_w, "loc", None) == CurrentLocation:
                    _so_npc_w.loc = "campus"

        scene black
        with fade
        pause 0.8

        jump .wake_up_duo

    # ── DUO WAKE UP ─────────────────────────────────
    label .wake_up_duo:

        # ── Morning BJ Event Check (Duo) ──
        python:
            print("[MORNING_BJ] wake_up_duo check: girl1=%s girl2=%s" % (_sm_girl1.Name, _sm_girl2.Name))
            _mbj_bj, _mbj_wit = _morning_bj_pick_duo(_sm_girl1, _sm_girl2)
            print("[MORNING_BJ] pick_duo result: bj=%s wit=%s" % (getattr(_mbj_bj, "Name", None), getattr(_mbj_wit, "Name", None)))
            if _mbj_bj is not None:
                _mbj_roll_result = _morning_bj_roll(_mbj_bj)
                print("[MORNING_BJ] roll for %s: %s" % (_mbj_bj.Name, _mbj_roll_result))
                _mbj_duo_ok = _mbj_roll_result
            else:
                _mbj_duo_ok = False
                print("[MORNING_BJ] no eligible girl, skipping roll")
        if _mbj_duo_ok:
            call morning_bj_duo(_mbj_bj, _mbj_wit) from _call_morning_bj_duo
            jump .wake_up_duo_done

        call Set_Scene(entry=False, quiet=True) from _call_Set_Scene_duo_wakeup

        $ Narration(_("You open your eyes. [_sm_girl1.Name] is on one side, [_sm_girl2.Name] on the other."))

        python:
            _duo_like_wake = min(_sm_girl1.get_like_for(_sm_girl2.gid), _sm_girl2.get_like_for(_sm_girl1.gid))

        if _duo_like_wake >= 500:
            $ Say_Line(_sm_girl1, renpy.random.choice(_SO_DUO_WAKE_FRIENDLY))
            $ set_scene_expression(_sm_girl2, "happy")
            $ Say_Line(_sm_girl2, _tl(_("Best sleep I've had in a while.")))
            $ Change_Status(_sm_girl1, "Love", 8)
            $ Change_Status(_sm_girl2, "Love", 8)
            python:
                _sm_girl1.add_like_for(_sm_girl2.gid, 5)
                _sm_girl2.add_like_for(_sm_girl1.gid, 5)
        else:
            $ Say_Line(_sm_girl1, renpy.random.choice(_SO_DUO_WAKE_TENSE))
            $ set_scene_expression(_sm_girl2, "uncomfortable")
            $ Say_Line(_sm_girl2, _tl(_("Yeah... it was... cozy.")))
            $ Change_Status(_sm_girl1, "Love", 3)
            $ Change_Status(_sm_girl2, "Love", 3)

    label .wake_up_duo_done:

        # NPC partner morning visit for duo (process each girl that qualifies)
        python:
            _duo_mv_confronted = False
            _duo_mv_girls = [_dg for _dg in [_sm_girl1, _sm_girl2]
                             if getattr(_dg, "_sleepover_consecutive", 0) >= 3
                             and hasattr(_dg, "has_npc_partner") and _dg.has_npc_partner()]
        if _duo_mv_girls:
            call _sleepover_npc_morning_visit(_duo_mv_girls[0]) from _call_snmv_duo1
            if _return:
                $ _duo_mv_confronted = True
            if len(_duo_mv_girls) > 1 and not _duo_mv_confronted:
                call _sleepover_npc_morning_visit(_duo_mv_girls[1]) from _call_snmv_duo2
                if _return:
                    $ _duo_mv_confronted = True
        if _duo_mv_confronted:
            # Move any non-confronted girl to her scheduled location (confronted girl
            # was already relocated by roster_girl_leaves inside the confrontation)
            python:
                for _dg in [_sm_girl1, _sm_girl2]:
                    # both leave the night's list: the confronted one is no longer here either
                    if _dg in LastPresentGirls:
                        LastPresentGirls.remove(_dg)
                    if _dg.loc == store.CurrentLocation:
                        _dg_dest = get_scheduled_location_for(_dg, Day, TimeIndex)
                        _dg.loc = _dg_dest
                        hide_girl_sprite(_dg)
            jump .wake_up_duo_run_day

        $ Narration(_("You all get ready for the day."))

        # Move both girls to their scheduled morning location BEFORE Wait.
        # Same fix as solo: Girl_TimeChange_Handler keeps high-Love girls
        # in the room forever.
        python:
            _duo_in_girl_room = store.CurrentLocation in GIRL_ROOMS.values()
            for _dg in [_sm_girl1, _sm_girl2]:
                _dg_dest = get_scheduled_location_for(_dg, Day, TimeIndex)
                _dg.loc = _dg_dest
                if _dg in LastPresentGirls:
                    LastPresentGirls.remove(_dg)
                hide_girl_sprite(_dg)
                print("[SLEEPOVER] %s morning departure -> %s" % (_dg.gid, _dg_dest))

        if _duo_in_girl_room:
            "You leave the room."
            $ navigate_to("campus", None)

    label .wake_up_duo_run_day hide:

        call Wait from _call_Wait_sleepover_duo
        call Set_Scene(entry=True) from _call_Set_Scene_duo_morning

        return

# ============================================================
# SLEEPOVER NPC PARTNER AWARENESS — evening warnings
# ============================================================
#
# Called from .accept_sleepover / .accept_sleepover_duo BEFORE RegisterAction.
# Increments girl._sleepover_consecutive and shows progressive warnings.
# Returns True if the player sent her home (abort the sleepover).

label _sleepover_partner_check(girl):

    python:
        _so_pc_npc = get_npc_partner_for(girl)
        if _so_pc_npc and _ntr_active_discovered(girl):
            # he knows and lets it happen (NTR boundary): he doesn't wonder where she is, nobody comes looking
            print("[SLEEPOVER] %s partner check skipped: %s knows (NTR active + boundary discovered)" % (girl.gid, _so_pc_npc.name))
            _so_pc_npc = None
        if not _so_pc_npc:
            renpy.return_statement()
        girl._sleepover_consecutive = getattr(girl, "_sleepover_consecutive", 0) + 1
        _so_pc_consec = girl._sleepover_consecutive
        print("[SLEEPOVER] %s partner check: consecutive=%d (npc=%s)" % (girl.gid, _so_pc_consec, _so_pc_npc.name))

    if _so_pc_consec == 1:
        python:
            _so_pc_lines = [
                _("You know... my %(pl)s is going to wonder where I am tonight."),
                _("I hope %(pp)s doesn't text asking where I am..."),
            ]
            _so_pc_warn = _format_partner_line(girl, renpy.random.choice(_so_pc_lines))
        $ set_scene_expression(girl, "worried")
        $ Say_Line(girl, _so_pc_warn)
        return

    elif _so_pc_consec == 2:
        python:
            _so_pc_lines = [
                _("This is the second night in a row... my %(pl)s is definitely going to start asking questions."),
                _("If I keep sleeping here, %(pp)s is going to come looking for me."),
            ]
            _so_pc_warn = _format_partner_line(girl, renpy.random.choice(_so_pc_lines))
        $ set_scene_expression(girl, "uncomfortable")
        $ Say_Line(girl, _so_pc_warn)
        return

    else:
        # Night 3+: confirmation menu
        $ _so_pc_warn = _format_partner_line(girl, _("This will be three nights in a row... I'm sure my %(pl)s is going to show up looking for me tomorrow."))
        $ set_scene_expression(girl, "scared")
        $ Say_Line(girl, _so_pc_warn)

        menu:
            "Let her stay":
                $ _so_pc_stay = _format_partner_line(girl, _("...Okay. But if %(pp)s shows up, that's on you."))
                $ set_scene_expression(girl, "worried")
                $ Say_Line(girl, _so_pc_stay)
                return

            "Better if she goes home":
                $ _so_pc_bye = _format_partner_line(girl, _("Yeah... you're right. I should go home before %(pp)s gets suspicious."))
                $ set_scene_expression(girl, "uncomfortable")
                $ Say_Line(girl, _so_pc_bye)
                $ girl._sleepover_consecutive = 0
                return True


# ============================================================
# SLEEPOVER NPC PARTNER AWARENESS — morning visit
# ============================================================
#
# Called from .wake_up_solo_done / .wake_up_duo_done when
# girl._sleepover_consecutive >= 3 and she has an NPC partner.
# The NPC shows up at the door, player picks an excuse.
# Returns True if suspicion hit 100 and confrontation fired.

label _sleepover_npc_morning_visit(girl):

    python:
        _so_mv_npc = get_npc_partner_for(girl)
        if _so_mv_npc and _ntr_active_discovered(girl):
            print("[SLEEPOVER] NPC morning visit skipped: %s knows (NTR active + boundary discovered)" % _so_mv_npc.name)
            _so_mv_npc = None
        if not _so_mv_npc:
            girl._sleepover_consecutive = 0
            renpy.return_statement()
        _so_mv_npc_name = _so_mv_npc.name
        print("[SLEEPOVER] NPC morning visit: %s looking for %s (suspicion=%d)" % (_so_mv_npc_name, girl.gid, _so_mv_npc.suspicion))

    "There's a knock at the door. Before you can answer, it opens."

    $ _so_mv_npc.show_sprite(slot_right)

    python:
        _so_mv_enter = [
            _("I've been looking everywhere for you. What's going on? You haven't come home in days."),
            _("Where have you been?! I've been worried sick!"),
        ]
    $ Say_Line(_so_mv_npc, renpy.random.choice(_so_mv_enter))

    $ set_scene_expression(girl, "scared")
    $ _so_mv_excuse = 0

    menu:
        "We have an exam this week, been studying a lot":
            $ _so_mv_excuse = 1
            $ Say_Line(_so_mv_npc, _tl(_("Oh... alright, that makes sense. Just let me know next time, okay?")))
            $ Change_NPC_Status(_so_mv_npc, "suspicion", 15)
            $ _so_mv_npc.change_love(10)
            $ Change_Status(girl, "Love", -10)

        "She says my bed is more comfortable than hers":
            $ _so_mv_excuse = 2
            $ Say_Line(_so_mv_npc, _tl(_("More comfortable...? That's your explanation?")))
            $ Change_NPC_Status(_so_mv_npc, "suspicion", 40)
            $ Change_Status(girl, "Love", 5)
            $ Change_Status(girl, "Obed", 10)

        "We're not sleeping, we've been staying up all night":
            $ _so_mv_excuse = 3
            $ Say_Line(_so_mv_npc, _tl(_("Staying up all night?! What the hell does that even mean?!")))
            $ Change_NPC_Status(_so_mv_npc, "suspicion", 80)
            $ Change_Status(girl, "Obed", 10)
            $ Change_Status(girl, "Inbt", 10)
            $ Change_NPC_Status(_so_mv_npc, "friendship_with_player", -50)

    # Confrontation check: if suspicion hit 100, the NPC confronts her immediately
    if _so_mv_npc.suspicion >= 100:
        $ print("[SLEEPOVER] %s suspicion=%d, triggering confrontation" % (_so_mv_npc_name, _so_mv_npc.suspicion))
        call npc_suspicion_confrontation(_so_mv_npc) from _call_so_npc_confrontation
        $ girl._sleepover_consecutive = 0
        return True

    # No confrontation: NPC leaves normally
    if _so_mv_excuse == 1:
        "[_so_mv_npc_name] nods and heads out."
    elif _so_mv_excuse == 2:
        "[_so_mv_npc_name] gives you a long look before leaving."
    elif _so_mv_excuse == 3:
        "[_so_mv_npc_name] slams the door on the way out."
    $ _so_mv_npc.hide_sprite()
    # he came looking for her and left without her
    $ unlock_achievement("finders_keepers")

    # Girl reaction after NPC leaves
    if _so_mv_excuse == 1:
        $ _so_mv_react = _format_partner_line(girl, _("I don't love being your study alibi... but at least %(pp)s bought it."))
        $ set_scene_expression(girl, "uncomfortable")
        $ Say_Line(girl, _so_mv_react)

    elif _so_mv_excuse == 2:
        $ _so_mv_react = _format_partner_line(girl, _("Well, it's not exactly a lie... I just hope %(pp)s doesn't think too hard about it."))
        $ set_scene_expression(girl, "uncomfortable")
        $ Say_Line(girl, _so_mv_react)

    elif _so_mv_excuse == 3:
        $ _so_mv_react = _format_partner_line(girl, _("Are you insane?! Did you see %(poss)s face?! %(Pp)s looked ready to kill you!"))
        $ set_scene_expression(girl, "angry")
        $ Say_Line(girl, _so_mv_react)

    $ girl._sleepover_consecutive = 0
    return
