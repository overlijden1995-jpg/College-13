## options.rpy – College Traits

init python:
    config.quit_action = Show("quit_screen")

init -1 python hide:

    ##############################################
    # CONFIGURAÇÕES GERAIS
    ##############################################

    config.developer = True
    if "reload_game" in config.keymap:
        config.keymap["reload_game"] = []
    if "reload" in config.keymap:
        config.keymap["reload"] = []

    # Add our own reload hotkey: full restart (no pickle)
    config.underlay.append(renpy.Keymap(rod_full_reload=renpy.full_restart))
    config.keymap["rod_full_reload"] = [ "shift_K_r", "ctrl_K_r" ]

    config.screen_width  = 1920
    config.screen_height = 1080
    config.image_cache_size = 96

    config.window_title = u"College Traits"
    config.name = "College Traits"
    config.version = "0.13"


    ##############################################
    # THEME (não usamos gui.*, então é seguro)
    ##############################################

    theme.tv(
        widget="#122034",
        widget_hover="#1b2f4a",
        widget_text="#e6edf7",
        widget_selected="#ffffff",

        disabled="#2d3e57",
        disabled_text="#8da0bb",

        label="#0b1422",
        frame="#0b1422",

        mm_root="#0a1220",
        gm_root="#0c1626",

        rounded_window=False,
    )



    ##############################################
    # JANELA DE DIÁLOGO PADRÃO (ADV)
    # (Raramente usada, pois usamos o screen say())
    ##############################################

    style.window.background = Frame("images/menus/GirlsCard_Blue.png", 12, 12)
    style.window.left_padding = 28
    style.window.right_padding = 28
    style.window.top_padding = 26
    style.window.bottom_padding = 26
    style.window.xminimum = 5
    style.window.yminimum = 5
    style.window.xmaximum = 360


    ##############################################
    # ESTILO — CAIXA DE NARRAÇÃO / AÇÃO (TOPO)
    ##############################################

    style.narration_box = Style(style.default)
    style.narration_box.background = Frame("images/menus/ComicPanelCaption.png", 40, 40)
    style.narration_box.padding = (24, 22)
    style.narration_box.xmaximum = 1000
    style.narration_box.outlines = [(2, "#0b0f17", 0, 0)]
    style.narration_box.color = "#f8fafc"
    style.narration_box.size = 26
    style.narration_box.xalign = 1
    style.narration_box.yalign = 0.5   # Fica no topo


    ##############################################
    # NAMEBOX (caixa de nome do personagem)
    ##############################################

    style.say_who_window.background = Frame("images/menus/Nametag.png", 18, 18)
    style.say_who_window.xminimum = 80
    style.say_who_window.left_padding = 16
    style.say_who_window.right_padding = 16
    style.say_who_window.top_padding = 10
    style.say_who_window.bottom_padding = 10


    ##############################################
    # BALÃO DE FALA (two_window=True)
    ##############################################

    style.say_balloon = Style(style.default)
    style.say_balloon.background = Frame("images/menus/ComicPanelCaption.png", 32, 32)
    style.say_balloon.left_padding = 30
    style.say_balloon.right_padding = 30
    style.say_balloon.top_padding = 24
    style.say_balloon.bottom_padding = 24
    style.say_balloon.xmaximum = 980
    style.say_balloon.color = "#0b1324"
    style.say_balloon.outlines = [(1, "#0b1220", 0, 0)]
    style.say_balloon.size = 34


    ##############################################
    # FONTE GLOBAL
    ##############################################

    style.default.font = "fonts/WorkSans-Medium.ttf"
    style.default.size = 24
    style.default.color = "#e5e7eb"
    style.default.drop_shadow = None
  





    ##############################################
    # ÁUDIO
    ##############################################

    config.has_sound = True
    config.has_music = True
    config.has_voice = False


    ##############################################
    # AJUDA E TRANSIÇÕES
    ##############################################

    config.help = None

    config.enter_transition = None
    config.exit_transition = None
    config.intra_transition = None
    config.main_game_transition = None
    config.game_main_transition = None
    config.end_splash_transition = None
    config.end_game_transition = None
    config.after_load_transition = None
    config.window_show_transition = None
    config.window_hide_transition = None

    config.adv_nvl_transition = dissolve
    config.nvl_adv_transition = dissolve

    config.enter_yesno_transition = None
    config.exit_yesno_transition = None
    config.enter_replay_transition = None
    config.exit_replay_transition = None
    config.say_attribute_transition = None



# Diretório de saves
python early:
    config.save_directory = "CollegeTraits-1.0"



init -1 python hide:

    ##############################################
    # PREFERÊNCIAS PADRÃO
    ##############################################

    config.default_fullscreen = False
    config.default_text_cps = 0
    config.default_afm_time = 10
    config.skip_delay = 75



##############################################
# SEÇÃO DE BUILD
##############################################
init python:

    build.directory_name = "CollegeTraits-0.13"
    build.executable_name = "CollegeTraits"

    build.include_update = False

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)
    build.classify('docs/**', None)
    build.classify('_tl_work/**', None)
    build.classify('**.md', None)
    build.classify('**.csv', None)
    build.classify('**/log.txt', None)
    # temporary engine test harnesses (game/zz_*.rpy / .rpyc) never ship, even if one is present while building
    build.classify('game/zz_**', None)

    build.classify("**.png", "archive")
    build.classify("**.jpg", "archive")
    build.classify("**.rpy", "archive")
    build.classify("**.rpyc", "archive")
    build.classify("**.ttf", "archive")

    build.documentation('*.html')
    build.documentation('*.txt')
