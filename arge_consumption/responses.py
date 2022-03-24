from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

# 3rd party
from pydantic import BaseModel, Field, conint, constr


class BillingUnitNumberMSC(BaseModel):
    __root__: constr(min_length=1, max_length=9) = Field(
        ...,
        description="The identifier of a billing unit defined by the MSC.",
        example="123456789",
    )


class BillingUnitReference(BaseModel):
    mscnumber: BillingUnitNumberMSC
    pmnumber: Optional[constr(min_length=1, max_length=20)] = Field(
        None,
        description="The identifier of a billing unit defined by the PM.",
        example="XY-12345-00",
    )


class PeriodId(BaseModel):
    __root__: constr(regex=r"^\d{4}-\d{2}$") = Field(
        ...,
        description="Identifier of a consumption period with year and month.",
        example="2021-06",
    )


class ResidentialUnitReference(BaseModel):
    mscnumber: constr(min_length=1, max_length=4) = Field(
        ...,
        description="The identifier of a residential unit defined by the MSC.",
        example="0001",
    )
    pmnumber: Optional[constr(min_length=1, max_length=20)] = Field(
        None,
        description="The identifier of a residential unit defined by the PM.",
        example="XY-12345-00-R1",
    )


class Service(Enum):
    HEATING = "HEATING"
    HOT_WATER = "HOT_WATER"
    COOLING = "COOLING"
    COLD_WATER = "COLD_WATER"


class UnitOfMeasure(Enum):
    """
    Hot water is measured in m^3
    Heating is measured in HCU (bei Heizkostenverteilern) oder kWh (Wärmemengenzähler)
    """

    KWH = "KWH"
    HCU = "HCU"
    M3 = "M3"


class Year(BaseModel):
    __root__: conint(ge=1900, le=9999) = Field(
        ..., description="Data type for year information."
    )


class Benchmark(BaseModel):
    service: Service
    unitofmeasure: UnitOfMeasure
    amount: float = Field(..., description="The benchmark amount.", example="80.0")


class Consumption(BaseModel):
    """

    Attributes:
        service:
            „Service“ ist die Definition für die ausgewiesene Bemessungsart, also ob "Heizung" oder "Warmwasser"

        unitofmeasure:
            Das Attribut „unitofmeasure“ definiert die Maßeinheit zur Bemessungsart „Service“.

            Nach der Novellierung der HKVO soll diese in „kWh“ ausgewiesen werden. Bislang stand die Arge in Abstimmung, wie diese Anforderung einheitlich umgesetzt werden kann.
            Einen Produktivnahmetermin kann ista momentan leider noch nicht nennen. Alle bis dahin vergangenen Monate mit der gesetzlichen Verpflichtung, werden nachträglich mit „KWh“ aufbereitet. Bis zu diesem Zeitpunkt werden die Einheiten in dem derzeitig gemessenen Format ausgegeben.

            Also
            · Hot Water in m³
            · Heating in Einheiten (HCU bei Heizkostenverteilern) oder kWh (Wärmemengenzähler)
    """

    service: Service
    unitofmeasure: UnitOfMeasure
    amount: Optional[float] = Field(
        None,
        description="The actual consumption amount in case no errors are present, related to `unitofmeasure`.",
        example="99.03",
    )
    converted: bool = Field(
        ...,
        description="True if the amount is converted from another unit of measure.\n\nThis applies e.g. when consumption measured in `HCU` is converted to `KWH`\nas required by the German HeizkostenV regulations.\n",
        example="false",
    )
    estimated: bool = Field(
        ..., description="True if this is an estimated consumption.", example="true"
    )
    errors: bool = Field(
        ...,
        description="True if errors occurred and no consumption can be presented.",
        example="false",
    )


class ConsumptionDataResidentialUnit(BaseModel):
    reference: ResidentialUnitReference
    consumptions: List[Consumption] = Field(
        ...,
        description="Consumption values for different services and measurement units.",
    )
    benchmarks: Optional[List[Benchmark]] = Field(
        None, description="Benchmarks for different services."
    )


class ConsumptionSummaryPeriod(BaseModel):
    period: PeriodId
    update: datetime = Field(
        ..., description="The timestamp of the last data update for this period."
    )


class ConsumptionDataBillingUnit(BaseModel):
    reference: BillingUnitReference
    period: PeriodId
    residentialunits: List[ConsumptionDataResidentialUnit] = Field(
        ..., description="List of consumption data on residential unit level."
    )


class ConsumptionSummaryBillingUnit(BaseModel):
    reference: BillingUnitReference
    periods: List[ConsumptionSummaryPeriod] = Field(
        ...,
        description="Overview of available consumption periods and their last update.",
    )


class ConsumptionData(BaseModel):
    billingunit: ConsumptionDataBillingUnit


class ConsumptionSummary(BaseModel):
    billingunit: ConsumptionSummaryBillingUnit
