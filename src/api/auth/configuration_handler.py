from decouple import config


class ConfigurationHandler:
    """
    ConfigurationHandler is a class responsible for handling configuration settings for an application.
    
    Attributes:
    -----------
    `secret` : str
        The secret key used for encryption or authentication. This secret signs the token, making it
        recognized on decoding only if the signature is present.
    `algorithm` : str
        The algorithm used in conjunction with the secret key for cryptographic operations.
    
    Methods:
    --------
    __init__():
        Initializes the ConfigurationHandler with values from the configuration.
    """
    def __init__(self):
        """
        Initializes the ConfigurationHandler instance.
        
        The constructor retrieves the values for the secret and algorithm from the
        application's .env file using the `config` function from decouple. These values are
        assigned to the respective instance attributes.
        
        Raises:
        -------
        KeyError:
            If the .env does not contain the necessary keys ('SECRET', 'ALGORITHM').
        """
        self.secret = config("SECRET")
        self.algorithm = config("ALGORITHM")
