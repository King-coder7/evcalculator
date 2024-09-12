from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import csv

# Abstract class for Calculator
class Calculator(ABC):
    @abstractmethod
    def calculate_savings(self):
        pass

    @abstractmethod
    def calculate_payback_period(self):
        pass

    @abstractmethod
    def calculate_co2_reduction(self):
        pass

    @abstractmethod
    def display_results(self, detailed=True):
        pass

    @abstractmethod
    def export_results_to_csv(self, filename):
        pass

    @abstractmethod
    def plot_costs(self):
        pass

    @abstractmethod
   

# ElectricCarSavingsCalculator that inherits from Calculator
class ElectricCarSavingsCalculator(Calculator):
    def __init__(self, calculator_type, miles_per_year, mpg, gas_price, miles_per_kwh, electric_price, gas_maintenance, electric_maintenance, gas_car_price, electric_car_price, co2_per_gallon, co2_per_kwh):
        self.calculator_type = calculator_type  # New attribute for calculator type
        self.miles_per_year = miles_per_year
        self.mpg = mpg
        self.gas_price = gas_price
        self.miles_per_kwh = miles_per_kwh
        self.electric_price = electric_price
        self.gas_maintenance = gas_maintenance
        self.electric_maintenance = electric_maintenance
        self.gas_car_price = gas_car_price
        self.electric_car_price = electric_car_price
        self.co2_per_gallon = co2_per_gallon
        self.co2_per_kwh = co2_per_kwh
        self._gas_cost = None
        self._electric_cost = None
        self._annual_savings = None

    # Validation function to ensure required fields are present
    def validate_inputs(self):
        if any(x is None for x in [
            self.miles_per_year, self.mpg, self.gas_price, self.miles_per_kwh, 
            self.electric_price, self.gas_maintenance, self.electric_maintenance, 
            self.gas_car_price, self.electric_car_price, self.co2_per_gallon, 
            self.co2_per_kwh]):
            raise ValueError("All required fields must be set before calculations can be performed.")

    def calculate_gasoline_cost(self):
        self.validate_inputs()
        gallons_used = self.miles_per_year / self.mpg
        self._gas_cost = gallons_used * self.gas_price
        return self

    def calculate_electric_cost(self):
        self.validate_inputs()
        kwh_used = self.miles_per_year / self.miles_per_kwh
        self._electric_cost = kwh_used * self.electric_price
        return self

    def calculate_savings(self):
        if self._gas_cost is None or self._electric_cost is None:
            raise Exception("Gasoline and Electric costs must be calculated before calculating savings.")
        
        maintenance_savings = self.gas_maintenance - self.electric_maintenance
        self._annual_savings = (self._gas_cost - self._electric_cost) + maintenance_savings
        return self

    def calculate_payback_period(self):
        if self._annual_savings == 0:
            return float('inf')
        price_difference = self.gas_car_price - self.electric_car_price
        return price_difference / self._annual_savings

    def calculate_co2_reduction(self):
        gas_emissions = (self.miles_per_year / self.mpg) * self.co2_per_gallon
        electric_emissions = (self.miles_per_year / self.miles_per_kwh) * self.co2_per_kwh
        return gas_emissions - electric_emissions

    def display_results(self, detailed=True):
        self.validate_inputs()
        if detailed:
            print(f"\nAnnual cost for gasoline car: ${self._gas_cost:.2f}")
            print(f"Annual cost for electric car: ${self._electric_cost:.2f}")
            print(f"Annual savings (including maintenance): ${self._annual_savings:.2f}")
            print(f"Payback period (years) for the electric car: {self.calculate_payback_period():.2f} years")
            print(f"Annual CO2 reduction by switching to electric car: {self.calculate_co2_reduction():.2f} kg")
        else:
            print(f"\nAnnual savings: ${self._annual_savings:.2f}")
            print(f"Payback period: {self.calculate_payback_period():.2f} years")
            print(f"CO2 reduction: {self.calculate_co2_reduction():.2f} kg")

    def export_results_to_csv(self, filename="savings_report.csv"):
        self.validate_inputs()
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Annual Gasoline Cost", f"${self._gas_cost:.2f}"])
            writer.writerow(["Annual Electric Cost", f"${self._electric_cost:.2f}"])
            writer.writerow(["Annual Savings", f"${self._annual_savings:.2f}"])
            writer.writerow(["Payback Period (years)", f"{self.calculate_payback_period():.2f}"])
            writer.writerow(["CO2 Reduction (kg)", f"{self.calculate_co2_reduction():.2f}"])

    def plot_costs(self):
        labels = ['Gasoline Cost', 'Electric Cost', 'Savings']
        values = [self._gas_cost, self._electric_cost, self._annual_savings]
        
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=['blue', 'green', 'orange'])
        plt.title('Annual Costs Comparison')
        plt.ylabel('Cost ($)')
        plt.show()

    def plot_co2_reduction(self):
        labels = ['Gasoline CO2', 'Electric CO2', 'Reduction']
        values = [
            (self.miles_per_year / self.mpg) * self.co2_per_gallon,
            (self.miles_per_year / self.miles_per_kwh) * self.co2_per_kwh,
            self.calculate_co2_reduction()
        ]
        
        plt.figure(figsize=(10, 6))
        plt.bar(labels, values, color=['red', 'green', 'blue'])
        plt.title('CO2 Emissions Comparison')
        plt.ylabel('CO2 (kg)')
        plt.show()


# Builder Pattern with validation and calculator type
class ElectricCarSavingsCalculatorBuilder:
    def __init__(self):
        self.calculator_type = None
        self.miles_per_year = None
        self.mpg = None
        self.gas_price = None
        self.miles_per_kwh = None
        self.electric_price = None
        self.gas_maintenance = None
        self.electric_maintenance = None
        self.gas_car_price = None
        self.electric_car_price = None
        self.co2_per_gallon = None
        self.co2_per_kwh = None

    def set_calculator_type(self, calculator_type):
        self.calculator_type = calculator_type
        return self

    def set_miles_per_year(self, miles_per_year):
        self.miles_per_year = miles_per_year
        return self

    def set_mpg(self, mpg):
        self.mpg = mpg
        return self

    def set_gas_price(self, gas_price):
        self.gas_price = gas_price
        return self

    def set_miles_per_kwh(self, miles_per_kwh):
        self.miles_per_kwh = miles_per_kwh
        return self

    def set_electric_price(self, electric_price):
        self.electric_price = electric_price
        return self

    def set_gas_maintenance(self, gas_maintenance):
        self.gas_maintenance = gas_maintenance
        return self

    def set_electric_maintenance(self, electric_maintenance):
        self.electric_maintenance = electric_maintenance
        return self

    def set_gas_car_price(self, gas_car_price):
        self.gas_car_price = gas_car_price
        return self

    def set_electric_car_price(self, electric_car_price):
        self.electric_car_price = electric_car_price
        return self

    def set_co2_per_gallon(self, co2_per_gallon):
        self.co2_per_gallon = co2_per_gallon
        return self

    def set_co2_per_kwh(self, co2_per_kwh):
        self.co2_per_kwh = co2_per_kwh
        return self

    def validate_builder_inputs(self):
        if any(x is None for x in [
            self.calculator_type, self.miles_per_year, self.mpg, self.gas_price, 
            self.miles_per_kwh, self.electric_price, self.gas_maintenance, 
            self.electric_maintenance, self.gas_car_price, self.electric_car_price, 
            self.co2_per_gallon, self.co2_per_kwh]):
            raise ValueError("All fields in the builder must be set before building the calculator.")

    def build(self):
        self.validate_builder_inputs()  # Ensure inputs are valid
        return ElectricCarSavingsCalculator(
            self.calculator_type, self.miles_per_year, self.mpg, self.gas_price, 
            self.miles_per_kwh, self.electric_price, self.gas_maintenance, 
            self.electric_maintenance, self.gas_car_price, self.electric_car_price, 
            self.co2_per_gallon, self.co2_per_kwh
        )


# Example usage
builder = ElectricCarSavingsCalculatorBuilder()
calculator = (builder.set_calculator_type("Savings")
              .set_miles_per_year(15000)
              .set_mpg(25)
              .set_gas_price(3.50)
              .set_miles_per_kwh(4)
              .set_electric_price(0.13)
              .set_gas_maintenance(500)
              .set_electric_maintenance(200)
              .set_gas_car_price(25000)
              .set_electric_car_price(30000)
              .set_co2_per_gallon(8.89)
              .set_co2_per_kwh(0.43)
              .build())

calculator.calculate_gasoline_cost().calculate_electric_cost().calculate_savings().display_results(detailed=True)
