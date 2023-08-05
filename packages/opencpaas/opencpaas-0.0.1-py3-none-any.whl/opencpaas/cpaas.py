from abc import ABC, abstractmethod

"""

Progressive CPaaS is a one-stop site to allow Bandwidth and Twilio clients to easily switch 
providers without having to rewrite code. 

"""

class CpaasClient(ABC):
    """
    The CpaasClient class encapsulates messaging and number management functions for
    Bandwidth and Twilio users.
    """
    def __init__(self, provider, auth):
        """
        Provides an interface for CpaasClients.

        :param str provider: 'bandwidth' or 'twilio'
        :param dict auth: A dictionary that contains the following keys determined by the type of client.
            Twilio: 
                {
                'account_sid': A username located in your Console dashboard. 
                'auth_token': A password located in your Console dashboard.
                }

            Bandwidth: 
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
        :raises Error: CpaasAuthenticationException
        """
        self.provider = provider
        self.auth = auth   

    @abstractmethod
    def send_sms(self, to, from_, text):
        """
        Provides a format for the send_sms method. This is implemented by 
        provider child class.

        :param str to: The phone number (E.164 format) that the message will be sent to.                
        :param str from: The phone number (E.164 format) the message will be sent from. This value will be 
            one of your provider phone numbers.
        :param str text: The message text.

        :returns:
            This returns a dictionary with the following keys,
                
                    'segment_count': The number of segments that will make up the complete message. A message that is too large to be sent in a single SMS will be segmented.

                    'text': The message text.

                    'to': The phone number (E.164 format) that received the message.

                    'date_time_sent': Date and time the message was sent. (RFC822 format)

                    'from': The phone number (E.164 format) that initiated the message. This value will be one of your provider phone numbers

                    'id': The ID associated with the account that created the message.

                        (Twilio: account_sid, Bandwidth: application_id)
                
        :rtype: dict
        :raises Error: CpaasRESTException, CpaasAuthenticationException
        """

    @abstractmethod
    def send_mms(self, to, from_, text, media_url):
        """
        Provides a format for the send_mms method. This is implemented by 
        provider child class.

        :param str to: The phone number (E.164 format) that the message will be sent to.                
        :param str from: The phone number (E.164 format) the message will be sent from. This value will be 
            one of your provider phone numbers.
        :param str text: The message text.
        :param str media_url: A URL to include as a media attachment as part of a message.

        :returns:
            This returns a dictionary with the following keys:
                
                    'segment_count': The number of segments that will make up the complete message. A message that is too large to be sent in a single SMS will be segmented.

                    'text': The message text.

                    'to': The phone number (E.164 format) that received the message.

                    'date_time_sent': Date and time the message was sent. (RFC822 format)

                    'from': The phone number (E.164 format) that initiated the message. This value will be one of your provider phone numbers

                    'id': The ID associated with the account that created the message.

                        (Twilio: account_sid, Bandwidth: application_id)

                    'media_url': The media URL of the image sent in the MMS message.
                
        :rtype: dict
        :raises Error: CpaasRESTException, CpaasAuthenticationException
        """

    @abstractmethod
    def get_available_numbers(self, area_code, quantity):
        """
        Provides a list of phone numbers beginning with the area code parameter that are available for purchase.
        Currently supports US numbers only.
        
        :param str area_code: NPA 3 digit area code.
        :param int quantity: The number of available phone numbers to be returned.
            
        :returns:
            This returns a dictionary with the following keys,

                'count': The number of numbers returned in the numbers_list.

                'numbers': A list of phone numbers.

        :rtype: dict
        :raises Error: CpaasRESTException, CpaasAuthenticationException
        """


    @abstractmethod
    def order_number(self, phone_number):
        """
        Orders a single phone number from the provider if it is available. Throws exception otherwise. 
        Currently supports US numbers only.

        :param str phone_number: The phone number (E.164 format) to be ordered. 
        :returns: 
            This returns a dictionary with the following keys,
            
                'order_status': 'COMPLETE' (HTTP Status Code 200) or 'RECEIVED' (HTTP Status Code 201)
            
        :rtype: dict
        :raises Error: CpaasRESTException, phonenumbers.phonenumberutil.NumberParseException, CpaasAuthenticationException
        """

    @abstractmethod
    def order_numbers(self, area_code, quantity):
        """
        Purchases phone numbers with specified area code from your provider if available. Throws exception otherwise.
        Currently supports US numbers only.

        :param str area_code: The area code of the phone numbers to be ordered.
        :param int quantity: The amount of available numbers to be purchased.

        :returns: 
            This returns a dictionary with the following keys,
            
                'order_status': 'COMPLETE' (HTTP Status Code 200) or 'RECEIVED' (HTTP Status Code 201)
            
        :rtype: dict
        :raises Error: CpaasRESTException, ValueError, CpaasAuthenticationException
        """

    @abstractmethod
    def get_phone_numbers(self, area_code, quanitity):
        """
        Returns a list of phone numbers that belong to the client. 

        :param str area_code: (optional) Filters the list of phone numbers by area_code.
        :param int quantity: (optional) Specify the max amount of phone_numbers to return.

        :returns list: A list of phone numbers.
        :rtype list:
        :raises Error: CpaasRESTException, CpaasAuthenticationException
        """

    @abstractmethod
    def release_number(self, phone_number):
        """
        Releases this phone number from your account. Throws an exception otherwise.

        :param str phone_number: The phone number (E.164 format) to be deleted.

        :returns:
            This returns a dictionary with the following keys:
        
                'order_status': 'COMPLETE' (HTTP Status Code 200)
            
        :rtype: dict 

        :raises Error: CpaasRESTException, phonenumbers.phonenumberutil.NumberParseException, CpaasAuthenticationException
        """  

    @abstractmethod
    def create_call(self, to, from_, **parameters):
        """
        Create an outgoing phone call. 

        :param str to: The phone number (E.164 format) that is receiving the phone call.      
        :param str from: The phone number (E.164 format) that is making the outgoing phone call.
        :param dict parameters: A dictionary that contains the client specific URLS associated with the call and also other optional 
            client specific parameters. Refer to client specific documentation for a list of optional parameters. 

            Twilio: 
                url: The absolute URL that returns TwiML for this call

                status_callback: The URL we should call to send status information to your application            

            Bandwidth: 
                answer_url (str): The full URL to send the Answer event to when the called party answers. This endpoint should return the first BXML document to be executed in the call.

        :returns: The ID associated with the phone call
        :rtype: str
        :raises Error: CpaasAuthenticationException
        """

    def update_auth(self, auth):
        """
        Updates the client's authorizations. If an auth key already exists it will be overwritten. If an auth key does not exist it will be added.

        :param dict auth: The new authorizations to be added to the client's existing authorizations.

        :returns: Nothing
        """
        self.auth.update(auth)
        
    def get_provider(self):
        """
        :returns: Returns a string containing the type of provider associated with the client.
        :rtype: str
        
        """
        return self.provider