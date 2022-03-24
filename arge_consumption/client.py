import os

# 3rd party
import requests as requests
from requests.auth import HTTPBasicAuth

from arge_consumption import errors
from arge_consumption.responses import ConsumptionData, ConsumptionSummary


class HaweikoClient:
    """Client to retrieve EED consumption data from a ARGE HeiWaKo API.

    OpenAPI specification:
        https://app.swaggerhub.com/apis-docs/m.duchene/arge-consumption/1.1
    """

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
        response = requests.get(url, auth=self.auth)
        match response.status_code:
            case 200:
                return response
            case 401:
                raise errors.AutorizationFailure()
            case 403:
                raise errors.PermissionError()
            case 404:
                raise errors.NotFound()
            case 500:
                raise errors.TechnicalError()
            case 501:
                raise errors.UnsopportedOperation()
            case _:
                raise errors.UnsupportedResponse(
                    status_code=response.status_code, message=response.content
                )

    def get_periods(self, msc_number: int) -> ConsumptionSummary:
        """Liste der verfügbaren Zeiträume abrufen

        Mit dieser Operation können die verfügbaren Perioden für eine Liegenschaft abgerufen werden.

        Eine Periode stellt dabei immer den Verbrauch für einen Monat dar.
        Die Anzahl der bereitgestellten Perioden und der Zeitpunkt der Bereitstellung neuer Perioden muss mit dem
        jeweiligen WDU vereinbart werden.

        Grundsätzlich ist es möglich, dass Verbräuche rückwirkend korrigiert werden können. Der letzte Zeitpunkt
        eines Updates für eine Periode kann dem Attribut „update“ entnommen.
        werden.

        :param msc_number: Identifier der Liegenschaft
        """
        response = self._get(
            self.url + f"/billingunits/{msc_number}/consumptions/periods"
        )
        return ConsumptionSummary.parse_obj(response.json())

    def get_consumptions(self, msc_number: int, period: str) -> ConsumptionData:
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

        :param msc_number: Identifier der Liegenschaft
        :param period: Abrechnungsperiode im Format MM-YYYY
        """
        response = self._get(
            self.url + f"/billingunits/{msc_number}/consumptions/periods/{period}"
        )
        return ConsumptionData.parse_obj(response.json())
