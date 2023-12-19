import logging
from importlib.metadata import entry_points, metadata

import pluggy

from .models import PluginRegistry  # noqa: F401

logger = logging.getLogger(__name__)


class FlaskshopPluginManager(pluggy.PluginManager):
    def __init__(self, project_name):
        super().__init__(project_name)
        self.external_plugins = set()
        self.plugin_metadata = {}

    def load_setuptools_entrypoints(self, group: str, name: str | None = None) -> int:
        """Load modules from querying the specified setuptools entrypoint name.
        Return the number of loaded plugins."""
        logger.info(f"Loading plugins under entrypoint {group}")
        for ep in entry_points().select(group=group):
            if self.get_plugin(ep.name) or self.is_blocked(ep.name):
                continue

            plugin = ep.load()
            self.register(plugin, name=ep.name)
            self.external_plugins.add(ep.name)
            self._plugin_distinfo.append((plugin, ep.dist))
            self.plugin_metadata[ep.name] = metadata(ep.dist._normalized_name).json
            logger.info(f"Loaded plugin: {ep.name}")
        logger.info(
            f"Loaded {len(self._plugin_distinfo)} plugins for entrypoint {group}"
        )
        return len(self._plugin_distinfo)
