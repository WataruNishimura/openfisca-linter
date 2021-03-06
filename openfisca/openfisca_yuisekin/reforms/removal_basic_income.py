"""
This file defines a reform.

A reform is a set of modifications to be applied to a reference tax and benefit system to carry out experiments.

See https://openfisca.org/doc/key-concepts/reforms.html
"""

# Import from openfisca-core the Python objects used to code the legislation in OpenFisca
from openfisca_core.reforms import Reform


class removal_ベーシックインカム(Reform):
    def apply(self):
        """
        Apply reform.

        A reform always defines an `apply` method that builds the reformed tax and benefit system from the reference one.
        See https://openfisca.org/doc/coding-the-legislation/reforms.html#writing-a-reform

        Our reform neutralizes the `ベーシックインカム` variable. When this reform is applied, calculating `ベーシックインカム` will always return its default value, 0.
        """
        self.neutralize_variable("ベーシックインカム")
