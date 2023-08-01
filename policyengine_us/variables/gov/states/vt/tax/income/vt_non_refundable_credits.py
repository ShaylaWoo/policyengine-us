from policyengine_us.model_api import *


class vt_non_refundable_credits(Variable):
    value_type = float
    entity = TaxUnit
    label = "Vermont capped non-refundable tax credits"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.VT
