# ============================================================
# stepmom_sex_lines.rpy... the sex menu voice of the "stepmom" ROLE
# (docs/plan_shion.md; GIRL_SEX_LINES["role:stepmom"], read in Chat/interactions.rpy)
# ============================================================
#
# A role is what a girl IS in the player's life (GIRLS_CONFIG[gid]["role"], girl_role_key -> "role:stepmom").
# The author's decision: "exclusive variants for characters with the stepmom profile; other characters can take that
# role later, so the lines must be specific." Today only Shion holds it. Her own table (shion_sex_lines.rpy) is read
# FIRST: these lines are what she says where she has none of her own, and what any future stepmom says.
#
# The voice is the ROLE, never one character: a mature, experienced woman married to his father. The taboo (your
# father, your stepmother, I'm married), authority, composure. No name, no job, no money, no girlfriend talk (that is
# each girl's "pgf" moods), never a college girl's life. It has to fit a cold, commanding stepmother AND a warmer one:
# confident and in control either way (a cute_sex stepmom is tender and slow, never bashful).
#
# What is here (the shared pools say "We barely know each other!" / "What kind of girl do you think I am?", false
# for her):
#   - "<mood>.<trait>": her voice about one of her traits (_sex_response_line step 0: her own "<mood>.<trait>", then
#     these, then the shared TRAIT_COMBO_LINES / TRAIT_SINGLE_LINES). One slot for every (mood, act) where the shared
#     lines speak for that trait, alone or in any combo she can have (combos with virgin / loyal / cheater / nerd left
#     out: a stepmom is never a virgin or a student, and loyal / cheater need her own NPC partner). Every line keeps
#     the meaning of the shared lines it replaces (accept vs deny, what the trait implies), and speaks for that ONE
#     trait: a trait line also plays when she has no other trait of the combo.
#     The guards of step 0 hold: public_fetish / public_shy / exhibitionist only in public, camera_lover only while
#     recording (so only those lines name a public place or a camera that is on). camera_hater has no guard: its
#     lines are about proof and secrecy, true anywhere.
#     "accepted.<trait>" also answers the first time (step 0 runs before "accepted_first"): no line claims a first
#     time or a repeat. Eager traits (cum_slut, hardcore_sex) want and demand, they never claim a history.
#     Acts: only where the shared trait lines have one (masturbate, hj, tj, bj, sex). No kiss / anal / oral (only the
#     nerd pools have them), no fj (no shared trait line for it).
#   - "stranger": the "offended" gates (an absurd request at low stats: the deny handler, the tip check, the sex
#     check). Acts "tip" / "sex" / "anal", and "_any" (any other act, so those lines never name one).
#   - "skip": a skipped step (_skip_step_deny_line), act = the _SKIP_STEP_LINES context; "skip.<trait>" where the
#     shared pools have that trait in that context. A line says only what its context guarantees:
#     bj_before_kiss = no kiss; sex_before_kiss = no kiss, no hj / bj / tj; sex_before_oral = a kiss, no hj / bj / tj;
#     anal_before_vaginal = hj or bj done, no sex; anal_before_everything = no sex, no hj, no bj.
#     As in the shared pools, hardcore_sex welcomes the skip and anal_lover wants it, just not cold. (Today
#     _skip_step_penalty clears the context for a hardcore_sex girl and is never asked about "bj": those lines wait
#     for the day that changes.)
# ============================================================

init 1 python:

    GIRL_SEX_LINES["role:stepmom"] = {

        # ══════════════════════════════════════════════════════════
        #  CAMERA HATER (no guard: secrecy and proof, true anywhere)
        # ══════════════════════════════════════════════════════════
        "accepted.camera_hater": {
            "masturbate": [
                _("You can watch. Only watch. No phone, no pictures, and not a word to anyone."),
                _("Fine. Watch all you like. But no pictures, and it never leaves your head."),
                _("Sit. Watch. And if a single picture of this ever exists, I'll know who took it."),
            ],
            "hj": [
                _("Fine. My hand, and nothing else. No phone, no pictures, no proof."),
                _("Very well. But this never happened, do you understand me? Not a word to your father."),
                _("Put that phone away first. Then you can have my hand."),
            ],
            "tj": [
                _("Fine. But that phone goes face down. No pictures of these, ever."),
                _("Very well. And these are not something you describe to your friends."),
                _("Fine. Not a word of this to anyone. Especially not your father."),
            ],
            "bj": [
                _("Fine. But that phone stays in your pocket. There will be no proof of this, ever."),
                _("Very well. And this stays between us. Your father never hears a word of it."),
                _("Fine. No pictures, no stories, no bragging. I have a marriage to protect."),
            ],
            "sex": [
                _("Fine. But this stays between us. No phone, no pictures, and your father never knows."),
                _("Very well. And understand me: there will never be any proof that this happened."),
                _("Fine. I'm a married woman. What happens here stays here, completely."),
            ],
        },
        "hard_deny.camera_hater": {
            "masturbate": [
                _("A show? So you can film it the moment I look away? No."),
                _("No. What I do in private stays private. It will never end up on anyone's phone."),
                _("Absolutely not. I don't perform for a boy with a camera in his pocket."),
            ],
            "hj": [
                _("No. I'm not putting my hands on you and leaving you something to brag about."),
                _("Absolutely not. Things like that get out, and I don't let things get out."),
                _("No. Your father's wife does not leave evidence lying around."),
            ],
            "tj": [
                _("No. These are not ending up in anyone's photo gallery."),
                _("Absolutely not. I know exactly what boys do with their phones."),
                _("No. And don't even think about taking a picture of me like that."),
            ],
            "bj": [
                _("No. I don't hand anyone something they could hold over me. Least of all my husband's son."),
                _("Absolutely not. One photo, one careless word, and my marriage is over."),
                _("No. Do you have any idea what would happen if anyone ever found out?"),
            ],
            "sex": [
                _("No. I'm a married woman, and I'm not handing anyone proof of anything."),
                _("Absolutely not. Do you know what it would cost me if this ever got out?"),
                _("No. Your father would find out. Things like this always leave a trail."),
            ],
        },
        "tempted_deny.camera_hater": {
            "sex": [
                _("Don't think I'm not tempted. But if this ever got out... no. Not yet."),
                _("I want to. That's the problem. I need to be sure nobody ever finds out first."),
                _("Not yet. When I'm certain this stays between us... then we'll see."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  CAMERA LOVER (only while he is recording)
        # ══════════════════════════════════════════════════════════
        "accepted.camera_lover": {
            "masturbate": [
                _("Keep recording. Consider it a private screening, just for you."),
                _("Film all of it. I want you to watch this again when you're alone."),
                _("The camera stays on me. Don't you dare miss a second."),
            ],
            "hj": [
                _("Keep filming. I want a record of how easily my hand undoes you."),
                _("Camera on? Good. Watch what your father's wife can do with one hand."),
                _("Hold it steady. If we're doing this, it's going to look perfect."),
            ],
            "tj": [
                _("Point that camera here. These deserve a proper close-up."),
                _("Film it. I want to see how you look between them."),
                _("Keep recording. You'll want to remember this."),
            ],
            "bj": [
                _("Keep the camera on my face. I want you to see exactly how good your stepmother is at this."),
                _("Recording? Good. Frame it properly. I don't do anything halfway."),
                _("Film it. Something to watch every time you see me standing next to your father."),
            ],
            "sex": [
                _("Leave the camera running. I want to see how we look together."),
                _("Film it. And make sure my good side is in the shot."),
                _("Keep it running. Every time you watch it, remember whose wife you had."),
            ],
        },
        "tempted_deny.camera_lover": {
            "masturbate": [
                _("A recording of that? I'd enjoy it far too much. Ask me another day."),
                _("On camera... don't think I'm not tempted. Not yet."),
                _("Keep that camera ready. Just not today."),
            ],
            "hj": [
                _("My hand on you, on film... I've thought about it. Not yet."),
                _("Tempting. Very tempting. Put the camera down for now."),
                _("Not today. But keep that camera charged."),
            ],
            "tj": [
                _("Filming these? I like the idea more than I should. Not today."),
                _("On camera... God. No. Not yet."),
                _("Not yet. But I can see you already have the angle picked out."),
            ],
            "bj": [
                _("With the camera on? Tempting... very tempting. Not yet."),
                _("You filming me doing that... don't tempt me. Not today."),
                _("Not yet. But keep that camera close. I might change my mind."),
            ],
            "sex": [
                _("On camera... God, I want that. But not yet."),
                _("Tempting. You and me, on film... ask me another day."),
                _("Not today. But I'm thinking about how we'd look on that screen."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  CUM SLUT (she wants it; never claims a history)
        # ══════════════════════════════════════════════════════════
        "accepted.cum_slut": {
            "masturbate": [
                _("Watch me. I'm this wet just thinking about how you taste."),
                _("Sit and watch. I'm going to touch myself thinking about you cumming for me."),
                _("Look how wet I am already. That's what the thought of you does to your stepmother."),
            ],
            "hj": [
                _("Give it here. I want to feel you throb in my hand when you finish."),
                _("Yes. And when you cum, I want to watch every drop of it."),
                _("Let me. I want it all over my hand, and I want to see it happen."),
            ],
            "tj": [
                _("Put it between them. I want you to cover me."),
                _("Yes. And when you finish, I want it all over my chest."),
                _("Come here. I want to feel you throb between them, right to the end."),
            ],
            "bj": [
                _("Give it to me. I want every drop, and I'm not wasting any of it."),
                _("Yes. In my mouth. Don't you dare pull away when you finish."),
                _("Come here. I want to taste you, and I want all of it."),
            ],
            "sex": [
                _("Yes. I need you inside me, and I want everything you've got."),
                _("Finally. Get inside me, and don't hold anything back."),
                _("Yes. And when you finish, I want to feel all of it."),
            ],
        },
        "tempted_deny.cum_slut": {
            "masturbate": [
                _("I'm already wet thinking about you... which is exactly why not. Not yet."),
                _("If I start touching myself in front of you, I won't stop there. Not today."),
                _("Don't look at me like that. I want to, and I'm still saying no."),
            ],
            "hj": [
                _("I want to feel you finish in my hand... no. Not yet."),
                _("Stop. I can almost feel you throbbing in my hand already. Not today."),
                _("Tempting. Far too tempting. Ask me another time."),
            ],
            "tj": [
                _("I want you finishing all over them... no. Not yet."),
                _("Tempting. I can almost feel you there. Still no."),
                _("Stop staring at them. I want it too, and I'm still saying no."),
            ],
            "bj": [
                _("I want to taste you. God help me, I do. But not yet."),
                _("Don't tempt me... my mouth is watering, and the answer is still no. For now."),
                _("You have no idea what I'd give to... no. Not today."),
            ],
            "sex": [
                _("I want you inside me more than I'll ever admit. But not yet."),
                _("Don't. I'm your father's wife, and I'm this close to forgetting it. Not today."),
                _("I want every drop of you... and that's exactly why I'm saying no. For now."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  CUTE SEX (tender and slow, never bashful)
        # ══════════════════════════════════════════════════════════
        "accepted.cute_sex": {
            "masturbate": [
                _("Stay close. Watch me, and don't rush me. I like it slow."),
                _("Sit with me. I want you near me while I do this."),
                _("Slowly... just watch. I want you to see what feels good to me."),
            ],
            "hj": [
                _("Come here. Let me do this slowly. I want to feel every bit of you."),
                _("Relax. Breathe. I'll take care of you."),
                _("Slowly... there's no hurry. I want to enjoy this too."),
            ],
            "tj": [
                _("Come here. Gently... let me take care of you."),
                _("Slowly. I want to feel you between them, and I want to take my time."),
                _("Relax. Let me do this my way. Slow and soft."),
            ],
            "bj": [
                _("Come here. Slowly... let me take my time with you."),
                _("Relax. Let me be gentle with you. There's no rush."),
                _("Lie back. I'm going to do this slowly, and you're going to let me."),
            ],
            "sex": [
                _("Come here. Slowly... hold me, and don't rush."),
                _("Gently. I want to feel all of you, one slow inch at a time."),
                _("Yes. But slowly, and look at me while we do this."),
            ],
        },
        "soft_deny.cute_sex": {
            "hj": [
                _("Not now. I don't like being rushed, and right now you're rushing me."),
                _("Give me a little time. I'd rather wait than do it in a hurry."),
                _("Not yet. Be patient with me. It will be worth it."),
            ],
            "sex": [
                _("Not yet. I want it slow and I want it right, and today isn't that day."),
                _("Slow down. I need a little more time. You can give me that."),
                _("Not today. Be patient with me. I'll let you know when."),
            ],
        },
        "tempted_deny.cute_sex": {
            "masturbate": [
                _("I've thought about letting you watch... not yet."),
                _("Not today. Be patient, and maybe next time I'll let you stay."),
                _("I want to... slowly, with you right there. Just not yet."),
            ],
            "hj": [
                _("I want to touch you... slowly... but not yet."),
                _("Don't rush me. I'm closer than you think. Not today."),
                _("Mmm... tempting. Give me a little more time."),
            ],
            "tj": [
                _("Tempting... slowly, gently... but not yet."),
                _("Not today. Be patient with me. It won't be long."),
                _("I want to... just not yet. Soon."),
            ],
            "bj": [
                _("I'd like that more than I should... not yet. Be patient with me."),
                _("Not today. When I do, I want to take my time with you."),
                _("Tempting... but no. Soon, maybe. And slowly."),
            ],
            "sex": [
                _("Slowly, gently... God, I want that. Not yet."),
                _("Not today. When I say yes, I want all the time in the world with you."),
                _("Don't push. I'm almost there, and I don't want it rushed."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  EXHIBITIONIST (only in public)
        # ══════════════════════════════════════════════════════════
        "accepted.exhibitionist": {
            "masturbate": [
                _("Watch me. You, and anyone else who happens to look."),
                _("Right here, in the open. Let them see what a grown woman looks like."),
                _("Let them stare. An audience only makes it better."),
            ],
            "hj": [
                _("Right here. Let anyone who walks by see where my hand is."),
                _("Let them look. I have nothing to hide, and now neither do you."),
                _("In the open? Perfect. I want them watching what I do to you."),
            ],
            "tj": [
                _("Right here, in the open. Let them see you between them."),
                _("Let them stare. They can look all they like. Only you get to touch."),
                _("Out here? Good. I want an audience for this."),
            ],
            "bj": [
                _("Right here? Good. Let them watch your stepmother take care of you."),
                _("Let them stare. I want every one of them to know exactly what I'm doing."),
                _("Here, in the open. I don't care who sees. Actually, I hope they do."),
            ],
            "sex": [
                _("Right here. Let everyone see who's fucking your father's wife."),
                _("In the open? Good. I want them to hear every sound I make."),
                _("Let them watch. Let them talk. I want to be seen."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  FEMDOM (Shion has her own for all four slots; a future stepmom hears these)
        # ══════════════════════════════════════════════════════════
        "accepted.femdom": {
            "hj": [
                _("Sit. Hands at your sides. My hand, my pace, my rules."),
                _("Give it here. I decide how fast this goes, and when it ends."),
                _("Don't move. I want to watch you beg your stepmother for more."),
            ],
            "bj": [
                _("Sit down and keep your hands to yourself. I set the pace."),
                _("Lie back. You finish when I say so, and not a second before."),
                _("Stay still. You'll take it exactly the way I give it."),
            ],
        },
        "hard_deny.femdom": {
            "hj": [
                _("My hand is something you earn. You haven't."),
                _("No. You'll get it when I decide you deserve it, not when you ask."),
                _("Not yet. Show me you can behave first."),
            ],
            "sex": [
                _("No. I decide when, and it isn't today."),
                _("You don't ask me for that. I choose when, and today I choose no."),
                _("Not happening. You haven't earned anything close to that."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  HARDCORE (she demands it rough; never claims a history)
        # ══════════════════════════════════════════════════════════
        "accepted.hardcore_sex": {
            "masturbate": [
                _("Eyes on me. Don't you dare look away."),
                _("Watch closely. I don't hold back, not even with an audience."),
                _("Sit. Watch. And try not to embarrass yourself."),
            ],
            "hj": [
                _("Give it here. Fast and hard. I don't do gentle."),
                _("Sit back. I'm not going to be delicate about this."),
                _("Hard and fast. Try to keep up."),
            ],
            "tj": [
                _("Put it between them. And don't you dare be gentle."),
                _("Go on. Use them. Hard."),
                _("You'd better enjoy these. I'm not going easy on you."),
            ],
            "bj": [
                _("Don't be gentle with me. I can take it."),
                _("Deep and rough. And don't you dare hold back on my account."),
                _("Hard. I'm not made of glass."),
            ],
            "sex": [
                _("Hard. Don't you dare treat me like I'm fragile."),
                _("Take me, and don't be gentle about it."),
                _("Do it properly. Hard, deep, and no holding back."),
            ],
        },
        "hard_deny.hardcore_sex": {
            "masturbate": [
                _("No. And trust me, you're not ready to see me let go."),
                _("No. I don't put on shows for boys who couldn't keep up."),
                _("Not a chance. What I do alone would be far too much for you."),
            ],
            "hj": [
                _("My hand? No. You couldn't handle my grip."),
                _("Not a chance. And I wouldn't go easy on you, either."),
                _("No. You'd last ten seconds, and I'd be bored."),
            ],
            "tj": [
                _("No. You'd be done in a minute, and I'd be disappointed."),
                _("Not a chance. You couldn't handle them."),
                _("No. I don't waste them on someone who can't take it rough."),
            ],
            "bj": [
                _("No. You couldn't handle what I'd do to you."),
                _("My mouth? No. You'd be finished before I even started."),
                _("No. You're not ready for the way I do that."),
            ],
            "sex": [
                _("No. You couldn't keep up with me."),
                _("Not happening. You're far too soft for a woman like me."),
                _("No. I'd break you, and your father would ask questions."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  HATE CUM (yes to the act, never to the mess)
        # ══════════════════════════════════════════════════════════
        "accepted.hate_cum": {
            "masturbate": [
                _("Fine. At least this way there's no mess to worry about."),
                _("Watch, then. Nothing of yours ends up on me this way."),
                _("Fine. Just watch. And keep your hands, and everything else, to yourself."),
            ],
            "hj": [
                _("Fine. But you warn me before you finish. I mean it."),
                _("Very well. And if any of it gets on me, we're done."),
                _("Fine. Aim it away from me, or you'll regret it."),
            ],
            "tj": [
                _("Fine. But when you finish, you aim away from me."),
                _("Very well. And not a drop on my chest. I mean it."),
                _("Fine. But warn me before you finish, or you'll regret it."),
            ],
            "bj": [
                _("Fine. But you warn me before you finish. Not a drop in my mouth."),
                _("Very well. And when you're close, you tell me. I'm not swallowing anything."),
                _("Fine. But the ending happens nowhere near my mouth. Understood?"),
            ],
            "sex": [
                _("Fine. But if you make a mess on me, I swear..."),
                _("Very well. And you'd better use protection. I'm not cleaning up after you."),
                _("Fine. But you finish nowhere near me. Understood?"),
            ],
        },
        "hard_deny.hate_cum": {
            "masturbate": [
                _("A show, so you can make a mess watching me? Disgusting. No."),
                _("No. I'm not performing so you can spray yourself everywhere."),
                _("Absolutely not. I know what you'd be doing while you watched."),
            ],
            "hj": [
                _("No. I'm not letting you make a mess on my hands."),
                _("Absolutely not. I know exactly how that ends."),
                _("No. Your mess, my hand? Never."),
            ],
            "tj": [
                _("No. You'd finish all over my chest, and that's revolting."),
                _("Absolutely not. I'm not letting you leave your mess on me."),
                _("No. I know how that ends, and I want nothing to do with it."),
            ],
            "bj": [
                _("Absolutely not. I know where that ends, and it's not ending in my mouth."),
                _("No. I don't want that anywhere near my mouth, or what comes after it."),
                _("No. The thought of how that finishes is enough to put me off."),
            ],
            "sex": [
                _("No. And if you even think about making a mess of me, forget it."),
                _("Not unless it stays wrapped. And even then, not today."),
                _("Absolutely not. I know exactly where that leads, and I want none of it."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  PUBLIC FETISH (only in public)
        # ══════════════════════════════════════════════════════════
        "accepted.public_fetish": {
            "masturbate": [
                _("Right here. Let them catch me, if they dare."),
                _("The risk of being seen... I can't resist it."),
                _("Anyone could walk past and see me. That's the whole point."),
            ],
            "hj": [
                _("Out here, where anyone could see? Even better."),
                _("Someone might see my hand on you... good."),
                _("If anyone who knows your father walks by... God, that's exciting."),
            ],
            "tj": [
                _("Here? Out in the open? Get over here before I change my mind."),
                _("Anyone could see us. Good. Let them."),
                _("Right here, where someone might catch us. Yes."),
            ],
            "bj": [
                _("Right here? Where anyone could walk by? ...Yes. Come here."),
                _("Anyone could catch your stepmother like this. That's exactly why I'm saying yes."),
                _("Here, in the open. My heart is racing, and I love it."),
            ],
            "sex": [
                _("Here, where anyone could catch us? ...Yes. Right now."),
                _("A married woman, caught in public with her husband's son... God, yes. Do it."),
                _("The risk of being seen makes this so much better. Hurry."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  PUBLIC SHY (only in public)
        # ══════════════════════════════════════════════════════════
        "accepted.public_shy": {
            "masturbate": [
                _("Here? My heart is pounding... fine. Watch me, and watch for anyone else."),
                _("If anyone sees me doing this, I'll never forgive you. ...Fine."),
                _("God, I must be losing my mind. Fine. Quickly."),
            ],
            "hj": [
                _("Here? ...Fine. Quickly, and keep watch."),
                _("If someone walks by, you stop. Instantly. Understood?"),
                _("This is insane... fine. But stand where nobody can see."),
            ],
            "tj": [
                _("Out here? ...Fine. Quickly, and stand in front of me."),
                _("If anyone sees me like this... fine. Just be quick."),
                _("My heart is racing. Fine. But you keep an eye out."),
            ],
            "bj": [
                _("Here? ...Fine. Quickly, and keep watch for anyone coming."),
                _("If anyone sees me like this, my marriage is over. So be quick about it."),
                _("God, this is reckless... fine. But you keep your eyes open."),
            ],
            "sex": [
                _("Here? Someone could see us... fine. Quickly, before I come to my senses."),
                _("If anyone recognizes me... God. Fine. Just be fast."),
                _("This is terrifying. And I'm saying yes anyway. Hurry."),
            ],
        },
        "hard_deny.public_shy": {
            "masturbate": [
                _("Touch myself here? Where people could see? Have you lost your mind?"),
                _("No. Not in public. Not ever."),
                _("In the open? I would never recover from that. No."),
            ],
            "hj": [
                _("Here? Where anyone could walk by? Never."),
                _("No. Not where someone could see my hand on you."),
                _("Absolutely not. Someone who knows your father could be anywhere."),
            ],
            "tj": [
                _("My chest out, here? Where anyone could see? No."),
                _("Absolutely not. Not in public, not like that."),
                _("Here? Are you trying to get me caught? No."),
            ],
            "bj": [
                _("Here? Where anyone could see me on my knees? Absolutely not."),
                _("In public? Do you have any idea what would happen if someone recognized me?"),
                _("No. I'm not risking everything so a stranger can watch."),
            ],
            "sex": [
                _("In public? Where someone could see us? Are you trying to ruin me?"),
                _("No. Being seen is the one thing I will never risk."),
                _("Absolutely not. A married woman, caught in public with her stepson? Never."),
            ],
        },
        "soft_deny.public_shy": {
            "sex": [
                _("Not here. Someone might see us."),
                _("No... not in public. I couldn't bear being seen."),
                _("Somewhere private, maybe. Not here."),
            ],
        },
        "tempted_deny.public_shy": {
            "masturbate": [
                _("I want to... but here? Where someone could hear me? No."),
                _("Not out here. I'd never forgive myself if someone saw."),
                _("Tempting. But not where strangers could walk by."),
            ],
            "hj": [
                _("What if someone walks by and sees my hand on you?"),
                _("I want to, but I can't risk being seen doing this."),
                _("Not here. Somewhere nobody could possibly see us... then maybe."),
            ],
            "tj": [
                _("Here? My chest out in public? I can't. Not here."),
                _("I want to... but someone could see me. Not here."),
                _("Not out here. Take me somewhere private and ask me again."),
            ],
            "bj": [
                _("I want to... but here? Someone could see me. Not here."),
                _("Don't tempt me out here. Anyone could walk by."),
                _("Not here. If someone caught me on my knees... no."),
            ],
            "sex": [
                _("Not here... anyone could see us. Not here."),
                _("I want you. But this place is far too exposed."),
                _("God, I want you... but not here. Not where people can see."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  VOYEUR (she has been watching him)
        # ══════════════════════════════════════════════════════════
        "accepted.voyeur": {
            "masturbate": [
                _("You want to watch me? I've watched you often enough. Fair is fair."),
                _("You've caught me looking often enough. Might as well give you something to look at."),
                _("I've seen plenty of you. Now you can see what I do when nobody's looking."),
            ],
            "hj": [
                _("I've spent long enough staring at it. Now let me touch it."),
                _("I've watched you when you thought nobody was looking. My hands want their turn."),
                _("I've been watching how you like it. Come here, let me show you what I learned."),
            ],
            "bj": [
                _("I've watched you more than a stepmother should. Now I want you in my mouth."),
                _("Watching you isn't enough anymore. Come here."),
                _("I've spent far too long looking at you. Let me have a taste."),
            ],
            "sex": [
                _("I've watched you long enough. Now I want to feel you."),
                _("Watching was never going to be enough. Come here."),
                _("I've watched you far too long for a woman in my position. Get over here."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  STRANGER: an absurd request at low stats (the "offended" gates). She is not a stranger: she is his
        #  father's wife. "_any" = any other act (never names one).
        # ══════════════════════════════════════════════════════════
        "stranger": {
            "tip": [
                _("'Just the tip'? From my husband's son? You must think I'm a fool."),
                _("Excuse me? I'm your father's wife. Not the tip, not anything. Ever."),
                _("The audacity. You think a little wordplay makes that acceptable? Get out of my sight."),
            ],
            "sex": [
                _("Excuse me? I'm your father's wife. Have you completely lost your mind?"),
                _("Sex? With me? I'm your stepmother. Say that again and your father hears every word."),
                _("Do you hear yourself? I am married to your father. Never speak to me like that again."),
            ],
            "anal": [
                _("You want WHAT? From your father's wife? Have you no shame at all?"),
                _("Have you lost your mind? I'm your stepmother, not one of your college girls."),
                _("That is the most vulgar thing anyone has ever said to me. And from my husband's son."),
            ],
            "_any": [
                _("Excuse me? I'm your stepmother. Remember that before you open your mouth again."),
                _("Have you forgotten who you're talking to? I'm married to your father."),
                _("The nerve. I'm your father's wife, and you'll speak to me with some respect."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  SKIP: he skipped a step (act = the _SKIP_STEP_LINES context)
        # ══════════════════════════════════════════════════════════
        "skip": {
            "bj_before_kiss": [
                _("You haven't so much as kissed me, and you want my mouth on you? Know your place."),
                _("Not even a kiss, and you ask your stepmother for that? Slow down."),
                _("A blowjob, before you've even kissed me? You're getting ahead of yourself."),
            ],
            "sex_before_kiss": [
                _("Sex? You haven't even kissed me. I'm not some girl you picked up at a party."),
                _("You haven't so much as kissed me, and you want to take your father's wife to bed? No."),
                _("You skip every step and go straight to that? That's not how it works with a grown woman."),
            ],
            "sex_before_oral": [
                _("A kiss or two, and you think you've earned my bed? Slow down."),
                _("You haven't had my hand or my mouth yet, and you want all of me? Not so fast."),
                _("Straight to sex? A grown woman likes to be worked up to it."),
            ],
            "anal_before_vaginal": [
                _("My ass, before you've even had the rest of me? You're getting ahead of yourself."),
                _("Anal, before we've even had sex? Slow down, young man."),
                _("You haven't even had me properly yet, and you ask for that? Bold."),
            ],
            "anal_before_everything": [
                _("My ass? You haven't had my hand or my mouth, let alone the rest of me. No."),
                _("Straight to my ass, skipping everything that should come first? Absolutely not."),
                _("You haven't earned my hand yet, and you ask your stepmother for that? Out of the question."),
            ],
        },
        # Hardcore welcomes the skip (as the shared pool does)
        "skip.hardcore_sex": {
            "bj_before_kiss": [
                _("No kiss, straight to my mouth? Bold. I like that in a man."),
                _("Skipping the kiss? You've got nerve... fine."),
            ],
            "sex_before_kiss": [
                _("No kiss, no foreplay, straight to it? You don't waste time. I respect that."),
                _("Straight to the point. Good. I hate wasting time."),
            ],
            "sex_before_oral": [
                _("Skipping the warmup? Good. I didn't want one."),
                _("Straight to it? That works for me."),
            ],
            "anal_before_vaginal": [
                _("My ass before the rest of me? Filthy. I like it."),
                _("Anal, before you've even had my pussy? Filthy. I approve."),
            ],
            "anal_before_everything": [
                _("No sex, not even my hand, and straight to my ass? You're insane. ...I'm in."),
                _("No warmup, straight there? Bold. Let's see if you can handle it."),
            ],
        },
        # Tender and slow: too fast is a no (never bashful)
        "skip.cute_sex": {
            "bj_before_kiss": [
                _("Not even a kiss first? No. I like to be kissed before anything else."),
                _("You haven't kissed me yet. Start there, slowly, and we'll see."),
            ],
            "sex_before_kiss": [
                _("You haven't even kissed me, and you want all of me? No. Slowly."),
                _("Start with a kiss. Nothing else happens before that."),
            ],
            "sex_before_oral": [
                _("Already? We've barely started. Slow down."),
                _("Not yet. I like to take my time, and you're rushing past all of it."),
            ],
            "anal_before_vaginal": [
                _("My ass? We haven't even made love yet. No. Slowly."),
                _("Not that, not before you've had the rest of me. Slow down."),
            ],
            "anal_before_everything": [
                _("That, before my hand or my mouth? No. We start slowly, the way I like it."),
                _("You're rushing past everything that matters. Absolutely not."),
            ],
        },
        "skip.anal_hater": {
            "anal_before_vaginal": [
                _("My ass? Before you've even had sex with me? Absolutely not. I hate even the thought of it."),
                _("You skip straight past sex to the one thing I can't stand? No."),
                _("That is the last thing I'd ever give you, and you want it before we've even had sex? Never."),
            ],
            "anal_before_everything": [
                _("You start with the one thing I hate most? Over my dead body."),
                _("You haven't had my hand or my mouth, and you want the thing I hate most? Never."),
            ],
        },
        # She wants it, just not cold (a denial, as the shared pool)
        "skip.anal_lover": {
            "anal_before_everything": [
                _("I'd enjoy that... but you're going to warm me up first. Properly."),
                _("Tempting. But nobody goes straight there with me. Work your way to it."),
                _("I want it. But not like this, not cold. Do something else first."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  STORY_LOCKED.<step>: an act her step does not open yet (story_steps.rpy, story_locked_line), whatever her
        #  stats. Never claims anything happened between them; "_any" = any act (never names one). "<mood>.<trait>"
        #  = that trait's tone, tried first per act key (the act key beats a trait's "_any": story_locked_line).
        #  The cold pools never hint, never promise, never say "yet": being asked at all is the offense.
        # ══════════════════════════════════════════════════════════
        # her husband is in the room with them (family_father.rpy): whatever her step, not in front of him. This
        # shared pool is the two of them hiding something: steps 1+ only (story_locked_line skips it on her first
        # step, where "story_locked.husband_here.cold" speaks instead)
        "story_locked.husband_here": {
            "_any": [
                _("Your father is RIGHT there. Have you lost your mind?"),
                _("Not with him in the room. Not ever."),
                _("Lower your voice. And keep your hands where he can see them."),
                _("...Later. When he isn't three feet away."),
            ],
            "outing": [
                _("In front of him? We leave separately, or not at all."),
                _("Not together. Not where he can watch us leave."),
            ],
        },
        # ...on her first step: there is nothing between them, and he asks THAT with his father in the room
        "story_locked.husband_here.cold": {
            "_any": [
                _("Your father is sitting RIGHT there. Say that again and I'll make sure he hears every word."),
                _("Have you lost your mind? That man is your FATHER. And I am his WIFE."),
                _("I'm going to assume that was a very bad joke. For your sake. Now be quiet."),
                _("Not another word. If I repeated what you just said, this family would be over by dinner."),
            ],
            "outing": [
                _("Go somewhere? With you? Your father is right here. Ask HIM to entertain you."),
                _("No. Family outings happen when I schedule them, and I didn't."),
            ],
        },
        "story_locked.husband_here.cold.femdom": {
            "_any": [
                _("Say that again, louder, with your father three steps away. No? Then sit down and be quiet."),
                _("You don't have the nerve to repeat that in front of him. Silence suits you better, boy."),
                _("One word from me and your father handles you himself. Choose your next sentence carefully."),
            ],
        },
        # step 0: nothing of her yet. Shock first, authority second: a stepson ASKING at all is the offense
        "story_locked.cold": {
            "_any": [
                _("Excuse me? I'm your father's wife. Get out of my sight."),
                _("Are you out of your mind? Go to your room. Now."),
                _("Disgusting. Don't ever try that again."),
                _("Do you hear yourself? I married your FATHER. This conversation is over."),
                _("I'm going to pretend those words never left your mouth. Don't make me hear them twice."),
                _("What exactly do you think I am to you? Ask me again and your father hears about it."),
            ],
            "touch": [
                _("Touch me again and your allowance is the first thing you lose."),
                _("Hands. Off. I'm not one of your little girlfriends, I'm your father's wife."),
                _("Put that hand on me again and you'll be explaining it to your father."),
            ],
            "kiss": [
                _("Kiss you? I'd slap you before you got anywhere near me."),
                _("You want to kiss your father's wife. Say that out loud, hear how it sounds, and never say it again."),
                _("No. Kisses belong to the man I married. Don't bring this up again."),
            ],
            "petname": [
                _("A pet name. For your father's wife. Do you even hear yourself?"),
                _("No. My name works perfectly fine, and so does yours."),
                _("We are not that kind of anything, you and I. Use my name."),
            ],
            "masturbate": [
                _("You asked me to WHAT? Get out. Now."),
                _("I should wash your mouth out with soap. Never ask me that again."),
                _("That you can even form that sentence about your father's wife... unbelievable. No."),
            ],
            "hj": [
                _("My hands are never going anywhere near you, boy. Ever."),
                _("You asked your stepmother for THAT? I don't know whether to laugh or call your father."),
                _("No. And that you thought you could ask tells me your father has been far too soft on you."),
            ],
            "bj": [
                _("My MOUTH? You must have lost your mind on the way home."),
                _("I won't even repeat what you just asked me. Out. NOW."),
                _("Boys your age really think they can say anything. No. Never. Not in this lifetime."),
            ],
            "sex": [
                _("Sleep with you? With my husband's SON? You're insane."),
                _("I'm going to say this once. I am your father's wife. Nothing on this earth makes that happen."),
                _("You just asked your stepmother for sex. Sit with that sentence. Then go to your room."),
            ],
            "anal": [
                _("...I don't know what disgusts me more, the request or where you aimed it."),
                _("THAT? You asked ME for THAT? Get out before I say something we'll both regret."),
                _("There is something wrong with you. Truly. Get out of my sight."),
            ],
            "outing": [
                _("Go somewhere? With you? I don't have the time, and you don't have the standing."),
                _("No. Being family doesn't make us company for each other."),
                _("I go where I decide, with whom I decide. Keep walking, boy."),
            ],
            # the romantic dinner (act "date", restaurant_girl_accepts): harsher than the generic
            # no, it names the dinner (author 2026-10-11, "mais rispida nos steps baixos")
            "date": [
                _("A dinner date? With my husband's son? That sentence alone could burn this family down. Never say it again."),
                _("I have dinners with boards and investors, boy. Not with a student who lives on my husband's money."),
                _("We share a table on Sundays, as a family. That is every dinner you will ever get from me."),
            ],
            # his "send me a photo" on her phone (phone_photos.rpy)
            "photo": [
                _("A photo. Of me. On your phone. I can already see the headline, boy. Delete this conversation."),
                _("I pose for shareholder reports. Ask again and your father reads this chat."),
                _("No. And if my face ever leaves your phone, my lawyers will live in your dorm."),
            ],
            # asking to shower with her (actions.rpy shower_join)
            "shower_join": [
                _("OUT. This is MY bathroom, in MY house, and that door had a lock for a reason."),
                _("Join me? I'll count to three, and at two I'm calling your father."),
                _("You walked in on your father's wife in the shower and asked THAT. Get out and pray I forget it."),
            ],
            # she walked in on HIS shower (actions.rpy _shower_solo): she saw, she does not care
            "shower_walkin": [
                _("...This bathroom has an occupied side and a hallway side. Learn the difference. I'm taking the hallway."),
                _("Cover yourself. This is a bathroom, not a statement."),
                _("Noted: the lock works and you don't use it. That's a you problem, boy."),
            ],
            # his "can I get your number" (_ask_phone_number): she gives him nothing on her cold step
            "phone_number": [
                _("My number? It's for your father, my board, and my lawyer. You are none of those."),
                _("You have a roof, meals and an allowance. None of them requires my number."),
                _("If it's urgent, tell your father. If it's not, don't bother me at all."),
            ],
        },
        "story_locked.cold.femdom": {
            "phone_number": [
                _("People earn a line to me, boy. You haven't even earned the right to knock."),
                _("My number goes to people I summon. You get summoned. Learn the difference."),
            ],
            "_any": [
                _("No. And the next time you forget who commands this house, you'll lose more than your allowance."),
                _("You mistake me for something you can have. I decide what you get, boy. You get nothing."),
                _("I give orders in this house. I don't take requests. Especially not that one."),
            ],
            "touch": [
                _("That hand. I decide what touches me, and you are not on any list. Remove it."),
                _("Touch me without permission again and you'll learn exactly who runs this family."),
            ],
            "kiss": [
                _("Kiss me? You just asked your father's wife to KISS you. Say that out loud and hear how insane it sounds."),
                _("Are you out of your mind? One word from me and your father hears exactly what you just tried, boy."),
            ],
            "petname": [
                _("Names between us are my decision, not yours. And I've decided: no."),
                _("A nickname. From you. The terms in this house are mine, boy, and the terms are no."),
            ],
            "masturbate": [
                _("A show. For you. I don't perform, boy. People obey me, that's the whole arrangement."),
                _("I don't perform. Certainly not for a boy who can't keep his own grades standing."),
            ],
            "hj": [
                _("These hands sign your allowance. That is the only thing they will ever do for you."),
                _("No. My hands do what I decide, for whom I decide. You're not on the list, boy."),
            ],
            "bj": [
                _("You just asked the woman who runs this house to KNEEL. Think very carefully about your next sentence."),
                _("My mouth gives orders. That is all it will ever give you."),
            ],
            "sex": [
                _("Sex. With you. I don't entertain children, and I certainly don't sleep with my husband's son."),
                _("No. I belong to no one, boy. Least of all to someone I could break with one phone call."),
            ],
            "anal": [
                _("The audacity is almost impressive. Almost. The answer is the door."),
                _("That's what you ask the woman who runs your life? You can't even meet my eyes when I'm angry."),
            ],
            "outing": [
                _("I don't follow, boy. And I certainly don't follow you."),
                _("You want me walking behind you? Learn the order of this house first."),
            ],
            "date": [
                _("You don't invite me, boy. The day I want you somewhere, you'll be told the time, the place, and what to wear."),
                _("A date. You, planning MY evening. I schedule this family's lives, yours included. Know your place."),
            ],
            "photo": [
                _("People petition ME for pictures, boy. And they get told no by an assistant."),
                _("My image is an asset. Assets don't go to boys' phones. Ever."),
            ],
            "shower_join": [
                _("You don't walk in on me. I summon. That's the entire system, and you just failed it."),
                _("Out. In this house even the water answers to me, and so do you."),
            ],
            "shower_walkin": [
                _("Stand there dripping if you like. I needed the mirror, not the view."),
                _("Relax, boy. I audit everything in this house. Nothing I see changes my numbers."),
            ],
        },
        "story_locked.cold.hardcore_sex": {
            "_any": [
                _("Ask me again and I will make your life harder than you can imagine. Try me."),
                _("No. And if you push, I push back. I always push back harder."),
                _("You've mistaken me for someone patient. I'm not. Drop it, now."),
            ],
        },
        "story_locked.cold.cute_sex": {
            "_any": [
                _("No. I'm saying it gently because I'd rather keep this house civil. Don't ask again."),
                _("I'm not angry, I'm something worse. Disappointed. Never bring this up again."),
                _("You're getting a soft 'no' exactly once. The next one won't be soft."),
            ],
        },
        "story_locked.cold.submissive": {
            "_any": [
                _("That is not appropriate. It will never be appropriate. Please stop."),
                _("I... am going to leave now, and we will both pretend this conversation never happened."),
                _("Don't do this. Some things can't be unsaid, and that was nearly one of them."),
            ],
        },
        # step 1: his hands, a kiss, her hand, a show. Nothing more
        "story_locked.she_decides": {
            "_any": [
                _("You'll get that when I decide. Not a minute before."),
                _("Greedy. I give you a little and you want everything."),
                _("Not that. I decide how far this goes, and it isn't there yet."),
                _("Patience. Something has to change between us before you get that."),
            ],
            # the romantic dinner: the _any above dangles a promise; a PUBLIC date gets her
            # cold voice back (author 2026-10-11, "mais rispida nos steps baixos")
            "date": [
                _("A restaurant? Where this whole city can SEE us? Use your head, boy."),
                _("No. Whatever this is, it does not sit at a candlelit table in public. Ask me that again and it becomes nothing."),
                _("Outside these walls I am his wife. You don't get to forget that because I let you close once."),
            ],
        },
        "story_locked.she_decides.femdom": {
            "_any": [
                _("Greedy. I set the pace, boy. You take what I give and you say thank you."),
                _("No. When you've pleased me enough, I'll tell you. Until then, don't ask."),
                _("You'll get that the day I decide you've earned it. Today is not that day."),
            ],
            "date": [
                _("I decide when we are seen together. The answer is never, and you don't get a vote, boy."),
                _("What I allow you happens where I say, behind doors I choose. A restaurant is you showing me off. Nobody shows me off."),
            ],
        },
        # step 2: almost everything. Not her ass, not inside her, never bare
        "story_locked.giving_in": {
            "_any": [
                _("Not that. That part of me you haven't won yet."),
                _("No. There are still a few lines I haven't crossed. That's one of them."),
                _("Greedy boy. That one you'll have to wait for."),
            ],
            # "raw": no condom (starting bare, taking it off)
            "raw": [
                _("With a condom, or not at all. That one isn't up for debate."),
                _("Put one on. Bare, you don't get anywhere near me."),
                _("No condom, no me. Pick one."),
            ],
        },
        "story_locked.giving_in.femdom": {
            "_any": [
                _("Not that. Even now, there are parts of me you haven't earned."),
                _("No. I still decide where the lines are, and that one stands."),
            ],
            "raw": [
                _("You go in wrapped, boy. That's the price of me, and I set it."),
                _("Bare is a privilege. You haven't been granted it. Condom."),
            ],
        },
        # step 3: she's his. Still not her ass, not inside her, never bare
        "story_locked.his": {
            "_any": [
                _("I'm yours. That doesn't mean everything is, not yet."),
                _("Not that. There's one wall left, and you're not knocking it down today."),
                _("Greedy. You have me. Let me keep a little something for later."),
            ],
            "raw": [
                _("Condom. I'm yours, not careless."),
                _("I said I'm yours. I never said bare. Put it on."),
                _("Not without one. Not yet. Wrap it, or we stop right here."),
            ],
        },
        "story_locked.his.femdom": {
            "_any": [
                _("I gave you a lot, boy. The rest is still mine to give."),
                _("No. Even now, that line is mine to move, not yours."),
            ],
            "raw": [
                _("Wrapped, boy. I'm yours on my terms, and that's one of them."),
                _("You want me bare? Earn it. Until then, a condom."),
            ],
        },

        # ══════════════════════════════════════════════════════════
        #  AFTERSCENE.<step>[.<route>]: one line after a normal scene with her, steps 2+ (_story_afterscene,
        #  story_steps.rpy; once a day). The route is the one that OPENED her current step (story_step_route):
        #  love never sounds bought, blackmail never sounds won over. "_any" only: no line names the act.
        # ══════════════════════════════════════════════════════════
        "afterscene.giving_in": {
            "_any": [
                _("...Hand me my things. And fix your face before anyone sees you."),
                _("Not a word of this outside this room. Not one."),
            ],
        },
        "afterscene.giving_in.love": {
            "_any": [
                _("...Stay there a moment. Just a moment. Then we never speak of how much I wanted that."),
                _("I think about this more than I'll ever admit to you. There. That's all you get."),
            ],
        },
        "afterscene.giving_in.inbt": {
            "_any": [
                _("One of these days we'll be careless and burn this family down. ...Why doesn't that stop me."),
                _("Every time, I swear it's the last time. And every time I'm already planning the next one."),
            ],
        },
        "afterscene.giving_in.obed": {
            "_any": [
                _("...I did everything you said. I don't know what's happening to me, and I don't want it explained."),
                _("Tell me to leave. ...No. Don't. Don't tell me anything for a minute."),
            ],
        },
        "afterscene.giving_in.blackmail": {
            "_any": [
                _("You got what your little videos paid for. Enjoy it while it lasts, boy."),
                _("Don't mistake this for wanting you. We have an arrangement. That's all this is."),
            ],
        },
        "afterscene.his": {
            "_any": [
                _("...I'll shower at home. His soap, his towels, and not one thought about him."),
                _("Look at me. Whatever happens, this does not end. Understood?"),
            ],
        },
        "afterscene.his.love": {
            "_any": [
                _("Twenty years I ran my life like a ledger. Then you. ...Don't you dare repeat that."),
                _("I'm yours. I hate the word, and it's the only one that fits."),
            ],
        },
        "afterscene.his.inbt": {
            "_any": [
                _("In his home. Again. I should feel something about that, and all I feel is your hands."),
                _("One day I'll stop being careful. Pray you're worth it, because I already know I won't stop."),
            ],
        },
        "afterscene.his.obed": {
            "_any": [
                _("Whatever you want next, say it and it happens. That's what I am now. ...Start with something small."),
                _("Order me to rest. If it's an order, I might actually do it."),
            ],
        },

        # ════ AFTER THE BREAK (she lost the femdom past her final step; trait submissive) ════
        # Her accepted / deny / afterscene voice as the one who obeys now. The resolver tries "<mood>.submissive"
        # before the shared submissive pools and her base (girl_sex_voice_trait_line).
        "accepted.submissive": {
            "_any": [
                _("Yes. However you want it. Just keep telling me."),
                _("Alright. ...Direct me. It's easier when you do."),
            ],
            "hj": [
                _("My hands used to sign everything in this house. Tell them what to do now."),
            ],
            "bj": [
                _("I used to give orders with this mouth. ...On my knees, then. Say when."),
            ],
            "sex": [
                _("Take me, then. I stopped pretending I'd say no a while ago."),
            ],
        },
        "soft_deny.submissive": {
            "_any": [
                _("I... can't. Not right now. Please don't be angry with me."),
                _("Not here. I'm sorry. Ask me again somewhere safer and I won't refuse."),
            ],
        },
        "tempted_deny.submissive": {
            "_any": [
                _("I want to say yes. I always want to say yes now. ...Just not here. Please."),
                _("Don't look at me like that, I'll fold. ...Later. I promise you later."),
            ],
        },
        "story_locked.husband_here.submissive": {
            "_any": [
                _("He's RIGHT there... please. It's the one no I have left. Don't make me spend it."),
                _("Not in front of him. Please. Everywhere else I'm yours, you know that."),
            ],
            "outing": [
                _("With him home? I'll make an excuse tomorrow and meet you anywhere. Just not under his eyes."),
            ],
        },
        "afterscene.his.submissive": {
            "_any": [
                _("Tell me I did well. ...I know how that sounds. Say it anyway."),
                _("I used to run this house. Now I lie here hoping you're pleased. I've decided not to examine that."),
                _("Whatever you need next, it's yours. That's not an offer, it's just... what I am now."),
            ],
        },
    }
