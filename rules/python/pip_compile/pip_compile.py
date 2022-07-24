"Set defaults for the pip-compile command to run it under Bazel"

import argparse
import glob
import os
import os.path
import sys

from piptools.scripts.compile import cli


def _get_repos(dir: str):
    root = os.path.join(dir, "external", "pypi")
    groups = []
    for filename in os.listdir(root):
        if os.path.isdir(os.path.join(root, filename)):
            groups.append(filename)
    return groups


def main() -> None:
    if "BUILD_WORKSPACE_DIRECTORY" not in os.environ:
        print(
            "$BUILD_WORKSPACE_DIRECTORY enviroment variable is not set. Please run this tool using `bzl run`",
            file=sys.stderr,
        )
        sys.exit(1)

    workspace_path: str = os.environ["BUILD_WORKSPACE_DIRECTORY"]

    parser = argparse.ArgumentParser(
        description="Compiles one of our standard requirements files"
    )
    parser.add_argument(
        "-g",
        "--group",
        nargs="*",
        help="the requirement files to compile",
        default=_get_repos(workspace_path),
        choices=_get_repos(workspace_path),
    )

    args = parser.parse_args(sys.argv[1:])

    print(f"Compiling {', '.join(args.group)} ...")
    for group in args.group:
        root = os.path.join(workspace_path, "external", "pypi", group)
        input_files = [
            os.path.relpath(p, root) for p in glob.glob(os.path.join(root, "*.in"))
        ]
        output_file = os.path.join(root, "requirements.txt")
        os.chdir(root)
        sys.argv[1:] = [
            "--no-header",
            "--generate-hashes",
            "--allow-unsafe",
            "--output-file",
            output_file,
        ] + input_files
        cli()


if __name__ == "__main__":
    main()
