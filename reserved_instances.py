#!/usr/bin/env python3

from pprint import pprint as pp

hours_in_month = 730

redshift_pricing = {
    'ondemand': {
        'upfront': 0,
        'monthly': .25 * hours_in_month,
        'effective': .25,
    },
    '1y_noupfront': {
        'upfront': 0,
        'monthly': 146,
        'effective': .2,
    },
    '1y_partial_upfront': {
        'upfront': 750,
        'monthly': 55,
        'effective': .161,
    },
    '1y_all_upfront': {
        'upfront': 1380,
        'monthly': 0,
        'effective': .157,
    },
    '3y_partial_upfront': {
        'upfront': 1325,
        'monthly': 37,
        'years': 3,
        'effective': .100,
    },
    '3y_all_upfront': {
        'upfront': 2465,
        'monthly': 0,
        'years': 3,
        'effective': .094,
    },
}


def calculate_effective_hourly_cost(upfront, monthly, years=1):
    months = years * 12
    return round((monthly + upfront / months) / hours_in_month, 3)


def hourly_cost(monthly):
    return monthly / hours_in_month


def generate_monthly_costs(option, months):
    monthly = list()
    for month in range(0, months):
        monthly.append(redshift_pricing[option]['monthly'])
        if month % (12 * redshift_pricing[option].get('years', 1)) == 0:
            monthly[month] = monthly[month] + redshift_pricing[option]['upfront']
    return monthly


def aggregate_costs(monthly):
    costs = list()
    for num, month in enumerate(monthly):
        if num == 0:
            costs.append(month)
        else:
            if num == 2:
                pp(costs)
            costs.append(month + costs[num - 1])
    return costs


def show_hourly_vs_effective_hourly():

    hourly_cost = dict()
    for option in redshift_pricing.keys():
        hourly_cost[option] = calculate_effective_hourly_cost(redshift_pricing[option]['upfront'],
                                                            redshift_pricing[option]['monthly'],
                                                            redshift_pricing[option].get('years', 1))
        delta = round(abs(redshift_effective_hourly[option] - hourly_cost[option]), 3)
        print("Option {}: {}, {}".format(option, hourly_cost[option], delta))

    return hourly_cost


def main():
    pricing = dict()
    for option in redshift_pricing.keys():
        pricing[option] = aggregate_costs(generate_monthly_costs(option, 36))
# END
