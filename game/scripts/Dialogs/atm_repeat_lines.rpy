# ============================================================
# atm_repeat_lines.rpy... what she says when ATM happens AGAIN in the same session
# ============================================================
#
# Read by Cum.rpy: PlayerCumMenu_Penetration_Raw (moment "pre", before the 2nd+ ATM of the session) and
# _post_atm_swallow_reaction (moment "post", after the 2nd+ swallow). Each trait has its own voice, so two girls
# with different traits never sound alike: femdom lets him and keeps count, submissive obeys, cum_slut wants the
# cum, anal_lover wants the ass, hardcore wants it faster and rougher, cute_sex is hurt, hate_cum is disgusted.
# Her FIRST trait in ATM_REPEAT_PRIORITY that has a pool speaks, else "_default" (the girl who just endures it).
#
# Tiers count THIS session only ("pre": ATMs already done, 1 to 4 = 4 or more; "post": this swallow's number, 2 to
# 5 = 5 or more). No line claims a habit from other days: they are safe while she is still discovering a trait.
# ============================================================

init python:

    ATM_REPEAT_PRIORITY = ("femdom", "submissive", "cum_slut", "hate_cum", "anal_lover", "hardcore_sex", "cute_sex")

    ATM_REPEAT_LINES = {
        "pre": {
            "femdom": {
                1: [
                    _("Again? Fine. But this time I decide when you finish."),
                    _("Round two happens because I allow it. Remember that."),
                    _("You want my mouth again? Ask nicely... Good. Now give it here."),
                ],
                2: [
                    _("Three times, and every one on my terms. Don't forget who's allowing this."),
                    _("Again? You're lucky I'm in a generous mood. Stay still."),
                    _("My mouth, my rules. The third round goes at my pace."),
                ],
                3: [
                    _("Four times. I'm keeping count, and you're going to owe me for every one."),
                    _("Again? Hands off my head. I'm running this."),
                    _("Fine. A fourth time. But you'll beg me for the fifth."),
                ],
                4: [
                    _("I've let you do this so many times today. You'd better be grateful."),
                    _("Still not done? Then lie back and let me finish you my way."),
                    _("You don't get to be tired before I say so. Again."),
                ],
            },
            "submissive": {
                1: [
                    _("Again? If you want it again, I'll open up again."),
                    _("You don't even have to ask. Just tell me."),
                    _("A second time... whatever you want, I'll do it."),
                ],
                2: [
                    _("A third time... I'll take it as many times as you tell me to."),
                    _("You want it again? Then it's yours."),
                    _("I stopped asking why. Tell me to open, I open."),
                ],
                3: [
                    _("Again and again... you just can't get enough of using me like this."),
                    _("Four times... and I'd still say yes to a fifth. Say it."),
                    _("Use my mouth again. That's what it's for today."),
                ],
                4: [
                    _("I've lost count. Just keep going. My mouth is yours."),
                    _("However many times you want. I'm not saying no."),
                    _("Keep using me. I'll keep swallowing."),
                ],
            },
            "cum_slut": {
                1: [
                    _("Again? Mmm... you really liked that, huh? I'm not complaining."),
                    _("More? God, yes. I was hoping you'd ask."),
                    _("Round two... I want to taste it again."),
                ],
                2: [
                    _("At this point my mouth knows the way. Come here."),
                    _("A third time and I'm still greedy for it. Give it to me."),
                    _("Again? My mouth is already watering."),
                ],
                3: [
                    _("Four loads straight from my ass... and I still want the next one."),
                    _("Don't stop now. I want every single one of them."),
                    _("Again? Fill my mouth. I can't get enough today."),
                ],
                4: [
                    _("I'm not saying no to this. Not today. Give it to me."),
                    _("Keep them coming. I want to taste every one."),
                    _("Again... God, I'm so greedy for it today."),
                ],
            },
            "hate_cum": {
                1: [
                    _("Again?! You know I hate the taste. ...Fine. Fast."),
                    _("Another load in my mouth? Ugh. Get it over with."),
                    _("Twice?! I still haven't gotten the first one out of my mouth."),
                ],
                2: [
                    _("A third load. I'm going to need a gallon of mouthwash."),
                    _("Three times. I hate this. I hate you a little right now."),
                    _("Again? Just... aim for the back so I don't taste it."),
                ],
                3: [
                    _("Four loads. I can't taste anything but cum and ass. Great."),
                    _("FOUR. I hate cum. You know that. You KNOW that."),
                    _("Fine. But I'm spitting... no, you won't let me. Ugh."),
                ],
                4: [
                    _("I've swallowed more cum today than I ever wanted to in my life. Happy?"),
                    _("I don't even gag anymore. That's the worst part."),
                    _("Just finish. The taste is never leaving me anyway."),
                ],
            },
            "anal_lover": {
                1: [
                    _("Back in my ass and then my mouth? Round two, I'm in."),
                    _("A second time from back there... yes. Do it again."),
                    _("You want to go from my ass to my mouth again? Mmm, yes."),
                ],
                2: [
                    _("Third time... you're obsessed. I kind of love that about you."),
                    _("My ass first, then my mouth. Again. I love how filthy this is."),
                    _("Keep fucking my ass like that and I'll clean you off every time."),
                ],
                3: [
                    _("Four times? You're turning this into a routine. I'm into it."),
                    _("My ass and my mouth both want you. Again."),
                    _("Four times from my ass... and I'm still wet thinking about it."),
                ],
                4: [
                    _("My ass is sore and my mouth wants more. Keep going."),
                    _("As many times as you want. Ass first, mouth after."),
                    _("I lost count of how many times it went from my ass to my mouth. Again."),
                ],
            },
            "hardcore_sex": {
                1: [
                    _("Round two? Fine by me. You know I can take it."),
                    _("Again? Then pound my ass hard first. I want to feel it."),
                    _("Again? Shove it in fast. No warm-up."),
                ],
                2: [
                    _("Third round. Harder than the last one, got it?"),
                    _("Again? Faster this time. I want to feel it in my throat."),
                    _("Keep going. As rough as you want."),
                ],
                3: [
                    _("Four times and you're still going strong? Then don't slow down."),
                    _("Again. Deep and fast. Don't you dare go easy now."),
                    _("My jaw aches. Good. Again."),
                ],
                4: [
                    _("I'm shaking and I still want it rougher. Again."),
                    _("Keep pounding and keep feeding me. Don't stop."),
                    _("Again. Faster. I want to feel this tomorrow."),
                ],
            },
            "cute_sex": {
                1: [
                    _("Again...? I... okay. If it really makes you happy."),
                    _("Again? Can we please do something softer after this?"),
                    _("You want me to do that again? ...I'll try. For you."),
                ],
                2: [
                    _("A third time? I thought... never mind. Okay."),
                    _("Please be gentle at least... okay?"),
                    _("Why do you keep wanting this? ...Okay."),
                ],
                3: [
                    _("Four times... I don't feel very cared for right now."),
                    _("Can we stop after this one? Please?"),
                    _("I'm doing this because you want it. Not because I do."),
                ],
                4: [
                    _("I keep saying yes because I don't want to disappoint you... that's all."),
                    _("Please, this is the last one... okay?"),
                    _("I just want you to hold me after this."),
                ],
            },
            "_default": {
                1: [
                    _("Again?! Seriously? ...Fine. Just get it over with."),
                    _("You're doing this AGAIN? ...Whatever."),
                    _("Again? ...You really don't let up, do you?"),
                ],
                2: [
                    _("A THIRD time? How many times are you going to make me do this?"),
                    _("Three times... are you trying to break some kind of record?"),
                    _("Three? You're pushing it. Fine."),
                ],
                3: [
                    _("FOUR TIMES?! What is WRONG with you?!"),
                    _("I've tasted my own ass four times today. Let that sink in."),
                    _("Four. Nobody would believe me if I told them."),
                ],
                4: [
                    _("I can't even count anymore. My mouth permanently tastes like ass now. Happy?"),
                    _("At this point I don't even react. Just do it. My dignity left a while ago."),
                    _("I'm numb. Just do it."),
                ],
            },
        },
        "post": {
            "femdom": {
                2: [
                    _("Twice. And both times because I let you. Don't forget it."),
                    _("There. The second one's down. You're welcome."),
                    _("I swallowed it because I wanted to. Not because you asked."),
                ],
                3: [
                    _("Three. I'm counting, and you owe me for every single one."),
                    _("Done. Now it's my turn, and you're going to earn it."),
                    _("A third time. I still decide how this ends."),
                ],
                4: [
                    _("Four. You've been very lucky today. Don't push it."),
                    _("I swallowed four of those. Now you do exactly what I say."),
                    _("That's four. Next time you ask, you beg first."),
                ],
                5: [
                    _("I stopped counting, but you'll remember every one. I'll make sure of it."),
                    _("Enough for now. I'll tell you when you get another."),
                    _("Every drop, every time, on my terms. Now lie back."),
                ],
            },
            "submissive": {
                2: [
                    _("Swallowed again, like you wanted. Was I good?"),
                    _("Two times... tell me when you want the next one."),
                    _("I didn't even hesitate this time. Is that what you wanted?"),
                ],
                3: [
                    _("I'm not even thinking about it anymore. My mouth just opens."),
                    _("Three times. I'll keep going as long as you want."),
                    _("Swallowed it all. Tell me what's next."),
                ],
                4: [
                    _("Four times... I'd do it forty if you told me to."),
                    _("I do what you want. I swallow what you give me. That's all."),
                    _("Every time you ask, I say yes. I can't help it."),
                ],
                5: [
                    _("I'm yours. Completely. Use me however you want."),
                    _("I don't care how many times anymore. Just use me."),
                    _("Whatever you give me, I take. That's how it is today."),
                ],
            },
            "cum_slut": {
                2: [
                    _("Second time tastes better than the first. Or maybe I'm just getting used to it."),
                    _("Mmm... I could get used to this flavor."),
                    _("Two loads down. I want more."),
                ],
                3: [
                    _("Three times... I'm starting to crave it. What have you done to me?"),
                    _("Every drop. I didn't waste a single one."),
                    _("Three loads and I'm still hungry."),
                ],
                4: [
                    _("I've completely lost it. Four times and I'm asking for more."),
                    _("Four. My mouth is sticky and I love it."),
                    _("Don't you dare give the next one to anyone else."),
                ],
                5: [
                    _("I can't even remember what anything else tastes like. Just keep going."),
                    _("My whole mouth tastes like you. Perfect."),
                    _("I'll swallow every load you've got left."),
                ],
            },
            "hate_cum": {
                2: [
                    _("Twice. I can still taste the first one. Disgusting."),
                    _("That's two loads I never wanted in my mouth."),
                    _("Ugh. It's worse the second time."),
                ],
                3: [
                    _("Three. I'm never kissing anyone again."),
                    _("My mouth tastes like cum and ass. I hate you right now."),
                    _("Three loads. My stomach is turning."),
                ],
                4: [
                    _("Four. I hate cum. I swallowed four. What is happening?"),
                    _("I can't get the taste out. It's everywhere."),
                    _("Four times... I'm going to be sick."),
                ],
                5: [
                    _("I've stopped fighting it. It's still disgusting."),
                    _("Whatever. It all tastes like cum now anyway."),
                    _("Just... don't ever tell anyone about today."),
                ],
            },
            "anal_lover": {
                2: [
                    _("Twice now... and it's getting easier. Is that bad?"),
                    _("From my ass to my mouth, twice. I love how dirty this is."),
                    _("I can still feel you in my ass while I swallow. God."),
                ],
                3: [
                    _("Three times... my ass is aching and I still want you in it."),
                    _("My ass, then my mouth, three times. Don't stop now."),
                    _("I can't tell what I love more anymore. My ass or this."),
                ],
                4: [
                    _("At this point my mouth tastes like my ass permanently. And I don't care."),
                    _("Four times... my ass is going to be sore for days. Worth it."),
                    _("Put it back in my ass. I'll clean it again after."),
                ],
                5: [
                    _("I've lost count. Ass, mouth, ass, mouth... don't stop."),
                    _("My ass is so wet and my mouth is full. Perfect."),
                    _("Keep going. I want your cock in my ass until you're empty."),
                ],
            },
            "hardcore_sex": {
                2: [
                    _("Twice. And you didn't go easy either time. Good."),
                    _("My throat's raw and I want another round."),
                    _("That was rough. Do it rougher."),
                ],
                3: [
                    _("Three. My legs are shaking. Keep going."),
                    _("You fuck my ass that hard and then my throat? Again."),
                    _("Three times and still not gentle. Perfect."),
                ],
                4: [
                    _("Four times. I'm going to feel this all week."),
                    _("My jaw hurts and my ass is on fire. Again."),
                    _("Don't slow down now. I can still take it."),
                ],
                5: [
                    _("I'm wrecked. And I'm not done."),
                    _("Keep going until one of us breaks."),
                    _("Harder. Faster. Again. I don't care how many times."),
                ],
            },
            "cute_sex": {
                2: [
                    _("Twice... I really don't like this."),
                    _("I did it again for you... can we cuddle after?"),
                    _("Please don't make me do that again..."),
                ],
                3: [
                    _("Three times... I feel really small right now."),
                    _("I did it because you wanted it... I don't feel good."),
                    _("Can you please just hold me for a bit?"),
                ],
                4: [
                    _("Four... I'm trying so hard for you."),
                    _("I just want this to be over."),
                    _("Please tell me you still care about me..."),
                ],
                5: [
                    _("I stopped counting... please be gentle with me after this."),
                    _("I don't know why I keep saying yes."),
                    _("I'm so tired... please."),
                ],
            },
            "_default": {
                2: [
                    _("Twice... I can't believe you made me do it twice."),
                    _("Again... the taste hasn't gone away from the first time and now there's more."),
                    _("Again... I can't believe I did that twice."),
                ],
                3: [
                    _("Three times. My mouth is never going to recover from today."),
                    _("I've swallowed from my ass three times. This is rock bottom."),
                    _("Three. I'm running out of ways to be shocked."),
                ],
                4: [
                    _("Four times. I don't even have words anymore. Just... why?"),
                    _("I've given up complaining. You clearly don't care what I think."),
                    _("Four. I'm just... numb about it now."),
                ],
                5: [
                    _("I stopped counting. The taste of my ass is just... my life now."),
                    _("Whatever. Just... whatever. I'm done reacting."),
                    _("I'm done keeping track. Just finish."),
                ],
            },
        },
    }

    def atm_repeat_line(girl, moment, count):
        """Her line for an ATM repeated in this session. moment "pre": count = ATMs already done this session (1+);
        "post": count = this swallow's number in the session (2+). Her first trait in ATM_REPEAT_PRIORITY with a
        pool speaks, else "_default"; the count is clamped to the moment's tiers."""
        _table = ATM_REPEAT_LINES[moment]
        _tiers = sorted(_table["_default"])
        _tier = max(_tiers[0], min(int(count), _tiers[-1]))
        _key = next((_t for _t in ATM_REPEAT_PRIORITY if girl.has_trait(_t) and _t in _table), "_default")
        print("[ATM_REPEAT] %s %s count=%d -> %s tier %d" % (girl.gid, moment, count, _key, _tier))
        return renpy.random.choice(_table[_key][_tier])
