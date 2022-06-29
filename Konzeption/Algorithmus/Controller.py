import OrderProcessing
import ProductionPlanning
import Product
# Optimized Order Amount
OrderProcessing.calloptOrderAmount(OrderProcessing.materialPlanning(OrderProcessing.b1))

# Optimize Frequency and Costs per Product
machine_list = ProductionPlanning.getMachineList(Product.recipes[0])
costs_per_product = ProductionPlanning.create_costs_per_product_estimator(Product.recipes[0], machine_list)
bounds = ProductionPlanning.getBounds(Product.recipes[0])
opt = ProductionPlanning.minimize(costs_per_product, x0=[1 for m in machine_list],bounds=bounds)
print("\nCosts per product:","\033[1m",round(opt.fun,2), "monetary units", "\033[0;0m"
      "\nThe capacity utilisation of the individual machines are:")
ProductionPlanning.getMachineCapabilities(Product.recipes[0], opt.x)