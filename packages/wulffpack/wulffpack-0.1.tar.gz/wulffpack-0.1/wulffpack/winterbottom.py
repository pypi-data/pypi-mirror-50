from typing import Dict
import numpy as np
from .core import BaseParticle
from .core.form import setup_forms
from .core.geometry import (get_primitive_with_symmetries,
                            break_symmetry,
                            get_angle,
                            get_rotation_matrix)
from ase import Atoms
from ase.build import bulk


class Winterbottom(BaseParticle):
    """
    A `Winterbottom` object is a Winterbottom construction, i.e.,
    the lowest energy shape adopted by a single crystalline particle
    in contact with an interface.

    Parameters
    ----------
    surface_energies
        A dictionary with surface energies, where keys are
        Miller indices and values surface energies (per area)
        in a unit of choice, such as J/m^2.
    interface_direction
        Miller indices for the interface facet.
    interface_energy
        Energy per area for twin boundaries.
    primitive_structure
        Primitive cell to implicitly define the space group as
        well as the atomic structure used if an atomic structure
        is requested. By default, an Au FCC structure is used.
    natoms
        Together with `primitive_structure`, this parameter
        defines the volume of the particle. If an atomic structure
        is requested, the number of atoms will as closely as possible
        match this value.
    tol
        Numerical tolerance parameter.

    Example
    -------
    The following example illustrates some possible uses of a
    `Winterbottom` object::

        from wulffpack import Winterbottom
        from ase.build import bulk
        from ase.io import write

        surface_energies = {(1, 1, 0): 1.0, (1, 0, 0): 1.08}
        prim = bulk('Ag', a=4.1, crystalstructure='fcc')
        particle = Winterbottom(surface_energies=surface_energies,
                                interface_direction=(3, 2, 1),
                                interface_energy=0.4,
                                primitive_structure=prim)
        particle.view()
        # Writes atomic structure to file
        write('winterbottom.xyz', particle.atoms)

    """

    def __init__(self,
                 surface_energies: Dict[tuple, float],
                 interface_direction: tuple,
                 interface_energy: float,
                 primitive_structure: Atoms = None,
                 natoms: int = 1000,
                 tol: float = 1e-5):
        if primitive_structure is None:
            primitive_structure = bulk('Au', crystalstructure='fcc', a=4.0)
        prim, cubic_symmetries = get_primitive_with_symmetries(primitive_structure)

        symmetries = break_symmetry(cubic_symmetries,
                                    [interface_direction])

        if interface_energy > min(surface_energies.values()):
            raise ValueError('The construction expects an interface energy '
                             'that is smaller than than the smallest '
                             'surface energy.')
        surface_energies = surface_energies.copy()
        surface_energies['interface'] = interface_energy
        forms = setup_forms(surface_energies,
                            prim.cell.T,
                            symmetries,
                            cubic_symmetries,
                            interface=interface_direction)

        super().__init__(forms=forms,
                         primitive_structure=prim,
                         natoms=natoms,
                         tol=tol)

        # Rotate particle such that the interface aligns with the plane z=0
        target = (0, 0, -1)
        rotation_axis = np.cross(interface_direction, target)
        angle = get_angle(interface_direction, target)
        R = get_rotation_matrix(angle, rotation_axis.astype(float))
        self.rotate_particle(R)

    @property
    def atoms(self):
        """
        Returns an ASE Atoms object
        """
        return self._get_atoms()
