



def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    rate=93
    if from_currency.upper()=='USD' and to_currency.upper()=='EGP':
        result= amount*rate
    elif from_currency.upper()=='EGP' and to_currency.upper()=='USD':
        result= amount/rate
    else:
        return 'error in currency'
    
    return f"{amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}"
                


def generate_invoice(customer_name: str, items: list[dict]) -> str:
    total_price = sum(item.get('price', 0.0) for item in items)
    item_count = len(items)
    return f"Invoice for {customer_name}: {item_count} items, total ${total_price:.2f}"
