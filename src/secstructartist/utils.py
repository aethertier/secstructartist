import os, io
import json
import yaml
from pathlib import Path
from typing import Generator, Iterable, Tuple
from .constants import SSA_CONFIGURATIONS
from .typing_ import ArtistConfig, PathOrFile, FileFormat

def aggregate(x: Iterable[str], /) -> Generator[Tuple[str, int], None, None]:
    """
    Aggregate consecutive identical elements and count their occurrences.
    It yields tuples containing each distinct element and the number of times 
    it appears consecutively in the input.

    Parameters
    ----------
    x : Iterable[str]
        An iterable of strings. Consecutive identical elements are grouped
        together and counted.

    Yields
    ------
    tuple of (str, int)
        A tuple containing the element value and the count of its consecutive
        occurrences.
    """
    xiter = iter(x)
    try:
        xval, xcnt = next(xiter), 1
    except StopIteration:
        return
    for xi in xiter:
        if xi == xval:
            xcnt += 1
        else:
            yield xval, xcnt
            xval, xcnt = xi, 1
    yield xval, xcnt

def infer_file_format(fname: str, fmt: FileFormat='auto'):
    """Infers the format of a configuration file"""
    if fmt == 'auto':
        _, ext = os.path.splitext(fname)
        fmt = ext.lstrip('.').lower()

    if fmt in ['json', 'yaml']:
        return fmt
    
    raise ValueError(f"Unkown configuration file format: '{fmt}'")

def load_configuration(config_: ArtistConfig, format_: FileFormat='auto'):
    """Loads a configuration file"""

    _loaders = {
        'json': json.load,
        'yaml': yaml.safe_load
    }

    # Resolve named configurations
    if isinstance(config_, str) and config_ in SSA_CONFIGURATIONS:
        config_ = SSA_CONFIGURATIONS[config_]

    # Path-like input
    if isinstance(config_, (str, os.PathLike)):
        path = Path(config_)
        fmt = infer_file_format(path.name, format_)
        with path.open("r") as fh:
            return _loaders[fmt](fh)
    
    # File handle input
    if isinstance(config_, io.IOBase):
        if format_ == 'auto' and not hasattr(config_, 'name'):
            raise RuntimeError(
                "format='auto' requires a file path or a file object with a .name attribute"
            )
        fmt = infer_file_format(config_.name, format_)
        return _loaders[fmt](config_)
    
    raise TypeError(
         "config must be a path, file-like object, or named configuration key"
    )

def write_configuration(
    data,
    file_: PathOrFile, 
    format_: FileFormat = 'auto',
    **kwargs
):
    _dumpers = {
        'json': json.dump,
        'yaml': yaml.safe_dump
    }
    # Path-like input
    if isinstance(file_, (str, os.PathLike)):
        path = Path(file_)
        fmt = infer_file_format(path.name, format_)
        with path.open("w") as fh:
            return _dumpers[fmt](data, fh, **kwargs)
    
    # File handle input
    elif isinstance(file_, io.IOBase):
        if format_ == 'auto' and not hasattr(file_, 'name'):
            raise RuntimeError(
                "format='auto' requires a file path or a file object with a .name attribute"
            )
        fmt = infer_file_format(file_.name, format_)
        return _dumpers[fmt](data, file_, **kwargs)
    
    else:
        raise TypeError(
            "file_ must be a path or file-like object"
        )