.. _fire-suppression-api:

Fire Suppression
----------------
Fire Suppression is a `Scope 1 Emission <glossary.html>`_ that accounts for fire suppressant gas use. There are three different carbon accounting methods
employed in the final formula to calculate :math:`\text{CO}_2\; Equivalent\; Emissions` , and all three can be
utilized simultaneously if need be.

The EPA's SGEC workbook employs three methods for calculating emissions in Fire Suppression: material balance,
simplified material balance, and screening method.

Class Documentation
************************
.. module:: atomic6ghg.formulas.fire_suppression

.. autoclass:: FireSuppression
    :members:
    :undoc-members:
    :inherited-members:

Example Usage
******************

Python example code usage:

.. code-block:: python

    from atomic6ghg.formulas import FireSuppression

    fire_suppression_input: dict = {
        "version": "fire-suppression.1.0.0",
        "materialBalance": [
            {"gas": "hfc23", "inventoryChange": 25,
                "transferredAmount": 10, "capacityChange": 0}
        ]
    }
    engine = FireSuppression(fire_suppression_input)

    outputs: dict = engine.to_dict()
    print(outputs.get('totalCo2EquivalentEmissions'))

Material Balance
****************
The fundamental calculation for each fire suppressant gas type input for the Material Balance Method are their
:math:`\text{CO}_2\; Equivalent\; Emissions` emissions associated with the :math:`Inventory\; Change`,
:math:`Transferred\; Amount`, and :math:`Capacity\; Change` and based on :math:`GWP_{gas}`.

The possible gas types that :math:`\text{CO}_2\; Equivalent\; Emissions` can be calculated for when using the material
balance method for fire suppression are:

.. csv-table::
   :file: ./fire_suppression_material_balance.csv
   :header-rows: 1

The formula for :math:`\text{CO}_2\; Equivalent\; Emissions` is:

.. math::

   \text{CO}_2\; Equivalent\; Emissions_{B, E, gas} = GWP_{gas} \cdot \left(\left(I_{B} - I_{E}\right) + \left(P - S\right) + \left(C_{B} - C_{E}\right)\right)

This is derived from Equation 5 from [EPA2015FugitiveEmissions]_.

where :math:`gas` is the refrigerant gas type, :math:`GWP_{gas}` is the global
warming potential for that :math:`gas`, :math:`\left(I_{B} - I_{E}\right)` is the inventory change or the difference
between the amount of fire suppressant in inventory at the beginning of the reporting period and the amount in
inventory at the end of the reporting period, :math:`\left(P - S\right)` is the transferred amount or the difference
between the amount of fire suppressant purchases or other acquisitions (:math:`P`) and the amount of fire suppressant
sales or disbursements (:math:`S`), and :math:`\left(C_{B} - C_{E}\right)` is the  capacity change or the net change to
the total equipment volume for a given fire suppressant during the reporting period.


This is derived from Equation 5 from [EPA2015FugitiveEmissions]_.

Simplified Material Balance
***************************
The Simplified Material Balance Method is a simplified version of the Material Balance Method. With this simplified
method, there are fewer flows of fire suppressants to consider. This method is appropriate for entities that do not
maintain and track a stock of fire suppressants, and have not retrofitted equipment to use a different fire suppressant
during the reporting period. This method requires information on the quantity of fire suppressant:
(a) used to fill any new equipment installed during the reporting period,
(b) used to service equipment,
and (c) recovered from any equipment retired during the reporting period.
It also requires information on the total fire suppressant capacity of installed and retired equipment.

The possible gas types that :math:`\text{CO}_2\; Equivalent\; Emissions` can be calculated for when using the
simplified material balance method for fire suppression are:

.. csv-table::
   :file: ./fire_suppression_material_balance.csv
   :header-rows: 1

The fundamental calculation for each fire suppressant gas type input for the Simplified Material Balance Method are
their :math:`\text{CO}_2\; Equivalent\; Emissions` emissions based on :math:`GWP_{gas}`.
The formula for :math:`\text{CO}_2\; Equivalent\; Emissions` is:

.. math::


   \text{CO}_2\; Equivalent\; Emissions_{N, S, D, gas} = GWP_{gas} \cdot \left(\left(P_{N} - C_{N}\right) + P_{S} + \left(C_{D} - R_{D}\right)\right)

This is derived from Equation 6 from [EPA2015FugitiveEmissionsSimplified]_.

where :math:`gas` is the fire suppressant type, :math:`GWP_{gas}` is the global warming potential for that :math:`gas`,
:math:`P_{N}` is the new units charge or the purchases of fire suppressant used to charge new equipment, :math:`C_{N}`
is the new units capacity or the total fire suppressant capacity of the new equipment, :math:`P_{S}` is the existing
units recharge or the purchases of fire suppressant used to service equipment, :math:`C_{D}` is the disposed units
capacity or the total fire suppressant capacity of retiring equipment, and :math:`R_{D}` is the disposed units
recovered or the fire suppressant recovered from retiring equipment.

Screening Method
****************

In addition to the fire suppressants, the Screening Method requires an equipment type to be entered to the fire
suppressant used with the equipment, and must be one of the following:

.. csv-table::
   :file: ./fire_suppression_equipment.csv
   :widths: 9
   :header-rows: 1

The possible gas types that :math:`\text{CO}_2\; Equivalent\; Emissions` can be calculated for when using the
screening method for fire suppression are:

.. csv-table::
   :file: ./fire_suppression_material_balance.csv
   :header-rows: 1

The Screening Method is another way to calculate emissions from Fire Suppression.
With this method, there are four emission stages which include charging, operation, servicing, and end-of-life.

The fundamental calculation for each fire suppressant gas type input for the Screening Method are
their :math:`\text{CO}_2\; Equivalent\; Emissions` based on :math:`GWP_{gas}` and the emission stages.
The formula for :math:`\text{CO}_2\; Equivalent\; Emissions` is:

.. math::


    \text{CO}_2\; Equivalent\; Emissions_{gas, E} = GWP_{gas} \cdot EF_{E} \cdot Unit\; Capacity

This is derived from Section 2.1.2 from [EPA2014FugitiveEmissionsScreening]_.

where :math:`gas` is the fire suppressant gas type, :math:`E` is the type of equipment (either fixed or portable)
:math:`GWP_{gas}` is the global warming potential for that :math:`gas`,
:math:`EF_{E}` is the emission factor for that equipment type :math:`E`, and
:math:`Unit\; Capacity` is the fire suppressant capacity for each piece of equipment.

.. [EPA2014FugitiveEmissionsScreening] EPA, 2014: 2014 EPA Greenhouse Gas Inventory Guidance, Direct Fugitive Emissions from Refrigeration, Air Conditioning, Fire Suppression, and Industrial Gases, pp. 7

For fire suppression, the :math:`\text{CO}_2\; Equivalent\; Emissions_{method}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{method} = \sum_{n=1}^{\infty} Emissions_{method}

This equation is derived from [EPA2015FugitiveEmissions]_.

where :math:`Emissions_{method}` are the total :math:`\text{CO}_2\; Emissions` for that :math:`method`
(material balance, simplified material balance, or screening method).
Note that in atomic6 the :math:`Emissions_{material\; balance}` and :math:`Emissions_{simplified\; material\; balance}`
are multiplied by :math:`kilogram\; per\; pound` to convert the values from :math:`lbs` to :math:`kilograms`
and the final value is divided by :math:`1000` to convert this value into :math:`metric \; tons`.
