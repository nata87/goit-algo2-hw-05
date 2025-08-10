import mmh3

class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, item):
        """Додає елемент у фільтр"""
        if not isinstance(item, str):
            item = str(item)
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            self.bit_array[index] = 1

    def contains(self, item):
        """Перевіряє, чи є елемент у фільтрі"""
        if not isinstance(item, str):
            item = str(item)
        for i in range(self.num_hashes):
            index = mmh3.hash(item, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True


def check_password_uniqueness(bloom_filter, passwords):
    """Перевіряє список паролів на унікальність"""
    results = {}
    for pwd in passwords:
        if not pwd: 
            results[pwd] = "некоректний пароль"
        elif bloom_filter.contains(pwd):
            results[pwd] = "вже використаний"
        else:
            bloom_filter.add(pwd)
            results[pwd] = "унікальний"
    return results


if __name__ == "__main__":

    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords = ["password123", "newpassword", "admin123", "guest", ""]
    results = check_password_uniqueness(bloom, new_passwords)

    for pwd, status in results.items():
        print(f"Пароль '{pwd}' — {status}.")
