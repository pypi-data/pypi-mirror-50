from distutils.version import StrictVersion as V

from pip import __version__
from pip._internal.index import PackageFinder


PIP_VERSION = V(__version__)


def get_dist_from_abstract_dist(abstract_dist, finder):
    if PIP_VERSION >= V("19.2"):
        return abstract_dist.get_pkg_resources_distribution()
    elif PIP_VERSION >= V("19.0"):
        return abstract_dist.dist()
    else:
        return abstract_dist.dist(finder)


def get_package_finder(session):
    if PIP_VERSION >= V("19.2"):
        from pip._internal.models.search_scope import SearchScope
        from pip._internal.models.selection_prefs import SelectionPreferences

        selection_prefs = SelectionPreferences(allow_yanked=False)
        return PackageFinder.create(
            search_scope=SearchScope(find_links=[], index_urls=[]),
            selection_prefs=selection_prefs,
            session=session,
        )
    else:
        return PackageFinder(find_links=[], index_urls=[], session=session)
