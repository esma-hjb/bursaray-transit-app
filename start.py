"""
Bursa Transit - Tek Komut Başlatıcı
====================================
Mock API (Flask) ve Streamlit uygulamasını aynı anda başlatır.

Kullanım:
    python start.py

Durdurmak için: Ctrl+C
"""

import subprocess
import sys
import time
import signal
import os

API_PORT = 5000
STREAMLIT_PORT = 8501


def check_port(port: int) -> bool:
    """Port zaten kullanılıyor mu kontrol eder."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def main():
    procs = []

    # ── 1. Flask Mock API ────────────────────────────────────
    if check_port(API_PORT):
        print(f"✅ Port {API_PORT} zaten açık — Mock API atlanıyor.")
    else:
        print(f"🚀 Mock API başlatılıyor → http://127.0.0.1:{API_PORT}")
        api_proc = subprocess.Popen(
            [sys.executable, "api/mock_api.py"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        procs.append(api_proc)
        time.sleep(1.5)  # Flask'ın ayağa kalkması için bekle

        if check_port(API_PORT):
            print(f"✅ Mock API hazır → http://127.0.0.1:{API_PORT}/buses")
        else:
            print("⚠️  Mock API başlatılamadı, Streamlit yine de açılıyor.")

    # ── 2. Streamlit ─────────────────────────────────────────
    print(f"🌐 Streamlit başlatılıyor → http://localhost:{STREAMLIT_PORT}")
    st_proc = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", str(STREAMLIT_PORT),
            "--server.headless", "true",
        ]
    )
    procs.append(st_proc)

    # ── Ctrl+C gelince her ikisini de kapat ──────────────────
    def shutdown(sig, frame):
        print("\n🛑 Kapatılıyor...")
        for p in procs:
            p.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    print("\n✨ Her şey hazır! Tarayıcında aç: http://localhost:8501")
    print("   Durdurmak için: Ctrl+C\n")

    # Streamlit bitene kadar bekle
    st_proc.wait()


if __name__ == "__main__":
    main()
