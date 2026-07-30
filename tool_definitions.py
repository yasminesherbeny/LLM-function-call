# tool_definitions.py

TOOLS = [
    {
        'type': 'function',
        'function': {
            'name': 'convert_currency',
            'description': 'Converts a specified monetary amount from one currency to another.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'amount': {
                        'type': 'number',
                        'description': 'The numeric amount of money to convert.'
                    },
                    'from_currency': {
                        'type': 'string',
                        'description': 'The source currency code (e.g., USD, EGP).'
                    },
                    'to_currency': {
                        'type': 'string',
                        'description': 'The target currency code (e.g., USD, EGP).'
                    }
                },
                'required': ['amount', 'from_currency', 'to_currency']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'generate_invoice',
            'description': 'Generates a summarized text invoice for a customer based on their list of purchased items.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'customer_name': {
                        'type': 'string',
                        'description': 'The full name of the customer.'
                    },
                    'items': {
                        'type': 'array',
                        'description': 'The list of item objects purchased by the customer.',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {
                                    'type': 'string',
                                    'description': 'The descriptive name of the item.'
                                },
                                'price': {
                                    'type': 'number',
                                    'description': 'The unit price of the item.'
                                }
                              },
                            'required': ['name', 'price']
                        }
                    }
                },
                'required': ['customer_name', 'items']
            }
        }
    }
]
