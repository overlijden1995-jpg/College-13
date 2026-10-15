## children.rpy: life AFTER the birth.
## pregnancy.rpy owns everything until she is back on campus. From that morning on the child is DATA that lives
## here: the record frozen at birth, its age, whether her NPC partner is fooled, the weekly child support, and
## the ONE wipe the Baby Eraser calls. Text only: the baby never appears, it lives with her family.

# Weekly child support, computed by the daily tick and announced by label Wait (system_time.rpy, step 6a2):
# (((gid, amount), ...), balance right after the charge) or None. Saved; `default` also covers old saves.
# The stored balance is for the log only: the narration reads the LIVE balance (other money moves in between).
default _child_support_notice = None
# Morning phone events about the children (children_morning_pick): the Day one already played, and the mother who
# commented on the support money last week. Saved; `default` also covers old saves.
default _child_event_day = -1
default _child_money_react_last = None
# gids of the mothers the LAST weekly charge really paid (she only comments on money that went out)
default _child_support_paid = ()
# Her birth post on Instabook, narrated the morning after she is back: [(gid, Day it shows), ...]
default _child_birth_posts = []

init python:

    # ============================================================
    # THE CHILD RECORD (frozen at birth)
    # ============================================================
    # girl._children = [record, ...]: one plain dict per child (plain data only: it lives in the girl snapshot).
    #   "born"     : Day her labor started (the Day she left campus)
    #   "response" : his answer at the discovery ("supportive" / "breeding" / "deny" / "npc_paternity" / None).
    #                The live flag _player_pregnancy_response is scoped ("cycle"): it dies with the next pregnancy.
    #   "official" : who she names as the father on the day the child is born: "npc" / "player" / "nobody"
    #   "npc_id" / "npc_name" : her NPC partner that day (None when she is single)
    # girl._children_count stays the counter every older reader uses: children_sync keeps the two in step.

    def child_npc_is_father(girl):
        """Her NPC partner stands as the father RIGHT NOW: the paternity claim is live and he is still with her.
        Either he was fooled (Choice 4 of the discovery) or he is the NTR boundary 4 partner who knows and said
        "I'll raise the kid". The claim dies with the relationship (clear_npc_partner resets it)."""
        return bool(getattr(girl, "_npc_paternity_claimed", False)) and girl.has_npc_partner()

    def child_husband_is_father(girl):
        """A married girl names her HUSBAND as the father (shion_pregnancy.rpy): officially his, he believes it, he
        raises the child with her. Every child of hers, as long as she is married to him."""
        return pregnancy_husband(girl) is not None

    def _child_official_at_birth(girl):
        if child_husband_is_father(girl):
            return "husband"
        if child_npc_is_father(girl):
            return "npc"
        if girl.is_dating_player() or getattr(girl, "_player_pregnancy_response", None) in ("supportive", "breeding"):
            return "player"
        return "nobody"

    def _child_new_record(girl, born_day):
        # Her partner is read from the GIRL (npc_partner_id / _npc_partner_name live in her snapshot), never from
        # the NPC registry: children_sync runs in after_load BEFORE the registry is rebuilt, when it still
        # holds the partners of the save that was open before.
        _has = girl.has_npc_partner()
        return {
            "born": max(1, int(born_day)),
            "response": getattr(girl, "_player_pregnancy_response", None),
            "official": _child_official_at_birth(girl),
            "npc_id": getattr(girl, "npc_partner_id", None) if _has else None,
            "npc_name": getattr(girl, "_npc_partner_name", None) if _has else None,
        }

    def child_register_birth(girl, born_day=None):
        """THE writer: one more child. Called by pregnancy_return_apply (the morning she is back) BEFORE the
        birth state is cleared: born = the Day her labor started (_birth_return_day - _BIRTH_AWAY_DAYS)."""
        if born_day is None:
            born_day = getattr(girl, "_birth_return_day", 0) - _BIRTH_AWAY_DAYS
            if born_day <= 0:
                born_day = store.Day - _BIRTH_AWAY_DAYS
        _rec = _child_new_record(girl, born_day)
        girl._children = list(getattr(girl, "_children", None) or []) + [_rec]
        girl._children_count = len(girl._children)
        print("[CHILDREN] %s: child #%d registered: %s" % (girl.gid, girl._children_count, _rec))
        girl._child_event_next = {"baby_news": store.Day + renpy.random.randint(5, 8)}    # her first baby news
        store._child_birth_posts = list(getattr(store, "_child_birth_posts", None) or []) + [(girl.gid, store.Day + 1)]
        child_achievements_check("birth of %s's child" % girl.gid)
        return _rec

    def children_sync(girl):
        """Invariant len(_children) == _children_count, idempotent. Pads a save made before the record
        existed (the author's development saves: pregnancy was never public without it) and drops records
        a console edit left behind. A padded birth day is the best guess the save allows: the 14 day
        cooldown starts the morning she is back, so while it runs it dates the return exactly."""
        _recs = list(getattr(girl, "_children", None) or [])
        _count = max(0, int(getattr(girl, "_children_count", 0) or 0))
        if len(_recs) == _count:
            return False
        if len(_recs) > _count:
            _recs = _recs[:_count]
        else:
            _cd = getattr(girl, "_pregnancy_cooldown", 0) or 0
            _returned = (store.Day - (14 - _cd)) if _cd > 0 else (store.Day - 14)
            while len(_recs) < _count:
                _recs.append(_child_new_record(girl, _returned - _BIRTH_AWAY_DAYS))
        girl._children = _recs
        print("[CHILDREN][MIGRATE] %s: records synced to %d child(ren): %s" % (girl.gid, _count, _recs))
        return True

    def girl_is_mother(girl):
        return getattr(girl, "_children_count", 0) > 0

    def player_mothers():
        """Girls who have a child of his, in ALL_GIRLS order."""
        return [_g for _g in ALL_GIRLS if girl_is_mother(_g)]

    def _child_word(girl, one="the baby", many="the kids"):
        return many if getattr(girl, "_children_count", 0) >= 2 else one

    def child_record(girl, idx=-1):
        """Her child record (the latest by default), or None."""
        _recs = getattr(girl, "_children", None) or []
        try:
            return _recs[idx]
        except IndexError:
            return None

    # ============================================================
    # AGE (game days: time is compressed, like the 65 / 130 day pregnancy itself)
    # ============================================================
    # tier -> first day of age, LATEST FIRST (resolved like _PREG_BODY_MOMENTS). A line that only makes sense
    # at some age carries its tiers next to it: (line, first_tier, last_tier), see child_lines_for_age.
    _CHILD_AGE_TIERS = (("toddler", 150), ("baby", 60), ("infant", 21), ("newborn", 0))
    _CHILD_AGE_ORDER = tuple(_t for _t, _d in reversed(_CHILD_AGE_TIERS))   # youngest first

    def child_age_days(girl, idx=-1):
        """Age of her child in game days, or None when she has no record."""
        _rec = child_record(girl, idx)
        if _rec is None:
            return None
        return max(0, store.Day - _rec["born"])

    def child_age_tier(girl, idx=-1):
        """"newborn" / "infant" / "baby" / "toddler", or None when she has no record."""
        _age = child_age_days(girl, idx)
        if _age is None:
            return None
        for _tier, _from in _CHILD_AGE_TIERS:
            if _age >= _from:
                return _tier
        return _CHILD_AGE_ORDER[0]

    # what the screens print for each tier (resolved with _tr at display, like the rest of the Fertility app)
    _CHILD_AGE_LABELS = {"newborn": _("Newborn"), "infant": _("Infant"), "baby": _("Baby"), "toddler": _("Toddler")}

    def _child_age_label_for(girl, idx):
        _tier = child_age_tier(girl, idx)
        if _tier is None:
            return None
        return "%s (%s)" % (_tr(_CHILD_AGE_LABELS[_tier]), _fert_days(child_age_days(girl, idx)))

    def child_age_label(girl):
        """"Newborn (3 days)" for the screens, or None when she has no child.
        For 2+ children returns a comma-separated list, newest first."""
        _count = getattr(girl, "_children_count", 0)
        if _count == 0:
            return None
        if _count == 1:
            return _child_age_label_for(girl, -1)
        _labels = [_child_age_label_for(girl, i) for i in range(_count - 1, -1, -1)]
        return ", ".join(_l for _l in _labels if _l)

    def child_raised_by(girl):
        """"Raised by Kyle" while her NPC partner stands as the father (the LIVE partner: the name frozen in
        the record grows stale the day he leaves), else None."""
        if child_husband_is_father(girl):
            return _tr("Raised by %s") % _tl(_("her husband"))
        _name = getattr(girl, "_npc_partner_name", None)
        if not child_npc_is_father(girl) or not _name:
            return None
        return _tr("Raised by %s") % _name

    def child_status_row(girl):
        """One mother of the CHILDREN block of the player status page. Plain data, pure."""
        return {"gid": girl.gid, "name": girl.Name, "color": girl.color, "age": child_age_label(girl) or "",
                "raised_by": child_raised_by(girl), "support": child_support_due(girl)}

    def child_lines_for_age(pool, girl):
        """Lines of a pool that are TRUE for her child's age right now. A pool entry is either a plain line
        (true at any age) or (line, first_tier, last_tier). With no record only the plain lines qualify.
        Returns plain strings; [] when nothing fits (the caller falls back to a pool that always fits)."""
        _tier = child_age_tier(girl)
        _at = _CHILD_AGE_ORDER.index(_tier) if _tier is not None else None
        _out = []
        for _entry in pool:
            if not isinstance(_entry, tuple):
                _out.append(_entry)
                continue
            _line, _first, _last = _entry
            if _at is not None and _CHILD_AGE_ORDER.index(_first) <= _at <= _CHILD_AGE_ORDER.index(_last):
                _out.append(_line)
        return _out

    # ============================================================
    # WHO BELIEVES WHAT
    # ============================================================
    def child_father_fooled(girl):
        """Her NPC partner BELIEVES the child is his. _npc_paternity_claimed alone does not say so: it is set
        by Choice 4 of the discovery (he is lied to) AND by the NTR boundary 4 partner who KNOWS and said
        "I'll raise the kid". Fooled = the claim is live AND the player chose to pass the child off as his
        (the answer frozen in the record once the child is born, the live flag before that)."""
        if child_husband_is_father(girl):
            return True     # her husband believes it (shion_pregnancy.rpy): she never tells him
        if not child_npc_is_father(girl):
            return False
        _rec = child_record(girl)
        _resp = _rec["response"] if _rec is not None else getattr(girl, "_player_pregnancy_response", None)
        return _resp == "npc_paternity"

    # ============================================================
    # HER MOOD ABOUT HIM AS A FATHER (one reader: mother_mood)
    # ============================================================
    # girl._father_involvement: 0..100, how present he is as a father. None = never moved: his answer at the
    # discovery (frozen in the child record) still speaks for him. Moved ONLY by father_involvement_change
    # (asking about the baby, answering her texts...). It sets the TONE of what she says about the baby,
    # never a stat by itself, and nothing here may run from the daily tick through Change_Status (that
    # would count as contact in hardcore mode).
    _FATHER_INVOLVEMENT_SEED = {"supportive": 60, "breeding": 50, "npc_paternity": 35, "deny": 10}
    _FATHER_INVOLVEMENT_NO_ANSWER = 35    # a mother with no answer on record (console, old save)
    _FATHER_INVOLVEMENT_WARM = 40         # from here up she talks about the baby warmly

    def father_involvement(girl):
        _value = getattr(girl, "_father_involvement", None)
        if _value is None:
            # frozen in the record once the child is born; the live answer before that (her week away)
            _rec = child_record(girl)
            _resp = _rec["response"] if _rec is not None else getattr(girl, "_player_pregnancy_response", None)
            return _FATHER_INVOLVEMENT_SEED.get(_resp, _FATHER_INVOLVEMENT_NO_ANSWER)
        return _value

    def father_involvement_change(girl, amount, reason=""):
        """THE writer. Returns the new value."""
        _old = father_involvement(girl)
        girl._father_involvement = max(0, min(100, _old + int(amount)))
        print("[CHILDREN] %s: father involvement %d -> %d (%s)" % (girl.gid, _old, girl._father_involvement, reason))
        return girl._father_involvement

    def father_tone(girl):
        """How she talks to HIM about the baby: "secret" (her NPC partner believes it is his: she keeps her
        voice down), "warm", "distant" (he denied it and has not made up for it). Works before the birth too
        (her week away)."""
        if child_father_fooled(girl):
            return "secret"
        if father_involvement(girl) >= _FATHER_INVOLVEMENT_WARM or girl.has_trait("pregnancy_fetish"):
            return "warm"
        return "distant"

    def mother_mood(girl):
        """father_tone of a MOTHER; None = not a mother."""
        return father_tone(girl) if girl_is_mother(girl) else None

    def mother_hush(girl):
        """The fooled partner is ON SCREEN right now: she will not talk about whose baby it is at all.
        _preg_npc_present (ChitChat.rpy) is the presence test with the phone guard: never true over the phone."""
        return mother_mood(girl) == "secret" and (_preg_npc_present(girl) or husband_present(girl))

    # ============================================================
    # LINES ABOUT THE BABY (one picker for the chitchat, the question and her texts)
    # ============================================================
    # Lines of the postpartum pools that only work FACE TO FACE (she offers to show him a picture): never texted.
    # English source text, byte for byte (mock_test23 fails when one of them no longer exists in the pools).
    _BABY_LINES_FACE_ONLY = (
        "I'm NOT one of those moms who shows baby pictures to everyone. But do you want to see one? Just one. Whatever.",
        "I never thought I'd be the kind of person who shows baby pictures. Do you want to see one?",
    )

    # Lines of the multi-child pools (here and ChitChat.rpy) that state EXACTLY two children: never for a mother
    # of three or more (no birth limit since v0.12.1). English source text, byte for byte.
    _CHILD_LINES_TWO_ONLY = (
        "Good. Really good. Keeping up with two is wild, though.",
        "Loud, messier, and twice the fun. My family is going insane.",
        "Two of them now. Two! My mom says I owe her a vacation.",
        "Both doin' just fine, sugar. My aunt's got her hands full.",
        "Gettin' along like two peas in a pod. Mostly.",
        "Both alive. Both loud. I call that a win.",
        "T-they're great! Grandpa says two is easier because they entertain each other.",
        "Having two is a whole different beast. My mom says she's aged ten years in a month.",
        "Two babies, sugar. My aunt says the house sounds like a zoo and she wouldn't change a thing.",
        "Two kids. I have TWO kids. How did that happen? Don't answer that.",
        "G-grandpa says having two is easier because they entertain each other. I think he's lying.",
    )

    def _child_lines_for_count(lines, girl):
        """Drops the lines that say EXACTLY two when she has three or more children."""
        if getattr(girl, "_children_count", 0) <= 2:
            return list(lines)
        return [_l for _l in lines if _l not in _CHILD_LINES_TWO_ONLY]

    def baby_line_pick(girl, texting=False):
        """One line about the baby in her style, TRUE for the baby's age right now, that he has not heard yet.
        Memory: girl._baby_lines_seen (English source lines, plain data). When every line that fits was heard
        the memory of THOSE lines restarts, and the line heard last never opens the new round.
        texting=True (her phone events) leaves out the lines that only work face to face. Phone mode counts as
        texting too: the Chat action of her thread runs the chitchat and Say_Line turns the line into a text."""
        texting = texting or getattr(store, "_phone_mode", False)
        _pool = child_lines_for_age(girl_pool(_PREG_CHITCHAT_POSTPARTUM, girl, "baby line"), girl)
        if not _pool:
            _pool = child_lines_for_age(_PREG_CHITCHAT_POSTPARTUM["_default"], girl)
        if getattr(girl, "_children_count", 0) >= 2:
            _pool_multi = _child_lines_for_count(girl_pool(_PREG_CHITCHAT_POSTPARTUM_MULTI, girl, "baby line multi"), girl)
            if not _pool_multi:
                _pool_multi = _child_lines_for_count(_PREG_CHITCHAT_POSTPARTUM_MULTI["_default"], girl)
            if _pool_multi:
                _pool = list(_pool) + list(_pool_multi)
        if texting:
            _pool = [_l for _l in _pool if _l not in _BABY_LINES_FACE_ONLY] or _pool
        _seen = list(getattr(girl, "_baby_lines_seen", None) or [])
        _fresh = [_l for _l in _pool if _l not in _seen]
        if not _fresh:
            _last = _seen[-1] if _seen else None
            _seen = [_l for _l in _seen if _l not in _pool]
            _fresh = [_l for _l in _pool if _l != _last] or list(_pool)
        _line = renpy.random.choice(_fresh)
        girl._baby_lines_seen = _seen + [_line]
        return _line

    # ============================================================
    # CHILD SUPPORT (one rule, read by the tick and by both Fertility data providers)
    # ============================================================
    def child_support_player_share(girl):
        """The part of the weekly child support that falls on the player, by her family's money
        (_CHILD_SUPPORT_PLAYER_SHARE, pregnancy.rpy): poor 1.0, middle class 0.5, rich 0.0 (her family pays it all)."""
        for _trait, _share in _CHILD_SUPPORT_PLAYER_SHARE.items():
            if girl.has_trait(_trait):
                return _share
        return _CHILD_SUPPORT_PLAYER_SHARE_MIDDLE

    def child_support_due(girl):
        """What he owes her every week. NOTHING while her NPC partner stands as the father (author's rule,
        2026-09-18): that man is raising the child. The week he leaves her, the claim is gone and the player
        pays again: the weekly narration shows her name back in the breakdown. Otherwise her family's money
        sets his part (child_support_player_share, 2026-09-30): a rich mother's family pays it all (0 here)."""
        if child_npc_is_father(girl):
            return 0
        _full = _CHILD_SUPPORT_WEEKLY * getattr(girl, "_children_count", 0)
        return int(round(_full * child_support_player_share(girl)))

    def child_support_total():
        return sum(child_support_due(_g) for _g in ALL_GIRLS)

    def child_support_next_in():
        """Days until the next weekly charge (the tick charges when Day % 7 == 0, at dawn: on a charge day
        this morning's charge already ran, so the answer is 7)."""
        return 7 - (store.Day % 7)

    def child_support_charge():
        """Weekly charge, once per tick for every mother together (the daily tick calls it on pay day). The
        tick only computes: label Wait announces it (store._child_support_notice), so the money never just
        disappears. A negative balance is allowed (author's rule)."""
        child_achievements_check("weekly charge")     # a save that already had children catches up here
        _rows = tuple((_g.gid, child_support_due(_g)) for _g in ALL_GIRLS if child_support_due(_g) > 0)
        store._child_support_paid = tuple(_gid for _gid, _amount in _rows)
        if not _rows:
            return 0
        _total = sum(_amount for _gid, _amount in _rows)
        store.Player.cash -= _total
        store._child_support_notice = (_rows, store.Player.cash)
        # the receipt stays where he talks to her (an orange system chip in her thread). The text is translated
        # BEFORE it is stored: a formatted phone text never matches a translation pair at display.
        for _gid, _amount in _rows:
            phone_add_msg(_gid, "system", _tl_fmt(_("Child support sent: $%d"), _amount), "system")
        print("[CHILDREN] child support charged: $%d %s, balance $%d" % (_total, _rows, store.Player.cash))
        return _total

    def child_support_notice_lines():
        """Narration of the pending weekly charge (translated, names resolved now), and the notice is consumed.
        [] when nothing is pending."""
        _notice = getattr(store, "_child_support_notice", None)
        store._child_support_notice = None
        if not _notice:
            return []
        _rows, _balance_then = _notice
        _rows = [(_gid, _amount) for _gid, _amount in _rows if _gid in GIRL_BY_ID]
        if not _rows:
            return []
        # the balance he SEES: BigFans income lands in the same cleanup and the investor income one step before
        # this narration (told with the live balance), so the number frozen at the tick contradicted them
        _balance = store.Player.cash
        _total = sum(_amount for _gid, _amount in _rows)
        _who = format_name_list(["%s $%d" % (GIRL_BY_ID[_gid].Name, _amount) for _gid, _amount in _rows])
        _lines = [_tl_fmt(_("Child support went out this week: {b}$%d{/b} (%s). Balance: {b}$%d{/b}."), _total, _who, _balance)]
        if _balance < 0:
            _lines.append(_tl(_("You are in the red. Until the balance is positive again, you cannot pay for anything.")))
        return _lines

    # ============================================================
    # THE ONE WIPE (Baby Eraser)
    # ============================================================
    # attr -> neutral value (deep-copied). Anything a later feature stores per child gets ONE row here, never
    # one more line in the Eraser label. NOT here on purpose: player_firsts["first_pregnancy"] and
    # _pregnancy_told_day (his milestone: SHE forgets, he does not) and the achievements (persistent).
    _CHILD_STATE = {
        "_children": [],
        "_children_count": 0,
        "_pregnancy_count": 0,
        "_postpartum": False,
        "_pregnancy_cooldown": 0,
        "_father_involvement": None,
        "_baby_lines_seen": [],
        "_baby_asked_day": 0,
        "_child_event_next": {},
    }
    # flags the OTHER girls hold about this mother: "<prefix><mother gid>"
    _CHILD_PAIR_FLAG_PREFIXES = ("preg_gossip_jealous_", "child_gossip_jealous_", "child_news_labor_", "child_news_back_")

    def children_forget(mother, reason=""):
        """The Baby Eraser: the birth never happened, for her and for everybody else. Child state, the
        pregnancy-scoped flags (his discovery answer, the paternity claim and what her partner was about
        to do: _pregnancy_reset_flags), the procedure, what the other girls hold about her pregnancy, and
        any notice still queued with her name."""
        import copy as _copy
        _changed = []
        if girl_is_mother(mother):
            # HE remembers a child she no longer has: "How's the baby?" stays in the Ask Her menu and she does
            # not understand the question (never part of _CHILD_STATE: it is his memory, not hers)
            mother._child_forgotten = True
        for _attr, _neutral in _CHILD_STATE.items():
            if getattr(mother, _attr, _neutral) != _neutral:
                _changed.append("%s=%r" % (_attr, getattr(mother, _attr)))
            setattr(mother, _attr, _copy.deepcopy(_neutral))
        _pregnancy_reset_flags(mother, "cycle", "children_forget")
        if pregnancy_procedure_undo(mother, reason or "children_forget"):
            _changed.append("procedure")
        for _other in ALL_GIRLS:
            if _other is mother:
                continue
            for _prefix in _CHILD_PAIR_FLAG_PREFIXES:
                if _other.get_flag(_prefix + mother.gid):
                    _other.clear_flag(_prefix + mother.gid)
                    _changed.append("%s.%s%s" % (_other.gid, _prefix, mother.gid))
        _notice = getattr(store, "_child_support_notice", None)
        if _notice:
            _rows = tuple(_r for _r in _notice[0] if _r[0] != mother.gid)
            store._child_support_notice = (_rows, _notice[1]) if _rows else None
        store._child_birth_posts = [_p for _p in (getattr(store, "_child_birth_posts", None) or []) if _p[0] != mother.gid]
        print("[CHILDREN] %s: FORGOTTEN (%s), cleared: %s" % (mother.gid, reason, ", ".join(_changed) or "nothing"))
        return _changed

    # ============================================================
    # MORNING PHONE EVENTS: she brings the baby into his week (label Wait step 6k)
    # ============================================================
    # At most ONE children event per morning for ALL mothers together (store._child_event_day), candidates
    # shuffled: with three mothers nothing piles up and nobody is favored by the ALL_GIRLS order.
    #   "away_text"   the one text of her week away ("We're both fine"): his reply already sets her tone
    #   "money_react" the morning after the weekly charge, ONE mother a week comments on the money
    #   "baby_news"   every 7 to 10 days she tells him something about the baby, and he can answer
    # Every event is a phone conversation with the same shape (label _child_morning_event): her opening
    # messages, his choices (if any), the effect of his answer, her closing messages.
    _CHILD_EXTRA_MONEY = 100      # "Need anything? I can send money."

    # event -> ((reply key, caption = what HE writes), ...)
    _CHILD_EVENT_CHOICES = {
        "baby_news": (
            ("more",  _("Tell me more.")),
            ("money", _("Need anything? I can send money.")),
            ("busy",  _("Busy right now. Talk later.")),
        ),
        "away_text": (
            ("glad", _("I'm glad you're both okay.")),
            ("ok",   _("Good. Text me when you're back.")),
            ("read", _("Leave her on read.")),
        ),
        "money_react": (),
    }
    # (event, reply) -> effect. "involvement": father_involvement_change. "stats": Change_Status (a real answer is
    # real contact, hardcore mode included). "cost": money he sends; when he cannot pay the reply becomes
    # "<reply>_broke" (a real branch, never a hidden button). "baby_line": she tells one more thing about the
    # baby. "silent": he writes nothing and she says nothing. "no_answer": he writes, she does not answer.
    # "ignored" = he closed the phone without answering.
    _CHILD_EVENT_EFFECTS = {
        ("baby_news", "more"):        {"involvement": 4, "stats": {"Love": 2}, "baby_line": True},
        ("baby_news", "money"):       {"involvement": 8, "stats": {"Love": 3}, "cost": _CHILD_EXTRA_MONEY},
        ("baby_news", "money_broke"): {"involvement": 2},
        ("baby_news", "busy"):        {"involvement": -5, "stats": {"Love": -2}},
        ("baby_news", "ignored"):     {"involvement": -2, "silent": True},
        ("away_text", "glad"):        {"involvement": 10},
        ("away_text", "ok"):          {},
        ("away_text", "read"):        {"involvement": -5, "silent": True},
        ("away_text", "ignored"):     {"involvement": -5, "silent": True},
        # her partner never leaves her side and she asked him NOT to write back ("<reply>_secret" replaces the
        # reply in the secret tone): writing anyway costs him, staying quiet is what she wanted
        ("away_text", "glad_secret"):    {"involvement": -3, "no_answer": True},
        ("away_text", "ok_secret"):      {"involvement": -3, "no_answer": True},
        ("away_text", "read_secret"):    {"involvement": 2, "silent": True},
        ("away_text", "ignored_secret"): {"involvement": 2, "silent": True},
    }
    # event -> {gid: {key: [script, ...]}}; a script = the messages she sends, in order. Fallback PER KEY to
    # "_default" (girl_pool with key). Keys: the opening is "open_<tone>" (father_tone: warm / secret, and
    # for the money "thanks" / "cold" / "red"), a closing is the reply key. Texts go through
    # _format_partner_line (it translates; partner placeholders allowed). The baby is always "the baby".
    _CHILD_EVENT_LINES = {
        "baby_news": {
            "_default": {
                # said AFTER a baby line (baby_line_pick)
                "open_warm":   [(_("Thought you would want to know."),), (_("I figured you should hear it from me."),)],
                "open_secret": [(_("Delete this after you read it."),), (_("Don't answer if %(pn)s is around you."),)],
                "more":        [(_("Okay, I have to go. I'll keep you posted."),), (_("That's all for today. Talk soon."),)],
                "money":       [(_("You didn't have to. Thank you. It really helps."),), (_("Thank you. I'll put it toward the baby's things."),)],
                "money_broke": [(_("It's okay. Asking was enough."),)],
                "busy":        [(_("Oh. Okay."),), (_("Right. Sure."),)],
            },
            "gwen":  {"open_warm": [(_("That's your baby bulletin. Don't get used to it."),)],
                      "money":     [(_("Look at you, being responsible. Thanks. Really."),)]},
            "rogue": {"open_warm": [(_("Just felt like tellin' you, sugar."),)],
                      "money":     [(_("Well, ain't you sweet. Thank you, sugar."),)]},
            "ntw":   {"open_warm": [(_("There. You're updated."),)],
                      "money":     [(_("...Thanks. I'll use it well."),)]},
            "tenny": {"open_warm": [(_("I-I just wanted to share it with someone. With you."),)],
                      "money":     [(_("T-thank you! Grandpa says every bit helps."),)]},
        },
        "away_text": {
            "_default": {
                "open_warm":   [(_("We're both fine. The baby is tiny and perfect."), _("I'll be back on campus in a few days."))],
                "open_secret": [(_("We're both fine. I can't text much, %(pn)s never leaves my side."), _("I'll be back in a few days. Don't write back."))],
                "glad":        [(_("That means a lot. More than you know."),), (_("Okay. I'll tell you everything when I'm back."),)],
                "ok":          [(_("Will do."),)],
            },
            "gwen":  {"open_warm": [(_("Still alive. Both of us. The baby has my lungs, unfortunately for everyone here."), _("Back in a few days. Try not to burn the campus down."))]},
            "rogue": {"open_warm": [(_("We're both doin' fine, sugar. This baby is the prettiest thing I ever saw."), _("Back on campus in a few days. Miss me a little, will ya?"))]},
            "ntw":   {"open_warm": [(_("We're fine. Both of us. The baby is small and loud."), _("Back in a few days."))]},
            "tenny": {"open_warm": [(_("W-we're both okay! The baby is so small. Grandpa cried. I cried too."), _("I'll be back in a few days. I-I miss campus."))]},
        },
        "money_react": {
            "_default": {
                "open_thanks": [(_("The money came through. Thank you."),), (_("Got the support. It helps more than you think."),)],
                "open_cold":   [(_("Got the money."),), (_("Payment received. That's all."),)],
                "open_red":    [(_("The support came through. Just don't sink yourself, okay? Tell me if it gets tight."),),
                                (_("I got the money. Are you doing okay? Be honest with me."),)],
            },
            "gwen":  {"open_thanks": [(_("Money landed. Look at us, being functional adults."),)], "open_cold": [(_("Paid. Noted."),)]},
            "rogue": {"open_thanks": [(_("Money came through, sugar. Thank you kindly."),)],        "open_cold": [(_("Money's here. That's all I got to say."),)]},
            "ntw":   {"open_thanks": [(_("Got it. Thanks."),)],                                     "open_cold": [(_("Received."),)]},
            "tenny": {"open_thanks": [(_("T-the money arrived! Thank you so much."),)],             "open_cold": [(_("I-it arrived. Thanks."),)]},
        },
    }
    # Her auto-reply when he opens her chat during the week away (phone_messaging.rpy phone_open_chat)
    _CHILD_AWAY_AUTOREPLY = {
        "_default": [_("I'm with my family right now. The baby... everything happened so fast. I can't talk. I'll let you know when I'm back.")],
        "gwen":     [_("Can't talk. Family, baby, chaos. I'll text you when I'm back.")],
        "rogue":    [_("Can't talk now, sugar. My hands are full, literally. I'll holler when I'm back.")],
        "ntw":      [_("Busy. Baby. I'll text when I'm back.")],
        "tenny":    [_("S-sorry, I can't talk right now! Everything is happening at once. I'll text you when I'm back.")],
    }

    def _child_phone_reachable(girl, away_ok=False):
        """She can text him this morning: he has her number, she is not with him (a text to somebody standing
        next to you reads wrong), not angry / sad. Away (her birth week) only for an event that says so."""
        if girl.gid not in getattr(store.Player, "phone_contacts", set()):
            return False
        # same guards as the neighbouring morning events (label Wait 6c / 6d) and as her own chat: an ex who has
        # not confronted him yet answers "Don't text me", and a girl with a catch / violation message pending
        # is about to send a very different text in the same thread
        if girl.is_ex_of_player() and not getattr(girl, "_ex_confrontation_done", False):
            return False
        if (getattr(girl, "_npc_catch_pending", False) or getattr(girl, "_npc_catch_msg_pending", False)
                or getattr(girl, "_ntr_violation_pending", False)):
            return False
        if girl.has_temp_status("angry") or girl.has_temp_status("sad") or girl.has_temp_status("unavailable"):
            return False
        if girl_is_away(girl):
            return away_ok
        if getattr(girl, "loc", None) == store.CurrentLocation or girl.gid in getattr(store, "_girls_were_with_player", set()):
            return False
        return True

    def _child_event_due(girl, ev_type):
        return store.Day >= (getattr(girl, "_child_event_next", None) or {}).get(ev_type, 0)

    def _child_ev_away_text_ok(girl):
        # once per birth, from the middle of her week away, only from a mother who still talks to him
        _back = getattr(girl, "_birth_return_day", 0)
        return (getattr(girl, "_giving_birth", False) and not getattr(girl, "_away_text_sent", False)
                and _back - 4 <= store.Day < _back and father_tone(girl) != "distant")

    def _child_ev_money_ok(girl):
        # the morning after the weekly charge, a mother that charge REALLY paid (not one who came back from the
        # birth after the tick, not one whose partner stood as the father yesterday); not the one who
        # commented last week unless she is the only one who can text this morning
        _paid = [_gid for _gid in getattr(store, "_child_support_paid", ())
                 if _gid in GIRL_BY_ID and girl_is_mother(GIRL_BY_ID[_gid]) and _child_phone_reachable(GIRL_BY_ID[_gid])]
        if store.Day % 7 != 1 or girl.gid not in _paid:
            return False
        return girl.gid != getattr(store, "_child_money_react_last", None) or len(_paid) == 1

    def _child_ev_news_ok(girl):
        # a distant mother does not volunteer baby talk (same rule as her chitchat)
        return girl_is_mother(girl) and mother_mood(girl) != "distant" and _child_event_due(girl, "baby_news")

    def _child_ev_away_text_picked(girl):
        girl._away_text_sent = True

    def _child_ev_money_picked(girl):
        store._child_money_react_last = girl.gid

    # (event, eligible(girl), chance per morning, (min, max) days before the next one for HER, away_ok, on_pick)
    # in priority order: what cannot wait comes first.
    _CHILD_EVENTS = (
        ("away_text",   _child_ev_away_text_ok, 1.0, (0, 0),  True,  _child_ev_away_text_picked),
        ("money_react", _child_ev_money_ok,     1.0, (0, 0),  False, _child_ev_money_picked),
        ("baby_news",   _child_ev_news_ok,      0.5, (7, 10), False, None),
    )

    def children_morning_pick():
        """The children event of this morning as (event, gid), or None. WRITES when it picks: the morning
        stamp, her cooldown for that event, the event's own marker. Called once per morning by label Wait."""
        if getattr(store, "_child_event_day", -1) == store.Day:
            return None
        for _ev, _ok, _chance, _cool, _away_ok, _on_pick in _CHILD_EVENTS:
            _cands = [_g for _g in ALL_GIRLS if _child_phone_reachable(_g, _away_ok) and _ok(_g)]
            renpy.random.shuffle(_cands)
            for _g in _cands:
                if renpy.random.random() > _chance:
                    continue
                store._child_event_day = store.Day
                _next = dict(getattr(_g, "_child_event_next", None) or {})
                _next[_ev] = store.Day + renpy.random.randint(*_cool)
                _g._child_event_next = _next
                if _on_pick is not None:
                    _on_pick(_g)
                print("[CHILDREN] morning event '%s' picked for %s (Day %d, next not before Day %d)" % (_ev, _g.gid, store.Day, _next[_ev]))
                return (_ev, _g.gid)
        return None

    def _child_event_tone(ev_type, girl):
        """Key of her OPENING script."""
        if ev_type == "money_react":
            # her mood first: the distant mother (the very player who ends up in the red) stays cold
            if mother_mood(girl) == "distant":
                return "open_cold"
            return "open_red" if store.Player.cash < 0 else "open_thanks"
        return "open_" + father_tone(girl)

    def _child_event_script(ev_type, girl, key):
        """One script of her pool (per key fallback), every message translated and formatted."""
        _script = renpy.random.choice(girl_pool(_CHILD_EVENT_LINES[ev_type], girl, ev_type, key=key))
        return [_format_partner_line(girl, _m) for _m in _script]

    def child_event_open(ev_type, girl):
        """Her opening messages and his choices: {"lines": [...], "choices": [(caption, reply key), ...]}.
        Baby news open with a line about the baby (baby_line_pick WRITES her memory of lines)."""
        _key = _child_event_tone(ev_type, girl)
        _lines = _child_event_script(ev_type, girl, _key)
        if ev_type == "baby_news":
            _lines = [_tl(baby_line_pick(girl, texting=True))] + _lines
        _choices = [(_tl(_caption), _reply) for _reply, _caption in _CHILD_EVENT_CHOICES[ev_type]]
        print("[CHILDREN] event '%s' %s: opening=%s choices=%d" % (ev_type, girl.gid, _key, len(_choices)))
        return {"lines": _lines, "choices": _choices}

    def child_event_reply(ev_type, girl, picked):
        """His answer. WRITES: the money he sends, his involvement. Returns {"player": what he wrote or None,
        "chip": system chip or None, "lines": her closing messages, "stats": for Change_Status}."""
        _captions = dict(_CHILD_EVENT_CHOICES[ev_type])
        _reply = picked if picked in _captions else "ignored"
        if (ev_type, _reply + "_secret") in _CHILD_EVENT_EFFECTS and father_tone(girl) == "secret":
            _reply = _reply + "_secret"
        _fx = _CHILD_EVENT_EFFECTS.get((ev_type, _reply), {})
        _chip = None
        _cost = _fx.get("cost", 0)
        if _cost:
            if store.Player.spend_cash(_cost):
                _chip = _tl_fmt(_("You sent her $%d."), _cost)
            else:
                _chip = _tl_fmt(_("You don't have $%d to send."), _cost)
                _reply = _reply + "_broke"
                _fx = _CHILD_EVENT_EFFECTS.get((ev_type, _reply), {})
        _amount = _fx.get("involvement", 0)
        _now = father_involvement(girl)
        if _amount < 0 and _now >= _FATHER_INVOLVEMENT_WARM:
            # a warm father cools down TO the warm line, never below it: "distant" is the voice of the man who
            # denied the child ("You said it wasn't yours"), and brushing off a text is not that. A father who
            # is already below the line (denied, fooled partner) takes the full cost.
            _amount = max(_amount, _FATHER_INVOLVEMENT_WARM - _now)
        if _amount:
            father_involvement_change(girl, _amount, "%s: %s" % (ev_type, _reply))
        _silent = _fx.get("silent", False)
        _lines = [] if (_silent or _fx.get("no_answer")) else _child_event_script(ev_type, girl, _reply)
        if _fx.get("baby_line"):
            _lines = [_tl(baby_line_pick(girl, texting=True))] + _lines
        _said = None if (_silent or picked not in _captions) else _tl(_captions[picked])
        print("[CHILDREN] event '%s' %s: he picked %r -> %s, involvement now %d" % (ev_type, girl.gid, picked, _reply, father_involvement(girl)))
        return {"player": _said, "chip": _chip, "lines": _lines, "stats": dict(_fx.get("stats", {}))}

    # ============================================================
    # INSTABOOK: her birth post (label Wait step 6i2, the convention of the "entered a relationship" post)
    # ============================================================
    # The baby never appears: the post is described, the caption is hers. "_default" for a girl with no pool.
    _CHILD_BIRTH_POST_CAPTIONS = {
        "_default": [_("Welcome to the world, little one.")],
        "gwen":     [_("New tiny human. Already louder than me.")],
        "rogue":    [_("My whole heart, right here.")],
        "ntw":      [_("Mine. Back off.")],
        "tenny":    [_("Hello, world! Love, the baby (and mom).")],
    }

    def child_birth_post_lines():
        """Narration lines of the birth posts that are due (translated), and those posts are consumed.
        With her NPC partner standing as the father she tags HIM (no gendered word: the partner can be a woman)."""
        _queue = list(getattr(store, "_child_birth_posts", None) or [])
        _due = [_p for _p in _queue if _p[1] <= store.Day]
        store._child_birth_posts = [_p for _p in _queue if _p[1] > store.Day]
        _lines = []
        for _gid, _day in _due:
            _g = GIRL_BY_ID.get(_gid)
            if _g is None or not girl_is_mother(_g):
                continue
            _caption = _tl(renpy.random.choice(girl_pool(_CHILD_BIRTH_POST_CAPTIONS, _g, "birth post")))
            _lines.append(_tl_fmt(_("You check Instabook. {b}%s{/b} posted a picture of a tiny hand wrapped around her finger. {i}%s{/i}"), _g.Name, _caption))
            _partner = getattr(_g, "_npc_partner_name", None)
            if child_husband_is_father(_g):
                _lines.append(_tl(_("She tagged her husband in it. The comments are full of congratulations for the happy couple.")))
            elif child_npc_is_father(_g) and _partner:
                _lines.append(_tl_fmt(_("She tagged {b}%s{/b} in it. The comments are full of congratulations for the two of them."), _partner))
            print("[CHILDREN] Instabook birth post of %s (queued for Day %d)" % (_gid, _day))
        return _lines

    # ============================================================
    # ACHIEVEMENTS (General/achievements.rpy: persistent, the Baby Eraser never takes them back)
    # ============================================================
    # (key, test(mothers)), least specific first: only the LAST banner of a batch stays on screen.
    # Checked at every birth and at every weekly charge (a save that already had children catches up there).
    _CHILD_ACHIEVEMENTS = (
        ("first_child",    lambda _m: len(_m) >= 1),
        ("two_cribs",      lambda _m: len(_m) >= 2),
        ("full_house",     lambda _m: len(_m) >= 2 and len(_m) >= len(pregnancy_candidates())),
        ("not_the_father", lambda _m: any((child_record(_g) or {}).get("official") in ("npc", "husband") for _g in _m)),
    )

    def child_achievements_check(reason=""):
        _mothers = player_mothers()
        for _key, _test in _CHILD_ACHIEVEMENTS:
            if _test(_mothers) and not is_achievement_unlocked(_key):
                print("[CHILDREN] achievement '%s' (%s, %d mother(s))" % (_key, reason, len(_mothers)))
                unlock_achievement(_key)

    # ============================================================
    # ASK HER: "How's the baby?" (talk_ask_question, interactions.rpy)
    # ============================================================
    # Mood of the answer: "warm" / "distant" / "secret" (mother_mood), "hush" (the fooled partner is on screen),
    # "thaw" (he denied the child and kept asking: the ask that makes her warm), "erased" (the Baby Eraser:
    # HE remembers a baby she never had). Pools: {gid: {mood: [lines]}}, fallback PER MOOD to "_default"
    # (girl_pool with key). A girl writes only the moods where her pool matters. Lines go through
    # _format_partner_line: partner placeholders are allowed, the baby is always "the baby" (no sex, no name).
    # After a warm / thaw / secret line she tells one thing about the baby (baby_line_pick).
    _CHILD_ASK_LINES = {
        "_default": {
            "warm": [
                _("Doing great. Growing so fast I can barely keep up."),
                _("Good. Really good. I called home this morning."),
            ],
            "distant": [
                _("Fine. Not that you cared before."),
                _("The baby is fine. Money is not the same as being there."),
                _("Why do you want to know? You made it clear it wasn't your problem."),
            ],
            "thaw": [
                _("...You keep asking. Okay. Maybe you do care, in your own way."),
            ],
            "secret": [
                _("Keep your voice down. As far as %(pn)s knows, the baby is %(poss)s."),
                _("Not so loud. %(Pn)s can never hear you ask me that."),
            ],
            "hush": [
                _("Not here. Not now."),
                _("We can talk about that another time."),
            ],
            "erased": [
                _("Baby? What baby? Are you feeling okay?"),
                _("I don't have a baby. That is a really strange thing to ask me."),
            ],
        },
        "gwen": {
            "warm": [
                _("Tiny, loud and already has my attitude. So, perfect."),
                _("Thriving. My family sends so many pictures my phone is begging for mercy."),
            ],
            "distant": [
                _("Oh, now you're curious? Cute."),
                _("Fine. No thanks to you."),
            ],
        },
        "rogue": {
            "warm": [
                _("Gettin' bigger every day, sugar. My aunt says the baby eats like a little horse."),
                _("Doin' just fine. I miss that little face somethin' fierce."),
            ],
            "distant": [
                _("The baby's fine. Ain't your concern though, is it? You said so yourself."),
                _("Funny. You didn't wanna know a thing back then."),
            ],
        },
        "ntw": {
            "warm": [
                _("Alive. Loud. Strong grip. I approve."),
                _("Good. Better than good. Don't make it weird."),
            ],
            "distant": [
                _("Fine. Next question."),
                _("You don't get to ask that like nothing happened."),
            ],
        },
        "tenny": {
            "warm": [
                _("R-really good! Grandpa says the baby is already the smartest one in the house."),
                _("S-so good. I get pictures every day. I look at them between classes."),
            ],
            "distant": [
                _("F-fine. The baby is fine."),
                _("Y-you said it wasn't yours. W-why are you asking now?"),
            ],
        },
    }
    _CHILD_ASK_LINES_MULTI = {
        "_default": {
            "warm": [
                _("The kids are good. The little one keeps the big one busy."),
                _("Good. Really good. Keeping up with two is wild, though."),
            ],
            "distant": [
                _("The kids are fine. Not that you'd know."),
                _("My kids don't need your pity. They needed a father."),
            ],
            "thaw": [
                _("...You keep asking about them. Maybe you do care after all."),
            ],
            "secret": [
                _("Keep your voice down. %(Pn)s can never know how many are yours."),
            ],
        },
        "gwen": {
            "warm": [
                _("Loud, messier, and twice the fun. My family is going insane."),
                _("Two of them now. Two! My mom says I owe her a vacation."),
            ],
        },
        "rogue": {
            "warm": [
                _("Both doin' just fine, sugar. My aunt's got her hands full."),
                _("Gettin' along like two peas in a pod. Mostly."),
            ],
        },
        "ntw": {
            "warm": [
                _("Both alive. Both loud. I call that a win."),
            ],
        },
        "tenny": {
            "warm": [
                _("T-they're great! Grandpa says two is easier because they entertain each other."),
            ],
        },
    }
    _CHILD_ASK_EXPR = {"warm": "smile", "distant": "annoyed", "thaw": "looking_down", "secret": "worried",
                       "hush": "nervous", "erased": "confused"}
    _CHILD_ASK_BABY_LINE = ("warm", "thaw", "secret")    # moods where she goes on to tell something about the baby
    _CHILD_ASK_LOVE = 3                                   # a warm answer, first ask of the Day
    _CHILD_ASK_INVOLVEMENT = 6                            # he asked: first ask of the Day (10 -> 40 takes 5 asks)

    def child_ask_available(girl):
        """The question is in the menu for a mother, and for a girl whose child only HE remembers (Baby Eraser).
        Not while she carries a NEW pregnancy he knows about (the Eraser makes her fertile again): "What baby?"
        from a girl with a belly he was told about reads as a bug. After that birth she is a mother again."""
        if girl_is_mother(girl):
            return True
        return getattr(girl, "_child_forgotten", False) and not getattr(girl, "_pregnancy_known", False)

    def child_ask_mood(girl):
        if not girl_is_mother(girl):
            return "erased"
        if mother_hush(girl):
            return "hush"
        return mother_mood(girl)

    def child_ask_resolve(girl):
        """Her answer to "How's the baby?". WRITES: the day he asked, his involvement (first ask of the Day),
        the memory of baby lines. Returns {"mood", "expr", "lines" (English source, in order), "stats"}."""
        _mood = child_ask_mood(girl)
        _asked_before = getattr(girl, "_baby_asked_day", 0) > 0
        _first = getattr(girl, "_baby_asked_day", 0) != store.Day
        _stats = {}
        if _mood in ("warm", "distant", "secret") and _first:
            girl._baby_asked_day = store.Day
            _now = father_involvement_change(girl, _CHILD_ASK_INVOLVEMENT, "asked about the baby")
            # "...You keep asking." needs a man who really asked before: from 35 (Choice 4 after her partner
            # left, or no answer on record) the very first ask already crosses the line, and that one stays cold
            if _mood == "distant" and _now >= _FATHER_INVOLVEMENT_WARM and _asked_before:
                _mood = "thaw"
            elif _mood == "warm":
                _stats["Love"] = _CHILD_ASK_LOVE
        _ask_pool = _CHILD_ASK_LINES_MULTI if getattr(girl, "_children_count", 0) >= 2 and _mood not in ("hush", "erased") else _CHILD_ASK_LINES
        _cands = _child_lines_for_count(girl_pool(_ask_pool, girl, "ask about the baby", key=_mood), girl)
        if not _cands:
            # every line of her own multi pool says "two": the shared pool answers for a mother of three or more
            _cands = _child_lines_for_count(_ask_pool["_default"][_mood], girl) or list(_ask_pool["_default"][_mood])
        _lines = [renpy.random.choice(_cands)]
        if _mood in _CHILD_ASK_BABY_LINE:
            _lines.append(baby_line_pick(girl))
        print("[CHILDREN] %s asked about the baby: mood=%s first_today=%s involvement=%d stats=%s" % (
            girl.gid, _mood, _first, father_involvement(girl), _stats))
        return {"mood": _mood, "expr": _CHILD_ASK_EXPR[_mood], "lines": _lines, "stats": _stats}

    # ============================================================
    # QA
    # ============================================================
    def child_debug_birth(girl, age_days=30, response="supportive", claimed=False):
        """Console: child_debug_birth(Gwen, age_days=30, response="deny", claimed=False). Makes her a mother
        through the REAL path (pregnancy_return_apply -> child_register_birth). A real birth takes 65 or
        130 game days plus 7 away: nothing after the birth is testable without this.
        claimed=True needs an NPC partner."""
        girl._player_pregnancy_response = response
        girl._npc_paternity_claimed = bool(claimed) and girl.has_npc_partner()
        girl._pregnancy_known = True
        girl._giving_birth = True
        # a save younger than the age asked for: the oldest child this save can have (born on Day 1), not the
        # "return day lost" fallback of child_register_birth
        _age = max(0, min(int(age_days), store.Day - 1))
        girl._birth_return_day = store.Day - _age + _BIRTH_AWAY_DAYS
        pregnancy_return_apply(girl)
        return child_debug(girl)

    def child_debug_age(girl, age_days):
        """Console: child_debug_age(Gwen, 90) moves her child's birth day."""
        _rec = child_record(girl)
        if _rec is None:
            return "%s has no child" % girl.Name
        _rec["born"] = max(1, store.Day - int(age_days))
        return child_debug(girl)

    def child_debug(girl=None):
        """Console: child_debug(Gwen), or child_debug() for every mother."""
        if girl is None:
            return "\n".join(child_debug(_g) for _g in player_mothers()) or "no children"
        _out = "%s: children=%d age=%s tier=%s fooled_partner=%s support=$%d records=%s" % (
            girl.Name, getattr(girl, "_children_count", 0), child_age_days(girl), child_age_tier(girl),
            child_father_fooled(girl), child_support_due(girl), getattr(girl, "_children", None))
        print("[CHILDREN] debug " + _out)
        return _out

# ============================================================
# ASK HER: "How's the baby?"
# ============================================================
label _ask_about_baby(girl):
    if getattr(girl, "_children_count", 0) >= 2:
        $ Say_Player(_("How are the kids?"))
    else:
        $ Say_Player(_("How's the baby?"))

    $ _ab = child_ask_resolve(girl)
    $ set_scene_expression(girl, _ab["expr"])
    python:
        # _format_partner_line translates, and fills the partner placeholders of the "secret" lines
        for _ab_line in _ab["lines"]:
            Say_Line(girl, _format_partner_line(girl, _ab_line))
        for _ab_stat, _ab_amt in _ab["stats"].items():
            Change_Status(girl, _ab_stat, _ab_amt)
    $ set_scene_expression(girl, "normal")
    return

# ============================================================
# MORNING PHONE EVENT (label Wait step 6k, at most one per morning: children_morning_pick)
# ============================================================
label _child_morning_event(ev_type, girl):
    play sound "audio/Notification.mp3" noloop
    $ Narration(_("Your phone buzzes. Someone sent you a message."))

    $ _cme = child_event_open(ev_type, girl)
    call _child_phone_lines(girl, _cme["lines"]) from _call_child_event_open

    $ _cme_closed = False
    if _cme["choices"]:
        call screen phone_chat_screen(girl, choices=_cme["choices"])
        $ _cme_closed = _return in ("close", "home")      # Back / Home at the choices: he already put the phone away
        $ _cme_r = child_event_reply(ev_type, girl, _return)
        if _cme_r["player"]:
            $ phone_add_msg(girl.gid, "player", _cme_r["player"])
        if _cme_r["chip"]:
            $ phone_add_msg(girl.gid, "system", _cme_r["chip"], "system")
        call _child_phone_lines(girl, _cme_r["lines"]) from _call_child_event_reply
        python:
            for _cme_stat, _cme_amt in _cme_r["stats"].items():
                Change_Status(girl, _cme_stat, _cme_amt)

    # he closes the phone himself (a text that shuts after 1.5 s cannot be read), as in _sugar_daddy_event
    if not _cme_closed:
        call screen phone_chat_screen(girl, choices=[])
    return

label _child_phone_lines(girl, lines):
    # her messages, one typing pause each (the texts arrive translated and formatted)
    $ _cpl_i = 0
    while _cpl_i < len(lines):
        call _phone_typing(girl, choices=[]) from _typing_child_lines
        $ phone_add_msg(girl.gid, girl.gid, lines[_cpl_i])
        $ _cpl_i += 1
    return

init 1 python:

    # set_scene_expression() silently shows a neutral face for an unknown name: catch typos at startup
    # (Core_Images.rpy loads after children.rpy, hence init 1). Same log line the lint check greps for.
    def _child_validate_expressions():
        _valid = POSE_EXPRESSIONS.get("standing", {})
        _bad = sorted(_e for _e in set(_CHILD_ASK_EXPR.values()) if _e not in _valid)
        _bad += sorted("mood without a face: " + _m for _v in _CHILD_ASK_LINES.values() for _m in _v if _m not in _CHILD_ASK_EXPR)
        if _bad:
            print("[CHILDREN] INVALID expression names (will render neutral): %s" % ", ".join(_bad))
        return _bad

    _child_validate_expressions()
