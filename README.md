# scdp-ml-project

## Ambiente virtual (venv)

Crie e ative o ambiente virtual conforme seu sistema.

### Windows (PowerShell)

```powershell
# Criar o venv
python -m venv .venv

# Ativar
.\.venv\Scripts\Activate.ps1
```

Se aparecer erro de política de execução, execute no PowerShell (como administrador, se necessário):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (CMD):**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### macOS e Linux

```bash
# Criar o venv
python3 -m venv .venv

# Ativar
source .venv/bin/activate
```

### Instalar dependências

Com o venv ativado, em qualquer sistema:

```bash
pip install -r requirements.txt
```
