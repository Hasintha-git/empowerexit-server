import json
from flask import Response as FlaskResponse


class ResponseDto:

    def __init__(self, status, msg, data):
        self.status = status
        self.msg = msg
        self.data = data

    def __repr__(self) -> dict[str, int]:
        return {"status": self.status, "msg": self.msg, "data": self.data}
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=1)
       
    
