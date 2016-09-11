config = {
    "app-name":         "vbox-infra-ctl",

    "virt-root":        "/home/virt",
    "vbox-dir":         "vbox",

    "log-file-enabled": True,
    "log-file-path":    "/tmp/vbox-infra.log",

    "premade-install": {
        "centos-7-minimal": {
            "ostype":           "Linux24_64",
            "iso":              "/opt/virt/os-images/CentOS-7-x86_64-Minimal-1511.iso",
            "memory":           512,
            "disk":             5120,
            "network-adapter":  "enp0s25",
            "vrde":             True
        }
    },

    "install-defaults": {
        "cpus":             1,
        "cpucap":           100,
        "ostype":           "Linux_64",
        "memory":           1024,
        "vram":             32,
        "disk":             5120,
        "network-adapter":  "eth0",
        "vrde":             True
    }
}

def get_config():
    return config
