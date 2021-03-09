# coding: utf-8

from dataclasses import dataclass
from pathlib import Path
import uritools
from bookworm import typehints as t
from bookworm.logger import logger


log = logger.getChild(__name__)
BOOKWORM_URI_SCHEME = "bkw"


@dataclass
class DocumentUri:
    format: str
    path: str
    openner_args: dict[str, t.Union[str, int]]

    @classmethod
    def from_uri_string(cls, uri_string):
        """Return a populated instance of this class or raise ValueError."""
        if not uritools.isuri(uri_string):
            raise ValueError(f"Invalid uri string {uri_string}")
        try:
            parsed = uritools.urisplit(uri_string)
        except Exception as e:
            raise ValueError(f"Could not parse uri {uri_string}") from e
        return cls(
            format=parsed.authority,
            path=uritools.uridecode(parsed.path).lstrip("/"),
            openner_args=parsed.getquerydict(),
        )

    @classmethod
    def from_filename(cls, filename):
        filepath = Path(filename)
        return cls(
            format=filepath.suffix.lstrip("."),
            path=str(filepath),
            openner_args={}
        )
    def to_uri_string(self):
        return uritools.uricompose(
            scheme=BOOKWORM_URI_SCHEME,
            authority=self.format,
            path=f"/{str(self.path)}",
            query=self.openner_args
        )

    def to_bare_uri_string(self):
        return uritools.uricompose(
            scheme=BOOKWORM_URI_SCHEME,
            authority=self.format,
            path=f"/{str(self.path)}",
        )

    def __hash__(self):
        return hash(self.to_uri_string())

    def __str__(self):
        return self.to_uri_string()

    def __repr__(self):
        return f"DocumentUri(format='{self.format}', path='{self.path}', openner_args={self.openner_args})"

    def __eq__(self, other):
        if not isinstance(other, DocumentUri):
            return NotImplemented
        return all(
            self.format == other.format,
            self.path == other.path
        )