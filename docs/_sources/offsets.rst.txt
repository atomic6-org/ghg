
.. _offsets-api:

Offsets
-------
A `carbon offset` [EPA2018_offset]_ is a project that is a specific activity intended to reduce GHG emissions, increase
`carbon storage <glossary.html>`_, or enhance GHG removals from the atmosphere.
The offset can be used to address direct and indirect emissions associated with an organization's operations.

Class Documentation
************************
.. module:: atomic6ghg.formulas.purchased_offsets

.. autoclass:: PurchasedOffsets
    :members:
    :undoc-members:
    :inherited-members:

Example Usage
******************
Python example code usage:

.. code-block:: python

    from atomic6ghg.formulas import PurchasedOffsets
    offsets_input: dict = {
        "version": "purchased-offsets.1.0.0",
        "purchasedOffsets": [
            {"purchasedOffset": 500}
        ]
    }
    engine = PurchasedOffsets(offsets_input)
    outputs: dict = engine.to_dict()
    print(outputs.get('totalPurchasedOffsets'))

EPA Equation Analysis
**********************
Offsets calculates the total purchased :math:`\text{CO}_2` offsets by summing up the inputs of offsets purchased.

The fundamental calculation for offsets is their :math:`\text{CO}_2\; Equivalent\; Emission\; Reductions`

The formulas is:

.. math::

    \text{CO}_2\; Equivalent\; Emission\; Reductions = \sum_{n=1}^{\infty} Purchased\; Offset_{n}

where :math:`Purchased\; Offset_{n}` is the amount of offsets that have been purchased during the reporting period for
one entry in the offsets table.
Note that in atomic6 final values for offsets are converted into :math:`metric \; tons`.

.. [EPA2018_offset] `EPA & Green power partnership, Offsets and RECs <https://www.epa.gov/sites/default/files/2018-03/documents/gpp_guide_recs_offsets.pdf#page=3>`_