load("@bazel_gazelle//:def.bzl", "gazelle")
load("@rules_python//gazelle:def.bzl", "GAZELLE_PYTHON_RUNTIME_DEPS")

# gazelle:python_generation_mode project
# gazelle:python_manifest_file_name external/pypi/default/gazelle.yaml

# gazelle:exclude services/warehouse
# gazelle:exclude tests
# gazelle:exclude bin
# gazelle:exclude docs
# gazelle:exclude dev
# gazelle:exclude gunicorn-*.py

alias(
    name = "pip-compile",
    actual = "@warehouse//rules/python/pip_compile:bin",
)

gazelle(
    name = "gazelle",
    data = GAZELLE_PYTHON_RUNTIME_DEPS,
    gazelle = "@rules_python//gazelle:gazelle_python_binary",
)
