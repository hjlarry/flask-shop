from pluggy.manager import PluginManager, DistFacade
import sys

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata

from .models import PluginRegistry

class FlaskshopPluginManager(PluginManager):
    def __init__(self, project_name, implprefix=None):
        super().__init__(project_name, implprefix)
        self.external_plugins = set()   # hack here

    def load_setuptools_entrypoints(self, group, name=None):
        count = 0
        for dist in importlib_metadata.distributions():
            for ep in dist.entry_points:
                if (
                    ep.group != group
                    or (name is not None and ep.name != name)
                    # already registered
                    or self.get_plugin(ep.name)
                    or self.is_blocked(ep.name)
                ):
                    continue
                plugin = ep.load()
                self.register(plugin, name=ep.name)
                self.external_plugins.add(ep.name)  # hack here
                self._plugin_distinfo.append((plugin, DistFacade(dist)))
                count += 1
        return count

