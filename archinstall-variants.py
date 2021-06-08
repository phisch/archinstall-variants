from pprint import pprint

import archinstall

__version__ = 0.1


class Plugin:
    VARIANTS_KEY = "variants"

    def __init__(self):
        if self.has_variants() and self.variants_is_dict():
            variant_key = self.get_selected_variant_key()
            variant = archinstall.arguments[self.VARIANTS_KEY][variant_key]
            self.apply_variant(variant)
            self.remove_variants_key()
            pprint(archinstall.arguments)

    def has_variants(self) -> bool:
        return self.VARIANTS_KEY in archinstall.arguments

    def variants_is_dict(self) -> bool:
        return isinstance(archinstall.arguments[self.VARIANTS_KEY], dict)

    def get_selected_variant_key(self) -> str:
        options = list(archinstall.arguments[self.VARIANTS_KEY].keys())

        if len(options) > 1:
            return archinstall.generic_select(
                options,
                f"Select which variant you want to install (default: { options[0] }):",
                True
            ) or options[0]

        return options[0]

    def apply_variant(self, variant: dict):
        for option in variant:
            if option in archinstall.arguments:
                if isinstance(archinstall.arguments[option], list):
                    archinstall.arguments[option] += variant[option]
                    continue

            self.overwrite(option, variant[option])

    def remove_variants_key(self):
        del archinstall.arguments[self.VARIANTS_KEY]

    def overwrite(self, key: str, value):
        archinstall.arguments[key] = value
