import subprocess
import logging
import random
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
    if ((args.premade == None) and (args.iso == None)):
        logger.error("You need to either specify --premade or at least --iso in a custom installation")
        sys.exit(2)

    if (args.NAME == None):
        logger.error("You need to specify a name!")
        sys.exit(3)

    name    = args.NAME if (args.group == None) else "{}-{}".format(args.group, args.NAME)
    iso     = None
    cpus    = config["install-defaults"]["cpus"]
    cpucap  = config["install-defaults"]["cpucap"]
    memory  = config["install-defaults"]["memory"]
    vram    = config["install-defaults"]["vram"]
    disk    = config["install-defaults"]["disk"]
    ostype  = config["install-defaults"]["ostype"]
    netif   = config["install-defaults"]["network-adapter"]
    vrde    = config["install-defaults"]["vrde"]
    vrdeport= None

    if (name in get_all_machines()):
        logger.error("The specified name '{}' already exists".format(name))
        sys.exit(4)

    if (args.premade != None):
        if (args.premade not in config["premade-install"]):
            logger.error("The premade collection '{}' was not found in config".format(args.premade))
            sys.exit(5)

        if ("iso" in config["premade-install"][args.premade]):              iso     = config["premade-install"][args.premade]["iso"]
        if ("cpus" in config["premade-install"][args.premade]):             cpus    = config["premade-install"][args.premade]["cpus"]
        if ("cpucap" in config["premade-install"][args.premade]):           cpucap  = config["premade-install"][args.premade]["cpucap"]
        if ("memory" in config["premade-install"][args.premade]):           memory  = config["premade-install"][args.premade]["memory"]
        if ("vram" in config["premade-install"][args.premade]):             vram    = config["premade-install"][args.premade]["vram"]
        if ("disk" in config["premade-install"][args.premade]):             disk    = config["premade-install"][args.premade]["disk"]
        if ("ostype" in config["premade-install"][args.premade]):           ostype  = config["premade-install"][args.premade]["ostype"]
        if ("network-adapter" in config["premade-install"][args.premade]):  netif   = config["premade-install"][args.premade]["network-adapter"]
        if ("vrde" in config["premade-install"][args.premade]):             vrde    = config["premade-install"][args.premade]["vrde"]
        if ("vrde-port" in config["premade-install"][args.premade]):        vrdeport= config["premade-install"][args.premade]["vrde-port"]

    if (args.iso != None):      iso     = args.iso
    if (args.cpus != None):     cpus    = args.cpus
    if (args.cpu_limit != None):cpucap  = args.cpu_limit
    if (args.memory != None):   memory  = args.memory
    if (args.vram != None):     vram    = args.vram
    if (args.disk != None):     disk    = args.disk
    if (args.os_type != None):  ostype  = args.os_type
    if (args.netif != None):    netif   = args.networkadapter
    if (args.vrde != None):     vrde    = args.vrde
    if (args.vrde_port != None):vrdeport= args.vrde_port

    if (vrde and (vrdeport == None)): vrdeport = random.randint(1050, 65500)
    path = "{}/{}/{}".format(config["virt-root"], config["vbox-dir"], name)
    verbose = "" if logger.isEnabledFor(logging.INFO) else "1>/dev/null"

    logger.info("Creating a new VM...")
    logger.info("Path       : {}".format(path))
    logger.info("Name       : {}".format(name))
    logger.info("Memory     : {}MB".format(memory))
    logger.info("VRAM       : {}MB".format(vram))
    logger.info("CPUs       : {}".format(cpus))
    logger.info("CPU limit  : {}%".format(cpucap))
    logger.info("Disk       : {}MB".format(disk))
    logger.info("Network    : {}".format(netif))
    logger.info("VRDE       : {}".format("on" if vrde else "off"))
    logger.info("VRDE port  : {}".format(vrdeport if vrde else "-"))
    logger.info("OS type    : {}".format(ostype))
    logger.info("Install ISO: {}".format(iso))
    logger.info("Start      : {}".format("yes" if (not args.no_start) else "no"))

    subprocess.call("mkdir -p {} {}".format(path, verbose), shell=True)

    subprocess.call("{} createhd --filename {}/{}.vdi --size {} {} 2>&1".format(CMD, path, name, disk, verbose), shell=True) # Geniuses output everything to stderr so goodbye error messages!
    subprocess.call("{} createvm --name {} --ostype {} --register {}".format(CMD, name, ostype, verbose), shell=True)

    subprocess.call("{} storagectl {} --name SATAController --add sata --controller IntelAHCI {}".format(CMD, name, verbose), shell=True)
    subprocess.call("{} storagectl {} --name IDEController --add ide {}".format(CMD, name, verbose), shell=True)

    subprocess.call("{} storageattach {} --storagectl SATAController --port 0 --device 0 --type hdd      --medium {}/{}.vdi {}".format(CMD, name, path, name, verbose), shell=True)
    subprocess.call("{} storageattach {} --storagectl IDEController  --port 0 --device 0 --type dvddrive --medium {} {}".format(CMD, name, iso, verbose), shell=True)

    subprocess.call("{} modifyvm {} --ioapic on --boot1 dvd --boot2 disk --boot3 none --boot4 none {}".format(CMD, name, verbose), shell=True)
    subprocess.call("{} modifyvm {} --memory {} --vram {} {}".format(CMD, name, memory, vram, verbose), shell=True)
    subprocess.call("{} modifyvm {} --cpus {} --cpuexecutioncap {} {}".format(CMD, name, cpus, cpucap, verbose), shell=True)
    subprocess.call("{} modifyvm {} --nic1 bridged --bridgeadapter1 {} {}".format(CMD, name, netif, verbose), shell=True)
    if (vrde): subprocess.call("{} modifyvm {} --vrde on --vrdeport {} {}".format(CMD, name, vrdeport, verbose), shell=True)

    if (not args.no_start): subprocess.call("{} startvm {} --type headless {}".format(CMD, name, verbose), shell=True)

def destroy(args, config, logger):
    unimplemented(args, config, logger)

def start(args, config, logger):
    unimplemented(args, config, logger)

def stop(args, config, logger):
    unimplemented(args, config, logger)

def eject_install_medium(args, config, logger):
    unimplemented(args, config, logger)


def get_all_machines(group=None):
    output = subprocess.check_output("{} list vms".format(CMD), shell=True)
    return filter(lambda x: re.match("{}-".format(group), x) if (group != None) else lambda x: True, map(lambda x: x.strip('"'), re.findall('".*?"', output)))

def get_running_machines(group=None):
    output = subprocess.check_output("{} list runningvms".format(CMD), shell=True)
    return filter(lambda x: re.match("{}-".format(group), x) if (group != None) else lambda x: True, map(lambda x: x.strip('"'), re.findall('".*?"', output)))
