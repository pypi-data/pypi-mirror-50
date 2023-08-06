"""Module with base class for all Siren components."""

import lila.core.common as common


class Component:
    """Class for base Siren component."""

    def __init__(self, classes=()):
        self._classes = common.adjust_classes(classes)

    @property
    def classes(self):
        """Classes of the component."""
        return tuple(self._classes)
