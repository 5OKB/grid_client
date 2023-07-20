class Token:
    __username: str
    __company_id: int
    __oauth_token: dict

    def __init__(self, username: str, company_id: int, oauth_token: dict):
        self.__username = username
        self.__company_id = company_id
        self.__oauth_token = oauth_token

    @property
    def username(self) -> str:
        return self.__username

    @property
    def company_id(self) -> int:
        return self.__company_id

    @property
    def access_token(self) -> str:
        return self.__oauth_token['access_token']
