# ============================================================
# femdom_lines_shion.rpy... Shion's own voice for the femdom trait (docs/plan_femdom.md, docs/plan_shion.md)
# ============================================================
#
# Keys: "femdom_<moment>.shion". scene_pick_line puts her gid first among the modifiers, so these pools win over
# the shared "femdom_<moment>" pools of femdom_lines.rpy (same moments, same comments there).
# Her voice: cold, controlling, narcissistic and possessive. He is her tool ("boy", "my little investment"), she
# talks about him in business words ("results", "unacceptable", "I don't reward mediocrity") and humiliates often.
# Femdom and experienced are her canon: she is ALWAYS a veteran, so she has NO discovery pools (femdom_first / new).
# Her story (the family, the apartment, her turning stages) is not in the game yet: these lines stay on control,
# power, contempt and possession. Her stages will enter as a modifier when they exist.
# ============================================================

init 1 python:

    SCENE_LINES.update({

        # ══════════════════════════════════════════════════════════
        #  REFUSED: he said no to one of her requests
        # ══════════════════════════════════════════════════════════
        "femdom_refused.shion": [
            _("No? You don't say no to me, boy. You say yes, and you say it quickly."),
            _("Refusal noted. I keep a very detailed record of every disappointment."),
            _("My little investment has opinions now? Careful. I write off bad assets."),
        ],

        # ══════════════════════════════════════════════════════════
        #  ORDERS
        # ══════════════════════════════════════════════════════════

        # He stood up to her (any order)
        "femdom_defied_won.shion": [
            _("Fine. Take your little victory. I'll collect the interest on it later."),
            _("So there is a spine in there. Don't mistake one good quarter for a promotion."),
            _("Enjoy it, boy. I let you have this one, and I decide when you get the next."),
        ],
        "femdom_defied_lost.shion": [
            _("That was your big move? Adorable. Now be quiet and let me handle this."),
            _("Did you really think that would work on me? I've broken far better men than you."),
            _("Cute attempt. Rejected. We do this my way, boy."),
        ],
        "femdom_obeyed.shion": [
            _("Good. Obedience looks much better on you than ambition."),
            _("See how easy that was? Keep following orders and you stay my favorite investment."),
            _("Acceptable. Do exactly as I say and I may even be pleased with you."),
        ],

        # Take over: she gets on top (from doggy / full nelson / laying down)
        "femdom_take_over.shion": [
            _("Enough. On your back, boy. Nobody else runs this for long."),
            _("Stop. You had your turn, and frankly it was underwhelming. Lie down, I'm taking over."),
            _("On your back. Now. I prefer to look down on my investments."),
        ],
        "femdom_forced.shion": [
            _("Did you mistake that for a negotiation? It wasn't one."),
            _("Stay down. You belong exactly where I put you."),
            _("There. Beneath me. That's your place, boy, and don't forget it."),
        ],

        # Challenge
        "femdom_challenge.shion": [
            _("Is this your best effort? Because if it is, I'm deeply unimpressed."),
            _("I've sat through budget meetings more exciting than this. Try harder."),
            _("Show me results, boy. I don't reward mediocrity."),
        ],
        "femdom_challenge_met.shion": [
            _("Better. Much better. See what a little pressure produces?"),
            _("There it is. Keep that up and you might justify the investment."),
            _("Good boy. That's the kind of performance I expect from what's mine."),
        ],

        # Pace
        "femdom_pace_faster.shion": [
            _("Faster. I don't intend to wait all night for you to get going."),
            _("Pick up the pace, boy. You're wasting my time, and my time is expensive."),
            _("Faster. That wasn't a suggestion."),
        ],
        "femdom_pace_slower.shion": [
            _("Slow down. I set the pace here, not your desperate little body."),
            _("Easy, boy. Slowly. I like to take my time with what I own."),
            _("Did I say you could rush? Slower. This runs on my schedule."),
        ],

        # "Don't you dare cum yet"
        "femdom_no_cum.shion": [
            _("Don't you dare cum. You haven't earned it, and I haven't allowed it."),
            _("Hold it, boy. You finish when I authorize it, not a second before."),
            _("Cum without my permission and I'll treat it as a breach of contract."),
        ],
        "femdom_edge_release.shion": [
            _("Now. Cum for me, boy. Permission granted."),
            _("Good. You held it like I told you. Now let go."),
            _("You may cum now. Consider it a bonus for good behavior."),
        ],
        "femdom_edge_kept.shion": [
            _("You waited for my permission. Good. That's what discipline looks like."),
            _("Held it until I said so. There may be hope for you yet, boy."),
            _("Right on my schedule. I do love a good return on an investment."),
        ],
        "femdom_edge_broken.shion": [
            _("I said hold it. One simple instruction, and you failed it. Unacceptable."),
            _("Did I give you permission? No. I didn't. Pathetic."),
            _("You couldn't even wait for my say-so. What a disappointing little investment."),
        ],

        # Where he cums
        "femdom_demand_inside.shion": [
            _("When you cum, you cum inside me. Every drop. That isn't up for discussion."),
            _("Don't even think about pulling out, boy. It all goes inside me."),
            _("You're finishing inside me. I made the decision, you just carry it out."),
        ],
        "femdom_demand_on_me.shion": [
            _("When you cum, you pull out and cum on me. I want to see what I did to you."),
            _("Not inside. On me. I want the evidence where I can look at it."),
            _("You'll pull out and cover me with it, boy. Not a single drop inside."),
        ],
        "femdom_demand_mouth.shion": [
            _("When you cum, it goes in my mouth. Don't you dare pull away."),
            _("In my mouth, boy. All of it. I don't let anything I own go to waste."),
            _("You cum in my mouth, nowhere else. I always collect what I'm owed."),
        ],
        "femdom_demand_kept.shion": [
            _("Exactly where I ordered it. Good boy."),
            _("Instructions followed to the letter. I could almost be proud of you."),
            _("Right where I wanted it. You're learning who's in charge."),
        ],
        "femdom_demand_broken.shion": [
            _("That is not where I told you to cum. Unacceptable."),
            _("I gave you one order, boy. One. And you ignored it."),
            _("Wrong place. You'll pay for that mistake, with interest."),
        ],

        # Me first
        "femdom_me_first.shion": [
            _("You don't cum until I do. I come first, boy. In everything."),
            _("Me first. Then, if your performance is adequate, maybe you."),
            _("My pleasure is the priority here. Yours is a footnote. Understood?"),
        ],
        "femdom_me_first_kept.shion": [
            _("Me first, exactly as I ordered. Good boy."),
            _("You made me cum first. See? You can deliver when it matters."),
            _("That's the correct order of business. Me, then you."),
        ],
        "femdom_me_first_broken.shion": [
            _("You finished before me. I said me first. Did you forget who you belong to?"),
            _("Selfish and early. Two failures at once, boy. Impressive, in the worst way."),
            _("Unbelievable. My pleasure was your only priority, and you couldn't deliver."),
        ],

        # He came too fast (her profile's "humiliate")
        "femdom_humiliate_fast.shion": [
            _("Already? That was embarrassingly fast. Pathetic."),
            _("That's it? I've had elevator rides that lasted longer than you, boy."),
            _("Finished before I even got comfortable. I'll have to train you properly."),
        ],

        # He wants to leave her position for his (she is on top: cowgirl / reverse cowgirl)
        "femdom_pos_refuse.shion": [
            _("You want me under you? Cute. No. I'm staying right where I am."),
            _("Switch? Request denied. I like the view from up here."),
            _("I'm comfortable on top, boy. You stay beneath me until I decide otherwise."),
        ],

        # Forced cum: she is on top and keeps him inside (Cum.rpy)
        "femdom_force_cum.shion": [
            _("Don't move. You're cumming inside me, and you don't get a vote."),
            _("Pull out? No. I'm keeping every drop, boy. It's mine."),
            _("Stay exactly where you are. You finish inside me because I say so."),
        ],
        "femdom_force_cum_after.shion": [
            _("That's where it belongs. Remember who made that decision."),
            _("Good. Next time, don't even think about pulling out on me."),
            _("See? I always get what I want, boy. Always."),
        ],
    })
