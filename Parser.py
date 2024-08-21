import csv
from collections import defaultdict
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger()

def parse_lookup_table(file_path):
    """
    Parses the lookup table CSV file to create a mapping of (dstport, protocol) to tags.

    Args:
        file_path (str): Path to the lookup table CSV file.

    Returns:
        dict: A dictionary with keys as (dstport, protocol) tuples and values as the associated tag.
    """
    lookup_table = {}
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = (row['dstport'], row['protocol'].lower())
                lookup_table[key] = row['tag']
        logger.info(f"Successfully parsed lookup table from {file_path}")
    except Exception as e:
        logger.error(f"Error parsing lookup table file {file_path}: {e}")
        raise
    return lookup_table

def parse_protocol(file_path):
    """
    Parses the protocol CSV file to create a mapping of protocol numbers to their corresponding names.

    Args:
        file_path (str): Path to the protocol CSV file.

    Returns:
        dict: A dictionary mapping protocol numbers (as strings) to their corresponding protocol names (as strings).
    """
    prot_table = {}
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                key = row["Decimal"]
                val = row["Keyword"]
                prot_table[key] = val
        logger.info(f"Successfully parsed protocol table from {file_path}")
    except Exception as e:
        logger.error(f"Error parsing protocol table file {file_path}: {e}")
        raise
    return prot_table


def parse_flow_log(file_path,prot_table):
    """
    Parses the flow log file to extract dstport and protocol fields.

    Args:
        file_path (str): Path to the flow log file.
        prot_table (dict): A dictionary mapping protocol numbers to protocol names.

    Returns:
        list: A list of tuples, each containing (dstport, protocol) for each flow log entry.
    """
    flow_logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.split()
                    if parts[6] == "dstport":
                        continue
                    dstport = parts[6]
                    protocol = 'unknown'
                    if parts[7] in prot_table.keys():
                        protocol = prot_table[parts[7]].lower()
                    flow_logs.append((dstport, protocol))
        logger.info(f"Successfully parsed flow logs from {file_path}")
    except Exception as e:
        logger.error(f"Error parsing flow log file {file_path}: {e}")
        raise
    return flow_logs

def generate_tag_counts(flow_logs, lookup_table):
    """
    Generates counts for tags based on the lookup table and counts for port/protocol combinations.

    Args:
        flow_logs (list): A list of tuples containing (dstport, protocol) for each flow log entry.
        lookup_table (dict): A dictionary mapping (dstport, protocol) tuples to tags.

    Returns:
        tuple: A dictionary with tag counts and a dictionary with port/protocol combination counts.
    """
    tag_counts = defaultdict(int)
    port_protocol_counts = defaultdict(int)
    try:
        for dstport, protocol in flow_logs:
            tag = lookup_table.get((dstport, protocol), "Untagged")
            tag_counts[tag] += 1
            port_protocol_counts[(dstport, protocol)] += 1
        logger.info("Successfully generated tag and port/protocol combination counts")
    
    except Exception as e:
        logger.error(f"Error generating tag counts: {e}")
        raise

    return tag_counts, port_protocol_counts

def write_output(tag_counts, port_protocol_counts, output_file):
    """
    Writes the output of tag counts and port/protocol combination counts to a CSV file.

    Args:
        tag_counts (dict): A dictionary with tags as keys and their counts as values.
        port_protocol_counts (dict): A dictionary with (dstport, protocol) tuples as keys and their counts as values.
        output_file (str): Path to the output CSV file.
    """
    try:
        with open(output_file, 'w') as file:
            
            file.write("Tag Counts:\nTag,Count\n")
            for tag, count in tag_counts.items():
                file.write(f"{tag},{count}\n")

            
            file.write("\nPort/Protocol Combination Counts:\nPort,Protocol,Count\n")
            for (port, protocol), count in port_protocol_counts.items():
                file.write(f"{port},{protocol},{count}\n")
        logger.info(f"Successfully wrote output to {output_file}")
    except Exception as e:
        logger.error(f"Error writing output to {output_file}: {e}")
        raise

def main():
    lookup_table_file = 'data/input/lookup.csv'  # Path to your lookup table CSV file
    flow_log_file = 'data/input/yshah.log'  # Path to your flow log file
    prot_table_file = 'data/input/protocol.csv' # Path to your Protocol CSV File
    output_file = 'data/output/output.csv'  # Path to the output file

    # Parse lookup table, protocol table and flow logs
    lookup_table = parse_lookup_table(lookup_table_file)
    prot_table = parse_protocol(prot_table_file)
    flow_logs = parse_flow_log(flow_log_file,prot_table)
    
    # Generate counts
    tag_counts, port_protocol_counts = generate_tag_counts(flow_logs, lookup_table)

    # Write output to file
    write_output(tag_counts, port_protocol_counts, output_file)

if __name__ == "__main__":
    main()
