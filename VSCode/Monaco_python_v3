import random
import math
import numpy as np
import time


class Company:
    
    def __init__(self, name, stage, valuation, state, firm_invested_capital, firm_ownership, stages, valuations, dilution):
        self.name = name
        self.stage = stage
        self.valuation = valuation
        self.state = state
        self.firm_invested_capital = firm_invested_capital
        self.firm_ownership = firm_ownership
        self.market_constraints = {
            'stages': stages,
            'valuations': valuations,
            'dilution': dilution
        }
        self.age = 0
    
    ## Promote this company to the next stage in its life
    def promote(self, secondary_dry_powder, pro_rata_at_or_below):
        
        ## Promote to the next stage and update states accordingly
        self.age += 1
        self.stage = self.market_constraints['stages'][min(self.market_constraints['stages'].index(self.stage) + 1, len(self.market_constraints['stages'])-1)] ## if already at last stage, stay at last stage
        self.valuation = self.market_constraints['valuations'][self.stage]

        ## Determine post-dilution ownership
        dilution = self.market_constraints['dilution'][self.stage]
        post_dilution_ownership = self.firm_ownership*(1-dilution)
        
        ## If the fund does pro rata at this stage, and still has dry powder to contribute to secondaries, then determine pro rata investment
        ## This logic is included as part of the "Company" class (instead of the firm class) b/c each company requires a different amount of pro rata depending on investment history
        pro_rata_investment = 0
        if self.valuation <= pro_rata_at_or_below:
            pro_rata_investment = min((self.firm_ownership - post_dilution_ownership)*self.valuation, secondary_dry_powder)
        self.firm_invested_capital += pro_rata_investment

        ## Update firm ownership based on dilution and pro rata
        self.firm_ownership = (self.firm_ownership*(1-dilution)) + pro_rata_investment/self.valuation ## existing ownership minus dilution plus pro rata investment ownership
        
        return pro_rata_investment
            

    ## execute M&A for this company
    def m_and_a(self):

        ## Increment age and adjust stage
        self.age += 1
        self.state = "Acquired"

        ## M&A outcomes - todo: move these to global or montecarlo class
        ## 1% chance of 10x outcome, 2% chance of 5x outcome, 27% chance of 1x outcome, 70% chance of 0.5x outcome
        m_and_a_outcome_odds = [0.01, 0.02, 0.27, 0.7]
        m_and_a_multipliers = [10,5,1,.5]

        
        ## Generate random value which determines M&A outcomes
        rand = random.random()
        if rand <m_and_a_outcome_odds[0]:
            # print('10x')
            self.valuation = m_and_a_multipliers[0]*self.valuation
        elif rand < m_and_a_outcome_odds[0]+m_and_a_outcome_odds[1]:
            # print('5x')
            self.valuation = m_and_a_multipliers[1]*self.valuation
        elif rand < m_and_a_outcome_odds[0]+m_and_a_outcome_odds[1]+m_and_a_outcome_odds[2]:
            # print('1x')
            self.valuation = m_and_a_multipliers[2]*self.valuation
        else:
            # print('0.5x')
            self.valuation = m_and_a_multipliers[3]*self.valuation
    
    
    def get_firm_value(self):
        return self.valuation * self.firm_ownership

    def fail(self):
        self.age += 1
        self.state = 'Failed'
        self.valuation = 0
    
    ## Function just for aging company - only used when a company is already failed or acquired, and we want to track age anyway
    def age_company(self):
        self.age += 1
    
    def get_numerical_stage(self):
        return self.market_constraints['stages'].index(self.stage)

    def __str__(self):
        return '[' + self.name + ', ' + self.stage + ', ' + str(self.valuation) + ', ' + self.state + ', ' + str(self.firm_invested_capital) + ', ' + str(self.firm_ownership) + ']'
    
    def __repr__(self):
        return '[' + self.name + ', ' + self.stage + ', ' + str(self.valuation) + ', ' + self.state + ', ' +  str(self.firm_ownership) + ',' + str(self.get_firm_value()) + ']\n'


#############################################################################
#############################################################################
############################# FIRM CLASS ####################################
#############################################################################
#############################################################################
class Firm:
    ''' A firm is a collection of companies that it has invested in. It has a set of primary investments that it makes, a follow-on reserve, a fund size, and a lifespan in years.'''


    ## Create Firm object, set empty portfolio
    def __init__(self, name, primary_investments, follow_on_reserve, fund_size, firm_lifespan_years):
        self.name = name
        self.primary_investments = primary_investments
        self.follow_on_reserve = follow_on_reserve
        self.primary_capital_deployed = 0
        self.follow_on_capital_deployed = 0
        self.fund_size = fund_size
        self.firm_lifespan_years = firm_lifespan_years
        self.portfolio = []
    
    ## Initialize portfolio with full set of companies, with initial investments
    ## Take as input the full set of stages, valuations, and dilutions for each stage so that an individual company can run it's own operations on itself
    def initialize_portfolio(self, stages, valuations, dilution):
        
        ## For each primary investment type (e.g., pre-seed or seed)
        for primary_capital_rounds in self.primary_investments:
            ## What stage are we investing at
            stage_invested = primary_capital_rounds[0]
            
            ## How much are we investing in a company for a single investment
            capital_invested_per_company = primary_capital_rounds[1]

            ## How much total capital are we allocating at that stage
            capital_to_be_allocated = primary_capital_rounds[2]

            ## While we have capital left for this type of investment, initialize a company in the portfolio at that stage
            while capital_to_be_allocated > 0 and capital_to_be_allocated >= capital_invested_per_company:
                
                self.portfolio.append(Company('comp_name' + stage_invested[:2] + str(capital_to_be_allocated), 
                                            stage_invested, 
                                            valuations[stage_invested],
                                            'Alive', 
                                            capital_invested_per_company, 
                                            capital_invested_per_company/valuations[stage_invested],
                                            stages, 
                                            valuations, 
                                            dilution))
                
                ## We have just made an investment, so decrease the amount of remaining capital_to_be_allocated by how much we invested (capital_invested_per_company), and update the amount of primary capital deployed
                capital_to_be_allocated -= capital_invested_per_company
                self.primary_capital_deployed += capital_invested_per_company
        
        # print('----------------------------------------------------------')
        # print('Initialized portfolio with', len(self.portfolio))
        # print('Pre-seed', len(list(filter(lambda x: x.stage == 'Pre-seed', self.portfolio))))
        # print('Seed', len(list(filter(lambda x: x.stage == 'Seed', self.portfolio))))
        # print('Series A', len(list(filter(lambda x: x.stage == 'Series A', self.portfolio))))
        # print('----------------------------------------------------------')
    
    
    ## Concise view of companies alive, failed, acquired
    def concise_portfolio_value(self):
        total_value = 0
        for portco in self.portfolio:
            if portco.state == 'Alive':
                total_value += portco.valuation * portco.firm_ownership
            elif portco.state == 'Failed':
                total_value += 0
            elif portco.state == 'Acquired':
                total_value += portco.valuation * portco.firm_ownership
        return total_value

    
    def detailed_portfolio_value(self):
        total_value = {
            'Alive': 0,
            'Acquired': 0
        }
        for portco in self.portfolio:
            # print(portco.stage, portco.state, '-- val', portco.valuation, 'return', portco.valuation*portco.firm_ownership, 'ic', portco.firm_invested_capital, 'ownership', portco.firm_ownership)
            if portco.state == 'Alive':
                total_value['Alive'] += portco.valuation * portco.firm_ownership
            elif portco.state == 'Acquired':
                total_value['Acquired'] += portco.valuation * portco.firm_ownership
        return total_value

    
    def get_capital_invested(self):
        return self.primary_capital_deployed + self.follow_on_capital_deployed
    
    def get_remaining_follow_on_capital(self):
        return self.follow_on_reserve - self.follow_on_capital_deployed
    
    def get_irr(self):
        # fv = self.concise_portfolio_value()
        # pv = self.primary_capital_deployed + self.follow_on_capital_deployed
        # # print(fv, pv)
        # IRR = ((fv / pv) ** (1/self.firm_lifespan_years)) -1
        # return IRR
        print ('ERROR: ' + 'IRR not implemented')

    def get_MoM(self):
        MoM = round(self.concise_portfolio_value()/self.get_capital_invested(), 1)
        return MoM
    
    def __repr__(self):
        f = {
            'Pre-seed':0,
            'Seed':0,
            'Series A':0,
            'Series B':0,
            'Series C':0,
            'Series D':0,
            'Series E':0,
            'Series F':0,
            'Failed': 0,
            'Acquired': 0
        }
        # f = {
        #     'Alive':0,
        #     'Failed': 0,
        #     'Acquired': 0
        # }
        for comp in self.portfolio:
            if comp.state == 'Alive':
                f[comp.stage] += 1
                # f['Alive'] += 1
            elif comp.state == 'Failed':
                f['Failed'] += 1
            elif comp.state == 'Acquired':
                f['Acquired'] += 1 
        return str(f)
    
    # def check_portfolio(self):
    #     ages = [company.age for company in self.portfolio]
    #     ## print(ages)
        

#############################################################################################################################################
#############################################################################################################################################
################################################           MONTECARLO CLASS        ##########################################################
#############################################################################################################################################
#############################################################################################################################################
class Montecarlo:
    ''' The Montecarlo class simulates a firm's investing lifecycle'''
    
    def __init__(self, num_scenarios, stages, stage_probs, stage_valuations, stage_dilution, firm_attributes):
        
        ## Each scenario is a firm that is simulated from the initialization of their portfolio to the end of their funds lifespan (i.e., after ~10yrs)
        self.num_scenarios = num_scenarios
        self.firm_scenarios = []
        
        ## These are all variables that are needed to calculate the probability of companies moving on to the next stage, the corresponding dilution, and valuations
        self.stages = stages
        self.stage_probs = stage_probs
        self.stage_valuations = stage_valuations
        self.stage_dilution = stage_dilution
        
        ## Firm attributes contain information about firm's entry point (e.g., pre-seed vs seed), fund size, primary vs. follow-on capital
        self.firm_attributes = firm_attributes
    
    def initialize_scenarios(self):

        ## Initialize the firm_scenarios list with a new firm for each simulated scenario
        for i in range(self.num_scenarios):
            
            ## Create the firm object
            new_firm = Firm('Gradient'+ str(i), 
                            self.firm_attributes['primary_investments'], 
                            self.firm_attributes['follow_on_reserve'], 
                            self.firm_attributes['fund_size'], 
                            self.firm_attributes['firm_lifespan_years'])
            
            ## Initialize the portfolio inside that firm
            new_firm.initialize_portfolio(self.stages, self.stage_valuations, self.stage_dilution)
            self.firm_scenarios.append(new_firm)
        
    
    ################################################################################################################################################################################################
    ################################################################ Contains core simulation logic for Montecarlo simulation ######################################################################
    ################################################################################################################################################################################################
    def simulate(self):
        ## Re-seed random number generator 
        random.seed(time.time())

        ## For each firm that we want to simulate, run the simulation
        for firm in self.firm_scenarios:
            ## Iteratively age companies in portfolio, deploying any secondary capital available, and rendering a judgement based on random outcomes about how a company performs
            ## Each portfolio is aged for a set number of periods, which for the purposes of this simulation, is roughly 11 / 1.5yrs = 7 periods
            for period in range(self.firm_attributes['firm_lifespan_periods']):
                
                ## For each company in the portfolio, determine whether to promote, fail, or M&A based on random performance
                for company in firm.portfolio:
                    
                    ## If company is still alive, determine action based on random + probabilities calculation
                    ## Probabilities in order of [next round, fail, M&A]
                    if company.state == 'Alive' and company.get_numerical_stage() < len(self.stages)-1:
                        rand = random.random()
                        # print ('Company', rand, self.stage_probs[company.stage][0])
                        if rand < self.stage_probs[company.stage][2]:
                            company.m_and_a()
                        elif rand < self.stage_probs[company.stage][2] + self.stage_probs[company.stage][1]:
                            company.fail()
                        else: 
                            secondary_capital_consumed = company.promote(firm.get_remaining_follow_on_capital(), self.firm_attributes['pro_rata_at_or_below'])
                            firm.follow_on_capital_deployed += secondary_capital_consumed
                    
                    ## If already failed or acquired, just increment age
                    elif company.state == 'Failed':
                        company.age_company()
                    elif company.state == 'Acquired':
                        company.age_company()
        
            
            ## If we didn't use all of our pro rata b/c our portfolio didn't do well, deploy remaining capital as primary investments
            if firm.get_remaining_follow_on_capital() > 0:
                extra_investments = []
                extra_investment_type = self.firm_attributes['primary_investments'][0]
                num_extra_investments = int(firm.get_remaining_follow_on_capital() // extra_investment_type[1])
                for extra_investment_index in range (num_extra_investments):
                    extra_investments.append(Company('extra' + str(extra_investment_index), 
                                            extra_investment_type[0], 
                                            self.stage_valuations[extra_investment_type[0]],
                                            'Alive', 
                                            extra_investment_type[1], 
                                            extra_investment_type[1]/self.stage_valuations[extra_investment_type[0]],
                                            self.stages, 
                                            self.stage_valuations, 
                                            self.stage_dilution))
                    firm.primary_capital_deployed += extra_investment_type[1]
                    firm.follow_on_reserve -= extra_investment_type[1]

                for period in range(self.firm_attributes['firm_lifespan_periods']):
                    for company in extra_investments:
                        if company.state == 'Alive' and company.get_numerical_stage() < len(self.stages)-1:
                            rand = random.random()
                            # print ('Company', rand, self.stage_probs[company.stage][0])
                            if rand < self.stage_probs[company.stage][2]:
                                company.m_and_a()
                            elif rand < self.stage_probs[company.stage][2] + self.stage_probs[company.stage][1]:
                                company.fail()
                            else: 
                                # No secondary capital available b/c this is the "extra" batch of companies
                                company.promote(0, self.firm_attributes['pro_rata_at_or_below'])
                        elif company.state == 'Failed':
                            company.age_company()
                        elif company.state == 'Acquired':
                            company.age_company()
                firm.portfolio += extra_investments


    def get_IRR_return_outcomes(self):
        print('ERROR: ' + 'IRR not implemented')

    def get_MoM_return_outcomes(self):
        outcomes = []
        for firm in self.firm_scenarios:
            outcomes.append(firm.get_MoM())
        return outcomes
    
    def get_median_return_outcome(self, type):
        outcomes = []
        if type == 'MoM':
            outcomes = self.get_MoM_return_outcomes()
        elif type == 'IRR':
            outcomes = self.get_IRR_return_outcomes()
        if len(outcomes) % 2 == 0:
            return (outcomes[len(outcomes)//2] + outcomes[len(outcomes)//2 - 1])/2
        else:
            return outcomes[len(outcomes)//2]

    def get_exact_return_outcomes(self):
        outcomes = []
        for firm in self.firm_scenarios:
            outcomes.append(firm.concise_portfolio_value())
        return outcomes

    
    def performance_quartiles(self):
        
        outcomes = self.get_MoM_return_outcomes()
        performance = {}
        
        performance['25'] = [str(np.percentile(outcomes, 25))]
        performance['50'] = [str(np.percentile(outcomes, 50))]
        performance['75'] = [str(np.percentile(outcomes, 75))]
        performance['90'] = [str(np.percentile(outcomes, 90))]
        performance['95'] = [str(np.percentile(outcomes, 95))]

        return performance


    

    def montecarlo_histogram(self):
        ''' Histogram for montecarlo simulation - very ugly code optimized for  being able to combine multiple hisograms across different simulations'''
        
        histogram = {}
        outcomes = self.get_MoM_return_outcomes()
        hist_size = .25
        counter = 0.0
        upper_limit = 15
        while counter < upper_limit:
            relevant = list(filter(lambda y: counter <= y < counter+hist_size, outcomes))
            histogram[f"{counter}-{counter+hist_size}"] = [str(len(relevant))]
            counter += hist_size
        
        return histogram

    
    def get_montecarlo_outcomes_overview(self):
        return {
            'Num Simulations': self.num_scenarios,
            'Fund Size': self.firm_attributes['fund_size'],
            'Initial Investment': self.firm_attributes['primary_investments'],
            'Follow on': self.firm_attributes['follow_on_reserve'],
            'Median MoM': self.get_median_return_outcome('MoM')
        }

    def print_results(self):
        print(f"Montecarlo Simulation Results ({self.num_scenarios} scenarios):")
        for i, scenario in enumerate(self.firm_scenarios, start=1):
            print(f"Scenario {i}: {scenario}")
            



#######################################################################################################################################################
############################################# Helper functions for running variations of MC sims ######################################################
#######################################################################################################################################################


stages = ['Pre-seed', 'Seed', 'Series A', 'Series B', 'Series C', 'Series D', 'Series E', 'Series F']
        
#Probability distribution: next round, fail, m&a,
stage_probs = {
    'Pre-seed':    [.35, .5, .1],
    'Seed':        [.35, .45, .2], 
    'Series A':    [.6, .25, .15],
    'Series B':    [.5, .25, .25],
    'Series C':    [.4, .35, .25],
    'Series D':    [.4, .25, .35],
    'Series E':    [.4, .25, .35],
    'Series F':    [.2, .2, .6] 
}

stage_dilution = {
    'Seed': 0.20,
    'Series A': 0.22,
    'Series B': 0.2,
    'Series C': 0.15,
    'Series D': 0.1,
    'Series E': 0.08,
    'Series F': 0.08
}

stage_valuations = {
    'Pre-seed': 15,
    'Seed': 30,
    'Series A': 70,
    'Series B': 200,
    'Series C': 500,
    'Series D': 750,
    'Series E': 1500,
    'Series F': 10000
}

lifespan_periods = 7
lifespan_years = 11
num_scenarios = 1000


def build_firm_attributes_for_simulation(pre_seed_percentage, pre_seed_investment_amount, seed_percentage, seed_investment_amount, primary, follow_on, total_fund_size, pro_rata_at_or_below):
    
    attributes = {
        'primary_investments': [], ## round, invested capital, total capital allocated to this stage
        'follow_on_reserve':follow_on, ## total dollars reserved for fdund size
        'fund_size': total_fund_size,
        'pro_rata_at_or_below': stage_valuations[pro_rata_at_or_below],
        'firm_lifespan_periods': lifespan_periods,
        'firm_lifespan_years': lifespan_years
    }
    

    ## Check to make sure the firm you are building is valid
    if pre_seed_percentage + seed_percentage != 1:
        print('pre_seed + seed percentage split does not equal 100%')
        return
    if primary + follow_on != total_fund_size:
        print('primary + follow_on does not equal total fund size')
        return

    investments = []
    total_pre_seed_invested_capital = 0
    total_seed_invested_capital = 0
    if pre_seed_percentage > 0:
        # print(pre_seed_percentage)
        total_pre_seed_invested_capital = int(math.floor(pre_seed_percentage*primary/pre_seed_investment_amount)*pre_seed_investment_amount)
        investments.append(('Pre-seed', pre_seed_investment_amount, total_pre_seed_invested_capital))
    if seed_percentage >0:
        total_seed_invested_capital = int(math.floor(seed_percentage*primary/seed_investment_amount)*seed_investment_amount)
        investments.append(('Seed', seed_investment_amount, total_seed_invested_capital))
    
    ## If there is a small amount of extra capital that won't fit into primary investments, reserve it for follow_on
    # print('primary', primary, 'seed', total_pre_seed_invested_capital, 'pre_seed', total_seed_invested_capital)
    revised_follow_on = follow_on + (primary - total_pre_seed_invested_capital - total_seed_invested_capital)

    attributes['follow_on_reserve'] = revised_follow_on
    attributes['primary_investments'] = investments

    ## Last check to ensure that all calc's were completed successfully, and that firm attributes are valid
    total_capital_invested = 0
    for investment_type in attributes['primary_investments']:
        total_capital_invested += investment_type[2]
    total_capital_invested += attributes['follow_on_reserve']
    if total_capital_invested != total_fund_size:
        print('Error: Total capital allocated does not match fund size')
        return

    return attributes



def run_montecarlo(firm_attributes):
    ''' Run a montecarlo simulation with a specified set of firm attributes'''

    ## Perform checks that firm attributes are properly set
    ## 1st check ensures that the total capital set to be allocated through reserves and primary investments is equal to the total fund size
    if firm_attributes['follow_on_reserve'] + sum(investment[-1] for investment in firm_attributes['primary_investments']) != firm_attributes['fund_size']:
        print('Error: Fund size does not match capital allocation', firm_attributes)
        return
    
    ## Second check ensures that there are enough periods for a company to possibly reach the final stage (e.g., Series F), and also that there are the right number of stage definitions for stage probabilities and valuations
    if firm_attributes['firm_lifespan_periods'] != len(stages)-1 or len(stages) != len(stage_valuations.keys()) or len(stages) != len(stage_probs.keys()):
        print('Error: Stages do not match probabilities, valuations, or firm lifespan', firm_attributes)
        return
    
    ## Initialize the Montecarlo Simulation
    montecarlo = Montecarlo(num_scenarios, stages, stage_probs, stage_valuations, stage_dilution, firm_attributes)
    montecarlo.initialize_scenarios()
    montecarlo.simulate()
    
    print('Overview of simulation outputs:', montecarlo.get_montecarlo_outcomes_overview(), '\n')
    
    return montecarlo



if __name__ == '__main__':
    print('\n')

    firm1 = build_firm_attributes_for_simulation(.3, 1.5, .7, 4, 180, 20, 200, 'Series A')
    print('Firm attributes defined as:', firm1, '\n')
    
    simulation = run_montecarlo(firm1)
    
    print ('Histogram')
    print(simulation.montecarlo_histogram())
    print('\nQuartiles')
    print(simulation.performance_quartiles())
















## Old Stuff
##########################################
##########################################
    # }
    # firm_attributes2 = {
    #     'primary_investments': [['Seed', 4, 176]], ## round, invested capital, total capital allocated to this stage
    #     'follow_on_reserve':25, ## total dollars reserved for fdund size
    #     'fund_size': 200,
    #     'pro_rata_at_or_below': 30,
    #     'firm_lifespan_periods': 7,
    #     'firm_lifespan_years': 11
    # }
    # firm_attributes3 = {
    #     'primary_investments': [['Pre-seed', 1.5, 12],['Seed', 4, 136], ['Series A', 10, 50]], ## round, invested capital, total capital allocated to this stage
    #     'follow_on_reserve':50, ## total dollars reserved for fdund size
    #     'fund_size': 200,
    #     'pro_rata_at_or_below': 30,
    #     'firm_lifespan_periods': 7,
    #     'firm_lifespan_years': 11
    # }
    # firm_attributes4 = {
    #     'primary_investments': [['Seed', 4, 300]], ## round, invested capital, total capital allocated to this stage
    #     'follow_on_reserve':0, ## total dollars reserved for fdund size
    #     'fund_size': 300,
    #     'pro_rata_at_or_below': 200,
    #     'firm_lifespan_periods': 7,
    #     'firm_lifespan_years': 11
    # }


    # helper_combine([run_montecarlo(firm_attributes1), run_montecarlo(firm_attributes2), run_montecarlo(firm_attributes3), run_montecarlo(firm_attributes4)])
    # helper_combine([run_montecarlo(firm_attributes1), run_montecarlo(firm_attributes2), run_montecarlo(firm_attributes3)])

    # helper_combine([run_montecarlo(firm_attributes1)])
    
    # firm_attributes_mold = {
    #     'primary_investments': None, ## round, invested capital, total capital allocated to this stage
    #     'follow_on_reserve':0, ## total dollars reserved for fdund size
    #     'fund_size': 200,
    #     'pro_rata_at_or_below': 30,
    #     'firm_lifespan_periods': 7,
    #     'firm_lifespan_years': 11 
    # }
    

    # stage_splits = [(1.0, 0), (.9, .1), (.8, .2), (.7, .3), (.6, .4), (.5, .5), (.4, .6), (.3, .7), (.2, .8), (.1, .9), (0, 1.0)]
    # stage_investments = (1.5, 4)
    
    # outcomes = []
    # for split in stage_splits:
    #     fs = 200
    #     reserve = 50
    #     pro_rata_at_or_below = 70
    #     print('Split:', 'Pre-seed', split[0], 'Seed', split[1])
    #     pre_seed_capital = split[0]*(fs-reserve)
    #     seed_capital = split[1]*(fs-reserve)
    #     num_seed_invesments = seed_capital // stage_investments[1]
    #     num_pre_seed_investments = pre_seed_capital // stage_investments[0]
    #     extra = (fs-reserve)-num_pre_seed_investments*stage_investments[0]-num_seed_invesments*stage_investments[1]
    #     reserve += extra

    #     print('Pre-seed:', num_pre_seed_investments*stage_investments[0], 'Seed:', num_seed_invesments*stage_investments[1], 'Extra:', extra)

    #     firm_attributes_mold['primary_investments'] = [['Seed', stage_investments[1], num_seed_invesments*stage_investments[1]], ['Pre-seed', stage_investments[0], num_pre_seed_investments*stage_investments[0]]]
    #     firm_attributes_mold['follow_on_reserve'] = reserve
    #     firm_attributes_mold['pro_rata_at_or_below'] = pro_rata_at_or_below
    #     firm_attributes_mold['fund_size'] = fs
    #     outcomes.append(run_montecarlo(firm_attributes_mold))
    # helper_combine(outcomes)

    
    #----------------------------------------------------
    #----------------------------------------------------
    # outcomes = []
    # fs = 200
    # reserve = 50
    # up_to_valuation = 70
    # pre_seed_percent = .1
    # seed_percent = .9
    # pre_seed_investment = 1.5
    # seed_investment = 4
    # # print('here1')
    # for x in [.25, .5, .75, 1, 1.25, 1.5, 1.75, 2, 2.25]:
        
    #     # print('status:', (fs)//x, ((fs)//x)*x, x)
    #     # print('here2')
    #     primary_avaliable = fs-reserve
    #     pre_seed_capital = math.floor(pre_seed_percent*primary_avaliable)
    #     seed_capital = math.floor(seed_percent*primary_avaliable)
    #     psi = pre_seed_investment*x
    #     si = seed_investment*x

    #     firm_attributes_mold['primary_investments'] = [['Seed', si, seed_capital], ['Pre-seed', psi, pre_seed_capital]]
    #     firm_attributes_mold['fund_size'] = fs
    #     firm_attributes_mold['follow_on_reserve'] = fs - seed_capital-pre_seed_capital
    #     outcomes.append(run_montecarlo(firm_attributes_mold))
    
    # helper_combine(outcomes)
    #---------------------------------------------------
    #---------------------------------------------------


    # outcomes = []
    # fs = 200
    # reserve = 50
    # up_to_valuation = 70
    # for x in [i/4 for i in range(4,31)]:
    #     print('status:', (fs-reserve)//x, ((fs-reserve)//x)*x, x)
    #     to_be_deployed = ((fs-reserve)//x)*x
    #     firm_attributes_mold['primary_investments'] = [['Seed', x, to_be_deployed]]
    #     firm_attributes_mold['fund_size'] = fs
    #     firm_attributes_mold['pro_rata_at_or_below'] = up_to_valuation
    #     firm_attributes_mold['follow_on_reserve'] = fs - to_be_deployed
    #     outcomes.append(run_montecarlo(firm_attributes_mold))
    # helper_combine(outcomes)


    # outcomes = []
    # for x in [2500, 5000, 7500, 10000, 12500, 15000]:
    #     fs = 200
    #     reserve = 50
    #     firm_attributes_mold['primary_investments'] = [['Seed', 4, 150]]
    #     firm_attributes_mold['fund_size'] = 200
    #     firm_attributes_mold['follow_on_reserve'] = 50
    #     firm_attributes_mold['pro_rata_at_or_below'] = 70
    #     outcomes.append(run_montecarlo(firm_attributes_mold, x))
    # helper_combine(outcomes)


    # outcomes = []
    
    # for z in [.1, .2]:
    # for y in [30, 70, 200, 500]:
    #     for x in [0,40, 50, 60]:
    #         fs = 200
    #         reserve = x
    #         up_to_valuation = y
    #         amount_invested = (1.5, 4)

    #         seed_capital = ((1-.1)*(fs-reserve)//amount_invested[1])*amount_invested[1]
    #         pre_seed_capital = (.1*(fs-reserve)//amount_invested[0])*amount_invested[0]
    #         amount_deployed = seed_capital + pre_seed_capital
    #         actual_reserve = fs - amount_deployed
    #         print('ammount deployed', amount_deployed, 'actual reserve', actual_reserve)    


    #         firm_attributes_mold['primary_investments'] = [['Seed', amount_invested[1],seed_capital ], ['Pre-seed', amount_invested[0], pre_seed_capital]]
    #         firm_attributes_mold['fund_size'] = 200
    #         firm_attributes_mold['follow_on_reserve'] = actual_reserve
    #         firm_attributes_mold['pro_rata_at_or_below'] = up_to_valuation
    #         print('pre_seed_capital:', pre_seed_capital, 'seed_capital:', seed_capital, 'actual_reserve:', actual_reserve)
    #         outcomes.append(run_montecarlo(firm_attributes_mold))
    # helper_combine(outcomes)


    





