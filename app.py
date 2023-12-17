from flask import Flask, request, jsonify
from calculator import Calculator


calculator = Calculator()
app = Flask(__name__)


@app.route('/evaluate', methods=['POST'])
def evaluate_expression():
    try:
        data = request.get_json()
        expression = data['expression']
        result = calculator.evaluate(expression)
        return jsonify({'answer': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
