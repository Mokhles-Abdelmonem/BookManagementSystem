import logging
from functools import wraps
from flask import request
from pydantic import ValidationError, BaseModel


def validate(request_model=None, response_model=None, is_list: bool = False):
    if request_model and not issubclass(request_model, BaseModel):
        raise TypeError(f"request_model '{request_model.__name__}' is not a subclass of Pydantic's BaseModel")
    if response_model and not issubclass(response_model, BaseModel):
        raise TypeError(f"response_model '{response_model.__name__}' is not a subclass of Pydantic's BaseModel")

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if request_model:
                    try:
                        # Validate the incoming request data
                        request_data = request.get_json()
                        validated_request = request_model(**request_data)
                        kwargs['request_model'] = validated_request
                    except ValidationError as e:
                        return {"error": e.errors(include_url=False, include_input=False)}, 400

                # Pass the validated data to the endpoint function
                response = f(*args, **kwargs)
                # If the response data is a dictionary, convert it to a pydantic model
                if response_model:
                    status = 0
                    try:
                        if isinstance(response, dict):
                            response_model_data = response
                        # If the response data is a tuple, check to see if it contains a dictionary and states 200, 201
                        elif (isinstance(response, tuple) and len(response) == 2 and
                              isinstance(response[1], int) and response[1] in [200, 201]):
                            response_model_data = response[0]
                            status = response[1]
                        # If the response data is a list, convert it to a list of pydantic models
                        elif isinstance(response, list) and is_list:
                            response_model_data = list()
                            for item in response:
                                if isinstance(item, dict):
                                    data = item
                                elif hasattr(item, "to_dict"):
                                    data = item.to_dict()
                                elif hasattr(item, "__dict__"):
                                    data = item.__dict__
                                else:
                                    continue

                                obj = response_model(**data)
                                response_model_data.append(obj.model_dump(mode='json'))

                            return response_model_data
                        else:
                            return response

                        # Validate the response data
                        validated_response = response_model(**response_model_data)
                        data = validated_response.model_dump(mode='json')
                        if status:
                            return data, status
                        return data
                    except ValidationError as e:
                        return {"error": e.errors(include_url=False, include_input=False)}, 501
                return response
            except Exception as e:
                logging.exception(e)
                return {"error": str(e)}, 403
        return decorated_function
    return decorator
