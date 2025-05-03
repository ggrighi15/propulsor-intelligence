
import os

def revisar_estrutura(base_path='C:/propulsor-intelligence'):
    print(f"Verificando arquivos em {base_path}")
    for root, dirs, files in os.walk(base_path):
        for file in files:
            print(f"✓ Encontrado: {os.path.join(root, file)}")

if __name__ == '__main__':
    revisar_estrutura()
