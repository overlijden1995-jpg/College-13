# ============================================================
# family_grades.rpy... his stepmother watches his grades (docs/plan_shion.md, Fase 4: the antagonist stepmother)
#
# WHO: the woman of his family whose GIRLS_CONFIG "role" is in FAMILY_GUARDIAN_ROLES (Shion, "stepmom") and who has
#   lines here (FAMILY_GRADE_TEXTS, her gid or "role:<role>"). None: his grades only go to grade_history.
# HIS GRADE: every exam grade goes through exam_record_grade (exam.rpy): taken, skipped (F) or missed (F). It calls
#   family_on_exam_grade: the bad-grade streak (D / F count, A / B reset it, C keeps it) and her news, a text she
#   sends from the Evening of the exam day when no girlfriend of his and not she herself is with him (label Wait
#   step 4c, label _family_grade_news), then his father's text (DAD_GRADE_TEXTS).
# THE LADDER (FAMILY_LADDER, by the streak): 1 = she takes money (FAMILY_CONFISCATE) and freezes his Friday
#   allowance (FAMILY_ALLOWANCE_FREEZE); 2+ = same, plus a text demanding he study. With a girlfriend, ANY bad
#   grade is her fault: he breaks up with her by text, the words she dictates (player_breakup_apply, via "text",
#   reason "stepmom"). He can refuse: the punishment of the streak plus the money, and a turn point.
# HER GIRLFRIEND TALK: while he is dating, a morning text every FAMILY_GF_TEXT_EVERY days ("that girl").
# AFTER HER TURN (femdom stage FAMILY_LADDER_STOP_STAGE, femdom_turn.rpy): no ladder, no girlfriend talk; she lies
#   to his father for him ("s3_bad") and his father's texts turn ironic.
# ============================================================

default _family_grade_news = None   # her text about his last grade: {"gid", "grade", "kind", "day", "rung"}
default _bad_grade_streak = 0       # his bad grades in a row (FAMILY_BAD_GRADES); a good one resets it, C keeps it
default _grade_summons_idx = 0      # how many grades she already nagged about (grade_summons fires once per new bad grade)
default _allowance_frozen = None    # {"gid": who froze it, "fridays": Fridays left without allowance}
default _family_gf_text_day = 0     # the morning she may text him about his girlfriend again (0 = not rolled yet)
default _family_grade_source_told = False   # she explained HOW she knows his grades (once, her first grade text)
default _family_private_number_told = False # the grade thread's one-time closing note (today: "number saved"; pre-2026-10-11 saves read "you can't reply" instead)

init python:

    FAMILY_GUARDIAN_ROLES = ("stepmom",)
    FAMILY_BAD_GRADES = ("D", "F")
    FAMILY_GOOD_GRADES = ("A", "B")          # reset the streak; C keeps it
    FAMILY_LADDER = {1: ("confiscate",), 2: ("confiscate", "study_demand"), 3: ("confiscate", "study_demand")}
    FAMILY_LADDER_STOP_STAGE = 3             # her STORY step from which she covers for him (story_steps.rpy)
    FAMILY_NEWS_SLOT = 2                     # her news of the exam day comes from the Evening
    FAMILY_CONFISCATE_SHARE = 0.5            # she takes this share of his cash...
    FAMILY_CONFISCATE_MIN = 50               # ...at least this much (never more than he has)
    FAMILY_ALLOWANCE_FREEZE = 2              # Fridays without allowance after she takes his money
    FAMILY_SUGAR_COMP = 100                  # a SUBMISSIVE guardian pays him this when she hides a bad grade
    FAMILY_GF_TEXT_EVERY = (6, 10)           # days between her texts about his girlfriend

    # Her lines: gid (or "role:<role>") -> key -> variants. A text variant is a tuple of messages ("%s" = the
    # grade or a girl's name, "%d" = dollars or Fridays); a face-to-face one is a list of (face, line), face None =
    # narration.
    FAMILY_GRADE_TEXTS = {
        "shion": {
            # her first text about his grade ("%s": the grade, A to F)
            "good": [
                (_("I saw your grade. %s."), _("Acceptable. Don't expect a reward for doing the bare minimum.")),
                (_("%s. Your father hasn't stopped talking about it."), _("I told him not to get used to it. Prove me wrong.")),
                (_("%s. So you CAN study when you're afraid of me."), _("Remember that feeling.")),
            ],
            "good_reward": [
                (_("Keep this up and maybe I'll come see you one of these nights."),),
                (_("Good boys get rewarded. Keep studying and you'll see what I mean."),),
            ],
            "average": [
                (_("%s. Average."), _("I don't invest in average. Do better.")),
                (_("I saw your grade. %s."), _("Not a failure. Not a success either. Mediocrity is just failure taking its time.")),
            ],
            "bad": [
                (_("I saw your grade. %s."), _("Do you have any idea what you cost this family?")),
                (_("%s. I'm not even surprised."), _("Your father raised a disappointment. I'm going to fix that.")),
                (_("%s?"), _("You had two weeks. TWO WEEKS. And this is what you bring me?")),
            ],
            "missed": [
                (_("The school called. You didn't even show up to your exam."), _("An automatic F. Do you know how that makes ME look?")),
                (_("You skipped your exam."), _("An F for not even showing up. Your father is speechless. I'm not.")),
            ],
            # her punishments ("%d": the dollars she took / the Fridays without allowance)
            "confiscate": [
                (_("I just took $%d from your account."), _("Consider it a refund on a bad investment.")),
                (_("$%d. That's what your little vacation from the books just cost you."), _("Your father gave me the password. He trusts me with everything.")),
            ],
            "confiscate_broke": [
                (_("I went to take your money. There was nothing to take."), _("Of course there wasn't.")),
            ],
            "freeze": [
                (_("And no allowance. %d Fridays."),),
                (_("Your allowance is frozen. %d Fridays. Learn what things cost."),),
            ],
            "study_demand": [
                (_("I expect to see your books open tonight."), _("I'll be checking.")),
                (_("You're going to study until your eyes hurt."), _("No friends, no games, no distractions. I'll know if you don't.")),
            ],
            # his girlfriend is to blame ("%s": her name, or their names)
            "breakup_demand": [
                (_("And I know why your grades are falling. %s."), _("You're ending it. Tonight. By text.")),
                (_("This is that girl's fault. %s."), _("Open her chat. You're ending it. Now.")),
                # the author's lines (College Traits - Development for Shion)
                (_("Look at these scores... It's because of that girl! Isn't it!"), _("Break it off. Tonight... Or I'll do it for you... You won't like my methods.")),
                (_("That girl... Tsk... She's not good enough for you... You're better off ending it..."), _("Tonight. By text. I'll tell you exactly what to write.")),
            ],
            "breakup_write": [
                (_("Write exactly what I tell you. Not one word more."),),
            ],
            # what he types to his girlfriend
            "dictate": [
                _("I can't see you anymore. I need to focus on my studies. It's over."),
                _("We're done. My grades come first. Please don't text me back."),
                _("I'm sorry. My family thinks you're a distraction, and they're right. It's over."),
            ],
            "breakup_done": [
                (_("Good boy."), _("See how easy that was? Now study.")),
                (_("Done? Good."), _("Your father will be relieved. So am I.")),
            ],
            "breakup_refused": [
                (_("No?"), _("Then you'll learn what my patience costs.")),
                (_("You're telling ME no?"), _("Fine. Keep her. You'll pay for her too.")),
            ],
            # after her turn: she covers for him with his father ("%s": the grade)
            "s3_bad": [
                (_("%s. Your father thinks it was a B."), _("I told him myself. You owe me, and I always collect.")),
                (_("Don't worry about your grade."), _("I told your father you've been studying hard. You can thank me tonight.")),
            ],
            "s3_ok": [
                (_("%s. Look at you."), _("Maybe I'll let you celebrate with me.")),
            ],
            # while he is dating ("%s": his girlfriend's name)
            "gf_ask": [
                (_("Are you still seeing %s?"),),
                (_("That girl. %s. Is she the reason you look so tired lately?"),),
                (_("I asked around about %s. I'm not impressed."),),
            ],
            "gf_back_off": [
                (_("Everything you do is my business. Your father's roof is my roof."),),
                (_("Careful. I'm the one who decides what's my business."),),
            ],
            "gf_slow": [
                (_("Take it slow all the way to the exit."),),
                (_("Slow is good. Slow is easy to stop."),),
            ],
        },
    }

    # His father's text after her news (label _dad_grade_text). A key is a list of variants, or "excuse" / "blame"
    # lists: blame when the grade is an F (he skipped or did nothing), excuse otherwise.
    DAD_GRADE_TEXTS = {
        "good": [
            (_("Shion showed me your grade! That's my boy."),),
            (_("Saw your grade, kid. Proud of you. Even Shion smiled. Almost."),),
        ],
        "average": [
            (_("A C is fine, son. Don't tell Shion I said that."),),
        ],
        "confiscate": {
            "excuse": [(_("Shion told me about the money. Don't be mad at her, kid."), _("She just wants you to take this seriously."))],
            "blame": [(_("Shion told me about the money. I backed her up."), _("You brought this on yourself, son."))],
        },
        "study_demand": {
            "excuse": [(_("Shion told me she's making you study tonight."), _("She's right, son. Hit the books."))],
            "blame": [(_("Your grades are slipping, kid. Shion is furious."), _("Open a book. Don't make her come over there."))],
        },
        "breakup": {
            "excuse": [(_("Shion told me about the girl. I know it hurts, kid."), _("She's thinking about your future. We both are."))],
            "blame": [(_("Your grades were slipping because of some girl?"), _("Shion did the right thing. Focus."))],
        },
        "refused": [
            (_("Shion says you talked back to her."), _("That's not how I raised you, son.")),
        ],
        "s3_bad": [
            (_("Shion says you've been studying hard. Proud of you, son."),),
            (_("Shion told me your grade was great! See? She's good for you."),),
        ],
        "s3_ok": [
            (_("Shion showed me your grade. Proud of you, son!"),),
        ],
    }

    # ── Who watches his grades ──
    def family_lines(girl):
        """Her FAMILY_GRADE_TEXTS block (her gid, then her role), or None."""
        if girl is None:
            return None
        return FAMILY_GRADE_TEXTS.get(girl.gid) or FAMILY_GRADE_TEXTS.get(girl_role_key(girl) or "")

    def family_guardian():
        """The girl of his family who watches his grades (role in FAMILY_GUARDIAN_ROLES, with lines), reachable, or
        None."""
        for _g in girls_reachable():
            if girl_role(_g) in FAMILY_GUARDIAN_ROLES and family_lines(_g) is not None:
                return _g
        return None

    def family_covers_for_him(girl):
        """From that step of her STORY she is on his side: no punishments, she lies to his father for him
        (story_step, not femdom_stage: losing the femdom trait must never bring the punishments back)."""
        return story_step(girl) >= FAMILY_LADDER_STOP_STAGE

    def family_girlfriends(her):
        """The girls he is dating whom she can make him leave by text (reachable)."""
        return [_g for _g in get_player_girlfriends(girls_reachable()) if _g is not her]

    def family_pick(her, key):
        """A random variant of her lines for key (a tuple / list), or ()."""
        _pool = (family_lines(her) or {}).get(key) or ()
        return renpy.random.choice(_pool) if _pool else ()

    def family_fmt(line, *args):
        """A line of hers, translated, with its "%s" / "%d" filled (only when the English has one)."""
        if "%" in line and args:
            return _tl_fmt(line, *args)
        return _tl(line)

    # ── His grade ──
    def family_on_exam_grade(grade, why, day):
        """exam_record_grade: the streak and her news (played by label Wait 4c, family_grade_news_now)."""
        _her = family_guardian()
        if _her is None:
            print("[FAMILY] grade %s (%s): no one in his family watches his grades" % (grade, why))
            return
        _bad = grade in FAMILY_BAD_GRADES
        _rung = 0
        if family_covers_for_him(_her):
            _kind = "s3_bad" if _bad else "s3_ok"
        else:
            if _bad:
                store._bad_grade_streak += 1
                _rung = min(store._bad_grade_streak, max(FAMILY_LADDER))
            elif grade in FAMILY_GOOD_GRADES:
                store._bad_grade_streak = 0
            _kind = "missed" if why != "exam" else ("bad" if _bad else "good" if grade in FAMILY_GOOD_GRADES else "average")
        store._family_grade_news = {"gid": _her.gid, "grade": grade, "kind": _kind, "day": day, "rung": _rung}
        print("[FAMILY] grade %s (%s, Day %d): %s's news '%s', bad streak %d, rung %d" % (
            grade, why, day, _her.gid, _kind, store._bad_grade_streak, _rung))

    def family_grade_news_now():
        """label Wait 4c: the girl whose news about his grade plays now, or None. From the Evening of the exam day,
        and never in front of a girlfriend of his or of her (it is a text)."""
        _n = store._family_grade_news
        if not _n:
            return None
        _her = next((_g for _g in girls_reachable() if _g.gid == _n["gid"]), None)
        if _her is None:
            return None
        if store.Day == _n["day"] and store.TimeIndex < FAMILY_NEWS_SLOT:
            return None
        if _her.loc == store.CurrentLocation:
            return None
        if any(_g.loc == store.CurrentLocation for _g in family_girlfriends(_her)):
            return None
        return _her

    def family_punishments(news, refused=False):
        """What she does to him for that grade: FAMILY_LADDER by the rung, plus the money when he refused to break
        up. () for a grade that is not bad (or after her turn)."""
        _p = list(FAMILY_LADDER.get(news.get("rung", 0), ()))
        if refused and "confiscate" not in _p:
            _p.insert(0, "confiscate")
        return _p

    def family_confiscate(her):
        """She takes his money and freezes his allowance. Returns the dollars taken (0: nothing to take)."""
        _cash = int(getattr(store.Player, "cash", 0) or 0)
        _amt = min(_cash, max(FAMILY_CONFISCATE_MIN, int(_cash * FAMILY_CONFISCATE_SHARE)))
        store.Player.cash = _cash - _amt
        family_freeze_allowance(her, FAMILY_ALLOWANCE_FREEZE)
        print("[FAMILY] %s took $%d (cash %d -> %d)" % (her.gid, _amt, _cash, store.Player.cash))
        return _amt

    def family_freeze_allowance(her, fridays):
        _f = store._allowance_frozen or {"gid": her.gid, "fridays": 0}
        _f["gid"] = her.gid
        _f["fridays"] += fridays
        store._allowance_frozen = _f
        print("[FAMILY] allowance frozen by %s: %d Friday(s) left" % (her.gid, _f["fridays"]))

    def allowance_frozen_by():
        """label Wait 6 (Friday morning): the girl who froze his allowance this Friday (one Friday is used up), or
        None (he gets paid)."""
        _f = store._allowance_frozen
        if not _f or _f.get("fridays", 0) <= 0:
            store._allowance_frozen = None
            return None
        _f["fridays"] -= 1
        _her = next((_g for _g in ALL_GIRLS if _g.gid == _f["gid"]), None)
        print("[FAMILY] Friday allowance frozen by %s (%d Friday(s) left)" % (_f["gid"], _f["fridays"]))
        if _f["fridays"] <= 0:
            store._allowance_frozen = None
        return _her

    # ── His girlfriend ──
    def family_gf_text_now():
        """label Wait 6zz3 (once per morning): (her, girlfriend) of her text about his girlfriend, or None."""
        _her = family_guardian()
        if _her is None or family_covers_for_him(_her) or store._family_dinner != "done":
            return None
        _gfs = family_girlfriends(_her)
        if not _gfs:
            return None
        if store._family_gf_text_day <= 0:
            store._family_gf_text_day = store.Day + renpy.random.randint(*FAMILY_GF_TEXT_EVERY)
            print("[FAMILY] %s will text him about his girlfriend on Day %d" % (_her.gid, store._family_gf_text_day))
            return None
        if store.Day < store._family_gf_text_day or store._family_grade_news:
            return None
        store._family_gf_text_day = store.Day + renpy.random.randint(*FAMILY_GF_TEXT_EVERY)
        return (_her, renpy.random.choice(_gfs))

# ============================================================
# Her text about his grade (label Wait 4c), the punishment, then his father's text
# ============================================================
label _family_grade_news(her):
    python:
        _fg = store._family_grade_news
        store._family_grade_news = None
        _fg_msgs = [family_fmt(_l, _fg["grade"]) for _l in family_pick(her, _fg["kind"])]
        _fg_gfs = family_girlfriends(her) if _fg["rung"] else []
        _fg_refused = False
        _fg_dad = _fg["kind"] if _fg["kind"] in DAD_GRADE_TEXTS else None
        print("[FAMILY] %s's news: grade %s (%s), rung %d, girlfriends %s" % (
            her.gid, _fg["grade"], _fg["kind"], _fg["rung"], [_g.gid for _g in _fg_gfs]))

    play sound "audio/Notification.mp3" noloop
    $ Narration(_("Your phone buzzes. Someone sent you a message."))
    # Once ever: HOW she knows a grade he got in person minutes ago (tester 2026-10-10; wording his,
    # 2026-10-11: the old line read awkward and implied she reads a flooded inbox herself)
    if not store._family_grade_source_told:
        $ store._family_grade_source_told = True
        call _phone_typing(her, choices=[]) from _family_news_typing_source
        $ phone_add_msg(her.gid, her.gid, _tl(_("The college has standing instructions to forward me your results the moment they post.")))
    while _fg_msgs:
        call _phone_typing(her, choices=[]) from _family_news_typing
        $ phone_add_msg(her.gid, her.gid, _fg_msgs.pop(0))
    # her first text put her number in his phone (phone_add_msg, author 2026-10-11): the closing note
    # SAYS so once (it replaced "Sent from a private number. You can't reply.", which kept him unable
    # to answer her; same one-time flag, so old saves that read the old note get nothing new)
    if not store._family_private_number_told and getattr(her, "_number_from_her_text", False):
        $ store._family_private_number_told = True
        $ phone_add_msg(her.gid, "system", _tl(_("Number saved to your contacts.")), "system")

    # A good grade at step 1: she hints at a reward (the vent_night unlock needs a good grade)
    if _fg["kind"] == "good" and story_step(her) == 1 and not family_covers_for_him(her):
        python:
            _fg_reward = [family_fmt(_l) for _l in family_pick(her, "good_reward")]
        while _fg_reward:
            call _phone_typing(her, choices=[]) from _family_news_reward_typing
            $ phone_add_msg(her.gid, her.gid, _fg_reward.pop(0))

    # A SUBMISSIVE guardian covering a bad grade also pays for the scare (the author's "ela compensa", 2026-10-03):
    # she hid it from his father, and money is how she says sorry now. [SUGAR]-style log, flat amount.
    if _fg["kind"] == "s3_bad" and her.has_trait("submissive"):
        python:
            Player.add_cash(FAMILY_SUGAR_COMP)
            print("[SUGAR] %s compensates the bad grade: +$%d (cash %d)" % (her.gid, FAMILY_SUGAR_COMP, Player.cash))
        call _phone_typing(her, choices=[]) from _family_news_typing_comp
        $ phone_add_msg(her.gid, her.gid, _tl(_("I sent you something for the scare. Spend it on coffee and STUDY. Please.")))

    # a girlfriend: any bad grade is her fault
    if _fg_gfs:
        call _family_breakup_demand(her, _fg_gfs) from _call_family_breakup_demand
        if _return == "obeyed":
            $ _fg_dad = "breakup"
            $ _fg_punish = []
        else:
            $ _fg_refused = True
            $ _fg_punish = family_punishments(_fg, refused=True)
    else:
        $ _fg_punish = family_punishments(_fg)

    python:
        _fg_msgs = []
        for _fg_p in _fg_punish:
            if _fg_p == "confiscate":
                _fg_amt = family_confiscate(her)
                if _fg_amt > 0:
                    _fg_msgs += [family_fmt(_l, _fg_amt) for _l in family_pick(her, "confiscate")]
                else:
                    _fg_msgs += [family_fmt(_l) for _l in family_pick(her, "confiscate_broke")]
                _fg_msgs += [family_fmt(_l, FAMILY_ALLOWANCE_FREEZE) for _l in family_pick(her, "freeze")]
            elif _fg_p == "study_demand":
                _fg_msgs += [family_fmt(_l) for _l in family_pick(her, "study_demand")]
            if not _fg_refused:
                _fg_dad = _fg_p
        if _fg_refused:
            _fg_dad = "refused"
    while _fg_msgs:
        call _phone_typing(her, choices=[]) from _family_news_punish_typing
        $ phone_add_msg(her.gid, her.gid, _fg_msgs.pop(0))
    call screen phone_chat_screen(her, choices=[])

    if _fg_dad is not None:
        call _dad_grade_text(_fg_dad, _fg["grade"]) from _call_dad_grade_text
    return

# ============================================================
# A girlfriend: she makes him end it by text. Returns "obeyed" / "refused"
# ============================================================
label _family_breakup_demand(her, gfs):
    python:
        _fbd_names = ", ".join(_g.Name for _g in gfs)
        _fbd_msgs = [family_fmt(_l, _fbd_names) for _l in family_pick(her, "breakup_demand")]
    while _fbd_msgs:
        call _phone_typing(her, choices=[]) from _family_breakup_demand_typing
        $ phone_add_msg(her.gid, her.gid, _fbd_msgs.pop(0))
    python:
        _fbd_choices = [
            (_tl(_("Fine. I'll do it.")), "obey"),
            (_tl(_("No. I'm not breaking up with her.")) if len(gfs) == 1 else _tl(_("No. I'm not breaking up with them.")), "refuse"),
        ]
    call screen phone_chat_screen(her, choices=_fbd_choices)
    $ _fbd_pick = _return

    if _fbd_pick == "obey":
        $ phone_add_msg(her.gid, "player", _fbd_choices[0][0])
        python:
            _fbd_msgs = [family_fmt(_l) for _l in family_pick(her, "breakup_write")]
        while _fbd_msgs:
            call _phone_typing(her, choices=[]) from _family_breakup_write_typing
            $ phone_add_msg(her.gid, her.gid, _fbd_msgs.pop(0))
        call screen phone_chat_screen(her, auto_close=1.2, choices=[])
        $ _fbd_queue = list(gfs)
        while _fbd_queue:
            call _family_breakup_text(her, _fbd_queue.pop(0)) from _call_family_breakup_text
        python:
            _fbd_msgs = [family_fmt(_l) for _l in family_pick(her, "breakup_done")]
            femdom_turn_note(her, "obeyed", "breakup")
        while _fbd_msgs:
            call _phone_typing(her, choices=[]) from _family_breakup_done_typing
            $ phone_add_msg(her.gid, her.gid, _fbd_msgs.pop(0))
        return "obeyed"

    # "No" (or he put the phone away without a word: she takes it as a no)
    if _fbd_pick == "refuse":
        $ phone_add_msg(her.gid, "player", _fbd_choices[1][0])
    python:
        _fbd_msgs = [family_fmt(_l) for _l in family_pick(her, "breakup_refused")]
        femdom_turn_note(her, "talked_back", "breakup")
        print("[FAMILY] he refused to break up with %s (%s)" % ([_g.gid for _g in gfs], _fbd_pick))
    while _fbd_msgs:
        call _phone_typing(her, choices=[]) from _family_breakup_refused_typing
        $ phone_add_msg(her.gid, her.gid, _fbd_msgs.pop(0))
    return "refused"

# He sends one girlfriend the words his stepmother dictated; she answers
label _family_breakup_text(her, gf):
    python:
        _fbt_line = renpy.random.choice((family_lines(her) or {}).get("dictate") or [_("It's over.")])
        phone_add_msg(gf.gid, "player", _tl(_fbt_line))
    call screen phone_chat_screen(gf, auto_close=1.2, choices=[])
    python:
        _fbt_mood, _fbt_reply = player_breakup_apply(gf, "stepmom", "text")
        _fbt_reply = list(_fbt_reply)
        print("[FAMILY] %s made him break up with %s by text (%s)" % (her.gid, gf.gid, _fbt_mood))
    while _fbt_reply:
        call _phone_typing(gf, choices=[]) from _family_breakup_reply_typing
        $ phone_add_msg(gf.gid, gf.gid, _tl(_fbt_reply.pop(0)))
    call screen phone_chat_screen(gf, choices=[])
    return

# ============================================================
# His father's text after her news (DAD_GRADE_TEXTS)
# ============================================================
label _dad_grade_text(key, grade):
    python:
        _dgt = DAD_GRADE_TEXTS.get(key)
        if isinstance(_dgt, dict):
            _dgt = _dgt["blame" if grade == "F" else "excuse"]
        _dgt_msgs = [_tl(_l) for _l in renpy.random.choice(_dgt)] if _dgt else []
        print("[DAD] grade text '%s' (grade %s)" % (key, grade))
    if _dgt_msgs:
        play sound "audio/Notification.mp3" noloop
        $ Narration(_("Your phone buzzes. A message from your father."))
        while _dgt_msgs:
            call _phone_typing(Dad, choices=[]) from _dad_grade_text_typing
            $ phone_add_msg(Dad.gid, Dad.gid, _dgt_msgs.pop(0))
        call screen phone_chat_screen(Dad, choices=[])
    return

# ============================================================
# A morning text about his girlfriend (label Wait 6zz3, family_gf_text_now)
# ============================================================
label _family_gf_text(her, gf):
    python:
        _fgf_msgs = [family_fmt(_l, gf.Name) for _l in family_pick(her, "gf_ask")]
        print("[FAMILY] %s texts him about %s (Day %d)" % (her.gid, gf.gid, Day))
    play sound "audio/Notification.mp3" noloop
    $ Narration(_("Your phone buzzes. Someone sent you a message."))
    while _fgf_msgs:
        call _phone_typing(her, choices=[]) from _family_gf_ask_typing
        $ phone_add_msg(her.gid, her.gid, _fgf_msgs.pop(0))
    python:
        _fgf_choices = [
            (_tl(_("She's none of your business.")), "back_off"),
            (_tl(_("We're taking it slow.")), "slow"),
        ]
    call screen phone_chat_screen(her, choices=_fgf_choices)
    $ _fgf_pick = _return
    if _fgf_pick in ("back_off", "slow"):
        python:
            phone_add_msg(her.gid, "player", _fgf_choices[0][0] if _fgf_pick == "back_off" else _fgf_choices[1][0])
            _fgf_msgs = [family_fmt(_l) for _l in family_pick(her, "gf_" + _fgf_pick)]
            if _fgf_pick == "back_off":
                Change_Status(her, "Love", -2)
                Change_Status(her, "Inbt", 3)
            else:
                Change_Status(her, "Love", 1)
        while _fgf_msgs:
            call _phone_typing(her, choices=[]) from _family_gf_reply_typing
            $ phone_add_msg(her.gid, her.gid, _fgf_msgs.pop(0))
        call screen phone_chat_screen(her, choices=[])
    return

# Her face-to-face lines: a list of (face, line), face None = narration
label _family_face_lines(her, lines):
    $ _ffl = list(lines or [])
    while _ffl:
        $ _ffl_face, _ffl_line = _ffl.pop(0)
        if _ffl_face is None:
            $ Narration(_ffl_line)
        else:
            $ set_scene_expression(her, _ffl_face, pose="standing")
            $ Say_Line(her, _ffl_line)
    $ set_scene_expression(her, "normal", pose="standing")
    return
