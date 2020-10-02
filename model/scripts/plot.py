import pkgutil

from plot_scripts import dispatch, electricity_spot_price_timeseries, heat_demand_timeseries,\
    sq_to_ff_capacity, sq_to_ff_cost, sq_to_ff_energy


dispatch.plot()

electricity_spot_price_timeseries.plot()

heat_demand_timeseries.plot()

sq_to_ff_capacity.plot()

sq_to_ff_cost.plot()

sq_to_ff_energy.plot()
