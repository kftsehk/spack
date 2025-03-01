# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Readline(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Readline library provides a set of functions for use by
    applications that allow users to edit command lines as they are typed in.
    Both Emacs and vi editing modes are available. The Readline library
    includes additional functions to maintain a list of previously-entered
    command lines, to recall and perhaps reedit those lines, and perform
    csh-like history expansion on previous commands."""

    homepage = "https://tiswww.case.edu/php/chet/readline/rltop.html"
    # URL must remain http:// so Spack can bootstrap curl
    gnu_mirror_path = "readline/readline-8.0.tar.gz"

    license("GPL-3.0-or-later")

    version("8.2", sha256="3feb7171f16a84ee82ca18a36d7b9be109a52c04f492a053331d7d1095007c35")
    version("8.1", sha256="f8ceb4ee131e3232226a17f51b164afc46cd0b9e6cef344be87c65962cb82b02")
    version("8.0", sha256="e339f51971478d369f8a053a330a190781acb9864cf4c541060f12078948e461")
    version("7.0", sha256="750d437185286f40a369e1e4f4764eda932b9459b5ec9a731628393dd3d32334")
    version("6.3", sha256="56ba6071b9462f980c5a72ab0023893b65ba6debb4eeb475d7a563dc65cafd43")

    depends_on("c", type="build")  # generated

    depends_on("ncurses")

    patches = [
        ("8.2", "001", "bbf97f1ec40a929edab5aa81998c1e2ef435436c597754916e6a5868f273aff7"),
        ("8.2", "002", "e06503822c62f7bc0d9f387d4c78c09e0ce56e53872011363c74786c7cd4c053"),
        ("8.2", "003", "24f587ba46b46ed2b1868ccaf9947504feba154bb8faabd4adaea63ef7e6acb0"),
        ("8.2", "004", "79572eeaeb82afdc6869d7ad4cba9d4f519b1218070e17fa90bbecd49bd525ac"),
        ("8.2", "005", "622ba387dae5c185afb4b9b20634804e5f6c1c6e5e87ebee7c35a8f065114c99"),
        ("8.2", "006", "c7b45ff8c0d24d81482e6e0677e81563d13c74241f7b86c4de00d239bc81f5a1"),
        ("8.2", "007", "5911a5b980d7900aabdbee483f86dab7056851e6400efb002776a0a4a1bab6f6"),
        ("8.2", "008", "a177edc9d8c9f82e8c19d0630ab351f3fd1b201d655a1ddb5d51c4cee197b26a"),
        ("8.2", "009", "3d9885e692e1998523fd5c61f558cecd2aafd67a07bd3bfe1d7ad5a31777a116"),
        ("8.2", "010", "758e2ec65a0c214cfe6161f5cde3c5af4377c67d820ea01d13de3ca165f67b4c"),
        ("8.2", "011", "e0013d907f3a9e6482cc0934de1bd82ee3c3c4fd07a9646aa9899af237544dd7"),
        ("8.2", "012", "6c8adf8ed4a2ca629f7fd11301ed6293a6248c9da0c674f86217df715efccbd3"),
        ("8.2", "013", "1ea434957d6ec3a7b61763f1f3552dad0ebdd6754d65888b5cd6d80db3a788a8"),
        ("8.1", "001", "682a465a68633650565c43d59f0b8cdf149c13a874682d3c20cb4af6709b9144"),
        ("8.1", "002", "e55be055a68cb0719b0ccb5edc9a74edcc1d1f689e8a501525b3bc5ebad325dc"),
        ("8.0", "001", "d8e5e98933cf5756f862243c0601cb69d3667bb33f2c7b751fe4e40b2c3fd069"),
        ("8.0", "002", "36b0febff1e560091ae7476026921f31b6d1dd4c918dcb7b741aa2dad1aec8f7"),
        ("8.0", "003", "94ddb2210b71eb5389c7756865d60e343666dfb722c85892f8226b26bb3eeaef"),
        ("8.0", "004", "b1aa3d2a40eee2dea9708229740742e649c32bb8db13535ea78f8ac15377394c"),
        ("7.0", "001", "9ac1b3ac2ec7b1bf0709af047f2d7d2a34ccde353684e57c6b47ebca77d7a376"),
        ("7.0", "002", "8747c92c35d5db32eae99af66f17b384abaca961653e185677f9c9a571ed2d58"),
        ("7.0", "003", "9e43aa93378c7e9f7001d8174b1beb948deefa6799b6f581673f465b7d9d4780"),
        ("7.0", "004", "f925683429f20973c552bff6702c74c58c2a38ff6e5cf305a8e847119c5a6b64"),
        ("7.0", "005", "ca159c83706541c6bbe39129a33d63bbd76ac594303f67e4d35678711c51b753"),
        ("6.3", "001", "1a79bbb6eaee750e0d6f7f3d059b30a45fc54e8e388a8e05e9c3ae598590146f"),
        ("6.3", "002", "39e304c7a526888f9e112e733848215736fb7b9d540729b9e31f3347b7a1e0a5"),
        ("6.3", "003", "ec41bdd8b00fd884e847708513df41d51b1243cecb680189e31b7173d01ca52f"),
        ("6.3", "004", "4547b906fb2570866c21887807de5dee19838a60a1afb66385b272155e4355cc"),
        ("6.3", "005", "877788f9228d1a9907a4bcfe3d6dd0439c08d728949458b41208d9bf9060274b"),
        ("6.3", "006", "5c237ab3c6c97c23cf52b2a118adc265b7fb411b57c93a5f7c221d50fafbe556"),
        ("6.3", "007", "4d79b5a2adec3c2e8114cbd3d63c1771f7c6cf64035368624903d257014f5bea"),
        ("6.3", "008", "3bc093cf526ceac23eb80256b0ec87fa1735540d659742107b6284d635c43787"),
    ]

    # TODO: patches below are not managed by the GNUMirrorPackage base class
    for verstr, num, checksum in patches:
        ver = Version(verstr)
        patch(
            "https://ftpmirror.gnu.org/readline/readline-{0}-patches/readline{1}-{2}".format(
                ver, ver.joined, num
            ),
            level=0,
            when="@{0}".format(ver),
            sha256=checksum,
        )

    def build(self, spec, prefix):
        make("SHLIB_LIBS=" + spec["ncurses:wide"].libs.ld_flags)

    def flag_handler(self, name, flags):
        # nvhpc is detected as a gnu compiler, which causes the build system
        # to add unrecognized -W flags. Defining CFLAGS overrides those defaults.
        if name == "cflags" and self.spec.satisfies("%nvhpc"):
            flags.append("-O2")
            flags.append("-g")
            return (None, flags, None)
        return (flags, None, None)
