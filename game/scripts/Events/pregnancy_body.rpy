## pregnancy_body.rpy: her body changes. Three moments that open the next conversation with her.
##   "changing"   progression stage 2 (small bump, visual stage 1): she notices her body changing.
##                No player reaction.
##   "looks"      progression stage 3 (full belly, visual stage 2): she asks how she looks, he answers.
##   "procedure"  back from her LAST birth: the delivery was complicated, the doctor recommended an IUD
##                for a couple years to stabilize (pregnancy.rpy, "THE PROCEDURE"). She tells him; the trait is revealed.
## Each plays once per pregnancy, at the top of talk_main (interactions.rpy). Text only, so they also play
## in Lite mode. Pools are per girl; a girl with no pool here uses "_default".

init python:

    # moment -> first stage it plays at, LATEST FIRST (stage = _preg_body_stage). If he never talked to her
    # during stage 2, the stage 3 moment plays and the earlier one is dropped: "my body is starting to
    # change" makes no sense any more with a full belly.
    _PREG_BODY_MOMENTS = (("procedure", 4), ("looks", 3), ("changing", 2))
    # progression stages stop at 3: this one means "back from the birth, procedure done"
    _PREG_BODY_STAGE_AFTER_BIRTH = 4

    # "%s" in a narration = her name.
    _PREG_BODY_CHANGING = {
        "gwen": {
            "narr": _("%s tugs at the hem of her top, frowning at it like it personally betrayed her."),
            "lines": [
                ("bemused", _("Okay, so... my clothes have started a rebellion. Nothing fits the way it did last month.")),
                ("looking_down", _("My chest hurts, my jeans hate me, and I swear there's a bump now. A small one. But it's there.")),
                ("smirk", _("I keep catching myself in the mirror and going 'huh'. It's weird watching your own body do stuff without asking.")),
            ],
        },
        "rogue": {
            "narr": _("%s smooths a hand down her stomach without seeming to notice she's doing it."),
            "lines": [
                ("shy", _("Sugar, I've got to tell somebody... my body's changing. I can feel it.")),
                ("looking_down", _("My tops are getting tight up here, and there's this little curve starting down here.")),
                ("smile", _("It ain't much yet. But every morning I look, and it's a little more real.")),
            ],
        },
        "ntw": {
            "narr": _("%s yanks her top down for the third time in a minute, glaring at nothing."),
            "lines": [
                ("annoyed", _("My body is doing things. I did not authorize any of it.")),
                ("grimace", _("Everything is tighter. My chest is sore. And there's a bump. An actual bump.")),
                ("angry", _("I did fifty sit-ups this morning out of spite. It did not care.")),
            ],
        },
        "tenny": {
            "narr": _("%s keeps her arms crossed over her stomach, then seems to realize it and drops them."),
            "lines": [
                ("nervous", _("I-I think my body is starting to change... I measured. Twice.")),
                ("embarrassed", _("My bras don't fit right anymore, and my tummy is... rounder. Just a little.")),
                ("shy", _("I read that it's completely normal at this point. It still feels strange to watch it happen to me.")),
            ],
        },
        "_default": {
            "narr": _("%s rests a hand on her stomach for a second, almost without noticing."),
            "lines": [
                ("looking_down", _("My body's starting to change. I can see it now.")),
                ("thinking", _("My clothes fit differently, and there's a small bump that wasn't there before.")),
                ("smile", _("It's strange. It makes all of this feel a lot more real.")),
            ],
        },
    }

    # Gwen finds it funny and blames him as a joke. Rogue never pictured herself like this. NTW is angry and
    # confused: no sports, clumsy. Tenny is insecure. "replies" are keyed by his answer (label menu below).
    _PREG_BODY_LOOKS = {
        "gwen": {
            "narr": _("%s turns sideways, hands framing her belly like she's presenting a prize on a game show."),
            "lines": [
                ("laugh", _("Look at this. LOOK at it. I can balance a cup on here now. I tried. It works.")),
                ("smirk", _("I went from 'mysterious goth girl' to 'goth girl who swallowed a bowling ball'. Honestly? It's kind of hilarious.")),
                ("annoyed", _("This is your fault, by the way. You did this to me, you absolute menace.")),
            ],
            "ask": ("sly", _("So be honest. How do I look? Choose your words carefully. I can't see my feet, but I can still kick.")),
            "replies": {
                "sweet": [("embarrassed", _("Ugh. Don't be sincere, I wasn't ready for sincere.")),
                          ("smile", _("...Thanks, jerk. I needed that more than I'm going to admit."))],
                "tease": [("laugh", _("HA! Flattery and terrible judgment. My favorite combination.")),
                          ("smirk", _("Keep talking like that and I might forgive you for doing this to me. Might."))],
                "cold":  [("annoyed", _("Wow. I handed you the easiest question in the world and you still fumbled it.")),
                          ("sad", _("Try to remember whose kid this is the next time you feel like being charming."))],
            },
        },
        "rogue": {
            "narr": _("%s stands with both hands resting on her belly, looking down at it like she still isn't sure it belongs to her."),
            "lines": [
                ("looking_down", _("I never pictured myself like this, sugar. Not once.")),
                ("sad", _("Growing up, I figured this kind of life was for other girls. Not for somebody like me.")),
                ("thinking", _("And now I catch my reflection in a window and there's this whole other woman staring back.")),
            ],
            "ask": ("shy", _("So tell me straight. When you look at me now... what do you see?")),
            "replies": {
                "sweet": [("shy", _("Lord... you can't just say things like that to a girl in my condition. I'll start crying right here.")),
                          ("smile", _("Thank you, sugar. I think I needed to hear that out loud."))],
                "tease": [("embarrassed", _("Is that so? Well, ain't you sweet. And a little bit of a scoundrel.")),
                          ("smirk", _("Keep talking like that and you'll find out how much energy I've still got."))],
                "cold":  [("sad", _("No. I suppose there ain't.")),
                          ("looking_down", _("I should've known better than to ask."))],
            },
        },
        "ntw": {
            "narr": _("%s stares down at her belly with the look she usually saves for people who talk during movies."),
            "lines": [
                ("angry", _("I can't train. I can't run. I tried one pull-up yesterday and my own body said no.")),
                ("annoyed", _("I bump into doorframes. DOORFRAMES. I've lived here a year and suddenly I can't find the door.")),
                ("confused", _("I don't know what I'm supposed to feel. I'm angry. Then I'm not. Then I'm angry that I'm not.")),
            ],
            "ask": ("serious", _("So. Go ahead. Tell me what I look like. And think before you answer.")),
            "replies": {
                "sweet": [("looking_left", _("...That was the right answer.")),
                          ("embarrassed", _("Whatever. Thanks. Shut up."))],
                "tease": [("smirk", _("Hotter. Sure. I walk like a penguin, but go off.")),
                          ("annoyed", _("Say it again in a month, when I can't reach my own shoes. Then I'll believe you."))],
                "cold":  [("angry", _("Wow. Insightful. Get out of my face.")),
                          ("annoyed", _("I asked ONE question."))],
            },
        },
        "tenny": {
            "narr": _("%s tugs her top down over her belly, crosses her arms over it, then uncrosses them, unsure where her hands should go."),
            "lines": [
                ("nervous", _("I-I know I look different now. Everyone stares. Or maybe they don't, and I just think they do...")),
                ("sad", _("None of my clothes fit. I feel huge, and slow, and I keep thinking you must see it too.")),
                ("looking_down", _("I looked up whether it's normal to feel like this. It is. Knowing that didn't help.")),
            ],
            "ask": ("shy", _("D-do I still look okay to you? You can be honest. I think.")),
            "replies": {
                "sweet": [("surprised", _("R-really? You're not just saying that?")),
                          ("smile", _("Okay... okay. I'm going to believe you. Thank you."))],
                "tease": [("embarrassed", _("H-hotter?! Like THIS?!")),
                          ("shy", _("You can't just... I... okay. Maybe say it again later."))],
                "cold":  [("sad", _("Oh. Right. Yeah... that makes sense.")),
                          ("looking_down", _("S-sorry I asked."))],
            },
        },
        "_default": {
            "narr": _("%s looks down at her belly, then back at you, a little unsure."),
            "lines": [
                ("looking_down", _("It keeps getting bigger. Some days I barely recognize myself.")),
                ("worried", _("Nothing fits, everything is harder, and everyone can see it now.")),
            ],
            "ask": ("shy", _("Be honest with me. How do I look?")),
            "replies": {
                "sweet": [("smile", _("Thank you. I really needed to hear that."))],
                "tease": [("embarrassed", _("You're terrible. ...Say it again."))],
                "cold":  [("sad", _("Right. Forget I asked."))],
            },
        },
    }

    # Back from her last birth: she tells him the doctor recommended an IUD for a couple years to let her
    # body stabilize. ONE story for everybody (a medical recommendation, never her choice), so it holds for
    # any trait. "lines" come before his question, "answer" replies to it, then ONE closer by mood.
    _PREG_PROCEDURE_PLAYER_LINE = _("Wait. Are you okay?")
    _PREG_BODY_PROCEDURE = {
        "gwen": {
            "narr": _("%s picks at her sleeve for a moment. The joke you were expecting never comes."),
            "lines": [
                ("looking_down", _("So. There's a part of the birth story I left out of the texts.")),
                ("serious", _("The delivery got rough. Really rough. Afterwards, the doctor sat me down and said my body needs time to recover properly.")),
            ],
            "answer": ("shy", _("They put in an IUD. It stays for a couple years, maybe more. So... no babies for a while. Doctor's orders.")),
            "closers": {
                "default": ("smirk", _("One kid is plenty of chaos for now. And hey, at least it's not permanent. Just a really long time-out.")),
                "fear":    ("bemused", _("Honestly? I'm kind of relieved. The idea of going through all that again anytime soon was terrifying.")),
                "fetish":  ("looking_down", _("I know it's not forever, but... I wanted more, sooner. Guess my body had other plans.")),
            },
        },
        "rogue": {
            "narr": _("%s takes your hand before she says anything, and holds on a little too tight."),
            "lines": [
                ("looking_down", _("Sugar, there's somethin' I couldn't put in a text.")),
                ("worried", _("The delivery got rough. Real rough. The doctor said my body needs time to heal proper before I even think about another baby.")),
            ],
            "answer": ("shy", _("They put in an IUD. It'll stay for a couple years, let everything settle. So I'm benched for a while, I guess.")),
            "closers": {
                "default": ("smile", _("My aunt says rest is just wisdom your body is askin' for. And it ain't forever, just for now.")),
                "fear":    ("shy", _("And Lord forgive me, part of me is relieved. I was scared half to death of goin' through that again so soon.")),
                "fetish":  ("looking_down", _("I always pictured havin' more, sugar. And maybe I still will, just... not for a while.")),
            },
        },
        "ntw": {
            "narr": _("%s stands with her arms crossed, staring at a spot somewhere past your shoulder."),
            "lines": [
                ("annoyed", _("I'm going to say this once. No hugging.")),
                ("serious", _("The birth went sideways. After they got everything under control, the doctor said my body needs a break. A long one.")),
            ],
            "answer": ("looking_down", _("They put in an IUD. Couple years, minimum. So that's that for now.")),
            "closers": {
                "default": ("angry", _("Fine by me. One is more than enough drama for now. And if I change my mind later, that's MY call.")),
                "fear":    ("smirk", _("Honestly? Good. I don't have to think about it for a while. Don't look at me like that, I mean it.")),
                "fetish":  ("looking_down", _("I liked it. Being pregnant. And knowing I have to wait years before I can again... I hate that.")),
            },
        },
        "tenny": {
            "narr": _("%s twists her fingers together, rehearsing something under her breath before she looks up."),
            "lines": [
                ("nervous", _("I-I need to tell you something about the birth. I practiced it, but it still comes out wrong.")),
                ("worried", _("There were complications. The doctor said my body needs time to recover, so they put in an IUD.")),
            ],
            "answer": ("shy", _("I-I'm okay now. But I can't try again for a while. The doctor said a couple years at least, to let everything heal.")),
            "closers": {
                "default": ("smile", _("So it's just the one for now. I-I think that's okay. I just wanted you to hear it from me.")),
                "fear":    ("embarrassed", _("Is it awful that I felt relieved? I was so scared the whole time. At least now I don't have to worry about it for a while.")),
                "fetish":  ("looking_down", _("I-I wanted more. Soon, not years from now. I keep looking things up, but the doctor said to wait.")),
            },
        },
        "_default": {
            "narr": _("%s is quiet for a moment, like she is deciding how to start."),
            "lines": [
                ("looking_down", _("There's something about the birth I haven't told you.")),
                ("serious", _("It got complicated. The doctor said my body needs time to recover, so they recommended an IUD.")),
            ],
            "answer": ("shy", _("I'm fine now. But I can't try again for a while. A couple years, at least.")),
            "closers": {
                "default": ("smile", _("One is enough for now. I just wanted you to hear it from me.")),
                "fear":    ("shy", _("And honestly? Part of me is relieved. At least I don't have to worry about it for a while.")),
                "fetish":  ("looking_down", _("I wanted more, sooner. But the doctor says wait, so... I'll wait.")),
            },
        },
    }
    # pregnancy trait -> closer. No trait = "default".
    _PREG_PROCEDURE_TRAIT_MOOD = {"pregnancy_fear": "fear", "pregnancy_fetish": "fetish"}

    # His answer -> stat changes. A trait can override one answer.
    _PREG_LOOKS_EFFECTS = {
        "sweet": (("Love", 20),),
        "tease": (("Love", 8), ("Lust", 10)),
        "cold":  (("Love", -25),),
    }
    _PREG_LOOKS_TRAIT_EFFECTS = {
        "pregnancy_fetish": {"tease": (("Love", 15), ("Lust", 20))},
    }
    # answers after which she is done talking for now
    _PREG_LOOKS_ENDS_TALK = ("cold",)

    def _preg_body_stage(girl):
        """Where she is, for the moments: her progression stage while he knows she is pregnant,
        _PREG_BODY_STAGE_AFTER_BIRTH once she is back from her last birth (procedure done), else 0."""
        if getattr(girl, "_giving_birth", False):
            return 0
        if pregnancy_had_procedure(girl):
            return _PREG_BODY_STAGE_AFTER_BIRTH
        if getattr(girl, "_pregnant", False) and getattr(girl, "_pregnancy_known", False):
            return getattr(girl, "_pregnancy_stage", 0)
        return 0

    def pregnancy_body_moment_pending(girl):
        """Key of the body moment that should open this conversation, or None. Only the moment of the
        stage she is IN counts: once it has played, nothing earlier comes back."""
        if store._pregnancy_mode == "off":
            return None
        _at = _preg_body_stage(girl)
        _done = getattr(girl, "_preg_body_moments_done", None) or ()
        for _key, _stage in _PREG_BODY_MOMENTS:
            if _at >= _stage:
                return None if _key in _done else _key
        return None

    def _preg_procedure_mood(girl):
        for _trait, _mood in _PREG_PROCEDURE_TRAIT_MOOD.items():
            if girl.has_trait(_trait):
                return _mood
        return "default"

    def _preg_body_mark_done(girl, key):
        """Played: this moment and every earlier one are over for this pregnancy (tuple: the record is
        reset through _PREG_SCOPED_FLAGS, whose reset values must stay immutable)."""
        _stage = dict(_PREG_BODY_MOMENTS)[key]
        _done = tuple(getattr(girl, "_preg_body_moments_done", None) or ())
        girl._preg_body_moments_done = _done + tuple(_k for _k, _s in _PREG_BODY_MOMENTS if _s <= _stage and _k not in _done)
        print("[PREG_BODY] %s: '%s' played at stage %d, done=%s" % (girl.gid, key, girl._pregnancy_stage, girl._preg_body_moments_done))

    def _preg_body_narrate(text, girl):
        # every "narr" takes her name as %s (translated first, formatted after: _tl_fmt)
        Narration(_tl_fmt(text, girl.Name))

    def _preg_body_speak(girl, lines):
        for _expr, _text in lines:
            set_scene_expression(girl, _expr)
            Say_Line(girl, _text)

    def _preg_looks_apply(girl, answer):
        _effects = _PREG_LOOKS_EFFECTS[answer]
        for _trait, _by_answer in _PREG_LOOKS_TRAIT_EFFECTS.items():
            if girl.has_trait(_trait) and answer in _by_answer:
                _effects = _by_answer[answer]
        for _stat, _amount in _effects:
            Change_Status(girl, _stat, _amount)
        print("[PREG_BODY] %s: looks answer=%s effects=%s" % (girl.gid, answer, _effects))


# Dispatcher, called by talk_main. Returns his answer for "looks" (None for "changing" / "procedure").
label _pregnancy_body_moment(girl):
    $ _pbm_key = pregnancy_body_moment_pending(girl)
    if not _pbm_key:
        return None
    $ print("[PREG_BODY] %s: moment '%s' opens the conversation (stage %d, mode %s)" % (girl.gid, _pbm_key, girl._pregnancy_stage, store._pregnancy_mode))
    call expression "_pregnancy_body_" + _pbm_key pass (girl) from _call_preg_body_dispatch
    return _return


label _pregnancy_body_changing(girl):
    python:
        _pbc = girl_pool(_PREG_BODY_CHANGING, girl, "body moment changing")
        _preg_body_narrate(_pbc["narr"], girl)
        _preg_body_speak(girl, _pbc["lines"])
        set_scene_expression(girl, "normal")
        _preg_body_mark_done(girl, "changing")
    return None


label _pregnancy_body_procedure(girl):
    python:
        _pbp = girl_pool(_PREG_BODY_PROCEDURE, girl, "body moment procedure")
        _pbp_mood = _preg_procedure_mood(girl)
        _preg_body_narrate(_pbp["narr"], girl)
        _preg_body_speak(girl, _pbp["lines"])
        Say_Player(_PREG_PROCEDURE_PLAYER_LINE)
        _preg_body_speak(girl, [_pbp["answer"], _pbp["closers"][_pbp_mood]])
        # she told him: the trait is his to see from now on (banner, status screen, Fertility app "Infertile")
        girl.discover("discovered_trait_" + _PROCEDURE_TRAIT)
        set_scene_expression(girl, "normal")
        _preg_body_mark_done(girl, "procedure")
        print("[PREG_BODY] %s: told him about the procedure (mood=%s, removed traits=%s)" % (
            girl.gid, _pbp_mood, list(getattr(girl, "_birth_procedure_removed", None) or ()) or "none"))
    return None


label _pregnancy_body_looks(girl):
    python:
        _pbl = girl_pool(_PREG_BODY_LOOKS, girl, "body moment looks")
        _preg_body_narrate(_pbl["narr"], girl)
        _preg_body_speak(girl, _pbl["lines"] + [_pbl["ask"]])

    menu:
        "You look beautiful. I mean it.":
            $ _pbl_answer = "sweet"
        "Honestly? You somehow got even hotter.":
            $ _pbl_answer = "tease"
        "You look pregnant. What else is there to say?":
            $ _pbl_answer = "cold"

    python:
        _preg_body_speak(girl, _pbl["replies"][_pbl_answer])
        _preg_looks_apply(girl, _pbl_answer)
        _preg_body_mark_done(girl, "looks")

    if _pbl_answer in _PREG_LOOKS_ENDS_TALK:
        "She turns away. This conversation is over."
    $ set_scene_expression(girl, "normal")
    return _pbl_answer
