import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

# Defina um caminho padrão caso a variável de ambiente não esteja configurada
DEFAULT_USER_SENHA_PATH = 'users.csv'
USER_SENHA_PATH = os.getenv('user_senha', DEFAULT_USER_SENHA_PATH)

# Use um caminho relativo para o arquivo de informações
INFOS_PATH = Path('infos.csv')

def load_user_data():
    try:
        return pd.read_csv(USER_SENHA_PATH, sep=';')
    except FileNotFoundError:
        print(f"Arquivo de usuários não encontrado: {USER_SENHA_PATH}")
        print("Criando um novo arquivo de usuários...")
        df = pd.DataFrame({'Usuário': [], 'Senha': []})
        df.to_csv(USER_SENHA_PATH, sep=';', index=False)
        return df

def load_account_data():
    try:
        return pd.read_csv(INFOS_PATH, sep=';')
    except FileNotFoundError:
        print(f"Arquivo de informações não encontrado: {INFOS_PATH}")
        print("Criando um novo arquivo de informações...")
        df = pd.DataFrame({'Usuário': [], 'Saldo': []})
        df.to_csv(INFOS_PATH, sep=';', index=False)
        return df

def save_account_data(df):
    df.to_csv(INFOS_PATH, sep=';', index=False)

def login():
    user_senha = load_user_data()
    print("| ------------------------- |")
    print("| BEM-VINDO(A) AO FlaBank's! |")
    print("| ------------------------- |")
    
    while True:
        try:
            user = int(input('* Digite o usuário: '))
            senha = input('* Digite a senha: ')

            if user_senha.empty:
                print("Nenhum usuário cadastrado. Criando novo usuário...")
                new_user = pd.DataFrame({'Usuário': [user], 'Senha': [senha]})
                user_senha = pd.concat([user_senha, new_user], ignore_index=True)
                user_senha.to_csv(USER_SENHA_PATH, sep=';', index=False)
                print("Usuário criado com sucesso!")
                return user

            if ((user_senha['Usuário'] == user) & (user_senha['Senha'] == senha)).any():
                print('Login efetuado\n')
                return user
            else:
                print('\nUsuário ou senha incorretos, tente novamente.\n')
        except ValueError:
            print('\nOpção inválida, utilize somente números para o usuário. Por favor, tente novamente.\n')

def get_balance(user):
    user_data = load_account_data()
    user_row = user_data[user_data['Usuário'] == user]
    if user_row.empty:
        # Se o usuário não existe no arquivo de informações, adicione-o com saldo zero
        new_user = pd.DataFrame({'Usuário': [user], 'Saldo': [0.0]})
        user_data = pd.concat([user_data, new_user], ignore_index=True)
        save_account_data(user_data)
        return 0.0
    return user_row['Saldo'].values[0]

def update_balance(user, new_balance):
    user_data = load_account_data()
    if user not in user_data['Usuário'].values:
        # Se o usuário não existe, adicione-o
        new_user = pd.DataFrame({'Usuário': [user], 'Saldo': [new_balance]})
        user_data = pd.concat([user_data, new_user], ignore_index=True)
    else:
        user_data.loc[user_data['Usuário'] == user, 'Saldo'] = new_balance
    save_account_data(user_data)

def deposit(user):
    current_balance = get_balance(user)
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
                new_balance = current_balance + valor
                update_balance(user, new_balance)
                print('\nDepósito concluído com sucesso.\n')
                break
            else:
                print('\nDepósito cancelado.\n')
                break
        except ValueError:
            print('\nValor inválido. Por favor, digite um número.\n')

def withdraw(user):
    current_balance = get_balance(user)
    while True:
        try:
            valor = float(input('Digite o valor de saque: '))
            if valor <= 0:
                print('\nO valor deve ser positivo. Tente novamente.\n')
                continue
            if valor > 5000:
                print('\nO valor é superior ao limite de R$ 5.000. Tente novamente\n')
                continue
            if valor > current_balance:
                print('\nSaldo insuficiente\n')
                continue
            
            confirmacao = input('Deseja continuar? (S/N): ').upper().strip()
            if confirmacao == 'S':
                new_balance = current_balance - valor
                update_balance(user, new_balance)
                print('\nSaque concluído com sucesso\n')
                break
            else:
                print('\nSaque cancelado.\n')
                break
        except ValueError:
            print('\nValor inválido. Por favor, digite um número.\n')

def transfer(user):
    current_balance = get_balance(user)
    user_data = load_account_data()
    while True:
        try:
            destinatario = int(input('Digite o usuário destinatário: '))
            if destinatario not in user_data['Usuário'].values:
                print('\nUsuário não encontrado\n')
                continue
            
            valor = float(input('Digite o valor para transferência: '))
            if valor <= 0:
                print('\nO valor deve ser positivo. Tente novamente.\n')
                continue
            if valor > 5000:
                print('\nO valor é superior ao limite de R$ 5.000. Tente novamente.\n')
                continue
            if valor > current_balance:
                print('\nSaldo insuficiente\n')
                continue
            
            confirmacao = input('Deseja confirmar? (S/N): ').upper().strip()
            if confirmacao == 'S':
                new_balance_sender = current_balance - valor
                new_balance_receiver = get_balance(destinatario) + valor
                update_balance(user, new_balance_sender)
                update_balance(destinatario, new_balance_receiver)
                print('\nTransferência concluída com sucesso\n')
                break
            else:
                print('\nTransferência cancelada.\n')
                break
        except ValueError:
            print('\nValor inválido. Por favor, digite um número.\n')

def main():
    try:
        user = login()
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
                    print(f' - Saldo: R$ {get_balance(user):.2f}\n')
                elif menu == 2:
                    deposit(user)
                elif menu == 3:
                    withdraw(user)
                elif menu == 4:
                    transfer(user)
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