__author__ = "Hugo Wickham"
__copyright__ = "Copyright 2019, Apexx Fintech"
__credits__ = ["Hugo Wickham", "James Jackson"]
__version__ = "1.0.1"
__email__ = "hugo.wickham@apexx.global"

"""
This is a package of functions to simplify the implementation of Apexx API calls within a Python backend.
To execute an API call, call the relevant 'execute...' function filling in the required fields. 
"""

import requests
from apexxapi import utils


#################################################
#               DIRECT TRANSACTIONS             #
#################################################

def createCardTransaction(X_APIKEY, amount, capture_now, merchant_reference, customer_ip, user_agent, cvv=None,
                          card_number=None, expiry_month=None, expiry_year=None,
                          token=None, create_token=False, account=None, dynamic_descriptor=" ",
                          recurring_type=None,
                          first_name=None, last_name=None, email=None, address=None, city=None, state=None,
                          postal_code=None,
                          country=None, phone=None, organisation=None, currency=None, customer_id=None,
                          customer_last_name=None,
                          customer_DOB=None, customer_postal_code=None, customer_account=None,
                          webhook_transaction_update=None,
                          card_brand=None,
                          shopper_interaction=None,
                          three_ds_required=None,
                          airline_itinerary_data=False, numeric_code=None, airline_name=None, carrier_code=None,
                          destination_airport=None, origin_airport=None, service_class=None, departure_date=None,
                          flight_leg=None,
                          passenger_name=None, ticket_number=None, agency_code=None, agency_name=None,
                          fare_basis_code=None,
                          flight_number=None, stop_over_code=None, invoice_number=None,
                          Content_Type="application/json"):
    """
    Function for constructing and executing a createCardTransaction API call.
    Note: All parameters are of type String unless otherwise stated below.

    REQUIRED ARGUMENTS
    :param X_APIKEY: Authentication key for the API
    :param amount: Integer - Amount to be moved, without decimal place
    :param capture_now: Boolean - Specify whether or not to capture the transaction immediately
    :param merchant_reference: Reference code for the merchant
    :param customer_ip: Customer's IP address
    :param user_agent: String The full user agent string of the device the customer used to submit the transaction
    :param cvv: Bank card cvv

    CARD DETAILS: MUST SEND EITHER CARD DETAILS (INC CVV) OR TOKEN+CVV, UNLESS TRANSACTION IS RECURRING OR ONE-CLICK

    :param card_number: Bank card number
    :param expiry_month: Bank card expiry month
    :param expiry_year: Bank card expiry year
    :param token: The token representing the payment card. Note: Once the provided token will be used, you
                        will get new token in response.


    OPTIONAL ARGUMENTS - NOTE: DIFFERENT ACQUIRERS MAY REQUIRE SOME OF THESE
    :param create_token: Boolean - Whether create a token or not for the card. Defaults to 'false'. Setting the to
                        'true' will create the token for the card.
    :param account: The ID of the account. Acts as an override. Must be submitted if organisation and currency are not
                        used in the request.
    :param dynamic_descriptor: A short reference/descriptor that will show up on the customers bank statement.
                        Only supported by some acquirers. Please confirm with your Implementation Manager for supported
                        acquirers and formats.
    :param recurring_type: String (Valid values "first", "recurring" and "oneclick") - This field is to be used only
                        when a transaction is part of a series of recurring transactions. If it's the initial
                        transaction, set the value to 'first', and if it's not, set it to 'recurring'.
                        This field must not be included in transactions that will not be part of a series of
                        repeated transactions. (All values are written in lowercase letters).
    :param first_name: Note: Only alphabetic characters, Special characters allowed are (hyphen(-),
                        underscore(_), dot(.), comma(,) and apostrophe(‘))
    :param last_name: Note: Only alphabetic characters, Special characters allowed are (hyphen(-),
                        underscore(_), dot(.), comma(,) and apostrophe(‘))
    :param email: Note: Only alphabets, numeric, @, comma(,) dot(.), plus(+), underscore(_), dash(-) and
                        apostrophe(‘)
    :param address: Note: All characters support
    :param city: Note: Only alphabetic characters, Special characters allowed are (hyphen(-), underscore(_),
                        dot(.), comma(,) and apostrophe(‘))
    :param state: Note: Only alphabetic characters, Special characters allowed are (hyphen(-), underscore(_),
                        dot(.), comma(,) and apostrophe(‘))
    :param postal_code: Note: Only alpha-numeric characters
    :param country: A 2-letter ISO3166 alpha-2. country code for the address. Note: Alphabets upto two
                        characters (e.g. GB, RU etc..)
    :param phone: Numbers only, no dash or any other separator. Note: Length - min(3) & max(20)
    :param organisation: The ID of an organisation
    :param currency: A 3-letter ISO 4217 currency code, see Currencies Section for more details.
    :param customer_id: The customer_id of recipient's
    :param customer_last_name: The last name(s) of recipient's
    :param customer_DOB: The date of birth of a recipient's, 10 characters, ISO-8601 (YYYY-MM-DD)
    :param customer_postal_code: This is the recipient's postcode/zip
    :param customer_account: This is the recipient's account number
    :param webhook_transaction_update: A webhook url that is called when a transaction is updated.
                        Note: This overrides any URL set on the account.
    :param card_brand: String (Valid values "amex" "diners" "discover" "elo" "jcb" "maestro" "mastercard" "visa"
                        "visa electron") - Card brand for the card used for processing.
    :param shopper_interaction: String (Valid values "ecommerce" "pos" "moto" "unknown") - Determines the point of sale
                        of a customer. Default value: ecommerce.
    :param three_ds_required: Boolean - True if 3DS required for this transaction, False otherwise.
                        Note: This field is mandatory if account is not passed.
    :param Content_Type: Default to "application/json"
    :param airline_itinerary_data: Boolean - If set to true then below fields are mandatory else if set to false then
                        below fields are not mandatory
    :param numeric_code: Airline numeric code
    :param airline_name: String Airline name
    :param carrier_code: Travel carrier code
    :param destination_airport: Destination airport/city IATA code
    :param origin_airport: Origin airport/city IATA
    :param service_class: Service class
    :param departure_date: Travel departure date
    :param flight_leg: Sequence number of the flight leg
    :param passenger_name: Passenger name
    :param ticket_number: Ticker/document number, or PNR locator code
    :param agency_code: Travel agency code
    :param agency_name: Travel agency name
    :param fare_basis_code: Fare basis code
    :param flight_number: Flight number excluding carrier code
    :param stop_over_code: Stop over code
    :param invoice_number: Invoice number of the ticket
    :return: JSON Response object from the API
    """
    url = "https://qaigate.apexxfintech.com/mgw/payment/direct"

    headers = utils.createHeaders(X_APIKEY, Content_Type)

    payload = utils.createCardTransactionPayload(amount, capture_now, merchant_reference, card_number, cvv,
                                                 expiry_month,
                                                 expiry_year,
                                                 token, create_token, customer_ip, user_agent, account,
                                                 dynamic_descriptor,
                                                 recurring_type,
                                                 first_name, last_name, email, address, city, state, postal_code,
                                                 country, phone, organisation, currency, customer_id,
                                                 customer_last_name,
                                                 customer_DOB, customer_postal_code, customer_account,
                                                 webhook_transaction_update,
                                                 card_brand, shopper_interaction, three_ds_required,
                                                 airline_itinerary_data, numeric_code, airline_name, carrier_code,
                                                 destination_airport, origin_airport, service_class, departure_date,
                                                 flight_leg,
                                                 passenger_name, ticket_number, agency_code, agency_name,
                                                 fare_basis_code,
                                                 flight_number, stop_over_code, invoice_number)

    response = requests.request("POST", url, data=payload, headers=headers)

    return response


#################################################
#               REFUND TRANSACTIONS             #
#################################################


def refundCardTransaction(transactionID, X_APIKEY, amount, reason=None, merchant_refund_reference=None,
                          refund_time=None,
                          Content_Type="application/json"):
    """
    Function for constructing and executing a refundCardTransaction API call.
    Note: All parameters are of type String unless otherwise stated below.

    REQUIRED ARGUMENTS
    :param amount: Integer - Amount to be refunded
    :param X_APIKEY: Authorisation API Key

    OPTIONAL ARGUMENTS - NOTE: DIFFERENT ACQUIRERS MAY REQUIRE SOME OF THESE
    :param reason: Reason for refund
    :param transactionID: ID of transaction
    :param merchant_refund_reference: A reference specified by the merchant to identify the refund. This field must be
                        unique per refund.
    :param refund_time: Date and time of the request. Format - YYYY-MM-DD HH:mm:ss
    :param Content_Type: Default to"application/json"
    :return: JSON Response object from the API
    """
    url = "https://qaigate.apexxfintech.com/mgw/refund/" + transactionID

    headers = utils.createHeaders(X_APIKEY, Content_Type)

    payload = utils.refundCardTransactionPayload(amount, reason, merchant_refund_reference, refund_time)

    response = requests.request("POST", url, data=payload, headers=headers)

    return response


#################################################
#                 HOSTED PAYMENTS               #
#################################################


def hostedPaymentPage(X_APIKEY, amount, capture_now, merchant_reference, return_url, locale, account=None,
                      organisation=None, currency=None, dynamic_descriptor=None,
                      webhook_transaction_update=None, shopper_interaction=None, first_name=None, last_name=None,
                      email=None,
                      address=None, city=None, state=None, postal_code=None, country=None, phone=None,
                      three_ds_required=None,
                      show_order_summary=None, create_token=None, card_brand=None, Content_Type="application/json"):
    """
    Function for constructing and executing a hostedPaymentPage API call.
    Note: All parameters are of type String unless otherwise stated below.

    REQUIRED ARGUMENTS
    :param X_APIKEY: Authentication key for the API
    :param amount: Integer - Amount of currency's smallest denomination to be moved
    :param capture_now: Boolean - Specify whether or not to capture the transaction immediately
    :param merchant_reference: Reference code for the merchant
    :param return_url: The return url to which the customer is redirected after an transaction is processed.
    :param locale: Valid values: "en_GB", "en_US". Locale code

    OPTIONAL ARGUMENTS - NOTE: DIFFERENT ACQUIRERS MAY REQUIRE SOME OF THESE
    :param account: The ID of the account. Acts as an override. Must be submitted if organisation and currency are not
                        used in the request.
    :param organisation: The ID of the organisation
    :param currency: A 3-letter ISO 4217 currency code, see Currencies Section for more details.
    :param dynamic_descriptor: A short reference/descriptor that will show up on the customers bank statement.
                        Only supported by some acquirers. Please confirm with your Implementation Manager for supported
                        acquirers and formats.
    :param webhook_transaction_update: A webhook url that is called when a transaction is updated. Note: This overrides any URL set on the account.
    :param shopper_interaction: String (Valid values "ecommerce" "pos" "moto" "unknown") - Determines the point of sale
                        of a customer. Default value: ecommerce.
    :param first_name: Note: Only alphabetic characters, Special characters allowed are (hyphen(-),
                        underscore(_), dot(.), comma(,) and apostrophe(‘))
    :param last_name: Note: Only alphabetic characters, Special characters allowed are (hyphen(-),
                        underscore(_), dot(.), comma(,) and apostrophe(‘))
    :param email: Note: Only alphabets, numeric, @, comma(,) dot(.), plus(+), underscore(_), dash(-) and
                        apostrophe(‘)
    :param address: Note: All characters support
    :param city: Note: Only alphabetic characters, Special characters allowed are (hyphen(-), underscore(_),
                        dot(.), comma(,) and apostrophe(‘))
    :param state: Note: Only alphabetic characters, Special characters allowed are (hyphen(-), underscore(_),
                        dot(.), comma(,) and apostrophe(‘))
    :param postal_code: Note: Only alpha-numeric characters
    :param country: A 2-letter ISO3166 alpha-2. country code for the address. Note: Alphabets upto two
                        characters (e.g. GB, RU etc..)
    :param phone: Numbers only, no dash or any other separator. Note: Length - min(3) & max(20)
    :param three_ds_required: Boolean - True if 3DS required for this transaction, False otherwise.
                        Note: This field is mandatory if account is not passed.
    :param show_order_summary: Boolean - This field allows you to customise the order summary block in the HPP iframe.
                        True will load the order summary in the page and false will hide it.
    :param create_token: Boolean - Whether create a token or not for the card. Defaults to 'false'. Setting the to
                        'true' will create the token for the card.
    :param card_brand: String (Valid values "amex" "diners" "discover" "elo" "jcb" "maestro" "mastercard" "visa"
                        "visa electron") - Card brand for the card used for processing.
    :param Content_Type: Defaults to 'application/json'
    :return: JSON Response object from the API
    """
    url = "https://qaigate.apexxfintech.com/mgw/payment/hosted"

    headers = utils.createHeaders(X_APIKEY, Content_Type)

    payload = utils.hostedPaymentPagePayload(amount, capture_now, merchant_reference, return_url, locale, account,
                                             organisation, currency, dynamic_descriptor,
                                             webhook_transaction_update, shopper_interaction, first_name, last_name,
                                             email,
                                             address, city, state, postal_code, country, phone, three_ds_required,
                                             show_order_summary, create_token, card_brand)

    response = requests.request("POST", url, data=payload, headers=headers)

    return response

def easterEgg():
    print("Rosebud")
#################################################
#               CAPTURE TRANSACTIONS            #
#################################################


def captureCardTransaction(amount, capture_reference, transactionID, X_APIKEY, Content_Type="application/json"):
    """
    Function for constructing and executing a captureCardTransaction API call.
    Note: All parameters are of type String unless otherwise stated below.

    REQUIRED ARGUMENTS
    :param amount: Integer - Value of transaction to be captured
    :param transactionID: ID of transaction
    :param X_APIKEY: Authorisation API Key

    OPTIONAL ARGUMENTS - NOTE: DIFFERENT ACQUIRERS MAY REQUIRE SOME OF THESE
    :param capture_reference: A reference specified by the merchant to identify the transaction
    :param Content_Type: Default "application/json", should not ever need to be changed
    :return: JSON Response object from the API
    """
    url = "https://qaigate.apexxfintech.com/mgw/capture/" + transactionID

    headers = utils.createHeaders(X_APIKEY, Content_Type)

    payload = utils.captureCardTransactionPayload(amount, capture_reference)

    response = requests.request("POST", url, data=payload, headers=headers)

    return response


#################################################
#               CANCEL TRANSACTIONS             #
#################################################


def cancelCardTransaction(transactionID, X_APIKEY, cancel_time=None, Content_Type="application/json"):
    """
    Function for constructing and executing a cancelCardTransaction API call.
    Note: All parameters are of type String unless otherwise stated below.

    REQUIRED ARGUMENTS
    :param transactionID: ID of transaction
    :param X_APIKEY: Authorisation API Key

    OPTIONAL ARGUMENTS - NOTE: DIFFERENT ACQUIRERS MAY REQUIRE SOME OF THESE
    :param cancel_time: Date and time of the request. Format - YYYY-MM-DD HH:mm:ss
    :param Content_Type: Default TO "application/json"
    :return: Response object
    """
    url = "https://qaigate.apexxfintech.com/mgw/" + transactionID + "/cancel"

    headers = utils.createHeaders(X_APIKEY, Content_Type)

    payload = utils.cancelCardTransactionPayload(cancel_time)

    response = requests.request("POST", url, data=payload, headers=headers)

    return response
