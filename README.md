# autoSSL_renewal_Proxmox_python
A Python script for automatic SSL certificate renewal (Let's Encrypt) for a domain assigned to a Proxmox server.
It checks if the certificate is expiring within 7 days and, if so, renews it, replaces the active certificate files, and restarts the pveproxy service. </br>
You can automate execution using a cron job. For example, to run the script daily at 9:00 AM:
<p> 0 9 * * * root python3 renewal.py -d DOMAIN </p>
