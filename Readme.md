# Flow Log Tagging and Analysis

This program parses flow log data and maps each row to a tag based on a lookup table. The flow logs are processed to count occurrences of each tag and track how often specific port/protocol combinations appear. The lookup table defines tags using a combination of destination ports and protocols.

## Problem Statement

The goal is to read and process flow log data, tag the logs based on predefined mappings from a lookup table, and generate statistics for both tag counts and port/protocol combinations.

### Flow Log Format (Version 2)

Flow logs are assumed to be in the default format (version 2), as specified in the [AWS Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html). An example flow log line:

2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 49153 6 25 20000 1620140761 1620140821 ACCEPT OK

### Lookup Table Format

The lookup table is a CSV file with the following columns:

- dstport: The destination port number.
- protocol: The protocol name (e.g., tcp, udp).
- tag: The tag to apply when the dstport and protocol match.

An example lookup table:

| dstport | protocol | tag   |
| ------- | -------- | ----- |
| 25      | tcp      | sv_P1 |
| 443     | tcp      | sv_P2 |
| 110     | tcp      | email |
| 993     | tcp      | email |

### Assumptions

- The program only supports logs in the default format and version 2.
- Matching is case-insensitive.
- Logs with no matching tag in the lookup table are labeled as "Untagged."
- Port/protocol mappings are unique in the lookup table.
- The protocol is looked up using a protocol.csv file containing protocol mappings (e.g., 6 -> tcp).

### Input Files

- Flow Log File (yshah.log): Contains flow log entries. It also works on a .txt file just replace the path.
- Lookup Table File (lookup.csv): Maps dstport and protocol to tags.
- Protocol Table File (protocol.csv): Maps protocol numbers to protocol names.

### Output File

The output is generated as a CSV file (output.csv) containing:

- Tag Counts: Number of flow logs assigned to each tag.
- Port/Protocol Combination Counts: Frequency of each unique port/protocol combination.

### Instructions to Run

1. Ensure the following input files are present in the same directory:

- yshah.log: Flow log file
- lookup.csv: Lookup table file
- protocol.csv: Protocol table file

2. If the name of the files vary from the above name then you need to modify the
3. Run the program: `python flow_log_parser.py`
4. The output will be saved as output.csv in the same directory.

## Code Explanation

### Functions

- parse_lookup_table(file_path): Reads the lookup table and returns a dictionary mapping (dstport, protocol) to a tag.
- parse_protocol(file_path): Reads the protocol table and maps protocol numbers to names.
- parse_flow_log(file_path, prot_table): Reads the flow logs, extracting the relevant fields (dstport, protocol) and returns them for tagging.
- generate_tag_counts(flow_logs, lookup_table): Generates counts for tags and port/protocol combinations.
- write_output(tag_counts, port_protocol_counts, output_file): Writes the counts to the output file.

### Tests

- The Program was tested based on the sample VPC Log Data from one of my AWS Account.
- Test cases include scenarios with both matching and non-matching tags.
