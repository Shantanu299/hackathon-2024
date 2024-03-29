from abc import abstractmethod


class BaseJob:
    def __init__(self, *args, **kwargs):
        self.ie_prediction_api = 'https://api.insights.cropwise.com/v2.0/predictions'
        self.data = None
        self.context = kwargs.get('context')
        self.seed = kwargs.get('seed')
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImNyb3B3aXNlLWJhc2UtdG9rZW4tcHViLWtleSJ9.eyJzdWIiOiJmZjVjZTA1Zi1hMmQ1LTQ4OTUtOGU0Mi0zNWVjZTI4N2JmNDkiLCJpc191c2luZ19yYmFjIjp0cnVlLCJhdWQiOlsic3RyaWRlci1iYXNlIl0sInVzZXJfbmFtZSI6InByb3RlY3RvciIsInNjb3BlIjpbInJlYWQiLCJ3cml0ZSJdLCJpc3MiOiJjcm9wd2lzZS1iYXNlLXN0cml4IiwiZXhwIjoxNzExMjM3MjgzLCJhdXRob3JpdGllcyI6WyJBU1NJR05FRVNfV1JJVEUiLCJQVVJDSEFTRV9PUkRFUlNfUkVBRCIsIkFTU0lHTkVFU19SRUFEIiwiQlVER0VUU19XUklURSIsIkZBUk1TSE9UU19SRUFEIiwiVEVNUExBVEVTX1dSSVRFIiwiUFJPUEVSVElFU19XUklURSIsIkZJRUxEU19XUklURSIsIlNVUFBPUlQiLCJFUVVJUE1FTlRTX1JFQUQiLCJJTlZFTlRPUllfV1JJVEUiLCJTVVBQTElFU19XUklURSIsIlZFTkRPUlNfUkVBRCIsIkZJTkFOQ0lBTF9SRUFEIiwiUFJPUEVSVElFU19SRUFEIiwiUkVWRU5VRVNfUkVBRCIsIklORk9STUFUSU9OX1dSSVRFIiwiUFJPRFVDVFNfV1JJVEUiLCJTRUFTT05TX1JFQUQiLCJTRUFTT05fQVJFQV9XUklURSIsIlBVUkNIQVNFX09SREVSU19XUklURSIsIkVRVUlQTUVOVFNfV1JJVEUiLCJURU1QTEFURVNfUkVBRCIsIlJFUE9SVFNfV1JJVEUiLCJUQVNLU19XUklURSIsIldBUkVIT1VTRVNfUkVBRCIsIkFQUFNfV1JJVEUiLCJFWFBFTlNFU19SRUFEIiwiU1VQRVJfVVNFUiIsIkZJRUxEU19SRUFEIiwiQVBQU19SRUFEIiwiU1VQUExJRVNfUkVBRCIsIldBUkVIT1VTRVNfV1JJVEUiLCJJTlZFTlRPUllfUkVBRCIsIk9SR19SRUFEIiwiUFJPRFVDVFNfUkVBRCIsIlRBU0tTX1JFQUQiLCJFWFBFTlNFU19XUklURSIsIlNFQVNPTl9BUkVBX1JFQUQiLCJSRVBPUlRTX1JFQUQiLCJSRVZFTlVFU19XUklURSIsIkJVREdFVFNfUkVBRCJdLCJqdGkiOiJhZGRmYWRkOS1iN2NhLTQzZWEtYTQ5Ni1hYmM4ZGM1MTE1Y2EiLCJjbGllbnRfaWQiOiI3OTYyMjBiZDdlZDc0ZmMxYmQzYzA3MTRkOTQxMTM2OSJ9.oQwqiGfmgUOu1vWtz8Pggg1l2hAfexUfSWQIhRD1fudYuZc8-TH64Xj-ktfRQ0kDhL8sqTf_T00RPYpbSbjwiHCp6--RIlGGIZWvCMeYO5RUgzvYn2THUBTxIf77DoynIdnj1MhhzqULQXYoJl6f8DslfD6ymrW_083dNjKV0x6vFUJZzL2UWqi-CW_HEXrWRbxynlHnBgKg4fV7cHld_4j-IY1Y8GAML21lpVOOZdvO6U4DkofBqHlxaDh77zFZurYm5skZ_fUiq8SFESSl3aoBGdUsS3kpCI_5lSXGpJW3oBc1l3TJrZLxja_2x2YyojYpbng0N8Vu-k4ILDjAmQ'
        }

    @abstractmethod
    def prepare(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError
