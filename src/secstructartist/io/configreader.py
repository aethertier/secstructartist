from typing import Any, Dict
from ..elementartist import ElementArtist
from ..secstructartist import SecStructArtist
from ..primitives import PrimitiveArtist, PRIMITIVES_AVAIL
from ..typing_ import ArtistConfig, FileFormat
from ..utils import load_configuration


class SSAConfigReader:

    def __init__(self, config_: ArtistConfig, format_: FileFormat='auto'):
        self._config : Dict[str, Dict[str, Any]] = None
        self._secstructartist : SecStructArtist = None
        self._elements : Dict[str, ElementArtist] = None
        self._primitives : Dict[str, PrimitiveArtist] = None
        self._drawstyle : Dict[str, float] = None
        self._load_configuration(config_, format_)
        
    @property
    def config(self) -> Dict[str, Dict[str, Any]]:
        if self._config is None:
            raise RuntimeError(
                'Configuration is not set. Start by loading a configuration '
                'using the ``load_json`` or ``load_yaml`` methods.'
            )
        return self._config

    def get_secstructartist(self) -> SecStructArtist:
        """Returns the SecStructArtist parsed from a loaded config file"""
        if self._secstructartist is None:
            elements = self.get_elementartists()
            drawstyle = self.get_drawstyle()
            self._secstructartist = SecStructArtist(elements, **drawstyle)
        return self._secstructartist

    def get_elementartists(self) -> Dict[str, ElementArtist]:
        """Returns the ElementArtists parsed from a loaded config file"""
        if self._elements is None:
            primitives = self.get_primitiveartists()
            elements = {}
            for elem_key, elem_dict in self.config['elements'].items():
                elements[elem_key] = ElementArtist(
                    primitives=[primitives[pkey] for pkey in elem_dict['primitives']],
                    label=elem_dict['label']
                )
            self._elements = elements
        return self._elements

    def get_primitiveartists(self) -> Dict[str, PrimitiveArtist]:
        """Returns the PrimitiveArtists parsed from a loaded config file"""
        if self._primitives is None:
            primitives = {}
            for pkey, pkwargs in self.config['primitives'].items():
                pkwargs = dict(pkwargs)
                ptype = pkwargs.pop('type')
                ptype = PRIMITIVES_AVAIL[ptype]
                primitives[pkey] = ptype(**pkwargs)
            self._primitives = primitives
        return self._primitives

    def get_drawstyle(self):
        """Returns the DrawStyle parsed from a loaded config file"""
        if self._drawstyle is None:
            self._drawstyle = dict(self.config['drawstyle'])
        return self._drawstyle

    def _load_configuration(self, config_: ArtistConfig, format_: FileFormat='auto'):
        """Loads a configuration file"""
        self._config = load_configuration(config_, format_)