import subprocess
import argparse
import datetime
import sys

# Function to log events to a file with a timestamp
def log_event(message):
    with open("/var/log/renewal_script", "a") as log_file:
        log_file.write(f"[{datetime.datetime.now()}] {message}\n")

# Function to check if the certificate for a given domain is close to expiry
def check_certificate_validity(domain):
    try:
        # Run certbot to check certificate details
        result = subprocess.run(
            ["certbot", "certificates", "-d", domain],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Check if the certificate validity is between 1 and 7 days
        return any(
            f"VALID: {i} days" in result.stdout for i in range(1, 8)
        )
    except Exception as e:
        # Log and exit if an error occurs during the check
        log_event(f"Error checking certificate validity for {domain}: {str(e)}")
        sys.exit(1)

# Function to renew the SSL certificate and update necessary files
def renew_certificate(domain):
    try:
        # Request a new certificate from certbot
        subprocess.run([
            "certbot", "certonly", "--standalone", "-d", domain,
            "--non-interactive", "--agree-tos", "--email", "alarmy@dataspace.pl",
            "--force-renewal"
        ], check=True)

        # Copy the new certificate to the required locations
        subprocess.run([
            "cp", f"/etc/letsencrypt/live/{domain}/fullchain.pem",
            "/etc/pve/nodes/node-01/pveproxy-ssl.pem"
        ], check=True)

        subprocess.run([
            "cp", f"/etc/letsencrypt/live/{domain}/privkey.pem",
            "/etc/pve/nodes/node-01/pveproxy-ssl.key"
        ], check=True)

        # Restart the pveproxy service to apply the new certificate
        subprocess.run(["systemctl", "restart", "pveproxy"], check=True)

        # Log the successful renewal
        log_event(f"SSL Certificate for {domain} properly renewed.")
    except subprocess.CalledProcessError as e:
        # Log and exit if an error occurs during the renewal process
        log_event(f"Error during certificate renewal for {domain}: {str(e)}")
        sys.exit(1)

# Main function to parse arguments and perform actions
def main():
    parser = argparse.ArgumentParser(description="Renew SSL certificates.")
    # Define the domain argument
    parser.add_argument("-d", "--domain", required=True, help="Domain to check and renew certificate for.")

    args = parser.parse_args()
    domain = args.domain

    # Check if the certificate is close to expiry and renew if necessary
    if check_certificate_validity(domain):
        renew_certificate(domain)
        sys.exit(0)
    else:
        # Log and print a message if renewal is not needed
        message = f"Certificate for {domain} not yet due for renewal."
        print(message)
        log_event(message)
        sys.exit(1)

if __name__ == "__main__":
    main()
