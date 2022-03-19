.. _waste-gases-api:

Waste Gases
-----------
Waste Gases are a `Scope 1 Emission <glossary.html>`_ that account for `waste gas streams <glossary.html>`_ that are
combusted with a `flare <glossary.html>`_ or `thermal oxidizer <glossary.html>`_. These combustion's result in
:math:`\text{CO}_2` emissions that should be included in GHG inventories.

Usage
**********
.. module:: atomic6ghg.formulas.waste_gases

.. autoclass:: WasteGases
   :members:
   :undoc-members:
   :inherited-members:

.. code-block:: python

    from atomic6ghg.formulas.waste_gases import WasteGases

    calculated_data = WasteGases.to_dict(input_data)

    calculated_data['totalCo2EquivalentEmissions']

**Parameters:**
    * **input_data** - (dict) input data that follows the JSON schema


EPA Equation Analysis
**************************************************
Waste Gases calculates the carbon content (or emission factor) for some complex waste gas streams. These complex waste
gas streams include:

.. csv-table::
    :file: ./waste_gases.csv
    :header-rows: 1


The fundamental calculations for each waste gas Component are their :math:`Total\; Moles_{a}`,
:math:`Carbon\; Content_{a}`.
The formulas are:


.. math::

    Total\; Moles_{a} = Molar\; Fraction_{a} \cdot Oxidation\; Factor

where :math:`Total\; Moles_{a}` is the Molar concentration of gas :math:`a`, the :math:`Molar\; Fraction_{a}` is the
molar fraction of gas :math:`a`, and :math:`Oxidation\; Factor` is the percentage of carbon that is actually oxidized
when combustion occurs.

.. math::

    Carbon\; Content_{a} = Total\; Moles_{a} \cdot Molecular\; Weight_{a} \cdot Percent\; Carbon_{a}

These equations are derived from Equation 4 from [EPA2016DirectEmissionsfromStationaryCombustionSources]_.

where :math:`Carbon\; Content_{a}` is the amount of carbon produced from gas :math:`a`, :math:`Total\; Moles_{a}` is
the Molar concentration of gas :math:`a`, :math:`Molecular\; Weight_{a}` is the molecular weight of gas component
:math:`a`, and :math:`Percent\; Carbon_{a}` is the carbon fraction of gas :math:`a`.


For waste gases, the :math:`\text{CO}_2\; Equivalent\; Emissions` in metric tons is calculated. The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions = Total\; Carbon\; Content\; for\; All\; Components \cdot Oxidation\; Factor \cdot Atomic\; Weight\; of\; Carbon \cdot Molar\; Concentration

This equation is derived from Equation 5 from [EPA2016DirectEmissionsfromStationaryCombustionSources]_.

where :math:`Total\; Carbon\; Content` is the sum of all the carbon contents for all gas components,
:math:`Oxidation\; Factor` is the percentage of carbon that is actually oxidized when combustion occurs,
:math:`Atomic\; Weight\; of\; Carbon` is the natural atomic weight of carbon gas, and :math:`Molar\; Concentration` is
the gas total number of moles per unit volume.

