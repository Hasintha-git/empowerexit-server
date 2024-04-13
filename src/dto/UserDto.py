class UserDto:
    def __init__(self,id,email,first_name,refresh_token,access_token):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.refresh_token = refresh_token
        self.access_token = access_token


    def __repr__(self) -> dict[str, int]:
        return { "id": self.id,'email':self.email,"first_name": self.first_name,'refresh_token':self.refresh_token,"access_token": self.access_token}
