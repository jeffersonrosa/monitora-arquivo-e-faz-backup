# Monitora Arquivo e Faz Backup

Este projeto foi criado para atender a uma necessidade específica: fazer backups periódicos de um arquivo gerado no ZBrush, de forma similar ao que o Blender faz automaticamente. A ideia surgiu quando o autor estava trabalhando em um projeto no ZBrush e percebeu a falta de um backup automático periódico, algo que o Blender já faz muito bem. Assim, nasceu este script, que fica atento a alterações em um arquivo específico e cria cópias de segurança (backups) do mesmo, mantendo um histórico rotativo de versões antigas.

Este projeto permite o monitoramento automático de um arquivo, criando backups rotacionais sempre que ele for alterado. Foi pensado inicialmente para arquivos do ZBrush, mas pode ser usado com qualquer tipo de arquivo.

## Principais Funcionalidades

- **Monitoramento Automático:** Ao detectar mudanças no arquivo monitorado, o script cria automaticamente um backup datado.
- **Rotação de Backups:** Define quantos backups manter. Quando atinge o limite, o mais antigo é excluído.
- **Watchdog + Fallback:** Usa o [watchdog](https://pypi.org/project/watchdog/) para detectar alterações em tempo real. Caso o watchdog não detecte certos tipos de mudanças, um fallback opcional verifica periodicamente se o arquivo foi alterado, garantindo que o backup seja feito de qualquer forma.
- **Configurações Persistentes:** As configurações são salvas em `config.json` após a primeira execução. Ao iniciar, o script pergunta se quer continuar monitorando o último arquivo ou escolher outro.

## Pré-requisitos

- Python 3.10 ou superior recomendado.
- Módulos Python necessários:
  - [watchdog](https://pypi.org/project/watchdog/)
  - [rich](https://pypi.org/project/rich/)

Esses módulos estão listados em `requirements.txt`.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/jeffersonrosa/monitora-arquivo-e-faz-backup.git
   ```
   
2. Entre na pasta do projeto:
   ```bash
   cd monitora-arquivo-e-faz-backup
   ```

3. Se desejar, crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   ```
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/MacOS:
     ```bash
     source .venv/bin/activate
     ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Executando Pelo Python Diretamente

1. Com o ambiente virtual ativo, execute:
   ```bash
   python main.py
   ```
   
2. O script perguntará sobre o último arquivo monitorado (se houver), se quer manter ou escolher outro. Caso escolha outro, poderá fornecer o caminho completo ou selecionar a partir de uma pasta.

3. Escolha a pasta de backup (padrão ou customizada) e quantos backups manter.

4. O script então começa a monitorar o arquivo. Ao detectar alterações, criará backups automaticamente.

5. Para interromper, pressione `Ctrl+C`.

### Executando Pelo .bat

O projeto inclui um arquivo `backup.bat` que automatiza o processo:

- Ao rodar o `backup.bat` pela primeira vez, ele criará automaticamente um ambiente virtual local (`.venv`), instalará as dependências e iniciará o script.
- Em execuções futuras, se `.venv` já existir, apenas ativará o ambiente e rodará o script.

Basta clicar duas vezes no `backup.bat` no Windows Explorer ou executá-lo pelo terminal:
```bash
backup.bat
```

O script irá iniciar e você poderá seguir as instruções no terminal.

## Personalizando

- Após a primeira execução, um arquivo `config.json` é criado com as configurações escolhidas.
- Você pode editar manualmente o `config.json` se preferir.
- A pasta de backups pode ser alterada conforme necessário.
- O fallback (checagem periódica) pode ser desativado editando a variável `ENABLE_FALLBACK_CHECK` no `main.py`.

## Problemas Conhecidos

- Alguns softwares podem não disparar eventos de modificação de arquivos de maneira esperada. Por isso, o fallback opcional existe.
- Caso caracteres acentuados apareçam de forma estranha, tente mudar a codificação do terminal (por exemplo, `chcp 65001` no Windows) ou remover acentos.

## Contribuição

Sinta-se livre para abrir issues e pull requests, sugerindo melhorias ou reportando problemas.

## Licença

Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais informações.