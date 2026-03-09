from app.tools import convert_currency, generate_invoice
from app.schemas import currency_conversion, invoice_item, invoice_schema
from app.security import sanitize_string


use_mock_llm = True

if not use_mock_llm:
    import ollama

TOOLS = [
    {
        'name': 'convert_currency',
        'description':'convert currency using rate',
        'parameters':{
            'type':'object',
            'properties':{
                'amount': {'type':'number'},
                'from_currency':{'type': 'string'},'enum':['USD','EGP'],
                'to_currency':{'type': 'string'},'enum':['USD','EGP']
            },
            'required':['amount','from_currency','to_currency']
        }
    },
    {
        'name': 'generate_invoice',
        'description':'generates an invoice for the customer',
        'parameters':{
            'type':'object',
            'properties':{
                'customer_name':{'type':'string'},
                'items':{'type':'array'}
            },
            'required':['customer_name','items']
        }
    }
]



def mock_llm(prompt: str):
    prompt_lower = prompt.lower

    if 'convert' in prompt:
        return{
            'tool_calls':[
                {
                    'name': 'convert_currency',
                    'arguments':{
                        'amount': '600',
                        'from_currency':'USD',
                        'to_currency':'EGP'
                    }
                }
            ]
        }
    if 'generate invoice' in prompt:
        return{
            'tool_calls':[
                {
                    'name':'generate_invoice',
                    'arguments': {
                        'customer_name':'Yasmine',
                        'items':['Laptop', 'Mouse', 'Keyboard']
                    }
                }
            ]
        }
    return {"content": "No function call required."}


def run_llm (prompt:str):

    if use_mock_llm:
        response= mock_llm(prompt)
        message = response
    else:
        response = ollama.chat(
            model="llama3.1",
            messages=[{"role": "user", "content": prompt}],
            tools=TOOLS
        )
        message = response["message"] 

    if "tool_calls" in message:
        tool_call = message["tool_calls"][0]
        name = tool_call["name"]
        args = tool_call["arguments"]

        if name == "convert_currency":
            from_currency= sanitize_string(args['from_currency'])
            to_currency= sanitize_string(args['to_currency'])
            return convert_currency(from_currency,to_currency)
        if name == "generate invoice":
            customer_name = sanitize_string(args['customer_name']) 
            validated_invoice = invoice_item(**args) 
            return generate_invoice(customer_name)
    return message.get("content", "")      

        







