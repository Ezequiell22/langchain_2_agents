import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from LoadData.dicionario_loader import rodarTabelas
from LoadData.update_tbl import AtualizarDescricaoTabelas

def main():
    rodarTabelas()
    AtualizarDescricaoTabelas()

if __name__ == "__main__":
    main()

