import subprocess
import sys
import re


CMD = "vboxmanage"


def driver_info():
    return "VirtualBox using vboxmanage [linux only]"

def driver_test(logger):
    if (subprocess.call("{} --version 1>/dev/null 2>&1".format(CMD), shell=True) == 0):
        logger.debug("Driver test successful")
    else:
        logger.error("Driver test unsuccessful, make sure you can run the command '{}'".format(CMD))
        sys.exit(1)


def unimplemented(args, config, logger):
    logger.error("The infra-ctl VirtualBox driver does not implement this operation")

def list(args, config, logger):
    if (args.all):
        machines = get_all_machines(args.group)
        if (len(machines) < 1):
            print "No known virtual machines"
        else:
            print "All known virtual machines:"
            machines.sort()
            for machine in machines:
                print " - {}".format(machine)
    else:
        machines = get_running_machines()
        if (len(machines) < 1):
            print "No running virtual machines"
        else:
            print "All running virtual machines:"
            machines.sort()
            for machine in machines:
                print " - {}".format(machine)

def create(args, config, logger):
    unimplemented(args, config, logger)

def destroy(args, config, logger):
    unimplemented(args, config, logger)

def start(args, config, logger):
    unimplemented(args, config, logger)

def stop(args, config, logger):
    unimplemented(args, config, logger)

def eject_install_medium(args, config, logger):
    unimplemented(args, config, logger)


def get_all_machines(group):
    output = subprocess.check_output("{} list vms".format(CMD), shell=True)
    return filter(lambda x: re.match("{}-".format(group), x) if (group != None) else lambda x: True, map(lambda x: x.strip('"'), re.findall('".*?"', output)))

def get_running_machines():
    output = subprocess.check_output("{} list runningvms".format(CMD), shell=True)
    return filter(lambda x: re.match("{}-".format(group), x) if (group != None) else lambda x: True, map(lambda x: x.strip('"'), re.findall('".*?"', output)))
