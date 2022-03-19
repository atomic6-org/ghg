
.. _mobile-sources-api:

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
