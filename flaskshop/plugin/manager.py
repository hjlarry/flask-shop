import sys
import logging

import pluggy
from pkg_resources import iter_entry_points, DistributionNotFound


from .models import PluginRegistry
from .utils import parse_pkg_metadata

logger = logging.getLogger(__name__)


class FlaskshopPluginManager(pluggy.PluginManager):
    def __init__(self, project_name, implprefix=None):
        super().__init__(project_name, implprefix)
        self.external_plugins = set()
        self.plugin_metadata = {}

    def load_setuptools_entrypoints(self, entrypoint_name):
        """Load modules from querying the specified setuptools entrypoint name.
        Return the number of loaded plugins. """
        logger.info(f"Loading plugins under entrypoint {entrypoint_name}")
        for ep in iter_entry_points(entrypoint_name):
            if self.get_plugin(ep.name) or self.is_blocked(ep.name):
                continue

            try:
                plugin = ep.load()
            except DistributionNotFound:
                logger.warn(f"Could not load plugin '{ep.name}'. Passing.")
                continue
            except VersionConflict as e:
                raise pluggy.PluginValidationError(
                    f"Plugin '{ep.name}' could not be loaded: {e}!"
                )

            self.register(plugin, name=ep.name)
            self.external_plugins.add(ep.name)
            self._plugin_distinfo.append((plugin, ep.dist))
            self.plugin_metadata[ep.name] = parse_pkg_metadata(ep.dist.key)
            logger.info(f"Loaded plugin: {ep.name}")
        logger.info(
            f"Loaded {len(self._plugin_distinfo)} plugins for entrypoint {entrypoint_name}"
        )
        return len(self._plugin_distinfo)
