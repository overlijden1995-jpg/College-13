# ============================================================
# count_slaps.rpy... "Make her count" (tease.rpy, submissive girls only; tester idea 2026-10-11, the author's go)
#
# After the tease, every ass spank (SpankHer) and every face slap (SpankHer in cowgirl, SexScene_Slap in hj / bj / tj)
# of the scene makes her call the running number out loud. Her number REPLACES the spank reaction line (the face slap
# keeps its short moan, the number comes after it). The voice is the trait:
#   - hardcore_sex: she counts happily, asks for the next one;
#   - any other submissive: resigned; from COUNT_SLAPS_AGITATED_AT in a row with nothing else in between (the Round
#     counter: a slap costs 1, anything else in between moves it further) she asks for something else, Love down;
#   - her orgasm (GirlCumming) makes her lose the count: the next number is uncertain and may be wrong by one
#     (a nerd freaks out about it; a hardcore girl asks to start over).
# A position switch (sub_event_reset) and the scene cleanup end the count.
# ============================================================

default _count_slaps = None   # {"gid", "n", "lost", "streak", "round"} while she counts, else None

init python:

    COUNT_SLAPS_AGITATED_AT = 6         # a submissive without hardcore: from this many in a row she asks for something else
    COUNT_SLAPS_AGITATED_LOVE = -2      # each number past that point
    COUNT_SLAPS_LOST_WRONG_CHANCE = 0.5 # after her orgasm: the number she says is off by one this often
    COUNT_SLAPS_OBED = 1                # every number she says: Obed (then her trait multiplier)
    # the scenes whose control menu has a spank or a slap next to the tease (full nelson, footjob and rimjob have none)
    COUNT_SLAPS_SCENES = ("reverse_cowgirl", "reverse_cowgirl_anal", "doggy", "anal", "laying_down", "laying_anal",
                          "cowgirl", "hj", "bj", "tj")

    # %d = the number (every %d of a line is the same number)
    COUNT_SLAPS_LINES = {
        "count": {
            "hardcore_sex": [
                _("%d! Again!"),
                _("Ahh! %d! Harder, please!"),
                _("%d... don't stop. Please don't stop."),
                _("Hah! %d! I can take more!"),
                _("%d! I love that you make me say it."),
                _("Nngh... %d. Keep going. Please keep going."),
            ],
            "nerd": [
                _("%d. That's exact. I'm keeping track."),
                _("Ah! %d... I'm sure of it. %d."),
                _("%d. I won't lose the number. I don't lose numbers."),
                _("Nnh... %d. Still counting. Still right."),
            ],
            "_default": [
                _("...%d."),
                _("%d. ...Yes."),
                _("Ah! %d."),
                _("%d. Thank you."),
                _("Nnh... %d. I'm counting. I'm still counting."),
                _("%d... like you told me."),
            ],
        },
        # a submissive without hardcore, too many in a row with nothing else
        "agitated": {
            "_default": [
                _("...%d. Can we... do something else now? Please?"),
                _("%d. I'm still counting. I just... could you hold me a second instead?"),
                _("%d... I'll keep counting if you want me to. I'd rather you didn't."),
                _("%d. ...Please. Something else. Anything else."),
            ],
        },
        # the first number after her orgasm: she lost the count
        "lost": {
            "hardcore_sex": [
                _("Mmm... %d? I stopped counting when I came. %d. Make me start over."),
                _("Hah... %d... or was it? I lost it when you made me cum. I don't care. Again."),
            ],
            "nerd": [
                _("I lost count. I LOST COUNT. That never happens. It's... %d. It has to be %d."),
                _("No no no, I had it, it was... %d? I don't lose numbers. I don't."),
                _("...%d? I think? I'm sorry. I'm so sorry. I had it until you made me..."),
            ],
            "_default": [
                _("...%d? I... I think it's %d. I'm sorry, I lost it for a second."),
                _("Hnn... %d. Maybe. I couldn't think when you made me cum."),
                _("%d... I'm not sure anymore. Please don't be mad. %d."),
            ],
        },
    }
    _COUNT_SLAPS_VOICE = ("hardcore_sex", "nerd")   # the first of her traits with a pool, else "_default"

    def count_slaps_active(girl=None):
        """She is counting this scene (the girl, when given, must be the one who was told to)."""
        _c = getattr(store, "_count_slaps", None)
        if not _c:
            return False
        return girl is None or _c.get("gid") == getattr(girl, "gid", None)

    def count_slaps_start(girl):
        """The tease landed: from now on every spank / slap of the scene gets its number."""
        store._count_slaps = {"gid": girl.gid, "n": 0, "lost": False, "streak": 0, "round": getattr(store, "Round", 0)}
        print("[COUNT_SLAPS] %s starts counting" % girl.gid)

    def count_slaps_reset(why=""):
        """A position switch (sub_event_reset) or the scene cleanup: the count is over."""
        if getattr(store, "_count_slaps", None):
            print("[COUNT_SLAPS] %s stops counting at %d (%s)" % (store._count_slaps["gid"], store._count_slaps["n"], why))
        store._count_slaps = None

    def count_slaps_orgasm(girl):
        """GirlCumming: the girl who counts just came: she loses the count (her next number is uncertain)."""
        if count_slaps_active(girl):
            store._count_slaps["lost"] = True
            print("[COUNT_SLAPS] %s lost the count at %d (orgasm)" % (girl.gid, store._count_slaps["n"]))

    def _count_slaps_pool(girl, moment):
        _table = COUNT_SLAPS_LINES[moment]
        for _t in _COUNT_SLAPS_VOICE:
            if _t in _table and girl.has_trait(_t):
                return _table[_t]
        return _table["_default"]

    def count_slaps_say(girl, face=False):
        """A spank / slap landed on the girl who counts: she says the number. Returns True when she spoke (SpankHer
        skips its own reaction line then). False = she is not counting (or cannot speak: a BJ with his hands on her head)."""
        if not count_slaps_active(girl):
            return False
        if getattr(store, "bj_forcing", False) and getattr(store, "_bj_girl", None) is girl:
            return False
        _c = store._count_slaps
        _c["n"] += 1
        _n = _c["n"]
        # "in a row": a slap costs 1 Round; anything else between two slaps moves the counter further
        _round = getattr(store, "Round", 0)
        _c["streak"] = _c["streak"] + 1 if _round - _c["round"] <= 1 else 1
        _c["round"] = _round
        _hc = girl.has_trait("hardcore_sex")
        _said = _n
        if _c["lost"]:
            _c["lost"] = False
            _moment = "lost"
            if renpy.random.random() < COUNT_SLAPS_LOST_WRONG_CHANCE:
                _said = max(1, _n + renpy.random.choice((-1, 1)))
        elif not _hc and _c["streak"] >= COUNT_SLAPS_AGITATED_AT:
            _moment = "agitated"
            Change_Status(girl, "Love", COUNT_SLAPS_AGITATED_LOVE)
        else:
            _moment = "count"
        _line = _tl(renpy.random.choice(_count_slaps_pool(girl, _moment)))
        _line = _line % ((_said,) * _line.count("%d")) if "%d" in _line else _line
        Change_Status(girl, "Obed", COUNT_SLAPS_OBED)
        print("[COUNT_SLAPS] %s says %d (real %d, %s, streak %d, face=%s)" % (girl.gid, _said, _n, _moment, _c["streak"], face))
        Say_Line(girl, _line)
        return True
