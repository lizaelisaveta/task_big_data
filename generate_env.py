import subprocess
import yaml
import os


VAULT_FILE = "ansible/secrets.yml"
VAULT_PASS = ".vault_pass.txt"
ENV_FILE = ".env"


result = subprocess.run(
    ["ansible-vault", "view", VAULT_FILE, "--vault-password-file", VAULT_PASS],
    capture_output=True, text=True
)

if result.returncode != 0:
    print("Ошибка при расшифровке Vault:", result.stderr)
    exit(1)

secrets = yaml.safe_load(result.stdout)


with open(ENV_FILE, "w") as f:
    for k, v in secrets.items():
        f.write(f"{k}={v}\n")

print(f"{ENV_FILE} сгенерирован из Vault")
