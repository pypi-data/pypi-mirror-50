from typing import List
import numpy as np
from ase import Atoms
from ase.build import bulk
from spglib import get_symmetry_dataset


def get_tetrahedral_volume(triangle, origin):
    """
    Get the volume of the tetrahedron formed by the origin
    and three vertices defined by the input.

    Parameters
    ----------
    triangle : list of list of 3 floats
        Three coordinates forming a triangle
    origin : list of 3 floats
        The origin

    Returns
    -------
    float
        The volume
    """
    if len(triangle) != 3:
        raise ValueError('triangle argument must contain three coordinates')
    M = np.vstack((triangle, [0, 0, 0]))
    M = np.vstack((M.transpose(), [1, 1, 1, 1]))
    return abs(np.linalg.det(M)) / 6


def get_angle(v1, v2, tol=1e-5):
    cos = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    if abs(abs(cos) - 1) < tol:
        if cos < -1.0:
            cos = -1.0
        elif cos > 1.0:
            cos = 1.0
    return np.arccos(cos)


def get_rotation_matrix(theta, u):
    u /= np.linalg.norm(u)
    R = np.zeros((3, 3))
    R[0, 0] = np.cos(theta) + u[0] * u[0] * (1 - np.cos(theta))
    R[1, 0] = u[0] * u[1] * (1 - np.cos(theta)) + u[2] * np.sin(theta)
    R[2, 0] = u[0] * u[2] * (1 - np.cos(theta)) - u[1] * np.sin(theta)
    R[0, 1] = u[0] * u[1] * (1 - np.cos(theta)) - u[2] * np.sin(theta)
    R[1, 1] = np.cos(theta) + u[1] * u[1] * (1 - np.cos(theta))
    R[2, 1] = u[1] * u[2] * (1 - np.cos(theta)) + u[0] * np.sin(theta)
    R[0, 2] = u[0] * u[2] * (1 - np.cos(theta)) + u[1] * np.sin(theta)
    R[1, 2] = u[1] * u[2] * (1 - np.cos(theta)) - u[0] * np.sin(theta)
    R[2, 2] = np.cos(theta) + u[2] * u[2] * (1 - np.cos(theta))
    return R


def break_symmetry(full_symmetry: List[np.ndarray],
                   symmetry_axes: List[np.ndarray],
                   inversion: List[bool] = None) -> List[np.ndarray]:
    """
    Reduce symmetry elements to only those that do not affect
    one or more vectors.

    Parameters
    ----------
    full_symmetry
        List of candidate symmetries
    symmetry_axes
        Vectors that must remain unchanged by symmetry operation
    inversion
        One boolean for each `symmetry_axis`, if True, a symmetry
        element is kept if it only inverts any or all of the
        symmetry axes
    """
    if inversion is None:
        inversion = [False] * len(symmetry_axes)
    else:
        if len(inversion) != len(symmetry_axes):
            raise ValueError('inversion must be a list of bools with '
                             'the same length as symmetry_axes '
                             '({} != {})'.format(len(inversion),
                                                 len(symmetry_axes)))
    broken_symmetry = []
    for R in full_symmetry:
        for symmetry_axis, inv in zip(symmetry_axes, inversion):
            v = np.dot(R, symmetry_axis)
            if not np.allclose(v, symmetry_axis):
                if inv:
                    if not np.allclose(v, -symmetry_axis):
                        break
                else:
                    break
        else:
            broken_symmetry.append(R)
    return broken_symmetry


def get_primitive_with_symmetries(primitive_structure: Atoms) -> (Atoms, List[np.ndarray]):
    """
    Get symmetry operations of the point group. For fcc and bcc,
    we make a cubic cell because everyone expects that Miller
    indices refer to the conventional cell.

    TODO: What about other cubic structures?

    Parameters
    ----------
    primitive_structure
        The primitive structure for which the symmetry operations
        is to be extracted

    Returns
    -------
    ASE Atoms
        If a primitive fcc or bcc cell was provided, the
        conventional cell is returned, otherwise the same
        primitive structure as was provided as argument is
        returned.
    symmmetries : list of NumPy arrays
        The symmetry operations of the point group in matrix format.
    """
    symmetry_data = get_symmetry_dataset(primitive_structure)
    if symmetry_data['pointgroup'] == 'm-3m' and len(primitive_structure) == 1:
        spacegroup = symmetry_data['number']
        if spacegroup == 225:  # fcc

            primitive_structure = bulk(
                primitive_structure[0].symbol,
                crystalstructure='fcc',
                a=(4 * primitive_structure.get_volume())**(1 / 3.),
                cubic=True)
            symmetry_data = get_symmetry_dataset(bulk('Au', a=1.0, crystalstructure='sc'))
        elif spacegroup == 229:  # bcc
            primitive_structure = bulk(
                primitive_structure[0].symbol,
                crystalstructure='bcc',
                a=(2 * primitive_structure.get_volume())**(1 / 3.),
                cubic=True)
            symmetry_data = get_symmetry_dataset(bulk('Au', a=1.0, crystalstructure='sc'))
    symmetries = []
    for R, _ in zip(symmetry_data['rotations'], symmetry_data['translations']):
        symmetries.append(R)
    return primitive_structure, symmetries


def is_array_in_arrays(array: np.ndarray, arrays: List[np.ndarray]) -> bool:
    """
    Checks whether an array exists (True) or not (False) in a list
    of arrays.

    Parameters
    ----------
    array
        Array to be searched for
    arrays
        List of arrays to search among
    """
    for array_comp in arrays:
        if np.allclose(array, array_comp):
            return True
    return False


def where_is_array_in_arrays(array: np.ndarray, arrays: List[np.ndarray]) -> int:
    """
    Returns the index of an array in a list of arrays.

    array
        Array to search for
    arrays
        List of arrays to search within
    """
    for i, array_comp in enumerate(arrays):
        if np.allclose(array, array_comp):
            return i
    return -1
