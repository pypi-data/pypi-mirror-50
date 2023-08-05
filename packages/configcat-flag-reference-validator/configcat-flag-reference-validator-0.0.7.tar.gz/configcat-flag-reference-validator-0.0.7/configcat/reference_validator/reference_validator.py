import logging
import sys

log = logging.getLogger(sys.modules[__name__].__name__)


class ReferenceValidator:
    @staticmethod
    def validate(remote_keys,
                 reference_keys):
        missing_references = remote_keys.difference(reference_keys)
        missing_remote_keys = reference_keys.difference(remote_keys)

        result = True
        if len(missing_references) > 0:
            result = False
            log.warning(
                "There are settings set on the ConfigCat dashboard which are not used anywhere in the code! Keys: %s!",
                missing_references)

        if len(missing_remote_keys) > 0:
            result = False
            log.warning(
                "There are settings used in the code which are not set on the ConfigCat dashboard! Keys: %s!",
                missing_remote_keys)

        return result
