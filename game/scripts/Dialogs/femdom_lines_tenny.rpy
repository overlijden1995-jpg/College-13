# ============================================================
# femdom_lines_tenny.rpy... Tenny's voice for the femdom trait (docs/plan_femdom.md, sections 3 and 6.4)
# ============================================================
#
# Keys: "femdom_<moment>.tenny". scene_pick_line puts her gid first among the modifiers, so these pools win over
# the shared ones in femdom_lines.rpy (same moments, same comments). Her voice (D4): shy and filthy AT THE SAME
# TIME. Every line starts shy / stuttering / apologizing and ends in the filthiest order; she argues with data.
#
# Discovery phase (D7): ".tenny.femdom_first" (her very first scene) and ".tenny.femdom_new" (her first few, may
# say "again") for refused / take_over / challenge. Every other pool also plays while she is discovering, so none
# of them talks like an old habit, except the veteran-only ones (forced, force_cum, force_cum_after).
# ============================================================

init 1 python:

    SCENE_LINES.update({

        # ══════════════════════════════════════════════════════════
        #  REFUSED: he said no to one of her requests (any scene, any request)
        # ══════════════════════════════════════════════════════════
        "femdom_refused.tenny": [
            _("I-I'm sorry, did you just tell me no? U-um... wrong answer. Right now I'm in charge of that cock, and it does what I say."),
            _("U-um... that wasn't a request. I-I should have been clearer. When I tell you what I want, you say yes, and you stay hard while you say it."),
            _("N-no? Okay... data point logged. You're a disobedient little toy, and I'm going to use you until you learn some manners."),
        ],
        "femdom_refused.tenny.femdom_first": [
            _("O-oh. You said no and I'm... angry? I-I've never wanted to boss anyone around before. Now I want to sit on your face until you say yes."),
            _("W-wait, I didn't know I had this in me... hearing you say no makes me furious. And wet. I-I want you doing exactly what I say."),
        ],
        "femdom_refused.tenny.femdom_new": [
            _("Y-you're ignoring me again... I-I'm starting to think I like giving orders way more than I should. Obey me, or I'll edge that cock until you beg."),
            _("U-um, again? My hypothesis keeps holding up: I love being in charge, and I hate being told no. Next time you say yes, or you don't get to cum at all."),
        ],

        # ══════════════════════════════════════════════════════════
        #  ORDERS: what she orders, and how it ends
        # ══════════════════════════════════════════════════════════

        # He stood up to her (any order)
        "femdom_defied_won.tenny": [
            _("O-okay... you win this one. I-I'm writing it down, though. Next time I'm sitting on your face until you apologize."),
            _("F-fine, your way. D-don't look so proud... watching you take charge just made me soaking wet, that's the only reason I'm letting it go."),
            _("U-um... okay. Sample size of one. Next round I'm pinning your wrists down and we're repeating the experiment until I win."),
        ],
        "femdom_defied_lost.tenny": [
            _("S-sorry, was that supposed to be you taking charge? That was adorable. Now shut up and let me use you."),
            _("U-um, no. Nice try. Be a good little toy and do it my way, or you don't cum at all."),
            _("I-I'm sorry, I shouldn't laugh... but you lost. Hypothesis confirmed: I'm in charge, and your cock is just my favorite lab equipment."),
        ],
        "femdom_obeyed.tenny": [
            _("G-good boy... just like that. You doing exactly what I say is making me drip."),
            _("Th-that's it... see how easy it is when you listen? Keep doing exactly what I say and maybe I'll let you cum."),
            _("U-um, thank you. Perfect. Keep that cock moving exactly like that, I-I'm grading this and you're getting an A."),
        ],

        # Take over: she gets on top (from doggy / full nelson / laying down)
        "femdom_take_over.tenny": [
            _("I-I'm sorry, I just... lie down. Now. I've been thinking about riding you since we started, and I'm done waiting."),
            _("U-um, could you... no. On your back. I'm getting on top and bouncing on that cock until you can't think."),
            _("S-sorry, change of plans. You, on your back. Me, on your cock. N-no questions."),
        ],
        "femdom_take_over.tenny.femdom_first": [
            _("W-wait, stop... I-I've never told anyone to do this before. On your back. I want to ride you. Now."),
            _("U-um, I want to be on top. I didn't know I'd ever say that out loud... lie down and let me sit on that cock."),
        ],
        "femdom_take_over.tenny.femdom_new": [
            _("O-on your back again, please... no, not please. Now. I-I'm starting to love being the one on top."),
            _("S-sorry, I'm taking over again... I keep finding out I like riding you way more than letting you drive."),
        ],
        # Veteran only: she shoved him onto his back anyway
        "femdom_forced.tenny": [
            _("I-I did say sorry... in my head. Now stay down. I'm riding you whether you like it or not."),
            _("U-um, you really thought you could stop me? That's so cute. Hands on my hips and shut up."),
            _("S-sorry, no is not an option anymore. Stay on your back like a good toy and let me fuck you."),
        ],

        # Challenge (he is moving inside her)
        "femdom_challenge.tenny": [
            _("U-um... is that it? I-I've run the numbers, and you can fuck me a lot harder than that. So do it. That's an order."),
            _("S-sorry, I'm getting bored. Prove it. Fuck me like you actually want me, or I'm taking over and doing it myself."),
            _("I-is this your maximum output? Because my data says there's more in you. Show me. Hard."),
        ],
        "femdom_challenge.tenny.femdom_first": [
            _("I-is that all...? Oh god, I just said that out loud. I've never talked to anyone like this. Now fuck me harder, I'm not asking."),
            _("U-um, harder? P-please... no, forget please. Harder. I didn't know bossing you around would make me this wet."),
        ],
        "femdom_challenge.tenny.femdom_new": [
            _("Th-that's all you've got, again? I-I'm learning I love pushing you. So push back. Fuck me harder."),
            _("S-sorry, I have to ask again... is that it? I keep finding out I like testing you. Pass the test and fuck me properly."),
        ],
        "femdom_challenge_met.tenny": [
            _("Oh god, yes... th-there it is. See? You just needed someone to tell you. G-good boy."),
            _("Th-that's more like it... hypothesis confirmed. You fuck so much better when I'm giving the orders."),
            _("Y-yes, like that... keep it up and I-I might let you cum. Might."),
        ],

        # Pace
        "femdom_pace_faster.tenny": [
            _("U-um, sorry, could you... no. Faster. Now. I want to be sore tomorrow."),
            _("F-faster... please. No, not please. Faster. Pound me like you mean it, I'm not asking twice."),
            _("S-sorry, this pace is statistically insufficient. Speed up before I get bored of your cock."),
        ],
        "femdom_pace_slower.tenny": [
            _("S-slow down... I-I'm sorry, I just want to feel every single inch. We go at my pace."),
            _("U-um, easy. Slower. Did I say you could rush? I want to savor that cock."),
            _("Sl-slower... you don't get to finish that fast. I say when this is over, and it's not over."),
        ],

        # "Don't you dare cum yet" (any scene: handjob, titjob, footjob, blowjob, any position)
        "femdom_no_cum.tenny": [
            _("U-um... you don't get to cum until I've used you properly. Statistically you'll last four more minutes. P-prove me wrong."),
            _("D-don't you dare cum yet. I-I'm sorry, I can feel you twitching... hold it. That cock is mine, and I decide when it empties."),
            _("W-wait, hold it. Hold it! I-I'm not done playing with you, and if you cum before I allow it, you'll regret it."),
        ],
        "femdom_edge_release.tenny": [
            _("O-okay... now. Cum for me. I-I want to watch you completely lose it."),
            _("G-good boy, you held it. Now let go... give me everything you saved up. All of it."),
            _("U-um... permission granted. Cum. Now. Don't make me say it twice."),
        ],
        "femdom_edge_kept.tenny": [
            _("Y-you waited exactly like I told you... that was so hot. Good boy."),
            _("Th-that's how it's done... you held it until I allowed it. I-I'm going to touch myself thinking about that later."),
            _("E-experiment successful... you're very trainable. I-I mean that as a compliment. Mostly."),
        ],
        "femdom_edge_broken.tenny": [
            _("I-I told you to wait. One instruction. You couldn't even hold it for me."),
            _("D-did I say you could cum? No. I didn't. N-next time you're going to beg on your knees for permission."),
            _("U-um... that was pathetic. I-I'm sorry, but it was. Zero self-control. We are fixing that."),
        ],

        # Where he cums
        "femdom_demand_inside.tenny": [
            _("U-um... when you cum, it goes inside me. All of it. I-I want to feel you fill me up. That's an order."),
            _("D-don't even think about pulling out. I-I'm sorry, I've already decided. You're cumming deep inside me."),
            _("W-when you finish... inside. Every drop. I want to walk around leaking you."),
        ],
        "femdom_demand_on_me.tenny": [
            _("W-when you cum, pull out and cum all over me. I-I want to see it. On my skin, not inside."),
            _("U-um, not inside. On me. I want to look down and see the mess I made you make."),
            _("S-sorry, rules: you pull out and you paint me with it. I-I want to be covered."),
        ],
        "femdom_demand_mouth.tenny": [
            _("Mmh... w-when you cum, it goes in my mouth. D-don't you dare pull away."),
            _("I-in my mouth. Every drop. I-I want to taste all of it, and you're going to watch."),
            _("U-um, just so we're clear... you cum on my tongue, nowhere else. That's an order."),
        ],
        "femdom_demand_kept.tenny": [
            _("E-exactly where I told you... g-good boy. You can follow instructions after all."),
            _("R-right where I wanted it... mmh, I can still feel it. Full marks."),
            _("S-see? You listen, and I get exactly what I want. Th-that's how this works."),
        ],
        "femdom_demand_broken.tenny": [
            _("Th-that is not where I told you to cum. I-I gave you one order. One."),
            _("W-wrong place. I-I was very specific. We're going to have a long talk about following instructions."),
            _("Y-you ignored me. I told you exactly where, and you just... did whatever you wanted. Unacceptable."),
        ],

        # Me first
        "femdom_me_first.tenny": [
            _("U-um, I... you don't cum until I do. I'm going first, and you're going to make it happen."),
            _("S-sorry, new rule: me first. You keep going until I'm shaking, then maybe you."),
            _("M-me first. My orgasm, then yours. That cock stays hard and working until I cum all over it."),
        ],
        "femdom_me_first_kept.tenny": [
            _("Mmh... me first, just like I said. G-good boy. You earned yours."),
            _("Y-you made me cum first... I-I'm still shaking. That's exactly the order I like."),
            _("Th-thank you... that was perfect. Me, then you. Just how I planned it."),
        ],
        "femdom_me_first_broken.tenny": [
            _("Y-you finished before me. I said me first. I-I was very clear."),
            _("U-um, excuse me? I'm dripping and nowhere near done, and you already came. That's so selfish."),
            _("I-I told you I come first. Next time you don't cum at all until I've had mine."),
        ],

        # He came too fast (her profile's "humiliate")
        "femdom_humiliate_fast.tenny": [
            _("A-already? I-I'm sorry, I'm not laughing... okay, I am. That was really fast."),
            _("U-um... that's it? I barely got started. I-I'm going to have to train that cock to last longer."),
            _("O-oh. That was... statistically below average. W-we'll work on your stamina."),
        ],

        # He wants to leave her position (cowgirl / reverse cowgirl) for his
        "femdom_pos_refuse.tenny": [
            _("U-um, no. I-I'm sorry, I'm comfortable right here, grinding on your cock. You stay under me."),
            _("S-switch? No. I'm on top, and I'm staying on top until I've had enough of you."),
            _("I-I know what you want... but no. My position, my pace, my rules. Stay down."),
        ],

        # Forced cum: a veteran on top keeps him inside (Cum.rpy)
        "femdom_force_cum.tenny": [
            _("U-um, where do you think you're going? S-sorry, no. You're cumming inside me. Right now."),
            _("D-don't move. I-I'm not letting you pull out. Every drop stays inside me."),
            _("Sh-shh... pull out? No. You finish where I say, and I say deep inside me."),
        ],
        "femdom_force_cum_after.tenny": [
            _("Th-that's where it belongs... I-I can feel you dripping out of me. Remember who decided that."),
            _("Mmh... all of it, inside. N-next time don't even think about pulling out."),
            _("S-see? I-I always get what I want in the end. And what I wanted was your cum inside me."),
        ],
    })
