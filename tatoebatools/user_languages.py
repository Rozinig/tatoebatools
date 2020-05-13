import csv
import logging

from .config import DATA_DIR
from .utils import lazy_property
from .version import Version

logger = logging.getLogger(__name__)


class UserLanguages:
    """The self-reported skill levels of members in individual languages. 
    """

    _table = "user_languages"
    _dir = DATA_DIR.joinpath(_table)

    def __init__(self, language):

        self._lg = language

    def __iter__(self):

        try:
            with open(self.path) as f:
                fieldnames = [
                    "lang",
                    "skill_level",
                    "username",
                    "details",
                ]

                rows = csv.DictReader(
                    f, delimiter="\t", escapechar="\\", fieldnames=fieldnames
                )
                for row in rows:
                    yield UserLanguage(**row)
        except OSError:
            msg = (
                f"no data locally available for the "
                f"'{UserLanguages._table}' table."
            )

            logger.warning(msg)

    @property
    def language(self):
        """Get the language of the datafile.
        """
        return self._lg

    @property
    def filename(self):
        """Get the name of the datafile.
        """
        return f"{self._lg}_{UserLanguages._table}.tsv"

    @property
    def path(self):
        """Get the path of the datafile.
        """
        return UserLanguages._dir.joinpath(self.filename)

    @lazy_property
    def version(self):
        """Get the version of the downloaded data.
        """
        with Version() as vs:
            return vs[self.filename]


class UserLanguage:
    """The self-reported skill level of a user in a language.
    """

    def __init__(self, lang, skill_level, username, details):
        # the language
        self._lg = lang
        # the leval of the user in this language
        self._skl = skill_level
        # the name of the user
        self._usr = username
        # optional comments
        self._dtl = details

    @property
    def lang(self):
        """Get the language for this user skill. 
        """
        return self._lg

    @property
    def skill_level(self):
        """Get the value of this skill level. 
        """
        return int(self._skl) if self._skl != "N" else None

    @property
    def username(self):
        """Get the name of the user who have this language skill. 
        """
        return self._usr

    @property
    def details(self):
        """Get more details about this user's language skill.
        """
        return self._dtl