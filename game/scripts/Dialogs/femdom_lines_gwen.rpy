# ============================================================
# femdom_lines_gwen.rpy... Gwen's femdom voice (docs/plan_femdom.md), read by scene_pick_line
# ============================================================
#
# Keys: "femdom_<moment>.gwen" for every moment of femdom_lines.rpy. scene_pick_line puts her gid first among the
# modifiers, so these pools win over the shared "femdom_<moment>" ones. Her voice: challenging and ironic, a dry
# goth artist who turns everything into a contest (art metaphors welcome), mocks lightly, never cruelly.
#
# Discovery phase (D7): "femdom_<moment>.gwen.femdom_first" = her very first scene giving orders (she may say it is
# new), "femdom_<moment>.gwen.femdom_new" = her first few scenes (she may say "again", never "first time"). Only the
# veteran moments (femdom_forced, femdom_force_cum, femdom_force_cum_after) may sound experienced: every other pool
# also plays in her discovery phase, so none of them claims an old habit.
# ============================================================

init 1 python:

    SCENE_LINES.update({

        # ══════════════════════════════════════════════════════════
        #  REFUSED: he said no to one of her requests (femdom.rpy _femdom_refused_react), any scene
        # ══════════════════════════════════════════════════════════
        "femdom_refused.gwen": [
            _("Wow. I tell you exactly what I want and you just... don't? Bold strategy. Let's see how that works out for you."),
            _("No? Cute. Enjoy that one. It's the last no you're getting."),
            _("That wasn't a suggestion, genius. I don't do suggestions."),
        ],
        "femdom_refused.gwen.femdom_first": [
            _("Hey. I told you what I wanted. ...Weird. I've never cared this much about being listened to."),
            _("No? Huh. That really got under my skin. Guess I just found out I like calling the shots."),
        ],
        "femdom_refused.gwen.femdom_new": [
            _("Ignoring me again? I'm starting to figure out I don't just want to be heard. I want to be obeyed."),
            _("Another no. Funny, every time you say it I want to be in charge a little more."),
        ],

        # ══════════════════════════════════════════════════════════
        #  ORDERS (femdom.rpy, F2)
        # ══════════════════════════════════════════════════════════

        # He stood up to her (any order, or her position refusal)
        "femdom_defied_won.gwen": [
            _("Fine. You win this round. Don't let it go to your head, it's one round."),
            _("Okay, okay. Point to you. I'm keeping score, by the way."),
            _("Hmph. Look who grew a spine. ...Enjoy it. I want a rematch."),
        ],
        "femdom_defied_lost.gwen": [
            _("That was adorable. Really. A for effort, F for results. We're doing it my way."),
            _("Nice try. I've beaten tougher opponents with a cold and no sleep. Sit still."),
            _("Was that your big power move? Cute. My way. Now."),
        ],
        "femdom_obeyed.gwen": [
            _("See? Not so hard when you actually listen."),
            _("Good. Just like that. Look at you, following directions."),
            _("Mm, there it is. Keep that up and I might even say something nice about you."),
        ],

        # Take over: from doggy / full nelson / laying down, she puts him on his back and rides him
        "femdom_take_over.gwen": [
            _("Okay, enough of your rough draft. On your back. I'm taking over."),
            _("Stop. Lie down. You had your turn, now watch how it's done."),
            _("On your back. That's an order, and yes, I'm riding you whether you like it or not."),
        ],
        "femdom_take_over.gwen.femdom_first": [
            _("Wait. Stop. Lie down, I want to be on top. ...Huh. I've never ordered anyone around like that before."),
            _("On your back. No, I'm not asking. ...Wow. I didn't know I had that in me. I kind of love it."),
        ],
        "femdom_take_over.gwen.femdom_new": [
            _("On your back again. I'm starting to think I just like watching you do what I say."),
            _("Lie down. I keep ending up on top, and I keep liking it more."),
        ],
        # Veteran only: she shoved him onto his back anyway
        "femdom_forced.gwen": [
            _("Did you really think that was a vote? Stay down."),
            _("I said on your back. I don't repeat myself, and I definitely don't negotiate."),
            _("You'd think you'd have learned by now. I always end up on top."),
        ],

        # Challenge (penetration)
        "femdom_challenge.gwen": [
            _("C'mon, didn't you want to fuck me? Then do it hard. That's an order."),
            _("Wow. Is that the whole show? I've seen more effort from a screensaver."),
            _("Is that all you've got? I've seen more passion in a paint-by-numbers kit. Prove me wrong."),
        ],
        "femdom_challenge.gwen.femdom_first": [
            _("Is that all you've got? ...Huh. I've never talked to anyone like that during sex. Why do I like it so much?"),
            _("C'mon, harder. That's an order. ...Wow. I've never given anyone an order like that. I could get used to this."),
        ],
        "femdom_challenge.gwen.femdom_new": [
            _("Coasting again? Harder. I'm finding out I really like making you work for it."),
            _("That's all you've got, again? Good thing I'm starting to enjoy pushing you around."),
        ],
        "femdom_challenge_met.gwen": [
            _("There it is. Good boy. ...Don't let it go to your head."),
            _("Better. Okay, I take back half of what I said."),
            _("Now we're talking. Still a rough draft, but it's getting there. Don't stop."),
        ],

        # Pace
        "femdom_pace_faster.gwen": [
            _("Faster. I'm not here for a slow dance."),
            _("Pick up the pace. That's an order, not a suggestion."),
            _("Faster. Unless you're trying to bore me to death, in which case, it's working."),
        ],
        "femdom_pace_slower.gwen": [
            _("Slow down. This isn't a race, and even if it was, I'd be the one deciding who wins."),
            _("Easy. Slower. Good art takes time, and I want to feel every stroke."),
            _("Whoa. Who said you could speed through this? Slow down, we go at my pace."),
        ],

        # "Don't you dare cum yet" (any scene: handjob, titjob, footjob, blowjob, any position)
        "femdom_no_cum.gwen": [
            _("Oh, you're close? Too bad. You don't cum until I say so."),
            _("Hold it. If you cum now, you lose. And I don't reward losers."),
            _("Don't you dare. You finish when I decide, and I haven't decided."),
        ],
        "femdom_edge_release.gwen": [
            _("Okay. You held it. Now cum for me."),
            _("Time's up. Go ahead and cum, you earned it. ...Barely."),
            _("Now. Cum for me. That's an order, and it's the fun kind."),
        ],
        "femdom_edge_kept.gwen": [
            _("You actually waited. Color me impressed."),
            _("Look at that. You held it until I let you. Gold star."),
            _("See? That's what happens when you listen. Worth it, right?"),
        ],
        "femdom_edge_broken.gwen": [
            _("I said wait. One instruction. You had one instruction."),
            _("Seriously? I told you to hold it and you just... couldn't. Disqualified."),
            _("Did I say you could cum? No? Didn't think so. We're working on that."),
        ],

        # Where he cums (inside: vaginal or anal; mouth: blowjob)
        "femdom_demand_inside.gwen": [
            _("When you cum, you cum inside me. Don't even think about pulling out. That's an order."),
            _("Pull out and you lose. Inside me. Every drop."),
            _("Here's the plan: you finish inside me. That's not up for discussion."),
        ],
        "femdom_demand_on_me.gwen": [
            _("When you cum, you pull out and paint me with it. I want to watch."),
            _("Not inside. On me. I want to see exactly what I did to you."),
            _("You're cumming on me, not in me. My canvas, my rules."),
        ],
        "femdom_demand_mouth.gwen": [
            _("When you cum, it goes in my mouth. Pull away and you'll regret it."),
            _("In my mouth. All of it. That's an order, not a request."),
            _("You're finishing in my mouth. I already decided, so don't bother arguing."),
        ],
        "femdom_demand_kept.gwen": [
            _("Right where I told you. Look at you, following the plan."),
            _("Exactly where I wanted it. See? You can be taught."),
            _("Perfect. Exactly as planned. I might even let you pick next time. ...Probably not."),
        ],
        "femdom_demand_broken.gwen": [
            _("That's not where I told you to cum. Not even close."),
            _("One order. I gave you one order, and you ignored it. Wow."),
            _("Wrong place. I've seen toddlers follow directions better."),
        ],

        # Me first
        "femdom_me_first.gwen": [
            _("Here's the deal: I cum first. You wait your turn."),
            _("Me first. You don't finish until I do. Think of it as a challenge."),
            _("Ladies first. Especially the lady giving the orders."),
        ],
        "femdom_me_first_kept.gwen": [
            _("Me first, just like I said. Okay, you pass."),
            _("You made me cum first. I'll admit it, that was good work."),
            _("That's the correct order. Me, then you. See? Everybody wins."),
        ],
        "femdom_me_first_broken.gwen": [
            _("You came before me. I said me first. That was literally the only rule."),
            _("Seriously? I told you I cum first, and you couldn't hold out. Selfish."),
            _("Wow. You crossed the finish line and left me at the start. Next time I cum first, or you don't cum at all."),
        ],

        # He came too fast (her profile's "humiliate"), any scene
        "femdom_humiliate_fast.gwen": [
            _("Already? Wow. That was less a performance and more a quick sketch."),
            _("That's it? I barely got started. I've had longer warm-ups."),
            _("Done already? Cute. We'll have to work on your stamina. A lot."),
        ],

        # He wants to leave her position (cowgirl / reverse cowgirl) for his
        "femdom_pos_refuse.gwen": [
            _("You want to take over? Cute. No. I'm comfortable up here."),
            _("Switch? I like the view from up here way too much. Stay put."),
            _("Request denied. I'm staying right here on top of you."),
        ],

        # Forced cum: a veteran on top keeps him inside (Cum.rpy)
        "femdom_force_cum.gwen": [
            _("Don't you dare pull out. You're cumming inside me. Now."),
            _("Stay right there. Every drop goes inside me, and you're not going anywhere."),
            _("You know by now how this ends. Inside me. Don't even try to wiggle out."),
        ],
        "femdom_force_cum_after.gwen": [
            _("There. That's where it belongs. Remember who decided that."),
            _("See? I always get what I want. You might as well stop fighting it."),
            _("Good. Next time, don't even pretend you're pulling out."),
        ],
    })
