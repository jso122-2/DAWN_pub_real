import os
import shutil

def unseal_if_needed(seed):
    sealed_path = os.path.join("juliet_flowers", "sealed", seed)
    active_path = os.path.join("juliet_flowers", seed)

    if not os.path.exists(sealed_path):
        return

    for fname in os.listdir(sealed_path):
        src = os.path.join(sealed_path, fname)
        dst = os.path.join(active_path, fname)
        if not os.path.exists(dst):
            os.makedirs(active_path, exist_ok=True)
            shutil.move(src, dst)
            print(f"[Memory] 🔓 Unsealed {fname} into {seed}/")
            
def unseal_if_needed(seed):
    sealed_path = os.path.join("juliet_flowers", "sealed", seed)
    active_path = os.path.join("juliet_flowers", seed)

    if not os.path.exists(sealed_path):
        return

    for fname in os.listdir(sealed_path):
        src = os.path.join(sealed_path, fname)
        dst = os.path.join(active_path, fname)
        if not os.path.exists(dst):
            os.makedirs(active_path, exist_ok=True)
            shutil.move(src, dst)
            print(f"[Memory] 🔓 Unsealed {fname} into {seed}/")
