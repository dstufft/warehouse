load("@rules_python//python:defs.bzl", "py_library")
load("//rules/python/web_service:web_service.bzl", "web_service")

web_service(
    name = "serve",
    entrypoint = "demo.app:app",
    deps = [":demo"],
)

py_library(
    name = "demo",
    srcs = [
        "src/demo/__init__.py",
        "src/demo/app.py",
    ],
    imports = ["src"],
    visibility = ["//:__subpackages__"],
    deps = [
        "@pip_pyramid//:pkg",
        "@pip_requests//:pkg",
    ],
)
