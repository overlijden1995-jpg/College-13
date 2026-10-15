# ============================================================
# femdom_lines_ntw.rpy... NTW's own femdom voice (docs/plan_femdom.md, section 6.4), read by scene_pick_line
# ============================================================
#
# Keys: "femdom_<moment>.ntw". scene_pick_line puts her gid first among the modifiers, so these pools win over
# the shared ones in femdom_lines.rpy. Discovery phase (D7): "femdom_<moment>.ntw.femdom_first" (her very first
# scene) and "femdom_<moment>.ntw.femdom_new" (her first few scenes).
# Her voice: bossy to the extreme, clipped and deadpan, NO exclamation marks, "genius" / "idiot", training and
# discipline metaphors, a temper under the calm. She humiliates him every chance she gets (every verdict, every
# challenge he loses). Only femdom_forced / femdom_force_cum / femdom_force_cum_after are veteran-only: every
# other pool also plays in her discovery phase, so none of them talks like it is an old habit.
# ============================================================

init 1 python:

    SCENE_LINES.update({

        # ══════════════════════════════════════════════════════════
        #  REFUSED: he said no to one of her requests (femdom.rpy _femdom_refused_react)
        # ══════════════════════════════════════════════════════════
        "femdom_refused.ntw": [
            _("Excuse me? That wasn't a request, idiot."),
            _("No? Wrong answer. You'll pay for that."),
            _("You don't get to say no to me, genius. Remember that."),
        ],
        "femdom_refused.ntw.femdom_first": [
            _("No? ...Huh. I hate hearing that from you. More than I expected."),
            _("You ignored me. I didn't know that would piss me off this much. Noted."),
        ],
        "femdom_refused.ntw.femdom_new": [
            _("Ignoring me again, genius? I'm learning I really like being obeyed."),
            _("Again? Turns out I don't take no well. At all."),
        ],

        # ══════════════════════════════════════════════════════════
        #  ORDERS (femdom.rpy, F2): what she orders, and how it ends
        # ══════════════════════════════════════════════════════════

        # He stood up to her (any order)
        "femdom_defied_won.ntw": [
            _("Fine. You win this round. Enjoy it. It won't happen again."),
            _("Hm. You've got some spine, genius. Don't get used to it."),
            _("Okay. Your way. Once. I'm keeping score."),
        ],
        "femdom_defied_lost.ntw": [
            _("Cute. That was your best? My way. Now."),
            _("Nice try, idiot. Sit still and take it."),
            _("You lost. Obviously. Stop squirming."),
        ],
        "femdom_obeyed.ntw": [
            _("Good. Keep it exactly there."),
            _("See? You can follow instructions."),
            _("Better. Don't stop until I say."),
        ],

        # Take over: she gets on top (from doggy / full nelson / laying down)
        "femdom_take_over.ntw": [
            _("On your back. Now."),
            _("Enough. Pull out and lie down. I'm riding you."),
            _("You had your turn, genius. On your back. I'm driving."),
        ],
        "femdom_take_over.ntw.femdom_first": [
            _("On your back. ...Huh. Never said that to anyone before. I like how it sounds."),
            _("Stop. Lie down. I want to ride you. First time I've given that order. Don't make it weird."),
        ],
        "femdom_take_over.ntw.femdom_new": [
            _("On your back again. Being on top is growing on me."),
            _("Lie down. Again. Turns out I like giving you orders, genius."),
        ],
        "femdom_forced.ntw": [
            _("I wasn't asking, genius."),
            _("Stay down. You don't get a vote."),
            _("You really thought that was a question? Cute."),
        ],

        # Challenge
        "femdom_challenge.ntw": [
            _("That's all you've got? Pathetic. Try harder."),
            _("I'm bored, genius. Give me something worth my time."),
            _("Weak. I've had better workouts on a treadmill. More."),
        ],
        "femdom_challenge.ntw.femdom_first": [
            _("That's all? ...Huh. Pushing you around feels good. Didn't know that."),
            _("Harder. I've never talked to anyone like this during sex. Turns out I'm good at it."),
        ],
        "femdom_challenge.ntw.femdom_new": [
            _("Weak, again. Making you work for it is becoming my favorite part."),
            _("Is that all, again? I'm starting to really like telling you what to do."),
        ],
        "femdom_challenge_met.ntw": [
            _("Better. Barely. Keep it up."),
            _("There. Was that so hard, genius?"),
            _("Good. That's the pace. Drop it and we start over."),
        ],

        # Pace
        "femdom_pace_faster.ntw": [
            _("Faster. Stop slacking."),
            _("Pick it up, genius. This isn't a warm-up."),
            _("Faster. Did I stutter?"),
        ],
        "femdom_pace_slower.ntw": [
            _("Slower. I set the pace, not you."),
            _("Slow down, idiot. It's not a race."),
            _("Easy. Slower. Control. Look it up."),
        ],

        # "Don't you dare cum yet" (any scene: handjob, titjob, footjob, blowjob, any position)
        "femdom_no_cum.ntw": [
            _("Don't you dare cum. Not yet."),
            _("Hold it. You cum when I say, idiot."),
            _("No finishing. I'm not done with you. Hold it."),
        ],
        "femdom_edge_release.ntw": [
            _("Now. Cum."),
            _("Okay. You earned it. Barely. Let go."),
            _("Go on, genius. Cum for me."),
        ],
        "femdom_edge_kept.ntw": [
            _("You held it until I said. Good. There's hope for you."),
            _("Disciplined. Didn't think you had it in you, genius."),
            _("See? Wait for my say and it's better. Remember that."),
        ],
        "femdom_edge_broken.ntw": [
            _("I said wait. You lasted about two seconds. Pathetic."),
            _("One order, genius. Hold it. And you couldn't even do that."),
            _("Zero discipline. You'd wash out of any training program in a day."),
        ],

        # Where he cums (inside = vaginal or anal; mouth = during a blowjob)
        "femdom_demand_inside.ntw": [
            _("When you cum, you cum inside me. Don't argue."),
            _("Inside me. All of it. Pull out and you're done here."),
            _("You're finishing inside. I decided. You don't."),
        ],
        "femdom_demand_on_me.ntw": [
            _("When you cum, pull out and cum on me. Got it?"),
            _("Not inside. On me. I want to see the mess."),
            _("You cum on me, idiot. Not in me. My call."),
        ],
        "femdom_demand_mouth.ntw": [
            _("When you cum, it goes down my throat. Don't pull away."),
            _("Mouth. Every drop. Pull out and you'll regret it."),
            _("You finish in my mouth, genius. Nowhere else."),
        ],
        "femdom_demand_kept.ntw": [
            _("Right where I said. Good."),
            _("You followed one order. Congratulations, genius."),
            _("Exactly where I wanted it. You're trainable after all."),
        ],
        "femdom_demand_broken.ntw": [
            _("Wrong place, idiot. I gave you one instruction."),
            _("That's not where I told you. Can you follow anything?"),
            _("You had one job. You failed it. Embarrassing."),
        ],

        # Me first
        "femdom_me_first.ntw": [
            _("Me first. You, maybe. If you earn it."),
            _("You don't cum until I do. Understood?"),
            _("I cum first, genius. You wait your turn."),
        ],
        "femdom_me_first_kept.ntw": [
            _("Me first. Like I said. Good."),
            _("You got me there first. Fine. Be proud. Quietly."),
            _("That's the order. Me, then you. Learn it."),
        ],
        "femdom_me_first_broken.ntw": [
            _("You finished first. Selfish and useless. Great combo."),
            _("I said me first. You couldn't even last long enough to get me there."),
            _("Done, and I'm not. Next time you don't cum at all until I do."),
        ],

        # He came too fast (her profile's "humiliate")
        "femdom_humiliate_fast.ntw": [
            _("Already? Pathetic. Again. And this time last longer."),
            _("That's it? That wasn't even a warm-up, genius."),
            _("Done already? Zero stamina. I'm putting you on a training plan."),
        ],

        # He wants to leave her position (cowgirl / reverse cowgirl) for his
        "femdom_pos_refuse.ntw": [
            _("You want me under you? No. Stay down."),
            _("Switch? Denied. I'm on top, I'm staying on top."),
            _("Nice try, genius. You're comfortable down there. Stay."),
        ],

        # Forced cum: a veteran on top keeps him inside (Cum.rpy)
        "femdom_force_cum.ntw": [
            _("Hold still. You're finishing inside me. That's final."),
            _("Pull out? No. I'm not getting up, and neither are you."),
            _("Stay. Every drop goes inside me. I decided."),
        ],
        "femdom_force_cum_after.ntw": [
            _("Inside me, where I said. Remember who's in charge."),
            _("How many times do I have to tell you? I decide where you finish."),
            _("You tried to pull out. Cute. Didn't work, did it?"),
        ],
    })
