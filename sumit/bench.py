import subprocess
import time
import frappe

#create a new site and allocate ssl certificate
@frappe.whitelist()
def new_site():
   
        mariad_password = "creative mind"
        site_name = "sitgrrjfeee1dsfd.local"
        admin_password = "admin"
        #nes site
        p = subprocess.Popen(["bench", "new-site", site_name, "--mariadb-root-password", mariad_password, "--admin-password", admin_password],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #add site nginx port
        out, err = p.communicate()
        if p.returncode == 0:
            return out, err
        else:
            return "Error: " + err + "Output: " + out

   