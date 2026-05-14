"""Calculadora simples em linha de comando."""

import math


SAFE_NAMES = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
SAFE_NAMES.update({"abs": abs, "round": round, "min": min, "max": max})


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Divisão por zero não é permitida.")
    return a / b


def power(a: float, b: float) -> float:
    return a ** b


def modulo(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Módulo por zero não é permitida.")
    return a % b


def square_root(a: float) -> float:
    if a < 0:
        raise ValueError("Raiz quadrada de número negativo não é permitida.")
    return math.sqrt(a)


def factorial(a: float) -> int:
    if a < 0 or a != int(a):
        raise ValueError("Fatorial só é definido para inteiros não negativos.")
    return math.factorial(int(a))


def logarithm(a: float, base: float) -> float:
    if a <= 0 or base <= 0 or base == 1:
        raise ValueError("Logaritmo inválido: a > 0, base > 0 e base != 1.")
    return math.log(a, base)


def compile_function(expression: str):
    code = compile(expression, "<f(x)>", "eval")

    def f(x: float) -> float:
        return eval(code, {"__builtins__": {}}, {**SAFE_NAMES, "x": x})

    return f


def integrate(expression: str, lower: float, upper: float, n: int = 1000) -> float:
    """Integral numérica de f(x) entre lower e upper usando Simpson composto."""
    if n % 2 != 0:
        n += 1
    f = compile_function(expression)
    h = (upper - lower) / n
    total = f(lower) + f(upper)
    for i in range(1, n):
        x = lower + i * h
        total += (4 if i % 2 else 2) * f(x)
    return total * h / 3


def derivative(expression: str, x: float, h: float = 1e-5) -> float:
    """Derivada numérica de f(x) no ponto x (diferenças centrais)."""
    f = compile_function(expression)
    return (f(x + h) - f(x - h)) / (2 * h)


def read_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite um número.")


def binary_op(func, symbol):
    def runner():
        a = read_number("Primeiro número: ")
        b = read_number("Segundo número: ")
        result = func(a, b)
        print(f"Resultado: {a} {symbol} {b} = {result}")
    return runner


def unary_op(func, name):
    def runner():
        a = read_number("Número: ")
        result = func(a)
        print(f"Resultado: {name}({a}) = {result}")
    return runner


def log_op():
    a = read_number("Número (a): ")
    base = read_number("Base: ")
    print(f"Resultado: log_{base}({a}) = {logarithm(a, base)}")


def integral_op():
    expr = input("f(x) = ").strip()
    lower = read_number("Limite inferior: ")
    upper = read_number("Limite superior: ")
    result = integrate(expr, lower, upper)
    print(f"Resultado: ∫({expr}) dx de {lower} a {upper} ≈ {result}")


def derivative_op():
    expr = input("f(x) = ").strip()
    x = read_number("Ponto x: ")
    result = derivative(expr, x)
    print(f"Resultado: f'({x}) ≈ {result}")


OPERATIONS = {
    "1": ("Somar (a + b)", binary_op(add, "+")),
    "2": ("Subtrair (a - b)", binary_op(subtract, "-")),
    "3": ("Multiplicar (a * b)", binary_op(multiply, "*")),
    "4": ("Dividir (a / b)", binary_op(divide, "/")),
    "5": ("Potência (a ^ b)", binary_op(power, "^")),
    "6": ("Módulo (a % b)", binary_op(modulo, "%")),
    "7": ("Raiz quadrada (√a)", unary_op(square_root, "√")),
    "8": ("Fatorial (a!)", unary_op(factorial, "fact")),
    "9": ("Logaritmo (log_base(a))", log_op),
    "10": ("Integral definida ∫ f(x) dx", integral_op),
    "11": ("Derivada f'(x) num ponto", derivative_op),
}


def main() -> None:
    print("=== Calculadora Simples ===")
    print("Dica: em f(x), use sintaxe Python e funções de math (sin, cos, exp, log, pi, e, ...).")
    while True:
        print("\nEscolha a operação:")
        for key, (label, _) in OPERATIONS.items():
            print(f"  {key}. {label}")
        print("  0. Sair")

        choice = input("Opção: ").strip()
        if choice == "0":
            print("Até mais!")
            break

        if choice not in OPERATIONS:
            print("Opção inválida.")
            continue

        _, runner = OPERATIONS[choice]
        try:
            runner()
        except (ZeroDivisionError, ValueError, OverflowError) as exc:
            print(f"Erro: {exc}")
        except (SyntaxError, NameError) as exc:
            print(f"Expressão inválida: {exc}")


if __name__ == "__main__":
    main()
