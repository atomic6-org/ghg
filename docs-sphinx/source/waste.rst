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

Python example code usage:

.. code-block:: python

    from atomic6ghg.formulas import Waste
    waste_input: dict = {
        "version": "waste.1.0.0",
        "wasteDisposal": [
            {
                "sourceId": "",
                "sourceDescription": "",
                "wasteMaterial": "aluminumCans",
                "disposalMethod": "recycled",
                "weight": 800,
                "unit": "pounds"
            }
        ]
    }
    engine = Waste(waste_input)
    outputs: dict = engine.to_dict()
    print(outputs.get('totalCO2EquivalentEmissions'))

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

   \text{CO}_2\; Equivalent\; Emissions_{material, method} = Emission\; Factor_{material, method} \cdot Weight_{material}


This equation is derived from Equation 3.2 from [IPCC2006_V5CH3]_.

where :math:`material` is the waste material, :math:`method` is the disposal method,
:math:`Emission\; Factor_{material, method}` is the emission factor for that :math:`material` and :math:`method`, and
:math:`Weight_{material}` is the weight, mass, or amount of the :math:`material` that has been disposed via :math:`method` during
that reporting period. Note that in atomic6, the calculations are done directly to :math:`\text{CO}_2` by using the
`IPCC's AR4 GWP values <https://archive.ipcc.ch/publications_and_data/ar4/wg1/en/ch2s2-10-2.html>`_ as a conversion
factor to convert waste emission factors to :math:`\text{CO}_2\;`, while in the reference material the calculations are done directly to :math:`\text{CH}_4`. The input units are
converted to a standard unit of short tons, and the short tons are converted into kilograms.

For waste, the :math:`\text{CO}_2\; Equivalent\; Emissions_{method}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{method} = \sum_{n=1}^{\infty} Total\; Emissions_{method}

This equation is derived from [IPCC2006_V5CH3]_.

where :math:`Total\; Emissions_{method}` is the sum of all the :math:`\text{CO}_2\;` emissions for that
:math:`method` (recycled, landfilled, combusted, composted, anaerobically digested (dry digestate with
curing), or anaerobically digested (wet digestate with curing)).
Note that in atomic6 the final value of this calculation is converted into :math:`metric\; tons`.


.. [IPCC2006_V5CH3] `IPCC, 2006: 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 5, IPPU, Chapter 3, Solid Waste Disposal, pp. 9 <https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/5_Volume5/V5_3_Ch3_SWDS.pdf#page=9>`_
