from django.db import models

# Create your models here.

class ssh_useradmin(models.Model):
    ssh_ip = models.CharField(max_length=20,default='')
    ssh_root = models.CharField(max_length=20)
    ssh_passwd = models.CharField(max_length=50)
    ssg_hostport = models.CharField(max_length=20)
    ssh_host_cloud_merchant = models.CharField(max_length=50)
    ssh_host_in_the_area = models.CharField(max_length=50)
    ssh_host_status_code = models.CharField(max_length=50, default=0)
    ssh_hsot_public_key = models.CharField(max_length=5200)
    ssh_hsot_private_key = models.CharField(max_length=5200)
    ssh_host_cpu = models.CharField(max_length=16)
    ssh_host_Memory = models.CharField(max_length=16)
    ssh_host_disk = models.CharField(max_length=16)
    ssh_host_system = models.CharField(max_length=50)
   

class useradmin_user(models.Model):
    user = models.CharField(max_length=20)
    user_email = models.CharField(max_length=20)
    user_level = models.CharField(max_length=20)
    user_ip = models.CharField(max_length=20,default='')
    user_passwd = models.CharField(max_length=50)
    user_hostport = models.CharField(max_length=20)
    user_area = models.CharField(max_length=50)
    user_Merchant = models.CharField(max_length=50)
    user_status = models.CharField(max_length=10)