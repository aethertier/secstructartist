import os, io
import json
import yaml
from pathlib import Path
from typing import Union
from ..constants import SSA_CONFIGURATION_PRESETS
from ..typing_ import ArtistKW, PathOrFile, FileFormat

def infer_file_format(fname: str, fmt: FileFormat='auto'):
    """
    Infer configuration file format from filename or explicit format.

    Parameters
    ----------
    fname : str
        File name or path.
    fmt : {'auto', 'json', 'yaml'}, optional
        File format. If 'auto', inferred from file extension.

    Returns
    -------
    str
        Inferred file format.

    Raises
    ------
    ValueError
        If the file format is unsupported.
    """
    if fmt == 'auto':
        _, ext = os.path.splitext(fname)
        fmt = ext.lstrip('.').lower()

    if fmt in ['json', 'yaml']:
        return fmt
    
    raise ValueError(f"Unknown configuration file format: '{fmt}'")

def load_configuration(config_: Union[ArtistKW, PathOrFile], format_: FileFormat='auto'):
    """
    Load a configuration from a path, file-like object, or named preset.

    Parameters
    ----------
    config_ : str, path-like, file-like, or ArtistConfig
        Configuration source or named configuration key.
    format_ : {'auto', 'json', 'yaml'}, optional
        File format. If 'auto', inferred from filename.

    Returns
    -------
    dict
        Parsed configuration data.

    Raises
    ------
    TypeError
        If input type is unsupported.
    RuntimeError
        If format inference is impossible.
    """
    _loaders = {
        'json': json.load,
        'yaml': yaml.safe_load
    }

    # Resolve named configurations
    if isinstance(config_, str) and config_ in SSA_CONFIGURATION_PRESETS:
        config_ = SSA_CONFIGURATION_PRESETS[config_]

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
    """
    Write configuration data to a file or file-like object.

    Parameters
    ----------
    data : any
        Data to serialize.
    file_ : str, path-like, or file-like
        Output target.
    format_ : {'auto', 'json', 'yaml'}, optional
        File format. If 'auto', inferred from filename.
    **kwargs
        Passed to the underlying dump function.

    Raises
    ------
    TypeError
        If output target type is unsupported.
    RuntimeError
        If format inference is impossible.
    """
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