"""Module to work with Siren links."""

import lila.core.common as common
from lila.core.base import Component


class Link(Component):
    """Class to work with Siren link."""

    def __init__(self, relations, target, classes=(), title=None, target_media_type=None):
        # pylint: disable=too-many-arguments
        super(Link, self).__init__(classes=classes)

        self._relations = common.adjust_relations(relations)
        self._target = str(target)

        if title is not None:
            title = str(title)
        self._title = title

        if target_media_type is not None:
            target_media_type = str(target_media_type)
        self._target_media_type = target_media_type

    @property
    def relations(self):
        """Relationships between the link and entity."""
        return tuple(self._relations)

    @property
    def target(self):
        """Target of the link."""
        return self._target

    @property
    def title(self):
        """Descriptive title for the link."""
        return self._title

    @property
    def target_media_type(self):
        """Media type of the target resource."""
        return self._target_media_type


class EmbeddedLink(Link):
    """Class to work with embedded Siren links."""

    def __init__(self, relations, target, classes=(), title=None, target_media_type=None):
        # pylint: disable=too-many-arguments
        relations = common.adjust_relations(relations)
        if not relations:
            raise ValueError("No relations are passed to create an embedded link")

        super(EmbeddedLink, self).__init__(
            relations=relations,
            target=target,
            classes=classes,
            title=title,
            target_media_type=target_media_type,
            )
