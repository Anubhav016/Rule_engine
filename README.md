

# Rule Engine with Abstract Syntax Tree (AST)

## Overview

The Rule Engine is a 3-tier application designed to determine user eligibility based on attributes such as age, department, income, and experience. It utilizes an Abstract Syntax Tree (AST) to represent conditional rules, allowing for dynamic creation, combination, and modification of these rules.

## Features

- Define and manage eligibility rules using a simple API.
- Dynamically create, combine, and modify rules using an AST.
- Evaluate user attributes against defined rules.
- Support for error handling and validation of input data.

## Data Structure

The AST is represented by a `Node` class with the following structure:

```python
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # Reference to the left child
        self.right = right     # Reference to the right child (for operators)
        self.value = value     # Optional value for operand nodes (e.g., number for comparisons)
```

## Sample Rules

- **Rule 1**: `((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)`
- **Rule 2**: `((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)`

## API Endpoints

### 1. Create Rule

**Endpoint**: `/create_rule`

**Method**: POST

**Description**: Creates a new rule from a given string representation.

**Request Body**:
```json
{
  "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
}
```

**Response**:
```json
{
  "ast": "Node object representing the corresponding AST"
}
```

### 2. Combine Rules

**Endpoint**: `/combine_rules`

**Method**: POST

**Description**: Combines multiple rules into a single AST.

**Request Body**:
```json
{
  "rules": [
    "((age > 30 AND department = 'Sales'))",
    "((age < 25 AND department = 'Marketing'))"
  ]
}
```

**Response**:
```json
{
  "combined_ast": "Node object representing the combined AST"
}
```

### 3. Evaluate Rule

**Endpoint**: `/evaluate_rule`

**Method**: POST

**Description**: Evaluates the combined rule's AST against user attributes.

**Request Body**:
```json
{
  "attributes": {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 3
  }
}
```

**Response**:
```json
{
  "result": true
}
```

## Test Cases

Test cases are included in the `test_rule_engine.py` file, covering:

- Creation of individual rules and verification of their AST representation.
- Combination of rules and validation of the resulting AST.
- Evaluation of rules against sample JSON data.
- Additional tests for various scenarios and rule combinations.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Rule Engine
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for flexible rule evaluation systems.
- Contributions from community members and open-source libraries.


