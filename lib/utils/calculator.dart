import 'dart:math' as math;

class Calculator {
  double add(double a, double b) => a + b;

  double subtract(double a, double b) => a - b;

  double multiply(double a, double b) => a * b;

  double divide(double a, double b) {
    if (b == 0) {
      throw ArgumentError('Cannot divide by zero');
    }
    return a / b;
  }

  double percentage(double value, double percent) => value * percent / 100;

  double power(double base, double exponent) => math.pow(base, exponent).toDouble();

  double squareRoot(double value) {
    if (value < 0) {
      throw ArgumentError('Cannot take square root of a negative number');
    }
    return math.sqrt(value);
  }

  double modulo(double a, double b) {
    if (b == 0) {
      throw ArgumentError('Cannot take modulo by zero');
    }
    return a % b;
  }
}
