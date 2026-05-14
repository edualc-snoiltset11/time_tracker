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


def nth_root(a: float, n: float) -> float:
    if n == 0:
        raise ValueError("O índice da raiz não pode ser zero.")
    if a < 0 and int(n) == n and int(n) % 2 == 0:
        raise ValueError("Raiz par de número negativo não é permitida.")
    sign = -1 if a < 0 else 1
    return sign * (abs(a) ** (1 / n))


def factorial(a: float) -> int:
    if a < 0 or a != int(a):
        raise ValueError("Fatorial só é definido para inteiros não negativos.")
    return math.factorial(int(a))


def logarithm(a: float, base: float) -> float:
    if a <= 0 or base <= 0 or base == 1:
        raise ValueError("Logaritmo inválido: a > 0, base > 0 e base != 1.")
    return math.log(a, base)


def natural_log(a: float) -> float:
    if a <= 0:
        raise ValueError("ln só é definido para a > 0.")
    return math.log(a)


def log10(a: float) -> float:
    if a <= 0:
        raise ValueError("log10 só é definido para a > 0.")
    return math.log10(a)


def exp_e(a: float) -> float:
    return math.exp(a)


def absolute(a: float) -> float:
    return abs(a)


def percentage(a: float, b: float) -> float:
    """Calcula a% de b."""
    return (a / 100) * b


def percent_change(a: float, b: float) -> float:
    """Variação percentual de a para b."""
    if a == 0:
        raise ValueError("Variação percentual indefinida quando o valor inicial é zero.")
    return (b - a) / abs(a) * 100


def hypotenuse(a: float, b: float) -> float:
    return math.hypot(a, b)


def gcd(a: float, b: float) -> int:
    if a != int(a) or b != int(b):
        raise ValueError("MDC só é definido para inteiros.")
    return math.gcd(int(a), int(b))


def lcm(a: float, b: float) -> int:
    if a != int(a) or b != int(b):
        raise ValueError("MMC só é definido para inteiros.")
    return math.lcm(int(a), int(b))


def floor_div(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Divisão inteira por zero não é permitida.")
    return a // b


def trig(func, radians: bool):
    def wrapper(a: float) -> float:
        x = a if radians else math.radians(a)
        return func(x)
    return wrapper


def compile_function(expression: str):
    code = compile(expression, "<f(x)>", "eval")

    def f(x: float) -> float:
        return eval(code, {"__builtins__": {}}, {**SAFE_NAMES, "x": x})

    return f


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


def read_choice(prompt: str, options: tuple[str, ...]) -> str:
    while True:
        answer = input(prompt).strip().lower()
        if answer in options:
            return answer
        print(f"Opção inválida. Use: {', '.join(options)}")


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


def nth_root_op():
    a = read_number("Radicando (a): ")
    n = read_number("Índice (n): ")
    print(f"Resultado: ⁿ√a = {n}√{a} = {nth_root(a, n)}")


def percentage_op():
    a = read_number("Percentual (a%): ")
    b = read_number("Sobre o valor (b): ")
    print(f"Resultado: {a}% de {b} = {percentage(a, b)}")


def percent_change_op():
    a = read_number("Valor inicial: ")
    b = read_number("Valor final: ")
    print(f"Resultado: variação = {percent_change(a, b):.4f}%")


def trig_op(func, name):
    def runner():
        unit = read_choice("Unidade (r=radianos, d=graus): ", ("r", "d"))
        a = read_number("Ângulo: ")
        result = trig(func, radians=(unit == "r"))(a)
        print(f"Resultado: {name}({a} {'rad' if unit == 'r' else '°'}) = {result}")
    return runner


def average_op():
    raw = input("Números separados por espaço ou vírgula: ").replace(",", " ").split()
    if not raw:
        raise ValueError("Nenhum número informado.")
    nums = [float(x) for x in raw]
    print(f"Resultado: média de {len(nums)} valores = {sum(nums) / len(nums)}")


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
    "5": ("Divisão inteira (a // b)", binary_op(floor_div, "//")),
    "6": ("Módulo (a % b)", binary_op(modulo, "%")),
    "7": ("Potência (a ^ b)", binary_op(power, "^")),
    "8": ("Raiz quadrada (√a)", unary_op(square_root, "√")),
    "9": ("Raiz enésima (ⁿ√a)", nth_root_op),
    "10": ("Fatorial (a!)", unary_op(factorial, "fact")),
    "11": ("Valor absoluto |a|", unary_op(absolute, "|·|")),
    "12": ("Exponencial (eˣ)", unary_op(exp_e, "exp")),
    "13": ("Logaritmo natural (ln a)", unary_op(natural_log, "ln")),
    "14": ("Logaritmo base 10 (log a)", unary_op(log10, "log10")),
    "15": ("Logaritmo qualquer base", log_op),
    "16": ("Seno", trig_op(math.sin, "sin")),
    "17": ("Cosseno", trig_op(math.cos, "cos")),
    "18": ("Tangente", trig_op(math.tan, "tan")),
    "19": ("Porcentagem (a% de b)", percentage_op),
    "20": ("Variação percentual", percent_change_op),
    "21": ("Hipotenusa √(a²+b²)", binary_op(hypotenuse, "⊿")),
    "22": ("MDC (gcd)", binary_op(gcd, "gcd")),
    "23": ("MMC (lcm)", binary_op(lcm, "lcm")),
    "24": ("Média aritmética de N valores", average_op),
    "25": ("Derivada f'(x) num ponto", derivative_op),
    "26": ("Piso ⌊a⌋", unary_op(math.floor, "floor")),
    "27": ("Teto ⌈a⌉", unary_op(math.ceil, "ceil")),
}


def main() -> None:
    print("=== Calculadora Simples ===")
    print("Dica: em f(x), use sintaxe Python e funções de math (sin, cos, exp, log, pi, e, ...).")
    while True:
        print("\nEscolha a operação:")
        for key, (label, _) in OPERATIONS.items():
            print(f"  {key:>2}. {label}")
        print("   0. Sair")

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
