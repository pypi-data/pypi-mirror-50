__all__ = [
    # general purpose
    'is_windows',
    # python and anaconda
    'get_conda_env_path',
    'get_python_script_path',
    # docker
    'get_docker_mount_path_builder',
    'is_docker_toolbox',
    ]

import fabric
import invoke
import io
import json
import os
import pathlib
import typing


# General helpers


def is_windows(conn: fabric.Connection = None) -> bool:
    """Check if local or remote OS is Windows; for remote OS, it is required to have python on path."""
    if conn is None or type(conn) == invoke.Context:
        # no remote connection, executed locally
        return os.name == 'nt'
    else:
        # for remote connection, we need python on path
        stream = io.StringIO()
        conn.run('python -c "import os; print(os.name == \'nt\')"', replace_env=False, out_stream=stream)
        return stream.getvalue().strip() == 'True'


# Python and Anaconda helpers


def get_conda_env_path(conn: fabric.Connection, envname: str = 'base') -> pathlib.Path:
    """Get path of specific Anaconda environment."""
    stream = io.StringIO()
    conn.run('conda info --envs --json', replace_env=False, out_stream=stream)
    info = json.loads(stream.getvalue())
    return next(iter(p for p in (pathlib.Path(s) for s in info['envs']) if p.name == envname))


def get_python_script_path(conn: fabric.Connection, envdir: pathlib.Path, scriptname: str = 'python') -> pathlib.Path:
    """Get path to specific script from Python/Anaconda environment."""
    if not is_windows(conn):
        path =  envdir / 'bin' / scriptname
    else:
        if scriptname in ('python', 'pythonw'):
            path = envdir / f'{scriptname}.exe'
        else:
            path = envdir / 'Scripts' / f'{scriptname}.exe'
    return path


#  Docker helpers


def get_docker_mount_path_builder(conn: fabric.Connection) -> typing.Callable[[pathlib.Path], str]:
    """Get docker mount path builder function."""

    def docker_desktop(path: pathlib.Path) -> str:
        return str(path.resolve())

    def docker_toolbox(path: pathlib.Path) -> str:
        p = path.resolve()
        mountpath = f'/{p.drive.lower().replace(":", "")}/{pathlib.Path(*p.parts[1:]).as_posix()}'
        if not mountpath.startswith('/c/Users/'):
            raise ValueError('Only files under C:/Users/ can be shared automatically with Docker Toolbox.')
        return mountpath

    return docker_toolbox if is_docker_toolbox(conn) else docker_desktop


def is_docker_toolbox(conn: fabric.Connection) -> bool:
    """Check if docker uses Docker Toolbox."""
    stream = io.StringIO()
    conn.run('docker system info', replace_env=False, out_stream=stream)
    info = stream.getvalue()
    return info.find('Operating System: Boot2Docker') >= 0
