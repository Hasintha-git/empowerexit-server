import logging
import re

from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.general_constants import ERROR, EXCEPTION_MSG, RESPONSE_RETURN_TYPE, SUCCESS
from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, \
    HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR
from src.dto.ResponseDto import ResponseDto
from flask import Response
from src.dto.UserDto import UserDto
from src.models.Database import db, User
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

auth = Blueprint("auth", __name__, url_prefix='/api/v1/auth')


@auth.post('/register')
def register():
    try:
        logging.info('auth - register() CALLED')

        first_name = request.json['first_name']
        # last_name = request.json['last_name']
        email = request.json['email']
        password = request.json['password']

        if not first_name.isalpha() :
            #return jsonify({'ERROR': "NAME SHOULD BE CONTAIN LETTERS"}), HTTP_400_BAD_REQUEST
        
            response_dto =ResponseDto(status=ERROR,msg='NAME SHOULD BE CONTAIN ONLY LETTERS',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)


        if User.query.filter_by(email=email).first() is not None:
            #return jsonify({'ERROR': 'ERROR  OCCURRED', 'MESSAGE': "EMAIL IS ALREADY IN USE"}), HTTP_409_CONFLICT
        
            response_dto =ResponseDto(status=ERROR,msg='EMAIL IS ALREADY IN USE',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_409_CONFLICT,mimetype=RESPONSE_RETURN_TYPE)
        
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not re.fullmatch(regex, email):
            #return jsonify({'ERROR': 'ERROR  OCCURRED', 'MESSAGE': "EMAIL IS NOT VALID"}), HTTP_400_BAD_REQUEST
        
            response_dto =ResponseDto(status=ERROR,msg='EMAIL IS NOT VALID',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)
        

        if len(password) < 6:
            #return jsonify({'ERROR': "PASSWORD IS TOO SHORT"}), HTTP_400_BAD_REQUEST
        
            response_dto =ResponseDto(status=ERROR,msg='PASSWORD IS TOO SHORT',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_400_BAD_REQUEST,mimetype=RESPONSE_RETURN_TYPE)

        

        pwd_hash = generate_password_hash(password)

        user = User(first_name=first_name, last_name="", email=email, password=pwd_hash)
        db.session.add(user)

        db.session.commit()

        user_data = UserDto(id=user.id,email=email,first_name=user.first_name,refresh_token="",access_token="")

        response_dto =ResponseDto(status=SUCCESS,msg='USER CREATED SUCCESSFULLY',data=user_data).toJSON()
        return Response(response=response_dto,status=HTTP_201_CREATED,mimetype=RESPONSE_RETURN_TYPE)

        # return jsonify({
        #     'message': 'USER CREATED SUCCESSFULLY',
        #     'user': {'id': user.id, 'email': email, 'first_name': user.first_name}}), HTTP_201_CREATED

    except Exception as exception:
        db.session.rollback()
        db.session.flush()
        logging.error('auth - login() ERROR :' + str(exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None).toJSON()
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)
    


@auth.post('/login')
def login():
    try:
        logging.info('auth - login() CALLED')

        email = request.json.get('email', '')
        password =  request.json.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                refresh = create_refresh_token(identity=user.id)
                access = create_access_token(identity=user.id)

                user_data = UserDto(id=user.id,email=email,first_name=user.first_name,refresh_token=refresh,access_token=access)

                response_dto =ResponseDto(status=SUCCESS,msg='USER LOGGING SUCCESSFUL',data=user_data).toJSON()
                return Response(response=response_dto,status=HTTP_200_OK,mimetype=RESPONSE_RETURN_TYPE)

                # return jsonify({'message': 'USER LOGGING SUCCESSFUL',
                #                 'user': {'id': user.id, 'email': email, 'first_name': user.first_name,
                #                          'refresh_token': refresh, 'access_token': access}}), HTTP_200_OK

        #return jsonify({'ERROR': 'ERROR  OCCURRED', 'MESSAGE': "WRONG CREDENTIALS"}), HTTP_401_UNAUTHORIZED
            else:
                response_dto =ResponseDto(status=ERROR,msg='PASSWORD IS INCORRECT',data=None).toJSON()
                return Response(response=response_dto,status=HTTP_401_UNAUTHORIZED,mimetype=RESPONSE_RETURN_TYPE)

        else:
            response_dto =ResponseDto(status=ERROR,msg='EMAIL IS NOT FOUND',data=None).toJSON()
            return Response(response=response_dto,status=HTTP_401_UNAUTHORIZED,mimetype=RESPONSE_RETURN_TYPE)

    except Exception as exception:
        db.session.rollback()
        db.session.flush()
        logging.error('auth - login() ERROR :' + str(exception))

        response_dto =ResponseDto(status=ERROR,msg=EXCEPTION_MSG + str(Exception),data=None).toJSON()
        return Response(response=response_dto,status=HTTP_500_INTERNAL_SERVER_ERROR,mimetype=RESPONSE_RETURN_TYPE)



@auth.get("/profile")
@jwt_required()
def get_user_profile():
    try:
        logging.info('auth - get_user_profile() CALLED')

        user_id = get_jwt_identity()
        user = User.query.filter_by(id=user_id).first()
        return jsonify({
            'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email
        }), HTTP_200_OK

    except Exception as exception:
        db.session.rollback()
        db.session.flush()
        logging.error('auth - login() ERROR :' + str(exception))

        return jsonify({
            'message': 'EXCEPTION  OCCURRED',
            'exception': str(exception)}),HTTP_500_INTERNAL_SERVER_ERROR


@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_users_token():
    try:
        logging.info('auth - refresh_users_token() CALLED')

        identity = get_jwt_identity()
        access = create_access_token(identity=identity)

        return jsonify({'access_token': access}), HTTP_200_OK

    except Exception as exception:
        db.session.rollback()
        db.session.flush()
        logging.error('auth - login() ERROR :' + str(exception))

        return jsonify({
            'message': 'EXCEPTION  OCCURRED',
            'exception': str(exception)}),HTTP_500_INTERNAL_SERVER_ERROR
