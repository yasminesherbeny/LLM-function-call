from tools import convert_currency, generate_invoice
from tool_definitions import TOOLS
from schemas import currency_conversion, invoice_item, invoice_schema
from security import sanitize_string
import json


use_mock_llm = False

if not use_mock_llm:
    import ollama


def mock_llm(prompt: str):
    prompt_lower = prompt.lower()

    if 'convert' in prompt_lower:
        return{
            'tool_calls':[
                {
                    'function':{
                        'name': 'convert_currency',
                        'arguments':{
                                    'amount': '600',
                                    'from_currency':'USD',
                                    'to_currency':'EGP'
                                }
                    }
                    
                }
            ]
        }
    if 'generate invoice' in prompt_lower:
        return{
            'tool_calls':[
                {
                    'function':{
                        'name':'generate_invoice',
                        'arguments': {
                                        'customer_name':'Yasmine',
                                        'items': [
                                                     {'name': 'Laptop|', 'price': 10000.0}, # Added unsafe '|' to test sanitization
                                                    {'name': 'Mouse$', 'price': 500.0}     # Added unsafe '$' to test sanitization
                                                    ]
                                            }

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
            model="llama3.2:3b",
            messages=[
        {
            "role": "system", 
            "content": "CRITICAL: When calling generate_invoice, you MUST format the 'items' key as a real, unquoted JSON array. Never return 'items' as a string block."
        },
        {"role": "user", "content": prompt}],
            tools=TOOLS
        )
        message = response.get("message", {}) 

    if "tool_calls" in message:
        tool_call = message["tool_calls"][0]
        name = tool_call["function"]["name"]
        args = tool_call["function"]["arguments"]

        if name == "convert_currency":
            validated_currency = currency_conversion(**args)
            clean_from_currency= sanitize_string(validated_currency.from_currency)
            clean_to_currency= sanitize_string(validated_currency.to_currency)
            return convert_currency(validated_currency.amount,clean_from_currency,clean_to_currency)
        
        if name == "generate_invoice":
            # 1. Catch if Llama 3.2:3b passed the items list as a text string
            if "items" in args and isinstance(args["items"], str):
                try:
                    args["items"] = json.loads(args["items"])
                except json.JSONDecodeError:
                    return "Error: Local model generated an invalid items list string format."
            
            # 2. Catch if the items are inside an array but still trapped as string fragments
            elif "items" in args and isinstance(args["items"], list):
                for i, item in enumerate(args["items"]):
                    if isinstance(item, str):
                        try:
                            args["items"][i] = json.loads(item)
                        except json.JSONDecodeError:
                            pass
            validated_invoice = invoice_schema(**args) 
            clean_customer_name = sanitize_string(validated_invoice.customer_name) 
            clean_items=[]
            for item in validated_invoice.items:
                clean_items.append(
                    {
                        'name':sanitize_string(item.name),
                        'price':item.price
                    }
                )
            return generate_invoice(clean_customer_name,clean_items)
        
    return message.get("content", "")      

        



