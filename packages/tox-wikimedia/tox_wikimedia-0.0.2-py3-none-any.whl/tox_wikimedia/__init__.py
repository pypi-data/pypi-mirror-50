"""
Copyright (C) 2019 Kunal Mehta <legoktm@member.fsf.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
import pluggy
import os
from tox.config import DepConfig
from tox.reporter import verbosity2

hookimpl = pluggy.HookimplMarker("tox")


# Pre-configured tools
TOOLS = {
    "flake8": {"commands": ["flake8"], "deps": ["flake8"]},
    "pytest": {"commands": ["pytest"], "deps": ["pytest"]},
}


def is_enabled(toxinidir):
    # TODO: is there a tox API to read this?
    toxini = os.path.join(toxinidir, "tox.ini")
    assert os.path.exists(toxini)
    config = ConfigParser()
    config.read(toxini)
    return "wikimedia" in config


@hookimpl
def tox_configure(config):
    # Only run if we're enabled
    if not is_enabled(str(config.toxinidir)):
        verbosity2("[wikimedia] tox-wikimedia is not enabled, skipping")
        return

    verbosity2("[wikimedia] tox-wikimedia is enabled")
    for envname, config in config.envconfigs.items():
        for factor in config.factors:
            # factors are py35, flake8, pytest, etc.
            try:
                fconfig = TOOLS[factor]
            except KeyError:
                continue

            for dep in fconfig["deps"]:
                # Check to make sure the dep is not already
                # specific (e.g. to specify a constraint)
                for cdep in config.deps:
                    if dep in cdep.name:
                        break
                else:
                    config.deps.append(DepConfig(dep))
                    verbosity2(
                        "[wikimedia] {}: Adding dep on {}".format(envname, dep)
                    )
            if not config.commands:
                # If there's no command, then set one
                config.commands.append(fconfig["commands"])
                verbosity2(
                    "[wikimedia] {}: Setting command to {}".format(
                        envname, str(fconfig["commands"])
                    )
                )
