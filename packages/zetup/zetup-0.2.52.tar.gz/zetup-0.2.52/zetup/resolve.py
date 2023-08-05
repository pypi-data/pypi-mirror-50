# ZETUP
#
# Zimmermann's Extensible Tools for Unified Project setups
#
# Copyright (C) 2014-2017 Stefan Zimmermann <user@zimmermann.co>
#
# ZETUP is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ZETUP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ZETUP. If not, see <http://www.gnu.org/licenses/>.

"""
Resolver for setup requirements, fetching ``.eggs/`` on demand
"""

import re
import sys

from pkg_resources import (
    get_distribution, working_set, DistributionNotFound, VersionConflict)
from setuptools.dist import Distribution

__all__ = ['resolve']


#: The egg installer
INSTALLER = Distribution().fetch_build_egg


class StdErrWrapper(object):
    """
    For safely redirecting ``stdout`` to ``stderr``

    For example on Windows, directly assigning ``stderr`` to ``stdout`` often
    leads to a detached ``stderr`` buffer in the end
    """

    def __getattr__(self, name):
        return getattr(sys.__stderr__, name)

    def detach(self):
        """
        Don't let ``stderr``'s buffer get stolen
        """
        return self

    def __del__(self):
        """
        Don't let :meth:`.__getattr__` fetch ``stderr``'s ``.__del__``
        """
        pass


def resolve(requirements):
    """
    Make sure that setup `requirements` are always correctly resolved and
    accessible by:

    * Recursively resolving their runtime requirements
    * Moving any installed eggs to the front of ``sys.path``
    * Updating ``pkg_resources.working_set`` accordingly
    """
    # don't pollute stdout! first backup
    __stdout__ = sys.__stdout__
    stdout = sys.stdout
    # then redirect to stderr...
    sys.stdout = sys.__stdout__ = StdErrWrapper()

    def _resolve(requirements, parent=None):
        """
        The actual recursive `requirements` resolver

        `parent` string is used for printing fully qualified requirement
        chains
        """
        for req in requirements:
            qualreq = parent and '%s->%s' % (req, parent) or req
            print("Resolving setup requirement %s:" % qualreq)
            try:
                dist = get_distribution(req)
            except (DistributionNotFound, VersionConflict):
                dist = INSTALLER(req)
                sys.path.insert(0, dist.location)
                working_set.add_entry(dist.location)
            print(repr(dist))
            extras = re.match(r'[^#\[]*\[([^#\]]*)\]', req)
            if extras:
                extras = list(map(str.strip, extras.group(1).split(',')))
            _resolve((str(req).split(';')[0]
                      for req in dist.requires(extras=extras or ())),
                     qualreq)

    _resolve((str(req).split(';')[0] for req in requirements))
    # ... and finally restore stdout
    sys.__stdout__ = __stdout__
    sys.stdout = stdout
