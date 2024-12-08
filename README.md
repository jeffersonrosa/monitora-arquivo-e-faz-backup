# Monitora Arquivo e Faz Backup

Este projeto foi criado para atender a uma necessidade específica: fazer backups periódicos de um arquivo gerado no ZBrush, de forma similar ao que o Blender faz automaticamente. A ideia surgiu quando o autor estava trabalhando em um projeto no ZBrush e percebeu a falta de um backup automático periódico, algo que o Blender já faz muito bem. Assim, nasceu este script, que fica atento a alterações em um arquivo específico e cria cópias de segurança (backups) do mesmo, mantendo um histórico rotativo de versões antigas.

## Visão Geral

O script monitora um arquivo especificado pelo usuário. Quando o arquivo é alterado, um backup é criado automaticamente em uma pasta dedicada. Você pode configurar quantos backups deseja manter. Quando o limite for atingido, o backup mais antigo é removido, garantindo assim um número máximo de cópias históricas.

## Pré-requisitos

- Python 3.10 ou superior (recomendado)
- Módulos Python necessários:
  - [watchdog](https://pypi.org/project/watchdog/)
  - [rich](https://pypi.org/project/rich/)

Esses módulos estão listados no `requirements.txt`.

## Instalação

1. Clone o repositório do GitHub:
   ```bash
   git clone https://github.com/jeffersonrosa/monitora-arquivo-e-faz-backup.git
   ```
   
2. Entre na pasta do projeto:
   ```bash
   cd monitora-arquivo-e-faz-backup
   ```

3. Crie um ambiente virtual (opcional, porém recomendado):
   ```bash
   python -m venv venv
   ```
   
4. Ative o ambiente virtual:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/MacOS:
     ```bash
     source venv/bin/activate
     ```

5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Com as dependências instaladas e o ambiente ativado, simplesmente execute o `main.py`:
   ```bash
   python main.py
   ```

2. O script irá solicitar que você forneça o arquivo a ser monitorado e a pasta de backup. Você também poderá configurar a quantidade de backups a serem mantidos.

3. Após configurado, o script começará a monitorar o arquivo. Sempre que uma alteração for detectada, um novo backup será criado na pasta especificada.

4. Para encerrar o monitoramento, pressione `Ctrl+C` no terminal.

## Personalizando

- É possível pode editar o arquivo `config.json` após a primeira execução para mudar as configurações salvas.
- Os backups são armazenados na pasta configurada, por padrão uma pasta `backup` ao lado do arquivo monitorado.
- A rotação de backups é gerenciada para manter o histórico no limite configurado.