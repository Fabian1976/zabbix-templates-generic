#! /usr/bin/python
#this script requires ovirt-engine-sdk-python
import sys
import pickle
pkl_filename = '/tmp/ovirt_stats.pkl'
vm_prefix = ''
vm_suffix = '_vm'

def write_pickle(obj):
    pkl_file = open(pkl_filename, 'wb')
    pickle.dump(obj, pkl_file)
    pkl_file.close()

def read_pickle():
    pkl_file = open(pkl_filename, 'rb')
    result = pickle.load(pkl_file)
    pkl_file.close()
    return result

def create_dict(api, vm_list):
    vm_dict = {}
    for vm in vm_list:
        vm_specs = {}
        vm_specs['cpu_cores'] = vm.get_cpu().get_topology().cores
        vm_specs['state'] = vm.get_status().state
        vm_specs['memory'] = vm.memory
        vm_specs['hypervisor'] = vm.get_display().address
        vm_specs['memory_guaranteed'] = vm.get_memory_policy().guaranteed
        #calculate total disksize
#        total_size = 0
#        for disk in api.vms.get(vm.name).get_disks().list():
#            try:
#                total_size+=disk.get_size()
#            except:
#                pass
#        vm_specs['total_disksize'] = total_size
        vm_dict[vm_prefix + vm.name + vm_suffix] = vm_specs
    write_pickle(vm_dict)
    return

def discover(URL, USERNAME, PASSWORD):
    from ovirtsdk.api import API
    from ovirtsdk.xml import params

    api = API(url=URL, username=USERNAME, password=PASSWORD,insecure=True)
    vm_list=api.vms.list()
    number_of_vms = len(vm_list)
    counter = 1
    result = '{\n\t"data":[\n'
    for vm in vm_list:
        if counter < number_of_vms:
            result += '\t\t{ "{#VMNAME}":"%s%s%s" },\n' % (vm_prefix, vm.name, vm_suffix)
        else:
            result += '\t\t{ "{#VMNAME}":"%s%s%s" }\n' % (vm_prefix, vm.name, vm_suffix)
        counter += 1
    result += '\t]\n}'
    create_dict(api, vm_list)
    return result

def get_vm_stats(vm_name, action):
    vm_stats = read_pickle()
    return vm_stats[vm_name][action]

def main():
    if len(sys.argv) < 3:
        print 'ZBX_NOTSUPPORTED: Too few parameters. <ovirtmanager-url> <username> <password> [<servername>] [<check>]'
        sys.exit(1)
    URL = 'https://%s:443/api' % sys.argv[1]
    USERNAME = '%s@internal' % sys.argv[2]
    PASSWORD = sys.argv[3]

    try:
        vm_name = sys.argv[4]
        action = sys.argv[5]
        print get_vm_stats(vm_name, action)
    except:
        vm_name = None
        action = 'discover'
        print discover(URL, USERNAME, PASSWORD)

if __name__ == '__main__':
    main()
