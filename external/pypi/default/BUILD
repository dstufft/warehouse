load("@rules_python//gazelle/modules_mapping:def.bzl", "modules_mapping")
load("@rules_python//gazelle/manifest:defs.bzl", "gazelle_python_manifest")
load("@pip//:requirements.bzl", "all_whl_requirements")

modules_mapping(
    name = "modules_map",
    wheels = all_whl_requirements,
)

gazelle_python_manifest(
    name = "gazelle_python_manifest",
    manifest = ":gazelle.yaml",
    modules_mapping = ":modules_map",
    pip_repository_incremental = True,
    pip_repository_name = "pip",
    requirements = "//external/pypi/default:requirements.txt",
)
