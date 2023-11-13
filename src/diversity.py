import pandas as pd
from sample_pf import *

gmm_output = pd.read_csv('probs_5_components.csv')
gmm_output

# turn pf into %%
def get_pf_percentage(pf):
    
    total = sum(pf.values())
    pf_perc = {stock : amount/total for stock, amount in pf.items()}

    return pf_perc

def get_diversity_vector(pf_perc):

    diversity_vector = [0, 0, 0, 0, 0]

    for stock, perc in pf_perc.items():
        row = gmm_output.loc[gmm_output['Symbol'] == stock].values.flatten().tolist()
        if (len(row) == 0):
            print("missing stock: ", stock)
            return None

        ticker, a, b, c, d, e = row

        diversity_vector[0] += a * perc
        diversity_vector[1] += b * perc
        diversity_vector[2] += c * perc
        diversity_vector[3] += d * perc
        diversity_vector[4] += e * perc
        
    return diversity_vector

def get_diversity_vector_withoutZero(pf_perc):

    diversity_vector = [0, 0, 0]

    for stock, perc in pf_perc.items():
        row = gmm_output.loc[gmm_output['Symbol'] == stock].values.flatten().tolist()
        if (len(row) == 0):
            print("missing stock: ", stock)
            return None

        ticker, a, b, c, d, e = row

        diversity_vector[0] += a * perc
        diversity_vector[1] += b * perc
        diversity_vector[2] += d * perc
        
    return diversity_vector

def get_diversity_score(diversity_vector):
    size = len(diversity_vector)
    perfect_diversity = [(1 / size) for i in range(len(diversity_vector))]

    score = 0
    for i in range(len(diversity_vector)):
        score += abs(diversity_vector[i] - perfect_diversity[i])

    return 1 / score

print("***********High Diversity***********")
print()

HD = [HDp1, HDp2, HDp3]

for i, pf in enumerate(HD):

    print(f"HDp{i+1}_perc")
    print()

    perc = get_pf_percentage(pf)
    diversity = get_diversity_vector(perc)
    score = get_diversity_score(diversity)

    print("Portfolio Percentage: ", perc)
    print("Diversity Vector: ", diversity)
    print("Diversity Score: ", score)

    print()

print("***********Mid Diversity***********")
print()

MD = [MDp1, MDp2, MDp3, MDp4]

for i, pf in enumerate(MD):

    print(f"MDp{i+1}_perc")
    print()

    perc = get_pf_percentage(pf)
    diversity = get_diversity_vector(perc)
    score = get_diversity_score(diversity)

    print("Portfolio Percentage: ", perc)
    print("Diversity Vector: ", diversity)
    print("Diversity Score: ", score)

    print()

print("***********Low Diversity***********")
print()

LD = [LDp1, LDp2, LDp3, LDp4, LDp5]

for i, pf in enumerate(LD):

    print(f"LDp{i+1}_perc")
    print()

    perc = get_pf_percentage(pf)
    diversity = get_diversity_vector(perc)
    score = get_diversity_score(diversity)


    print("Portfolio Percentage: ", perc)
    print("Diversity Vector: ", diversity)
    print("Diversity Score: ", score)

    print()

print("***********High Diversity No Col 3 and 5***********")
print()

HD = [HDp1, HDp2, HDp3]

for i, pf in enumerate(HD):

    print(f"HDp{i+1}_perc")
    print()

    perc = get_pf_percentage(pf)
    diversity = get_diversity_vector_withoutZero(perc)
    score = get_diversity_score(diversity)

    print("Portfolio Percentage: ", perc)
    print("Diversity Vector: ", diversity)
    print("Diversity Score: ", score)

    print()


print("***********Mid Diversity No Col 3 and 5***********")
print()

MD = [MDp1, MDp2, MDp3, MDp4]

for i, pf in enumerate(MD):

    print(f"MDp{i+1}_perc")
    print()

    perc = get_pf_percentage(pf)
    diversity = get_diversity_vector_withoutZero(perc)
    score = get_diversity_score(diversity)


    print("Portfolio Percentage: ", perc)
    print("Diversity Vector: ", diversity)
    print("Diversity Score: ", score)

    print()

print("***********Low Diversity No Col 3 and 5***********")
print()

LD = [LDp1, LDp2, LDp3, LDp4, LDp5]

for i, pf in enumerate(LD):

    print(f"LDp{i+1}_perc")
    print()

    perc = get_pf_percentage(pf)
    diversity = get_diversity_vector_withoutZero(perc)
    score = get_diversity_score(diversity)


    print("Portfolio Percentage: ", perc)
    print("Diversity Vector: ", diversity)
    print("Diversity Score: ", score)

    print()