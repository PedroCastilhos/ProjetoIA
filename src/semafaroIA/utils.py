import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Monitoramento de Semáforo com Visão Computacional")

    parser.add_argument(
        "problema",
        help="Problema a ser resolvido (ex: detectar_estado)"
    )

    return parser.parse_args()

