import opencpaas
import twilio.rest
from twilio.base.exceptions import TwilioRestException
from opencpaas import CpaasRESTException, CpaasAuthenticationException


class TwilioClient(opencpaas.CpaasClient):
    """
    The TwilioClient class provides implementations of Twilio specific messaging and number
    management services.
    """
    def __init__(self, auth):
        """
        Initializes a new Twilio Client.

        :param dict auth: 
            {
                'account_sid': A username located in your Console dashboard. 
                'auth_token': A password located in your Console dashboard.
            }
        """
        super().__init__('twilio', auth)

        if 'account_sid' not in auth or 'auth_token' not in auth:
            raise CpaasAuthenticationException('Twilio client must include an account sid and an auth token.')

        self.client = twilio.rest.Client(auth['account_sid'], auth['auth_token'])

 
    def send_sms(self, to, from_, text):
        try:
            message = self.client.messages.create(
                body = text,  
                to= to,
                from_= from_              
            )       
        except TwilioRestException as err:
            raise CpaasRESTException(err.status,
                                        err.msg,
                                        err.uri,
                                        err.method
                                    ) 

        return {
            'segment_count': message.num_segments,
            'text': text,
            'date_time_sent': message.date_created,
            'to': to,
            'from': from_,
            'id': message.account_sid
        }

    def send_mms(self, to, from_, text, media_url):
        try:
            message = self.client.messages.create(
                body = text,  
                to= to,
                media_url = media_url,
                from_= from_              
            )  
        except TwilioRestException as err:
            raise CpaasRESTException(err.status,
                                        err.msg,
                                        err.uri,
                                        err.method
                                    )

        return {
            'segment_count': message.num_segments,
            'text': text,
            'date_time_sent': message.date_created,
            'to': to,
            'from': from_,
            'id': message.account_sid,
            'media_url': media_url
        } 

    def get_available_numbers(self, area_code, quantity):
        try:
            numbers = self.client.available_phone_numbers("US") \
                    .local \
                    .list(area_code=area_code, limit=quantity)
        except TwilioRestException as err:
            raise CpaasRESTException(err.status,
                                        err.msg,
                                        err.uri,
                                        err.method
                                    )

        return {
            'count': len(numbers),
            'numbers': list(map(lambda num: num.phone_number, numbers))
        }
       
    def order_number(self, phone_number):
        try:
            self.client.incoming_phone_numbers.create(phone_number=phone_number)
        except TwilioRestException as err:
            raise CpaasRESTException(err.status,
                                        err.msg,
                                        err.uri,
                                        err.method
                                    )

        return {
            'order_status': 'COMPLETE'
        }
       
    def order_numbers(self, area_code, quantity):
        numbers = self.get_available_numbers(area_code, quantity)['numbers']

        if len(numbers) == 0:
            raise ValueError('No phone numbers in this area code are available for purchase.')
        elif quantity > len(numbers):
            raise ValueError("Quantity is greater than the number of available phone numbers.") 

        for i in range(0,quantity): 
            self.client.incoming_phone_numbers \
                .create(phone_number=numbers[i])    
                
        return {
            'order_status': 'COMPLETE'
        }    
    
    def get_phone_numbers(self, area_code=None, limit=None):
        try:
            numbers = list(map(lambda num: num.phone_number, self.client.incoming_phone_numbers.list(phone_number=area_code,
                                                                                                    limit=limit)))
        except TwilioRestException as err:
            raise CpaasRESTException(err.status,
                                        err.msg,
                                        err.uri,
                                        err.method
                                    )

        return numbers
        
    def __get_number_id(self, phone_number): 
        numbers = self.client.incoming_phone_numbers.list(phone_number=phone_number, limit=1)

        if not numbers:            
            raise ValueError('Cannot release a phone number that does not belong to the Twilio client.')
        
        return numbers[0].account_sid

    def release_number(self, phone_number):
        try:
            self.client.incoming_phone_numbers(self.__get_number_id(phone_number)).delete()
        except TwilioRestException as err:
            raise CpaasRESTException(err.status,
                                        err.msg,
                                        err.uri,
                                        err.method
                                    )
            
        return {
            'order_status': 'COMPLETE'
        }

    def create_call(self, to, from_, **parameters):
        call = self.client.calls.create(to=to,
                                        from_=from_,
                                        **parameters)

        return call.sid
