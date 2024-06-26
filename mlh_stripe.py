import stripe, sys, os, json, requests, py_compile
from typing import Union, Optional, cast, Any
from fastapi import FastAPI
from stripe._stripe_object import StripeObject


sys.path.append('/anaconda3/Lib/site-packages')
sys.path.insert(0, '/anaconda3/Lib/site-packages')

py_compile.compile('mlh_stripe.py')

app = FastAPI()

def pull_data(data_request: Optional[Any] = None) -> any:
    file = open('stripe_data.json')

    data = json.load(file)
    
    try:
        return data[data_request]
    except Exception:
        print("No value was passed to the function.")

 

global API_KEY

API_KEY = stripe.api_key = pull_data('apiKey')

# unnecessary? 
stripe.api_key = API_KEY

URL = 'https://raw.githubusercontent.com/stripe-samples/test-data/master/customer-with-subscription/create-fixtures.json'

app.route('/authorize', methods=['POST'])
def authorize() -> None:
    stripe.OAuth.authorize_url(scope='read-only', always_prompt=False)
    
app.route('/deauthorize', methods=['POST'])
def deAuthorize() -> None:
    stripe.OAuth.deauthorize(api_key=API_KEY, client_id='')
    
    
class MLH_Stripe(StripeObject):

    def __init__(self) -> None:
        pass
    
    
    def request_call(self, url: Optional[str] = None) -> json:
        # r = requests.Request('GET', URL)
        header = {
           'Authorization' : API_KEY 
        }
        response = requests.get(url=URL, headers=header)
        # print(r)
        # print(response.json())
        return response.json()





    # stripe.app_info('stripe-samples/checkout-one-time-payments', version='0.0.1', url='https://github.com/stripe-samples/checkout-one-time-payments')

    # create customer data to [initial test data]
    app.post('/v1/customers')
    def create_customer(self) -> stripe.Customer:
        customer_params =  {
                'id'  :  "cus_NffrFeUfNV2Hib",
                'address'  :  None,
                "object": "customer",
                'balance'  :  0,
                'cashBalance' : None,
                'created'  :  1680893993,
                'currency'  :  None,
                'defaultSource'  :  None,
                'delinquent'  :  False,
                'description'  :  None,
                'discount'  :  None,
                 'email'  :  "jennyrosen@example.com",
                'invoice_prefix'  :  "0759376C",
                'invoiceSettings'  :  {
                     'CustomFields'  :  None,
                     'DefaultPaymentMethod'  :  None,
                     'Footer'  :  None,
                     'RenderingOptions'  :  None
                },
                'liveMode'  :  False,
                'paymentMethod' : "card",
                'metadata'  :  {},
                'name'  :  "Jenny Rosen",
                'next_invoice_sequence'  :  1,
                'phone'  :  None,
                'plan' : None,
                'preferredLocales'  :  ["en-US"],
                'shipping'  :  None,
                'taxExempt'  :  None,
                'testClock'  :  None
                }
        stripe.CustomerService
        return cast(stripe.Customer, stripe.Customer.create(
                address  = customer_params.get('address') or None,
                balance  =  customer_params.get('balance') or 0,
                currency =  customer_params.get('currency') or None,
                cashBalance = customer_params.get('cashBalance') or None,
                default_source =  customer_params.get('defaultSource') or None,
                description  = customer_params.get('description') or None,
                discount  = customer_params.get('discount') or None,
                email  =  customer_params.get('email') or None,
                invoiceSettings  =  customer_params.get('invoiceSettings') or {},
                metadata  =  customer_params.get('metadata') or {},
                name  =  customer_params.get('name') or None,
                phone  =  customer_params.get('phone') or None,
                plan = customer_params.get('plan') or None,
                preferred_locales  = customer_params.get('preferredLocales') or [],
                shipping  =  customer_params.get('shipping') or None,
                tax_exempt  =  customer_params.get('taxExempt') or 'none',
                test_clock  =  customer_params.get('testClock') or None
            ))
    
    # search for customer: other than id parameter
    app.get(f'/v1/customers/search')
    def query_customer(self, param: Optional[list[Any] | str] = None, param_type: Optional[list[Any] | str] = None) -> stripe.Customer:
        params = ''
        while True:
            if type(param) == str:
                params += param_type + ': ' + '"'+param+'"'
                break
            for i,v in enumerate(param):
                if i == 0:
                    params += param_type + ': ' + param
                else:
                    params += param_type + ': ' + param + ' AND ' 
            break
        
        return cast(stripe.Customer, stripe.Customer.search(query=params))

    # request customer data object from strip
    app.get(f'/v1/customers/{id}')
    def request_customer(self, id: Optional[str] = None) -> stripe.Customer:
        return cast(stripe.Customer, stripe.Customer.retrieve(id, api_key=API_KEY))

        # "ch_3Lmjoz2eZvKYlo2C1rBER4Dk",
        # stripe_account="acct_1032D82eZvKYlo2C"

    # update customer data object
    app.post(f'/v1/customers/{id}')
    def update_customer(self, id: Optional[str] = None, update_option: Optional[dict] = None) -> None:
        # test = [update_key = update_value]
        metadata = {"order_id": "6735"}
        print(stripe.Customer.modify(id, ))
        return stripe.Customer.modify(id, metadata = {"order_id": "6735"})


    app.delete(f'/v1/customers/{id}')
    def delete_customer(self, id: Optional[str] = None) -> None:
        stripe.Customer.delete(id, stripe_account='')
    

    app.get('/v1/customers')
    def get_customer_list(self, count: int = 0) -> list:
        return stripe.Customer.list(list=count, stripe_account='')

if __name__ == '__main__':
    mlh_stripe = MLH_Stripe()
    mlh_stripe.create_customer()
    mlh_stripe.query_customer("Jenny Rosen", 'email')
    mlh_stripe.request_customer(mlh_stripe.create_customer().id)
    mlh_stripe.update_customer(mlh_stripe.create_customer().id)
    # app.get()
    # app.run()
    


    