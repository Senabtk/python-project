import sqlite3
import hashlib
import random
import string
import getpass

# Veritabanı bağlantısı oluşturmak için 

conn = sqlite3.connect('password_manager.db')
c = conn.cursor()

# Tablo oluşturma
 
c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY, 
             website TEXT NOT NULL, 
             username TEXT NOT NULL, 
             password TEXT NOT NULL)''')
conn.commit()

# Şifreyi güvenli bir şekilde saklamak için hash fonksiyonunu kullandık 

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Yeni şifre ekleme fonksiyonu

def add_password(website, username, password):
    hashed_password = hash_password(password)
    c.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)", (website, username, hashed_password))
    conn.commit()

# Şifre güncelleme fonksiyonu

def update_password(id, new_password):
    hashed_password = hash_password(new_password)
    c.execute("UPDATE passwords SET password = ? WHERE id = ?", (hashed_password, id))
    conn.commit()

# Şifre silme fonksiyonu

def delete_password(id):
    c.execute("DELETE FROM passwords WHERE id = ?", (id,))
    conn.commit()

# Tüm şifreleri getirme fonksiyonu

def get_all_passwords():
    c.execute("SELECT * FROM passwords")
    return c.fetchall()

# Rastgele güçlü şifre oluşturma fonksiyonu

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Kullanıcı arayüzü

def main():
    while True:
        print("\n1. Şifre Ekle")
        print("2. Tüm Şifreleri Görüntüle")
        print("3. Şifre Güncelle")
        print("4. Şifre Sil")
        print("5. Rastgele Şifre Oluştur")
        print("6. Çıkış")
        choice = input("Seçiminizi yapın: ")

        if choice == '1':
            website = input("Web sitesi adı: ")
            username = input("Kullanıcı adı: ")
            password = getpass.getpass("Şifre: ")
            add_password(website, username, password)
            print("Şifre başarıyla eklendi!")
        elif choice == '2':
            passwords = get_all_passwords()
            if passwords:
                print("\nTüm Şifreler:")
                for password in passwords:
                    print(f"ID: {password[0]}, Website: {password[1]}, Kullanıcı adı: {password[2]}, Şifre: {password[3]}")
            else:
                print("Henüz hiç şifre eklenmemiş.")
        elif choice == '3':
            id = int(input("Güncellemek istediğiniz şifrenin ID'si: "))
            new_password = getpass.getpass("Yeni Şifre: ")
            update_password(id, new_password)
            print("Şifre başarıyla güncellendi!")
        elif choice == '4':
            id = int(input("Silmek istediğiniz şifrenin ID'si: "))
            delete_password(id)
            print("Şifre başarıyla silindi!")
        elif choice == '5':
            length = int(input("Şifre uzunluğu: "))
            password = generate_password(length)
            print(f"Rastgele Şifre: {password}")
        elif choice == '6':
            break
        else:
            print("Geçersiz seçim!")

    conn.close()

if __name__ == "__main__":
    main()
