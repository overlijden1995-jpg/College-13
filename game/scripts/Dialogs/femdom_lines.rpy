# ============================================================
# femdom_lines.rpy... lines of the femdom trait (docs/plan_femdom.md), read by scene_pick_line
# ============================================================
#
# Keys: "femdom_<moment>". scene_pick_line puts her gid first among the modifiers, so a per-girl voice is
# "femdom_<moment>.<gid>" and it wins over the shared pool (Gwen ironic and challenging, Rogue in her own tone,
# NTW bossy to the extreme and humiliating, Tenny shy and filthy at the same time, Shion by her stage).
# A pool that has to win over a scene's own generic pool is written WITH the scene ("femdom_<moment>.<scene>").
#
# Discovery phase (D7, trait_discovery_keys): "femdom_first" = the very first time she hears herself giving
# orders, "femdom_new" = her first few scenes. There she is finding out she LIKES being in charge: she can say
# so, but never talks like it is an old habit ("as always", "like I always tell you").
# ============================================================

init 1 python:

    SCENE_LINES.update({

        # ══════════════════════════════════════════════════════════
        #  REFUSED: he said no to one of her requests (femdom.rpy _femdom_refused_react)
        # ══════════════════════════════════════════════════════════
        "femdom_refused": [
            _("Excuse me? I wasn't asking."),
            _("Did you just say no to me? Cute. Don't make it a habit."),
            _("Wrong answer. You'll make that up to me."),
            _("I tell you what I want and you ignore it? Remember this moment."),
        ],
        "femdom_refused.femdom_first": [
            _("Hey... I told you what I wanted. Why does it bother me this much that you didn't listen?"),
            _("No? I... okay. Huh. I really didn't like hearing that."),
        ],
        "femdom_refused.femdom_new": [
            _("You keep ignoring what I say... and I keep hating it. I guess I like being the one in charge."),
            _("Again? I'm starting to learn something about myself, and you're not going to like it."),
        ],

        # ══════════════════════════════════════════════════════════
        #  ORDERS (femdom.rpy, F2): what she orders, and how it ends
        # ══════════════════════════════════════════════════════════

        # He stood up to her (any order)
        "femdom_defied_won": [
            _("Fine. You win this one. Don't get used to it."),
            _("Hmph. Look at you, taking charge. ...Okay. This time."),
            _("You're lucky that was hot. Next time I won't let you."),
        ],
        "femdom_defied_lost": [
            _("Cute. Now do it my way."),
            _("Nice try. Sit still and let me work."),
            _("That was adorable. You lose."),
        ],
        "femdom_obeyed": [
            _("Good. Just like that."),
            _("See how easy it is when you listen?"),
            _("That's it. Keep doing exactly what I say."),
        ],

        # ── Her orders against her Obed (femdom_order_mode, femdom.rpy; author 2026-10-09): from 800 Obed she
        # ASKS for the pace / the ride instead of ordering it, from 900 she PLEADS and his word is final. The
        # denied pools are what she swallows on a no; below 700 the plain order pools above play, no menu. ──
        "femdom_take_over_ask": [
            _("Let me get on top? I'll make it worth your while."),
            _("I want to ride you. Can I? Say yes."),
            _("Switch with me? Look at me, I'm asking nicely now."),
        ],
        "femdom_take_over_beg": [
            _("Please let me ride you... please? I'll be so good, I promise."),
            _("Can I get on top? Please? If you say no I'll behave... but please say yes."),
        ],
        "femdom_pace_faster_ask": [
            _("Can we go faster? Please say yes."),
            _("Faster? For me? I'm asking, not telling. ...Mostly asking."),
        ],
        "femdom_pace_slower_ask": [
            _("Slow down a little for me? Pretty please?"),
            _("Can we take it slower? I want to feel every second of it."),
        ],
        "femdom_pace_faster_beg": [
            _("Please go faster... please... I'm not above begging anymore. I'm begging."),
        ],
        "femdom_pace_slower_beg": [
            _("Please, slower... please... I just want it to last. But it's your call."),
        ],
        "femdom_ask_denied": [
            _("...Fine. Your call. I did ask nicely."),
            _("Okay, okay. We do it your way. This time."),
        ],
        "femdom_beg_denied": [
            _("...Okay. Whatever you want. I'm yours either way."),
            _("I understand... you decide. Just don't stop."),
        ],
        "femdom_beg_granted": [
            _("Thank you... thank you. You won't regret it."),
            _("See? I can be so good when you let me."),
        ],

        # ── His video on the table and she says yes (the ACCEPTED override in _blackmail_attempt): a canon
        # femdom gives in to the NERVE, never to the threat, and keeps the frame the whole way. ──
        "femdom_blackmail_accept": [
            _("Blackmail. You actually grew a spine. Fine, I'll play along, but understand one thing: I'm doing it because the audacity amuses me. I'm still the one in charge here."),
            _("Oh, you sweet idiot. That video buys you my yes, not my obedience. I'll do it for the sheer nerve of it. On my terms. Watch closely."),
            _("You think that makes you the boss? Adorable. You get your reward because bravery deserves one. But make no mistake, I still own this room."),
        ],

        # Take over: she gets on top
        "femdom_take_over": [
            _("Stop. On your back. I'm riding you now."),
            _("Enough of this. Lie down, I'm taking over."),
            _("My turn. Get under me."),
        ],
        "femdom_take_over.femdom_first": [
            _("Wait... lie down. I want to be on top. No, I'm not asking."),
            _("Get on your back. I... I've never said that to anyone. I like it."),
        ],
        "femdom_take_over.femdom_new": [
            _("On your back again. I'm starting to really like being the one on top."),
            _("Lie down. I'm getting used to giving you orders."),
        ],
        "femdom_forced": [
            _("I didn't ask. I told you."),
            _("That's better. Now stay there."),
            _("You really thought you had a choice?"),
        ],

        # Challenge
        "femdom_challenge": [
            _("Is that all you've got?"),
            _("Come on. You wanted me, so fuck me like you mean it. That's an order."),
            _("I'm getting bored. Prove me wrong."),
        ],
        "femdom_challenge.femdom_first": [
            _("Is that all? ...Huh. I didn't know I'd like pushing you around this much."),
            _("Come on, prove it. I've never talked to anyone like this. I kind of love it."),
        ],
        "femdom_challenge.femdom_new": [
            _("That's all you've got, again? I like watching you try harder for me."),
            _("Harder. I'm finding out I really like telling you what to do."),
        ],
        "femdom_challenge_met": [
            _("There it is. Good boy."),
            _("Better. Keep that up and I might reward you."),
            _("See? You just needed someone to tell you."),
        ],

        # Pace
        "femdom_pace_faster": [
            _("Faster. Now."),
            _("Speed up. I didn't say you could take it easy."),
            _("Faster. I'm not asking twice."),
        ],
        "femdom_pace_slower": [
            _("Slow down. We go at my pace."),
            _("Easy. Slower. I want to feel every second of this."),
            _("Did I say you could rush? Slow. Down."),
        ],

        # "Don't you dare cum yet"
        "femdom_no_cum": [
            _("Don't you dare cum yet."),
            _("You cum when I say. Not a second before."),
            _("Hold it. I'm not done with you."),
        ],
        "femdom_edge_release": [
            _("Now. Cum for me."),
            _("Okay. You've earned it. Let go."),
            _("Good boy. You can cum now."),
        ],
        "femdom_edge_kept": [
            _("You waited like I told you. Good."),
            _("That's how it's done. You held it until I let you."),
            _("See? Worth the wait, wasn't it?"),
        ],
        "femdom_edge_broken": [
            _("I told you to wait. You couldn't even do that."),
            _("Did I say you could cum? No. I didn't."),
            _("Pathetic. One simple order and you failed it."),
        ],

        # Where he cums
        "femdom_demand_inside": [
            _("When you cum, you cum inside me. That's an order."),
            _("Don't even think about pulling out. Inside."),
            _("You're finishing inside me. I already decided."),
        ],
        "femdom_demand_on_me": [
            _("When you cum, you pull out and cum on me. Understood?"),
            _("Not inside. On me. I want to see it."),
            _("You're cumming on my body, not inside. My rules."),
        ],
        "femdom_demand_mouth": [
            _("When you cum, it goes in my mouth. Don't pull away."),
            _("In my mouth. Every drop. That's an order."),
            _("You cum in my mouth, nowhere else."),
        ],
        "femdom_demand_kept": [
            _("Exactly where I told you. Good boy."),
            _("See? You can follow simple instructions."),
            _("Right where I wanted it. You're learning."),
        ],
        "femdom_demand_broken": [
            _("That's not where I told you to cum."),
            _("I gave you one order. One. And you ignored it."),
            _("Wrong place. We're going to talk about this."),
        ],

        # Me first
        "femdom_me_first": [
            _("You don't cum until I do. Got it?"),
            _("Me first. Then maybe you."),
            _("I cum first. That's how this works tonight."),
        ],
        "femdom_me_first_kept": [
            _("Me first, just like I said. Good boy."),
            _("You made me cum first. Now you get to feel good about yourself."),
            _("That's the order I like. Me, then you."),
        ],
        "femdom_me_first_broken": [
            _("You finished before me. I said me first."),
            _("Unbelievable. I told you I come first, and you couldn't wait."),
            _("Selfish. Next time you don't cum at all until I do."),
        ],

        # He came too fast (her profile's "humiliate")
        "femdom_humiliate_fast": [
            _("Already? That was fast. Pathetic."),
            _("That's it? I barely got started."),
            _("Wow. I'll have to train you to last longer."),
        ],

        # He wants to leave her position for his
        "femdom_pos_refuse": [
            _("On my knees? Cute. No. I'm staying on top."),
            _("You want to switch? I don't. Stay where you are."),
            _("I'm comfortable up here. You'll stay under me."),
        ],

        # Forced cum: a veteran on top keeps him inside (Cum.rpy)
        "femdom_force_cum": [
            _("Don't move. You're cumming inside me. Now."),
            _("Every drop stays inside me. I'm not letting you go."),
            _("Pull out? No. You finish where I say."),
        ],
        "femdom_force_cum_after": [
            _("That's where it belongs. Remember who decided."),
            _("Good. Next time don't even think about pulling out."),
            _("See? I get what I want."),
        ],
    })
