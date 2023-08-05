import logging
import subprocess
import re
import sys

log = logging.getLogger(sys.modules[__name__].__name__)

FLAG_REGEX = "(?:(?:get_value|GetValue|GetValueAsync|GetValueForUser|GetValueAsyncForUser)(?:.*?\s*?)?\((?:\s*?)(?:[\"'])(?P<flags>.+?)(?:[\"'])|(?:getValue|getValueAsync)(?:.*?\s*?)?\((?:.*?\s*?)(?:[\"'])(?P<jflags>.+?)(?:[\"'])|(?:[\"'])(?P<remote_keys>##KEYS_PLACEHOLDER##)(?:[\"']))"


class ReferenceFinder:
    def __init__(self,
                 path):
        self._path = path

    def find_references(self, remote_keys):
        try:
            log.info("Searching for ConfigCat setting references.")

            regex_final = FLAG_REGEX.replace("##KEYS_PLACEHOLDER##", '|'.join(remote_keys))
            args = ["ag", "-s", "-o", regex_final, self._path]
            result = subprocess.check_output(args)

            matches = re.findall(regex_final, result.decode("utf-8"))
            log.info("%s references found.", len(matches))

            flags = []
            for match in matches:
                for group in match:
                    if group:
                        flags.append(group.strip())

            distinct = set(flags)
            log.debug("Distinct setting reference keys: %s", distinct)
            return distinct
        except subprocess.CalledProcessError:
            log.warning("No feature flag references found!")
            return set()
