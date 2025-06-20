"""Provides the utilities to generate the website.

Author: Elliot Simpson
"""

import importlib.resources as pkg_resources
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Literal, cast

import tomlkit
import tomlkit.items

from turbopelican._commands.init.config import InitConfiguration
from turbopelican._utils.shared.args import InstallType, Verbosity


def uv_sync(directory: Path, *, verbosity: Verbosity) -> None:
    """Sets up the repository with uv.

    Args:
        directory: The path where the repository is to be initialized.
        verbosity: Whether or not to suppress output.
    """
    uv_path = shutil.which("uv")
    if not uv_path:
        return

    uv_sync_args = [uv_path, "sync"]
    if verbosity == Verbosity.QUIET:
        uv_sync_args.append("--quiet")

    # Ensure warnings concerning virtual environments are filtered out.
    process = subprocess.Popen(
        uv_sync_args,
        stdout=sys.stdout,
        stderr=subprocess.PIPE,
        cwd=directory,
        text=True,
        bufsize=1,
    )
    while process.stderr:
        stderr_line = process.stderr.readline()
        if not stderr_line:
            break
        if "does not match the project environment path" not in stderr_line:
            print(stderr_line, file=sys.stderr, end="")

    process.wait()
    if process.returncode:
        raise subprocess.CalledProcessError(process.returncode, process.args)


def _copy_template(directory: Path, name: Literal["newsite", "minimal"]) -> None:
    """Copies all the files from a template over.

    Args:
        directory: The path where the repository is to be initialized.
        name: The name of the template to copy.
    """
    with pkg_resources.as_file(
        pkg_resources.files(__name__.split(".", 1)[0]).joinpath("_templates", name)
    ) as p:
        shutil.copytree(p, directory, dirs_exist_ok=True)


def generate_repository(args: InitConfiguration) -> None:
    """Generates the files in place for turbopelican to use.

    Args:
        args: The arguments to configure the website.
    """
    if not args.directory.parent.exists():
        raise FileNotFoundError(
            f"Cannot create repository. {args.directory.parent} does not exist.",
        )
    if args.directory.exists():
        if not args.directory.is_dir():
            raise NotADirectoryError("Cannot create repository at {args.directory}.")
        if any(args.directory.iterdir()):
            error_message = f"Non-empty target directory at {args.directory}."
            tip_message = "Use `turbopelican adorn` to modify existing repository."
            raise RuntimeError(f"{error_message}\n{tip_message}")
        args.directory.rmdir()
    _copy_template(args.directory, "newsite")
    if args.install_type == InstallType.MINIMAL_INSTALL:
        _copy_template(args.directory, "minimal")

    git_path = shutil.which("git")
    if git_path is None:
        raise OSError("git not installed")
    git_init_args = [git_path, "init"]
    if args.verbosity == Verbosity.QUIET:
        git_init_args.append("--quiet")
    subprocess.run(git_init_args, check=True, cwd=args.directory)

    git_use_main_branch = [git_path, "branch", "-m", "main"]
    subprocess.run(git_use_main_branch, check=True, cwd=args.directory)


def update_pyproject(directory: Path) -> None:
    """Updates pyproject.toml to use the provided information.

    Args:
        directory: The path to the directory to be modified.
    """
    pyproject_conf = Path(directory) / "pyproject.toml"

    with pyproject_conf.open(encoding="utf8") as configuration:
        toml = tomlkit.load(configuration)

    rawname = "".join(
        char for char in directory.name if char.isalpha() or char.isdigit()
    )
    project = cast("tomlkit.items.Table", toml["project"])
    project["name"] = rawname

    with pyproject_conf.open("w", encoding="utf8") as configuration:
        tomlkit.dump(toml, configuration)


def commit_changes(args: InitConfiguration) -> None:
    """Stages and commits the new files.

    Args:
        args: The arguments to configure the website.
    """
    if not args.commit_changes:
        return

    git_path = shutil.which("git")
    if git_path is None:
        raise OSError("git not installed")

    git_add_args = [git_path, "add", "."]
    subprocess.run(git_add_args, check=True, cwd=args.directory)

    try:
        email = subprocess.run(
            [git_path, "config", "user.email"],
            check=True,
            cwd=args.directory,
            capture_output=True,
        )
        username = subprocess.run(
            [git_path, "config", "user.name"],
            check=True,
            cwd=args.directory,
            capture_output=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "git not configured with `user.email` and `user.name`."
        ) from exc

    if not email.stdout.strip() or not username.stdout.strip():
        raise RuntimeError("git not configured with `user.email` and `user.name`.")

    git_commit_args = [git_path, "commit", "--no-edit", "-m", "Initial commit."]
    if args.verbosity == Verbosity.QUIET:
        git_commit_args.append("--quiet")
    subprocess.run(git_commit_args, check=True, cwd=args.directory)


def _create_remote_repo(args: InitConfiguration, gh_path: str) -> None:
    """Creates the remote repository.

    Args:
        args: The arguments to configure the website.
        gh_path: The string path to the GitHub executable.
    """
    repo_name = args.site_url.removeprefix("https://")
    gh_repo_create_args = [
        gh_path,
        "repo",
        "create",
        repo_name,
        "--public",
        "--source",
        ".",
        "--remote",
        "origin",
    ]
    capture_output = args.verbosity == Verbosity.QUIET
    try:
        subprocess.run(
            gh_repo_create_args,
            cwd=args.directory,
            check=True,
            capture_output=capture_output,
        )
    except subprocess.CalledProcessError as exc:
        if capture_output:
            sys.stderr.write(exc.stderr.decode())
        raise


def _configure_remote_deployment(args: InitConfiguration, gh_path: str) -> None:
    """Configures the remote repository to deploy from GitHub Actions.

    Args:
        args: The arguments to configure the website.
        gh_path: The string path to the GitHub executable.
    """
    repo_name = args.site_url.removeprefix("https://")
    owner = repo_name.removesuffix(".github.io")
    subprocess.check_call(
        [
            gh_path,
            "api",
            "--method",
            "POST",
            "-H",
            "Accept: application/vnd.github+json",
            "-H",
            "X-GitHub-Api-Version: 2022-11-28",
            f"/repos/{owner}/{repo_name}/pages",
            "-f",
            "build_type=workflow",
        ],
        stdout=subprocess.DEVNULL,
        cwd=args.directory,
    )


def _push_code_to_remote(args: InitConfiguration, git_path: str) -> None:
    """Pushes the code in the local repository to GitHub.

    Args:
        args: The arguments to configure the website.
        git_path: The string path to the Git executable.
    """
    git_push_args = [git_path, "push", "--set-upstream", "origin", "main"]
    if args.verbosity == Verbosity.QUIET:
        git_push_args.append("--quiet")
    subprocess.check_call(git_push_args, cwd=args.directory)


def run_gh_cli(args: InitConfiguration) -> None:
    """Runs any required GitHub CLI commands to create the remote repository.

    Args:
        args: The arguments to configure the website.
    """
    if not args.use_gh_cli:
        return

    gh_path = shutil.which("gh")
    if gh_path is None:
        raise RuntimeError("gh not installed")

    git_path = shutil.which("git")
    if git_path is None:
        raise OSError("git not installed")

    _create_remote_repo(args, gh_path)
    _configure_remote_deployment(args, gh_path)
    _push_code_to_remote(args, git_path)


def report_completion(args: InitConfiguration) -> None:
    """Reports that Turbopelican has finished initializing the repository.

    Args:
        args: The arguments to configure the website.
    """
    if args.verbosity == Verbosity.NORMAL:
        print("⚡ Turbopelican initialized! ⚡")
