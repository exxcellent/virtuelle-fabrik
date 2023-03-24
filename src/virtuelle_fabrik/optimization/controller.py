from typing import List
from virtuelle_fabrik.domain.models import Maschine, Produkt
from .production_planning import create_costs_per_product_estimator
from scipy.optimize import minimize

def get_bounds(maschinen):
    """This function creates the bounds for the optimization in a generic way

    :param recipe: Recipe object
    :type recipe: object
    :return: Returns the bounds
    :rtype: list
    """
    l = len(maschinen)
    i = 0
    bounds = []
    while i < l:
        bounds.append((1e-6, 1))
        i += 1
    return bounds


def costs_per_product_optimization(produkt: Produkt, maschinen: List[Maschine]):
    """This function calls the optimization for the optimal frequency and optimal costs per product"""
    costs_per_product = create_costs_per_product_estimator(
        produkt, maschinen
    )
    opt = minimize(
        costs_per_product, x0=[1 for m in maschinen], bounds=get_bounds(maschinen)
    )
    return opt
