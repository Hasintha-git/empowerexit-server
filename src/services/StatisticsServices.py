import io
import logging
from flask import Response,send_file
from collections import Counter
import time

from flask import Blueprint, request
from src.constants.general_constants import SUCCESS,ERROR,RESPONSE_RETURN_TYPE,EXCEPTION_MSG,REPORTS_SAVING_PATH
from src.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from src.dto.EmployeeAnalyticsDto import EmployeeAnalyticsDto
from src.dto.TurnoverDriverWithRateDto import TurnoverDriverWithRateDto
from src.dto.TurnoverRateWithMonthDto import TurnoverRateWithMonthDto
from src.models.Database import db, Employee, Prediction, TurnoverFactor, PredictionFactorMapping,Department
from flask_jwt_extended import jwt_required

from ..dto.ResponseDto import ResponseDto
from ..dto.EmployeeDepartmentStat import EmployeeDepartmentStat
from ..dto.HighPerformanceEmpStat import HighPerformanceEmpStat
from ..helpers.ReportGeneratingServices import generate_pdf
from ..helpers.HelperFunctions import get_current_month_start_date,get_current_month_end_date,get_current_month_name,get_current_year,get_custom_past_date,get_month_from_the_date,get_year_from_the_date

statistics = Blueprint("statistics", __name__, url_prefix='/api/v1/statistics')


@statistics.get('/employees/latest')
@jwt_required()
def get_employee_latest_stats():
    try:
        logging.info('StatisticsServices - get_employee_latest_stats() CALLED')

        current_month_first_date = get_current_month_start_date()
        current_month_last_date = get_current_month_end_date()

        # dashboard first stat-section
        # total emp count
        total_emp_count = len(Employee.query.all())
        total_emp_turnover_true_list = db.session.query(Prediction.fk_emp_id).filter(Prediction.is_leaving == True).filter(Prediction.updated_timestamp >= current_month_first_date).filter(Prediction.updated_timestamp <= current_month_last_date).all()
        total_emp_turnover_true_count = len(total_emp_turnover_true_list)

        #retriving emp record to check performance level (A) and Department
        total_emp_a_rated_turnover_true_count=0
        department_id_list = []
        highest_turnover_rate_dpt=""
        for turnover_true_emp in total_emp_turnover_true_list:

             # dashboard second stat-section
            emp_record = db.session.query(Employee).filter(Employee.id ==turnover_true_emp.fk_emp_id).first()
            department_id_list.append(emp_record.fk_department_id)

            #dashboard third stat-section
            if emp_record.performance_grade == "A":
                total_emp_a_rated_turnover_true_count=total_emp_a_rated_turnover_true_count+1
        
        # assigning the most frequeny department (econd stat-section)
        highest_turnover_rate_dpt =  Department.query.filter_by(id=max(department_id_list,key=department_id_list.count)).first().name

         # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                                  msg="EMPLOYEE DASHBOARD STATS RETRIEVED SUCCESSFULLY",
                                  data={"month_name":get_current_month_name(),
                                        "year":get_current_year(),
                                        "total_employee_count":total_emp_count,
                                        "turnover_true_emp_count":total_emp_turnover_true_count,
                                        "turnover_true_A_rated_emp_count":total_emp_a_rated_turnover_true_count,
                                        "highest_turnover_rate_department":highest_turnover_rate_dpt}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)
    

    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_latest_stats() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)

@statistics.get('/employees/department')
@jwt_required()
def get_employee_department_stats():
    try:
        logging.info('StatisticsServices - get_employee_department_stats() CALLED')

        current_month_first_date = get_current_month_start_date()
        current_month_last_date = get_current_month_end_date()

        # total emp count
        total_emp_count = len(Employee.query.all())
        total_emp_turnover_true_list = db.session.query(Prediction.fk_emp_id).filter(Prediction.is_leaving == True).filter(Prediction.updated_timestamp >= current_month_first_date).filter(Prediction.updated_timestamp <= current_month_last_date).all()
        total_emp_turnover_true_count = len(total_emp_turnover_true_list)
        total_emp_turnover_true_count_percentage = round((total_emp_turnover_true_count/total_emp_count) * 100)

        # retriving emp record to check Departments
        turnover_true_department_id_list = []
        for turnover_true_emp in total_emp_turnover_true_list:

            # department Ids retrieving 
            emp_record = db.session.query(Employee).filter(Employee.id ==turnover_true_emp.fk_emp_id).first()
            turnover_true_department_id_list.append(emp_record.fk_department_id)

        # calculating total department wise count
        emp_dept_stats_list =[]
        for dep_id in list(set(turnover_true_department_id_list)):
             
            department_name = Department.query.filter_by(id=dep_id).first().name
            department_total_count = len(db.session.query(Employee).filter(Employee.fk_department_id ==dep_id).all())
            department_total_predicted_true_count = turnover_true_department_id_list.count(dep_id)
            department_total_predicted_true_percentage = str(round((department_total_predicted_true_count/department_total_count) * 100)) +"%"

            employee_department_stat = EmployeeDepartmentStat(dep_id,department_name,department_total_count,
                                                              department_total_predicted_true_count,department_total_predicted_true_percentage)
            emp_dept_stats_list.append(employee_department_stat)

        # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                msg="EMPLOYEE DEPARTMENT WISE STATS RETRIEVED SUCCESSFULLY",
                data={"month_name":get_current_month_name(),
                  "year":get_current_year(),
                      "turnover_true_emp_count":total_emp_turnover_true_count,
                      'total_emp_turnover_true_count_percentage':total_emp_turnover_true_count_percentage,
                      "total_emp_turnover_true_dept_stats":emp_dept_stats_list}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_department_stats() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)
    

@statistics.get('/employees/performance')
@jwt_required()
def get_employee_high_performance_emp_stats():
    try:
        logging.info('StatisticsServices - get_employee_high_performance_emp_stats() CALLED')

        current_month_first_date = get_current_month_start_date()
        current_month_last_date = get_current_month_end_date()

        # total_emp_turnover_true_list (prediced as True for turnover)
        total_emp_turnover_true_list = db.session.query(Prediction).filter(Prediction.is_leaving == True).filter(Prediction.updated_timestamp >= current_month_first_date).filter(Prediction.updated_timestamp <= current_month_last_date).all()

        # retriving emp records
        employee_data = []
        for turnover_true_emp in total_emp_turnover_true_list:

            # emp data retrieving and initiating dara objects
            emp_record = db.session.query(Employee).filter(Employee.id ==turnover_true_emp.fk_emp_id).first()

            if(emp_record.performance_grade=="A"):
                high_performance_emp_stat_data=HighPerformanceEmpStat(emp_record.emp_id,emp_record.name,int(round(float(turnover_true_emp.turnover_rate),2)*100))
                employee_data.append(high_performance_emp_stat_data)

        # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                msg="HIGH PERFORMANCE EMPLOYE STATS RETRIEVED SUCCESSFULLY",
                data={"month_name":get_current_month_name(),"year":get_current_year(),"high_performance_emp_stats":employee_data}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_high_performance_emp_stats() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)


@statistics.get('/employees/turnover_drivers')
@jwt_required()
def get_employee_trunover_drivers_stats():
    try:
        logging.info('StatisticsServices - get_employee_trunover_drivers_stats() CALLED')

        current_month_first_date = get_current_month_start_date()
        current_month_last_date = get_current_month_end_date()

        # retriving the driver-pred mappings in the cureent month
        drivers_in_cureent_month = db.session.query(PredictionFactorMapping.fk_factor_id,PredictionFactorMapping.fk_prediction_id).filter(PredictionFactorMapping.updated_timestamp>= current_month_first_date).filter(PredictionFactorMapping.updated_timestamp <= current_month_last_date).all()
        drivers_of_true_turnover = []
        for driver in drivers_in_cureent_month:
          
            # prediction retriving and adding the driver if turnover pred is true
            prediction = db.session.query(Prediction).filter(Prediction.id==driver.fk_prediction_id).filter(Prediction.updated_timestamp>= current_month_first_date).filter(Prediction.updated_timestamp <= current_month_last_date).first()
            
            if prediction is not None:
                
                if(prediction.is_leaving):
                    drivers_of_true_turnover.append(driver.fk_factor_id)

        drivers_of_true_turnover_frequency = Counter(drivers_of_true_turnover).most_common(5)

        #top_turnover_drivers_map = {}
        top_turnover_drivers_list = []
        for factor in drivers_of_true_turnover_frequency:
         
            driver_name =  db.session.query(TurnoverFactor).filter(TurnoverFactor.id==factor[0]).first().display_name
            #top_turnover_drivers_map[driver_name]=factor[1]
            turnover_driver_with_rate = TurnoverDriverWithRateDto(name=driver_name,rate=factor[1])
            top_turnover_drivers_list.append(turnover_driver_with_rate)

        # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                msg="TURNOVER DRIVER STATS RETRIEVED SUCCESSFULLY",
                data={"month_name":get_current_month_name(),
                      "year":get_current_year(),
                      "top_drivers":top_turnover_drivers_list}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype='application/json')
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_trunover_drivers_stats() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)


@statistics.get('/employees/last_predictions')
@jwt_required()
def get_employee_trunover_last_predictions():
    try:
        logging.info('StatisticsServices - get_employee_trunover_last_predictions() CALLED')

       # past_predictions_map ={}
        past_predictions_list = []
        for value in reversed(range(5)):
            
            # generating past months (5 months)
            past_date = get_custom_past_date(value)
            generated_year =str(get_year_from_the_date(past_date))
            generated_month = str(get_month_from_the_date(past_date))
            start_date = generated_year+"-"+generated_month+"-01"
            end_date = generated_year+"-"+generated_month+"-31"

            # retriving the true predictions fro the date range and appending them to the map
            true_predictions_count = len(db.session.query(Prediction).filter(Prediction.is_leaving==True).filter(Prediction.updated_timestamp>= start_date).filter(Prediction.updated_timestamp <= end_date).all())
            turnover_rate_with_month =TurnoverRateWithMonthDto(date=generated_year+"-"+generated_month,rate=true_predictions_count)
            past_predictions_list.append(turnover_rate_with_month)
            #past_predictions_map[generated_year+"-"+generated_month] = true_predictions_count

        # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                msg="PAST TURNOVER PREDICTIONS RETRIEVED SUCCESSFULLY",
                data={"past_predictions":past_predictions_list}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_trunover_last_predictions() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)
    

@statistics.get('/employees/analytics')
@jwt_required()
def get_employee_analytics():
    try:
        logging.info('StatisticsServices - get_employee_analytics() CALLED')

        # all employees retrieving
        employee_analytics_list = []
        employees = db.session.query(Employee).all()
        for employee in employees:

            # dpt name retrieving
            department_name = Department.query.filter_by(id=employee.fk_department_id).first().name

            # emp latest prediction retrieving
            emp_latest_prediction = db.session.query(Prediction).filter(Prediction.fk_emp_id == employee.id).order_by(Prediction.updated_timestamp.desc()).first()
            
            # results initaiting
            if(emp_latest_prediction is None):
                # if no predictions
                employee_analytics_list.append(EmployeeAnalyticsDto(employee.id,employee.emp_id,employee.name,department_name,employee.performance_grade,"-","-"))
            else:
                if emp_latest_prediction.is_leaving:

                    months_to_leave =emp_latest_prediction.month_to_leave
                    employee_analytics_list.append(EmployeeAnalyticsDto(employee.id,employee.emp_id,employee.name,department_name,employee.performance_grade,
                                                                        str(int(round(float(emp_latest_prediction.turnover_rate),2)*100))+"%",str(months_to_leave) +" month(s)"))
                
                else:
                    employee_analytics_list.append(EmployeeAnalyticsDto(employee.id,employee.emp_id,employee.name,department_name,employee.performance_grade,"0%","-"))

        # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                msg="EMPLOYEE ANALYTICS RETRIEVED SUCCESSFULLY",
                data={"employee_analytics":employee_analytics_list}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_analytics() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)



@statistics.post('/employees/analytics/serach')
@jwt_required()
def get_employee_analytics_search_results():
    try:
        logging.info('StatisticsServices - get_employee_analytics_search_results() CALLED')

        # required fields validating (values exits or not)
        values = request.json
        if not (all(key in values for key in ('emp_id','department_value','performance_value','retention_value','turnover_value'))):
            response_dto =ResponseDto(status=ERROR,msg='REQUIRED FIELDS ARE MISSING',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)
        
        # required fields validating (values empty or not)
        if any(value == "" for value in values.values()):
            response_dto =ResponseDto(status=ERROR,msg='REQUIRED FIELDS ARE EMPTY',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)
        

        # capturing the body data
        emp_id = values['emp_id']
        department_id = values['department_value']
        emp_performance = values['performance_value']
        retention_period = values['retention_value']
        turnover_value_range = values['turnover_value']


        
        results =[]
        if emp_id is not None:
            # retriving all emp data matches to input emp ids
            emp_id = "{}%".format(emp_id)
            results = Employee.query.filter(Employee.emp_id.like(emp_id)).all()
        else:
            results = db.session.query(Employee).all()


        # department wise filtering
        if department_id is not None and len(department_id)>0:

            filtered_records_by_department = []
            for result in results:

                if result.fk_department_id in department_id:
                    filtered_records_by_department.append(result)

            results = filtered_records_by_department


        # performance wise filtering
        if emp_performance is not None and len(emp_performance)>0:

            filtered_records_by_performance = []
            for result in results:

                if result.performance_grade in emp_performance:
                    filtered_records_by_performance.append(result)

            results = filtered_records_by_performance
            

        # retention_period wise filtering (# days to leave)
        if retention_period is not None and len(retention_period)>0:
            
            all_retention_filtered_results = []
            for value in retention_period:

                retention_period_start=0
                retention_period_end = 0
                if (value==1):
                    retention_period_start = 0
                    retention_period_end = 2
                elif (value==2):
                    retention_period_start = 3
                    retention_period_end = 5
                elif (value==3):
                    retention_period_start = 6
                    retention_period_end = 11
                elif (value==4):
                    retention_period_start = 12
                    retention_period_end = 1000

                filtered_records_by_retention_period = []
                for result in results:

                    if(result.latest_months_to_leave=="-"):
                        continue
            
                    if int(result.latest_months_to_leave) >= retention_period_start and  int(result.latest_months_to_leave) <retention_period_end :
                        filtered_records_by_retention_period.append(result)

                all_retention_filtered_results.extend(filtered_records_by_retention_period)

            results = all_retention_filtered_results
        

        # turnover rate wise filtering
        if turnover_value_range is not None and len(turnover_value_range)>0:

            all_turnover_value_filtered_results = []
            for value in turnover_value_range:

                # turnover rates
                turnover_value_start=0
                turnover_value_end = 0
                if (value==1):
                    turnover_value_start = 0
                    turnover_value_end = 25
                elif (value==2):
                    turnover_value_start = 26
                    turnover_value_end = 50
                elif (value==3):
                    turnover_value_start = 51
                    turnover_value_end = 75
                elif (value==4):
                    turnover_value_start = 76
                    turnover_value_end = 100


                filtered_records_by_turnover_value_range = []
                for result in results:

                    if(result.latest_turnover_rate=="-"):
                        continue

                    if int(round(float(result.latest_turnover_rate),2)*100) >= turnover_value_start and  int(round(float(result.latest_turnover_rate),2)*100) < turnover_value_end :
                        filtered_records_by_turnover_value_range.append(result)

                all_turnover_value_filtered_results.extend(filtered_records_by_turnover_value_range)

            results = all_turnover_value_filtered_results


        # final results list initializing
        search_results = []
        for result in results:

            # dpt name retrieving
            department_name = Department.query.filter_by(id=result.fk_department_id).first().name

            # - and value seperating
            probability_value=""
            if result.latest_turnover_rate == "-":
                probability_value = "-"
            else:
                probability_value = str(int(round(float(result.latest_turnover_rate),2)*100))+"%"


            search_results.append(EmployeeAnalyticsDto(id=result.id,emp_id=result.emp_id,name=result.name,
                                                       department=department_name,performance=result.performance_grade,
                                                       probability=probability_value,
                                                       period=str(result.latest_months_to_leave) +" months(s)"))

        # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                msg="EMPLOYEE ANALYTICS SEARCH RESULTS RETRIEVED SUCCESSFULLY",
                data={"results":search_results}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_analytics_search_results() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)
    



@statistics.post('/employees/analytics/serach/download')
@jwt_required()
def get_employee_analytics_search_results_report():
    try:
        logging.info('StatisticsServices - get_employee_analytics_search_results_report() CALLED')

        # required fields validating (values exits or not)
        values = request.json
        if not "values" in values:
            response_dto =ResponseDto(status=ERROR,msg='REQUIRED FIELDS ARE MISSING',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)
        
        # required fields validating (values empty or not)
        if any(value == "" for value in values.values()):
            response_dto =ResponseDto(status=ERROR,msg='REQUIRED FIELDS ARE EMPTY',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)
        

        # capturing the body data
        values = values['values']
        
        if len(values)<=0:
            response_dto =ResponseDto(status=ERROR,msg='EMPTY DATA CANNOT PRINT',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)
        

        pdf_data_cols = ["Employee Id", "Employee Name","Department","Performance Grade","Turnover Rate","Retention Period"]
        pdf_data =[]
        for record in values:
            pdf_data.append([record['emp_id'],record['name'],record['department'],record['performance'],str(record['probability']),str(record['period'])])


        generate_pdf(file_path=REPORTS_SAVING_PATH,file_name="analytics_report.pdf",logo_path="src/assets/logo.png",header_data=pdf_data_cols,body_data=pdf_data)
        
        # file opening and sending
        time.sleep(5)
        generated_file = open(REPORTS_SAVING_PATH+"analytics_report.pdf", "rb")
        return send_file(io.BytesIO(generated_file.read()),as_attachment=True, download_name='analytics_report.pdf',mimetype='application/pdf')
    
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_analytics_search_results_report() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None).toJSON()
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)
    

@statistics.get('/department/insights')
@jwt_required()
def get_department_insights():
    # try:
        logging.info('StatisticsServices - get_department_insights() CALLED')

        #all departments retrieving
        departments = db.session.query(Department).all()
        print(len(departments))
        print(type(departments))
        department_insights = []
        highest_a_department_count=0
        highest_a_department_name=""
        highest_department_count=0
        highest_department_name=""
        lowest_department_count=100
        lowest_department_name=""
        for department in departments:
            employees=Employee.query.filter_by(fk_department_id=department.id).all()

            employee_A_total=0
            employee_A_turnover_true=0
            employee_B_total=0
            employee_B_turnover_true=0
            employee_C_total=0
            employee_C_turnover_true=0
            employee_D_total=0
            employee_D_turnover_true=0
            for employee in employees:
                if employee.performance_grade=="A":
                    employee_A_total+=1
                    if employee.is_leaving:
                        employee_A_turnover_true+=1
                elif employee.performance_grade=="B":
                    employee_B_total+=1
                    if employee.is_leaving:
                        employee_B_turnover_true+=1
                elif employee.performance_grade=="C":
                    employee_C_total+=1
                    if employee.is_leaving:
                        employee_C_turnover_true+=1
                elif employee.performance_grade=="D":
                    employee_D_total+=1
                    if employee.is_leaving:
                        employee_D_turnover_true+=1
            total_turonover_count = employee_A_turnover_true+employee_B_turnover_true+employee_C_turnover_true+employee_D_turnover_true
            grade_a_avg=0
            if employee_A_total>0:
                grade_a_avg = round((employee_A_turnover_true/total_turonover_count) * 100)
            grade_b_avg=0
            if employee_B_total>0:
                grade_b_avg = round((employee_B_turnover_true/total_turonover_count) * 100)
            grade_c_avg=0
            if employee_C_total>0:
                grade_c_avg = round((employee_C_turnover_true/total_turonover_count) * 100)
            grade_d_avg=0
            if employee_D_total>0:
                grade_d_avg = round((employee_D_turnover_true/total_turonover_count) * 100)

            avg_turnover_rate = round(total_turonover_count/len(employees)* 100)

            if highest_a_department_count<employee_A_total:
                highest_a_department_count=employee_A_total
                highest_a_department_name = department.name

            if highest_department_count<avg_turnover_rate:
                highest_department_count=avg_turnover_rate
                highest_department_name = department.name

            if lowest_department_count>avg_turnover_rate:
                lowest_department_count=avg_turnover_rate
                lowest_department_name = department.name

            department_insights.append({
                "department_name":department.name,
                 "total_emp":len(employees),
                 "avg_turnover_rate":str(avg_turnover_rate)+'%',
                 "chart_data":[{"Grade A " +str(grade_a_avg)+"%":grade_a_avg,
                                "Grade B " +str(grade_b_avg)+"%":grade_b_avg,
                                "Grade C " +str(grade_c_avg)+"%":grade_c_avg,
                                "Grade D " +str(grade_d_avg)+"%":grade_d_avg}],
                 "predicted_turnovers":
                 "Grade A: "+str(employee_A_turnover_true)+"/"+str(employee_A_total)
                 +", Grade B:"+str(employee_B_turnover_true)+"/"+str(employee_B_total) 
                 +", Grade C: "+str(employee_C_turnover_true)+"/"+str(employee_C_total) 
                 +", Grade D: "+str(employee_D_turnover_true)+"/"+str(employee_D_total)   
                }) 
        
       # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                msg="DEPARTMENT INSIGHTS RETRIEVED SUCCESSFULLY",
                data={"department_insight_stats":{
                        "date":str(get_current_month_name())+" "+str(get_current_year()),
                        "highest_gradeA_dept":highest_a_department_name,
                        "highest_dept":highest_department_name,
                        "lowest_dept":lowest_department_name},
                      "department_insights":department_insights}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)

    
    # except (ValueError, Exception):
    #     db.session.rollback()
    #     db.session.flush()
    #     logging.error('EmployeeServices - get_department_insights() ERROR :' + str(Exception))

    #     response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
    #     return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)
