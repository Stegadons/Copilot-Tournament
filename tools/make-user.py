"""
CLI rīks administratoru un config pārvaldībai.

Funkcionalitāte:
- pievienot lietotāju
- dzēst lietotāju
- mainīt paroli
- uzstādīt secret_key
"""

import json
import os
import sys
from getpass import getpass
from werkzeug.security import generate_password_hash

CONFIG_PATH = os.environ.get("CONFIG_PATH", "config.json")


# ===== util =====

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("❌ config.json nav atrasts")
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def find_admin(config, username):
    for admin in config.get("admins", []):
        if admin.get("username") == username:
            return admin
    return None


# ===== commands =====

def add_user(username):
    config = load_config()

    if find_admin(config, username):
        print(f"❌ Lietotājs '{username}' jau eksistē")
        return

    pwd = getpass("Parole: ")
    pwd2 = getpass("Atkārtot paroli: ")

    if pwd != pwd2:
        print("❌ Paroles nesakrīt")
        return

    password_hash = generate_password_hash(
        pwd,
        method="pbkdf2:sha256",
        salt_length=16
    )

    config.setdefault("admins", []).append({
        "username": username,
        "password_hash": password_hash
    })

    save_config(config)

    print(f"✅ Lietotājs '{username}' pievienots")


def delete_user(username):
    config = load_config()

    admins = config.get("admins", [])
    new_admins = [a for a in admins if a.get("username") != username]

    if len(admins) == len(new_admins):
        print(f"❌ Lietotājs '{username}' nav atrasts")
        return

    config["admins"] = new_admins
    save_config(config)

    print(f"✅ Lietotājs '{username}' dzēsts")


def set_password(username):
    config = load_config()

    admin = find_admin(config, username)

    if not admin:
        print(f"❌ Lietotājs '{username}' nav atrasts")
        return

    pwd = getpass("Jaunā parole: ")
    pwd2 = getpass("Atkārtot paroli: ")

    if pwd != pwd2:
        print("❌ Paroles nesakrīt")
        return

    admin["password_hash"] = generate_password_hash(
        pwd,
        method="pbkdf2:sha256",
        salt_length=16
    )

    save_config(config)

    print(f"✅ Parole lietotājam '{username}' nomainīta")


def set_secret():
    config = load_config()

    secret = getpass("Ievadi jaunu SECRET_KEY: ")

    if not secret:
        print("❌ Secret nevar būt tukšs")
        return

    config["secret_key"] = secret
    save_config(config)

    print("✅ SECRET_KEY atjaunots")


# ===== CLI =====

def main():
    if len(sys.argv) < 2:
        print("""
Lietošana:

  python tools/make-user.py add <username>
  python tools/make-user.py delete <username>
  python tools/make-user.py set-password <username>
  python tools/make-user.py set-secret
""")
        return

    command = sys.argv[1]

    if command == "add" and len(sys.argv) == 3:
        add_user(sys.argv[2])

    elif command == "delete" and len(sys.argv) == 3:
        delete_user(sys.argv[2])

    elif command == "set-password" and len(sys.argv) == 3:
        set_password(sys.argv[2])

    elif command == "set-secret":
        set_secret()

    else:
        print("❌ Nepareizi argumenti")


if __name__ == "__main__":
    main()