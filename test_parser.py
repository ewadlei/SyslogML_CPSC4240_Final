from parser import parse_log

LOG_FILES = [
        "/var/log/syslog",
        "/var/log/auth.log",
        "/var/log/kern.log"
]

parsed_count = 0
failed_count = 0

for file in LOG_FILES:
    print(f"\nTesting file: {file}")

    try:
        with open(file) as f:
            for line in f:
                result = parse_log(line)
                if result:
                    parsed_count += 1
                else:
                    failed_count += 1
    except PermissionError:
        print(f"Permission denied: {file}")

print("\nTotal parsed:", parsed_count)
print("Total failed:", failed_count)
