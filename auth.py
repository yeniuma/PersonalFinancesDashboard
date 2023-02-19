import yaml
import streamlit_authenticator as stauth


def get_authenticator():
    with open('auth.yaml') as file:
        config = yaml.load(file, Loader=stauth.SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )
    return authenticator
    

def get_authentication_status(authenticator):
    _, authentication_status, _ = authenticator.login('Login', 'main')
    return authentication_status

    