import opencpaas
from . import bandwidth_response_handler
from . import bandwidth_xml_request
from dateutil.parser import parse
import requests
import xmltodict
import phonenumbers

class BandwidthClient(opencpaas.CpaasClient):
    """   
    The BandwidthClient class provides implementations of Bandwidth specific messaging and number
    management services.
    """
    def __init__(self, auth):  
        """
        Initializes a new Bandwidth client. 

        :param dict auth: A dictionary that must include the following keys: 
            {
                'api_token': Your unique api token. The api_token is used as the username to authenticate to the API as part of the basic auth scheme.
                'api_secret': Your unique api secret. The api_secret is used as the password to authenticate to the API as part of the basic auth scheme.
                'account_id': Your unique account id. The account_id is used as part of the url to make API requests. 
                'application_id': The id associated with your Bandwidth HTTP Application. 
                'user': Your username to log into the Bandwidth Dashboard.
                'pass': Your password to log in to the Bandwidth Dashboard.
                'site_id': Your site_id or subAccountID is an id associated with a sub-account. The site_id is used as part of the url to make some 
                    API requests.
            }
        """

        super().__init__('bandwidth', auth)

        if 'account_id' not in auth:
            raise opencpaas.CpaasAuthenticationException('Bandwidth Client must include an account id.')  

        self.capabilities = {}
        self.__update_capabilities()   

    def __parse_phone_number(self, phone_number):
        """
        Removes the country code.
        :param str phone_number: The phone number (E.164 format)

        :returns: A modified US phone number that does not inlcude the country code (+1)
        :rtype: str
        :raises: phonenumbers.phonenumberutil.NumberParseException
        """

        valid_phone_number = phonenumbers.parse(phone_number)
        
        return valid_phone_number.national_number
    
    def __update_capabilities(self):
        """
        Makes sure that the required credentials are included in auth in order to utilize certain functionalities.
        Ex/ in order to send an sms, a Bandwidth client must include an api_token, api_secret, and application_id.

        :returns: Nothing
        """

        self.capabilities['messaging'] = (False, True)['api_token' in self.auth and\
                                                            'api_secret' in self.auth and\
                                                                'application_id' in self.auth]  

        self.capabilities['voice'] = (False, True)['user' in self.auth and \
                                                        'pass' in self.auth and\
                                                            'application_id' in self.auth]
                                                    
        self.capabilities['order'] = (False, True)['site_id' in self.auth and\
                                                        'user' in self.auth and\
                                                            'pass' in self.auth]

        self.capabilities['numbers'] = (False, True)['user' in self.auth and\
                                                        'pass' in self.auth]
        

    def send_sms(self, to, from_, text):
        if not self.capabilities['messaging']:
            raise opencpaas.CpaasAuthenticationException('Sending an SMS requires a Bandwidth Client to include the following authorizations: api_token, api_secret, and application_id')

        response = requests.post("https://messaging.bandwidth.com/api/v2/users/{account_id}/messages".format(**self.auth),
                    auth=(self.auth['api_token'],self.auth['api_secret']),
                    json={
                        "from": from_,
                        "to": to,
                        "text": text,
                        "applicationId": self.auth['application_id']
                    }
                    )

        bandwidth_response_handler.check_response_msg(response)

        return {
            'segment_count': "{}".format(response.json()['segmentCount']),
            'text': text,
            'date_time_sent': parse(response.json()['time']),
            'from': from_,
            'id': response.json()['id']
        }    
        
    def send_mms(self, to, from_, text, media_url):
        if not self.capabilities['messaging']:
            raise opencpaas.CpaasAuthenticationException('Sending an MMS requires a Bandwidth Client to include the following authorizations: api_token, api_secret, and application_id')

        response = requests.post("https://messaging.bandwidth.com/api/v2/users/{account_id}/messages".format(**self.auth),
                    auth=(self.auth['api_token'], self.auth['api_secret']),
                    json={
                        "from": from_,
                        "to": to,
                        "text": text,
                        "applicationId": self.auth['application_id'],
                        "media" : media_url
                    }
                    )

        bandwidth_response_handler.check_response_msg(response)

        return {
            'segment_count': "{}".format(response.json()['segmentCount']),
            'text': text,
            'date_time_sent': parse(response.json()['time']),
            'from': from_,
            'id': response.json()['id'],
            'media_url': media_url
        }       

    def get_available_numbers(self, area_code, quantity):
        if not self.capabilities['numbers']:
            raise opencpaas.CpaasAuthenticationException('Searching for available numbers requires a Bandwidth Client to include the following authorizations: \
                account_id, user, pass')

        url = "https://dashboard.bandwidth.com/api/accounts/{account_id}/availableNumbers?areaCode={area_code}&quantity={quantity}"\
                .format(account_id=self.auth['account_id'],
                    area_code=area_code,
                    quantity=quantity
                    )

        response = requests.get(url,
                    auth=(self.auth['user'], self.auth['pass'])
                    )

        if response.status_code == 204:
            return {
                'count': 0,
                'numbers': []
            }

        bandwidth_response_handler.check_response_get_available(response)

        values = xmltodict.parse(response.content)
        numbers = values['SearchResult']['TelephoneNumberList']['TelephoneNumber']
        
        return {
            'count': len(numbers),
            #Adds US country code to phone numbers
            'numbers': list(map(lambda num: "+1" + num, numbers))
        }

    def order_number(self, phone_number):
        if not self.capabilities['order']:
            raise opencpaas.CpaasAuthenticationException('Ordering a phone number requires a Bandwidth Client to include the following authorizations: \
                account_id, site_id, user, pass')

        #Removes the country code of the phone_number parameter
        valid_phone_number = self.__parse_phone_number(phone_number)

        headers = {'Content-Type': 'application/xml'}
        url = "https://dashboard.bandwidth.com/api/accounts/{account_id}/orders"\
            .format(**self.auth)
        xml = bandwidth_xml_request.BANDWIDTH_ORDER_NUMBER.format(phone_number=valid_phone_number,
                                                                    site_id=self.auth['site_id']
                                                                    )
        response = requests.post(url,
                    auth=(self.auth['user'], self.auth['pass']),
                    data=xml,
                    headers=headers
                    )

        bandwidth_response_handler.check_response_order(response)

        values = xmltodict.parse(response.content)

        return {
            'order_status': values['OrderResponse']['OrderStatus']
        }
       
    def order_numbers(self, area_code, quantity):
        if not self.capabilities['order']:
            raise opencpaas.CpaasAuthenticationException('Ordering phone numbers requires a Bandwidth Client to include the following authorizations: \
                account_id, site_id, user, pass')
        headers = {'Content-Type': 'application/xml'}
        url = "https://dashboard.bandwidth.com/api/accounts/{account_id}/orders"\
            .format(**self.auth)
        xml = bandwidth_xml_request.BANDWIDTH_ORDER_NUMBERS.format(area_code=area_code,
                                                                    quantity=quantity,
                                                                    site_id=self.auth['site_id']
                                                                    )

        response = requests.post(url,
                    auth=(self.auth['user'], self.auth['pass']),
                    data=xml,
                    headers=headers
                    )

        bandwidth_response_handler.check_response_order(response)

        values = xmltodict.parse(response.content)

        return {
            'order_status': values['OrderResponse']['OrderStatus']
        }

    def get_phone_numbers(self, area_code=None, limit=None):
        if not self.capabilities['numbers']:
            raise opencpaas.CpaasAuthenticationException('Retrieving owned phone numbers requires a Bandwidth Client to include the following authorizations: \
                account_id, user, pass')

        url = "https://dashboard.bandwidth.com/api/accounts/{account_id}/inserviceNumbers"\
            .format(**self.auth)
        headers = {'content-type': 'application/xml'}

        #query params
        if area_code is not None and limit is not None:
            url += "/?areacode={}&size={}".format(area_code, limit)
        elif area_code is not None:
            url += "/?areacode={}".format(area_code)
        elif limit is not None:
            url += "/?size={}".format(limit)      

        response = requests.get(url, 
                    auth=(self.auth['user'], self.auth['pass']),
                    headers=headers
                    )

        bandwidth_response_handler.check_response_get_numbers(response)

        if response.status_code == 204:
            return []

        values = xmltodict.parse(response.content)

        numbers = values['TNs']['TelephoneNumbers']['TelephoneNumber']
        count = values['TNs']['TelephoneNumbers']['Count']

        if count == "1":
            return ["+1" + numbers]

        #Adds US country code to phone numbers
        return list(map(lambda num: "+1" + num, numbers))

    def release_number(self, phone_number):
        if not self.capabilities['numbers']:
            raise opencpaas.CpaasAuthenticationException('Releasing a phone number requires a Bandwidth Client to include the following authorizations: \
                site_id, user, pass')
            
        #Removes the country code of the phone_number parameter
        valid_phone_number = self.__parse_phone_number(phone_number)

        headers = {'Content-Type': 'application/xml'}
        url = "https://dashboard.bandwidth.com/api/accounts/{account_id}/disconnects"\
            .format(**self.auth)
        xml = bandwidth_xml_request.BANDWIDTH_RELEASE_NUMBER.format(phone_number=valid_phone_number)

        response = requests.post(url, 
                    auth=(self.auth['user'], self.auth['pass']),
                    data=xml,
                    headers=headers
                    )

        bandwidth_response_handler.check_response_default(response)

        values = xmltodict.parse(response.content)
        order_id = values['DisconnectTelephoneNumberOrderResponse']['orderRequest']['id']

        url = "https://dashboard.bandwidth.com/api/accounts/{account_id}/disconnects/{order_id}"\
                .format(account_id=self.auth['account_id'],
                        order_id=order_id
                        )   

        response = requests.get(url, 
                    auth=(self.auth['user'], self.auth['pass']),
                    headers=headers
                    )    

        bandwidth_response_handler.check_response_default(response)

        values = xmltodict.parse(response.content)
        order_status = values['DisconnectTelephoneNumberOrderResponse']['OrderStatus']

        if order_status == 'FAILED':
            raise ValueError('Releasing phone number has failed. You may have entered an incorrect phone number.')

        return {
            'order_status': order_status
        }

    def create_call(self, to, from_, **parameters):

        def to_camel_case(snake_str):
            components = snake_str.split('_')
            return components[0] + ''.join(x.title() for x in components[1:])

        if not self.capabilities['voice']:
            raise opencpaas.CpaasAuthenticationException("Creating a call requires a Bandwidth Client to include the following authorizations: user, pass, and application_id.")        

        post_url = "https://voice.bandwidth.com/v2/accounts/{account_id}/calls/".format(**self.auth)

        json = {
            'applicationId': self.auth['application_id'],
            'from':from_,
            'to':to
            }

        #converts dict keys to camel case
        for key, value in parameters.items():
            json[to_camel_case(key)] = value

        response = requests.post(post_url, 
                    auth=(self.auth['user'], self.auth['pass']),
                    json=json
                    )

        bandwidth_response_handler.check_response_voice(response)

        return response.json()['callId']

    def update_auth(self, auth):
        #adds and updates auth dict
        self.auth.update(auth)

        #resets capabilities based on updated auth
        self.__update_capabilities()


