from vmmanager import VMManager

s = VMManager('https://shost2.g-host.ru:1500/vmmgr', 'web_service', 'F7h7G2o1')
# print(s.get_hosts())
# print(s.get_host_usedmem(2))
# print(s.send_request('vmhostnode.edit', dict(elid=2)))
# print(s.get_host(1))
# print(s.change_owner(133, 7))
# print(s.vm_remove(133))
# print(s.vm_reinstall(131, None, None, 'CentOS7New'))
# print(s.send_request('vm.reinstall', dict(elid=131)))
# print(s.vm_change_pass(131, 'TestTestTest'))
# print(s.create_vm('test_vm', 5, 2, 'ISPsystem__CentOS-7-amd64', 'null', 'CentOS7', 'test-vm.g-host.ru', 4000, 1000, 2,
#                   'TestPassword', 'localtime'))
# print(s.enable_user(5))
# print(s.create_user('test_api'))
# print(s.get_vnc_url(130, 'test'))
# print(s.vm_start(133))
# print(s.vm_stop(133))
