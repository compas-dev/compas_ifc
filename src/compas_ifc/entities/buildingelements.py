from compas_model.models import Model
from compas_model.elements import Element



class BuildingModel(Model):
    # This class will maintain and update a IFC file underneath.

    def __init__(self, **kwargs):

        # The model will start an empty IFC file if not provided.
        super().__init__(**kwargs)
        self._ifc_project = None # The underlying IFC project (we don't treat it as element here)
        # How about site? Maybe also integrate it here.

    @classmethod
    def from_ifc(self, ifc_file):
        pass

    @classmethod
    def from_template(self, building_count=1, storey_count=1):
        # Do we support multiple sites?
        pass

    @classmethod
    def from_blockmodel(self, blockmodel, mapping=None):
        # Create a building model from a blockmodel.
        # mapping is a dictionary that maps the blockmodel elements to IFC elements.
        # TODO: think about the role of different models.
        pass

    # To ...

    def add(self, **kwargs):
        super().add(**kwargs)
        # also update the IFC file
        pass

    def remove(self, **kwargs):
        super().remove(**kwargs)
        # also update the IFC file
        pass


class BuildingElement(Element):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._ifc_entity = None # Read-only, underlying IFC entity.
        self._ifc_class = None # Read-only, IFC class name, maybe redundant.
        # There are 30 IfcBuiling(/t)Elements, but they only add one or two more attributes and all of them OPTIONAL.
        # The value of adding these classes are questionable. 
        # The definition of these classes can be sometimes conflited between fields, for example Beams in architecrual and structrual context. 
        # At least in IFC cases, these classification are perhaps better expressed as "Labels" instead of branched-out classes.



        self.ifc_attributes = {} # View object, mimics dict but will update the underlying IFC entity when changed, it also validates againts the IFC schema.
        self.ifc_property_sets = {} # View object, the parametric definition will be added here too.
        # Should we abstract away these two, and have them managed together by a single JSON schema?
        # The artificial division between attributes and property sets is also a reason of "rogue customizetion". It also confuse with Python's interperation of these two words.
        # The combined name being?

        # Common attributes of all building elements.
        self._name = None
        self._description = None

        self.geometry = None
        # Option1: "Baked geometry", Brep (Tessellated or Full).
        # Option2a: "Parametric geometry", this class inherrits from another like `Beam`, this might branching out to too many classes.
        # Option2b: "Parametric geometry", this refers to a class like `Beam` as attribute, this makes the class structure convoluted.

        # The question becomes: 
        # 1.should the concept of "geometry" be detached from "Element"? which is the case of IFC.
        # 2.Data flow-wise, the data should always flow from Model to IFC, we will not likely modify geometry if IFC elements, but what happens when we read it back?
        # 3.How do we convert baked geometry back to a parametric definition? (we save the parametric definition in PSet)
        # 4.If we want to make update, do we convert the whole model back to a parametric (Block) model, or should we update the BuildingModel in-place?

        # Prefered: single class with consistant APIs that handles mapping to/from IFC classes.

        self.material = None # There needs to be some mapping mechanism between the material class and Qtos in IFC.

        # How about storeys? Maybe as a calculated property of the building elements?


        # links to parents
        self.storey = None
        self.building = None
        self.model = None


    @classmethod
    def from_ifc(cls, ifc_entity):
        # From a raw IFC entity fill-in all the attributes and setup the links etc.
        pass

    @classmethod
    def from_blockelement(cls, blockelement, mapping=None):
        # Create a building element from a blockelement.
        # mapping is a dictionary that maps the blockelement elements to IFC elements.
        pass

    def add(self, **kwargs):
        super().add(**kwargs)
        # also update the IFC file
        pass

    def remove(self, **kwargs):
        super().remove(**kwargs)
        # also update the IFC file
        pass

    @property
    def transformation(self):
        # Get the transformation matrix of the element
        pass

    @transformation.setter
    def transformation(self, transformation):
        # Set the transformation matrix of the element, will also update the placement of the underlying IFC entity.
        pass



# Use pydantic class for auto-generated IFC classes?? How does it deal with pointers in seriliasition?

# TODO: Transparent way to work with grid and storeys etc.