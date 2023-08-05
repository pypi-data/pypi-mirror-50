
import numpy as np
import uuid
import itertools

from PySimultan.base_classes import ObjectBaseClass
# from face import Face as NewFace
# from face import Face


class Part(ObjectBaseClass):

    new_part_id = itertools.count(0)

    def __init__(self,
                 name=None,
                 layers=None,
                 part_id=uuid.uuid4(),
                 color=np.append(np.random.rand(1, 3), 0)*255,
                 color_from_parent=False,
                 is_visible=True,
                 openable=False
                 ):

        super().__init__(id=part_id,
                         pid=next(type(self).new_part_id),
                         color=color,
                         name=name,
                         color_from_parent=color_from_parent,
                         is_visible=is_visible
                         )

        if name is None:
            self._Name = 'Part{}'.format(self.PID)
        else:
            self._Name = name

        if layers is None:
            self._Layers = [MatLayer()]
        else:
            if isinstance(layers, list):
                self._Layers = layers
            else:
                self._Layers = [layers]

        # ------------------------------------------------------
        # Physical Properties
        # ------------------------------------------------------

        self._U_Value = None
        self._G_Value = None
        self._ThermalResistance = None
        self._Openable = openable

        # -----------------------------------------------
        # bindings
        # -----------------------------------------------

        for layer in self._Layers:
            layer.bind_to(self._layer_updated)

    # --------------------------------------------------------
    # Attributes
    # --------------------------------------------------------

    @property
    def Layers(self):
        return self._Layers

    @Layers.setter
    def Layers(self, value):
        self._default_set_handling('Layers', value)

    @property
    def Openable(self):
        return self._Openable

    @Openable.setter
    def Openable(self, value):
        self._default_set_handling('Openable', value)


    @property
    def ThermalResistance(self):
        if self._ThermalResistance is None:
            self.calc_thermal_resistance()
        return self._ThermalResistance

    @ThermalResistance.setter
    def ThermalResistance(self, value):
        self._default_set_handling('ThermalResistance', value)

    @property
    def U_Value(self):
        if self._U_Value is None:
            self.calc_u_value()
        return self._U_Value

    @U_Value.setter
    def U_Value(self, value):
        self._default_set_handling('U_Value', value)

    @property
    def G_Value(self):
        if self._G_Value is None:
            self.calc_g_value()
        return self._G_Value

    @G_Value.setter
    def G_Value(self, value):
        self._default_set_handling('G_Value', value)

    # --------------------------------------------------------
    # update functions
    # --------------------------------------------------------

    def _layer_updated(self):
        self.print_status('updating part: Layers updated')
        self.calc_thermal_resistance()
        self.calc_u_value()

    def calc_thermal_resistance(self):
        self._ThermalResistance = sum([x.ThermalResistance for x in self.Layers])

    def calc_u_value(self, Rsi=0.13, Rse=0.04):
        self._U_Value = 1/(self.ThermalResistance + Rsi + Rse)


class Window(Part):
    def __init__(self,
                 face,
                 name=None,
                 part_id=uuid.uuid4(),
                 color=np.append(np.random.rand(1, 3), 0)*255,
                 color_from_parent=False,
                 is_visible=True,
                 openable=False,
                 u_g=0,
                 u_f=1,
                 psi=0.05,
                 frame_width=0.05,
                 eps=2.5,
                 tau=0.1,
                 rho=0.5,
                 alpha=0.4,
                 number_of_glazings=2,
                 glazing_thickness=0.01
                 ):

        # The hole window is modeled as a face with averaged material data.
        # The window is modeled as one material layer with a thickness of 1 cm of Material 'Glass'
        # The physical properties of the Material are adapted, so that the window can be modeled as homogeneous material
        # To achieve this the thermal conductivity is adapted

        super().__init__(name=name,
                         layers=None,
                         part_id=part_id,
                         color=color,
                         color_from_parent=color_from_parent,
                         is_visible=is_visible,
                         openable=openable)

        self._OriginalFace = face
        self._GlassFace = None
        self._FrameFace = None
        self._U_g = u_g
        self._U_f = u_f
        self._Psi = psi
        self._Eps = eps
        self._Tau = tau
        self._Rho = rho
        self._Alpha = alpha
        self._FrameWidth = frame_width
        self._NumberOfGlazings = number_of_glazings
        self._GlazingThickness = glazing_thickness
        self._FramePart = None
        self._GlassPart = None
        self._G_Value = None
        self._FrameWidth = frame_width
        self._NumberOfGlazings = number_of_glazings
        self._GlazingThickness = glazing_thickness

        self._WindowPart = None
        self._WindowLayers = None
        self._WindowMaterials = None

        self._FrameLayers = None
        self._FrameMaterials = None

        self._GlassLayers = None
        self._GlassMaterials = None

        self.create_window_part()

        self.Layers = self._WindowLayers

    @Part.G_Value.getter
    def G_Value(self):
        if self._G_Value is None:
            self.calc_g_value()
        return self._G_Value

    @property
    def U_Value(self, a_g, a_f, l_g):
        return self.calc_u_value(a_g=a_g, a_f=a_f, l_g=l_g)

    @property
    def U_g(self):
        return self._U_g

    @U_g.setter
    def U_g(self, value):
        if (value > 1) or (value < 0):
            raise ValueError('U_g value can not be grater than 1 or less than 0')
        self._default_set_handling('U_g', value)

    @property
    def U_f(self):
        return self._U_f

    @U_f.setter
    def U_f(self, value):
        if (value > 1) or (value < 0):
            raise ValueError('U_f value can not be grater than 1 or less than 0')
        self._default_set_handling('U_f', value)

    @property
    def Psi(self):
        return self._Psi

    @Psi.setter
    def Psi(self, value):
        if (value > 1) or (value < 0):
            raise ValueError('Psi value can not be grater than 1 or less than 0')
        self._default_set_handling('Psi', value)

    @property
    def FrameWidth(self):
        return self._FrameWidth

    @FrameWidth.setter
    def FrameWidth(self, value):
        self._default_set_handling('FrameWidth', value)

    @property
    def FramePart(self, a_f=1,
                        l_g=1,
                        thermal_conductivity=0.19,
                        density=1380,
                        heat_capacity=840,
                        solar_absorption_coefficient=0.5):
        if self._FramePart is None:
            self.create_frame_part(a_f=a_f,
                                   l_g=l_g,
                                   thermal_conductivity=thermal_conductivity,
                                   density=density,
                                   heat_capacity=heat_capacity,
                                   solar_absorption_coefficient=solar_absorption_coefficient)
        return self._FramePart

    @FramePart.setter
    def FramePart(self, value):
        self._default_set_handling('FramePart', value)

    @property
    def GlassPart(self,
                  thermal_conductivity=0.96,
                  density=2500,
                  heat_capacity=840,
                  solar_absorption_coefficient=0.1):

        if self._GlassPart is None:
            self.create_glass_part(thermal_conductivity=thermal_conductivity,
                                   density=density,
                                   heat_capacity=heat_capacity,
                                   solar_absorption_coefficient=solar_absorption_coefficient)
        return self._GlassPart

    @GlassPart.setter
    def GlassPart(self, value):
        self._default_set_handling('GlassPart', value)

    @property
    def OriginalFace(self):
        return self._OriginalFace

    @OriginalFace.setter
    def OriginalFace(self, value):
        self._default_set_handling('OriginalFace', value)

    @property
    def GlassFace(self):
        if self._GlassFace is None:
            self.create_glass_face()
        return self._GlassFace

    @GlassFace.setter
    def GlassFace(self, value):
        self._default_set_handling('GlassFace', value)

    @property
    def FrameFace(self):
        if self._FrameFace is None:
            self.create_frame_face()
        return self._GlassFace

    @FrameFace.setter
    def FrameFace(self, value):
        self._default_set_handling('FrameFace', value)

    def calc_u_value(self, a_g=1, a_f=1, l_g=1):
        """
        calculate the u-value of the window
        :param a_g: area of the glass [m²]
        :param a_f: area of the frame [m²]
        :param l_g: circumference of the face [m]
        :return: u-value of the window [W/m²K]
        """
        u_value = (a_g * self.U_g + a_f * self.U_f + l_g * self.Psi) / (a_g + a_f)
        return u_value

    def create_frame_part(self,
                          a_f=1,
                          l_g=1,
                          thermal_conductivity=0.19,
                          density=1380,
                          heat_capacity=840,
                          solar_absorption_coefficient=0.5):

        thermal_resistance_frame = 1 / ((1 / ((self.U_f + l_g * self.Psi) / a_f)) - 0.14)

        frame_material = Material(name='FrameMaterial_{}'.format(self.Name),
                                  density=density,
                                  heat_capacity=heat_capacity,
                                  thermal_conductivity=thermal_conductivity,
                                  transparent=False,
                                  solar_absorption_coefficient=solar_absorption_coefficient,
                                  g_value=0,
                                  wvdrf=20,
                                  w20=0,
                                  w80=0)

        frame_layer = MatLayer(material=frame_material, thickness=thermal_resistance_frame * thermal_conductivity)
        self._FramePart = Part(name='FramePart_{}'.format(self.Name),
                               layers=frame_layer)

        self._FrameLayers = frame_layer
        self._FrameMaterials = frame_material

        # return frame_material, frame_layer, self._FramePart

    def create_window_part(self,
                           thermal_conductivity=0.96,
                           density=2500,
                           heat_capacity=840,
                           solar_absorption_coefficient=0.1
                           ):
        mean_u_value = self.calc_u_value(a_g=self.GlassFace.Area, a_f=self.FrameFace.Area, l_g=self.FrameFace.Circumference)
        mean_g_value = self.G_Value
        thermal_resistance_window = 1 / ((1 / mean_u_value) - 0.14)

        materials = list()

        window_glazing_material = Material(name='WindowGlazingMaterial1_{}'.format(self.Name),
                                           density=density,
                                           heat_capacity=heat_capacity,
                                           thermal_conductivity=thermal_conductivity,
                                           transparent=True,
                                           solar_absorption_coefficient=solar_absorption_coefficient,
                                           g_value=(mean_g_value / self._NumberOfGlazings),
                                           wvdrf=999999,
                                           w20=0,
                                           w80=0)
        materials.append(window_glazing_material)

        window_air_material = Material(name='WindowMaterialAir_{}'.format(self.Name),
                                       density=1.4,
                                       heat_capacity=1.0,
                                       thermal_conductivity=0.026,
                                       transparent=True,
                                       solar_absorption_coefficient=0,
                                       g_value=1,
                                       wvdrf=1,
                                       w20=0,
                                       w80=0)

        thermal_resistance_glazing = (self._NumberOfGlazings * self._GlazingThickness) / thermal_conductivity

        materials.append(window_air_material)
        window_layers = list()
        window_layers.append(MatLayer(material=window_glazing_material, thickness=self._GlazingThickness))
        for i in range(self._NumberOfGlazings - 1):
            window_layers.append(MatLayer(material=window_air_material,
                                          thickness=((thermal_resistance_window - thermal_resistance_glazing) * 0.026) / (self._NumberOfGlazings - 1)
                                          )
                                 )
            window_layers.append(MatLayer(material=window_glazing_material, thickness=self._GlazingThickness))

        window_part = Part(name='WindowPart_{}'.format(self.Name),
                           layers=window_layers)

        self._WindowPart = window_part
        self._WindowLayers = window_layers
        self._WindowMaterials = materials

        # return window_part, window_layers, materials

    def create_glass_part(self,
                          thermal_conductivity=0.96,
                          density=2500,
                          heat_capacity=840,
                          solar_absorption_coefficient=0.1
                          ):

        thermal_resistance_window = 1 / ((1 / self.U_g) - 0.14)

        glass_materials = list()

        glazing_material = Material(name='WindowGlazingMaterial1_{}'.format(self.Name),
                                    density=density,
                                    heat_capacity=heat_capacity,
                                    thermal_conductivity=thermal_conductivity,
                                    transparent=True,
                                    solar_absorption_coefficient=solar_absorption_coefficient,
                                    g_value=self.G_Value / self._NumberOfGlazings,
                                    wvdrf=999999,
                                    w20=0,
                                    w80=0)

        glass_materials.append(glazing_material)

        air_material = Material(name='WindowMaterialAir_{}'.format(self.Name),
                                density=1.4,
                                heat_capacity=1.0,
                                thermal_conductivity=0.026,
                                transparent=True,
                                solar_absorption_coefficient=0,
                                g_value=1,
                                wvdrf=1,
                                w20=0,
                                w80=0)

        glass_materials.append(air_material)

        thermal_resistance_glazing = (self._NumberOfGlazings * self._GlazingThickness) / thermal_conductivity

        glass_layers = list()
        glass_layers.append(MatLayer(material=glazing_material, thickness=self._GlazingThickness))
        for i in range(self._NumberOfGlazings - 1):
            glass_layers.append(MatLayer(material=air_material,
                                          thickness=((thermal_resistance_window - thermal_resistance_glazing) * 0.026 / (self._NumberOfGlazings - 1))
                                          )
                                 )
            glass_layers.append(MatLayer(material=glazing_material, thickness=self._GlazingThickness))

        glass_part = Part(name='WindowPart_{}'.format(self.Name),
                           layers=glass_layers)

        self._GlassPart = glass_part
        self._GlassLayers = glass_layers
        self._GlassMaterials = glass_materials

        # return glass_part, glass_layers, glass_materials

    def create_glass_face(self):

        self.print_status('creating_glass_face')
        # create vertices:
        face = self.OriginalFace.create_offset_face(offset=-self.FrameWidth)
        # face.Part = self.GlassPart
        self.GlassFace = face

    def create_frame_face(self):
        from PySimultan.face import Face

        face = Face(boundary=self.OriginalFace.Boundary,
                       holes=self.GlassFace.Boundary,
                       orientation=self.OriginalFace.Orientation,
                       part=None)
        self.FrameFace = face

    def calc_g_value(self):
        self.G_Value = (self.GlassFace.Area * self.GlassFace.G_Value) / (self.GlassFace.Area + self.FrameFace.Area)


class Material(ObjectBaseClass):

    new_material_id = itertools.count(0)

    def __init__(self,
                 name=None,
                 material_id=uuid.uuid4(),
                 color=np.append(np.random.rand(1, 3), 0) * 255,
                 density=1000,                  # kg / m^3
                 heat_capacity=1000,            # specific heat capacity [J /(kg K)]
                 thermal_conductivity=1,        # W /(m K)
                 transparent=False,             # material is transparent
                 emission_coefficient=0.93,      # emission coefficient
                 solar_absorption_coefficient=0.5,
                 g_value=0,
                 wvdrf=15,
                 w20=1,
                 w80=5):

        super().__init__(id=material_id,
                         pid=next(type(self).new_material_id),
                         color=color,
                         name=name
                         )

        self._PID = next(self.new_id)

        if name is None:
            self._Name = 'Material{}'.format(self.PID)
        else:
            self._Name = name

        # ------------------------------------------------------
        # physical properties:
        # -----------------------------------------------------
        self._Density = density                                             # kg/m³
        self._HeatCapacity = heat_capacity                                  # J/kg K
        self._ThermalConductivity = thermal_conductivity                    # W/m K
        self._EmissionCoefficient = emission_coefficient                    # -
        self._SolarAbsorptionCoefficient = solar_absorption_coefficient     # -
        self._Transparent = transparent                                     # true/false
        self._G_Value = g_value                                             # -
        self._WaterVaporDiffusionResistanceFactor = wvdrf                    # -
        self._w20 = w20
        self._w80 = w80

    # ------------------------------------------------------
    # physical properties:
    # -----------------------------------------------------

    @property
    def Density(self):
        return self._Density

    @Density.setter
    def Density(self, value):
        if (value > 100000) or (value < 0):
            raise ValueError('Density can not be grater than 100000 or less than 0')
        self._default_set_handling('Density', value)

    @property
    def HeatCapacity(self):
        return self._HeatCapacity

    @HeatCapacity.setter
    def HeatCapacity(self, value):
        if (value > 1000000) or (value < 0):
            raise ValueError('HeatCapacity can not be grater than 1000000 or less than 0')
        self._default_set_handling('HeatCapacity', value)

    @property
    def ThermalConductivity(self):
        return self._ThermalConductivity

    @ThermalConductivity.setter
    def ThermalConductivity(self, value):
        if (value > 1000000) or (value < 0):
            raise ValueError('ThermalConductivity can not be grater than 1000000 or less than 0')
        self._default_set_handling('ThermalConductivity', value)

    @property
    def Transparent(self):
        return self._Transparent

    @Transparent.setter
    def Transparent(self, value):
        if not isinstance(value, bool):
            raise ValueError('Transparent can only be boolean value')
        self._default_set_handling('Transparent', value)

    @property
    def EmissionCoefficient(self):
        return self._EmissionCoefficient

    @EmissionCoefficient.setter
    def EmissionCoefficient(self, value):
        if (value > 1) or (value < 0):
            raise ValueError('EmissionCoefficient value can not be grater than 1 or less than 0')
        self._default_set_handling('EmissionCoefficient', value)

    @property
    def SolarAbsorptionCoefficient(self):
        return self._SolarAbsorptionCoefficient

    @SolarAbsorptionCoefficient.setter
    def SolarAbsorptionCoefficient(self, value):
        if (value > 1) or (value < 0):
            raise ValueError('SolarAbsorptionCoefficient value can not be grater than 1 or less than 0')
        self._default_set_handling('SolarAbsorptionCoefficient', value)

    @property
    def G_Value(self):
        return self._G_Value

    @G_Value.setter
    def G_Value(self, value):
        if (value > 1) or (value < 0):
            raise ValueError('G_Value value can not be grater than 1 or less than 0')
        self._default_set_handling('G_Value', value)

    @property
    def WaterVaporDiffusionResistanceFactor(self):
        return self._WaterVaporDiffusionResistanceFactor

    @WaterVaporDiffusionResistanceFactor.setter
    def WaterVaporDiffusionResistanceFactor(self, value):
        self._default_set_handling('WaterVaporDiffusionResistanceFactor', value)

    @property
    def w20(self):
        return self._w20

    @w20.setter
    def w20(self, value):
        self._default_set_handling('w20', value)

    @property
    def w80(self):
        return self._w80

    @w80.setter
    def w80(self, value):
        self._default_set_handling('w80', value)

    # --------------------------------------------------------
    # observed object change callbacks
    # --------------------------------------------------------


class MatLayer(ObjectBaseClass):

    new_matlayer_id = itertools.count(0)

    def __init__(self,
                 mat_layer_id=uuid.uuid4(),
                 name=None,
                 color=np.append(np.random.rand(1, 3), 0) * 255,
                 material=None,
                 thickness=0.1
                 ):

        super().__init__(id=mat_layer_id,
                         pid=next(type(self).new_matlayer_id),
                         color=color,
                         name=name
                         )

        if name is None:
            self._Name = 'Layer{}'.format(self.PID)
        else:
            self._Name = name

        if material is None:
            self._Material = [Material()]
        else:
            if not isinstance(material, list):
                self._Material = [material]
            else:
                self._Material = material

        self._Thickness = thickness
        self._ThermalResistance = None

        # --------------------------------------------------------
        # bind observed objects
        # --------------------------------------------------------

        for material in self._Material:
            material.bind_to(self.material_updated)

        # ------------------------------------------------------
        # physical properties:
        # -----------------------------------------------------

    @property
    def Thickness(self):
        return self._Thickness

    @Thickness.setter
    def Thickness(self, value):
        self._default_set_handling('Thickness', value)

    @property
    def Material(self):
        return self._Material

    @Material.setter
    def Material(self, value):
        self._default_set_handling('Material', value)

    @property
    def ThermalResistance(self):
        if self._ThermalResistance is None:
            self.calc_thermal_resistance()
        return self._ThermalResistance

    @ThermalResistance.setter
    def ThermalResistance(self, value):
        if value < 0:
            raise ValueError('ThermalResistance can not be less than 0')
        self._default_set_handling('ThermalResistance', value)

    def calc_thermal_resistance(self):
        self._ThermalResistance = self.Thickness / self.Material.ThermalConductivity

    def material_updated(self):
        self.calc_thermal_resistance()




