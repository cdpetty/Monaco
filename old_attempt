import streamlit as st
import random

# Define the Company class
class Company:
    STAGES = ["Seed", "Series A", "Series B", "Series C", "IPO"]
    STATES = ["Alive", "Failed"]

    def __init__(self, name, stage, valuation, state, investor_ownership, growth_rate, volatility):
        self.name = name
        self.stage = stage
        self.valuation = valuation
        self.state = state
        self.investor_ownership = investor_ownership
        self.growth_rate = growth_rate
        self.volatility = volatility

# Initialize the companies
def initialize_companies(num_companies, initial_valuation, initial_investor_ownership):
    companies = []
    for i in range(num_companies):
        name = f"Company {i+1}"
        stage = "Seed"
        valuation = initial_valuation
        state = "Alive"
        investor_ownership = initial_investor_ownership
        growth_rate = random.uniform(0.05, 0.15)
        volatility = random.uniform(0.01, 0.05)
        company = Company(name, stage, valuation, state, investor_ownership, growth_rate, volatility)
        companies.append(company)
    return companies

# Run the simulation
def run_simulation(companies, num_years):
    st.title("Monaco Simulation")
    st.write("Here's how the companies performed:")

    for year in range(num_years):
        st.write("---")
        st.write(f"Year {year+1}:")
        for company in companies:
            if company.state == "Alive":
                company.valuation += company.valuation * company.growth_rate + company.valuation * company.volatility * random.uniform(-1, 1)
                if random.random() < 0.05:
                    company.state = "Failed"
            st.write(f"{company.name} (Stage: {company.stage}, Valuation: {company.valuation:.2f}, State: {company.state}, Investor Ownership: {company.investor_ownership:.2f})")

    st.write("---")
    st.write("That's the end of the simulation. Thanks for watching!")

# Main function
def main():
    st.title("Monaco Simulation")
    num_companies = st.number_input("Number of companies:", min_value=1, step=1, value=10)
    initial_valuation = st.number_input("Initial valuation for each company:", min_value=100.0, step=10.0, value=500.0)
    initial_investor_ownership = st.number_input("Initial investor ownership for each company:", min_value=0.1, max_value=0.9, step=0.1, value=0.5)
    num_years = st.number_input("Number of years to simulate:", min_value=1, step=1, value=10)

    companies = initialize_companies(int(num_companies), initial_valuation, initial_investor_ownership)
    run_simulation(companies, int(num_years))

if __name__ == "__main__":
    main()
