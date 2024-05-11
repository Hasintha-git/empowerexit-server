import logging
import datetime
from datetime import date


from flask import Blueprint, request, jsonify
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_422_UNPROCESSABLE_ENTITY
from src.dto.EmployeeDto import EmployeeDto
from src.dto.EmployeeTurnoverAnalyticsDto import EmployeeTurnoverAnalyticsDto
from src.dto.EmployeeTurnoverEvaluationDto import EmployeeTurnoverEvaluationDto
from src.dto.EvaluationDto import EvaluationDto
from src.dto.TurnoverDriverWithRateDto import TurnoverDriverWithRateDto
from src.models.Database import db, Employee, Prediction, TurnoverFactor, PredictionFactorMapping,Department
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

from ..dto.ResponseDto import ResponseDto

from flask import Response
from src.constants.general_constants import SUCCESS,ERROR,RESPONSE_RETURN_TYPE,EXCEPTION_MSG

from ..dto.EmployeeSurveyClassificationData import EmployeeSurveyClassificationData
from ..dto.EmployeeSurveyRegressionData import EmployeeSurveyRegressionData
from ..helpers.PredictionService import predict_employee_turnover,predict_employee_turnover_days
from ..helpers.HelperFunctions import get_current_month_start_date,get_current_month_end_date, get_month_from_the_date,get_tuned_count, get_month_name, get_year_from_the_date

employee = Blueprint("employee", __name__, url_prefix='/api/v1/employee')


@employee.post('/register')
@jwt_required()
def employee_register():
    try:
        logging.info('EmployeeServices - employee_register() CALLED')

        # required fields validating (values exits or not)
        values = request.json
        if not (all(key in values for key in (
                "emp_id", "name", "designation", "department_id", "address", "contact", "supervisor",
                "joined_date", "performance_grade"))):
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'REQUIRED FIELDS ARE MISSING', "DATA": None}), HTTP_400_BAD_REQUEST

        # required fields validating (values empty or not)
        if any(value == "" for value in values.values()):
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'REQUIRED FIELDS ARE EMPTY', "DATA": None}), HTTP_400_BAD_REQUEST

        # capturing the body data
        emp_id = values['emp_id']
        name = values['name']
        designation = values['designation']
        department_id = values['department_id']
        address = values['address']
        contact = values['contact']
        supervisor = values['supervisor']
        joined_date = values['joined_date']
        performance_grade = values['performance_grade']

        # emp id status validating
        if Employee.query.filter_by(emp_id=emp_id).first() is not None:
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'EMPLOYEE IS IS ALREADY IN USE: ', "DATA": None}), HTTP_409_CONFLICT

        # object initialization
        employe = Employee(emp_id=emp_id, name=name, designation=designation, fk_department_id=department_id,
                           address=address, contact=contact, supervisor=supervisor, joined_date=joined_date,
                           performance_grade=performance_grade, note="",is_leaving=False,latest_turnover_rate="-",
                            latest_months_to_leave="-", created_timestamp=datetime.datetime.now(),
                           updated_timestamp=datetime.datetime.now())

        # db commit
        db.session.add(employe)
        db.session.commit()

        return jsonify(
            {'STATUS': "SUCCESS", 'MESSAGE': 'EMPLOYEE CREATED SUCCESSFULLY',
             "DATA": employe.__str__()}), HTTP_201_CREATED

    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - employee_register() ERROR :' + str(Exception))

        return jsonify(
            {'STATUS': "ERROR", 'MESSAGE': 'EXCEPTION OCCURRED: ' + str(Exception),
             "DATA": None}), HTTP_500_INTERNAL_SERVER_ERROR


@employee.put('/update')
@jwt_required()
def employee_update():
    try:
        logging.info('EmployeeServices - employee_update() CALLED')

        # required fields validating (values exits or not)
        values = request.json
        if not (all(key in values for key in (
                "id", "emp_id", "name", "designation", "department_id", "address", "contact", "supervisor", "note",
                "joined_date", "performance_grade"))):
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'REQUIRED FIELDS ARE MISSING', "DATA": None}), HTTP_400_BAD_REQUEST

        # capturing the body data
        emp_sys_id = values["id"]
        emp_id = values['emp_id']
        name = values['name']
        designation = values['designation']
        department_id = values['department_id']
        address = values['address']
        contact = values['contact']
        supervisor = values['supervisor']
        note = values['note']
        joined_date = values['joined_date']
        performance_grade = values['performance_grade']

        # emp id status validating
        if Employee.query.filter_by(id=emp_sys_id).first() is None:
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'EMPLOYEE ID NOT FOUND', "DATA": None}), HTTP_400_BAD_REQUEST

        # db commit
        employe = Employee.query.get(emp_sys_id)
        employe.emp_id = emp_id
        employe.name = name
        employe.designation = designation
        employe.fk_department_id = department_id
        employe.address = address
        employe.contact = contact
        employe.supervisor = supervisor
        employe.note = note
        employe.joined_date = joined_date
        employe.performance_grade = performance_grade
        employe.updated_timestamp = datetime.datetime.now()
        db.session.commit()

        return jsonify(
            {'STATUS': "SUCCESS", 'MESSAGE': 'EMPLOYEE UPDATED SUCCESSFULLY',
             "DATA": employe.__str__()}), HTTP_200_OK

    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - employee_update() ERROR :' + str(Exception))

        return jsonify(
            {'STATUS': "ERROR", 'MESSAGE': 'EXCEPTION OCCURRED: ' + str(Exception),
             "DATA": None}), HTTP_500_INTERNAL_SERVER_ERROR


@employee.delete('/delete')
@jwt_required()
def employee_delete():
    try:
        logging.info('EmployeeServices - employee_delete() CALLED')

        # required fields validating (values exits or not)
        values = request.args
        if not "id" in values:
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'REQUIRED FIELDS ARE MISSING', "DATA": None}), HTTP_400_BAD_REQUEST

        # required fields validating (values empty or not)
        if any(value == "" for value in values.values()):
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'REQUIRED FIELDS ARE EMPTY', "DATA": None}), HTTP_400_BAD_REQUEST

        # capturing the body data
        emp_sys_id = values["id"]

        # emp id status validating
        if Employee.query.filter_by(id=emp_sys_id).first() is None:
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'EMPLOYEE ID NOT FOUND', "DATA": None}), HTTP_422_UNPROCESSABLE_ENTITY
        

        # if predictions exists deleting them
        employee_prediction_records = db.session.query(Prediction).filter(Prediction.fk_emp_id == emp_sys_id).all()
        for record in employee_prediction_records:
            
            # mappings liest retreiving 
            prediction_record_mappings = db.session.query(PredictionFactorMapping).filter(PredictionFactorMapping.fk_prediction_id == record.id).all()
            
            # mappings deleting
            for mapping in prediction_record_mappings:
                PredictionFactorMapping.query.filter(PredictionFactorMapping.id == mapping.id).delete()

            # prediction deleting
            Prediction.query.filter(Prediction.id == record.id).delete()


        # emp deleting
        Employee.query.filter(Employee.id == emp_sys_id).delete()
        db.session.commit()

        return jsonify(
            {'STATUS': "SUCCESS", 'MESSAGE': 'EMPLOYEE DELETED SUCCESSFULLY', "DATA": None}), HTTP_200_OK

    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - employee_delete() ERROR :' + str(Exception))

        return jsonify(
            {'STATUS': "ERROR", 'MESSAGE': 'EXCEPTION OCCURRED: ' + str(Exception),
             "DATA": None}), HTTP_500_INTERNAL_SERVER_ERROR


@employee.post('/survey')
def employee_survey():
    # try:
        logging.info('EmployeeServices - employee_survey() CALLED')

        # required fields validating (values exits or not)
        values = request.json
        if not (all(key in values for key in (
                "emp_id", "working_hours", "promotional_barriers", "work_life_balance", "status_and_recognition",
                "salary", "opportunities", "workload", "work_environment", "training_and_development",
                "relationship_with_colleagues", "relationship_with_supervisor", "job_satisfaction",
                "distance_from_home", "age", "gender", "marital_status", "educational_status", "total_years_industry",
                "years_work_current_hotel", "number_of_years_current_role", "last_promotion",
                "hotel_assess_performance"))):
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'REQUIRED FIELDS ARE MISSING', "DATA": None}), HTTP_400_BAD_REQUEST

        # required fields validating (values empty or not)
        if any(value == "" for value in values.values()):
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'REQUIRED FIELDS ARE EMPTY', "DATA": None}), HTTP_400_BAD_REQUEST

        # capturing the body data
        emp_id = values['emp_id']
        working_hours = values['working_hours']
        promotional_barriers = values['promotional_barriers']
        work_life_balance = values['work_life_balance']
        status_and_recognition = values['status_and_recognition']
        salary = values['salary']
        opportunities = values['opportunities']
        workload = values['workload']
        work_environment = values['work_environment']
        training_and_development = values['training_and_development']
        relationship_with_colleagues = values['relationship_with_colleagues']
        relationship_with_supervisor = values['relationship_with_supervisor']
        job_satisfaction = values['job_satisfaction']
        distance_from_home = values['distance_from_home']
        age = values['age']
        gender = values['gender']
        marital_status = values['marital_status']
        educational_status = values['educational_status']
        total_years_industry = values['total_years_industry']
        years_work_current_hotel = values['years_work_current_hotel']
        number_of_years_current_role = values['number_of_years_current_role']
        last_promotion = values['last_promotion']
        hotel_assess_performance = values['hotel_assess_performance']

        # emp id status validating
        employee_record = Employee.query.filter_by(emp_id=emp_id).first()
        if employee_record is None:
            return jsonify(
                {'STATUS': "ERROR", 'MESSAGE': 'EMPLOYEE ID NOT FOUND', "DATA": None}), HTTP_400_BAD_REQUEST

        # emp system id
        emp_sys_id = employee_record.id
        emp_department =employee_record.fk_department_id
        employee_survey_classification_data = EmployeeSurveyClassificationData(working_hours=working_hours,
                                                  promotional_barriers=promotional_barriers,
                                                  work_life_balance=work_life_balance,
                                                  status_and_recognition=status_and_recognition, salary=salary,
                                                  opportunities=opportunities, workload=workload,
                                                  work_environment=work_environment,
                                                  training_and_development=training_and_development,
                                                  relationship_with_colleagues=relationship_with_colleagues,
                                                  relationship_with_supervisor=relationship_with_supervisor,
                                                  job_satisfaction=job_satisfaction,
                                                  distance_from_home=distance_from_home,
                                                  age=age, gender=gender, marital_status=marital_status,
                                                  educational_status=educational_status,
                                                  total_years_industry=total_years_industry,
                                                  years_work_current_hotel=years_work_current_hotel,
                                                  number_of_years_current_role=number_of_years_current_role,
                                                  department=emp_department, last_promotion=last_promotion,
                                                  hotel_assess_performance=hotel_assess_performance)
        
        # predicted result, score and factor
        employee_turnover_result = predict_employee_turnover(employee_survey_classification_data)
        print(employee_turnover_result.score)


        current_month_first_date = get_current_month_start_date()
        current_month_last_date = get_current_month_end_date()

        # checking if past prediction for the current month is exits or not. if exits updating it else adding new record
        employee_prediction_record = db.session.query(Prediction).filter(Prediction.fk_emp_id == emp_sys_id).filter(Prediction.updated_timestamp >= current_month_first_date).filter(Prediction.updated_timestamp <= current_month_last_date).first()
        if employee_prediction_record is None:
            # object initialization (prediction)
            employee_prediction_record = Prediction(fk_emp_id=emp_sys_id,
                                    is_leaving=employee_turnover_result.is_leaving,
                                    turnover_rate=employee_turnover_result.score,
                                    created_timestamp=datetime.datetime.now(),
                                    updated_timestamp=datetime.datetime.now())
            
            # days calculation
            employee_survey_regression_data = EmployeeSurveyRegressionData(  
                age=age, 
                gender=gender, 
                marital_status=marital_status,
                educational_status=educational_status,
                total_years_industry=total_years_industry,
                years_work_current_hotel=years_work_current_hotel,
                number_of_years_current_role=number_of_years_current_role,
                department=emp_department,
                salary=salary,
                opportunities=opportunities, 
                workload=workload) 
            
            employee_turnover_days_in_months =predict_employee_turnover_days(employee_survey_regression_data)#days to leave
            
            # deducting predicted total months from worked months from joined date to get rest days
            emp_worked_days = date.today()-date(employee_record.joined_date.year,employee_record.joined_date.month,employee_record.joined_date.day) # worked days from date of joined
            emp_worked_days_in_months = (emp_worked_days.days// 30) +1
            emp_worked_days_in_months=get_tuned_count(round(employee_turnover_result.score*100))
            employee_turnover_days_in_months = employee_turnover_days_in_months-emp_worked_days_in_months 

            if employee_turnover_days_in_months<=0:
                employee_turnover_days_in_months=1


            

            if employee_turnover_result.is_leaving:
                employee_prediction_record.month_to_leave = emp_worked_days_in_months
            else:
                employee_prediction_record.month_to_leave =0


            db.session.add(employee_prediction_record)
            db.session.commit()
        else:  
            employee_prediction_record.is_leaving=employee_turnover_result.is_leaving
            employee_prediction_record.turnover_rate =employee_turnover_result.score
            employee_prediction_record.updated_timestamp=datetime.datetime.now()

            # days calculation
            employee_survey_regression_data = EmployeeSurveyRegressionData(  age=age, 
                gender=gender, 
                marital_status=marital_status,
                educational_status=educational_status,
                total_years_industry=total_years_industry,
                years_work_current_hotel=years_work_current_hotel,
                number_of_years_current_role=number_of_years_current_role,
                department=emp_department,
                salary=salary,
                opportunities=opportunities, 
                workload=workload) 
            
            employee_turnover_days_in_months =predict_employee_turnover_days(employee_survey_regression_data)#days to leave

            # deducting predicted total months from worked months from joined date to get rest days
            emp_worked_days = date.today()-date(employee_record.joined_date.year,employee_record.joined_date.month,employee_record.joined_date.day) # worked days from date of joined
            # emp_worked_days_in_months = (emp_worked_days.days// 30) +1
            emp_worked_days_in_months=get_tuned_count(round(employee_turnover_result.score*100))
            print("kkk",employee_turnover_days_in_months,emp_worked_days_in_months)
            employee_turnover_days_in_months = employee_turnover_days_in_months-emp_worked_days_in_months 

            if employee_turnover_days_in_months<=0:
                employee_turnover_days_in_months=1


            if employee_turnover_result.is_leaving:
                #employee_prediction_record.month_to_leave = employee_turnover_days_in_months
                employee_prediction_record.month_to_leave = emp_worked_days_in_months
            else:
                employee_prediction_record.month_to_leave =0

            db.session.commit()

        
        # checking is there any exiting mappings to the prediction. if it is deleting them (if two records generated in same month only keeping the last record)
        prediction_factor_mappings = db.session.query(PredictionFactorMapping).filter(PredictionFactorMapping.fk_prediction_id==employee_prediction_record.id).all()
        for factor_mapping in prediction_factor_mappings:
            
            # deleting the exisiting records
            PredictionFactorMapping.query.filter(PredictionFactorMapping.id == factor_mapping.id).delete()
            db.session.commit()

        
        #factors commiting (mappings)
        for factor, score in employee_turnover_result.factors:
            system_factor_id = get_turnover_factor_by_name(factor).id

            prediction_factor_mapping = PredictionFactorMapping(fk_prediction_id= employee_prediction_record.id, fk_factor_id=system_factor_id, score=score,
                                                                created_timestamp= datetime.datetime.now(),updated_timestamp=datetime.datetime.now())
            # db commit (factor mappings)
            db.session.add(prediction_factor_mapping)
            db.session.commit()


        # updating employee table columns(is leaving,pred,days) by the latest records
        employee_record.is_leaving = employee_turnover_result.is_leaving
        employee_record.latest_turnover_rate=employee_turnover_result.score
        print("Buuuu1",employee_turnover_days_in_months)
        if employee_turnover_result.is_leaving:
                #employee_record.latest_months_to_leave = employee_turnover_days_in_months
                employee_record.latest_months_to_leave = emp_worked_days_in_months
        else:
            employee_record.latest_months_to_leave =0
        employee_record.updated_timestamp = datetime.datetime.now()
        
        db.session.add(employee_record)
        print("Buuuu",employee_record.latest_months_to_leave)
        db.session.commit()
        

        return jsonify(
            {'STATUS': "SUCCESS", 'MESSAGE': 'EMPLOYEE SURVEY DATA SUCCESSFULLY RECORDED',"DATA": ""}), HTTP_200_OK

    # except (ValueError, Exception):
    #     db.session.rollback()
    #     db.session.flush()
    #     logging.error('EmployeeServices - employee_survey() ERROR :' + str(Exception))
    
    #     return jsonify(
    #         {'STATUS': "ERROR", 'MESSAGE': 'EXCEPTION OCCURRED: ' + str(Exception),
    #          "DATA": None}), HTTP_500_INTERNAL_SERVER_ERROR


def get_turnover_factor_by_name(factor_name):
    logging.info('EmployeeServices - get_turnover_factor_by_name() CALLED')
    return TurnoverFactor.query.filter_by(factor=factor_name).first()


@employee.get('/view')
@jwt_required()
def get_employee_view():
    try:
        logging.info('EmployeeServices - get_employee_view() CALLED')

        # required fields validating (values exits or not)
        values = request.args
        if not "id" in values:
            response_dto =ResponseDto(status=ERROR,msg='REQUIRED FIELDS ARE MISSING',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)

        # required fields validating (values empty or not)
        if any(value == "" for value in values.values()):
            response_dto =ResponseDto(status=ERROR,msg='REQUIRED FIELDS ARE EMPTY',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)

        
        # capturing the body data
        id = values['id']

        # DB retrieving
        employee = Employee.query.filter_by(id=id).first()
        if employee is None:
            response_dto =ResponseDto(status=ERROR,msg='EMPLOYEE NOT FOUND',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_422_UNPROCESSABLE_ENTITY,mimetype=RESPONSE_RETURN_TYPE)

        else:
            # dpt name retrieving
            department_name = Department.query.filter_by(id=employee.fk_department_id).first().name

            employee_data = EmployeeDto(id=employee.id, emp_id=employee.emp_id, name=employee.name, 
                                    designation=employee.designation,department_code=employee.fk_department_id, 
                                    department_id=department_name, address=employee.address, contact=employee.contact, 
                                    supervisor=employee.supervisor, joined_date=employee.joined_date.strftime('%Y-%m-%d'), 
                                    performance_grade=employee.performance_grade, note=employee.note)
            # response initiating
            response_dto =ResponseDto(status=SUCCESS,
                msg="EMPLOYEE DETAILS RETRIEVED SUCCESSFULLY",
                data={"employee_details":employee_data}).toJSON()
            return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_view() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)
    

@employee.get('/view/analytics')
@jwt_required()
def get_employee_turnover_analytics():
    try:
        logging.info('EmployeeServices - get_employee_turnover_analytics() CALLED')

        # required fields validating (values exits or not)
        values = request.args
        if not "id" in values:
            response_dto =ResponseDto(status=ERROR,msg='REQUIRED FIELDS ARE MISSING',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)

        # required fields validating (values empty or not)
        if any(value == "" for value in values.values()):
            response_dto =ResponseDto(status=ERROR,msg='REQUIRED FIELDS ARE EMPTY',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)

        # capturing the body data
        id = values['id']

        # emp id status validating
        if Employee.query.filter_by(id=id).first() is None:
                response_dto =ResponseDto(status=ERROR,msg="EMPLOYEE ID NOT FOUND",data=None).toJSON()
                return Response(response=response_dto,status=HTTP_422_UNPROCESSABLE_ENTITY,mimetype=RESPONSE_RETURN_TYPE)

        # emp latest prediction retrieving
        emp_latest_prediction = db.session.query(Prediction).filter(Prediction.fk_emp_id == id).order_by(Prediction.updated_timestamp.desc()).first()
        if emp_latest_prediction is not None:
            prediction_factor_mappings = db.session.query(PredictionFactorMapping).filter(PredictionFactorMapping.fk_prediction_id == emp_latest_prediction.id).all()

            prediction_month = get_month_name(emp_latest_prediction.updated_timestamp)
            prediction_year =  get_year_from_the_date(emp_latest_prediction.updated_timestamp)

            turnover_factors_list = []
            turnover_measures_list = []
            for prediction_factor_mapping in prediction_factor_mappings:

                # factor retrieivig
                turnover_factor = db.session.query(TurnoverFactor).filter(TurnoverFactor.id == prediction_factor_mapping.fk_factor_id).first()
                turnover_factors_list.append(TurnoverDriverWithRateDto(name=turnover_factor.display_name, rate=str(round(float(prediction_factor_mapping.score)*100))+"%"))
                turnover_measures_list.append(turnover_factor.measure)
            
            employee_turnover_analytics_dto = EmployeeTurnoverAnalyticsDto(
                probability=str(round(float(emp_latest_prediction.turnover_rate)*100))+"%", 
                period=str(emp_latest_prediction.month_to_leave)+" month(s)",
                is_drivers_exists = True,
                drivers=turnover_factors_list, 
                measures=turnover_measures_list)
            
             # response initiating
            response_dto =ResponseDto(status=SUCCESS,msg="EMPLOYEE TURNOVER ANALYTICS RETRIEVED SUCCESSFULLY",
                    data={"period":"("+str(prediction_month)+' '+str(prediction_year)+")",
                          "tunover_details":employee_turnover_analytics_dto}).toJSON()
            return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)

        else:
            employee_turnover_analytics_dto = EmployeeTurnoverAnalyticsDto(
                probability="No Data", 
                period="No Data",
                is_drivers_exists = False,
                drivers="No Data to Show", 
                measures="No Data to Show")
            
            # response initiating
            response_dto =ResponseDto(status=SUCCESS,
                                      msg="EMPLOYEE TURNOVER ANALYTICS RETRIEVED SUCCESSFULLY",
                                      data={"period":"",
                                            "tunover_details":employee_turnover_analytics_dto}).toJSON()
            return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_turnover_analytics() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)
    


@employee.get('/view/evaluation')
@jwt_required()
def get_employee_turnover_evaluation():
    try:
        logging.info('EmployeeServices - get_employee_turnover_evaluation() CALLED')

        # required fields validating (values exits or not)
        values = request.args
        if not "id" in values:
            response_dto =ResponseDto(status=ERROR,msg='REQUIRED FIELDS ARE MISSING',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)

        # required fields validating (values empty or not)
        if any(value == "" for value in values.values()):
            response_dto =ResponseDto(status=ERROR,msg='REQUIRED FIELDS ARE EMPTY',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)

        # capturing the body data
        id = values['id']

        # emp id status validating
        if Employee.query.filter_by(id=id).first() is None:
                response_dto =ResponseDto(status=ERROR,msg="EMPLOYEE ID NOT FOUND",data=None).toJSON()
                return Response(response=response_dto,status=HTTP_422_UNPROCESSABLE_ENTITY,mimetype=RESPONSE_RETURN_TYPE)

        # emp latest prediction retrieving
        emp_latest_prediction = db.session.query(Prediction).filter(Prediction.fk_emp_id == id).order_by(Prediction.updated_timestamp.desc()).all()

        if emp_latest_prediction is not None and len(emp_latest_prediction)>0 :

            # checking is 2 predictions exists
            if(len(emp_latest_prediction)>=2):
                current_prob = round(float(emp_latest_prediction[0].turnover_rate)*100)
                previous_prob = round(float(emp_latest_prediction[1].turnover_rate)*100)

                prev_prediction_month = get_month_name(emp_latest_prediction[1].updated_timestamp)
                prev_prediction_year =  get_year_from_the_date(emp_latest_prediction[1].updated_timestamp)
                current_prediction_month = get_month_name(emp_latest_prediction[0].updated_timestamp)
                current_prediction_year =  get_year_from_the_date(emp_latest_prediction[0].updated_timestamp)
      
                is_prob_increase = None
                if current_prob>previous_prob:
                    is_prob_increase =True
                elif current_prob<previous_prob:
                    is_prob_increase=False
             
                prob_rate =current_prob-previous_prob
                current_period =emp_latest_prediction[0].month_to_leave
                prev_period = emp_latest_prediction[1].month_to_leave

                is_period_increase = None
                if current_period>prev_period:
                    is_period_increase =True
                elif current_period<prev_period:
                    is_period_increase=False

                period_rate = current_period-prev_period


                prev_pred_factors =  db.session.query(PredictionFactorMapping.fk_factor_id).filter(PredictionFactorMapping.fk_prediction_id==emp_latest_prediction[1].id).all()
                current_pred_factors =  db.session.query(PredictionFactorMapping.fk_factor_id).filter(PredictionFactorMapping.fk_prediction_id==emp_latest_prediction[0].id).all()
               

               # comapres prev month drivers and current driver by is increased, decreased or removes
                prev_factor_evaluation =[]
                for factor_id in prev_pred_factors:
                
                    if factor_id in current_pred_factors:
                        prev_pred_factor =  db.session.query(PredictionFactorMapping).filter(PredictionFactorMapping.fk_prediction_id==emp_latest_prediction[1].id).filter(PredictionFactorMapping.fk_factor_id==factor_id[0]).first()
                        current_pred_factor =  db.session.query(PredictionFactorMapping).filter(PredictionFactorMapping.fk_prediction_id==emp_latest_prediction[0].id).filter(PredictionFactorMapping.fk_factor_id==factor_id[0]).first()
                        
                        #prev_pred_factor_score =round(float(prev_pred_factor.score)*100)
                        #current_pred_factor_score = round(float(current_pred_factor.score))
                        prev_pred_factor_score =float(prev_pred_factor.score)*100
                        current_pred_factor_score = float(current_pred_factor.score)*100
                        rate_dif =  str(round(current_pred_factor_score-prev_pred_factor_score,2))+"%"
 

                        # object initialization
                        factor = db.session.query(TurnoverFactor).filter(TurnoverFactor.id == factor_id[0]).first()

                        is_rate_increased = None
                        if current_pred_factor_score>prev_pred_factor_score:
                            is_rate_increased =True
                        elif current_pred_factor_score<prev_pred_factor_score:
                            is_rate_increased=False

                        evaluation_dto = EvaluationDto(factor=factor.display_name+" ",rate=rate_dif,is_rate_increased=is_rate_increased)
                        prev_factor_evaluation.append(evaluation_dto)
                        
                    else:
                        factor = db.session.query(TurnoverFactor).filter(TurnoverFactor.id == factor_id[0]).first()
                        evaluation_dto = EvaluationDto(factor=factor.display_name,rate=None,is_rate_increased=None)
                        prev_factor_evaluation.append(evaluation_dto)


               
               
            #    # adding new factors with comparaing prev prediction
            #     new_factors_in_current_pred = []
            #     for factor_id in current_pred_factors:

            #         if factor_id not in prev_pred_factors:
                    
            #             factor = db.session.query(TurnoverFactor).filter(TurnoverFactor.id == factor_id[0]).first()
            #             if factor is not None:
            #                 new_factors_in_current_pred.append(factor.display_name)
                     
                employee_turnover_evaluation = EmployeeTurnoverEvaluationDto(current_prob=str(current_prob)+"%",
                                                                             previous_prob=str(previous_prob)+"%",
                                                                             is_prob_increase=is_prob_increase,
                                                                             prob_rate=str(prob_rate)+"%",
                                                                             current_period=str(current_period)+" month(s)",
                                                                             prev_period=str(prev_period)+" month(s)",
                                                                             is_period_increase=is_period_increase,
                                                                             period_rate=str(period_rate)+" M", 
                                                                             is_prev_factors_exists = True,
                                                                             prev_pred_factors=prev_factor_evaluation)
                # response initiating
                response_dto =ResponseDto(status=SUCCESS,msg="EMPLOYEE TURNOVER EVALATION RETRIEVED SUCCESSFULLY",
                        data={"prev_period":"("+str(prev_prediction_month)+' '+str(prev_prediction_year)+")",
                              "current_period":"("+str(current_prediction_month)+' '+str(current_prediction_year)+")",
                              "evaluation_details":employee_turnover_evaluation}).toJSON()
                return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)

        
            else:
                current_prob = round(float(emp_latest_prediction[0].turnover_rate)*100)
                previous_prob = "No Data"
                is_prob_increase = None
                prob_rate = ""
                current_period = emp_latest_prediction[0].month_to_leave
                prev_period = "No Data"
                is_period_increase = None 
                period_rate =""

                employee_turnover_evaluation = EmployeeTurnoverEvaluationDto(current_prob=str(current_prob)+"%",
                                                                             previous_prob=previous_prob,
                                                                             is_prob_increase=is_prob_increase,
                                                                             prob_rate=prob_rate,
                                                                             current_period=str(current_period)+" month(s)",
                                                                             prev_period=prev_period,
                                                                             is_period_increase=is_period_increase,
                                                                             period_rate=period_rate,
                                                                             is_prev_factors_exists = False ,
                                                                             prev_pred_factors="No Data to Show")
                
                # response initiating
                response_dto =ResponseDto(status=SUCCESS,msg="EMPLOYEE TURNOVER EVALATION RETRIEVED SUCCESSFULLY",
                        data={"prev_period":"",
                              "current_period":"",
                              "evaluation_details":employee_turnover_evaluation}).toJSON()
                return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)

        else:
            current_prob = "No Data"
            previous_prob = "No Data"
            is_prob_increase = None
            prob_rate = ""
            current_period = "No Data"
            prev_period = "No Data"
            is_period_increase = None 
            period_rate =""

            employee_turnover_evaluation = EmployeeTurnoverEvaluationDto(current_prob=current_prob,previous_prob=previous_prob,is_prob_increase=is_prob_increase,
                                                                            prob_rate=prob_rate,current_period=current_period,
                                                                            prev_period=prev_period,is_period_increase=is_period_increase,period_rate=period_rate,
                                                                            is_prev_factors_exists = False ,
                                                                            prev_pred_factors="No Data to Show")
            
            # response initiating
            response_dto =ResponseDto(status=SUCCESS,msg="EMPLOYEE TURNOVER EVALATION RETRIEVED SUCCESSFULLY",
                    data={"prev_period":"",
                            "current_period":"",
                            "evaluation_details":employee_turnover_evaluation}).toJSON()
            return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE) 
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('EmployeeServices - get_employee_turnover_evaluation() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)


    