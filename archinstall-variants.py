import logging

import archinstall

__version__ = 0.1


class Plugin:
    VARIANTS_DICT_KEY = "variants"
    VARIANT_KEY = "variant"

    def __init__(self):
        if self.has_variants() and self.variants_is_dict():
            variant_key = self.get_selected_variant_key()
            variant = archinstall.arguments[self.VARIANTS_DICT_KEY][variant_key]
            self.apply_variant(variant)
            self.clean_arguments()
            archinstall.log(
                f"The '{ variant_key }' variant was applied to the arguments.",
                level=logging.INFO
            )
            archinstall.log(
                "New arguments: " + archinstall.arguments.__str__(),
                level=logging.DEBUG
            )

    def variants_is_dict(self) -> bool:
        return isinstance(self.get_variants(), dict)

    def has_variant_argument(self) -> bool:
        return self.VARIANT_KEY in archinstall.arguments and \
               isinstance(self.get_variant_argument(), str)

    def get_variant_argument(self) -> str:
        return archinstall.arguments[self.VARIANT_KEY]

    def variant_argument_in_variants(self) -> bool:
        return self.get_variant_argument() in self.get_variants()

    def get_variants(self) -> dict:
        return archinstall.arguments[self.VARIANTS_DICT_KEY]

    def has_variants(self) -> bool:
        return self.VARIANTS_DICT_KEY in archinstall.arguments

    def variant_exists(self, variant: str) -> bool:
        return variant in self.get_variants()

    def get_selected_variant_key(self) -> str:
        options = list(self.get_variants().keys())

        if self.has_variant_argument() and self.variant_argument_in_variants():
            return self.get_variant_argument()

        if len(options) > 1:
            return archinstall.generic_select(
                options,
                f"Select which variant you want to install (default: {options[0]}):",
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

    def clean_arguments(self):
        del archinstall.arguments[self.VARIANTS_DICT_KEY]
        del archinstall.arguments[self.VARIANT_KEY]

    def overwrite(self, key: str, value):
        archinstall.arguments[key] = value
