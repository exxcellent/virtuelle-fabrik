from platform import machine
from pyclbr import Function
from typing import Callable, List, Mapping, Set, Tuple
from scipy.optimize import minimize
from functools import reduce

import attr


@attr.frozen
class Step:
    id = attr.ib(type=int)
    description = attr.ib(type=str)


@attr.frozen
class StepAbility:
    step = attr.ib(type=Step)
    frequency = attr.ib(type=float)


@attr.define
class Machine:
    id: int
    step_abilities: StepAbility  # we make it simple... a machine just has one ability...
    costs_per_timeunit: float


@attr.define
class Employee:
    step_abilities: Set[Step]
    cost_per_timeunit: float


@attr.define
class Product:
    id: int
    description: str


@attr.define
class Recipe:
    product: Product
    steps: List[Step]


# define some dummy problem

step1 = Step(1, "do something")
step2 = Step(2, "do something")
recipe = Recipe(Product(1, "dummy product"), steps=[step1, step2])

machines = [
    Machine(id=1, step_abilities=StepAbility(step1, 3.0), costs_per_timeunit=100),
    Machine(
        id=2,
        step_abilities=StepAbility(step1, frequency=1.0),
        costs_per_timeunit=50,
    ),
    Machine(
        id=3,
        step_abilities=StepAbility(step2, frequency=0.5),
        costs_per_timeunit=50,
    ),
]
# Note that machine 3 will be the bottleneck, so even though machine 1 is better than machine 2 in step 1
# the overall costs may be higher depending on the boundary conditions

# convert problem into a example optimization strategy (turning it into a function which can be optimized)
# This is the actual tricky part and the main task of your work


@attr.define
class CostPerformanceOverview:
    machine_id: int
    cost_per_timeunit: float
    frequency: float


def create_costs_per_product_estimator(
    recipe: Recipe, machine_pool: List[Machine], machine_constraints: Mapping[int, int]
) -> Tuple[Callable[[List[float]], float], List[int]]:
    step_id_to_machine_id_pool_mapping = {}
    machine_id_to_machine_mapping = {m.id: m for m in machine_pool}
    for step in recipe.steps:
        step_id_to_machine_id_pool_mapping.update(
            {
                step.id: set(
                    [
                        machine.id
                        for machine in machine_pool
                        if machine.step_abilities.step.id == step.id
                    ]
                )
            }
        )

    machine_id_to_parameter_index_mapping = {
        m.id: i for i, m in enumerate(machine_pool) if m.id not in machine_constraints
    }  # only regard machines for now

    def calculate_effective_frequency(n: float, freq: float) -> float:
        eff_freq = (
            freq * abs(n) * pow(1 - (min(abs(n - int(n)), abs(n - int(n + 1))) * 2), 10)
        )  # the further away from a integer value the more the frequency will be penalized
        return eff_freq

    def costs_per_product(parameters: List[float]) -> float:
        costs_and_products_per_timeframe = []
        for step in recipe.steps:
            costs_performance_overviews = [
                CostPerformanceOverview(
                    machine_id,
                    machine_id_to_machine_mapping[machine_id].costs_per_timeunit,
                    machine_id_to_machine_mapping[machine_id].step_abilities.frequency,
                )  # This [0] acesss is quick and dirty code
                for machine_id in step_id_to_machine_id_pool_mapping[step.id]
            ]
            costs_and_products_per_timeframe.append(
                reduce(
                    lambda a, b: (
                        a[0]
                        + abs(
                            parameters[
                                machine_id_to_parameter_index_mapping[b.machine_id]
                            ]
                            if b.machine_id in machine_id_to_parameter_index_mapping
                            else machine_constraints[b.machine_id]
                        )
                        * b.cost_per_timeunit,
                        a[1]
                        + calculate_effective_frequency(
                            parameters[
                                machine_id_to_parameter_index_mapping[b.machine_id]
                            ],
                            b.frequency,
                        )
                        if b.machine_id in machine_id_to_parameter_index_mapping
                        else machine_constraints[b.machine_id] * b.frequency,
                    ),
                    costs_performance_overviews,
                    (0.0, 0.0),
                )
            )

        (total_costs, products_per_timeframe) = reduce(
            lambda a, b: (
                a[0] + b[0],
                min(a[1], b[1]),
            ),  # the slowest step determines the overall work frequency
            costs_and_products_per_timeframe,
            (0.0, 1.0e10),
        )

        # this metric is arbitrary in selecting the
        return total_costs / (products_per_timeframe + 1e-8)

    return (costs_per_product, list(machine_id_to_parameter_index_mapping.keys()))


(estimator_function, optimization_parameters) = create_costs_per_product_estimator(
    recipe, machines, {3: 1}  # require machine 3 to exist exactly once
)

# lets see what the estimator calculates
print(optimization_parameters)
print(estimator_function([1, 1]))  # 50/0.5+100/0.5+50/0.5 => 400
print(estimator_function([1, 0]))  # 50/0.5+100/0.5+0      => 300
print(estimator_function([0, 1]))  # 50/0.5+0      +50/0.5 => 200

# use scipy minimize to find the minimum of the estimator function given some start parameters
result = minimize(
    estimator_function,
    x0=[0.1, 0.9],
)

print(result)  # we expect one machine of id 2 to be used instead of machine 1
