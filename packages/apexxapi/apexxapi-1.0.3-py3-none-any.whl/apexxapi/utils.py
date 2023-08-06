__author__ = "Hugo Wickham"
__copyright__ = "Copyright 2019, Apexx Fintech"
__credits__ = ["Hugo Wickham", "James Jackson"]
__version__ = "1.0.1"
__email__ = "hugo.wickham@apexx.global"

"""
This is a package of helper functions which support the apexx_python library. There should not be any need to invoke
these functions outside of their usage in apexx_python; however of course you are more than welcome to do with them
what you will.
"""

import json


def createHeaders(X_APIKEY, Content_Type="application/json"):
    """
    Create headers for API calls within this package

    REQUIRED ARGUMENTS
    :param X_APIKEY: String - Authentication key for the API

    OPTIONAL ARGUMENTS
    :param Content_Type: String - Default to "application/json"

    :return: JSON Headers for API call
    """
    headers = {
        'Content-Type': Content_Type,
        'X-APIKEY': X_APIKEY
    }

    return headers


def createCardTransactionPayload(amount, capture_now, merchant_reference, card_number, cvv, expiry_month, expiry_year,
                                 token, create_token, customer_ip, user_agent, account, dynamic_descriptor,
                                 recurring_type,
                                 first_name, last_name, email, address, city, state, postal_code,
                                 country, phone, organisation, currency, customer_id, customer_last_name,
                                 customer_DOB, customer_postal_code, customer_account, webhook_transaction_update,
                                 card_brand, shopper_interaction, three_ds_required,
                                 airline_itinerary_data, numeric_code, airline_name, carrier_code,
                                 destination_airport, origin_airport, service_class, departure_date, flight_leg,
                                 passenger_name, ticket_number, agency_code, agency_name, fare_basis_code,
                                 flight_number, stop_over_code, invoice_number):
    """
    Function for constructing payload for createCardTransaction API call.
    Note: All parameters are of type String unless otherwise stated below.

    :param amount: Integer - Amount of currency's smallest denomination to be moved
    :param capture_now: Boolean - Specify whether or not to capture the transaction immediately
    :param merchant_reference: Reference code for the merchant
    :param customer_ip: Customer's IP address
    :param user_agent: String The full user agent string of the device the customer used to submit the transaction
    :param cvv: Bank card cvv
    :param card_number: Bank card number
    :param expiry_month: Bank card expiry month
    :param expiry_year: Bank card expiry year
    :param token: The token representing the payment card. Note: Once the provided token will be used, you
                        will get new token in response.
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
    :return: JSON Payload for API call
    """
    payload_py = {
        "account": account,
        "organisation": organisation,
        "currency": currency,
        "amount": amount,
        "capture_now": capture_now,
        "dynamic_descriptor": dynamic_descriptor,
        "merchant_reference": merchant_reference,
        "card": {
            "card_number": card_number,
            "cvv": cvv,
            "expiry_month": expiry_month,
            "expiry_year": expiry_year,
            "token": token,
            "create_token": create_token
        },
        "customer": {
            "customer_id": customer_id,
            "last_name": customer_last_name,
            "date_of_birth": customer_DOB,
            "postal_code": customer_postal_code,
            "account_number": customer_account
        },
        "customer_ip": customer_ip,
        "recurring_type": recurring_type,
        "user_agent": user_agent,
        "webhook_transaction_update": webhook_transaction_update,
        "card_brand": card_brand,
        "billing_address": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "address": address,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "country": country,
            "phone": phone
        },
        "shopper_interaction": shopper_interaction,
        "three_ds": {
            "three_ds_required": three_ds_required
        },
        "airline_data": {
            "airline_itinerary_data": airline_itinerary_data,
            "numeric_code": numeric_code,
            "airline_name": airline_name,
            "carrier_code": carrier_code,
            "destination_airport": destination_airport,
            "origin_airport": origin_airport,
            "service_class": service_class,
            "departure_date": departure_date,
            "flight_leg": flight_leg,
            "passenger_name": passenger_name,
            "ticket_number": ticket_number,
            "agency_code": agency_code,
            "agency_name": agency_name,
            "fare_basis_code": fare_basis_code,
            "flight_number": flight_number,
            "stop_over_code": stop_over_code,
            "invoice_number": invoice_number
        }
    }

    payload_json = json.dumps(payload_py)

    return payload_json


def cancelCardTransactionPayload(cancel_time):
    """
    Function for constructing payload for cancelCardTransaction API call.
    Note: All parameters are of type String unless otherwise stated below.

    :param cancel_time: Date and time of the request. Format - YYYY-MM-DD HH:mm:ss
    :return: JSON Payload for API call
    """
    payload_py = {
        "cancel_time": cancel_time
    }
    payload_json = json.dumps(payload_py)

    return payload_json


def refundCardTransactionPayload(amount, reason, merchant_refund_reference, refund_time):
    """
    Function for constructing payload for refundCardTransaction API call.
    Note: All parameters are of type String unless otherwise stated below.

    :param amount: Integer - Amount to be refunded
    :param reason: Reason for refund
    :param merchant_refund_reference: A reference specified by the merchant to identify the refund. This field must be
                        unique per refund.
    :param refund_time: Date and time of the request. Format - YYYY-MM-DD HH:mm:ss
    :return: JSON payload for API call
    """
    payload_py = {
        "amount": amount,
        "reason": reason,
        "merchant_refund_reference": merchant_refund_reference,
        "refund_time": refund_time
    }

    payload_json = json.dumps(payload_py)

    return payload_json


def hostedPaymentPagePayload(amount, capture_now, merchant_reference, return_url, locale, account, organisation,
                             currency, dynamic_descriptor,
                             webhook_transaction_update, shopper_interaction, first_name, last_name, email,
                             address, city, state, postal_code, country, phone, three_ds_required,
                             show_order_summary, create_token, card_brand):
    """

    Function for constructing payload for hostedPaymentPage API call.
    Note: All parameters are of type String unless otherwise stated below.

    :param amount: Integer - Amount of currency's smallest denomination to be moved
    :param capture_now: Boolean - Specify whether or not to capture the transaction immediately
    :param merchant_reference: Reference code for the merchant
    :param return_url: The return url to which the customer is redirected after an transaction is processed.
    :param locale: Valid values: "en_GB", "en_US". Locale code
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
    :param create_token: Boolean - Whether create a token or not for the card. Defaults to 'false'. Setting the to
                        'true' will create the token for the card.
    :param show_order_summary: Boolean - This field allows you to customise the order summary block in the HPP iframe.
                        True will load the order summary in the page and false will hide it.
    :param card_brand: String (Valid values "amex" "diners" "discover" "elo" "jcb" "maestro" "mastercard" "visa"
                        "visa electron") - Card brand for the card used for processing.
    :return: JSON Payload for API call
    """
    payload_py = {
        "account": account,
        "amount": amount,
        "capture_now": capture_now,
        "dynamic_descriptor": dynamic_descriptor,
        "merchant_reference": merchant_reference,
        "return_url": return_url,
        "webhook_transaction_update": webhook_transaction_update,
        "organisation": organisation,
        "locale": locale,
        "currency": currency,
        "shopper_interaction": shopper_interaction,
        "create_token": create_token,
        "card_brand": card_brand,
        "billing_address": {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "address": address,
            "city": city,
            "state": state,
            "postal_code": postal_code,
            "country": country,
            "phone": phone
        },
        "three_ds": {
            "three_ds_required": three_ds_required
        },
        "show_order_summary": show_order_summary
    }

    payload_json = json.dumps(payload_py)

    return payload_json


def captureCardTransactionPayload(amount, capture_reference):
    """
    Create JSON payload for capture transaction API call
    :param amount: Integer - Amount of currency's smallest denomination to be moved
    :param capture_reference: String - A reference specified by the merchant to identify the transaction
    :return: JSON Payload for API call
    """

    payload_py = {
        "amount": amount,
        "capture_reference": capture_reference
    }

    payload_json = json.dumps(payload_py)

    return payload_json

#################################################
#               GENERAL USE FUNCTIONS           #
#################################################

def getTransactionAmount(response):
    """
    Get the value of a transaction from the API response
    :param response: Response object in JSON
    :return: Integer - Value of transaction
    """

    resp_dict = json.loads(response.text)

    try:
        amount = resp_dict["amount"]
    except KeyError:
        print('Retrieval unsuccessful.')
        return None

    return int(amount)


def getTransactionID(response):
    """
    Get the ID of a transaction from the API response
    :param response: Response object in JSON
    :return: Transaction ID
    """

    resp_dict = json.loads(response.text)

    url = resp_dict["_id"]

    return url


def getResponseUrl(response):
    """
    Get the return url from a hosted payment API call
    :param response: Response object in JSON
    :return: Transaction ID
    """

    resp_dict = json.loads(response.text)

    try:
        url = resp_dict["url"]
    except KeyError:
        print('Retrieval unsuccessful.')
        return None

    return int(url)


def getToken(response):
    """
    Get the tokenised card reference from the API response
    :param response: Response object in JSON
    :return: String - token
    """

    resp_dict = json.loads(response.text)

    try:
        token = resp_dict["token"]
    except KeyError:
        print('Retrieval unsuccessful.')
        return None

    return token


def getReasonCode(response):
    """
    Get the reason code from the API response
    :param response: Response object in JSON
    :return: String - reason code
    """

    resp_dict = json.loads(response.text)

    try:
        reason = resp_dict["reason_code"]
    except KeyError:
        print('Retrieval unsuccessful.')
        return None

    return reason


def getResponseCode(response):
    """
    Get the Https response code
    :param response: Response object in JSON
    :return: String - response code
    """

    return response.status_code


def getStatus(response):
    """
    Get the status of the request from the API response
    :param response: Response object in JSON
    :return: String - statuse
    """

    resp_dict = json.loads(response.text)

    try:
        status = resp_dict["status"]
    except KeyError:
        print('Retrieval unsuccessful.')
        return None

    return status


