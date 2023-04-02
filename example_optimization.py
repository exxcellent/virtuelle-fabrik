#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.getcwd())

from virtuelle_fabrik.domain.models import (
    Arbeitsschritt,
    Charge,
    Maschine,
    MaschinenBefaehigung,
    Material,
    Materialbedarf,
    Produkt,
    Produktbedarf,
    Produktionslinie,
    Produktionsschritt,
    Station,
)
from virtuelle_fabrik.optimization.controller import (
    calc_optimization,
    costs_per_product_optimization,
)


def sample_optimization():
    arbeitsschritte = [
        Arbeitsschritt(id="1", name="Sägen"),
        Arbeitsschritt(id="2", name="Härter Sägen"),
    ]
    # create some produkt and machines
    produkt = Produkt(
        id="1",
        name="Tisch",
        verkaufspreis=500,
        produktionsschritte=[
            Produktionsschritt(id="1", arbeitsschritt=arbeitsschritte[0], schritt=1),
            Produktionsschritt(id="2", arbeitsschritt=arbeitsschritte[1], schritt=2),
        ],
        materialbedarf=[
            Materialbedarf(
                id="1",
                material=Material(
                    id="1",
                    name="Holz",
                    kosten_stueck=40,
                    bestand=0,
                    aufstocken_minute=0,
                ),
                menge=5.0,
            )
        ],
    )

    charge = Charge(
        id="1",
        prioritaet=0,
        name="Tische",
        produktbedarf=[Produktbedarf(id="1", produkt=produkt, stueckzahl=1000)],
    )

    maschinen = [
        Maschine(
            id="1",
            name="Saege 1",
            ruestzeit=2.0,
            kosten_minute=10,
            ausfall_wahrscheinlichkeit=0.01,
            mitarbeiter_min=0,
            mitarbeiter_max=0,
            maschinenbefaehigungen=[
                MaschinenBefaehigung(id="1", schritt_id="1", taktrate=2)
            ],
        ),
        Maschine(
            id="2",
            name="Saege 2",
            ruestzeit=2.0,
            kosten_minute=15,
            ausfall_wahrscheinlichkeit=0.01,
            mitarbeiter_min=0,
            mitarbeiter_max=0,
            maschinenbefaehigungen=[
                MaschinenBefaehigung(id="1", schritt_id="1", taktrate=10)
            ],
        ),
        Maschine(
            id="3",
            name="Saege 3",
            ruestzeit=2.0,
            kosten_minute=5,
            ausfall_wahrscheinlichkeit=0.01,
            mitarbeiter_min=0,
            mitarbeiter_max=0,
            maschinenbefaehigungen=[
                MaschinenBefaehigung(id="1", schritt_id="1", taktrate=3)
            ],
        ),
        Maschine(
            id="4",
            name="Schleifmaschine 1",
            ruestzeit=0.1,
            kosten_minute=3,
            ausfall_wahrscheinlichkeit=0.01,
            mitarbeiter_min=0,
            mitarbeiter_max=0,
            maschinenbefaehigungen=[
                MaschinenBefaehigung(id="1", schritt_id="2", taktrate=4)
            ],
        ),
        Maschine(
            id="5",
            name="Schleifmaschine 2",
            ruestzeit=0.1,
            kosten_minute=3,
            ausfall_wahrscheinlichkeit=0.01,
            mitarbeiter_min=0,
            mitarbeiter_max=0,
            maschinenbefaehigungen=[
                MaschinenBefaehigung(id="1", schritt_id="2", taktrate=3)
            ],
        ),
    ]

    produktionslinie = Produktionslinie(
        id="1",
        stationen=[
            Station(
                id="1",
                name="Neue Statione",
                order=0,
                maschinen=maschinen,
                chargen=[charge],
            )
        ],
    )

    result = costs_per_product_optimization(produkt, maschinen)
    print(
        "\nCosts per product:",
        "\033[1m",
        round(result.fun, 2),
        "monetary units",
        "\033[0;0m" "\nThe capacity utilisation of the individual machines are:",
    )

    for i, m in enumerate(maschinen):
        print(
            "Machine ID:",
            m.id,
            "Costs per time unit:",
            m.kosten_minute,
            "Capacity Utilisation:",
            round(result.x[i], 2),
        )

    opt = calc_optimization(produktionslinie, maschinen, arbeitsschritte)

sample_optimization()
