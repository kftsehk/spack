# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.util.environment import EnvironmentModifications


class Rstudio(CMakePackage):
    """RStudio is an integrated development environment (IDE) for R."""

    homepage = "https://www.rstudio.com/products/rstudio/"
    url = "https://github.com/rstudio/rstudio/archive/refs/tags/v1.4.1717.tar.gz"
    git = "https://github.com/rstudio/rstudio.git"

    mainainers = ["dorton21"]
    version("main", git=git, branch="main")
    version("2024.09.1", git=git, tag="v2024.09.1+394", preferred=True)
    version("2024.04.2", git=git, tag="v2024.04.2+764")
    version("2023.12.1", git=git, tag="v2023.12.1+402")
    version("2023.09.0", git=git, tag="v2023.09.0+463")
    version("2023.06.2", git=git, tag="v2023.06.2+561")
    version("2023.03.2", git=git, tag="v2023.03.2+454")

    version(
        "1.4.1717",
        sha256="3af234180fd7cef451aef40faac2c7b52860f14a322244c1c7aede029814d261",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("notebook", default=False, when="@:1", description="Enable notebook support.")

    depends_on("cmake@3.4.3:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("ant", type="build")
    depends_on("r@3.0.1:", type=("build", "run"))

    depends_on("patchelf@0.9:")
    depends_on("pandoc@2.11.4:")
    depends_on("yaml-cpp")  # find_package fails with newest version

    # for old "@:1"
    depends_on("boost+pic@1.69:", when="@:1")
    depends_on("icu4c", when="@:1")
    depends_on("java@8:", when="@:1")
    depends_on("qt+webkit@5.12:", when="@:1")
    depends_on("soci~static+boost+postgresql+sqlite", when="@:1")

    # for new "@2020:"
    depends_on(
        "boost+atomic+chrono+date_time+filesystem+iostreams+program_options+random+regex+signals+system+thread+pic@1.69:",
        when="@2020:",
    )
    depends_on("fontconfig", when="@2020:")
    depends_on("egl", when="@2020:")
    depends_on("soci@4+sqlite+boost+static cxxstd=11 cppflags='-fpic'", when="@2020:")
    depends_on("uuid", when="@2020:")

    with when("+notebook"):
        depends_on("r-base64enc")
        depends_on("r-digest")
        depends_on("r-evaluate")
        depends_on("r-glue")
        depends_on("r-highr")
        depends_on("r-htmltools")
        depends_on("r-jsonlite")
        depends_on("r-knitr")
        depends_on("r-magrittr")
        depends_on("r-markdown")
        depends_on("r-mime")
        depends_on("r-rmarkdown")
        depends_on("r-stringi")
        depends_on("r-stringr")
        depends_on("r-tinytex")
        depends_on("r-xfun")
        depends_on("r-yaml")

    # to use node-js provided by spack
    patch(
        "https://src.fedoraproject.org/rpms/rstudio/raw/5bda2e290c9e72305582f2011040938d3e356906/f/0004-use-system-node.patch",
        sha256="4a6aff2b586ddfceb7c59215e5f4a03f25b08fcc55687acaa6ae23c11d75d0e8",
        when="@:1",
    )

    def cmake_args(self):
        args = [
            "-DRSTUDIO_PACKAGE_BUILD=Yes",
            "-DRSTUDIO_USE_SYSTEM_YAML_CPP=Yes",
            "-DRSTUDIO_USE_SYSTEM_BOOST=Yes",
            "-DRSTUDIO_USE_SYSTEM_SOCI=Yes",
        ]
        if self.spec.satisfies("@:1"):
            args += [
                "-DRSTUDIO_TARGET=Desktop",
                '-DQT_QMAKE_EXECUTABLE="{0}"'.format(self.spec["qt"].prefix.bin.qmake),
            ]

        if self.spec.satisfies("@2020:"):
            args += ["-DRSTUDIO_TARGET=Electron", "-DCMAKE_CXX_FLAGS=-fpic"]

        return args

    def setup_build_environment(self, env):
        env.set("RSTUDIO_TOOLS_ROOT", self.prefix.tools)

    def patch(self):
        # remove hardcoded soci path to use spack soci
        if self.spec["soci"].version <= Version("4.0.0"):
            soci_lib = self.spec["soci"].prefix.lib64
        else:
            soci_lib = self.spec["soci"].prefix.lib
        filter_file(
            'set(SOCI_LIBRARY_DIR "/usr/lib")',
            'set(SOCI_LIBRARY_DIR "{0}")'.format(soci_lib),
            "src/cpp/CMakeLists.txt",
            string=True,
        )

        # new R-studio 202x requires specific version of node-js
        # allow a r-specific node-js instance to be installed for r-studio
        if self.spec.satisfies("@:1"):
            # fix hardcoded path for node-js in use_system_node patch
            filter_file(
                '<property name="node.bin" value="/usr/bin/node"/>',
                '<property name="node.bin" value="{0}"/>'.format(
                    self.spec["node-js"].prefix.bin.node
                ),
                "src/gwt/build.xml",
                string=True,
            )
            # unbundle icu libraries
            filter_file(
                "${QT_LIBRARY_DIR}/${ICU_LIBRARY}.so",
                join_path(self.spec["icu4c"].prefix.lib, "${ICU_LIBRARY}.so"),
                "src/cpp/desktop/CMakeLists.txt",
                string=True,
            )

    @run_before("cmake")
    def install_deps(self):

        common_deps_dir = "dependencies/common"
        with working_dir(common_deps_dir):
            Executable("./install-dictionaries")()
            Executable("./install-mathjax")()
            Executable("./install-quarto")()
            Executable("./install-npm-dependencies")()
            Executable("./install-panmirror")()

        # two methods for pandoc
        # 1) replace install-pandoc:
        #    - link pandoc into tools/pandoc/$PANDOC_VERSION
        #      (this is what install-pandoc would do)
        #    - cmake then installs pandoc files from there into bin
        # 2) remove install-pandoc and cmake install step + link directly into bin

        # method 1)
        filter_file(
            'set(PANDOC_VERSION "2.11.4" CACHE INTERNAL "Pandoc version")',
            'set(PANDOC_VERSION "{0}" CACHE INTERNAL "Pandoc version")'.format(
                self.spec["pandoc"].version
            ),
            "src/cpp/session/CMakeLists.txt",
            string=True,
        )

        filter_file(
            "set(RSTUDIO_INSTALL_ELECTRON .)",
            "set(RSTUDIO_INSTALL_ELECTRON ./bin)",
            "cmake/globals.cmake",
            string=True,
        )

        # jsonrpc fix: boost forbids implicit conversion from boost::function<void> to bool
        filter_file(
            "   return afterResponse_;",
            "   return (bool) afterResponse_;",
            "src/cpp/core/json/JsonRpc.cpp",
            string=True,
        )

        pandoc_dir = join_path(self.prefix.tools, "pandoc", self.spec["pandoc"].version)
        os.makedirs(pandoc_dir)
        with working_dir(pandoc_dir):
            os.symlink(self.spec["pandoc"].prefix.bin.pandoc, "pandoc")
            os.symlink(
                os.path.join(self.spec["pandoc"].prefix.bin, "pandoc-citeproc"), "pandoc-citeproc"
            )
