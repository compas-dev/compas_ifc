from typing import Dict
from typing import Union

# from typing import Optional

import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.pset


class Entity:
    """
    Class representing a general IFC entity. Each entity corresponds to a line in IFC file.

    Parameters
    ----------
    entity : :class:`ifcopenshell.entity_instance`
    model : :class:`compas_ifc.model.Model`

    Attributes
    ----------
    ifc_type : str
        The IFC type of the entity.
    declaration : :class:`ifcopenshell.ifcopenshell_wrapper.schema.declaration`
        The IFC declaration of the entity.
    model : :class:`compas_ifc.model.Model`
        The model the entity belongs to.
    attributes : Dict[str, Union[str, float, int, list, tuple]]
        All the attributes of the entity.
    psets : Dict[str, Dict[str, Union[str, float, int, list, tuple]]]
        All the property sets of the entity.
    properties : Dict[str, Union[str, float, int, list, tuple]]
        All the properties of all property sets compiled into a single dict.

    """

    def __init__(self, entity: ifcopenshell.entity_instance, model):
        self._entity = entity
        self._model = model
        self._declaration = None
        self._psets = {}
        self._attributes = {}
        self._properties = {}
        self._ifc_type = None

    def __repr__(self):
        return "<{}:{}>".format(type(self).__name__, self.ifc_type)

    @property
    def declaration(self):
        if not self._declaration and self.model.schema:
            self._declaration = self.model.schema.declaration_by_name(self.ifc_type)
        return self._declaration

    @property
    def ifc_type(self):
        if not self._ifc_type and self._entity:
            self._ifc_type = self._entity.is_a()
        else:
            self._ifc_type = "Ifc" + type(self).__name__
        return self._ifc_type

    def is_a(self, ifc_type: str = None):
        # TODO: this is a bit mess, need to clean up
        if not ifc_type:
            return self.ifc_type
        if not self._entity:
            return ifc_type == self.ifc_type  # TODO: consider inheritance
        return self._entity.is_a(ifc_type)

    def __getitem__(self, key: str):
        return self.attribute(key)

    def __setitem__(self, key: str, value):
        self.set_attribute(key, value)

    def _collect_attributes(self):
        if not self._entity:
            return {attr.name(): None for attr in self.declaration.all_attributes()}

        attributes = self._entity.get_info(
            recursive=False,
            include_identifier=False,
        )
        del attributes["type"]
        return attributes

    def _collect_properties(self):
        properties = {}
        for pset in self.psets.values():
            for name in pset:
                properties[name] = pset[name]
        return properties

    def _collect_psets(self):
        psets = {}
        if not self._entity:
            return psets
        _psets = ifcopenshell.util.element.get_psets(self._entity)
        for name in _psets:
            psets[name] = _psets[name]
        return psets

    @property
    def model(self):
        return self._model

    @property
    def attributes(self) -> Dict:
        if not self._attributes:
            self._attributes = self._collect_attributes()

        # TODO: this is a bit of a hack, need to clean up
        for key, value in self._attributes.items():
            if isinstance(value, ifcopenshell.entity_instance):
                self._attributes[key] = self.model.reader.get_entity(value)
            elif isinstance(value, tuple) and value and isinstance(list(value)[0], ifcopenshell.entity_instance):
                self._attributes[key] = [self.model.reader.get_entity(v) for v in value]
        return self._attributes

    @property
    def psets(self) -> Dict:
        if not self._psets:
            self._psets = self._collect_psets()
        return self._psets

    @property
    def properties(self) -> Dict:
        if not self._properties:
            self._properties = self._collect_properties()
        return self._properties

    def has_attribute(self, name: str) -> bool:
        """
        Verify that the entity has a specific attributes.

        Returns
        -------
        bool

        """
        return name in self.attributes

    def attribute(self, name: str) -> Union[str, int, float]:
        """
        Get the value of a named attribute.

        Parameters
        ----------
        name : str
            The name of the attribute.

        Returns
        -------
        str | int | float
            The value of the attribute.

        """
        return self.attributes.get(name)

    def set_attribute(self, name: str, value: Union[str, int, float]) -> None:
        """
        Set the value of a named attribute.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : str | int | float
            The value of the attribute.

        Returns
        -------
        None

        """
        self.attributes[name] = value

    def set_attributes(self, attributes: Dict[str, Union[str, int, float]]) -> None:
        """
        Set the values of multiple attributes.

        Parameters
        ----------
        attributes : Dict[str, Union[str, int, float]]
            The attributes to set.

        Returns
        -------
        None

        """
        for name, value in attributes.items():
            self.set_attribute(name, value)

    def pset(self, name: str) -> Dict:
        """
        Get the property set with the given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        Dict

        """
        return self._psets[name]

    def has_property(self, name: str) -> bool:
        """
        Verify that this entity has a specific property.

        Parameters
        ----------
        name : str

        Returns
        -------
        bool

        """
        return name in self.properties

    def property(self, name: str) -> Union[str, int, float]:
        """
        Get the value of the property with the given name.

        Parameters
        ----------
        name : str

        Returns
        -------
        str | int | float

        """
        return self.properties.get(name)

    def set_property(self, name: str, value: Union[str, int, float]) -> None:
        """
        Set the value of the property with a given name.

        Parameters
        ----------
        name : str
            The name of the property.
        value : str | int | float
            The value of the property.

        Returns
        -------
        None

        """
        self.properties[name] = value

    def inheritance(self):
        """
        Find the ancestors of the current entity up to the root element.

        Returns
        -------
        List[str]

        """
        declaration = self.declaration
        inheritance = [declaration.name()]
        while declaration.supertype():
            inheritance.append(declaration.supertype().name())
            declaration = declaration.supertype()
        return inheritance[::-1]

    def print_inheritance(self) -> None:
        """
        Print the entity inheritance as a nested list.

        Returns
        -------
        None

        """
        for index, item in enumerate(self.inheritance()):
            print("-" * (index + 1) + f" {item}")

    def traverse_branch(self):
        yield self
