load("@rules_python//python:defs.bzl", "py_binary")
load("@pip_compile_deps//:requirements.bzl", "requirement")



py_binary(
    name = "bin",
    srcs = ["pip_compile.py"],
    main = "pip_compile.py",
    deps = [requirement("pip-tools")],
    visibility = ["//:__pkg__"],
)
