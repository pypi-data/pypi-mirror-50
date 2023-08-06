from maltego_crypto_test import MaltegoCrypto 
from maltego_crypto_test import OAuth2BearerToken
import requests 



def test_crypto():
    private_key_path = "private_key.pem"
    encrypted_secrets = "V4zHtsulTNPh4DyoP7J/y8+dgpzpsE934z+hd0/CvOEIg/BCEGNHKuBDQeXAJZFsmqbK/ZVrfErOoY6RFJL337+vdHd0f0d3ZXFnf3VAFW3/wR395HKjESiwgEdufavOr+U1ykycbsdFNvy2epfTSbbF6XJAVhY36OyP8ISVAu9yPJ4AnlGCy49qbzdTGc2BQcv141FIJrSRmWDNbW941z1DyuzrakwT7W3VESSYLHUkoYLQijedd9OdPtPCPDIQ6XrSKz+FwUE/Kxmo0S53XU+nnfxGMYdB8vp0263rykir3Ww3MG5C0Sgy6fWtyXv7aXbDS+OZYr8DeAFwphppoqd8Jlrr9mQlRtCaWuWfK/B7/HCTx1Cf4MsU7eMnCkyEEv9isi1LAmWmkKkku3MNiEVdswUgVguDT47UOKgR7uziyhrs59UGpAeQA6BZ4dC0bsYbf9tvCDuCtKJ8akuJDg==$+bCj5pVCf1jFzK+V/kFqEg==$no+FH/73GvJtyiXLY0r+Us308Hb4LJD3NlLf3cpaN+DBL8EVka3e5426W5OBT2QRwA8+TQgOjBmMG7g/CmhGT+TYiCQS1T2tTKFBP9PSHyAelZ3WBKFJenNyazYbbrkbeOF4gvv4DbrjFhvQ87YiEPFByQ/P2ryLLTy+G0nFOao="
    api_url = ("https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))")
    
    token_fields = {'token': 'AQUc7zOH-C2VZPn5M7-GzuDxaXuflDhPbcG-Oomas8J45L2rQAAfnrrkInvjrDPAZqB2-C6BoTwCqric_Md--s5iITI2winNgiYkROz379Xyu2ZpvD2LwgVWYD_AKDhrQRMXX8TDstG-TK5XhN-7OjyxVtl6pqj_lMKyMrkF4FKtIjTrAEIEY-nCGYY_FlhuXp9SgVyZ5cuydKpVYFPC77D2bS-5qVRkdOLVeZ11f_BLlf-u5k4JYYqxfYKvWvB5IPbwRHtt8xhP23dFrKN1LhULlzLXGm8tLwmItHlRA2Fn9TnnqgxHS4lpiv2eDpKny5g8wfVtN8LWZ-PVL9VEQkr3Wb-X4w', 'token_secret': ''}

    assert MaltegoCrypto.decrypt_secrets(private_key_path,encrypted_secrets) == token_fields

def test_OauthBearer_():
    private_key_path = "private_key.pem"
    encrypted_secrets = "V4zHtsulTNPh4DyoP7J/y8+dgpzpsE934z+hd0/CvOEIg/BCEGNHKuBDQeXAJZFsmqbK/ZVrfErOoY6RFJL337+vdHd0f0d3ZXFnf3VAFW3/wR395HKjESiwgEdufavOr+U1ykycbsdFNvy2epfTSbbF6XJAVhY36OyP8ISVAu9yPJ4AnlGCy49qbzdTGc2BQcv141FIJrSRmWDNbW941z1DyuzrakwT7W3VESSYLHUkoYLQijedd9OdPtPCPDIQ6XrSKz+FwUE/Kxmo0S53XU+nnfxGMYdB8vp0263rykir3Ww3MG5C0Sgy6fWtyXv7aXbDS+OZYr8DeAFwphppoqd8Jlrr9mQlRtCaWuWfK/B7/HCTx1Cf4MsU7eMnCkyEEv9isi1LAmWmkKkku3MNiEVdswUgVguDT47UOKgR7uziyhrs59UGpAeQA6BZ4dC0bsYbf9tvCDuCtKJ8akuJDg==$+bCj5pVCf1jFzK+V/kFqEg==$no+FH/73GvJtyiXLY0r+Us308Hb4LJD3NlLf3cpaN+DBL8EVka3e5426W5OBT2QRwA8+TQgOjBmMG7g/CmhGT+TYiCQS1T2tTKFBP9PSHyAelZ3WBKFJenNyazYbbrkbeOF4gvv4DbrjFhvQ87YiEPFByQ/P2ryLLTy+G0nFOao="
    api_url = ("https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))")
    
    token_fields = MaltegoCrypto.decrypt_secrets(private_key_path,encrypted_secrets)
    auth = OAuth2BearerToken(token_fields['token'])
    response = requests.get(api_url,auth=auth)

    assert response.status_code == 200