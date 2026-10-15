# ============================================================
# i18n_names.rpy... names in a language that writes them in another script (Russian, 2026-10-02:
# docs/translation_ru.md). The game stores every name in Latin (girl.Name, NPC names, speakers); on screen,
# in a language listed in LANG_NAMES, config.replace_text swaps each one for its local form.
#
# A language that declines (Russian) puts an inserted name in its case with the text tag {case=X}...{/case}
# (X = nom gen dat acc ins pre): "комната {case=gen}[girl.Name]{/case}". Indeclinable names (Гвен, Шион) stay as
# they are; a name the table does not know (the player's own) is declined only when it is written in Cyrillic.
# Ren'Py fills [vars] first, then runs the custom tags, then replace_text (renpy/text/text.py apply_custom_tags).
# ============================================================

init -5 python:

    # Latin name as the game stores it -> (local name, "m" / "f"). Russian: the official Russian names where they exist
    # (Rogue = Шельма, the comics / animated series name; Negasonic = Боеголовка, the Deadpool dub's "Сверхзвуковая
    # Боеголовка"; Yukio = Юкио), the rest transliterated.
    LANG_NAMES = {
        "ru": {
            "Gwen": ("Гвен", "f"), "Rogue": ("Шельма", "f"), "Negasonic": ("Боеголовка", "f"), "Tenny": ("Тенни", "f"),
            "Shion": ("Шион", "f"), "Yukio": ("Юкио", "f"), "Dad": ("Папа", "m"), "Hashimoto": ("Хашимото", "m"),
            "C. Johnson": ("К. Джонсон", "m"), "Johnson": ("Джонсон", "m"), "Professor": ("Профессор", "m"),
            # the names the player can give Tenny (intro.rpy: "Can I call you something else?")
            "Gwendolyn": ("Гвендолин", "f"), "Tennyson": ("Теннисон", "f"), "Gwen T": ("Гвен Т", "f"),
            "Cathy": ("Кэти", "f"), "Catherine": ("Кэтрин", "f"), "Lucky": ("Лаки", "f"), "Gwennie": ("Гвенни", "f"),
            "Red": ("Рыжая", "f"),
            # _NPC_NAMES_MALE / _NPC_NAMES_FEMALE (npc_partner.rpy)
            "James": ("Джеймс", "m"), "Ethan": ("Итан", "m"), "Lucas": ("Лукас", "m"), "Noah": ("Ноа", "m"),
            "Liam": ("Лиам", "m"), "Mason": ("Мейсон", "m"), "Logan": ("Логан", "m"), "Alex": ("Алекс", "m"),
            "Ryan": ("Райан", "m"), "Tyler": ("Тайлер", "m"), "Jake": ("Джейк", "m"), "Dylan": ("Дилан", "m"),
            "Kyle": ("Кайл", "m"), "Marcus": ("Маркус", "m"), "Derek": ("Дерек", "m"), "Brandon": ("Брэндон", "m"),
            "Trevor": ("Тревор", "m"), "Kevin": ("Кевин", "m"), "Chad": ("Чед", "m"), "Brad": ("Брэд", "m"),
            "Nathan": ("Нейтан", "m"), "Connor": ("Коннор", "m"), "Owen": ("Оуэн", "m"), "Hunter": ("Хантер", "m"),
            "Emma": ("Эмма", "f"), "Olivia": ("Оливия", "f"), "Sophia": ("София", "f"), "Ava": ("Ава", "f"),
            "Mia": ("Мия", "f"), "Chloe": ("Хлоя", "f"), "Lily": ("Лили", "f"), "Zoe": ("Зои", "f"),
            "Hannah": ("Ханна", "f"), "Ella": ("Элла", "f"), "Nora": ("Нора", "f"), "Grace": ("Грейс", "f"),
            "Riley": ("Райли", "f"), "Aria": ("Ария", "f"), "Luna": ("Луна", "f"), "Hazel": ("Хейзел", "f"),
            "Ivy": ("Айви", "f"), "Stella": ("Стелла", "f"), "Maya": ("Майя", "f"), "Ruby": ("Руби", "f"),
            "Violet": ("Вайолет", "f"), "Willow": ("Уиллоу", "f"), "Jade": ("Джейд", "f"), "Amber": ("Эмбер", "f"),
        },
    }
    # names that never decline although the rules would (foreign names ending in -а / -я sounds)
    RU_INDECLINABLE = {"Ноа"}
    # words the rules get wrong (a vowel that drops: парень -> парня), every case but the nominative
    RU_IRREGULAR = {
        "парень": {"gen": "парня", "dat": "парню", "acc": "парня", "ins": "парнем", "pre": "парне"},
        "Парень": {"gen": "Парня", "dat": "Парню", "acc": "Парня", "ins": "Парнем", "pre": "Парне"},
        "Рыжая": {"gen": "Рыжей", "dat": "Рыжей", "acc": "Рыжую", "ins": "Рыжей", "pre": "Рыжей"},
    }
    RU_CASES = ("nom", "gen", "dat", "acc", "ins", "pre")

    _LANG_NAME_RE = {}

    def _lang_name_table(lang):
        """(regex, {latin: local}) of a language, built once."""
        if lang not in _LANG_NAME_RE:
            import re as _re
            _t = LANG_NAMES.get(lang)
            if not _t:
                _LANG_NAME_RE[lang] = None
            else:
                _keys = sorted(_t, key=len, reverse=True)
                _rx = _re.compile(r"(?<![A-Za-z])(%s)(?![A-Za-z])" % "|".join(_re.escape(_k) for _k in _keys))
                _LANG_NAME_RE[lang] = (_rx, dict((_k, _v[0]) for _k, _v in _t.items()))
        return _LANG_NAME_RE[lang]

    def lang_replace_names(text):
        """config.replace_text: every Latin name on screen -> its local form, in a language of LANG_NAMES."""
        _t = _lang_name_table(renpy.game.preferences.language)
        if _t is None or not text:
            return text
        return _t[0].sub(lambda _m: _t[1][_m.group(1)], text)

    config.replace_text = lang_replace_names

    _RU_SIBILANT = "жшщчц"
    _RU_NO_Y = "гкхжшщч"            # after these: и, never ы

    def ru_decline(name, case, gender="m"):
        """A Russian personal name in a case (RU_CASES). Indeclinable: foreign names on a vowel other than -а / -я,
        women's names on a consonant, RU_INDECLINABLE."""
        if case == "nom" or not name or name in RU_INDECLINABLE:
            return name
        if name in RU_IRREGULAR:
            return RU_IRREGULAR[name][case]
        _last = name[-1]
        _stem = name[:-1]
        if name.endswith("ия"):
            return _stem + {"gen": "и", "dat": "и", "acc": "ю", "ins": "ей", "pre": "и"}[case]
        if _last == "я":
            return _stem + {"gen": "и", "dat": "е", "acc": "ю", "ins": "ей", "pre": "е"}[case]
        if _last == "а":
            _y = "и" if _stem[-1:] in _RU_NO_Y else "ы"
            _o = "ей" if _stem[-1:] in _RU_SIBILANT else "ой"
            return _stem + {"gen": _y, "dat": "е", "acc": "у", "ins": _o, "pre": "е"}[case]
        if gender == "f" or _last in "оеиуюэыё":
            return name
        if _last in "йь":
            return _stem + {"gen": "я", "dat": "ю", "acc": "я", "ins": "ем", "pre": "е"}[case]
        _o = "ем" if _last in _RU_SIBILANT else "ом"
        return name + {"gen": "а", "dat": "у", "acc": "а", "ins": _o, "pre": "е"}[case]

    def _is_cyrillic(text):
        return any(u"Ѐ" <= _c <= u"ӿ" for _c in text)

    def _case_tag(tag, argument, contents):
        """{case=gen}[girl.Name]{/case}: the name inside, in that case (Russian; other languages never use it)."""
        _case = (argument or "nom").strip()
        _table = LANG_NAMES.get("ru", {})
        _local = dict((_v[0], _v[1]) for _v in _table.values())
        _out = []
        for _kind, _text in contents:
            if _kind == renpy.TEXT_TEXT and _case in RU_CASES:
                _name = _text.strip()
                if _name in _table:
                    _ru, _g = _table[_name]
                elif _name in _local:
                    _ru, _g = _name, _local[_name]
                elif _is_cyrillic(_name):
                    _ru, _g = _name, "m"          # his own name, typed in Cyrillic
                else:
                    _ru = None                    # a Latin name nobody translated: as it is
                if _ru is not None:
                    _text = _text.replace(_name, ru_decline(_ru, _case, _g))
            _out.append((_kind, _text))
        return _out

    config.custom_text_tags["case"] = _case_tag
