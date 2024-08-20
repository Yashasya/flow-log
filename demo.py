import csv
from collections import defaultdict

def parse_lookup_table(file_path):
    lookup_table = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Normalize protocol and port to lowercase for case-insensitive matching
            key = (row['dstport'], row['protocol'].lower())
            lookup_table[key] = row['tag']
    return lookup_table

def parse_protocol(file_path):
    prot_table = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            key = row["Decimal"]
            val = row["Keyword"]
            prot_table[key] = val
    return prot_table


def parse_flow_log(file_path,prot_table):
    flow_logs = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                parts = line.split()
                # Extract relevant fields: dstport (7th field), protocol (8th field)
                if parts[6] == "dstport":
                    continue
                dstport = parts[6]
                protocol = 'unknown'
                if parts[7] in prot_table.keys():
                    protocol = prot_table[parts[7]].lower()
                flow_logs.append((dstport, protocol))
    return flow_logs

def generate_tag_counts(flow_logs, lookup_table):
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)

    for dstport, protocol in flow_logs:
        tag = lookup_table.get((dstport, protocol), "Untagged")
        tag_counts[tag] += 1
        port_protocol_counts[(dstport, protocol)] += 1

    return tag_counts, port_protocol_counts

def write_output(tag_counts, port_protocol_counts, output_file):
    with open(output_file, 'w') as file:
        # Write tag counts
        file.write("Tag Counts:\nTag,Count\n")
        for tag, count in tag_counts.items():
            file.write(f"{tag},{count}\n")

        # Write port/protocol combination counts
        file.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n")
        for (port, protocol), count in port_protocol_counts.items():
            file.write(f"{port},{protocol},{count}\n")

def main():
    lookup_table_file = 'lookup.csv'  # Path to your lookup table CSV file
    flow_log_file = 'yshah.log'  # Path to your flow log file
    prot_table_file = 'protocol.csv' # Path to your Protocol CSV File
    output_file = 'output.csv'  # Path to the output file

    # Parse lookup table and flow logs
    lookup_table = parse_lookup_table(lookup_table_file)
    prot_table = parse_protocol(prot_table_file)
    flow_logs = parse_flow_log(flow_log_file,prot_table)
    
    # Generate counts
    tag_counts, port_protocol_counts = generate_tag_counts(flow_logs, lookup_table)

    # Write output to file
    write_output(tag_counts, port_protocol_counts, output_file)

if __name__ == "__main__":
    main()
