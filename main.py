# ui/menu.py
# Kullanıcı arayüzü (CLI menü sistemi)
# Kullanıcıdan giriş alır ve ilgili service katmanına yönlendirir
"""Bursaray Transit App - giris noktasi."""
from cli.main_menu import MainMenu


def main():
    app = MainMenu()
    app.run()


if __name__ == "__main__":
    main()
