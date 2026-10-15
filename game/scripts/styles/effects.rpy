image Punchout:
    Null(0, 0)

label Punch:
    # causes the screen to shake a bit
    show Punchout with vpunch
    hide Punchout
    return

label HardPunch:
    show Punchout with vpunch
    pause 0.12
    show Punchout with hpunch
    pause 0.1
    show Punchout with vpunch
    hide Punchout
    return

label OrgasmPunch_light:
    show Punchout with vpunch
    pause 0.15
    hide Punchout
    return

label OrgasmPunch:
    show Punchout with vpunch
    pause 0.15
    show Punchout with hpunch
    pause 0.15
    hide Punchout
    return

label OrgasmPunch_hard:
    show Punchout with vpunch
    pause 0.1
    show Punchout with hpunch
    pause 0.1
    show Punchout with vpunch
    pause 0.15
    show Punchout with hpunch
    hide Punchout
    return
