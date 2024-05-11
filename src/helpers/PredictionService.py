import logging
import pickle
import pandas as pd
import shap
import numpy as np

from ..dto.EmployeeTurnoverResults import EmployeeTurnoverResults


def predict_employee_turnover(employee_survey):
    logging.info('EmployeeServices - predict_employee_turnover() CALLED')
   
    working_hours = employee_survey.working_hours
    promotional_barriers = employee_survey.promotional_barriers
    work_life_balance = employee_survey.work_life_balance
    status_and_recognition = employee_survey.status_and_recognition
    salary = employee_survey.salary
    opportunities = employee_survey.opportunities
    workload = employee_survey.workload
    work_environment = employee_survey.work_environment
    training_and_development = employee_survey.training_and_development
    relationship_with_colleagues = employee_survey.relationship_with_colleagues
    relationship_with_supervisor = employee_survey.relationship_with_supervisor
    job_satisfaction = employee_survey.job_satisfaction
    distance_from_home = employee_survey.distance_from_home
    age = employee_survey.age
    gender = employee_survey.gender
    marital_status = employee_survey.marital_status
    educational_status = employee_survey.educational_status
    total_years_industry = employee_survey.total_years_industry
    years_work_current_hotel = employee_survey.years_work_current_hotel
    number_of_years_current_role = employee_survey.number_of_years_current_role
    department = employee_survey.department
    last_promotion = employee_survey.last_promotion
    hotel_assess_performance = employee_survey.hotel_assess_performance
  
    # applying One-Hot encoding technique
    if age == 1:
        age_category_20_30 = 1
        age_category_30_40 = 0
        age_category_above_40 = 0
    elif age == 2:
        age_category_20_30 = 0
        age_category_30_40 = 1
        age_category_above_40 = 0
    else:
        age_category_20_30 = 0
        age_category_30_40 = 0
        age_category_above_40 = 1

    if gender == 1:
        gender_female = 0
        gender_male = 1
    else:
        gender_female = 1
        gender_male = 0

    if marital_status == 1:
        marital_status_married_with_children = 1
        marital_status_married_without_children = 0
        marital_status_single = 0

    elif marital_status == 2:
        marital_status_married_with_children = 0
        marital_status_married_without_children = 1
        marital_status_single = 0
    else:
        marital_status_married_with_children = 0
        marital_status_married_without_children = 0,
        marital_status_single = 1

    if educational_status == 1:
        educational_status_below_ol = 1
        educational_status_ol_passer = 0
        educational_status_al_passer = 0
        educational_status_diploma_holder = 0
        educational_status_degree_holder = 0

    elif educational_status == 2:
        educational_status_below_ol = 0
        educational_status_ol_passer = 1
        educational_status_al_passer = 0
        educational_status_diploma_holder = 0
        educational_status_degree_holder = 0

    elif educational_status == 3:
        educational_status_below_ol = 0
        educational_status_ol_passer = 0
        educational_status_al_passer = 1
        educational_status_diploma_holder = 0
        educational_status_degree_holder = 0

    elif educational_status == 4:
        educational_status_below_ol = 0
        educational_status_ol_passer = 0
        educational_status_al_passer = 0
        educational_status_diploma_holder = 1
        educational_status_degree_holder = 0
    else:
        educational_status_below_ol = 0
        educational_status_ol_passer = 0
        educational_status_al_passer = 0
        educational_status_diploma_holder = 0
        educational_status_degree_holder = 1

    if total_years_industry == 1:
        total_years_industry_less_than_1_year = 1
        total_years_industry_1_3_years = 0
        total_years_industry_3_5_years = 0
        total_years_industry_5_10_years = 0
        total_years_industry_10_15_years = 0
        total_years_industry_15_years_above = 0

    elif total_years_industry == 2:
        total_years_industry_less_than_1_year = 0
        total_years_industry_1_3_years = 1
        total_years_industry_3_5_years = 0
        total_years_industry_5_10_years = 0
        total_years_industry_10_15_years = 0
        total_years_industry_15_years_above = 0

    elif total_years_industry == 3:
        total_years_industry_less_than_1_year = 0
        total_years_industry_1_3_years = 0
        total_years_industry_3_5_years = 1
        total_years_industry_5_10_years = 0
        total_years_industry_10_15_years = 0
        total_years_industry_15_years_above = 0

    elif total_years_industry == 4:
        total_years_industry_less_than_1_year = 0
        total_years_industry_1_3_years = 0
        total_years_industry_3_5_years = 0
        total_years_industry_5_10_years = 1
        total_years_industry_10_15_years = 0
        total_years_industry_15_years_above = 0

    elif total_years_industry == 5:
        total_years_industry_less_than_1_year = 0
        total_years_industry_1_3_years = 0
        total_years_industry_3_5_years = 0
        total_years_industry_5_10_years = 0
        total_years_industry_10_15_years = 1
        total_years_industry_15_years_above = 0

    else:
        total_years_industry_less_than_1_year = 0
        total_years_industry_1_3_years = 0
        total_years_industry_3_5_years = 0
        total_years_industry_5_10_years = 0
        total_years_industry_10_15_years = 0
        total_years_industry_15_years_above = 1

    if years_work_current_hotel == 1:
        years_work_current_hotel_less_than_year = 1
        years_work_current_hotel_1_3_years = 0
        years_work_current_hotel_3_5_years = 0
        years_work_current_hotel_5_10_years = 0
        years_work_current_hotel_10_15_years = 0
        years_work_current_hotel_15_above = 0

    elif years_work_current_hotel == 2:
        years_work_current_hotel_less_than_year = 0
        years_work_current_hotel_1_3_years = 1
        years_work_current_hotel_3_5_years = 0
        years_work_current_hotel_5_10_years = 0
        years_work_current_hotel_10_15_years = 0
        years_work_current_hotel_15_above = 0

    elif years_work_current_hotel == 3:
        years_work_current_hotel_less_than_year = 0
        years_work_current_hotel_1_3_years = 0
        years_work_current_hotel_3_5_years = 1
        years_work_current_hotel_5_10_years = 0
        years_work_current_hotel_10_15_years = 0
        years_work_current_hotel_15_above = 0

    elif years_work_current_hotel == 4:
        years_work_current_hotel_less_than_year = 0
        years_work_current_hotel_1_3_years = 0
        years_work_current_hotel_3_5_years = 0
        years_work_current_hotel_5_10_years = 1
        years_work_current_hotel_10_15_years = 0
        years_work_current_hotel_15_above = 0

    elif years_work_current_hotel == 5:
        years_work_current_hotel_less_than_year = 0
        years_work_current_hotel_1_3_years = 0
        years_work_current_hotel_3_5_years = 0
        years_work_current_hotel_5_10_years = 0
        years_work_current_hotel_10_15_years = 1
        years_work_current_hotel_15_above = 0

    else:
        years_work_current_hotel_less_than_year = 0
        years_work_current_hotel_1_3_years = 0
        years_work_current_hotel_3_5_years = 0
        years_work_current_hotel_5_10_years = 0
        years_work_current_hotel_10_15_years = 0
        years_work_current_hotel_15_above = 1

    if number_of_years_current_role == 1:
        number_of_years_current_role_less_than_year = 1
        number_of_years_current_role_1_3_years = 0
        number_of_years_current_role_3_5_years = 0
        number_of_years_current_role_5_10_years = 0
        number_of_years_current_role_10_15_years = 0
        number_of_years_current_role_15_above = 0

    elif number_of_years_current_role == 2:
        number_of_years_current_role_less_than_year = 0
        number_of_years_current_role_1_3_years = 1
        number_of_years_current_role_3_5_years = 0
        number_of_years_current_role_5_10_years = 0
        number_of_years_current_role_10_15_years = 0
        number_of_years_current_role_15_above = 0

    elif number_of_years_current_role == 3:
        number_of_years_current_role_less_than_year = 0
        number_of_years_current_role_1_3_years = 0
        number_of_years_current_role_3_5_years = 1
        number_of_years_current_role_5_10_years = 0
        number_of_years_current_role_10_15_years = 0
        number_of_years_current_role_15_above = 0

    elif number_of_years_current_role == 4:
        number_of_years_current_role_less_than_year = 0
        number_of_years_current_role_1_3_years = 0
        number_of_years_current_role_3_5_years = 0
        number_of_years_current_role_5_10_years = 1
        number_of_years_current_role_10_15_years = 0
        number_of_years_current_role_15_above = 0

    elif number_of_years_current_role == 5:
        number_of_years_current_role_less_than_year = 0
        number_of_years_current_role_1_3_years = 0
        number_of_years_current_role_3_5_years = 0
        number_of_years_current_role_5_10_years = 0
        number_of_years_current_role_10_15_years = 1
        number_of_years_current_role_15_above = 0

    else:
        number_of_years_current_role_less_than_year = 0
        number_of_years_current_role_1_3_years = 0
        number_of_years_current_role_3_5_years = 0
        number_of_years_current_role_5_10_years = 0
        number_of_years_current_role_10_15_years = 0
        number_of_years_current_role_15_above = 1

    if last_promotion == 1:
        last_promotion_less_than_year = 1
        last_promotion_1_3_years = 0
        last_promotion_3_5_years = 0
        last_promotion_5_10_years = 0
        last_promotion_more_than_5_year = 0
        last_promotion_none_received = 0

    elif last_promotion == 2:
        last_promotion_less_than_year = 0
        last_promotion_1_3_years = 1
        last_promotion_3_5_years = 0
        last_promotion_5_10_years = 0
        last_promotion_more_than_5_year = 0
        last_promotion_none_received = 0

    elif last_promotion == 3:
        last_promotion_less_than_year = 0
        last_promotion_1_3_years = 0
        last_promotion_3_5_years = 1
        last_promotion_5_10_years = 0
        last_promotion_more_than_5_year = 0
        last_promotion_none_received = 0

    elif last_promotion == 4:
        last_promotion_less_than_year = 0
        last_promotion_1_3_years = 0
        last_promotion_3_5_years = 0
        last_promotion_5_10_years = 1
        last_promotion_more_than_5_year = 0
        last_promotion_none_received = 0

    elif last_promotion == 5:
        last_promotion_less_than_year = 0
        last_promotion_1_3_years = 0
        last_promotion_3_5_years = 0
        last_promotion_5_10_years = 0
        last_promotion_more_than_5_year = 1
        last_promotion_none_received = 0

    else:
        last_promotion_less_than_year = 0
        last_promotion_1_3_years = 0
        last_promotion_3_5_years = 0
        last_promotion_5_10_years = 0
        last_promotion_more_than_5_year = 0
        last_promotion_none_received = 1

    if hotel_assess_performance == 1:
        hotel_assess_performance_less_often = 1
        hotel_assess_performance_often = 0
        hotel_assess_performance_quite_often = 0

    elif hotel_assess_performance == 2:
        hotel_assess_performance_less_often = 0
        hotel_assess_performance_often = 1
        hotel_assess_performance_quite_often = 0

    else:
        hotel_assess_performance_less_often = 0
        hotel_assess_performance_often = 0
        hotel_assess_performance_quite_often = 1

    if department == 1:
        department_food_beverages = 1
        department_front_office = 0
        department_housekeeping = 0
        department_maintenance = 0
        department_security = 0

    elif department == 2:
        department_food_beverages = 0
        department_front_office = 1
        department_housekeeping = 0
        department_maintenance = 0
        department_security = 0

    elif department == 3:
        department_food_beverages = 0
        department_front_office = 0
        department_housekeeping = 1
        department_maintenance = 0
        department_security = 0

    elif department == 4:
        department_food_beverages = 0
        department_front_office = 0
        department_housekeeping = 0
        department_maintenance = 1
        department_security = 0

    else:
        department_food_beverages = 0
        department_front_office = 0
        department_housekeeping = 0
        department_maintenance = 0
        department_security = 1


    # initiating dataframe
    datapoint = pd.DataFrame({'working_hours': working_hours,
                              'promotional_barriers': promotional_barriers,
                              'work_life_balance': work_life_balance,
                              'status_and_recognition': status_and_recognition,
                              'salary': salary,
                              'opportunities': opportunities,
                              'workload': workload,
                              'work_environment': work_environment,
                              'training_and_development': training_and_development,
                              'relationship_with_colleagues': relationship_with_colleagues,
                              'relationship_with_supervisor': relationship_with_supervisor,
                              'job_satisfaction': job_satisfaction,
                              'distance_from_home': distance_from_home,
                              'age_category_20 - 30': age_category_20_30,
                              'age_category_30 - 40': age_category_30_40,
                              'age_category_Above 40': age_category_above_40,
                              'gender_Female': gender_female,
                              'gender_Male': gender_male,
                              'marital_status_Married with children': marital_status_married_with_children,
                              'marital_status_Married without children': marital_status_married_without_children,
                              'marital_status_Single': marital_status_single,
                              'educational_status_A/L passer': educational_status_al_passer,
                              'educational_status_Below O/L': educational_status_below_ol,
                              'educational_status_Degree holder': educational_status_degree_holder,
                              'educational_status_Diploma holder': educational_status_diploma_holder,
                              'educational_status_O/L passer': educational_status_ol_passer,
                              'total_years_industry_1 - 3 years': total_years_industry_1_3_years,
                              'total_years_industry_10 - 15 years': total_years_industry_10_15_years,
                              'total_years_industry_15 years and above': total_years_industry_15_years_above,
                              'total_years_industry_3 - 5 years': total_years_industry_3_5_years,
                              'total_years_industry_5 - 10 years': total_years_industry_5_10_years,
                              'total_years_industry_Less than 1 year': total_years_industry_less_than_1_year,
                              'years_work_current_hotel_1 - 3 years': years_work_current_hotel_1_3_years,
                              'years_work_current_hotel_10 - 15 years': years_work_current_hotel_10_15_years,
                              'years_work_current_hotel_15 years and above': years_work_current_hotel_15_above,
                              'years_work_current_hotel_3 - 5 years': years_work_current_hotel_3_5_years,
                              'years_work_current_hotel_5 - 10 years': years_work_current_hotel_5_10_years,
                              'years_work_current_hotel_Less than 1 year': years_work_current_hotel_less_than_year,
                              'number_of_years_current_role_1 - 3 years': number_of_years_current_role_1_3_years,
                              'number_of_years_current_role_10 - 15 years': number_of_years_current_role_10_15_years,
                              'number_of_years_current_role_15 years and above': number_of_years_current_role_15_above,
                              'number_of_years_current_role_3 - 5 years': number_of_years_current_role_3_5_years,
                              'number_of_years_current_role_5 - 10 years': number_of_years_current_role_5_10_years,
                              'number_of_years_current_role_Less than 1 year': number_of_years_current_role_less_than_year,
                              'department_Food and Beverages': department_food_beverages,
                              'department_Front office': department_front_office,
                              'department_Housekeeping': department_housekeeping,
                              'department_Maintenance': department_maintenance,
                              'department_Security': department_security,
                              'last_promotion_1 - 3 years': last_promotion_1_3_years,
                              'last_promotion_3 - 5 years': last_promotion_3_5_years,
                              'last_promotion_5 - 10 years': last_promotion_5_10_years,
                              'last_promotion_Less than 1 year': last_promotion_less_than_year,
                              'last_promotion_More than 5 year': last_promotion_more_than_5_year,
                              'last_promotion_None received': last_promotion_none_received,
                              'hotel_assess_performance_Less Often': hotel_assess_performance_less_often,
                              'hotel_assess_performance_Often': hotel_assess_performance_often,
                              'hotel_assess_performance_Quite often': hotel_assess_performance_quite_often},
                             index=[0])
    logging.info('EmployeeServices - data frame initiated:: ', datapoint)


    # load the model from disk
    loaded_model = pickle.load(open('prediction_model/turnover_prediction_model/employee_turnover_extra_tree_classifier.pkl', 'rb'))
    logging.info('EmployeeServices - prediction model loaded')

    # prediction
    pred_results_prob = loaded_model.predict_proba(datapoint)
    logging.info('EmployeeServices - turnover predicted as: ', pred_results_prob)

    # discovering the factors to the prediction
    explainer = shap.Explainer(model=loaded_model)
    shap_values = explainer.shap_values(datapoint)


    sorted_positive_values_with_feature_name = {}  # will leave 1
    sorted_negative_values_with_feature_name = {}  # will stay 0

    for main_array_index in range(len(shap_values)):

        datapoint_columns = datapoint.columns
        shap_values_array = shap_values[main_array_index][0]

        # initiating array of factor(column of dataset) name with value dict by negative positive score
        positive_values_with_feature_name = {}
        negative_values_with_feature_name = {}
        for index in range(len(datapoint_columns)):
            if shap_values_array[index] < 0:
                negative_values_with_feature_name[datapoint_columns[index]] = shap_values_array[index]
            else:
                positive_values_with_feature_name[datapoint_columns[index]] = shap_values_array[index]

        # sorting by the amount of affect
        positive_value_keys = list(positive_values_with_feature_name.keys())
        positive_values = list(positive_values_with_feature_name.values())
        positive_sorted_value_indexes = np.argsort(positive_values)  # returns the indexes of values by ascending order
        sorted_positive_values_with_feature_name = {positive_value_keys[i]: positive_values[i] for i in
                                                    positive_sorted_value_indexes}

        negative_value_keys = list(negative_values_with_feature_name.keys())
        negative_values = list(negative_values_with_feature_name.values())
        negative_sorted_value_indexes = np.argsort(negative_values)
        sorted_negative_values_with_feature_name = {negative_value_keys[i]: negative_values[i] for i in
                                                    negative_sorted_value_indexes}
        logging.info('EmployeeServices - shap values generated')


    
    # returns the predicted score and factores
    if pred_results_prob[0][0] > .90:
        return EmployeeTurnoverResults(False, 0,
                                       get_turnover_factors_organized_data(sorted_negative_values_with_feature_name,datapoint))
    else:
        # leaving
        return EmployeeTurnoverResults(True, pred_results_prob[0][1], 
                                       get_turnover_factors_organized_data(sorted_positive_values_with_feature_name,datapoint))

# organize the predicted list with actual factor names
def get_turnover_factors_organized_data(predicted_list,datapoint):
    turnover_factotrs_list = []
    for factor in  list(reversed(list(predicted_list.items())))[0:10]:

        # if zero values in the dataframe get scored below validation will skip it
        if(datapoint.loc[0][factor[0]]==0):
            continue

        # actual factor name and score
        turnover_factotrs_list.append((get_acutual_factor(factor[0]),factor[1]))
    return turnover_factotrs_list[0:3]   
    

# returns the actual factor (removes one hot encoded factor- "hotel_assess_performance_Less Often--->hotel_assess_performance)
def get_acutual_factor(encoded_factor):
    
  if encoded_factor in ["working_hours","promotional_barriers","work_life_balance","status_and_recognition","salary","opportunities","workload","distance_from_home",
                                           "work_environment","training_and_development","relationship_with_colleagues","relationship_with_supervisor","job_satisfaction"]:
    return encoded_factor
  else:
      if encoded_factor in ["age_category_20 - 30","age_category_30 - 40","age_category_Above 40"]:
          return "age"
      elif encoded_factor in ["gender_Female","gender_Male"]:
          return "gender"
      elif encoded_factor in ["marital_status_Married with children","marital_status_Married without children","marital_status_Single"]:
          return "marital_status"
      elif encoded_factor in ["educational_status_A/L passer","educational_status_Below O/L","educational_status_Degree holder","educational_status_Diploma holder","educational_status_O/L passer"]:
          return "educational_status"
      elif encoded_factor in ["total_years_industry_1 - 3 years","total_years_industry_10 - 15 years","total_years_industry_15 years and above","total_years_industry_3 - 5 years","total_years_industry_5 - 10 years","total_years_industry_Less than 1 year"]:
          return "total_years_industry"
      elif encoded_factor in ["years_work_current_hotel_1 - 3 years","years_work_current_hotel_10 - 15 years","years_work_current_hotel_15 years and above","years_work_current_hotel_3 - 5 years","years_work_current_hotel_5 - 10 years","years_work_current_hotel_Less than 1 year"]:
          return "years_work_current_hotel"
      elif encoded_factor in ["number_of_years_current_role_1 - 3 years","number_of_years_current_role_10 - 15 years","number_of_years_current_role_15 years and above","number_of_years_current_role_3 - 5 years","number_of_years_current_role_5 - 10 years","number_of_years_current_role_Less than 1 year"]:
          return "number_of_years_current_role"
      elif encoded_factor in ["department_Food and Beverages","department_Front office","department_Housekeeping","department_Maintenance","department_Security"]:
          return "department"
      elif encoded_factor in ["last_promotion_1 - 3 years","last_promotion_3 - 5 years","last_promotion_5 - 10 years","last_promotion_Less than 1 year","last_promotion_More than 5 year","last_promotion_None received"]:
          return "last_promotion"
      elif encoded_factor in ["hotel_assess_performance_Less Often","hotel_assess_performance_Often","hotel_assess_performance_Quite often"]:
          return "hotel_performance_asses"
      


# returns the number of weeks till turnover
def predict_employee_turnover_days(employee_survey_regression_data):
    logging.info('EmployeeServices - predict_employee_turnover_days() CALLED')

    age=employee_survey_regression_data.age 
    gender=employee_survey_regression_data.gender 
    marital_status=employee_survey_regression_data.marital_status 
    educational_status=employee_survey_regression_data.educational_status
    total_years_industry=employee_survey_regression_data.total_years_industry 
    years_work_current_hotel=employee_survey_regression_data.years_work_current_hotel
    number_of_years_current_role=employee_survey_regression_data.number_of_years_current_role 
    department=employee_survey_regression_data.department
    salary=employee_survey_regression_data.salary
    opportunities=employee_survey_regression_data.opportunities
    workload=employee_survey_regression_data.workload


    if(age==1):
        age_category_20_30=1
        age_category_30_40=0 
        age_category_above_40=0
    elif(age==2):
        age_category_20_30=0
        age_category_30_40=1 
        age_category_above_40=0
    else:
        age_category_20_30=0
        age_category_30_40=0 
        age_category_above_40=1 

    if(gender==1):
        gender_female=0
        gender_male=1
    else:
        gender_female=1
        gender_male=0 

        
    if(marital_status==1):
        marital_status_Married_with_children=1
        marital_status_Married_without_children=0
        marital_status_Single=0
        
    elif(marital_status==2):
        marital_status_Married_with_children=0
        marital_status_Married_without_children=1
        marital_status_Single=0
    else:
        marital_status_Married_with_children=0
        marital_status_Married_without_children=0,
        marital_status_Single=1


    if(educational_status==1):
        educational_status_below_ol = 1
        educational_status_ol_passer = 0
        educational_status_al_passer= 0
        educational_status_diploma_holder=0
        educational_status_degree_holder=0
        
    elif(educational_status==2):
        educational_status_below_ol = 0
        educational_status_ol_passer = 1
        educational_status_al_passer= 0
        educational_status_diploma_holder=0
        educational_status_degree_holder=0
        
    elif educational_status==3:
        educational_status_below_ol = 0
        educational_status_ol_passer = 0
        educational_status_al_passer= 1
        educational_status_diploma_holder=0
        educational_status_degree_holder=0
        
    elif educational_status==4:
        educational_status_below_ol = 0
        educational_status_ol_passer = 0
        educational_status_al_passer= 0
        educational_status_diploma_holder=1
        educational_status_degree_holder=0
    else:
        educational_status_below_ol = 0
        educational_status_ol_passer = 0
        educational_status_al_passer= 0
        educational_status_diploma_holder=0
        educational_status_degree_holder=1
    

    if(total_years_industry==1):
        total_years_industry_less_than_1_year=1
        total_years_industry_1_3_years=0
        total_years_industry_3_5_years=0 
        total_years_industry_5_10_years=0
        total_years_industry_10_15_years=0
        total_years_industry_15_years_above=0
        
    elif(total_years_industry==2):
        total_years_industry_less_than_1_year=0
        total_years_industry_1_3_years=1 
        total_years_industry_3_5_years=0 
        total_years_industry_5_10_years=0
        total_years_industry_10_15_years=0
        total_years_industry_15_years_above=0
        
    elif(total_years_industry==3):
        total_years_industry_less_than_1_year=0
        total_years_industry_1_3_years=0
        total_years_industry_3_5_years=1
        total_years_industry_5_10_years=0
        total_years_industry_10_15_years=0
        total_years_industry_15_years_above=0
        
    elif(total_years_industry==4):
        total_years_industry_less_than_1_year=0
        total_years_industry_1_3_years=0
        total_years_industry_3_5_years=0 
        total_years_industry_5_10_years=1
        total_years_industry_10_15_years=0
        total_years_industry_15_years_above=0
        
    elif(total_years_industry==5):
        total_years_industry_less_than_1_year=0
        total_years_industry_1_3_years=0
        total_years_industry_3_5_years=0 
        total_years_industry_5_10_years=0
        total_years_industry_10_15_years=1
        total_years_industry_15_years_above=0
        
    else:
        total_years_industry_less_than_1_year=0
        total_years_industry_1_3_years=0
        total_years_industry_3_5_years=0 
        total_years_industry_5_10_years=0
        total_years_industry_10_15_years=0
        total_years_industry_15_years_above=1


    if(years_work_current_hotel==1):
        years_work_current_hotel_less_than_year=1
        years_work_current_hotel_1_3_years=0
        years_work_current_hotel_3_5_years=0
        years_work_current_hotel_5_10_years=0
        years_work_current_hotel_10_15_years=0
        years_work_current_hotel_15_above=0
            
    elif years_work_current_hotel==2:
        years_work_current_hotel_less_than_year=0
        years_work_current_hotel_1_3_years=1
        years_work_current_hotel_3_5_years=0
        years_work_current_hotel_5_10_years=0
        years_work_current_hotel_10_15_years=0
        years_work_current_hotel_15_above=0
        
    elif years_work_current_hotel==3:
        years_work_current_hotel_less_than_year=0
        years_work_current_hotel_1_3_years=0
        years_work_current_hotel_3_5_years=1
        years_work_current_hotel_5_10_years=0
        years_work_current_hotel_10_15_years=0
        years_work_current_hotel_15_above=0
        
    elif years_work_current_hotel==4:
        years_work_current_hotel_less_than_year=0
        years_work_current_hotel_1_3_years=0
        years_work_current_hotel_3_5_years=0
        years_work_current_hotel_5_10_years=1
        years_work_current_hotel_10_15_years=0
        years_work_current_hotel_15_above=0

    elif years_work_current_hotel==5:
        years_work_current_hotel_less_than_year=0
        years_work_current_hotel_1_3_years=0
        years_work_current_hotel_3_5_years=0
        years_work_current_hotel_5_10_years=0
        years_work_current_hotel_10_15_years=1
        years_work_current_hotel_15_above=0
        
    else:
        years_work_current_hotel_less_than_year=0
        years_work_current_hotel_1_3_years=0
        years_work_current_hotel_3_5_years=0
        years_work_current_hotel_5_10_years=0
        years_work_current_hotel_10_15_years=0
        years_work_current_hotel_15_above=1
        
    
        
    if(number_of_years_current_role==1):
        number_of_years_current_role_less_than_year=1
        number_of_years_current_role_1_3_years=0
        number_of_years_current_role_3_5_years=0
        number_of_years_current_role_5_10_years=0
        number_of_years_current_role_10_15_years=0
        number_of_years_current_role_15_above=0
        
    elif number_of_years_current_role==2:
        number_of_years_current_role_less_than_year=0
        number_of_years_current_role_1_3_years=1
        number_of_years_current_role_3_5_years=0
        number_of_years_current_role_5_10_years=0
        number_of_years_current_role_10_15_years=0
        number_of_years_current_role_15_above=0
        
    elif number_of_years_current_role==3:
        number_of_years_current_role_less_than_year=0
        number_of_years_current_role_1_3_years=0
        number_of_years_current_role_3_5_years=1
        number_of_years_current_role_5_10_years=0
        number_of_years_current_role_10_15_years=0
        number_of_years_current_role_15_above=0
        
    elif number_of_years_current_role==4:
        number_of_years_current_role_less_than_year=0
        number_of_years_current_role_1_3_years=0
        number_of_years_current_role_3_5_years=0
        number_of_years_current_role_5_10_years=1
        number_of_years_current_role_10_15_years=0
        number_of_years_current_role_15_above=0

    elif number_of_years_current_role==5:
        number_of_years_current_role_less_than_year=0
        number_of_years_current_role_1_3_years=0
        number_of_years_current_role_3_5_years=0
        number_of_years_current_role_5_10_years=0
        number_of_years_current_role_10_15_years=1
        number_of_years_current_role_15_above=0
        
    else:
        number_of_years_current_role_less_than_year=0
        number_of_years_current_role_1_3_years=0
        number_of_years_current_role_3_5_years=0
        number_of_years_current_role_5_10_years=0
        number_of_years_current_role_10_15_years=0
        number_of_years_current_role_15_above=1

        
    if (department==1):
        department_food_beverages=1
        department_front_office=0
        department_housekeeping=0
        department_maintenance=0
        department_security=0

    elif department==2:
        department_food_beverages=0
        department_front_office=1
        department_housekeeping=0
        department_maintenance=0
        department_security=0
        
    elif department==3:
        department_food_beverages=0
        department_front_office=0
        department_housekeeping=1
        department_maintenance=0
        department_security=0
        
    elif department==4:
        department_food_beverages=0
        department_front_office=0
        department_housekeeping=0
        department_maintenance=1
        department_security=0
        
    else:
        department_food_beverages=0
        department_front_office=0
        department_housekeeping=0
        department_maintenance=0
        department_security=1


    datapoint = pd.DataFrame({
        'salary': salary,                  
        'opportunities': opportunities,
        'workload': workload,
        'age_category_20 - 30':age_category_20_30,
        'age_category_30 - 40': age_category_30_40, 
        'age_category_Above 40':age_category_above_40, 
        'gender_Female':gender_female,
        'gender_Male':gender_male,
        'marital_status_Married with children':marital_status_Married_with_children,
        'marital_status_Married without children':marital_status_Married_without_children, 
        'marital_status_Single':marital_status_Single,
        'educational_status_A/L passer':educational_status_al_passer, 
        'educational_status_Below O/L':educational_status_below_ol,
        'educational_status_Degree holder':educational_status_degree_holder, 
        'educational_status_Diploma holder':educational_status_diploma_holder,
        'educational_status_O/L passer':educational_status_ol_passer, 
        'total_years_industry_1 - 3 years':total_years_industry_1_3_years,
        'total_years_industry_10 - 15 years':total_years_industry_10_15_years,
        'total_years_industry_15 years and above':total_years_industry_15_years_above,
        'total_years_industry_3 - 5 years':total_years_industry_3_5_years, 
        'total_years_industry_5 - 10 years':total_years_industry_5_10_years,
        'total_years_industry_Less than 1 year':total_years_industry_less_than_1_year,
        'years_work_current_hotel_1 - 3 years':years_work_current_hotel_1_3_years,
        'years_work_current_hotel_10 - 15 years':years_work_current_hotel_10_15_years,
        'years_work_current_hotel_15 years and above':years_work_current_hotel_15_above,
        'years_work_current_hotel_3 - 5 years':years_work_current_hotel_3_5_years,
        'years_work_current_hotel_5 - 10 years':years_work_current_hotel_5_10_years,
        'years_work_current_hotel_Less than 1 year':years_work_current_hotel_less_than_year,
        'number_of_years_current_role_1 - 3 years':number_of_years_current_role_1_3_years,
        'number_of_years_current_role_10 - 15 years':number_of_years_current_role_10_15_years,
        'number_of_years_current_role_15 years and above':number_of_years_current_role_15_above,
        'number_of_years_current_role_3 - 5 years':number_of_years_current_role_3_5_years,
        'number_of_years_current_role_5 - 10 years':number_of_years_current_role_5_10_years,
        'number_of_years_current_role_Less than 1 year':number_of_years_current_role_less_than_year,
        'department_Food and Beverages':department_food_beverages, 
        'department_Front office':department_front_office,
        'department_Housekeeping':department_housekeeping, 
        'department_Maintenance':department_maintenance,
        'department_Security':department_security},index=[0])
    
    logging.info('EmployeeServices - predict_employee_turnover_days() datapoint initiated')
    
    #model/sclaers importing
    xgbr_model = pickle.load(open("prediction_model/turnover_days_model/employee_turnover_days_xgb_regression_updated_model.pkl", 'rb'))
    mx_input_scaler = pickle.load(open("prediction_model/turnover_days_model/employee_turnover_days_features_min_max_feature_updated_scaler.pkl", 'rb'))
    mx_output_scaler = pickle.load(open("prediction_model/turnover_days_model/employee_turnover_days_features_min_max_output_updated_scaler.pkl", 'rb'))

    logging.info('EmployeeServices - predict_employee_turnover_days() modesl/scaled impored')

    #scaling
    scaled_datapoint = mx_input_scaler.transform(datapoint)

    #predicting
    pred_results=xgbr_model.predict(scaled_datapoint)
    inverese_transformed_results = mx_output_scaler.inverse_transform(pred_results.reshape(1, -1)) #outputs in days
    return ((int(inverese_transformed_results[0][0]))//30)+1 # returns the num of days in months

