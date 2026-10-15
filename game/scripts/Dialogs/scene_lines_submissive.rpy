# ============================================================
# scene_lines_submissive.rpy... the submissive trait in the scene (docs/plan_submissive_pass.md S1 / S4 / S5)
#
# Deference, not appetite (the author's ruling 2026-10-11): she accepts the word, obeys the order, asks if she did
# well. The pools below are read by scene_pick_line with the modifier "submissive" (_detect_line_modifiers); the
# four that already existed and read like appetite are REWRITTEN here (update replaces the key):
# moan.speed2.submissive, moan.speed2.full_nelson.submissive. The Full Nelson gets its speed 1 and 3 (S4).
# ============================================================

init 1 python:

    SCENE_LINES.update({

        # ── moans: she asks, she reports, she waits for the next word ──
        "moan.speed2.submissive": [
            _("Like this...? Tell me if I should... move differently..."),
            _("Whatever you want... just say it... I'll do it..."),
            _("Am I... doing it right...? Please tell me..."),
        ],
        "moan.speed1.full_nelson.submissive": [
            _("I can't move... that's... okay. You've got me. Tell me what to do..."),
            _("Like this...? I'll stay just like this. However long you want..."),
            _("I don't... I don't have to decide anything like this. Okay..."),
        ],
        "moan.speed2.full_nelson.submissive": [
            _("I can't move at all... I'm not supposed to, right...? Okay..."),
            _("Hold me however you want... I'll keep still... I promise..."),
            _("Just tell me if I'm... doing okay... please..."),
        ],
        "moan.speed3.full_nelson.submissive": [
            _("I can't... I can't move... yes... yes...!"),
            _("Whatever you want... whatever you... AAH...!"),
            _("Don't let go... please don't let... go...!"),
        ],

        # ── her asks answered (SubEvents pos / pace): she takes the no as the answer ──
        "pos_denied.submissive": [
            _("Okay. We stay like this. You know best."),
            _("Sorry... I shouldn't have asked. Like this is fine."),
            _("Yes. Whatever you decide. I just... wanted to offer."),
        ],
        "pace_obeyed.submissive": [
            _("Thank you... yes... like that..."),
            _("That's... thank you. That's exactly it..."),
        ],
        "pace_ignored_1.submissive": [
            _("...Okay. Your pace. I'm sorry I said anything."),
            _("Right. You decide the pace. I'll keep up."),
        ],
        "pace_ignored_2.submissive": [
            _("I won't ask again. However you want it..."),
            _("Okay... okay. Your way. I'll stop asking."),
        ],

        # ── a strip, a touch, a kiss on a girl who waits for the order (S1: instant, eyes down) ──
        "cum_mouth_accepted.submissive": [
            _("Yes. In my mouth. Tell me when... or don't. It's yours."),
            _("Okay. I'll keep it all. Just... tell me if I should swallow."),
        ],
        "record_accepted.submissive": [
            _("If you want it filmed... okay. I'll do whatever you tell me on camera too."),
            _("Yes. Film it. Just... tell me where to look."),
        ],
    })
