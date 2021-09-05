# `cesurvey`
Python package for working with the US Consumer Expenditure Survey

# Installation

```shell
pip install git+https://github.com/PSLmodels/cesurvey
```


# Example usage

```python
import numpy as np
def compare(est, benchmark):
    print(f"The estimate is {np.round(est, 2)}")
    print(f"The published value is is {benchmark}")
    print(f"The rel error is {np.round(100 * (est - benchmark) / benchmark, 2)}%")

import cesurvey

fmli_2019 = cesurvey.get_interview_data(2019)

lku = cesurvey.get_data_dictionary()  # A tuple of variable and code lookups

income_bf_tax_2019 = cesurvey.estimate_annual_quantity("FINCBTXM", fmli_2019,
                                                       "demographics")
compare(income_bf_tax_2019, 82852)

tot_expenditures = cesurvey.estimate_annual_quantity("TOTEXPPQ", fmli_2019,
                                                     "expense")
compare(tot_expenditures, 63036)
food_expenditures = cesurvey.estimate_annual_quantity("FOODPQ", fmli_2019,
                                                      "expense")
compare(food_expenditures, 8169)

food_at_home = cesurvey.estimate_annual_quantity("FDHOMEPQ", fmli_2019,
                                                 "expense")
compare(food_at_home, 4643)

food_away = cesurvey.estimate_annual_quantity("FDAWAYPQ", fmli_2019,
                                                 "expense")
compare(food_away, 3526)

alcohol = cesurvey.estimate_annual_quantity("ALCBEVPQ", fmli_2019,
                                            "expense")
compare(alcohol, 579)

housing = cesurvey.estimate_annual_quantity("HOUSPQ", fmli_2019,
                                            "expense")
compare(housing, 20679)

shelter = cesurvey.estimate_annual_quantity("SHELTPQ", fmli_2019,
                                            "expense")
compare(shelter, 12190)

owned_dwellings = cesurvey.estimate_annual_quantity("OWNDWEPQ", fmli_2019,
                                                    "expense")
compare(owned_dwellings, 6797)

rented_dwellings = cesurvey.estimate_annual_quantity("RENDWEPQ", fmli_2019,
                                                     "expense")
compare(rented_dwellings, 4432)

other_lodging = cesurvey.estimate_annual_quantity("OTHLODPQ", fmli_2019,
                                                  "expense")
compare(other_lodging, 961)

utilies_fuels_public_services = cesurvey.estimate_annual_quantity(
    "UTILPQ", fmli_2019, "expense"
)
compare(utilies_fuels_public_services, 4055)

hsld_ops = cesurvey.estimate_annual_quantity("HOUSOPPQ", fmli_2019,
                                             "expense")
compare(hsld_ops, 1570)
# Household supply candidates: MISCEQCQ, OTHHEXCQ
hsld_supplies = cesurvey.estimate_annual_quantity("OTHHEXPQ", fmli_2019,
                                                  "expense")
compare(hsld_supplies, 766)

hsld_furnish_equip = cesurvey.estimate_annual_quantity("HOUSEQPQ", fmli_2019,
                                                       "expense")
compare(hsld_furnish_equip, 2098)

apparel_and_services = cesurvey.estimate_annual_quantity("APPARPQ", fmli_2019,
                                                         "expense")
compare(apparel_and_services, 1883)

transportation = cesurvey.estimate_annual_quantity("TRANSPQ", fmli_2019,
                                                         "expense")
compare(transportation, 10743)

used_car = cesurvey.estimate_annual_quantity("CARTKUPQ", fmli_2019,
                                             "expense")
new_car = cesurvey.estimate_annual_quantity("CARTKNPQ", fmli_2019,
                                            "expense")
compare(used_car + new_car, 4394)

gas_motor_oil = cesurvey.estimate_annual_quantity("GASMOPQ", fmli_2019,
                                                   "expense")
compare(gas_motor_oil, 2094)

vehicles_rent_lease = cesurvey.estimate_annual_quantity("VRNTLOPQ", fmli_2019,
                                                        "expense")
vehicle_insurance = cesurvey.estimate_annual_quantity("VEHINSPQ", fmli_2019,
                                                        "expense")
vehicle_maintenance = cesurvey.estimate_annual_quantity("MAINRPPQ", fmli_2019,
                                                        "expense")
compare(vehicles_rent_lease + vehicle_insurance + vehicle_maintenance, 3474)

public_other_trans = cesurvey.estimate_annual_quantity("PUBTRAPQ", fmli_2019,
                                                       "expense")
compare(public_other_trans, 781)

```
