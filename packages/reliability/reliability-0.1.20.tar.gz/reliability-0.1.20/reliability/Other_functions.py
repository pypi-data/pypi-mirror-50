'''
Other Functions

This is a collection of many tools that did not otherwise fit within their own module.
Included functions are:
one_sample_proportion - Calculates the upper and lower bounds of reliability for a given number of trials and successes.
two_proportion_test - Calculates whether the difference in test results between two samples is statistically significant.
sample_size_no_failures - used to determine the sample size required for a test in which no failures are expected, and the desired
    outcome is the lower bound on the reliability based on the sample size and desired confidence interval.
sequential_sampling_chart - plots the accept/reject boundaries for a given set of quality and risk levels. If supplied, the test results
    are also plotted on the chart.
reliability_growth - uses the Duane method to find the instantaneous MTBF and produce a reliability growth plot.
optimal_replacement_time - Calculates the cost model to determine how cost varies with replacement time. The cost model may be NHPP (as good as old) or HPP (as good as new). Default is HPP.
convert_dataframe_to_grouped_lists - groups values in a 2-column dataframe based on the values in the left column and returns those groups in a list of lists
'''
def one_sample_proportion(trials=None,successes=None,CI=0.95):
    '''
    Calculates the upper and lower bounds of reliability for a given number of trials and successes.

    inputs:
    trials - the number of trials which were conducted
    successes - the number of trials which were successful
    CI - the desired confidence interval. Defaults to 0.95 for 95% CI.

    returns: lower, upper - Confidence interval limits.
        will return nan for lower or upper if only one sided CI is calculated (ie. when successes=0 or successes=trials).
    '''
    import scipy.stats as ss
    if trials is None or successes is None:
        raise ValueError('You must specify the number of trials and successes.')
    if successes>trials:
        raise ValueError('successes cannot be greater than trials')
    if successes==0 or successes==trials: #calculate 1 sided CI in these cases
        n = 1
    else:
        n = 2
    V1_lower = 2*successes
    V2_lower = 2*(trials-successes+1)
    alpha_lower = (1-CI)/n
    F_lower = ss.f.ppf(alpha_lower, V1_lower, V2_lower)
    LOWER_LIM = (V1_lower*F_lower)/(V2_lower+V1_lower*F_lower)

    V1_upper = 2*(successes+1)
    V2_upper = 2*(trials-successes)
    alpha_upper = 1 - alpha_lower
    F_upper = ss.f.ppf(alpha_upper, V1_upper, V2_upper)
    UPPER_LIM = (V1_upper*F_upper)/(V2_upper+V1_upper*F_upper)

    return LOWER_LIM,UPPER_LIM #will return nan for lower or upper if only one sided CI is calculated (ie. when successes=0 or successes=trials).

def two_proportion_test(sample_1_trials=None,sample_1_successes=None,sample_2_trials=None,sample_2_successes=None,CI=0.95):
    '''
    Calculates whether the difference in test results between two samples is statistically significant. For example, assume we have
    a poll of respondents in which 27/40 people agreed, and another poll in which 42/80 agreed. This test will determine if the difference
    is statistically significant for the given sample sizes at the specified confidence level.

    inputs:
    sample_1_trials - number of trials in the first sample
    sample_1_successes - number of successes in the first sample
    sample_2_trials - number of trials in the second sample
    sample_2_successes - number of successes in the second sample
    CI - desired confidence interval. Defaults to 0.95 for 95% CI.

    returns:
    lower,upper,result - lower and upper are bounds on the difference. If the bounds do not include 0 then it is a statistically significant difference.
    '''
    import scipy.stats as ss
    if CI<0.5 or CI>=1:
        raise ValueError('CI must be between 0.5 and 1. Default is 0.95')
    if sample_1_trials is None or sample_1_successes is None or sample_2_trials is None or sample_2_successes is None:
        raise ValueError('You must specify the number of trials and successes for both samples.')
    if sample_1_successes>sample_1_trials or sample_2_successes>sample_2_trials:
        raise ValueError('successes cannot be greater than trials')
    p1 = sample_1_successes/sample_1_trials
    p2 = sample_2_successes/sample_2_trials
    diff = p1-p2
    Z = ss.norm.ppf(1-((1-CI)/2))
    k = Z*((p1*(1-p1)/sample_1_trials)+(p2*(1-p2)/sample_2_trials))**0.5
    lower = diff-k
    upper = diff+k
    if lower<0 and upper>0:
        result='non-significant'
    else:
        result='significant'
    return lower,upper,result

def sample_size_no_failures(reliability,CI=0.95,lifetimes=1,weibull_shape=1):
    '''
    This is used to determine the sample size required for a test in which no failures are expected, and the desired
    outcome is the lower bound on the reliability based on the sample size and desired confidence interval.

    inputs:
    reliability - lower bound on product reliability (between 0 and 1)
    CI - confidence interval of result (between 0.5 and 1). Defaults to 0.95 for 95% CI.
    lifetimes - if testing the product for multiple lifetimes then more failures are expected so a smaller sample
        size will be required to demonstrate the desired reliability (assuming no failures). Conversely, if testing for
        less than one full lifetime then a larger sample size will be required. Default is 1.
    weibull_shape - if the weibull shape (beta) of the failure mode is known, specify it here. Otherwise leave the
        default of 1 for the exponential distribution.

    returns:
    number of items required in the test. This will always be an integer (rounded up).
    '''
    import numpy as np
    import math
    if CI<0.5 or CI>=1:
        raise ValueError('CI must be between 0.5 and 1')
    if reliability<=0 or reliability>=1:
        raise ValueError('Reliability must be between 0 and 1')
    if weibull_shape<0:
        raise ValueError('Weibull shape must be greater than 0. Default (exponential distribution) is 1. If unknown then use 1.')
    if lifetimes>5:
        print('Testing for greater than 5 lifetimes is highly unlikely to result in zero failures.')
    if lifetimes<=0:
        raise ValueError('lifetimes must be >0. Default is 1. No more than 5 is recommended due to test feasibility.')
    n = math.ceil((np.log(1-CI))/(lifetimes**weibull_shape*np.log(reliability))) #rounds up to nearest integer
    return n

def sequential_samling_chart(p1,p2,alpha,beta,show_plot = True, print_results=True, test_results=None,max_samples=100):
    '''
    This function plots the accept/reject boundaries for a given set of quality and risk levels. If supplied, the test results are also
    plotted on the chart.

    inputs:
    p1 - producer_quality. The acceptable failure rate for the producer (typical around 0.01)
    p2 - consumer_quality. The acceptable failure rate for the consumer (typical around 0.1)
    alpha - producer_risk. Producer's CI = 1-alpha (typically 0.05)
    beta - consumer_risk. Consumer's CI = 1-beta (typically 0.1)
    test_results - array or list of binary test results. eg. [0,0,0,1] for 3 successes and 1 failure. Default=None
    show_plot - True/False. Defaults to True.
    print_results - True/False. Defaults to True.
    max_samples - the x_lim of the plot. optional input. Default=100.

    outputs:
    The sequential sampling chart - A plot of sequential sampling chart with decision boundaries. test_results are only plotted on the chart
    if provided as an input.
    results - a dataframe of tabulated decision results.

    '''

    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd

    if type(test_results)==list:
        F = np.array(test_results)
    elif type(test_results)==np.ndarray:
        F = test_results
    elif test_results is None:
        F = None
    else:
        raise ValueError('test_results must be a binary array or list with 1 as failures and 0 as successes. eg. [0 0 0 1] for 3 successes and 1 failure.')

    a = 1-alpha
    b = 1-beta
    d = np.log(p2/p1)+np.log((1-p1)/(1-p2))
    h1 = np.log((1-a)/b)/d
    h2 = np.log((1 - b) / a) / d
    s = np.log((1-p1)/(1-p2))/d

    xvals = np.arange(max_samples+1)
    rejection_line = s*xvals-h1
    acceptance_line = s*xvals+h2
    acceptance_line[acceptance_line<0]=0

    upper_line = np.ones_like(xvals)*(s * max_samples - h1)
    lower_line_range = np.linspace(-h2/s,max_samples,max_samples+1)
    acceptance_line2 = s*lower_line_range+h2 #this is the visible part of the line that starts beyond x=0

    acceptance_array = np.asarray(np.floor(s*xvals+h2), dtype=int)
    rejection_array = np.asarray(np.ceil(s*xvals-h1), dtype=int)
    for i,x in enumerate(xvals): # this replaces cases where the criteria exceeds the number of samples
        if rejection_array[i]>x:
            rejection_array[i]=-1

    data = {'Samples': xvals,'Failures to accept': acceptance_array,'Failures to reject': rejection_array}
    df = pd.DataFrame(data, columns=['Samples', 'Failures to accept','Failures to reject'])
    df.set_index('Samples', inplace=True)
    df.loc[df['Failures to accept'] < 0, 'Failures to accept'] = 'x'
    df.loc[df['Failures to reject'] < 0, 'Failures to reject'] = 'x'

    if print_results==True:
        print(df)

    if show_plot==True:
        #plots the results of tests if they are specified
        if type(F)==np.ndarray:
            if all(F) not in [0,1]:
                raise ValueError('test_results must be a binary array or list with 0 as failures and 1 as successes. eg. [0 0 0 1] for 3 successes and 1 failure.')
            nx = []
            ny = []
            failure_count = 0
            sample_count = 0
            for f in F:
                if f==0:
                    sample_count+=1
                    nx.append(sample_count)
                    ny.append(failure_count)
                elif f==1:
                    sample_count+=1
                    nx.append(sample_count)
                    ny.append(failure_count)
                    failure_count+=1
                    nx.append(sample_count)
                    ny.append(failure_count)
                else:
                    raise ValueError('test_results must be a binary array or list with 0 as failures and 1 as successes. eg. [0 0 0 1] for 3 successes and 1 failure.')
            plt.plot(nx, ny,label='test results')

        #plots the decision boundaries and shades the areas red and green
        plt.plot(lower_line_range,acceptance_line2,linestyle='--',color='green')
        plt.plot(xvals,rejection_line,linestyle='--',color='red')
        plt.fill_between(xvals,rejection_line,upper_line,color='red',alpha=0.3,label='Reject sample')
        plt.fill_between(xvals, acceptance_line, rejection_line, color='gray', alpha=0.1, label='Keep Testing')
        plt.fill_between(lower_line_range, 0, acceptance_line2, color='green', alpha=0.3, label='Accept Sample')
        plt.ylim([0,max(rejection_line)])
        plt.xlim([0,max(xvals)])
        plt.xlabel('Number of samples tested')
        plt.ylabel('Number of failures from samples tested')
        plt.title('Sequential sampling decision boundaries')
        plt.legend()
        plt.show()
    return df

def reliability_growth(times,xmax=None,target_MTBF=None,show_plot=True,print_results=True,**kwargs):
    '''
    Uses the Duane method to find the instantaneous MTBF and produce a reliability growth plot.

    inputs:
    times - array of list of failure times
    xmax - xlim to plot up to. Default is 1.5*max(times)
    target_MTBF - specify the target MTBF to obtain the total time on test required to reach it.
    show_plot - True/False. Defaults to true. Other keyword arguments are passed to the plot for style
    print_results - True/False. Defaults to True.

    returns:
    If print_results is True it will print a summary of the results
    [Lambda, beta, time_to_target] - Array of results. Time to target is only returned if target_MTBF is specified.
    If show_plot is True, it will plot the reliability growth. Use plt.show() to show the plot.
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    if type(times)==list:
        times = np.sort(np.array(times))
    elif type(times)==np.ndarray:
        times = np.sort(times)
    else:
        raise ValueError('times must be an array or list of failure times')
    if min(times)<0:
        raise ValueError('failure times cannot be negative. times must be an array or list of failure times')
    if xmax==None:
        xmax=int(max(times)*1.5)
    if 'color' in kwargs:
        c = kwargs.pop('color')
    else:
        c = 'steelblue'

    N = np.arange(1,len(times)+1)
    theta_c = times/N
    ln_t = np.log(times)
    ln_theta_c = np.log(theta_c)
    z = np.polyfit(ln_t,ln_theta_c,1) #fit a straight line to the data to get the parameters lambda and beta
    beta = 1-z[0]
    Lambda = np.exp(-z[1])
    xvals = np.linspace(0,xmax,1000)
    theta_i = (xvals**(1-beta))/(Lambda*beta) #the smooth line
    theta_i_points = (times**(1-beta))/(Lambda*beta) #the failure times highlighted along the line
    output = [Lambda, beta] #returns lambda and beta

    if print_results==True:
        print('Reliability growth model parameters:\nlambda:',Lambda,'\nbeta:',beta)

    if target_MTBF is not None:
        t_target = (target_MTBF * Lambda * beta) ** (1 / (1 - beta))
        output.append(t_target)  # also returns time to target MTBF if a target is specified
        print('Time to reach target MTBF:',t_target)

    if show_plot==True:
        plt.plot(xvals,theta_i,color=c,**kwargs)
        plt.plot(times,theta_i_points,'o',color=c,alpha=0.5)
        if target_MTBF is not None:
            plt.plot([0, t_target, t_target], [target_MTBF, target_MTBF, 0], 'red', label='Reliability target', linewidth=1)
        plt.title('Reliability Growth')
        plt.xlabel('Total time on test')
        plt.ylabel('Instantaneous MTBF')
        plt.xlim([0,max(xvals)])
        plt.ylim([0,max(theta_i)*1.2])
    return output

def optimal_replacement_time(cost_PM, cost_CM, weibull_alpha, weibull_beta, show_plot=True, print_results=True, q=0, **kwargs):
    '''
    Calculates the cost model to determine how cost varies with replacement time.
    The cost model may be HPP (good as new replacement) or NHPP (as good as old replacement). Default is HPP.

    inputs:
    Cost_PM - cost of preventative maintenance (must be smaller than Cost_CM)
    Cost_CM - cost of corrective maintenance (must be larger than Cost_PM)
    weibull_alpha - scale parameter of the underlying Weibull distribution
    weibull_beta - shape parameter of the underlying Weibull distribution. Should be greater than 1 otherwise conducting PM is not economical.
    q - restoration factor. q=1 is Power Law NHPP (as good as old), q=0 is HPP (as good as new). Default is q=0 (as good as new).
    show_plot - True/False. Defaults to True. Other plotting keywords are also accepted and used.
    print_results - True/False. Defaults to True

    outputs:
    [ORT, min_cost] - the optimal replacement time and minimum cost per unit time in an array
    Plot of cost model if show_plot is set to True. Use plt.show() to display it.
    Printed results if print_results is set to True.
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    import warnings
    from scipy import integrate
    if 'color' in kwargs:
        c = kwargs.pop('color')
    else:
        c = 'steelblue'
    if cost_PM>cost_CM:
        raise ValueError('Cost_PM must be less than Cost_CM otherwise preventative maintenance should not be conducted.')
    if weibull_beta<1:
        warnings.warn('weibull_beta is < 1 so the hazard rate is decreasing, therefore preventative maintenance should not be conducted.')

    if q == 1: #as good as old
        alpha_multiple = 4 #just used for plot limits
        t = np.linspace(1, weibull_alpha * alpha_multiple, 100000)
        CPUT = ((cost_PM*(t/weibull_alpha)**weibull_beta)+cost_CM)/t
        ORT = weibull_alpha*((cost_CM/(cost_PM*(weibull_beta-1)))**(1/weibull_beta))
        min_cost = ((cost_PM * (ORT / weibull_alpha) ** weibull_beta) + cost_CM) / ORT
    elif q == 0: #as good as new
        alpha_multiple = 3
        t = np.linspace(1, weibull_alpha * alpha_multiple, 10000)
        CPUT = []  # cost per unit time
        R = lambda x: np.exp(-((x/weibull_alpha)**weibull_beta))
        for T in t:
            SF = np.exp(-((T/weibull_alpha)**weibull_beta))
            integral_R, error = integrate.quad(R, 0, T)
            CPUT.append((cost_PM * SF + cost_CM * (1 - SF)) / integral_R)
            idx = np.argmin(CPUT)
            min_cost = CPUT[idx]  # minimum cost per unit time
            ORT = t[idx]  # optimal replacement time
    else:
        raise ValueError('q must be 0 or 1. Default is 0. Use 0 for "as good as new" and use 1 for "as good as old".')

    if min_cost<1:
        min_cost_rounded = round(min_cost, -int(np.floor(np.log10(abs(min_cost)))) + 1)  # this rounds to exactly 2 sigfigs no matter the number of preceding zeros
    else:
        min_cost_rounded = round(min_cost,2)
    ORT_rounded = round(ORT, 2)

    if print_results==True:
        if q==0:
            print('Cost model assuming as good as new replacement (q=0):')
        else:
            print('Cost model assuming as good as old replacement (q=1):')
        print('The minimum cost per unit time is',min_cost_rounded,'\nThe optimal replacement time is',ORT_rounded)

    if show_plot==True:
        plt.plot(t,CPUT,color=c,**kwargs)
        plt.plot(ORT,min_cost,'o',color=c)
        text_str = str('\nMinimum cost per unit time is '+str(min_cost_rounded)+'\nOptimal replacement time is '+str(ORT_rounded))
        plt.text(ORT,min_cost,text_str,verticalalignment='top')
        plt.xlabel('Replacement time')
        plt.ylabel('Cost per unit time')
        plt.title('Optimal replacement time estimation')
        plt.ylim([0,min_cost*2])
        plt.xlim([0,weibull_alpha*alpha_multiple])
    return [ORT,min_cost]

def convert_dataframe_to_grouped_lists(input_dataframe):
    '''
    Accepts a dataframe containing 2 columns
    This function assumes the identifying column is the left column
    returns:
    lists , names - lists is a list of the grouped lists
                  - names is the identifying values used to group the lists from the first column

    Example usage:
    #create sample data
    import pandas as pd
    data = {'outcome': ['Failed', 'Censored', 'Failed', 'Failed', 'Censored'],
        'cycles': [1253,1500,1342,1489,1500]}
    df = pd.DataFrame(data, columns = ['outcome', 'cycles'])
    #usage of the function
    lists,names = convert_dataframe_to_grouped_lists(df)
    print(names[1]) >>> Failed
    print(lists[1]) >>> [1253, 1342, 1489]
    '''
    df = input_dataframe
    column_names = df.columns.values
    if len(column_names)>2:
        raise ValueError('Dataframe contains more than 2 columns. There should only be 2 columns with the first column containing the labels to group by and the second containing the values to be returned in groups.')
    grouped_lists = []
    group_list_names = []
    for key, items in df.groupby(column_names[0]):
        values = list(items.iloc[:,1].values)
        grouped_lists.append(values)
        group_list_names.append(key)
    return grouped_lists,group_list_names
