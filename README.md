# FlaBank's - Sistema de Banco Simples
Este projeto é um sistema bancário simples implementado em Python que permite a gestão de usuários e suas contas bancárias. O sistema oferece funcionalidades básicas como login, depósito, saque, transferência e verificação de saldo.

# Funcionalidades
Login: Permite a autenticação de usuários. Se o usuário não existir, um novo será criado.
Verificar Saldo: Exibe o saldo atual do usuário.
Depósito: Permite que o usuário faça um depósito na sua conta, com limites e validações.
Saque: Permite que o usuário saque dinheiro, com validações de saldo e limites.
Transferência: Permite transferir valores entre contas, com validações de saldo e existência do destinatário.
# Dependências
Certifique-se de ter as seguintes dependências instaladas:

pandas: Para manipulação de dados.
python-dotenv: Para carregar variáveis de ambiente a partir de um arquivo .env.
Você pode instalar essas dependências usando:

bash
Copy code
pip install pandas python-dotenv
# Arquivos de Dados
O sistema utiliza dois arquivos CSV para armazenar informações:

users.csv: Armazena os dados de usuários e suas senhas.
infos.csv: Armazena os dados das contas dos usuários, incluindo saldos.
Se esses arquivos não existirem, o código irá criá-los automaticamente com cabeçalhos apropriados.

# Variáveis de Ambiente
A variável de ambiente user_senha define o caminho do arquivo de dados dos usuários. Caso não esteja configurada, será utilizado o caminho padrão users.csv.

# Como Usar
Executar o Código: Inicie o programa executando o arquivo Python.
Login: No primeiro acesso, crie um usuário informando um nome de usuário e senha. Para acessos subsequentes, utilize o nome de usuário e senha já existentes.
Menu Principal: Após o login, um menu será exibido com opções para consultar saldo, realizar depósitos, saques e transferências.
python
Copy code
if __name__ == "__main__":
    main()
# Exemplo de Uso
text
Copy code
| ------------------------- |
| BEM-VINDO(A) AO FlaBank's! |
| ------------------------- |
* Digite o usuário: 123
* Digite a senha: minhaSenha

---------------------
|       MENU        |
---------------------
| 1. SALDO          |
| 2. DEPÓSITO       |
| 3. SAQUE          |
| 4. TRANSFERÊNCIA  |
| 5. SAIR           |
Digite uma opção: 1
 - Saldo: R$ 0.00
# Notas
Limite de Transações: Os valores de depósito, saque e transferência são limitados a R$ 5.000.
Validações: O sistema inclui validações para entradas inválidas e condições de erro.
Problemas Conhecidos
Arquivos não encontrados: O sistema criará novos arquivos se os arquivos de dados não estiverem presentes, mas o caminho pode precisar ser ajustado conforme a configuração do ambiente.
# Contribuição
Sinta-se à vontade para contribuir com melhorias ou correções. Para sugestões, por favor, abra um issue ou envie um pull request.
