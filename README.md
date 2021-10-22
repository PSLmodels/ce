# `cesurvey`
Python package for working with the US Consumer Expenditure Survey

# Installation

```shell
pip install git+https://github.com/PSLmodels/cesurvey
```

# Example usage

```python
import numpy as np

import cesurvey

def compare(est, benchmark):
    """Convenience function to compare published CE estimates and estimated"""
    print(f"The estimate is {np.round(est, 2)}")
    print(f"The published value is is {benchmark}")
    print(f"The rel error is {np.round(100 * (est - benchmark) / benchmark, 2)}%")


fmli_2019 = cesurvey.get_interview_data(2019)

lku = cesurvey.get_data_dictionary()  # A tuple of variable and code lookups

# Replicating BLS Report from 2019 CE ------------------------------
# https://www.bls.gov/opub/reports/consumer-expenditures/2019/home.htm

income_bf_tax_2019 = cesurvey.estimate_annual_quantity("FINCBTXM", fmli_2019,
                                                       "demographics")
compare(income_bf_tax_2019, 82852)

tot_expenditures = cesurvey.estimate_annual_quantity("TOTEXPPQ", fmli_2019,
                                                     "expense")
compare(tot_expenditures, 63036)

food_expenditures = cesurvey.estimate_annual_quantity("FOODPQ", fmli_2019,
                                                      "expense")
compare(food_expenditures, 8169)

# Note how the differences in food_at_home and food_away offset each other
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

health_care = cesurvey.estimate_annual_quantity("HEALTHPQ", fmli_2019,
                                                "expense")
compare(health_care, 5193)

entertainment = cesurvey.estimate_annual_quantity("ENTERTPQ", fmli_2019,
                                                  "expense")
compare(entertainment, 3090)

personal_care = cesurvey.estimate_annual_quantity("PERSCAPQ", fmli_2019,
                                                  "expense")
compare(personal_care, 786)

reading = cesurvey.estimate_annual_quantity("READPQ", fmli_2019,
                                            "expense")
compare(reading, 92)

education = cesurvey.estimate_annual_quantity("EDUCAPQ", fmli_2019,
                                              "expense")
compare(education, 1443)

tobacco = cesurvey.estimate_annual_quantity("TOBACCPQ", fmli_2019,
                                            "expense")
compare(tobacco, 320)

misc = cesurvey.estimate_annual_quantity("MISCPQ", fmli_2019,
                                         "expense")
compare(misc, 899) 

cash_contrib = cesurvey.estimate_annual_quantity("CASHCOPQ", fmli_2019,
                                                 "expense")
compare(cash_contrib, 1995) 

retire_pension_ss = cesurvey.estimate_annual_quantity("RETPENPQ", fmli_2019,
                                                      "expense")
compare(retire_pension_ss, 7165) 
```

## Fremstad and Paul categories

```
from cesurvey import estimate_annual_quantity

# Trip expenditures on airfare last quarter
airfare = estimate_annual_quantity("TAIRFARP", fmli_2019)
alcohol = estimate_annual_quantity("ALCBEVPQ", fmli_2019)
education = estimate_annual_quantity("EDUCAPQ", fmli_2019)
auto_insurance = estimate_annual_quantity("VEHINSPQ", fmli_2019)
autos = (
  estimate_annual_quantity("CARTKUPQ", fmli_2019) # used car
  + estimate_annual_quantity("CARTKNPQ", fmli_2019) # new car
  + estimate_annual_quantity("VRNTLOPQ", fmli_2019) # rent/lease
)
books = estimate_annual_quantity("READPQ", fmli_2019)
# https://www.bls.gov/opub/btn/volume-8/the-relationship-between-cash-contributions-pretax-income-and-age.htm
charity = estimate_annual_quantity("CASHCOPQ", fmli_2019) * 396.59 / 2391.48
clothes = estimate_annual_quantity("APPARPQ", fmli_2019)
electricity = estimate_annual_quantity("ELCTRCPQ", fmli_2019)
food_at_home = estimate_annual_quantity("FDHOMEPQ", fmli_2019)
food_at_restaurants = estimate_annual_quantity("FDAWAYPQ", fmli_2019)
furnishings = cesurvey.estimate_annual_quantity("FURNTRPQ", fmli_2019)
# Includes motor oil
gasoline = estimate_annual_quantity("GASMOPQ", fmli_2019)
health = estimate_annual_quantity("HEALTHPQ", fmli_2019)
# Going with "fuel oil" although there's another category that includes "other fuels"
home_heating_fuel = estimate_annual_quantity("FULOILPQ", fmli_2019)
household_supplies = estimate_annual_quantity("OTHHEXPQ", fmli_2019)
# including personal insurance in this cateogry
life_insurance = estimate_annual_quantity("LIFINSPQ", fmli_2019)
mass_transit = estimate_annual_quantity("PUBTRAPQ", fmli_2019)
natural_gas = estimate_annual_quantity("NTLGASPQ", fmli_2019)
# I'm just going to call "other car services" maintenance
other_car_services = estimate_annual_quantity("MAINRPPQ", fmli_2019)
# The word "other" is ignored
other_dwelling_rentals = estimate_annual_quantity("RENDWEPQ", fmli_2019)
# judgement call here. Total outlays including... sport equip
recreation_and_sports = (
    estimate_annual_quantity("EENTRMTP", fmli_2019)
)
# OTHEQPPQ is part of total entertainment
other_recreation = estimate_annual_quantity("OTHEQPPQ", fmli_2019)
telephone = estimate_annual_quantity("TELEPHPQ", fmli_2019)
# tenant occupied dwellings is owned dwellings?
tentant_occupied_dwellings = estimate_annual_quantity("OWNDWEPQ", fmli_2019)
tobacco = estimate_annual_quantity("TOBACCPQ", fmli_2019)
water = estimate_annual_quantity("WATRPSPQ", fmli_2019)

# Fremstad and Paul (2019) Extraction method
2019: 6.6 billion metric tons, or 5.8 separated from land sector

hh_co2_kg = (
    1.0 * airfare
    + .33 * alcohol
    + .24 * education
    + .05 * auto_insurance
    + .73 * autos
    + .22 * books
    + .19 * charity
    + .22 * clothes
    + 2.24 * electricity
    + .39 * food_at_home
    + .24 * food_at_restaurants
    + .71 * furnishings
    + 3.22 * gasoline
    + .22 * health
    + 2.75 * home_heating_fuel
    + .36 * household_supplies
    + .05 * life_insurance
    + .94 * mass_transit
    + 1.82 * natural_gas
    + .23 * other_car_services
    + .06 * other_dwelling_rentals
    + .25 * other_recreation #TODO
    + .7 * recreation_and_sports
    + .18 * telephone
    + .05 * tentant_occupied_dwellings
    + .36 * tobacco
    + .38 * water
)

co2_bil_tons = (hh_co2_kg / 1000) * 128.58 * 1E6 / 1E9
co2_bil_tons


```
