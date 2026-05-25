# Pydantic & FastAPI Tutorial

Welcome to the Pydantic and FastAPI learning path! This project is structured to take you from basic data validation to advanced usage within a web framework.

## How to use this tutorial
1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Follow the chapters**: Each folder represents a topic. Open the `.py` files, read the comments, and run them to see the output.

## Chapter Overview
- **01_basics**: Learn about `BaseModel`, basic type hints, required vs optional fields, and how Pydantic coerces types.
- **02_nested_models**: See how to build complex data structures by nesting one model inside another.
- **03_validators**: Master custom validation logic using `@field_validator` and `@model_validator`.
- **04_advanced_types**: Explore built-in types like `EmailStr`, `HttpUrl`, and `SecretStr`.
- **05_field_customization**: Use the `Field` function for constraints (min/max), aliases, and documentation.
- **06_config_and_serialization**: Learn about `ConfigDict`, ORM compatibility, and exporting data to dict/JSON.
- **07_fastapi_integration**: See Pydantic in a real-world scenario: defining request bodies and response models in FastAPI.

## Running the Examples
Simply run any file with Python:
```bash
python 01_basics/01_basic_model.py
```

For the FastAPI chapter:
```bash
python 07_fastapi_integration/01_fastapi_usage.py
```
Then visit `http://127.0.0.1:8000/docs` in your browser.
