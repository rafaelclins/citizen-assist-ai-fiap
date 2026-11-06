from assistente import Assistente
from base_conhecimento import BaseConhecimento


def _pedir_nota():
    while True:
        try:
            nota = input("De 1 a 5, quão fácil foi usar o assistente? ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando sem registrar a nota.")
            return None

        if nota.isdigit() and 1 <= int(nota) <= 5:
            return int(nota)

        print("Entrada inválida. Digite um número de 1 a 5.")


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()

    assistente = Assistente("Citizen Assist AI", base)

    while True:
        print("\n===== Citizen Assist AI =====")
        print("1. Fazer uma pergunta")
        print("2. Navegar por categorias")
        print("3. Ver indicadores e sair")

        try:
            opcao = input("Escolha uma opção: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando. Até logo!")
            break

        if opcao == "1":
            try:
                if not assistente.perguntar():
                    print("Até logo!")
                    break
            except (EOFError, KeyboardInterrupt):
                print("\nEncerrando a pergunta atual.")
            except Exception as erro:
                print(f"Ocorreu um erro inesperado: {erro}")

        elif opcao == "2":
            try:
                assistente.navegar()
            except (EOFError, KeyboardInterrupt):
                print("\nRetornando ao menu.")
            except Exception as erro:
                print(f"Ocorreu um erro inesperado: {erro}")

        elif opcao == "3":
            try:
                assistente.indicadores()

                nota = _pedir_nota()
                if nota is not None and assistente.historico:
                    assistente.historico[-1]["nota_facilidade"] = nota

                assistente.exportar_csv()
            except (EOFError, KeyboardInterrupt):
                print("\nEncerrando sem exportar.")
            except Exception as erro:
                print(f"Ocorreu um erro inesperado ao encerrar: {erro}")

            print("Obrigado por usar o Citizen Assist AI. Até logo!")
            break

        else:
            print("Entrada inválida. Digite 1, 2 ou 3.")


if __name__ == "__main__":
    main()
