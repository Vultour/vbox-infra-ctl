import argparse


def get_arguments():
    return define_arguments().parse_args()
    
def define_arguments(driver, list_cb, create_cb, destroy_cb, start_cb, stop_cb):
    parser = argparse.ArgumentParser(
        prog="infra-ctl",
        description="Virtualization manager for small-scale environments, loaded driver: '{}'".format(driver),
    )

    parser.add_argument('--version', action='version', version='%(prog)s 0.1')
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Verbose output (repeat for more verbosity)")

    subparsers = parser.add_subparsers(title="Available subcommands")

    parser_list = subparsers.add_parser("list", help="List virtual machines")
    parser_list.add_argument("-a", "--all", action="store_true", help="List all virtual machines (not only running)")
    parser_list.add_argument("-g", "--group", help="Only list machines from a specified group")
    parser_list.set_defaults(func=list_cb)

    parser_create = subparsers.add_parser("create", help="Create a new virtual machine")
    parser_create.add_argument("NAME", help="Name of the new machine")
    parser_create.add_argument("-g", "--group", help="Add the machine to the specified group")
    parser_create.add_argument("-n", "--no-start", action="store_true", help="Do not power the machine on after provisioning")
    parser_create.set_defaults(func=create_cb)

    parser_destroy = subparsers.add_parser("destroy", help="Delete a virtual machine")
    parser_destroy.add_argument("NAME", help="Name of a virtual machine")
    parser_destroy.add_argument("--delete", action="store_true", help="Delete the machine's files as well (only unregisters the machine without this option)")
    parser_destroy.set_defaults(func=destroy_cb)

    parser_vm = subparsers.add_parser("vm", help="Control or modify an existing virtual machine")
    parser_vm.add_argument("NAME", help="Name of a virtual machine")
    parser_vm.add_argument("-g", "--group", action="store_true", help="Treat the supplied NAME as a group identifier")

    parser_vm_sub = parser_vm.add_subparsers(help="Available subcommands")
    parser_vm_sub.add_parser("start", help="Start a virtual machine").set_defaults(func=start_cb)

    parser_vm_stop = parser_vm_sub.add_parser("stop", help="Power off a virtual machine")
    parser_vm_stop_group = parser_vm_stop.add_mutually_exclusive_group(required=True)
    parser_vm_stop_group.add_argument("-p", "--poweroff", action="store_true", help="Issues a VirtualBox poweroff command")
    parser_vm_stop_group.add_argument("-c", "--clean", action="store_true", help="Cleanly shuts the machine down through SSH (requires working DNS and SSH keys)")
    parser_vm_stop.set_defaults(func=stop_cb)

    return parser
