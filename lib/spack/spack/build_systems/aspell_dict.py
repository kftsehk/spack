# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import llnl.util.filesystem as fs

import spack.directives
import spack.spec
import spack.util.executable
import spack.util.prefix

from .autotools import AutotoolsBuilder, AutotoolsPackage


class AspellBuilder(AutotoolsBuilder):
    """The Aspell builder is close enough to an autotools builder to allow
    specializing the builder class, so to use variables that are specific
    to the Aspell extensions.
    """

    def configure(
        self,
        pkg: "AspellDictPackage",  # type: ignore[override]
        spec: spack.spec.Spec,
        prefix: spack.util.prefix.Prefix,
    ):
        aspell = spec["aspell"].prefix.bin.aspell
        prezip = spec["aspell"].prefix.bin.prezip
        destdir = prefix

        sh = spack.util.executable.Executable("/bin/sh")
        sh("./configure", "--vars", f"ASPELL={aspell}", f"PREZIP={prezip}", f"DESTDIR={destdir}")


# Aspell dictionaries install their bits into their prefix.lib
# and when activated they'll get symlinked into the appropriate aspell's
# dict dir (see aspell's {de,}activate methods).
#
# They aren't really an Autotools package, but it's close enough
# that this works if we override configure().
class AspellDictPackage(AutotoolsPackage):
    """Specialized class for building aspell dictionairies."""

    spack.directives.extends("aspell", when="build_system=autotools")

    #: Override the default autotools builder
    AutotoolsBuilder = AspellBuilder

    def patch(self):
        aspell_spec = self.spec["aspell"]
        aspell = aspell_spec.command
        dictdir = aspell("dump", "config", "dict-dir", output=str).strip()
        datadir = aspell("dump", "config", "data-dir", output=str).strip()
        dictdir = os.path.relpath(dictdir, aspell_spec.prefix)
        datadir = os.path.relpath(datadir, aspell_spec.prefix)
        fs.filter_file(r"^dictdir=.*$", f"dictdir=/{dictdir}", "configure")
        fs.filter_file(r"^datadir=.*$", f"datadir=/{datadir}", "configure")
