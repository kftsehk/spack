# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path as osp

from ruamel.yaml import YAML

import spack.url
from spack.package import *


class Protobuf(CMakePackage):
    """Google's data interchange format."""

    homepage = "https://developers.google.com/protocol-buffers"
    url = "https://github.com/protocolbuffers/protobuf.git"
    git = "https://github.com/protocolbuffers/protobuf.git"
    maintainers("hyoklee")

    license("BSD-3-Clause")

    with open(osp.join(osp.dirname(osp.abspath(__file__)), "versions.yaml"), "r") as f:
        __VERSION_DATA__ = YAML().load(f)

    for _i, _v in enumerate(reversed(__VERSION_DATA__["versions"]["tags"])):
        version(_v, tag=f"v{_v}", preferred=_i == 0)

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("shared", default=True, description="Enables the build of shared libraries")
    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    depends_on("abseil-cpp@20230125.3:", when="@3.22.5:")
    # https://github.com/protocolbuffers/protobuf/issues/11828#issuecomment-1433557509
    depends_on("abseil-cpp@20230125:", when="@3.22:")
    depends_on("zlib-api")

    conflicts("%gcc@:4.6", when="@3.6.0:")  # Requires c++11
    conflicts("%gcc@:4.6", when="@3.2.0:3.3.0")  # Breaks

    # first fixed in 3.4.0: https://github.com/google/protobuf/pull/3406
    patch("pkgconfig.patch", when="@3.0.2:3.3.2")

    patch("intel-v1.patch", when="@3.2:3.6 %intel")

    # See https://github.com/protocolbuffers/protobuf/pull/7197
    patch("intel-v2.patch", when="@3.7:3.11.4 %intel")

    # See https://github.com/protocolbuffers/protobuf/issues/9916
    patch(
        "https://github.com/protocolbuffers/protobuf/pull/9936.patch?full_index=1",
        when="@3.20 %gcc@12.1.0",
        sha256="fa1abf042eddc1b3b43875dc018c651c90cd1c0c5299975a818a1610bee54ab8",
    )

    # fix build on Centos 8, see also https://github.com/protocolbuffers/protobuf/issues/5144
    patch(
        "https://github.com/protocolbuffers/protobuf/commit/462964ed322503af52638d54c00a0a67d7133349.patch?full_index=1",
        when="@3.4:3.21",
        sha256="9b6dcfa30dd3ae0abb66ab0f252a4fc1e1cc82a9820d2bdb72da35c4f80c3603",
    )

    patch("msvc-abseil-target-namespace.patch", when="@3.22 %msvc")

    # Misisng #include "absl/container/internal/layout.h"
    # See https://github.com/protocolbuffers/protobuf/pull/14042
    patch(
        "https://github.com/protocolbuffers/protobuf/commit/e052928c94f5a9a6a6cbdb82e09ab4ee92b7815f.patch?full_index=1",
        when="@3.22:3.24.3 ^abseil-cpp@20240116:",
        sha256="20e3cc99a9513b256e219653abe1bfc7d6b6a5413e269676e3d442830f99a1af",
    )

    # Missing #include "absl/strings/str_cat.h"
    # See https://github.com/protocolbuffers/protobuf/pull/14054
    patch(
        "https://github.com/protocolbuffers/protobuf/commit/38a24729ec94e6576a1425951c898ad0b91ad2d2.patch?full_index=1",
        when="@3.22:3.24.3 ^abseil-cpp@20240116:",
        sha256="c061356db31cdce29c8cdd98a3a8219ef048ebc2318d0dec26c1f2c5e5dae29b",
    )

    def fetch_remote_versions(self, *args, **kwargs):
        """Ignore additional source artifacts uploaded with releases,
        only keep known versions
        fix for https://github.com/spack/spack/issues/5356"""
        return dict(
            map(
                lambda u: (u, self.url_for_version(u)),
                spack.url.find_versions_of_archive(self.all_urls, self.list_url, self.list_depth),
            )
        )

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("protobuf_BUILD_TESTS", False),
            self.define("CMAKE_POSITION_INDEPENDENT_CODE", True),
        ]

        if self.spec.satisfies("@3.22:"):
            cxxstd = self.spec["abseil-cpp"].variants["cxxstd"].value
            args.extend(
                [
                    self.define("protobuf_ABSL_PROVIDER", "package"),
                    self.define("CMAKE_CXX_STANDARD", cxxstd),
                ]
            )

        if self.spec.satisfies("platform=darwin"):
            args.append(self.define("CMAKE_MACOSX_RPATH", True))

        return args

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@:3.20"):
            return join_path(self.stage.source_path, "cmake")
        else:
            return self.stage.source_path
