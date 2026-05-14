"""Calculadora simples em linha de comando."""


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


OPERATIONS = {
    "1": ("Somar", add, "+"),
    "2": ("Subtrair", subtract, "-"),
    "3": ("Multiplicar", multiply, "*"),
    "4": ("Dividir", divide, "/"),
}


def read_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Valor inválido. Digite um número.")


def main() -> None:
    print("=== Calculadora Simples ===")
    while True:
        print("\nEscolha a operação:")
        for key, (label, _, _) in OPERATIONS.items():
            print(f"  {key}. {label}")
        print("  0. Sair")

        choice = input("Opção: ").strip()
        if choice == "0":
            print("Até mais!")
            break

        if choice not in OPERATIONS:
            print("Opção inválida.")
            continue

        a = read_number("Primeiro número: ")
        b = read_number("Segundo número: ")

        label, func, symbol = OPERATIONS[choice]
        try:
            result = func(a, b)
        except ZeroDivisionError as exc:
            print(f"Erro: {exc}")
            continue

        print(f"Resultado: {a} {symbol} {b} = {result}")


if __name__ == "__main__":
    main()
