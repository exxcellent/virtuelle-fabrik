from typing import List

from attr import define

from virtuelle_fabrik.domain.models import Maschine, Produkt

@define
class MaschineADF:
    machine_id: str
    taktrate: float

def create_production_frequency_estimator(
    produkt: Produkt, machine_list: List[Maschine]
):
    """In this function, properties are passed with and so the other functions inside can then use these variables
    for the calculation of the production frequency

    :param recipe: Inputs a recipe
    :type recipe: object
    :param machine_list: Inputs a list of machines
    :type machine_list: list

    :return: Returns the adjusted production frequency
    :rtype: float
    """
    machine_id_to_index_mapping = {m.id: i for i, m in enumerate(machine_list)}

    def get_maschine_for_step(
        schritt_id: str,
    ) -> List[MaschineADF]:
        result: List[MaschineADF] = []
        for maschine in machine_list:
            mb = [ x                    
                    for x in maschine.maschinenbefaehigungen
                    if x.schritt_id == schritt_id
                ]
            if any(mb):
                result.append(MaschineADF(machine_id=maschine.id, taktrate=mb.pop().taktrate))
        return result

    produktionsschritt_id_to_maschine_mapping = dict(
        {
            ps.arbeitsschritt.id: get_maschine_for_step(ps.id)
            for ps in produkt.produktionsschritte
        }
    )

    def production_frequency(x: List[float]):
        """This function calculates the maximum frequency for each step. The step with the lowest frequency will decide
        the overall frequency for the production

        :param x: Inputs a list of starting values for the capacity utilisation of a machine
        :type x: list
        :return: Returns the overall production frequency
        :rtype: float
        """
        current_lowest_frequency = 1000
        for produktionsschritt in produkt.produktionsschritte:
            step_freq = 0
            for maschine in produktionsschritt_id_to_maschine_mapping.get(
                produktionsschritt.id, []
            ):
                step_freq += (
                    maschine.taktrate
                    * x[machine_id_to_index_mapping[maschine.machine_id]]
                )
            if step_freq < current_lowest_frequency:
                current_lowest_frequency = step_freq
        return current_lowest_frequency

    return production_frequency, produktionsschritt_id_to_maschine_mapping


def create_total_costs_estimator(machine_list: List[Maschine]):
    """In this function, properties are passed with and so the other functions inside can then use these variables
    for the calculation of the total costs

    :param recipe: Inputs a recipe
    :type recipe: object
    :param machine_list: Inputs a list of machines
    :type machine_list: list

    :return: Returns the total costs
    :rtype: float
    """

    def total_costs(x: List[float]):
        """This function calculates the total machine costs per time unit

        :param x: Inputs a list of starting values for the capacity utilisation of a machine
        :type x: list
        :return: Returns total costs per timeunit
        :rtype: float
        """
        total_costs = 0
        for i, m in enumerate(machine_list):
            total_costs += m.kosten_minute * x[i] + 1  # little penalty with +1
        # loop over machines and add up all costs and scale with usage times x
        return total_costs

    return total_costs


def create_costs_per_product_estimator(produkt: Produkt, machine_list: List[Maschine]):
    """In this function, properties are passed with and so the other functions inside can then use these variables
    for the calculation of the costs per product

    :param recipe: Inputs a recipe
    :type recipe: object
    :param machine_list: Inputs a list of machines
    :type machine_list: list

    :return: Returns the costs per product
    :rtype: float
    """
    (production_frequency, produktionsschritt_id_to_maschine_mapping) = create_production_frequency_estimator(produkt, machine_list)
    total_costs = create_total_costs_estimator(machine_list)

    def costs_per_product(x: List[float]):
        """This function calculates the costs per product

        :param x: Inputs a list of starting values
        :type x: list
        :return: Returns costs per product
        :rtype: float
        """
        return total_costs(x) / production_frequency(x)

    return costs_per_product, produktionsschritt_id_to_maschine_mapping
