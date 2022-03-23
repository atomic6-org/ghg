.. _refrigeration-and-ac-api:

Refrigeration and AC
--------------------
Refrigeration and Air Conditioning (AC) is `scope 1 emission <glossary.html>`_.
Refrigeration and Air Conditioning (AC) equipment sources can vary in size based on the type of organization.  Emissions from refrigeration and AC devices, in facilities or vehicles, are caused by the leakage of chemicals with global warming impact during use, maintenance and/or disposal of the device.  They are often small sources for office-based organizations.  For example, a small office building may have one rooftop AC unit while a grocery store chain may have several rooftop AC units per store as well as a multitude of other refrigeration equipment.


Usage
**********
.. module:: atomic6ghg.formulas.refrigeration_and_ac
.. autoclass:: RefrigerationAndAc
   :members:
   :undoc-members:
   :inherited-members:

Python example code usage:

.. code-block:: python

    from atomic6ghg.formulas import RefrigerationAndAc

    refrigeration_and_ac_input: dict = {
        "version": "refrigeration-and-ac.1.0.0",
        "materialBalance": [
            {
              "gas": "co2", "gasGWP": 1, "inventoryChange": 100,
                "transferredAmount": 100, "capacityChange": 100,
                "co2EquivalentEmissions": 300
            }
        ]
    }
    engine = RefrigerationAndAc(refrigeration_and_ac_input)

    outputs: dict = engine.to_dict()
    print(outputs.get('totalCo2EquivalentEmissions'))


EPA Equation Analysis
**************************************************

Refrigeration and AC calculates emissions for refrigerant gas use. There are three different carbon accounting methods
employed in the formula, and all three can be utilized simultaneously if need be. In general, Refrigeration and AC
allows for inputs of gases for the following:

.. csv-table::
   :file: ./refrigeration_and_ac_gases.csv
   :widths: 9
   :header-rows: 1

The EPA's SGEC workbook employs three methods for calculating emissions in Refrigeration and AC: material balance,
simplified material balance, and the screening method.

Material Balance
****************

The Material Balance Method tracks emissions of refrigerants from equipment through a mass balance analysis. Releases
of refrigerants can be calculated based on the inventory (in storage, not in operating equipment), purchases and sales
of refrigerants, as well as changes in total refrigerant capacity of equipment during the emissions reporting period.
The inventory should be tracked at the facility level by type of refrigerant.

The fundamental calculation for each refrigerant gas type input for the Material Balance Method are their
:math:`\text{CO}_2\; Equivalent\; Emissions` emissions associated with the :math:`Inventory\; Change`,
:math:`Transferred\; Amount`, and :math:`Capacity\; Change` and based on :math:`GWP_{gas}`.
The formula for :math:`\text{CO}_2\; Equivalent\; Emissions` is:

.. math::

   \text{CO}_2\; Equivalent\; Emissions_{B, E, gas} = GWP_{gas} \cdot \left(\left(I_{B} - I_{E}\right) + \left(P - S\right) + \left(C_{B} - C_{E}\right)\right)

This is derived from Equation 5 from [EPA2015FugitiveEmissions]_.

where :math:`gas` is the refrigerant gas type, :math:`GWP_{gas}` is the global
warming potential for that :math:`gas`, :math:`\left(I_{B} - I_{E}\right)` is the inventory change or the difference
between the amount of refrigerant in inventory at the end of the reporting period and the amount in inventory at the
beginning of the reporting period (where inventory is defined as the total stored on site in cylinders or other storage
and does not include refrigerants contained within equipment), :math:`\left(P - S\right)` is the difference between the
amount of refrigerant purchases or other acquisitions (:math:`P`) and the amount of refrigerant sales or disbursements
(:math:`S`), and :math:`\left(C_{B} - C_{E}\right)` is the  capacity change or the net change to the total equipment
volume for a given refrigerant during the reporting period.

.. [EPA2015FugitiveEmissions] EPA, 2015: 2015 EPA Greenhouse Gas Inventory Guidance, Direct Fugitive Emissions from Refrigeration, Air Conditioning, Fire Suppression, and Industrial Gases, pp. 8


Simplified Material Balance
***************************
The Simplified Material Balance Method is a simplified version of the Material Balance Method. With this simplified
method, there are fewer flows of refrigerants to consider. This method is appropriate for entities that do not maintain
and track a stock of refrigerants, and have not retrofitted equipment to use a different refrigerant during the
reporting period. This method requires information on the quantity of refrigerant:
(a) used to fill any new equipment installed during the reporting period,
(b) used to service equipment,
and (c) recovered from any equipment retired during the reporting period.
It also requires information on the total refrigerant capacity of installed and retired equipment.

The fundamental calculation for each refrigerant gas type input for the Simplified Material Balance Method are
their :math:`\text{CO}_2\; Equivalent\; Emissions` emissions based on :math:`GWP_{gas}`.
The formula for :math:`\text{CO}_2\; Equivalent\; Emissions` is:

.. math::

   \text{CO}_2\; Equivalent\; Emissions_{N, S, D, gas} = GWP_{gas} \cdot \left(\left(P_{N} - C_{N}\right) + P_{S} + \left(C_{D} - R{D}\right)\right)

This is derived from Equation 6 from [EPA2015FugitiveEmissionsSimplified]_.

where :math:`gas` is the refrigerant gas type, :math:`GWP_{gas}` is the global warming potential for that :math:`gas`,
:math:`P_{N}` is the new units charge or the purchases of refrigerant used to charge new equipment, :math:`C_{N}` is
the new units capacity or the total refrigerant capacity of the new equipment, :math:`P_{S}` is the existing units
recharge or the purchases of refrigerant used to service equipment, :math:`C_{D}` is the disposed units capacity or the
total refrigerant capacity of retiring equipment, and :math:`R_{D}` is the disposed units recovered or the refrigerant
recovered from retiring equipment.

.. [EPA2015FugitiveEmissionsSimplified] EPA, 2015: 2015 EPA Greenhouse Gas Inventory Guidance, Direct Fugitive Emissions from Refrigeration, Air Conditioning, Fire Suppression, and Industrial Gases, pp. 10


Screening Method
****************

In addition to the refrigerant gases, the Screening Method requires an equipment type to be entered to the refrigerant
used with the equipment, and must be one of the following:

.. csv-table::
   :file: ./refrigeration_and_ac_equipment.csv
   :widths: 9
   :header-rows: 1

The Screening Method is another way to calculate emissions from Refrigeration and AC and is particularly applicable to
the Refrigeration and AC application because of the significant servicing component required to maintain equipment.
With this method, there are four emission stages which include charging, operation, servicing, and end-of-life.

The fundamental calculation for each refrigerant gas type input for the Screening Method are
their :math:`\text{CO}_2\; Equivalent\; Emissions` based on :math:`GWP_{gas}` and the emission stages.
The formula for :math:`\text{CO}_2\; Equivalent\; Emissions` is:

.. math::

   \text{CO}_2\; Equivalent\; Emissions_{B, E, gas} = GWP_{gas} \cdot \left(\left(I_{B} - I_{E}\right) + \left(P - S\right) + \left(C_{B} - C_{E}\right)\right)

This is derived from Equation 7.9 from [IPCC2006V3CH7]_.

where :math:`gas` is the refrigerant gas type, :math:`GWP_{gas}` is the global warming potential for that :math:`gas`,
:math:`I_{B} - I_{E}` is the inventory change or the difference of gas stored in inventory from the beginning to the
end of the reporting period, :math:`P - S` is the transferred amount or the gas purchased minus the gas sold/disposed
during the reporting period, and  sum of the
full charges of all the new equipment that is sold in the country in a given year,
:math:`C_{B} - C_{E}` is the capacity change or the capacity of all units at the beginning of the reporting period
minus the capacity of all units at the end of the reporting period. Note that in atomic6, the input to this calculation
already accounts for intermediary calculations.

For refrigeration and ac, the :math:`\text{CO}_2\; Equivalent\; Emissions_{method}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{method} = \sum_{n=1}^{\infty} Emissions_{method}

This equation is derived from [IPCC2006V3CH7]_.

where :math:`Emissions_{method}` are the total :math:`\text{CO}_2\; Emissions` for that :math:`method`
(material balance, simplified material balance, or screening method).
Note that in atomic6 the :math:`Emissions_{material\; balance}` and :math:`Emissions_{simplified\; material\; balance}`
are multiplied by :math:`kilogram\; per\; pound` to convert the values from :math:`lbs` to :math:`kilograms`
and the final value is divided by :math:`1000` to convert this value into :math:`metric \; tons`.


.. [IPCC2006V3CH7] IPCC, 2006: 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 3, IPPU, Chapter 7, Emissions of Fluorinated Substitutes for Ozone Depleting Substances, pp. 48
