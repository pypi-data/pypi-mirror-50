# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2019 SerialLab Corp.  All rights reserved.
from quartet_masterdata.models import Company, Location, TradeItem


class DBProxy:
    """
    Performs common database operations.
    """

    def get_epcis_master_data_locations(self, sgln_list: []):
        """
        Will create a list of vocabulary elements for gs1 locations
        :return: A dictionary with the key being the sgln and a dictionary
        as the value.
        """
        db_records = {}
        for sgln in sgln_list:
            location = self._partner_by_sgln(sgln=sgln)
            if location and len(location) > 0:
                # there will only ever be one
                db_records[sgln] = location[0]
        return db_records

    def _partner_by_sgln(self, sgln: str):
        qd = Company.objects.filter(SGLN=sgln)
        partner = None
        if qd.exists():
            partner = qd.values()
        else:
            qd = Location.objects.filter(SGLN=sgln)
            if qd.exists():
                partner = qd.values()
        return partner

    def get_company_prefix_length(self, gtin14: str) -> int:
        """
        Uses the GTIN 14 to look up the company prefix in the trade items
        table.
        :param gtin14: The gtin
        :return: The length of the company prefix record.
        """
        try:
            trade_item = TradeItem.objects.select_related().get(
                GTIN14=gtin14)
            if trade_item.NDC:
                company_prefix_length = 2 + len(trade_item.NDC.split('-')[0])
            else:
                company_prefix_length = len(
                    trade_item.company.gs1_company_prefix)
        except TradeItem.DoesNotExist:
            raise self.TradeItemConfigurationError(
                'There is no trade item and corresponding company defined '
                'for gtin %s.  This must be defined '
                'in order for the system to '
                'determine company prefix length. '
                'Make sure you have a trade item configured and assigned to '
                'a company that has a valid gs1 company prefix entry.' %
                gtin14
            )
        return company_prefix_length

    class TradeItemConfigurationError(Exception):
        pass
