import sys
from .utils import parse_args


def main():
    args = parse_args()
    try:
        problema = args.problema
        print(f"Iniciando o monitoramento de semáforo para ver o problema: {problema}")
        return 0
    except AttributeError as e:
        print(f"Erro: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

