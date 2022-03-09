Formulas
========

Each of the 13 sheets in the EPA's SGEC workbook have a corresponding python script associated with them in atomic6 that
performs the calculations for the library, which are referred to as formulas in our documentation, and are located
under ghg/atomic6-ghg/formulas. Each formula is implemented as a python class with methods for calculating and
manipulating the data into the schema format.

Stationary Combustion
---------------------
Stationary Combustion is a Scope 1 Emission (`See glossary <glossary.html>`_) that includes, but is not limited to,
boilers, simple and combined-cycle combustion turbines, engines, incinerators, and process heaters. Stationary fuel
combustion sources are devices that combust solid, liquid, or gaseous fuel, generally for the purposes of producing
energy, generating steam, providing useful heat or energy for industrial, commercial or institutional use, or reducing
the volume of waste by removing combustible matter.

Usage
**********
.. code-block:: python

    from atomic6-ghg.formulas.stationary_combustion import StationaryCombustion

    calculated_data = StationaryCombustion.to_dict(input_data)
    calculated_data['totalCo2EquivalentEmissions']
    calculated_data['totalBiomassEquivalentEmissions']

**Parameters:**
    * **input_data** - (dict) input data that follows the JSON schema


EPA Equation Analysis
**************************************************
Stationary combustion allows for inputs of combusted quantities for the following sources with units, which are
converted into an internal atomic6 unit:

.. csv-table::
   :file: ./stationary_combustion.csv
   :header-rows: 1

The fundamental calculation for each source are their :math:`\text{CO}_2`, :math:`\text{CH}_4`, and
:math:`\text{N}_2\text{O}` emissions associated with the quantity combusted. The formula is:

.. math::

   Emissions_{GHG,\, fuel} = Fuel\; Consumption_{fuel} \cdot Emission\; Factor_{GHG,\, fuel}

This is Equation 2.1 from [IPCC2006V2CH2]_. Note, in atomic6, the :math:`Fuel\; Consumption_{fuel}` is actually composed
of two terms:

.. math::

   Fuel\; Consumption_{fuel} = User\; Input\; Fuel\; Consumption_{fuel,\, fuel\: units} \cdot Unit\; Conversion\; Factor_{fuel\: units}

where :math:`Unit\; Conversion\; Factor_{fuel\; units}` converts the :math:`fuel\; units` into the standardized
internal atomic6 unit for :math:`Fuel\; Consumption_{fuel}`, which varies depending on the stationary combustion source
(see above table). This is necessary, since :math:`Emission\; Factor_{GHG,\; fuel}` is only available in limited sets
of units, but we want to allow for a wide range of input units for :math:`fuel\; units` to minimize unit conversion
being done by the user from the system they use for record keeping.

For stationary combustion, the :math:`Total \text{CO}_2\; Equivalent\; Emissions_{GHG,\, fuel}` and
:math:`Total\; Biomass\; \text{CO}_2\; Equivalent\; Emissions_{GHG}` in metric tons are calculated. The formulas are:

.. math::

    Total\; \text{CO}_2\; Equivalent\; Emissions_{GHG,\, fuel} = \sum_{n=1}^{\infty} Emissions_{GHG,\, fuel, n} \cdot EF_{GHG}


where :math:`Total\; \text{CO}_2\; Equivalent\; Emissions_{GHG, fuel}` is the sum of all :math:`GHG` emissions by
each source (fossil fuel or non fossil fuel), :math:`Emissions_{GHG,\, fuel}` are emissions of any :math:`GHG`
(fossil fuel or non fossil fuel :math:`\text{CO}_2`, :math:`\text{CH}_4`, and :math:`\text{N}_2\text{O}`),
and :math:`EF_{GHG}` is the emission factor for that :math:`GHG` to convert it into :math:`\text{CO}_2\;`.
Note that in atomic6, those emissions with units of grams are converted into kilograms, then the final value of this
calculation is divided by :math:`1000` to convert this value into :math:`metric \; tons`.

.. math::

    Total\; Biomass\; \text{CO}_2\; Equivalent\; Emissions_{fuel} = \sum_{n=1}^{\infty} Non\; Fossil\; Fuel\; \text{CO}_2\; Emissions_{fuel, n}

These equations are outlined in Equation 2.2 from [IPCC2006V2CH2]_.

where :math:`Total\; Biomass\; \text{CO}_2\; Equivalent\; Emissions_{fuel}` is the sum of
:math:`Non\; Fossil\; Fuel\; \text{CO}_2\; Emissions_{fuel, n}`, which only accounts for the GHG :math:`\text{CO}_2`.
Note that in atomic6, all units for total calculations are converted :math:`metric \; tons`.

.. [IPCC2006V2CH2] IPCC, 2006: 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 2, Energy, Chapter 2, Stationary Combustion, pp. 11

Mobile Sources
--------------
Mobile sources allows for inputs of fuel usage for the following vehicle type and fuel type combinations:

.. csv-table::
   :file: ./mobile_sources.csv
   :header-rows: 1

Where CNG is compressed natural gas, LPG is liquefied petroleum gases, and LNG is liquefied natural gas.

The only acceptable units for fuel usage entry are gallons for all fuel types except CNG, which the only acceptable unit
for fuel entry entry is scf.

If entering data for Passenger Cars, Light-Duty Trucks, Heavy-Duty Vehicles, or Motorcycles that use a fuel type of
Gasoline, then the vehicle make year must be entered in as well as the :math:`\text{CH}_4`, and
:math:`\text{N}_2\text{O}` emissions factors for these vehicle types with gasoline depend on the year and will not
calculate otherwise.

The fundamental calculation for each vehicle type/fuel type input are their :math:`\text{CO}_2`, :math:`\text{CH}_4`,
and :math:`\text{N}_2\text{O}` emissions associated with the quantity combusted. The formula for :math:`\text{CO}_2`
emissions, denoted :math:`Emission_{a}` is:

.. math::

   Emission_{a} = Fuel_{a} \cdot EF_{a}

where :math:`a` is the fuel type, :math:`Fuel_{a}` is the fuel usage (fuel sold) and :math:`EF_{a}` is the
:math:`\text{CO}_2` emission factor for fuel type :math:`a`. This is derived from Equation 3.2.1 from [IPCC2006V2CH3]_.

Note:
 * :math:`\text{CO}_2` emissions for Gasoline, Gasoline (2 stroke), and Gasoline (4 stroke) are aggregated
   together under Gasoline for :math:`\text{CO}_2` emissions by fuel type, as well as the fraction of ethanol that is
   comprised of gasoline. This fraction is obtained from a value in the schema for mobile sources under the
   key "ethanolPercent" (under the top level key "properties"). To obtain the fraction of gasoline in the ethanol
   (:math:`f_g`), let :math:`EP` be the value for "ethanolPercent", then :math:`f_g = 1 - \frac{EP}{100}`. :math:`EP` is
   set to a default value of :math:`80\%`.
 * Similar to :math:`\text{CO}_2` emissions for Gasoline, :math:`\text{CO}_2` emissions for Diesel include the fraction
   of Biodiesel that is comprised of diesel. To obtain the fraction of diesel in the biodiesel
   (:math:`f_g`), let :math:`BP` be the value for "biodieselPercent", then :math:`f_g = 1 - \frac{BP}{100}`. :math:`BP`
   is set to a default value of :math:`20\%`.

The formula for :math:`\text{CH}_4` and :math:`\text{N}_2\text{O}` emissions, denoted :math:`Emission_{a,\, b,\, t}` is:

.. math::

   Emission_{a,\, b,\, t} = Fuel_{a,\, b,\, t} \cdot EF_{a,\, b,\, t}

where :math:`a` is the fuel type, where :math:`b` is the vehicle type, :math:`t` is the vehicle make year,
:math:`Fuel_{a,\, b,\, t}` is the fuel usage and :math:`EF_{a,\, b,\, t}` is the emission factor (for either
:math:`\text{CH}_4` or :math:`\text{N}_2\text{O}`). This is derived from Equation 3.2.4 from [IPCC2006V2CH3]_, but ignores
the emission control technology dependency and adds a vehicle make year dependency :math:`t`. Note that if the emission
factor for a vehicle type/fuel type combination does not depend on a vehicle make year then the user input year (which
can be entered) is ignored.


For mobile sources, the :math:`Total \text{CO}_2\; Equivalent\; Emissions_{GHG,\, fuel}` and
:math:`Total\; Biomass\; \text{CO}_2\; Equivalent\; Emissions_{biofuel}` in metric tons are calculated.
The formulas are:

.. math::

    Total\; \text{CO}_2\; Equivalent\; Emissions_{GHG,\, fuel} = \sum_{n=1}^{\infty} Emissions_{GHG,\, fuel, n} \cdot EF_{GHG}


where :math:`Total\; \text{CO}_2\; Equivalent\; Emissions_{GHG, fuel}` is the sum of all :math:`GHG` emissions by
either vehicle type (on road or non road), :math:`Emissions_{GHG,\, fuel}` are emissions of any :math:`GHG`
(:math:`\text{CO}_2`, :math:`\text{CH}_4`, and :math:`\text{N}_2\text{O}`),
and :math:`EF_{GHG}` is the emission factor for that :math:`GHG` to convert it into :math:`\text{CO}_2\;`.
Note that in atomic6, those emissions with units of grams are converted into kilograms, then the final value of this
calculation is divided by :math:`1000` to convert this value into :math:`metric \; tons`.

.. math::

    Total\; Biomass\; \text{CO}_2\; Equivalent\; Emissions_{biofuel} = \sum_{n=1}^{\infty} Fuel\; Usage_{biofuel}\; \cdot EF_{biofuel}\; \cdot Percent_{biofuel}

These equations are derived from Equation 2.2 from [IPCC2006V2CH3]_.

where :math:`biofuel` is either ethanol or biodisel, :math:`Fuel\; Usage_{biofuel}` is the amount of that
:math:`biofuel` used during the reporting period, :math:`EF_{biofuel}` is the emission factor for that :math:`biofuel`,
and :math:`Percent_{biofuel}` is the percent of that :math:`biofuel` that is mixed with petroleum fuel (disel or
gasoline).
Note that in atomic6, the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.


.. [IPCC2006V2CH3] IPCC, 2006: 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 2: Energy, Chapter 3: Mobile Combustion, pp. 12-13

Refrigeration and AC
--------------------
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
~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~

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


Fire Suppression
----------------
Fire Suppression calculates emissions for fire suppressant gas use. There are three different carbon accounting methods
employed in the final formula to calculate :math:`\text{CO}_2\; Equivalent\; Emissions` , and all three can be
utilized simultaneously if need be.

The EPA's SGEC workbook employs three methods for calculating emissions in Fire Suppression: material balance,
simplified material balance, and screening method.

Material Balance
~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~

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

Purchased Gases
---------------
Purchased gases calculates the carbon content (or emission factor) for some complex purchased gas streams. These complex gas streams include:

.. csv-table::
    :file: ./purchased_gases.csv
    :header-rows: 1

The fundamental calculations for each purchased gas Component are their

.. math::
   \text{CO}_2\; Equivalent\; Emissions_{gas} = GWP_{gas} * Purchased Amount_{gas}

These equations are derived from Equation 4 from [EPA2016DirectEmissionsfromStationaryCombustionSources]_.

where :math:`\text{CO}_2\; Equivalent\; Emissions_{gas}` is the total CO2 equivalent in merit unit pounds, :math:`GWP_{gas}`
is the global warming potential for that gas.


For purchased gases, the :math:`\text{CO}_2\; Equivalent\; Emissions_{gas}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{gas} = \sum_{n=1}^{\infty} \text{CO}_2\; Equivalent\; Emissions_{gas}

This equation is derived from [EPA2016DirectEmissionsfromStationaryCombustionSources]_.

where :math:`gas` is the purchased gas.
Note that in atomic6 the final value of this calculation is multiplied by :math:`kilogram\; per\; pound` to convert this
value from :math:`lbs` to :math:`kilograms` then divided by :math:`1000` to convert this value into
:math:`metric \; tons`.


.. [EPA2016DirectEmissionsfromStationaryCombustionSources] EPA, 2016: 2016 EPA Greenhouse Gas Inventory Guidance, Direct Emissions from Stationary Combustion Sources, pp. 11


Waste Gases
-----------
Waste Gases calculates the carbon content (or emission factor) for some complex waste gas streams. These complex waste gas streams include:

.. csv-table::
    :file: ./waste_gases.csv
    :header-rows: 1


The fundamental calculations for each waste gas Component are their :math:`Total\; Moles_{a}`,
:math:`Carbon\; Content_{a}`.
The formulas are:


.. math::

    Total\; Moles_{a} = Molar\; Fraction_{a} \cdot Oxidation\; Factor

where :math:`Total\; Moles_{a}` is the Molar concentration of gas :math:`a`, the :math:`Molar\; Fraction_{a}` is the molar fraction
of gas :math:`a`, and :math:`Oxidation\; Factor` is the percentage of carbon that is actually oxidized when combustion occurs.

.. math::

    Carbon\; Content_{a} = Total\; Moles{a} \cdot Molecular\; Weight_{a} \cdot Percent\; Carbon_{a}

These equations are derived from Equation 4 from [EPA2016DirectEmissionsfromStationaryCombustionSources]_.

where :math:`Carbon\; Content_{a}` is the amount of carbon produced from gas :math:`a`, :math:`Total\; Moles_{a}` is the Molar concentration of gas :math:`a`,
:math:`Molecular\; Weight_{a}` is the molecular weight of gas component :math:`a`, and :math:`Percent\; Carbon_{a}` is the carbon
fraction of gas :math:`a`


For waste gases, the :math:`\text{CO}_2\; Equivalent\; Emissions` in metric tons is calculated. The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_ = Total\; Carbon\; Content\; for\; All\; Components_ \cdot Oxidation\; Factor \cdot Atomic\; Weight\; of\; Carbon \cdot Molar\; Concentration

This equation is derived from Equation 5 from [EPA2016DirectEmissionsfromStationaryCombustionSources]_.

where :math:`Total\; Carbon\; Content\;` is the sum of all the carbon contents for all gas components,
:math:`Oxidation\; Factor` is the percentage of carbon that is actually oxidized when combustion occurs,
:math:`Atomic\; Weight\; of\; Carbon` is the natural atomic weight of carbon gas, and :math:`Molar\; Concentration` is
the gas total number of moles per unit volume.
Note that in atomic6 the final value of this calculation is multiplied by :math:`kilogram\; per\; pound` to convert this
value from :math:`lbs` to :math:`kilograms` then divided by :math:`1000` to convert this value into :math:`metric \; tons`.

.. [EPA2016DirectEmissionsfromStationaryCombustionSources] EPA, 2016: 2016 EPA Greenhouse Gas Inventory Guidance, Direct Emissions from Stationary Combustion Sources, pp. 11


Electricity
-----------
Electricity allows for inputs of purchased electricity quantities for the following eGrid subregions with units of kWh:

.. csv-table::
    :file: ./electricity.csv
    :header-rows: 1


The fundamental calculation for each eGrid subregion are their :math:`Market\; Based\; \text{CO}_2`,
:math:`Market\; Based\; \text{CH}_4`, :math:`Market\; Based\; \text{N}_2\text{O}` emissions and their
:math:`Location\; Based\; \text{CO}_2`, :math:`Location\; Based\; \text{CH}_4`,
:math:`Location\; Based\; \text{N}_2\te
xt{O}` emissions associated with the electricity purchased.
The formulas are:


.. math::

    Market\; Based\; Emissions_{electricity, eGrid\, subregion} = Electricity\; Purchased_{electricity} \cdot Market\; Based\; Emission\; Factor_{eGrid\, subregion}

.. math::

    Location\; Based\; Emissions_{electricity, eGrid\, subregion} = Electricity\; Purchased_{electricity} \cdot Location\; Based\; Emission\; Factor_{eGrid\, subregion}


This equation is derived from Equation 1 from [EPA2020IndirectEmissionsfromPurchasedElectricity]_.

where :math:`Electricity\; Purchased_{electricity}` is converted into watts, the default
:math:`Location\; Based\; Emission\; Factor_{eGrid\ subregion}` value is the emission factor for that
eGrid Subregion and fuel type if no :math:`Location\; Based\; Emission\; Factor_{eGrid\ subregion}` value is
input by the user, and the default :math:`Market\; Based\; Emission\; Factor_{eGrid\ subregion}` value is
the :math:`Location\; Based\; Emission\; Factor_{eGrid\ subregion}` if no
:math:`Market\; Based\; Emission\; Factor_{eGrid\ subregion}` value is input by the user.

For electricity, the :math:`\text{CO}_2\; Equivalent\; Emissions_{method}` in metric tons is calculated based on the
Total\; Emissions\; for\; All\; Sources_{method, GHG}. The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{method, GHG} = \sum_{n=1}^{\infty} Total\; Emissions\; for\; All\; Sources_{method, GHG} \cdot GWP_{GHG}

This equation is derived from Equation 2.2 from [EPA2020IndirectEmissionsfromPurchasedElectricity]_.

where :math:`Total\; Emissions\; for\; All\; Sources_{method, GHG}` are the sums of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`method` (either
:math:`location\; based` or :math:`market\; based`), and :math:`GWP_{GHG}` is the global warming potential of that
:math:`GHG`.
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.

.. [EPA2020IndirectEmissionsfromPurchasedElectricity] EPA, 2020: 2020 EPA Greenhouse Gas Inventory Guidance, Indirect Emissions from Purchased Electricity, pp. 3

Steam
------
Steam allows for inputs of purchased steam quantities for the following fuel types with units of MMBtu:

.. csv-table::
    :file: ./steam.csv
    :header-rows: 1


The fundamental calculation for each fuel type are their :math:`Location\; Based\; \text{CO}_2`,
:math:`Location\; Based\; \text{CH}_4`, :math:`Location\; Based\; \text{N}_2\text{O}` emissions and their
:math:`Market\; Based\; \text{CO}_2`, :math:`Market\; Based\; \text{CH}_4`, :math:`Market\; Based\; \text{N}_2\text{O}`
emissions associated with the steam purchased and based on boiler efficiency.
The formulas are:

.. math::

   Location\; Based\; Emissions_{GHG,\, fuel} = \frac{Steam\; Purchased_{fuel} \cdot Location\; Based\; Emission\; Factor_{GHG,\, fuel}}{Boiler\; Efficiency}

.. math::

    Market\; Based\; Emissions_{GHG,\, fuel} = \frac{Steam\; Purchased_{fuel} \cdot Market\; Based\; Emission\; Factor_{GHG,\, fuel}}{Boiler\; Efficiency}


This equation is derived from Equation 2.1 from [IPCC2006V2CH2]_ (see Stationary Combustion), with accounting for :math:`Boiler\; Efficiency`.

where the default :math:`Boiler\; Efficiency` value is 80% if no :math:`Boiler\; Efficiency` value is input by the user,
the default :math:`Location\; Based\; Emission\; Factor_{GHG,\, fuel}` value is the emission factor for that fuel
type if no :math:`Location\; Based\; Emission\; Factor_{GHG,\, fuel}` value is input by the user,
and the default :math:`Market\; Based\; Emission\; Factor_{GHG,\, fuel}` value is the
:math:`Location\; Based\; Emission\; Factor_{GHG,\, fuel}` if no :math:`Market\; Based\; Emission\; Factor_{GHG,\, fuel}`
value is input by the user.

For steam, the :math:`\text{CO}_2\; Equivalent\; Emissions_{method}` in metric tons is calculated based on the
Total\; Emissions\; for\; All\; Sources_{method, GHG}. The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{method, GHG} = \sum_{n=1}^{\infty} Total\; Emissions\; for\; All\; Sources_{method, GHG} \cdot GWP_{GHG}

This equation is derived from Equation 2.2 from [IPCC2006V2CH2]_.

where :math:`Total\; Emissions\; for\; All\; Sources_{method, GHG}` are the sums of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`method` (either
:math:`location\; based` or :math:`market\; based`), and :math:`GWP_{GHG}` is the global warming potential of that
:math:`GHG`.
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.


Business Travel
---------------
Business Travel calculates emissions from business travel of employees. There are three different tables and
therefore three different methods to calculate emissions from employee business travel. The first is for those employees
traveling by car, the second is for those employees traveling by rail or bus, and third one is for those employee
traveling by air.

Business Travel allows for inputs of personal vehicle types for the following vehicle types:

.. csv-table::
    :file: ./commuting_personal_vehicle.csv
    :header-rows: 1

Business Travel allows for inputs of public transportation types for the following public transport types:

.. csv-table::
    :file: ./commuting_public_transportation.csv
    :header-rows: 1

Business Travel allows for input of flight length types for the following flight length types:

.. csv-table::
    :file: ./business_travel_air.csv
    :header-rows: 1

The fundamental calculation for each vehicle type, public transport type, flight length for personal vehicle,
public transport, and flight length business travel are their :math:`\text{CO}_2`, :math:`\text{CH}_4`, and
:math:`\text{N}_2\text{O}` emissions associated with the vehicle type or flight length and based on the vehicle miles traveled.

The formulas are:

.. math::

   Travel\; Emissions_{travel\ mode, \, T} = Travel_{travel\, mode} \cdot EF_{T}

This equation is derived from Equation 1 from [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport]_.

where :math:`Travel\; Emissions_{travel\ mode, \, T}` is the mass of :math:`\text{CO}_2`, :math:`\text{CH}_4`,
or :math:`\text{N}_2\text{O}`4` emitted, :math:`Travel_{travel\, mode}` is the travel distance in miles for a
specific travel mode, which can be vehicle miles traveled, passenger miles traveled or flight length for personal vehicle
, public transportation or flight respectively and :math:`EF_{T}` is the travel :math:`\text{CO}_2`, :math:`\text{CH}_4`,
or :math:`\text{N}_2\text{O}` emission factor which is based on the type of personal vehicle, public transport
or air travel.

For business travel, the :math:`\text{CO}_2\; Equivalent\; Emissions_{GHG, transport}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{GHG, transport} = \sum_{n=1}^{\infty} Total\; Emissions_{GHG, transport} \cdot GWP_{GHG}

This equation is derived from [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport]_.

where :math:`Total\; Emissions_{GHG, transport}` is the sum of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`transport`
(either personal vehicle, public transportation, or air travel), and :math:`GWP_{GHG}` is the
global warming potential of that :math:`GHG`.
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.

Commuting
---------
Commuting calculates emissions from transportation of employees to and from work. There are two different tables and
therefore two different methods to calculate emissions from employee commuting. The first is for those employees who
commute via of personal vehicle, the second is for those employees who commute via public transportation.

Commuting allows for inputs of personal vehicle types for the following vehicle types:

.. csv-table::
    :file: ./commuting_personal_vehicle.csv
    :header-rows: 1

Commuting allows for inputs of public transportation types for the following public transport types:

.. csv-table::
    :file: ./commuting_public_transportation.csv
    :header-rows: 1


The fundamental calculation for each vehicle type or public transport type for personal vehicle and public transport
commuting are their :math:`\text{CO}_2`, :math:`\text{CH}_4`, and :math:`\text{N}_2\text{O}` emissions associated
with the vehicle type and based on the vehicle miles traveled.

The formulas are:

.. math::

   Travel\; Emissions_{travel\, mode, T} = Travel_{travel\, mode} \cdot EF_{T}

This equation is derived from Equation 1 from [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport]_.

where :math:`Travel\; Emissions_{travel\, mode, T}` is the mass of :math:`\text{CO}_2`, :math:`\text{CH}_4`,
or :math:`\text{N}_2\text{O}`4` emitted, :math:`Travel_{travel\, mode}` is the travel distance in miles for a
specific travel mode, which is either vehicle miles traveled or passenger miles traveled for personal vehicle
or public transportation respectively and :math:`EF_{T}` is the travel :math:`\text{CO}_2`, :math:`\text{CH}_4`,
or :math:`\text{N}_2\text{O}` emission factor which is based on the type of personal vehicle or public transport method.

For commuting, the :math:`\text{CO}_2\; Equivalent\; Emissions_{GHG, transport}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{GHG, transport} = \sum_{n=1}^{\infty} Total\; Emissions_{GHG, transport} \cdot GWP_{GHG}

This equation is derived from [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport]_.

where :math:`Total\; Emissions_{GHG, transport}` is the sum of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`transport`
(either personal vehicle or public transport), and :math:`GWP_{GHG}` is the
global warming potential of that :math:`GHG`.
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.

Product Transport
-----------------
Product Transport calculates emissions from transportation of products. There are two different tables and
therefore two different methods to calculate emissions from employee commuting. The first is for those products which
are transported over vehicle miles, the second is for those products which are transported over ton miles.

Product Transport allows for inputs of vehicle types for the calculation over vehicle miles for the following vehicle types:

.. csv-table::
    :file: ./product_transport_vehicle_miles.csv
    :header-rows: 1

Product Transport allows for inputs of vehicle types for the calculation over ton miles for the following vehicle types:

.. csv-table::
    :file: ./product_transport_ton_miles.csv
    :header-rows: 1


The fundamental calculation for each vehicle type for vehicle miles and ton miles
are their :math:`\text{CO}_2`, :math:`\text{CH}_4`, and :math:`\text{N}_2\text{O}` emissions associated
with the vehicle type and based on the vehicle miles or ton miles traveled, respectively.

The formulas are:

.. math::

   Emissions_{units,\; gas,\; vehicle\; type} = Vehicle\; Miles\; Traveled_{unit} \cdot EF_{gas,\; vehicle\; type}

This equation is derived from Equation 5 from [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport]_.

where :math:`Emissions_{unit, gas, vehicle\; type}` is the mass of :math:`\text{CO}_2`, :math:`\text{CH}_4`,
or :math:`\text{N}_2\text{O}` emitted, :math:`Vehicle\; Miles\; Traveled_{units}` is the travel distance in
:math:`units` (vehicle miles or ton miles), and :math:`EF_{gas, vehicle\; type}` is the product transport
emission factor of that :math:`gas` (:math:`\text{CO}_2`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`)
which is based on the :math:`vehicle\; type`.

For product transport, the :math:`\text{CO}_2\; Equivalent\; Emissions_{GHG, transport}` in metric tons is calculated.
The formula is:


.. math::

    \text{CO}_2\; Equivalent\; Emissions_{GHG, transport} = \sum_{n=1}^{\infty} Total\; Emissions_{GHG, transport} \cdot GWP_{GHG}

This equation is derived from Equation 5 from [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport]_.

where :math:`Total\; Emissions_{GHG, transport}` is the sum of all the emissions for that
:math:`GHG` (:math:`\text{CO}_2\;`, :math:`\text{CH}_4`, or :math:`\text{N}_2\text{O}`) and :math:`transport`
(either vehicle miles or ton miles), and :math:`GWP_{GHG}` is the global warming potential of that :math:`GHG`.
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.


.. [EPA2008OptionalEmissionsfromCommutingBusinessTravelandProductTransport] EPA, 2008: 2008 EPA Greenhouse Gas Inventory Protocol Core Module Guidance Optional Emissions from Commuting, Business Travel and Product Transport, pp. 10


Waste
-----
The fundamental calculation for Waste is the :math:`\text{CO}_2\; Equivalent\; Emissions` emissions produced by the
disposal of waste materials based on the :math:`Disposal Method` and :math:`weight`.

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
Note that in atomic6 the final value of this calculation is divided by :math:`1000` to convert this value into
:math:`metric \; tons`.


.. [IPCC2006V5CH3] IPCC, 2006: 2006 IPCC Guidelines for National Greenhouse Gas Inventories, Volume 5, IPPU, Chapter 3, Solid Waste Disposal, pp. 9



Offsets
-------
Offsets calculates the total purchased :math:`\text{CO}_2` offsets by summing up the inputs of offsets purchased.

The fundamental calculation for offsets is their :math:`\text{CO}_2\; Equivalent\; Emission\; Reductions`

The formulas is:

.. math::

    \text{CO}_2\; Equivalent\; Emission\; Reductions = \sum_{n=1}^{\infty} Purchased\; Offset_{n}

where :math:`Purchased\; Offset_{n}` is the amount of offsets that have been purchased during the reporting period for
one entry in the offsets table.