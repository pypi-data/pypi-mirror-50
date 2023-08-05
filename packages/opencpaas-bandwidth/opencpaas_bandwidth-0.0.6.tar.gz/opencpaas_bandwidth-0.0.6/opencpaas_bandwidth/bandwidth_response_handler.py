import requests
from urllib.parse import urlparse
import xmltodict
from opencpaas.exceptions import CpaasRESTException

def check_response(response_function):
        """
        Generic check_response function decorator. If a response error is not a Bandwidth detected client error,
                a default CpaasRESTException is thrown.

        :param function response_function: The check_response method associated with the type of request a 
                Bandwidth client makes.
        :returns: None
        :raises: CpaasRESTException
        """
        def wrapper(response):
                response_function(response)
                if not response.ok:
                        raise CpaasRESTException(response.status_code, response.reason, urlparse(response.url).path ,response.request.method)
        return wrapper

@check_response
def check_response_default(response):
        """
        This method is called when there are no Bandwidth defined response errors for a Bandwidth Client action.
        Wrapped by check_response decorator.
        """
        pass

@check_response
def check_response_msg(response):
    """
    Throws an exception if response includes a 400, 401, 403, 415, or 429 HTTP status code in 
    Bandwidth's send_sms() or send_mms() method.

    :param requests.models.Response response: response object from Python's requests library.
    :returns: nothing
    :raises Error: CpaasRESTException
    """

    def msg_parser(response):
        json = response.json()
        if response.status_code == 401:
            return "{} ERROR {}".format(json['error'].upper(), json['message'])

        error_type=json['type'].upper()
        error_description=json['description']

        message = "{} ERROR. {}".format(error_type, error_description)

        if response.status_code == 400:
            description_list = json['fieldErrors']
            
            for item in description_list:
                message = message + "\n" + item['description']

        return message

    if response.status_code in [400, 401, 403, 415, 429]:
        raise CpaasRESTException(status=response.status_code,
                                message= msg_parser(response),
                                uri= urlparse(response.url).path,
                                method=response.request.method,
                                )

@check_response
def check_response_get_numbers(response):
    """
    Throws an exception if response includes a 204 or 400 HTTP status code in 
    Bandwidth's get_phone_numbers() method.

    :param requests.models.Response response: response object from Python's requests library.
    :returns: nothing
    :raises Error: CpaasRESTException
    """
 
    if response.status_code == 404:
        raise CpaasRESTException(response.status_code, "Not Found - The search parameters are invalid and prevent finding any content.",
                                urlparse(response.url).path, response.request.method)

@check_response
def check_response_order(response):
    """
    Throws an exception if response includes a 400 HTTP status code in 
    Bandwidth's order_phone_number() or order_phone_numbers method.

    :param requests.models.Response response: response object from Python's requests library.
    :returns: nothing
    :raises Error: CpaasRESTException
    """
    if response.status_code == 400:
        xml = xmltodict.parse(response.content)
        message = "Error Code: {error_code}\n{description}"\
            .format(error_code=xml['OrderResponse']['ErrorList']['Error']['Code'],
                    description=xml['OrderResponse']['ErrorList']['Error']['Description']
                    )

        raise CpaasRESTException(status=response.status_code,
                                message=message,
                                uri= urlparse(response.url).path,
                                method=response.request.method,
                                )

@check_response
def check_response_get_available(response):
    """
    Throws an exception if response includes a 400 HTTP status code in 
    Bandwidth's get_available_numbers() method.

    :param requests.models.Response response: response object from Python's requests library.
    :returns: nothing
    :raises Error: CpaasRESTException
    """
    if response.status_code == 400:
        xml = xmltodict.parse(response.content)
        message = "Error Code: {error_code}\n{description}"\
            .format(error_code=xml['SearchResult']['Error']['Code'],
                    description=xml['SearchResult']['Error']['Description']
                    )

        raise CpaasRESTException(status=response.status_code,
                                message=message,
                                uri= urlparse(response.url).path,
                                method=response.request.method,
                                )


@check_response
def check_response_voice(response):
        """
        Throws an exception if response includes one of the following HTTP status codes: 400, 401, 403, 404, 409, 415, 500, 503

        :param requests.models.Response response: response object from Python's requests library.
        :returns: nothing
        :raises Error: CpaasRESTException
        """

        json = response.json()

        if response.status_code == 404 and 'timestamp' in json.keys():
                msg = "{type} ERROR {message} \n\n Timestamp: {timestamp} \n\n Path {path} does not exist.".format(type=json['error'].upper(), 
                                        message=json['message'],
                                        timestamp=json['timestamp'],
                                        path=json['path']
                                        )

                raise CpaasRESTException(status=response.status_code,
                                        message= msg,
                                        uri= urlparse(response.url).path,
                                        method=response.request.method,
                                        )

        elif response.status_code in [400, 401, 403, 404, 409, 415, 500, 503]:
                msg = "{} ERROR {}".format(json['type'].upper(), json['description'])

                raise CpaasRESTException(status=response.status_code,
                                        message= msg,
                                        uri= urlparse(response.url).path,
                                        method=response.request.method,
                                        )
