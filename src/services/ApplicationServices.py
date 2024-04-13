import logging
from flask import Response

from flask import Blueprint
from src.constants.general_constants import SUCCESS,ERROR,RESPONSE_RETURN_TYPE,EXCEPTION_MSG
from src.constants.http_status_codes import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
from src.dto.AnalyticsStatisticsDto import AnalyticsStatisticsDto
from src.models.Database import db,Department
from flask_jwt_extended import jwt_required

from ..dto.ResponseDto import ResponseDto

application = Blueprint("application", __name__, url_prefix='/api/v1/application')


@application.get('/departments')
@jwt_required()
def get_departments():
    try:
        logging.info('ApplicationServices - get_departments() CALLED')

        departments = Department.query.all()

        departments_list =[]
        for department in departments:
            departments_list.append(AnalyticsStatisticsDto(id=department.id,name=department.name,value=department.id))

        # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                    msg="DEPARTMENTS RETRIEVED SUCCESSFULLY",
                    data={"department_details":departments_list}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)
    
    except (ValueError, Exception):
        db.session.rollback()
        db.session.flush()
        logging.error('ApplicationServices - get_departments() ERROR :' + str(Exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)



@application.get('/performance_categories')
@jwt_required()
def get_performance_categories():
    try:
        logging.info('ApplicationServices - get_performance_categories() CALLED')

        performance_list = []
        performance_list.append(AnalyticsStatisticsDto(id=1, name="Grade A",value="A"))
        performance_list.append(AnalyticsStatisticsDto(id=2,name="Grade B",value="B"))
        performance_list.append(AnalyticsStatisticsDto(id=3,name="Grade C",value="C"))
        performance_list.append(AnalyticsStatisticsDto(id=4,name="Grade D",value="D"))

        # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                    msg="PERFORMANCE CATEGORIES RETRIEVED SUCCESSFULLY",
                    data={"performance_categories":performance_list}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)

    except (ValueError, Exception):
            db.session.rollback()
            db.session.flush()
            logging.error('ApplicationServices - get_performance_categories() ERROR :' + str(Exception))

            response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
            return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)
    

@application.get('/retention_pereiods')
@jwt_required()
def get_retention_pereiods():
    try:
        logging.info('ApplicationServices - get_retention_pereiods() CALLED')

        retention_pereiods_list = []
        retention_pereiods_list.append(AnalyticsStatisticsDto(id=1,name="1-3 Months",value="1"))
        retention_pereiods_list.append(AnalyticsStatisticsDto(id=2,name="3-6 Months",value="2"))
        retention_pereiods_list.append(AnalyticsStatisticsDto(id=3,name="6-12 Months",value="3"))
        retention_pereiods_list.append(AnalyticsStatisticsDto(id=4,name="More than 12 Months",value="4"))


        # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                    msg="RETENTION PERIODS RETRIEVED SUCCESSFULLY",
                    data={"retebtion_pereiods":retention_pereiods_list}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)

    except (ValueError, Exception):
            db.session.rollback()
            db.session.flush()
            logging.error('ApplicationServices - get_retention_pereiods() ERROR :' + str(Exception))

            response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
            return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)


@application.get('/turnover_rates')
@jwt_required()
def get_turnover_rates():
    try:
        logging.info('ApplicationServices - get_turnover_rates() CALLED')

        performance_list = []
        performance_list.append(AnalyticsStatisticsDto(id=1,name="0% - 25%",value=1))
        performance_list.append(AnalyticsStatisticsDto(id=2,name="25% - 50%",value=2))
        performance_list.append(AnalyticsStatisticsDto(id=3,name="50% - 75%",value=3))
        performance_list.append(AnalyticsStatisticsDto(id=4,name="75% - 100%",value=4))

        # response initiating
        response_dto =ResponseDto(status=SUCCESS,
                    msg="TURNOVER RATES RETRIEVED SUCCESSFULLY",
                    data={"performance_categories":performance_list}).toJSON()
        return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)

    except (ValueError, Exception):
            db.session.rollback()
            db.session.flush()
            logging.error('ApplicationServices - get_turnover_rates() ERROR :' + str(Exception))

            response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None)
            return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)
