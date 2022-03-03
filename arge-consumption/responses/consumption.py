# generated by datamodel-codegen:
#   filename:  scratch_5.json
#   timestamp: 2022-03-01T14:35:18+00:00

from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Reference(BaseModel):
    mscnumber: str


class Reference1(BaseModel):
    mscnumber: str


class Consumption(BaseModel):
    service: str
    unitofmeasure: str
    amount: float
    converted: bool
    estimated: bool
    errors: bool


class Residentialunit(BaseModel):
    reference: Reference1
    consumptions: List[Consumption]
    benchmarks: List


class Billingunit(BaseModel):
    reference: Reference
    period: str
    residentialunits: List[Residentialunit]


class ConsumptionResponse(BaseModel):
    billingunit: Billingunit
