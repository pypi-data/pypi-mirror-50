"""Module to work with Siren entities."""

from copy import deepcopy

import lila.core.common as common
from lila.core.base import Component
from lila.core.link import Link, EmbeddedLink
from lila.core.action import Action


class Entity(Component):
    """Class to work with Siren entities."""

    def __init__(self, title=None, classes=(), properties=(), entities=(), links=(), actions=()):
        # pylint: disable=too-many-arguments
        super(Entity, self).__init__(classes=classes)

        if title is not None:
            title = str(title)
        self._title = title

        self._properties = common.adjust_properties(properties)

        if any(not isinstance(link, Link) for link in links):
            raise ValueError("Some of the links are of incompatible type")
        self._links = tuple(links)

        if any(not isinstance(action, Action) for action in actions):
            raise ValueError("Some of the actions are of incompatible type")
        self._actions = tuple(actions)

        if any(not isinstance(entity, (EmbeddedLink, EmbeddedRepresentation)) for entity in entities):  # pylint: disable=line-too-long
            raise ValueError("Some of the entities are of incompatible type")
        self._entities = tuple(entities)

    @property
    def title(self):
        """Descriptive text about the entity."""
        return self._title

    @property
    def properties(self):
        """Properties of the entity."""
        return deepcopy(self._properties)

    @property
    def links(self):
        """Navigation links from the entity."""
        return tuple(self._links)

    @property
    def actions(self):
        """Actions of the entity."""
        return tuple(self._actions)

    @property
    def entities(self):
        """Subentities of the entity."""
        return tuple(self._entities)


class EmbeddedRepresentation(Entity):
    """Class to work with embedded Siren entities."""

    def __init__(
            self,
            relations,
            title=None,
            classes=(),
            properties=(),
            entities=(),
            links=(),
            actions=(),
        ):
        # pylint: disable=too-many-arguments
        relations = common.adjust_relations(relations)
        if not relations:
            raise ValueError("No relations are passed to create an embedded representation")
        self._relations = relations

        super(EmbeddedRepresentation, self).__init__(
            title=title,
            classes=classes,
            properties=properties,
            entities=entities,
            links=links,
            actions=actions,
            )

    @property
    def relations(self):
        """Relationship between the representation and parent entity."""
        return tuple(self._relations)
