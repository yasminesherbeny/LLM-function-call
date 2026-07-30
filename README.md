# LLM Function Calling Demo

A lightweight local Python project demonstrating how to implement secure, validated tool (function) calling with Large Language Models (LLMs) like llama3.2:3b. 

The project supports both an offline **Mock LLM mode** for rapid development/testing and a **Live Ollama mode** for real local model execution. It enforces data validity via Pydantic and protects the backend via input sanitization.

---

## Features

- **Tool Routing & Orchestration**: Automatically extracts LLM intents and matches them to physical Python backend scripts.
- **Pydantic Data Validation**: Enforces strict structural boundaries and data types (`float`, `Literal` currency enums, nested list objects).
- **Input Sanitization**: Eliminates potentially dangerous characters (`/`, `;`, `$`) using custom regular expressions.
- **Dual Runtime Pipeline**: Switch between automated programmatic mocks and live interactions using an offline local Ollama pipeline.

---

## File Structure

```text
├── main.py              # Interactive CLI wrapper loop accepting user prompts
├── llm_client.py        # Logic broker routing, processing, and validating data
├── schemas.py           # Pydantic models (CurrencyConversion, InvoiceSchema)
├── security.py          # Input regex sanitizer processing string inputs
├── tools.py             # Business logic functions (convert_currency, generate_invoice)
└── tool_definitions.py  # Standardized OpenAI/Ollama compatible JSON schemas
```

---

## Installation & Setup

1. **Clone or navigate** to the project directory:
   ```bash
   cd llm-function-calling-demo
   ```

2. **Install dependencies**:
   ```bash
   pip install pydantic ollama
   ```

3. **(Optional) Install and pull Llama 3.1 via Ollama**:
   If running live local inference instead of the mock environment:
   - Download Ollama from [ollama.com](https://ollama.com).
   - Fetch the model target:
     ```bash
     ollama run llama3.2:3b
     ```

---

## Execution Instructions

To launch the interactive command line environment, execute:

```bash
python main.py
```

### Configuration Options
Inside `llm_client.py`, you can change the routing engine by adjusting the `use_mock_llm` flag:
- `use_mock_llm = True`: Executes local lightning-fast hardcoded payloads (great for verification testing).
- `use_mock_llm = False`: Connects directly to your local running Ollama instance.

### Sample Test Queries
Once the loop is active, try passing the following inputs:
- `"Convert 100 USD to EGP"`
- `"Generate an invoice for Sarah Jenkins who bought a Laptop for 1500"`
- `"exit"` (Closes the CLI gracefully)
