# ============================================================
# shion_hashimoto.rpy... Shion's secret: the Hashimoto clan (docs/plan_role_situations.md, Fase 5; the author's
# "Blackmail opportunity 1", a callback to her lore in Overwatch). Narrated over the Downtown picture (no art for
# the bar).
#
# THE THREE NIGHTS (step events of hers, steps 0 to 2, trigger "downtown_night": her curfew sends him to the late bus;
# every eligible night PLAYS, one per night, so three curfews in a row see the whole chain):
#   hashimoto_1   from the bus stop he sees her slip out in a dark coat; he follows, loses her
#   hashimoto_2   the next night on: again, deeper into the old Japanese streets (bg jptown); loses her again
#   hashimoto_3   the night after that: he follows her to a bar by the docks and records it. She slaps a gang boss
#                 over a shipment of drugs lost at customs: she runs the Hashimoto clan. Her eyes find his through
#                 the glass: she knows. Her proof ("evidence": girl._story_evidence = 1)
# WHAT THE PROOF DOES (story_steps.rpy): the "evidence" route of her unlock 0 -> 1 (the dinner: she puts his hand on
# her herself, a contract: STORY_SCENES["hand_under_table"]["shion"]), weight on the "blackmail" route, and one more
# choice in his blackmail picker, with her own lines (STORY_EVIDENCE["shion"]): only inside her step, as any blackmail.
# ============================================================

init 2 python:

    STORY_NPCS["hashimoto_boss"] = (_("Gang boss"), "#b91c1c")

    STORY_EVENTS.update({
        # No "chance" and "priority" (author, 2026-10-09: "deve ser 100%"): every night he is sent away the
        # next sight of her PLAYS, and no flavor event (home_late) can take the draw from it. The "follows" gap
        # of 1 only keeps each night ITS night (author, same day: "deve poder ver em sequencia", three nights
        # in a row; never twice in the same one).
        "hashimoto_1": {
            "trigger": "downtown_night", "label": "_story_hashimoto_night", "once": True, "priority": True,
        },
        "hashimoto_2": {
            "trigger": "downtown_night", "label": "_story_hashimoto_night", "once": True, "priority": True,
            "follows": ("hashimoto_1", 1),
        },
        "hashimoto_3": {
            "trigger": "downtown_night", "label": "_story_hashimoto_night", "once": True, "priority": True,
            "follows": ("hashimoto_2", 1), "evidence": 1,
        },
    })
    STORY_STEP_EVENTS["shion"] = {
        0: ("hashimoto_1", "hashimoto_2", "hashimoto_3"),
        1: ("hashimoto_1", "hashimoto_2", "hashimoto_3"),
        2: ("hashimoto_1", "hashimoto_2", "hashimoto_3"),
    }

    # The three nights. Her lines with face "" (she is far from him: no sprite)
    STORY_SCENES["hashimoto_1"] = {
        "shion": {
            "open": [
                (None, _("The bus is late. While you wait at the stop across the street, the door of the building opens.")),
                (None, _("It's her. A long dark coat, sunglasses at night, walking fast toward the river.")),
                ("@walk", ""),
                ("@player", _("...Where are you going at this hour?")),
                (None, _("You follow her for three blocks. Then she turns a corner, and when you turn it after her, the street is empty.")),
                (None, _("By the time you get back to the stop, your bus is pulling away. You wait for the next one.")),
                (None, _("You tell yourself it's just curiosity. But roads like this one rarely let you walk back.")),
            ],
        },
    }
    STORY_SCENES["hashimoto_2"] = {
        "shion": {
            "open": [
                (None, _("Another night, another late bus. And there she is again, in the same dark coat, going the same way.")),
                ("@walk", ""),
                (None, _("This time you keep your distance. Two blocks. Four.")),
                ("@bg", "bg jptown"),
                (None, _("The streets get narrower, and the signs switch to Japanese.")),
                (None, _("A delivery truck backs out of an alley between you. By the time it's gone, so is she.")),
                ("@player", _("...What are you hiding?")),
                (None, _("Whatever it is, you're one night away from it. Keep following her and there will be no pretending you didn't choose this.")),
            ],
        },
    }
    STORY_SCENES["hashimoto_3"] = {
        "shion": {
            "open": [
                (None, _("The third time, you don't wait at the bus stop. You wait in the shadow of the building, and when she comes out, you're already moving.")),
                ("@walk", ""),
                ("@bg", "bg jptown"),
                (None, _("She leads you to a narrow street by the docks. A red lantern. A door with no sign. A bar that doesn't want customers.")),
                (None, _("Through the window, you watch her slide into a booth across from a man covered in tattoos. Two men stand behind him. Everyone else in the bar is very careful not to look at that booth.")),
                (None, _("You take out your phone and start recording.")),
                ("@hashimoto_boss", _("Forgive me. The port police were waiting for us. We couldn't...")),
                (None, _("She slaps him. Hard enough that you hear it through the glass.")),
                ("", _("A whole shipment. Do you have any idea what it cost me to get that through customs?")),
                ("@hashimoto_boss", _("I'll get it back. Every crate. I swear it.")),
                ("", _("You will. Or the Hashimoto clan will need a new man at this table.")),
                (None, _("The man bows his head until it almost touches the table.")),
                (None, _("You stop recording. Your hands are shaking. A shipment, customs, a gang boss bowing to her: she is smuggling drugs into the country.")),
                (None, _("Your stepmother doesn't just run a company. She runs the Hashimoto clan.")),
                (None, _("As you back away from the window, she turns her head. For one second, her eyes meet yours through the glass.")),
                (None, _("Then she looks away, as if she saw nothing at all.")),
                # why she cannot afford to lose his father (tester 2026-10-10): the marriage is her front
                (None, _("And suddenly the marriage makes sense. The ordinary husband, the ordinary apartment, the Sunday dinners: a clean, boring, documented life. A woman like her does not get to exist in daylight without one.")),
                (None, _("That is why she cannot afford to lose your father. He is not the love of her life. He is her alibi for having one.")),
                (None, _("{b}What you recorded tonight could force her story open. If it does, that is the road you walk to the end: there is no winning her heart afterwards.{/b}")),
                (None, _("Nothing forces your hand. The video only opens her story if you choose to use it; if her heart is what you want, make it matter more than the video by Sunday dinner.")),
                (None, _("Either way, the next move is the same: be at your father's table on Sunday.")),
            ],
        },
    }

    # Her unlock 0 -> 1 when his proof is the route (her version, merged into the role's scene)
    STORY_SCENES["hand_under_table"]["shion"] = {
        "routes": {
            "evidence": [
                (None, _("She hasn't looked at you once tonight. Not since the bar by the docks, when her eyes found yours through the glass.")),
                (None, _("Under the table, her hand finds yours. It's cold. She sets it on her thigh herself and holds it there.")),
                ("serious", _("You keep what you saw to yourself. And I keep you... happy. Is that clear?")),
                (None, _("Her nails dig into the back of your hand, just a little. A contract, signed.")),
            ],
        },
    }

    # His blackmail with the bar video (story_evidence_blackmail)
    STORY_EVIDENCE["shion"] = {
        "menu": _("The bar by the docks: her and the gang boss"),
        "first": [
            ("@player", _("I followed you the other night. The bar by the docks. I recorded everything.")),
            ("serious", _("You followed me.")),
            ("@player", _("You. The gang boss. The shipment you smuggled through customs.")),
            ("serious", _("Do you have any idea who you're threatening, boy?")),
            ("@player", _("My stepmother. Who runs the Hashimoto clan. I'm sure Dad would love to meet her.")),
            ("annoyed", _("...What do you want?")),
        ],
        "again": [
            ("@player", _("I still have the video from the bar.")),
            ("annoyed", _("Of course you do. You'll hold it over me until one of us is dead.")),
        ],
        "accept": [
            ("serious", _("Fine. You get what you want. And that video never sees daylight.")),
            (None, _("She says it the way she must sign every contract she hates: without blinking.")),
        ],
        "fail": [
            ("smirk", _("No. Go ahead, show someone. See who believes you, and who comes looking for you afterwards.")),
            ("serious", _("Now get out of my sight.")),
        ],
    }

# One of the three nights (story_event_play plays the event in store._story_event_now): the streets of Downtown
label _story_hashimoto_night(girl):
    python:
        _shn_ev = store._story_event_now
        hide_girl_sprite(girl)
        print("[STORY] %s: %s (Day %d)" % (girl.gid, _shn_ev, Day))
    scene expression ("bg downtown_night" if TimeIndex >= NIGHT_INDEX else "bg downtown")
    with fade
    call story_route_scene(girl, _shn_ev) from _call_story_route_scene_hashimoto
    return
