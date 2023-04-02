from datetime import datetime
from typing import List

from virtuelle_fabrik.domain.exception import DomainException
from virtuelle_fabrik.domain.models import (
    Arbeitsschritt,
    Maschine,
    Maschinenauslastung,
    Optimierung,
    OptimierungsErgebnis,
    LeistungsErgebnis,
    Produkt,
    Produktionslinie,
    Station,
)
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
    (
        costs_per_product,
        produktionsschritt_id_to_maschine_mapping,
    ) = create_costs_per_product_estimator(produkt, maschinen)
    opt = minimize(
        costs_per_product, x0=[1 for m in maschinen], bounds=get_bounds(maschinen)
    )

    opt.m_mapping = produktionsschritt_id_to_maschine_mapping

    return opt


def calc_optimized(
    produkt: Produkt, maschinen: List[Maschine], arbeitsschritte: List[Arbeitsschritt]
) -> LeistungsErgebnis:

    opt = costs_per_product_optimization(produkt, maschinen)

    # transforms map of arbeitsschrittId to dict, to a map of maschinen_id to Arbeitsschritt
    arbeitsschritte_dict = {
        maschine.machine_id: next((a for a in arbeitsschritte if a.id == schritt), None)
        for schritt, maschinen in opt.m_mapping.items()
        for maschine in maschinen
    }
    
    auslastungen = [
        Maschinenauslastung(
            maschine=m,
            arbeitsschritt=arbeitsschritte_dict[m.id],
            auslastung=round(opt.x[i], 2),
        )
        for i, m in enumerate(maschinen)
    ]

    # filter 0 utilisation
    auslastungen = list(filter(lambda m: m.auslastung > 0.0, auslastungen))

    return LeistungsErgebnis(
        kosten_produkt=round(opt.fun, 2), maschinenauslastung=auslastungen
    )


def calc_per_station(
    station: Station, maschinen: List[Maschine], arbeitsschritte: List[Arbeitsschritt]
) -> OptimierungsErgebnis:

    if len(station.chargen) < 1:
        raise DomainException(
            message=f"station '{station.name}' does not have a Charge assigned"
        )

    produkt = station.chargen[0].produktbedarf[0].produkt

    return OptimierungsErgebnis(
        station=station,
        gegeben=calc_optimized(produkt, station.maschinen, arbeitsschritte),
        optimiert=calc_optimized(produkt, maschinen, arbeitsschritte),
    )


def calc_optimization(
    produktionslinie: Produktionslinie,
    maschinen: List[Maschine],
    arbeitsschritte: List[Arbeitsschritt],
):

    optimization = Optimierung(
        id="1",
        ausfuehrung=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        produktionslinie=produktionslinie,
        stationen=[
            calc_per_station(s, maschinen, arbeitsschritte)
            for s in produktionslinie.stationen
        ],
    )

    return optimization
