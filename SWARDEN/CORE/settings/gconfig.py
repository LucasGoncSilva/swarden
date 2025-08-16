from gc import collect, freeze, set_threshold


def gc_config() -> None:
    set_threshold(1000, 1000, 1000)
    collect()
    freeze()
