import pandas as pd
import numpy as np
import scipy
from sentence_transformers import SentenceTransformer
import tabloo
import os
import json
from django.conf import settings
from api.models import IBIS, GrowthRate, SynergyMission

misc_inc_possibilites = ['Type: Strategic Buyer', 'Type: Financial Buyer', 'Functional Strength =',
                        'Workplace Culture Match', 'Same Cultural Value:', 'Similar Company Description',
                        'Similar Mission Statement',
                        'Similar Vision Statement',
                         'Desired Strength =',
                         'Potential Desired Strength in ']

operating_possiblites = [
    'Economies of Scale - Industry',
    'Economies of Scale - Specialty',
    'Higher Growth Rate in Seller Industry',
    'Upstream Vertical Supply Chain Synergy',
    'Downstream Vertical Supply Chain Synergy',
    'Product Strengthening in',
    'Product Expansion in',
    'Service Strengthening in',  ## new
    'Service Expansion in',  ## new
    'Geographic Strengthening in',
    'Geographic Expansion in',


]   

financial_possibilites = ['Cash for your Firms Opportunities',
                        'Tax Benefits - Buyer Profit Realization']  


def ISP(input,access):
    # Model used in the NLP
    model = SentenceTransformer('paraphrase-MiniLM-L3-v2')

    # PATH = pathlib.Path(__file__).parent
    # DATA_PATH = PATH.joinpath("../datasets").resolve()

    # df_master = pd.read_csv(DATA_PATH.joinpath('Synergy_test.csv'))
    # df = df_master.copy()

    # xls = pd.ExcelFile(DATA_PATH.joinpath('Synergy_test.xlsx'))
    # df1 = pd.read_excel(xls, 'Growth_rates')
    # df2 = pd.read_excel(xls, 'IBIS')
    # df = pd.read_excel(xls, 'Synergy_mission')

    #print(input)

    df1 = pd.DataFrame(list(GrowthRate.objects.all().values()))
    df2 = pd.DataFrame(list(IBIS.objects.all().values()))
    synergyData = pd.DataFrame(list(SynergyMission.objects.all().values()))
    dflength = len(synergyData)
    dfAllowedData = 0.33
    dfAllowedDataRatio = int(dflength * dfAllowedData)
    df = synergyData
    if access == False:
       df = synergyData[:dfAllowedDataRatio]
    speciality_growth_rates_df = df1.copy()
    naics_growth_rates_df = df2.copy()

    new_list = []

    descriptors = df['functional_descriptors']
    descriptors.dropna(inplace=True)

    new_list = descriptors.values.tolist()
    s = ""

    for item in new_list:
        s += item + ","

    q = s.split(",")
    other_list = []

    for i in q:
        other_list.append(i.strip())

    res = []
    for i in other_list:
        if i not in res:
            res.append(i)

    res.remove('')

    # Strength Values found

    states_dict = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maryland': 'MD',
        'Maine': 'ME',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana IS': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vernmont': 'VT',
        'Virginia': 'VA',
        'Virgin Islands': 'VI',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'

    }

    # Assigning Industry Growth Rates
    df['industry_growth_rate'] = 100.00

    df1['growth_rate'] = df1['growth_rate'].map(lambda x: x.rstrip('%'))

    df1['growth_rate'] = df1['growth_rate'].astype(float)

    df1['growth_rate'] = df1['growth_rate'] / 100

    for index in df.index:
        i = str(df['specialty'][index])
        i = i.split(",")

        if len(i) == 1:
            if i[0] == 'nan' or i[0] not in df1['specialty'].values:
                pass
            else:
                i[0] = i[0].strip()
                val = df1.loc[df1['specialty'] == i[0], 'growth_rate'].squeeze()
                df['industry_growth_rate'][index] = val

        else:

            total = 0
            q_counter = 0
            for q in i:
                q = q.strip()
                if q in df1.values:
                    q_counter += 1
                    rate = df1.loc[df1['specialty'] == q, 'growth_rate'].iloc[0]
                    total = total + rate
            try:
                total = total / q_counter

                df['industry_growth_rate'][index] = total

            except ZeroDivisionError:
                "Do Nothing"
    #print("test0")
    if input[0] is None:
        pass
    else:
        #print("test1")

        if input[0]['question-one'][1] == 'Sell':
            try:
                if input[0]['sale-four'][1] == 'Strategic Buyer':

                    # filter for corporation

                    df['corp_condition'] = df['type'] == 'Corporation'

                    df['relationships'] = np.where(df['corp_condition'] == True,
                                                   df.relationships + ',Type: Strategic Buyer,',
                                                   df.relationships)

                    df['score'] = df['score'].astype(int) + df['corp_condition'].astype(int)

                elif input[0]['sale-four'][1] == 'Financial Buyer':

                    # filter for private equity

                    df['pe_condition'] = df['type'] == 'Private Equity'

                    df['relationships'] = np.where(df['pe_condition'] == True,
                                                   df.relationships + ',Type: Financial Buyer,',
                                                   df.relationships)

                    df['score'] = df['score'].astype(int) + df['pe_condition'].astype(int)
            except IndexError:
                "Do Nothing"

            desired_strengths = input[0]['sale-five'][1]

            for i in desired_strengths:
                strength_formatted_input = []
                strength_formatted_input.append(i)

            df['functional_descriptors'] = df['functional_descriptors'].astype(str)

            user_specialty = input[1]['speciality_input'][0]

            df['second_condition'] = df['specialty'].str.contains(user_specialty, na=False, regex=False)

            df['new_functional_descriptors'] = np.where(df['second_condition'] == True, df.functional_descriptors,
                                                        "nan")
            df['new_functional_descriptors'] = df['new_functional_descriptors'].astype(str)

            keys = df['company_name'].values

            values = df['new_functional_descriptors'].values

            new_values = []

            for i in values:
                i = i.split(',')
                new_values.append(i)

            dictionary = {}

            for key, value in zip(keys, new_values):
                dictionary[key] = value

            clean_dict = {k: dictionary[k] for k in dictionary if str(dictionary[k][0]) != 'nan'}

            for q in desired_strengths:

                for i in clean_dict:

                    list_embeddings_str = model.encode(clean_dict[i])

                    strength_formatted_input = []
                    strength_formatted_input.append(q)

                    query_embeddings_str = model.encode(strength_formatted_input)

                    random_list_to_append = []

                    for query, query_embedding in zip(strength_formatted_input, query_embeddings_str):
                        distances = scipy.spatial.distance.cdist([query_embedding], list_embeddings_str, "cosine")[
                            0]

                        results = zip(range(len(distances)), distances)
                        results = sorted(results, key=lambda x: x[1])

                        for idx, distance in results:
                            score = round((1 - distance) * 100, 2)

                            random_list_to_append.append({'company_name': i,
                                                          'str': clean_dict[i][idx],
                                                          'str_similarity': float(score)})

                        for zq in random_list_to_append:

                            if zq['str_similarity'] > 50.00 and zq['str_similarity'] < 99.99:
                                df.loc[df['company_name'] == zq['company_name'], [
                                    'relationships']] = df.relationships + ',Potential Desired Strength in ' + str(
                                    q) + '(' + zq['str'] + ')' + ','

                                df.loc[df['company_name'] == zq['company_name'], [
                                    'score']] = df['score'].astype(int) + 1

                            elif zq['str_similarity'] == 100.00:
                                df.loc[df['company_name'] == zq['company_name'], [
                                    'relationships']] = df.relationships + ',Desired Strength =' + zq['str'] + ','

                                df.loc[df['company_name'] == zq['company_name'], [
                                    'score']] = df['score'].astype(int) + 1



            # desired_strengths = input[0]['sale-five'][1]
            #
            # strengths_check = [df['functional_descriptors'].str.contains(i, na=False) for i in
            #                    desired_strengths]
            #
            # recap_strength_count = 0
            #
            # for i in strengths_check:
            #     df['relationships'] = np.where(i == True,
            #                                    df.relationships + ',Functional Strength = ' + str(
            #                                        desired_strengths[recap_strength_count]) + ',',
            #                                    df.relationships)
            #     recap_strength_count += 1
            #
            # for i in strengths_check:
            #     df['score'] = df['score'].astype(int) + i.astype(int)

        elif input[0]['question-one'][1] == 'Recapitalize':
            #print("test3")
            if input[0]['recap-one'][1] == 'Cash':
                # provide options for straight financing
                print("Options for straight financing")
                try:
                    if input[0]['recap-six'][1] == "Yes":
                        #print("1.81gothere")
                        df['cash_opp_cond'] = df['functional_descriptors'].str.contains("Cash", na=False)

                        df['relationships'] = np.where(df['cash_opp_cond'] == True,
                                                       df.relationships + ',Cash for your Firms Opportunities,',
                                                       df.relationships)

                        df['score'] = df['score'].astype(int) + df['cash_opp_cond'].astype(int)
                except IndexError:
                    "Do Nothing"

            elif input[0]['recap-one'][1] == 'Strategic Partner':
                #print("test4")
                try:
                    if input[0]['recap-three'][1] == "Yes":
                        #print("1.81gothere")
                        df['cash_opp_cond'] = df['functional_descriptors'].str.contains("Cash", na=False)

                        df['relationships'] = np.where(df['cash_opp_cond'] == True,
                                                       df.relationships + ',Cash for your Firms Opportunities,',
                                                       df.relationships)

                        df['score'] = df['score'].astype(int) + df['cash_opp_cond'].astype(int)
                except IndexError:
                    "Do Nothing"

                #print("1.82gothere")
                desired_strengths = input[0]['recap-two'][1]

                for i in desired_strengths:
                    strength_formatted_input = []
                    strength_formatted_input.append(i)

                df['functional_descriptors'] = df['functional_descriptors'].astype(str)

                user_specialty = input[1]['speciality_input'][0]

                df['second_condition'] = df['specialty'].str.contains(user_specialty, na=False, regex=False)

                df['new_functional_descriptors'] = np.where(df['second_condition'] == True, df.functional_descriptors, "nan")
                df['new_functional_descriptors'] = df['new_functional_descriptors'].astype(str)


                keys = df['company_name'].values

                values = df['new_functional_descriptors'].values

                new_values = []

                for i in values:
                    i = i.split(',')
                    new_values.append(i)

                dictionary = {}

                for key, value in zip(keys, new_values):
                    dictionary[key] = value

                clean_dict = {k: dictionary[k] for k in dictionary if str(dictionary[k][0]) != 'nan'}

                for q in desired_strengths:

                    for i in clean_dict:

                        list_embeddings_str = model.encode(clean_dict[i])

                        strength_formatted_input = []
                        strength_formatted_input.append(q)

                        query_embeddings_str = model.encode(strength_formatted_input)

                        random_list_to_append = []

                        for query, query_embedding in zip(strength_formatted_input, query_embeddings_str):
                            distances = scipy.spatial.distance.cdist([query_embedding], list_embeddings_str, "cosine")[
                                0]

                            results = zip(range(len(distances)), distances)
                            results = sorted(results, key=lambda x: x[1])

                            for idx, distance in results:
                                score = round((1 - distance) * 100, 2)

                                random_list_to_append.append({'company_name': i,
                                                              'str': clean_dict[i][idx],
                                                              'str_similarity': float(score)})

                            for zq in random_list_to_append:

                                if zq['str_similarity'] > 50.00 and zq['str_similarity'] < 99.99:
                                    df.loc[df['company_name'] == zq['company_name'], [
                                        'relationships']] = df.relationships + ',Potential Desired Strength in ' + str(
                        q) + '(' + zq['str'] + ')' + ','

                                    df.loc[df['company_name'] == zq['company_name'], [
                                        'score']] = df['score'].astype(int) + 1

                                elif zq['str_similarity'] == 100.00:
                                    df.loc[df['company_name'] == zq['company_name'], [
                                        'relationships']] = df.relationships + ',Desired Strength =' + zq['str'] + ','

                                    df.loc[df['company_name'] == zq['company_name'], [
                                        'score']] = df['score'].astype(int) + 1



                # desired_strengths = input[0]['recap-two'][1]
                #
                # strengths_check = [df['functional_descriptors'].str.contains(i, na=False) for i in
                #                    desired_strengths]
                #
                # recap_strength_count = 0
                # print("1.835gothere")
                # for i in strengths_check:
                #     df['relationships'] = np.where(i == True,
                #                                    df.relationships + ',Functional Strength = ' + str(
                #                                        desired_strengths[recap_strength_count]) + ',',
                #                                    df.relationships)
                #     recap_strength_count += 1
                #
                # for i in strengths_check:
                #     df['score'] = df['score'].astype(int) + i.astype(int)
    #print("1.9gothere")
    if input[1] is None:
        pass
    else:
        #print("2gothere")
        user_naics_ind = input[1]['NAICS-Sub-Dropdown'][0]
        #user_specialty = input[1]['speciality_input'][0]
          

        if user_specialty == "NA":
            user_growth_rate = naics_growth_rates_df.loc[df2['Title'] == user_naics_ind, 'growth_rate_2021'].iloc[0]
        else:
            try:
                user_growth_rate = speciality_growth_rates_df.loc[df1['specialty'] == user_specialty, 'growth_rate'].iloc[0]
            except IndexError:
                user_growth_rate = 0

        if user_growth_rate == 0:
            pass

        else:
            user_growth_rate = user_growth_rate.rstrip('%')
            user_growth_rate = float(user_growth_rate)
            user_growth_rate = user_growth_rate / 100
            #print(user_growth_rate)



        supply_chain_dict = {'Medical Product Manufacturer': 1,
                             'Manufacturer': 1,

                             'Distributor or Group Purchasing Organization': 2,
                             'Distributor': 2,

                             'Healthcare Organization': 3,

                             'Healthcare Provider': 4,
                             'Provider': 4}

        supp_counter = 0
        for i in df['supply_chain_position']:

            try:
                if "," in i:
                    i = i.split(",")
                    df['supply_chain_position'][supp_counter] = i[0]

            except TypeError:
                "Do Nothing"

            supp_counter += 1
        
        user_supply_chain_position = supply_chain_dict[input[1]['supply_chain_dropdown'][0]]
        
        df['supply_chain_value'] = df['supply_chain_position'].map(supply_chain_dict)

        area_of_ops_user = input[1]['area_of_operations_dropdown']

        user_products = input[1]['product_input']
        user_services = input[1]['service_input']

        user_culture_and_values = input[1]['culture_and_values_input']

        cultures = ['Adhocracy',
                    'Clan',
                    'Customer',
                    'Hierarchy',
                    'Market',
                    'Purpose',
                    'Innovative',
                    'Creative']

        workplace_culture = input[1]['workplace_culture_dropdown'][0]

        for i in cultures:
            if i in workplace_culture:
                workplace_culture = i
            else:
                pass

        user_state_list = []
        for i in area_of_ops_user:
            user_state_list.append(states_dict[i])

        df['first_condition'] = df['naics_six_digit_industry'] == user_naics_ind

        #df['second_condition'] = df['specialty'].str.contains(user_specialty, na=False, regex=False)

        df['fifth_condition'] = df['industry_growth_rate'] < user_growth_rate

        # df['sixth_condition'] = df['down_up_previous_year'] == "Down"

        # df['seventh_condition'] = df['down_up_five_year'] == "Down"

        # Upstream
        df['ninth_condition'] = df['supply_chain_value'] > user_supply_chain_position

        # Downstream
        df['tenth_condition'] = df['supply_chain_value'] < user_supply_chain_position

        # Geographic Strengthening

        geo = [df['us_geographic_reach'].str.contains(i, na=False) for i in user_state_list]

        # Geographic Expansion

        geo_expansion = [df['us_geographic_reach'].str.contains(i, na=True) for i in user_state_list]

        # Culture and Values

        culture_and_values = [df['culture_and_values'].str.contains(i, na=False) for i in user_culture_and_values]


        # Workplace Culture

        df['eleventh_condition'] = df['workplace_culture'].str.contains(workplace_culture, na=False)

        df['relationships'] = np.where(df['first_condition'] == True,
                                       df.relationships + ',Economies of Scale - Industry,',
                                       df.relationships)

        df['relationships'] = np.where(df['second_condition'] == True,
                                       df.relationships + ',Economies of Scale - Specialty,',
                                       df.relationships)


        df['relationships'] = np.where(df['fifth_condition'] == True,
                                       df.relationships + ',Higher Growth Rate in Seller Industry,',
                                       df.relationships)

        # df['relationships'] = np.where(df['sixth_condition'] == True,
        #                                df.relationships + ',Buyer Industry Currently Declining (1 Year),',
        #                                df.relationships)

        # df['relationships'] = np.where(df['seventh_condition'] == True,
        #                                df.relationships + ',Buyer Industry Historically Declining (5 Years),',
        #                                df.relationships)

        df['relationships'] = np.where(df['ninth_condition'] == True,
                                       df.relationships + ',Upstream Vertical Supply Chain Synergy,',
                                       df.relationships)

        df['relationships'] = np.where(df['tenth_condition'] == True,
                                       df.relationships + ',Downstream Vertical Supply Chain Synergy,',
                                       df.relationships)

        df['relationships'] = np.where(df['eleventh_condition'] == True,
                                       df.relationships + ',Workplace Culture Match,',
                                       df.relationships)

        if user_products:
            prod_str = np.where(df['second_condition'] == True,
                                [df['products'].str.contains(i, na=False) for i in user_products], False)

            prod_expansion = np.where(df['second_condition'] == True,
                                      [df['products'].str.contains(i, na=True) for i in user_products], True)

            prod_str_count = 0

            for i in prod_str:
                df['relationships'] = np.where(i == True, df.relationships + ',Product Strengthening in ' + str(
                    user_products[prod_str_count]) + ',', df.relationships)
                prod_str_count += 1

            prod_expansion_count = 0

            for i in prod_expansion:
                df['relationships'] = np.where(i == False, df.relationships + ',Product Expansion in ' + str(
                    user_products[prod_expansion_count]) + ',', df.relationships)
                prod_expansion_count += 1

            for i in prod_str:
                df['score'] = df['score'].astype(int) + i.astype(int)

            for i in prod_expansion:
                i = np.where(i == True, 0, 1)
                df['score'] = df['score'] + i
        else:
            pass

        if user_services:
            serv_str = np.where(df['second_condition'] == True,
                                [df['services'].str.contains(i, na=False) for i in user_services], False)

            serv_expansion = np.where(df['second_condition'] == True,
                                      [df['services'].str.contains(i, na=True) for i in user_services], True)

            serv_str_count = 0

            for i in serv_str:
                df['relationships'] = np.where(i == True, df.relationships + ',Service Strengthening in ' + str(
                    user_services[serv_str_count]) + ',', df.relationships)
                serv_str_count += 1

            serv_expansion_count = 0

            for i in serv_expansion:
                df['relationships'] = np.where(i == False, df.relationships + ',Service Expansion in ' + str(
                    user_services[serv_expansion_count]) + ',', df.relationships)
                serv_expansion_count += 1

            for i in serv_str:
                df['score'] = df['score'].astype(int) + i.astype(int)

            for i in serv_expansion:
                i = np.where(i == True, 0, 1)
                df['score'] = df['score'].astype(int) + i
        else:
            pass


        geo_count = 0

        for i in geo:
            df['relationships'] = np.where(i == True, df.relationships + ',Geographic Strengthening in ' + str(
                user_state_list[geo_count]) + ',', df.relationships)
            geo_count += 1

        geo_expansion_count = 0

        for i in geo_expansion:
            df['relationships'] = np.where(i == False, df.relationships + ',Geographic Expansion in ' + str(
                user_state_list[geo_expansion_count]) + ',', df.relationships)
            geo_expansion_count += 1

        for i in geo:
            df['score'] = df['score'].astype(int) + i.astype(int)

        for i in geo_expansion:
            i = i.replace({True: 0, False: 1})          
            df['score'] = df['score'].astype(int) + i

        values_str_count = 0

        for i in culture_and_values:
            df['relationships'] = np.where(i == True, df.relationships + ',Same Cultural Value: ' + str(
                user_culture_and_values[values_str_count]) + ',', df.relationships)
            values_str_count += 1

        for i in culture_and_values:
            df['score'] = df['score'].astype(int) + i.astype(int)

        #print("just another day1")

        # Machine Learning - Description, Mission, Vision BERT NLP

        description = input[1]['description_input']
        mission = input[1]['mission_input']
        vision = input[1]['vision_input']
        #print("just another day2")
        # Duplicated Data like two Sunveras
        df = df.drop_duplicates(subset=['company_name'], keep='first')
        df = df.reset_index(drop=True)

        df['new_description'] = np.where(df['second_condition'] == True, df.description, "NA")
        df['new_description'] = df['new_description'].astype(str)
        #print("just another day3")
        list_of_descriptions = []
        for i in df['new_description']:
            list_of_descriptions.append(i)

        cleaned_description_list = [x for x in list_of_descriptions if str(x) != 'NA']

        list_of_missions = []
        for i in df['mission_statement']:
            list_of_missions.append(i)

        cleaned_mission_list = [x for x in list_of_missions if str(x) != 'nan']

        list_of_visions = []
        for i in df['vision_statement']:
            list_of_visions.append(i)

        cleaned_vision_list = [x for x in list_of_visions if str(x) != 'nan']
        #print("just another day4")
        list_embeddings_description = model.encode(cleaned_description_list)
        list_embeddings_mission = model.encode(cleaned_mission_list)
        list_embeddings_vision = model.encode(cleaned_vision_list)
        #print("just another day5")
        query_embeddings_description = model.encode(description)

        query_embeddings_mission = model.encode(mission)

        query_embeddings_vision = model.encode(vision)
        #print("just another day6")
        closest_n = 5

        #Trying to fix local reference error to empt_df_description

        empt_df_description = pd.DataFrame(columns=['new_description', 'description_similarity'])


        try:
            random_list_to_append = []

            for query, query_embedding in zip(description, query_embeddings_description):
                distances = scipy.spatial.distance.cdist([query_embedding], list_embeddings_description, "cosine")[0]

                results = zip(range(len(distances)), distances)
                results = sorted(results, key=lambda x: x[1])

                for idx, distance in results:
                    # print(cleanedList[idx].strip(), "(Score: %.4f)" % (1-distance))
                    score = round((1 - distance) * 100, 2)

                    random_list_to_append.append({'new_description': cleaned_description_list[idx].strip(),
                                                  'description_similarity': score})

            empt_df_description = pd.DataFrame.from_records(random_list_to_append)

            empt_df_description['new_description'] = empt_df_description['new_description'].astype(str)
            df['new_description'] = df['new_description'].astype(str)
        except ValueError:
            "Do Nothing"

        # ----------------------------------------------------------------------------------
        #print("just another day7")
        closest_n = 5
        try:
            random_list_to_append_one = []

            for query, query_embedding in zip(mission, query_embeddings_mission):
                distances = scipy.spatial.distance.cdist([query_embedding], list_embeddings_mission, "cosine")[0]

                results = zip(range(len(distances)), distances)
                results = sorted(results, key=lambda x: x[1])

                for idx, distance in results:
                    # print(cleanedList[idx].strip(), "(Score: %.4f)" % (1-distance))
                    score = round((1 - distance) * 100, 2)

                    random_list_to_append_one.append({'mission_statement': cleaned_mission_list[idx].strip(),
                                                      'mission_similarity': score})

            empt_df_mission = pd.DataFrame.from_records(random_list_to_append_one)

            empt_df_mission['mission_statement'] = empt_df_mission['mission_statement'].astype(str)
            df['mission_statement'] = df['mission_statement'].astype(str)

        except ValueError:
            "Do Nothing"
        # ----------------------------------------------------------------------------------
        #print("just another day8")
        closest_n = 5

        try:

            random_list_to_append_two = []

            for query, query_embedding in zip(vision, query_embeddings_vision):
                distances = scipy.spatial.distance.cdist([query_embedding], list_embeddings_vision, "cosine")[0]

                results = zip(range(len(distances)), distances)
                results = sorted(results, key=lambda x: x[1])

                for idx, distance in results:
                    # print(cleanedList[idx].strip(), "(Score: %.4f)" % (1-distance))
                    score = round((1 - distance) * 100, 2)

                    random_list_to_append_two.append({'vision_statement': cleaned_vision_list[idx].strip(),
                                                      'vision_similarity': score})

            empt_df_vision = pd.DataFrame.from_records(random_list_to_append_two)

            empt_df_vision['vision_statement'] = empt_df_vision['vision_statement'].astype(str)
            df['vision_statement'] = df['vision_statement'].astype(str)

        except ValueError:
            "Do Nothing"

        # # ------------------------------------------------------------------------------
        #("just another day9")
        df_ml = pd.merge(df, empt_df_description, on=['new_description', 'new_description'], how='left')
        #print("just another day10")
        df_ml1 = pd.merge(df, empt_df_mission, on=['mission_statement', 'mission_statement'], how='left')
        #print("just another day11")
        df_ml2 = pd.merge(df, empt_df_vision, on=['vision_statement', 'vision_statement'], how='left')

        df_ml1 = df_ml1.drop_duplicates(subset=['company_name'], keep='first')
        df_ml1 = df_ml1.reset_index(drop=True)
        df_ml2 = df_ml2.drop_duplicates(subset=['company_name'], keep='first')
        df_ml2 = df_ml2.reset_index(drop=True)

        df_ml['description_similarity'] = df_ml['description_similarity'] / 100
        df_ml1['mission_similarity'] = df_ml1['mission_similarity'] / 100
        df_ml2['vision_similarity'] = df_ml2['vision_similarity'] / 100

        df['twelfth_condition'] = df_ml['description_similarity'] > 0.30

        df['thirteenth_condition'] = df_ml1['mission_similarity'] > 0.50

        df['fourteenth_condition'] = df_ml2['vision_similarity'] > 0.50

        df['relationships'] = np.where(df['twelfth_condition'] == True,
                                       df.relationships + ',Similar Company Description,',
                                       df.relationships)

        df['relationships'] = np.where(df['thirteenth_condition'] == True,
                                       df.relationships + ',Similar Mission Statement,',
                                       df.relationships)

        df['relationships'] = np.where(df['fourteenth_condition'] == True,
                                       df.relationships + ',Similar Vision Statement,',
                                       df.relationships)

        df['score'] = np.where(df['second_condition'] == True,
                               df.score + 5,
                               df.score)

        df['score'] = df['score'].astype(int) + (
                (df['first_condition']).astype(int)
                + ((df['second_condition']).astype(int))
                + ((df['fifth_condition']).astype(int))
                + ((df['ninth_condition']).astype(int))
                + ((df['tenth_condition']).astype(int))
                + ((df['eleventh_condition']).astype(int))
                + ((df['twelfth_condition']).astype(int))
                + ((df['thirteenth_condition']).astype(int))
                + ((df['fourteenth_condition']).astype(int))
        )

    if input[2] is None:
        pass
    else:
        #print("3gothere")
        ebitda_input = float(input[2]['ebitda_year_one'][0])

        if ebitda_input < 0:
            df['eighth_condition'] = ebitda_input < 0

            df['relationships'] = np.where(df['eighth_condition'] == True,
                                           df.relationships + ',Tax Benefits - Buyer Profit Realization,',
                                           df.relationships)
            df['score'] = df['score'].astype(int) + (df['eighth_condition']).astype(int)



    # print(df['score'])
    # print(df['relationships'])

    # print(df)
    # print(df.columns)
    
    # Additional columns for AI Recommendation's Page
    df['misc_synergies'] = df.apply(lambda row: get_misc_synergies(row.relationships), axis=1)
    df['operating_synergies'] = df.apply(lambda row: get_operating_synergies(row.relationships), axis=1)
    df['financial_synergies'] = df.apply(lambda row: get_financial_synergies(row.relationships), axis=1)
    df['bar_chart'] = df.apply(lambda row: get_bar_chart(row.relationships), axis=1)


    df.sort_values(by=['score'], ascending=False, inplace=True)

    # df = df.rename(
    #     columns={'company_name': 'Investor', 'score': 'Rank',
    #              'relationships': 'Relationships'})

    # returned_df = df[['company_name', 'score', 'relationships']]
    # returned_df.sort_values(by=['score'], ascending=False, inplace=True)

    # returned_df = returned_df.rename(
    #     columns={'company_name': 'Investor', 'score': 'Rank',
    #              'relationships': 'Relationships'})

    # print(returned_df)

    # tooltip_data = [
    #     {
    #         'Investor': {'value': row['Motivators'], 'type': 'markdown'}
    #     } for row in returned_df.to_dict('records')
    # ]
    records = df.to_json(orient = 'records')
    data = json.loads(records)
    return data

def get_misc_synergies(relationships):
    relationships = [relationship for relationship in relationships.split(',') if relationship]
    
    misc_output = []
    for i in relationships:
        for m in misc_inc_possibilites:
            if m in i:
                misc_output.append(i)
    return misc_output 

def get_operating_synergies(relationships):
    relationships = [relationship for relationship in relationships.split(',') if relationship]
    
    operating_output = []
    for i in relationships:
        for o in operating_possiblites:
            if o in i:
                operating_output.append(i)
    return operating_output 

def get_financial_synergies(relationships):
    relationships = [relationship for relationship in relationships.split(',') if relationship]  
    
    financial_output = []
    for i in relationships:
        for f in financial_possibilites:
            if f in i:
                financial_output.append(i)
    return financial_output 
    
def get_bar_chart(relationships):
    bar1 = len(get_misc_synergies(relationships))
    bar2 = len(get_operating_synergies(relationships))
    bar3 = len(get_financial_synergies(relationships))
    return [
        {
            "value": bar1,
            "color": "#BDC1FE",
            "percent": int(100* bar1 / len(misc_inc_possibilites))
        },
        {
            "value": bar2,
            "color": "#D0BBFE",
            "percent": int(100* bar2 / len(operating_possiblites))
        },
        {
            "value": bar3,
            "color": "#EABBFE",
            "percent": int(100 * bar3 / len(financial_possibilites))               
        }
    ]