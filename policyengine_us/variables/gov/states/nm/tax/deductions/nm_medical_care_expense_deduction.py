from policyengine_us.model_api import *
import numpy as np


class nm_mediacal_care_expense_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "NM medical care expense deduction"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://klvg4oyd4j.execute-api.us-west-2.amazonaws.com/prod/PublicFiles/34821a9573ca43e7b06dfad20f5183fd/856ebf4b-3814-49dd-8631-ebe579d6a42b/Personal%20Income%20Tax.pdf"
    ) # 7-2-35. DEDUCTION – UNREIMBURSED OR UNCOMPENSATED MEDICAL CARE EXPENSES Page 237
    defined_for = StateCode.NM

    def formula(tax_unit, period, parameters):
        rates = parameters(
            period
        ).gov.states.nm.tax.income.deductions.medical_care_expense
        filing_status = tax_unit("filing_status", period)
        statuses = filing_status.possible_values
        agi = tax_unit("adjusted_gross_income", period)
        expenses = add(
            tax_unit,
            period,
            ["medical_out_of_pocket_expenses"],
        )
        return select(
            [
                filing_status == statuses.SINGLE,
                filing_status == statuses.JOINT,
                filing_status == statuses.HEAD_OF_HOUSEHOLD,
                filing_status == statuses.SEPARATE,
                filing_status == statuses.WIDOW,
            ],
            [
                rates.single.calc(agi) / agi * expenses,
                rates.joint.calc(agi) / agi * expenses,
                rates.head_of_household.calc(agi) / agi * expenses,
                rates.separate.calc(agi) / agi * expenses,
                rates.widow.calc(agi) / agi * expenses,
            ],
        )
