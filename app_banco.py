import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

# Defina um caminho padrão caso a variável de ambiente não esteja configurada
CAMINHO_PADRAO_USUARIOS_SENHAS = 'usuarios.csv'
CAMINHO_USUARIOS_SENHAS = os.getenv('user_senha', CAMINHO_PADRAO_USUARIOS_SENHAS)

# Use um caminho relativo para o arquivo de informações
CAMINHO_INFOS = Path('infos.csv')

def carregar_dados_usuarios():
    try:
        return pd.read_csv(CAMINHO_USUARIOS_SENHAS, sep=';')
    except FileNotFoundError:
        print(f"Arquivo de usuários não encontrado: {CAMINHO_USUARIOS_SENHAS}")
        print("Criando um novo arquivo de usuários...")
        df = pd.DataFrame({'Usuário': [], 'Senha': []})
        df.to_csv(CAMINHO_USUARIOS_SENHAS, sep=';', index=False)
        return df

def carregar_dados_conta():
    try:
        return pd.read_csv(CAMINHO_INFOS, sep=';')
    except FileNotFoundError:
        print(f"Arquivo de informações não encontrado: {CAMINHO_INFOS}")
        print("Criando um novo arquivo de informações...")
        df = pd.DataFrame({'Usuário': [], 'Saldo': []})
        df.to_csv(CAMINHO_INFOS, sep=';', index=False)
        return df

def salvar_dados_conta(df):
    df.to_csv(CAMINHO_INFOS, sep=';', index=False)

def login():
    usuarios_senhas = carregar_dados_usuarios()
    print("| ------------------------- |")
    print("| BEM-VINDO(A) AO FlaBank's! |")
    print("| ------------------------- |")
    
    while True:
        try:
            usuario = int(input('* Digite o usuário: '))
            senha = input('* Digite a senha: ')

            if usuarios_senhas.empty:
                print("Nenhum usuário cadastrado. Criando novo usuário...")
                novo_usuario = pd.DataFrame({'Usuário': [usuario], 'Senha': [senha]})
                usuarios_senhas = pd.concat([usuarios_senhas, novo_usuario], ignore_index=True)
                usuarios_senhas.to_csv(CAMINHO_USUARIOS_SENHAS, sep=';', index=False)
                print("Usuário criado com sucesso!")
                return usuario

            if ((usuarios_senhas['Usuário'] == usuario) & (usuarios_senhas['Senha'] == senha)).any():
                print('Login efetuado\n')
                return usuario
            else:
                print('\nUsuário ou senha incorretos, tente novamente.\n')
        except ValueError:
            print('\nOpção inválida, utilize somente números para o usuário. Por favor, tente novamente.\n')

def obter_saldo(usuario):
    dados_conta = carregar_dados_conta()
    linha_usuario = dados_conta[dados_conta['Usuário'] == usuario]
    if linha_usuario.empty:
        # Se o usuário não existe no arquivo de informações, adicione-o com saldo zero
        novo_usuario = pd.DataFrame({'Usuário': [usuario], 'Saldo': [0.0]})
        dados_conta = pd.concat([dados_conta, novo_usuario], ignore_index=True)
        salvar_dados_conta(dados_conta)
        return 0.0
    return linha_usuario['Saldo'].values[0]

def atualizar_saldo(usuario, novo_saldo):
    dados_conta = carregar_dados_conta()
    if usuario not in dados_conta['Usuário'].values:
        # Se o usuário não existe, adicione-o
        novo_usuario = pd.DataFrame({'Usuário': [usuario], 'Saldo': [novo_saldo]})
        dados_conta = pd.concat([dados_conta, novo_usuario], ignore_index=True)
    else:
        dados_conta.loc[dados_conta['Usuário'] == usuario, 'Saldo'] = novo_saldo
    salvar_dados_conta(dados_conta)

def deposito(usuario):
    saldo_atual = obter_saldo(usuario)
    while True:
        try:
            valor = float(input('Digite o valor de depósito: '))
            if valor <= 0:
                print('\nO valor deve ser positivo. Tente novamente.\n')
                continue
            if valor > 5000:
                print('\nO valor é superior ao limite de R$ 5.000. Tente novamente\n')
                continue
            
            confirmacao = input('Deseja continuar? (S/N): ').upper().strip()
            if confirmacao == 'S':
                novo_saldo = saldo_atual + valor
                atualizar_saldo(usuario, novo_saldo)
                print('\nDepósito concluído com sucesso.\n')
                break
            else:
                print('\nDepósito cancelado.\n')
                break
        except ValueError:
            print('\nValor inválido. Por favor, digite um número.\n')

def saque(usuario):
    saldo_atual = obter_saldo(usuario)
    while True:
        try:
            valor = float(input('Digite o valor de saque: '))
            if valor <= 0:
                print('\nO valor deve ser positivo. Tente novamente.\n')
                continue
            if valor > 5000:
                print('\nO valor é superior ao limite de R$ 5.000. Tente novamente\n')
                continue
            if valor > saldo_atual:
                print('\nSaldo insuficiente\n')
                continue
            
            confirmacao = input('Deseja continuar? (S/N): ').upper().strip()
            if confirmacao == 'S':
                novo_saldo = saldo_atual - valor
                atualizar_saldo(usuario, novo_saldo)
                print('\nSaque concluído com sucesso\n')
                break
            else:
                print('\nSaque cancelado.\n')
                break
        except ValueError:
            print('\nValor inválido. Por favor, digite um número.\n')

def transferencia(usuario):
    saldo_atual = obter_saldo(usuario)
    dados_conta = carregar_dados_conta()
    while True:
        try:
            destinatario = int(input('Digite o usuário destinatário: '))
            if destinatario not in dados_conta['Usuário'].values:
                print('\nUsuário não encontrado\n')
                continue
            
            valor = float(input('Digite o valor para transferência: '))
            if valor <= 0:
                print('\nO valor deve ser positivo. Tente novamente.\n')
                continue
            if valor > 5000:
                print('\nO valor é superior ao limite de R$ 5.000. Tente novamente.\n')
                continue
            if valor > saldo_atual:
                print('\nSaldo insuficiente\n')
                continue
            
            confirmacao = input('Deseja confirmar? (S/N): ').upper().strip()
            if confirmacao == 'S':
                novo_saldo_remetente = saldo_atual - valor
                novo_saldo_receptor = obter_saldo(destinatario) + valor
                atualizar_saldo(usuario, novo_saldo_remetente)
                atualizar_saldo(destinatario, novo_saldo_receptor)
                print('\nTransferência concluída com sucesso\n')
                break
            else:
                print('\nTransferência cancelada.\n')
                break
        except ValueError:
            print('\nValor inválido. Por favor, digite um número.\n')

def main():
    try:
        usuario = login()
        while True:
            try:
                print('---------------------')
                print('|       MENU        |')
                print('---------------------')
                print('| 1. SALDO          |')
                print('| 2. DEPÓSITO       |')
                print('| 3. SAQUE          |')
                print('| 4. TRANSFERÊNCIA  |')
                print('| 5. SAIR           |')
                menu = int(input('  Digite uma opção: '))
                
                if menu == 1:
                    print(f' - Saldo: R$ {obter_saldo(usuario):.2f}\n')
                elif menu == 2:
                    deposito(usuario)
                elif menu == 3:
                    saque(usuario)
                elif menu == 4:
                    transferencia(usuario)
                elif menu == 5:
                    print("Obrigado por usar o FlaBank's. Até logo!")
                    break
                else:
                    print('\nOpção inválida.\n')
            except ValueError:
                print('\nOpção inválida. Por favor, digite um número inteiro.\n')
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        print("Por favor, verifique sua configuração e tente novamente.")

if __name__ == "__main__":
    main()
