# ============================================================
# shion_pregnancy.rpy... a married girl's pregnancy by him (docs/plan_shion.md, Shion's pregnancy, D4 lifted)
#
# THE PILL: she holds her own pill until her turn (GIRLS_CONFIG "pill_own", girl_holds_her_pill, pregnancy.rpy):
#   before her stage 3 she can't get pregnant at all; from it he can ask her to stop ("He'll think it's his").
# THE FATHER: the player is always the biological father (the game has no other). A married girl whose husband
#   is a contact of his (girl_husband: Shion -> Dad) ALWAYS names her husband: the child is officially his
#   (pregnancy_husband, children.rpy: child_husband_is_father / "official": "husband" / raised by him / the
#   fooled tone "secret"). He never learns the truth; if the calls left him suspicious (husband.suspicion >=
#   PREG_HUSBAND_DOUBT) his birth text has an ironic doubt.
# HER VOICE: PREG_OWN_LINES[gid] (the discovery scene, her answer to each of his choices, her husband lie) is read
#   by label _pregnancy_discovery and the choice labels (pregnancy_discovery.rpy); her lines in the shared
#   pregnancy / children tables are merged below (init 5).
# HER HUSBAND'S TEXTS (DAD_TEXTS, shion_family.rpy): the news the morning she tells him, the labor, home with
#   the baby (the doubt goes there).
# ============================================================

init python:

    PREG_HUSBAND_DOUBT = 40     # husband suspicion (shion_netori.rpy calls) from which his "home with the baby" text doubts

    def pregnancy_husband(girl):
        """Her husband, who will be told the child is his: a married girl with a husband among his contacts."""
        return girl_husband(girl) if girl_wears_ring(girl) else None

    def husband_present(girl):
        """Her husband is in the room with them now (she won't say a word about whose baby it is)."""
        return pregnancy_husband(girl) is not None and husband_in_room(girl)

    # Her voice in the discovery: gid -> key -> [(face, line)] ("discovery" / "discovery_wanted" = her scene;
    # "supportive" / "breeding" / "deny" = her answer to his choice, with "love" / "obed" / "mood" / "mood_days";
    # "lie_<response>" = what she will tell her husband). Face None = narration.
    PREG_OWN_LINES = {
        "shion": {
            "discovery": [
                ("serious", _("I'm late. I'm never late. Not for meetings, not for anything.")),
                ("smug", _("Three tests this morning. All positive. So don't bother asking if I'm sure.")),
                ("serious", _("And before you ask: it's yours. Your father hasn't touched me in months.")),
                ("smirk", _("Breathe, boy. I've already decided how this ends. I always do.")),
            ],
            "discovery_wanted": [
                ("smug", _("Three tests this morning. All positive.")),
                ("sexy", _("Don't look so shocked. You've been trying hard enough for it.")),
                ("smirk", _("Your baby, in your father's wife. ...I've never wanted anything this badly.")),
            ],
            "supportive": {
                "lines": [
                    ("smug", _("Look at you. Trying so hard to be a man about it.")),
                    ("embarrassed", _("...Good. Keep that face. I'm going to need it.")),
                ],
                "love": 40,
            },
            "breeding": {
                "lines": [
                    ("sexy", _("You put a baby in your father's wife, and you want to do it AGAIN?")),
                    ("smirk", _("...God, you're perfect. Fine. As many times as you want.")),
                ],
                "love": 30, "obed": 15, "mood": None, "mood_days": 0,
            },
            "deny": {
                "lines": [
                    ("smirk", _("Not yours? Whose, then? Your father's?")),
                    ("smug", _("...Fine. Then it's his. That was always the plan, boy. You just made it easier.")),
                ],
                "love": -20, "mood": None, "mood_days": 0,
            },
            # what she will tell her husband, by his answer
            "lie_supportive": [
                ("smirk", _("To everyone else, it's your father's. He'll be the proudest idiot in the city.")),
                ("serious", _("He'll never know. Not from me. Not from you.")),
            ],
            "lie_breeding": [
                ("sexy", _("Your father is going to throw a party. For YOUR baby.")),
                ("smirk", _("I can't wait to watch him cry over it.")),
            ],
            "lie_deny": [
                ("serious", _("He'll paint the nursery himself. He'll never know the difference.")),
            ],
        },
    }

    def preg_own_lines(girl, key):
        """Her own pregnancy lines for key (PREG_OWN_LINES), or None."""
        return (PREG_OWN_LINES.get(getattr(girl, "gid", None)) or {}).get(key)

# Her own discovery scene (the per-girl chain and _PREG_DISCOVERY_WANTED of _pregnancy_discovery)
label _pregnancy_discovery_own(girl):
    $ _pdo_key = "discovery_wanted" if girl.has_trait("pregnancy_fetish") and preg_own_lines(girl, "discovery_wanted") else "discovery"
    call _preg_own_say(girl, preg_own_lines(girl, _pdo_key)) from _call_preg_own_say_disc
    return

# Her answer to his choice (supportive / breeding / deny): plays her lines, leaves the numbers in _preg_own_out
label _preg_own_react(girl, key):
    python:
        _preg_own_out = dict(preg_own_lines(girl, key) or {})
        print("[PREGNANCY] %s: her own answer to '%s' (%s)" % (girl.gid, key, dict((k, v) for k, v in _preg_own_out.items() if k != "lines")))
    call _preg_own_say(girl, _preg_own_out.get("lines")) from _call_preg_own_say_react
    return

# A married girl tells him what she will tell her husband (after his choice); her husband texts the news
label _pregnancy_husband_claim(girl):
    python:
        _phc_resp = getattr(girl, "_player_pregnancy_response", None) or "supportive"
        _phc_lines = preg_own_lines(girl, "lie_" + _phc_resp) or preg_own_lines(girl, "lie_supportive")
        _phc_h = pregnancy_husband(girl)
        if _phc_h is store.Dad:
            store._dad_text_pending = "baby_news"
        print("[PREGNANCY] %s: the baby is officially %s's (his answer %s)" % (girl.gid, getattr(_phc_h, "gid", "?"), _phc_resp))
    call _preg_own_say(girl, _phc_lines) from _call_preg_own_say_lie
    return

label _preg_own_say(girl, lines):
    $ _pos = list(lines or [])
    while _pos:
        $ _pos_face, _pos_line = _pos.pop(0)
        if _pos_face is None:
            $ Narration(_pos_line)
        else:
            $ set_scene_expression(girl, _pos_face)
            $ Say_Line(girl, _pos_line)
    return

# ============================================================
# Her lines in the shared pregnancy / children tables (each falls back to "_default" without them)
# ============================================================
init 5 python:

    _PREG_DISCOVERY_WANTED["shion"] = "_pregnancy_discovery_own"

    _PREG_FIN_RICH_TALK["shion"] = [
        ("serious", _("Money is the one thing this child will never lack. My money. Not yours, not your father's.")),
        ("smirk", _("Keep your allowance, boy. What I need from you isn't in your wallet.")),
    ]

    _PREG_BIRTH_TEXTS["shion"] = [
        _("My water broke in the middle of a board meeting. Of course it did."),
        _("Your father is driving me to the hospital. He's more nervous than I am."),
        _("I'll be gone for a week. Behave."),
    ]
    _PREG_RETURN_TEXTS["shion"] = [
        _("I'm home. The baby too. Your father hasn't slept in days."),
        _("He keeps saying the baby has his nose. I keep letting him."),
        _("Come see your little... sibling. Soon."),
    ]

    _PREG_CHITCHAT_EARLY["shion"] = [
        _("I threw up in the boardroom bathroom this morning. Twice. Nobody will ever know."),
        _("Your father keeps rubbing my back. As if he did anything to deserve it."),
        _("I can't stand the smell of my own perfume anymore. A thousand dollars a bottle, and it makes me sick."),
        _("I fell asleep in a meeting. Me. Your child is already ruining my reputation."),
    ]
    _PREG_CHITCHAT_LATE["shion"] = [
        _("It kicked. Right in the middle of a call with investors. Your child has your manners."),
        _("Your father wants to name it after his grandfather. I let him think he gets a vote."),
        _("My back is killing me. Rub it. ...What? He's at work."),
        _("I haven't seen my own shoes in weeks. I pay someone to tie them now."),
    ]
    _PREG_CHITCHAT_POSTPARTUM["shion"] = [
        _("The nanny says the baby slept through the night. Your father didn't. He kept checking on it."),
        _("Your father keeps saying the baby has his nose. I keep letting him."),
        (_("The baby grabbed my wedding ring today and wouldn't let go. Fitting."), "baby", "toddler"),
        _("Every time your father holds the baby, I think about you. ...Don't let it go to your head."),
    ]
    _PREG_CHITCHAT_POSTPARTUM_MULTI["shion"] = [
        _("Two of yours, both with his name. Your father is the happiest man alive."),
        _("I gave the nanny a raise. Two babies, one secret. She earns it."),
    ]

    rod_lines["shion"]["pregnancy_casual_worry"] = [
        _("If this child comes out with your face, your father will start asking questions."),
        _("My doctor says I need to slow down. I have never slowed down in my life."),
    ]
    rod_lines["shion"]["pregnancy_casual_positive"] = [
        _("I never wanted children. ...I want this one."),
        _("Your father bought a crib. I picked a better one."),
    ]

    _CHILD_EVENT_LINES["baby_news"]["shion"] = {
        "open_secret": [(_("Your father is asleep. Delete this when you're done."),),
                        (_("Don't you dare reply while he's home."),)],
        "more":        [(_("That's all for today. He's waking up."),)],
        "money":       [(_("Money? From you? Keep it, boy. This baby will never want for anything. ...But it's sweet."),)],
        "busy":        [(_("Hmmph. Busy. Like father, like son."),)],
    }
    _CHILD_EVENT_LINES["away_text"]["shion"] = {
        "open_secret": [(_("We're both fine. Your father hasn't left my side for a second."), _("I'll be home in a few days. Do NOT text back."))],
    }
    _CHILD_AWAY_AUTOREPLY["shion"] = [_("Not now. Your father is right here. I'll message you when I'm home.")]
    _CHILD_BIRTH_POST_CAPTIONS["shion"] = [_("Welcome to the family, little one. Your father and I couldn't be happier.")]
    _CHILD_ASK_LINES["shion"] = {
        "secret": [
            _("Lower your voice. As far as your father knows, the baby is his."),
            _("The baby is wonderful. It has your eyes. He'll never notice."),
        ],
        "hush": [
            _("Not here. Your father is right there."),
            _("Later. Not in this house."),
        ],
    }
    _CHILD_ASK_LINES_MULTI["shion"] = {
        "secret": [
            _("Keep your voice down. Your father can never know how many of them are yours."),
        ],
    }

    DAD_TEXTS["baby_news"] = [
        _("Son! Big news! Shion is pregnant!"),
        _("You're going to be a big brother! At my age! Can you believe it?"),
    ]
    DAD_TEXTS["baby_labor"] = [
        _("Shion is in labor! I'm at the hospital with her."),
        _("Next time I text you, you'll be a big brother!"),
    ]
    DAD_TEXTS["baby_home"] = [
        _("We're home with the baby! Healthy and loud. Shion was amazing."),
        _("Come meet your little sibling, kid. You're a big brother now."),
    ]
    DAD_TEXTS["baby_home_doubt"] = [
        _("We're home with the baby! Healthy and loud."),
        _("Funny thing, the nurse said the baby has your eyes, kid. Must run in the family."),
    ]
