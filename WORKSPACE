workspace(name = "warehouse")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# Setup our Python Support
http_archive(
    name = "rules_python",
    sha256 = "a3a6e99f497be089f81ec082882e40246bfd435f52f4e82f37e89449b04573f6",
    strip_prefix = "rules_python-0.10.2",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.10.2.tar.gz",
)

load("@rules_python//python:pip.bzl", "pip_parse")

# Setup our external dependencies specifically for our pip-compile
# wrapper. We cannot use our standard lockfile for this, as pip-compile
# is intended to produce this.
pip_parse(
    name = "pip_compile_deps",
    requirements_lock = "//rules/python/pip_compile:requirements.txt",
)
load("@pip_compile_deps//:requirements.bzl", pip_compile_install_deps = "install_deps")
pip_compile_install_deps()

# Setup our default external dependencies that can be installed from pip
pip_parse(
   name = "pip",
   requirements_lock = "//external/pypi/default:requirements.txt",
    # requirements_lock = "//:requirements.txt",
)
load("@pip//:requirements.bzl", "install_deps")
install_deps()


# Setup Go Support
http_archive(
    name = "io_bazel_rules_go",
    sha256 = "685052b498b6ddfe562ca7a97736741d87916fe536623afb7da2824c0211c369",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/rules_go/releases/download/v0.33.0/rules_go-v0.33.0.zip",
        "https://github.com/bazelbuild/rules_go/releases/download/v0.33.0/rules_go-v0.33.0.zip",
    ],
)

load("@io_bazel_rules_go//go:deps.bzl", "go_register_toolchains", "go_rules_dependencies")

go_rules_dependencies()
go_register_toolchains(version = "1.18.3")


# Setup Gazelle Support
http_archive(
    name = "bazel_gazelle",
    sha256 = "501deb3d5695ab658e82f6f6f549ba681ea3ca2a5fb7911154b5aa45596183fa",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-gazelle/releases/download/v0.26.0/bazel-gazelle-v0.26.0.tar.gz",
        "https://github.com/bazelbuild/bazel-gazelle/releases/download/v0.26.0/bazel-gazelle-v0.26.0.tar.gz",
    ],
)

load("@bazel_gazelle//:deps.bzl", "gazelle_dependencies")

gazelle_dependencies()

load("@rules_python//gazelle:deps.bzl", _py_gazelle_deps = "gazelle_deps")

_py_gazelle_deps()
