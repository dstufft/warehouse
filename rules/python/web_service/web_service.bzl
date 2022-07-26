"""
"""
load("@rules_python//python:defs.bzl", "py_binary")
load("@pip//:requirements.bzl", "requirement")
load("@io_bazel_rules_docker//python3:image.bzl", "py3_image")


def _web_service_impl(ctx):
    wrapper = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.expand_template(
        output = wrapper,
        template = ctx.file._template,
        substitutions = {
            "{ENTRYPOINT}": ctx.attr.entrypoint,
        },
    )
    return [DefaultInfo(files = depset([wrapper]))]


_web_service = rule(
    implementation = _web_service_impl,
    attrs = {
        "entrypoint": attr.string(),
        "_template": attr.label(
            allow_single_file = True,
            default = "//rules/python/web_service:web_service.py.tmpl",
        ),
    },
)


def web_service(name, entrypoint, deps):
    _web_service(
        name = "%s.py" % name,
        entrypoint = entrypoint,
    )

    # py_binary(
    #     name = name,
    #     srcs = [
    #         "%s.py" % name,
    #     ],
    #     main = "%s.py" % name,
    #     deps = deps + [requirement("gunicorn")],
    # )

    py3_image(
        name = name,
        srcs = ["%s.py" % name],
        main =  "%s.py" % name,
        deps = deps + [requirement("gunicorn")],
    )
