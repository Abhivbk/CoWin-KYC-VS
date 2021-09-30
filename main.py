import requests
import json
import hashlib

txnId = ""
Authentication_Token = ""

print( "-----------Want To Know Your vaccination Status?-----------" )
print( " " )
print( "-------Enter right details that you have used in Arogya setu App-------" )


def SendOtp():
    try:
        global txnId
        mobile_number = input( "Mobile Number : " ).strip()
        Full_name = input( 'Full_Name: ' )
        # Email_Id = input("Email ID: ").strip()
        credentials = {
            "mobile_number": mobile_number,
            "full_name": Full_name,
            # "email_id": Email_Id
        }
        getOTP = requests.post( 'https://cdn-api.co-vin.in/api/v3/vaccination/generateOTP', json=credentials )
        print( f'Otp has been Sent to {mobile_number}' )
        txnId = json.loads( getOTP.text )
        txnId = txnId.get( 'txnId' )
    except:
        print( "Please Use a registered NUMBER!" )
    # print(f"{getOTP}\n{txnId}" )


def VerifyOTP():
    global Authentication_Token
    while True:
        otp_in = input( "OTP: " ).strip()
        otp_in = hashlib.sha256( otp_in.encode( 'ASCII' ) )
        otp_in = otp_in.hexdigest()

        OTP = {
            "otp": otp_in,
            "txnId": txnId
        }

        verifyOTP = requests.post( 'https://cdn-api.co-vin.in/api/v3/vaccination/confirmOTP', json=OTP )

        Authentication_Token = json.loads( verifyOTP.text )
        Authentication_Token = Authentication_Token.get( 'token' )

        if verifyOTP.status_code == 401:
            print( "INVALID OTP!" )
        elif verifyOTP.status_code == 400:
            print( "PLEASE PROVIDE A OTP!" )
        elif verifyOTP.status_code == 200:
            break


def GetVaccinationStatus():
    global Authentication_Token
    headers = {
        'Authorization': 'Bearer ' + Authentication_Token
    }
    # print(Authentication_Token)
    # print(headers.get('Authorization'))

    vaccination_status_response = requests.get( 'https://cdn-api.co-vin.in/api/v3/vaccination/status', headers=headers )

    vaccination_status = json.loads( vaccination_status_response.text )
    vaccination_status = vaccination_status.get( "vaccination_status" )

    if vaccination_status == 0:
        print( "NOT VACCINATED" )
    elif vaccination_status == 1:
        print( "PARTIALLY VACCINATED" )
    elif vaccination_status == 2:
        print( "FULLY VACCINATED" )


if __name__ == 'main':
    SendOtp()
    VerifyOTP()
    GetVaccinationStatus()
