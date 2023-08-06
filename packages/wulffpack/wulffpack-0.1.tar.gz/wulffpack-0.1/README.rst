WulffPack
=========

**WulffPack** is a tool for making Wulff constructions, typically for
minimizing the energy of nanoparticles. A detailed description of the
functionality provided as well as an extensive tutorial can be found in the
`user guide <https://materials-modeling.gitlab.io/wulffpack>`_.

**WulffPack** constructs both continuum models and atomistic structures for
further modeling with, e.g., molecular dynamics or electronic structure
methods.

.. code-block:: python
   
    surface_energies = {(1, 1, 1): 1.0, (1, 0, 0): 1.2}
    particle = SingleCrystal(surface_energies)
    particle.view()
    write('atoms.xyz', particle.atoms)


Installation
------------

# TODO It cannot yet

In the most simple case, **WulffPack** can be installed using pip as follows::

    pip3 install wulffpack --user

or alternatively::

    python3 -m pip install wulffpack --user


**WulffPack** is based on Python3 and invokes functionality from other Python
libraries including

* `ASE <https://wiki.fysik.dtu.dk/ase>`_,
* `Spglib <https://atztogo.github.io/spglib/>`_,
* `NumPy <https://www.numpy.org/>`_, and
* `Matplotlib <https://matplotlib.org/>`_.


Credits
-------

* J Magnus Rahm