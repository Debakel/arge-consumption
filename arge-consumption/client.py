import os

import requests as requests
from requests.auth import HTTPBasicAuth
from responses.consumption import ConsumptionResponse
from responses.periods import PeriodResponse


class HaweikoClient:
    def __init__(self, url: str, user: str, password: str):
        self.url = url
        self.auth = HTTPBasicAuth(user, password)

    @staticmethod
    def instance():
        return HaweikoClient(
            url=os.getenv("HAWEIKO_API_URL"),
            user=os.getenv("HAWEIKO_API_USER"),
            password=os.getenv("HAWEIKO_API_PASSWORD"),
        )

    def _get(self, url):
        return requests.get(url, auth=self.auth)

    def get_periods(self, msc_number: int) -> PeriodResponse:
        """Liste der verfügbaren Zeiträume abrufen

        Mit dieser Operation können die verfügbaren Perioden für eine Liegenschaft abgerufen werden.

        Eine Periode stellt dabei immer den Verbrauch für einen Monat dar.
        Die Anzahl der bereitgestellten Perioden und der Zeitpunkt der Bereitstellung neuer Perioden muss mit dem
        jeweiligen WDU vereinbart werden.

        Grundsätzlich ist es möglich, dass Verbräuche rückwirkend korrigiert werden können. Der letzte Zeitpunkt
        eines Updates für eine Periode kann dem Attribut „update“ entnommen.
        werden.

        :param msc_number:
        """
        response = self._get(
            self.url + f"/billingunits/{msc_number}/consumptions/periods"
        )
        if not response.status_code == 200:
            raise Exception(
                f"Invalid status code ({response.status_code}): {response.content}"
            )
        return PeriodResponse.parse_obj(response.json())

    def get_consumptions(self, msc_number: int, period: str) -> ConsumptionResponse:
        """Liste der Verbräuche für eine Periode abrufen

        Mit dieser Operation können die Verbräuche aller Nutzeinheiten einer Liegenschaft für eine Periode abgefragt werden.

        Das WDU stellt je nach vertraglicher Vereinbarung folgende Verbräuche bereit.
        * Heizung in kWh
        * Heizung in Heizkostenverteiler-Einheiten
        * Kälte in kWh Warmwasser in m³
        * Kaltwasser in m³.

        Wird ein Verbrauch geschätzt, so ist dieser entsprechend gekennzeichnet.
        Ist eine Verbrauchsermittlung für einen vereinbarten Verbrauchstyp nicht möglich, wird für diesen
        Verbrauchstyp als Fehler gekennzeichnet
        """
        response = self._get(
            self.url + f"/billingunits/{msc_number}/consumptions/periods/{period}"
        )
        if not response.status_code == 200:
            raise Exception(
                f"Invalid status code ({response.status_code}): {response.content}"
            )
        return ConsumptionResponse.parse_obj(response.json())
