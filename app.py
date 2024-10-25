from flask import Flask, jsonify, request, render_template
import json
import re

app = Flask(__name__)

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

# Custom JSON encoder for Node
class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return {
                "type": obj.node_type,
                "left": self.default(obj.left) if obj.left else None,
                "right": self.default(obj.right) if obj.right else None,
                "value": obj.value
            }
        return super().default(obj)

# Function to parse rule strings and return an AST
def create_rule(rule_string):
    tokens = re.findall(r'(\w+|\S)', rule_string.strip())
    
    if len(tokens) != 3:
        raise ValueError("Invalid rule format. Expected a valid expression like 'age > 30'.")

    left_operand = Node("operand", value=tokens[0])
    operator = tokens[1]
    right_operand = Node("operand", value=tokens[2])
    
    return Node("operator", value=operator, left=left_operand, right=right_operand)

# Function to combine multiple rules into a single AST
def combine_rules(rules):
    if not rules:
        raise ValueError("No rules provided to combine.")

    # Initialize the combined AST with the first rule
    combined_ast = create_rule(rules[0].strip())

    # Combine with AND operator for subsequent rules
    for rule in rules[1:]:
        new_rule_ast = create_rule(rule.strip())
        combined_ast = Node("operator", value="AND", left=combined_ast, right=new_rule_ast)

    return combined_ast

def evaluate_combined_rule(node, data):
    if node.node_type == "operand":
        return data.get(node.value, None)  # Use None if the value doesn't exist

    elif node.node_type == "operator":
        left_value = evaluate_combined_rule(node.left, data)
        right_value = evaluate_combined_rule(node.right, data)

        # Perform the operation based on the operator
        if node.value == '>':
            return left_value > right_value
        elif node.value == '<':
            return left_value < right_value
        elif node.value == '==':
            return left_value == right_value
        elif node.value == '!=':
            return left_value != right_value
        elif node.value == '>=':
            return left_value >= right_value
        elif node.value == '<=':
            return left_value <= right_value
        elif node.value == 'AND':
            return left_value and right_value
        elif node.value == 'OR':
            return left_value or right_value

    return False

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule():
    try:
        request_data = request.json
        
        if 'data' not in request_data:
            return jsonify({"error": "Missing 'data' in request."}), 200

        data = request_data['data']
        if not data:
            return jsonify({"error": "Data must not be empty."}), 200
        
        if 'combined_rule' not in request_data:
            return jsonify({"error": "Missing 'combined_rule' in request."}), 200

        combined_rule = request_data['combined_rule']
        ast_node = reconstruct_ast(combined_rule)
        
        result = evaluate_combined_rule(ast_node, data)

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 200


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    rule_string = request.form.get('rule_string', '')
    try:
        ast = create_rule(rule_string)
        return jsonify(ast=json.loads(json.dumps(ast, cls=NodeEncoder)))
    except ValueError as e:
        return jsonify(error=str(e)), 400

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    data = request.get_json()
    rules = data.get('rules', [])
    try:
        combined_ast = combine_rules(rules)
        return jsonify(ast=json.loads(json.dumps(combined_ast, cls=NodeEncoder)))
    except ValueError as e:
        return jsonify(error=str(e)), 400

def reconstruct_ast(ast_data):
    if ast_data["type"] == "operand":
        return Node("operand", value=ast_data["value"])
    
    left = reconstruct_ast(ast_data["left"]) if ast_data["left"] else None
    right = reconstruct_ast(ast_data["right"]) if ast_data["right"] else None
    return Node("operator", value=ast_data["value"], left=left, right=right)

if __name__ == "__main__":
    app.run(debug=True)
