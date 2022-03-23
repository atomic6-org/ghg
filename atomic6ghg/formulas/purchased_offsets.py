"""" Purchased offsets"""
# pylint: disable=no-name-in-module
import logging

from atomic6ghg.formulas import Formula, null_replacer

logger = logging.getLogger(__name__)


class PurchasedOffsets(Formula):
    """ Calculate emissions savings from purchased offsets """

    def __init__(self, wks_data=None):
        super().__init__(wks_data=wks_data)
        self.recalc(self.wks_data)

    def recalc(self, wks_data: dict) -> dict:
        """Execute recalc procedure for purchased offsets"""
        self.wks_data = wks_data

        self.make_purchased_offsets()
        self.make_co2_equivalent_emissions()

        return self.to_dict()

    def make_purchased_offsets(self):
        """Tabulate project level offsets across all projects into the value purchasedOffsets"""
        self._total_emissions['sumOfPurchasedOffsets'] = 0.

        for project in self.wks_data['purchasedOffsets']:
            project_offset = null_replacer(project['purchasedOffset'])
            self._total_emissions['sumOfPurchasedOffsets'] += project_offset

    def make_co2_equivalent_emissions(self):
        """ Transform total purchased offsets and present as a negative value """
        self._output['totalPurchasedOffsets'] = -self._total_emissions['sumOfPurchasedOffsets']
