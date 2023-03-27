from policyengine_us.model_api import *


class childcare_deduction(Variable):
    value_type = float
    entity = SPMUnit
    label = "Maryland TANF childcare deduction"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.MD

    def formula(spm_unit, period, parameters):
        # Get earned income for the SPM unit.
        earned_income = add(spm_unit, period, ["earned_income"])
        # Determine if the SPM unit has any self-employment income.
        self_employment_income = add(
            spm_unit, period, ["self_employment_income"]
        )
        # Get the policy parameters.

        p = parameters(period).gov.states.md.tanf.income.deductions.earned
        childcare_deduction = select(
            # First arg: self employed or not
            [earned_income>0, self_employment_income>0],
            # Second arg: multiply by the percent deduction (0.2, 0.5)
            [earned_income * p.new, self_employment_income * p.self_employed],
            # Third arg: default value to return if none of the conditions are True
            default=0,
        )
        # Return if initially eligible
        return childcare_deduction
