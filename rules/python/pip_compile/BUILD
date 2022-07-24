load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@rules_python//gazelle/modules_mapping:def.bzl", "modules_mapping")
load("@rules_python//gazelle/manifest:defs.bzl", "gazelle_python_manifest")
load("@pip_compile_deps//:requirements.bzl", "all_whl_requirements")

# gazelle:python_manifest_file_name gazelle.yaml

modules_mapping(
    name = "modules_map",
    wheels = all_whl_requirements,
)

gazelle_python_manifest(
    name = "gazelle_python_manifest",
    manifest = ":gazelle.yaml",
    modules_mapping = ":modules_map",
    pip_repository_incremental = True,
    pip_repository_name = "pip_compile_deps",
    requirements = ":requirements.txt",
)

py_library(
    name = "pip_compile",
    srcs = ["pip_compile.py"],
    imports = ["."],
    visibility = ["//:__subpackages__"],
    deps = ["@pip_compile_deps_pip_tools//:pkg"],
)

py_binary(
    name = "bin",
    srcs = ["pip_compile.py"],
    main = "pip_compile.py",
    visibility = ["//:__pkg__"],
    deps = [":pip_compile"],
)
