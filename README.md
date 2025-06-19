# autoSSL_renewal_Proxmox_python
The script is used to automatically renew the SSL certificate (LE) for a domain assigned to Proxmox.
Automatic execution of the script can be set as a cron job:
<p> 0 9 * * * root python3 renewal.py -d DOMAIN </p>
