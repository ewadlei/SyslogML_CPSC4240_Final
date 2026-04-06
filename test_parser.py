from parser import parse_log

parsed_count = 0
failed_count = 0
failed_lines = []

with open("/var/log/syslog") as f:
    for line in f:
        result = parse_log(line)
        if result:
            parsed_count += 1
        else:
            failed_lines.append(line.strip())
            failed_count += 1

print("Parsed lines:", parsed_count)
print("Failed lines:", failed_count)
print("Failed lines:")
for line in failed_lines:
    print(line)
