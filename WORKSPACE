workspace(name = "warehouse")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

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
)
load("@pip//:requirements.bzl", "install_deps")
install_deps()
