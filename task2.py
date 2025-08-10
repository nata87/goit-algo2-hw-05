import re
import time
import hyperloglog

def load_ip_addresses(filename):
    ip_pattern = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
    ips = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            match = ip_pattern.search(line)
            if match:
                ips.append(match.group())
    return ips

def count_unique_exact(ips):
    return len(set(ips))

def count_unique_hll(ips):
    hll = hyperloglog.HyperLogLog(0.01)  
    for ip in ips:
        hll.add(ip)
    return len(hll)

def compare_methods(ips):
    start = time.time()
    exact_count = count_unique_exact(ips)
    exact_time = time.time() - start

    start = time.time()
    hll_count = count_unique_hll(ips)
    hll_time = time.time() - start

    print("Результати порівняння:")
    print(f"{'':25} {'Точний підрахунок':20} {'HyperLogLog'}")
    print(f"{'Унікальні елементи':25} {exact_count:<20} {hll_count}")
    print(f"{'Час виконання (сек.)':25} {exact_time:<20.5f} {hll_time:.5f}")


if __name__ == "__main__":
    ip_list = load_ip_addresses("lms-stage-access.log")
    compare_methods(ip_list)
