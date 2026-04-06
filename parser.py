import re
from datetime import datetime

iso_pattern = re.compile(
        r'^(\S+)\s+(\S+)\s+([^\[\s]+)(?:\[(\d+)\])?:\s+(.*)'
        )
journal_pattern = re.compile(
        r'^([A-Z][a-z]{2}\s+\d+\s+\d+:\d+:\d+)\s+(\S+)\s+([^\[]+)\[(\d+)\]:\s+(.*)'
        )
def parse_log(line):
    match = iso_pattern.match(line)
    if match: 
        return {
            "timestamp": datetime.fromisoformat(match.group(1)).timestamp(),
            "host": match.group(2),
            "process": match.group(3),
            "pid": match.group(4),
            "message": match.group(5),
        }
    match = journal_pattern.match(line)
    if match:
        return {
                "timestamp": datetime.now().timestamp(),
                "host": match.group(2),
                "process": match.group(3).strip(),
                "pid": match.group(4),
                "message": match.group(5),
                }
    return None

##if __name__ == "__main__":
    ##test_line = "2026-04-05T01:15:18.115163+00.00 linux systemd[1]: logrotate.service: Deactivated successfully."

    ##result = parse_log(test_line)
   ## print(result)
