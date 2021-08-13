from django.conf.urls import url
import useradmin.views


urlpatterns = [
    url('index/', useradmin.views.index),
    url('getmysqldata/', useradmin.views.datatables),
    url('deletemysqldate/', useradmin.views.deletedata),
    url('addmysqldate/', useradmin.views.adddata),
    url('addhostdate/', useradmin.views.addhost),
    url('deletehostdate/', useradmin.views.deletehost),
    url('findhostdate/', useradmin.views.findhostdate),
    url('sendcommand/', useradmin.views.ssh_command),
]