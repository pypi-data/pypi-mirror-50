class CpaasException(Exception):
    pass
    
class CpaasRESTException(CpaasException):
    """
    Cpaas Exceptions for 4XX/5XX response codes.

    :param int status: The HTTP Response Status Code.
    :param str message: A description of why the error occurred.  
    :param str uri: The URI that caused the exception.
    :param str method: HTTP method used to make the request.
    """
    
    def __init__(self, status, message, uri, method):        
        self.status = status
        self.message = message
        self.uri = uri
        self.method = method

    def __str__(self):
        message =(
            "\n\nHTTP ERROR Your request was:\n\n{method} {uri}\n\n" 
            "Error Code: {status}\n\n"
            "{message}".format(
                            method=self.method,
                            uri=self.uri,
                            status=self.status,
                            message=self.message
                            )
        )

        return message

class CpaasAuthenticationException(CpaasException):
    pass
