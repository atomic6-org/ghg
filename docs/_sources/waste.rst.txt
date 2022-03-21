.. _waste-api:

Waste
-----
Waste is a `Scope 3 Emission <glossary.html>`_ that accounts for garbage or `refuse <glossary.html>`_,
`sludge <glossary.html>`_ from a wastewater treatment plant, water supply treatment plant, or air pollution control
facility and other discarded material, resulting from industrial, commercial, mining, and agricultural operations, and
from community activities.

Usage
**********
.. module:: atomic6ghg.formulas.waste

.. autoclass:: Waste
   :members:
   :undoc-members:
   :inherited-members:

EPA Equation Analysis
**************************************************
The fundamental calculation for Waste is the :math:`\text{CO}_2\; Equivalent\; Emissions` produced by the
disposal of waste materials based on the :math:`Disposal\; Method` and :math:`weight`.

Waste allows for inputs of waste materials for the calculation over the following disposal methods and units:

.. csv-table::
    :file: ./waste.csv
    :header-rows: 1

The formula for :math:`\text{CO}_2\; Equivalent\; Emissions` is:

.. math::

   \text{CO}_2\; Equivalent\; Emissions_{ma, me} = EF_{ma, me} \cdot Weight


This equation is derived from Equation 3.2 from [IPCC2006V5CH3]_.

where :math:`ma` is the waste material, :math:`me` is the disposal method, :math:`EF_{ma, me}` is the emission factor
is the emission factor for that :math:`ma` and :math:`me`, and :math:`Weight` is the weight, mass, or amount of the
:math:`ma` that has been disposed via :math:`me` during that reporting period. Note that in atomic6, the calculations
are done directly to :math:`\text{CO}_2` by using the IPCC's AR4 GWP values as a conversion factor, while in the
reference material the calculations are done directly to :math:`\text{CH}_4`, the input units are converted to a
standard unit of short tons, and the short tons are converted into kilograms.

For waste, the :math:`\text{CO}_2\; Equivalent\; Emissions_{disposal\; method}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{disposal\; method} = \sum_{n=1}^{\infty} Total\; Emissions_{disposal\; method}

This equation is derived from [IPCC2006V5CH3]_.

where :math:`Total\; Emissions_{disposal\; method}` is the sum of all the :math:`\text{CO}_2\;` emissions for that
:math:`disposal\; method` (recycled, landfilled, combusted, composted, anaerobically digested (dry digestate with
curing), or anaerobically digested (wet digestate with curing)).
Note that in atomic6 the final value of this calculation is converted into :math:`metric\; tons`.


.. [IPCC2006V5CH3] IPCC, 2006: 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 5, IPPU, Chapter 3, Solid Waste Disposal, pp. 9
