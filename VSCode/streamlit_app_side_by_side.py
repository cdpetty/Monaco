import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from Monaco_python_v6 import Montecarlo, build_firm_attributes_for_simulation, stages, stage_probs, stage_valuations, stage_dilution

st.title('Monaco: Monte Carlo Simulation for VC Returns')

def run_single_simulation(params):
    firm_attributes = build_firm_attributes_for_simulation(
        params['pre_seed_percentage'], params['pre_seed_investment'],
        params['seed_percentage'], params['seed_investment'],
        params['primary'], params['follow_on'], params['fund_size'],
        params['pro_rata_stage']
    )
    
    montecarlo = Montecarlo(params['num_scenarios'], stages, stage_probs, stage_valuations, stage_dilution, firm_attributes)
    montecarlo.initialize_scenarios()
    montecarlo.simulate()
    
    return montecarlo

def display_results(montecarlo, title):
    st.subheader(title)
    
    overview = montecarlo.get_montecarlo_outcomes_overview()
    st.write(f"Number of Simulations: {overview['Num Simulations']}")
    st.write(f"Fund Size: ${overview['Fund Size']} million")
    st.write(f"Initial Investments: {overview['Initial Investment']}")
    st.write(f"Follow-on Reserve: ${overview['Follow on']} million")
    st.write(f"Median MoM: {overview['Median MoM']:.2f}x")
    
    outcomes = montecarlo.get_MoM_return_outcomes()
    fig = go.Figure(data=[go.Histogram(x=outcomes, nbinsx=50)])
    fig.update_layout(title='Distribution of Multiple on Money (MoM)',
                      xaxis_title='Multiple on Money',
                      yaxis_title='Frequency')
    st.plotly_chart(fig)
    
    quartiles = montecarlo.performance_quartiles()
    st.subheader('Performance Quartiles')
    for percentile, value in quartiles.items():
        st.write(f"{percentile}th Percentile: {float(value[0]):.2f}x")

# Sidebar for user inputs
st.sidebar.header('Simulation Parameters')

# User inputs
params = {}
params['num_scenarios'] = st.sidebar.slider('Number of Scenarios', 100, 10000, 1000)
params['fund_size'] = st.sidebar.number_input('Fund Size (in millions $)', min_value=1, max_value=1000, value=100)
params['pre_seed_percentage'] = st.sidebar.slider('Pre-Seed Allocation (%)', 0, 100, 50) / 100
params['seed_percentage'] = 1 - params['pre_seed_percentage']
params['pre_seed_investment'] = st.sidebar.number_input('Pre-Seed Investment Amount (in millions $)', min_value=0.1, max_value=10.0, value=1.0, step=0.1)
params['seed_investment'] = st.sidebar.number_input('Seed Investment Amount (in millions $)', min_value=0.1, max_value=10.0, value=2.0, step=0.1)
follow_on_percentage = st.sidebar.slider('Follow-on Reserve (%)', 0, 100, 30) / 100
params['primary'] = params['fund_size'] * (1 - follow_on_percentage)
params['follow_on'] = params['fund_size'] * follow_on_percentage
params['pro_rata_stage'] = st.sidebar.selectbox('Pro-rata Up To', options=stages, index=2)  # Default to Series A

if 'previous_params' not in st.session_state:
    st.session_state.previous_params = None

if 'current_results' not in st.session_state:
    st.session_state.current_results = None

if st.sidebar.button('Run Simulation'):
    current_results = run_single_simulation(params)
    
    col1, col2 = st.columns(2)
    
    with col1:
        display_results(current_results, "Current Simulation")
    
    with col2:
        if st.session_state.previous_params is not None:
            previous_results = run_single_simulation(st.session_state.previous_params)
            display_results(previous_results, "Previous Simulation")
        else:
            st.write("No previous simulation available")
    
    st.session_state.previous_params = params.copy()
    st.session_state.current_results = current_results

# Instructions
st.sidebar.markdown("---")
st.sidebar.subheader("How to use:")
st.sidebar.markdown("""
1. Adjust the parameters in the sidebar
2. Click 'Run Simulation'
3. View the results side by side
4. Adjust parameters and run again to compare
""")