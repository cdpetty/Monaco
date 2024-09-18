import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from Monaco_python_v6 import Montecarlo, build_firm_attributes_for_simulation, stages, stage_probs, stage_valuations, stage_dilution

st.title('Monaco: Monte Carlo Simulation for VC Returns')

st.sidebar.header('Simulation Parameters')

# User inputs
num_scenarios = st.sidebar.slider('Number of Scenarios', 100, 10000, 1000)
fund_size = st.sidebar.number_input('Fund Size (in millions $)', min_value=1, max_value=1000, value=100)
pre_seed_percentage = st.sidebar.slider('Pre-Seed Allocation (%)', 0, 100, 50)
seed_percentage = 100 - pre_seed_percentage
pre_seed_investment = st.sidebar.number_input('Pre-Seed Investment Amount (in millions $)', min_value=0.1, max_value=10.0, value=1.0, step=0.1)
seed_investment = st.sidebar.number_input('Seed Investment Amount (in millions $)', min_value=0.1, max_value=10.0, value=2.0, step=0.1)
follow_on_percentage = st.sidebar.slider('Follow-on Reserve (%)', 0, 100, 30)
primary_percentage = 100 - follow_on_percentage
pro_rata_stage = st.sidebar.selectbox('Pro-rata Up To', options=stages, index=2)  # Default to Series A

if st.sidebar.button('Run Simulation'):
    # Convert percentages to decimals
    pre_seed_percentage /= 100
    seed_percentage /= 100
    follow_on_percentage /= 100
    primary_percentage /= 100
    
    # Calculate amounts in millions
    primary = fund_size * primary_percentage
    follow_on = fund_size * follow_on_percentage
    
    # Build firm attributes
    firm_attributes = build_firm_attributes_for_simulation(
        pre_seed_percentage, pre_seed_investment, 
        seed_percentage, seed_investment, 
        primary, follow_on, fund_size, pro_rata_stage
    )
    
    # Run simulation
    montecarlo = Montecarlo(num_scenarios, stages, stage_probs, stage_valuations, stage_dilution, firm_attributes)
    montecarlo.initialize_scenarios()
    montecarlo.simulate()
    
    # Display results
    st.subheader('Simulation Results')
    
    overview = montecarlo.get_montecarlo_outcomes_overview()
    st.write(f"Number of Simulations: {overview['Num Simulations']}")
    st.write(f"Fund Size: ${overview['Fund Size']} million")
    st.write(f"Initial Investments: {overview['Initial Investment']}")
    st.write(f"Follow-on Reserve: ${overview['Follow on']} million")
    st.write(f"Median MoM: {overview['Median MoM']:.2f}x")
    
    # Plot MoM distribution
    outcomes = montecarlo.get_MoM_return_outcomes()
    fig = go.Figure(data=[go.Histogram(x=outcomes, nbinsx=50)])
    fig.update_layout(title='Distribution of Multiple on Money (MoM)',
                      xaxis_title='Multiple on Money',
                      yaxis_title='Frequency')
    st.plotly_chart(fig)
    
    # Performance quartiles
    quartiles = montecarlo.performance_quartiles()
    st.subheader('Performance Quartiles')
    for percentile, value in quartiles.items():
        st.write(f"{percentile}th Percentile: {float(value[0]):.2f}x")

# Instructions
st.sidebar.markdown("---")
st.sidebar.subheader("How to use:")
st.sidebar.markdown("""
1. Adjust the parameters in the sidebar
2. Click 'Run Simulation'
3. View the results and charts
""")