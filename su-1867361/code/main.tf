terraform {
  required_version = ">= 1.6.0"
  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = "=3.0.1-rc6"
    }
  }
}

provider "proxmox" {
  pm_api_url   = "https://192.168.1.130:8006/api2/json"
  pm_tls_insecure = true
  pm_api_token_id = var.pm_api_token_id
  pm_api_token_secret = var.pm_api_token_secret
  pm_debug = true
  #pm_log_enable = "true"
}

resource "proxmox_vm_qemu" "sambavmtest" {
  name        = "vm${count.index + 1}"
  count       = 2
  target_node = "node5"
  agent       = 1
  cores       = 2
  memory      = 2096
  boot        = "order=scsi0"
  clone       = "debian12-cloudinit"
  full_clone  = false
  scsihw      = "virtio-scsi-single"
  vm_state    = "running"
  automatic_reboot = true

  # cloud-init config
  cicustom   = "vendor=local:snippets/qemu-guest-agent.yml" # /var/lib/vz/snippets/qemu-guest-agent.yml
  ciupgrade  = true
  nameserver = "192.168.1.150"
  searchdomain = " "
  ipconfig0  = "ip=192.168.1.${count.index + 171}/24,gw=192.168.1.1"
  skip_ipv6  = true
  ciuser     = var.ciuser
  cipassword = var.cipassword
  sshkeys    = var.sshkeys

  # Most cloud-init images require a serial device for their display
  serial {
    id = 0
  }

  disks {
    scsi {
      scsi0 {
        disk {
          storage = "local-zfs"
          size    = "4G"
        }
      }
    }
    ide {
      ide1 {
        cloudinit {
          storage = "local-zfs"
        }
      }
    }
  }

  network {
    id = 0
    bridge = "vmbr0"
    model  = "virtio"
  }
}


variable "pm_api_token_id" {
  type     = string
  nullable = false
}
variable "pm_api_token_secret" {
  type     = string
  nullable = false
}
variable "sshkeys" {
  type     = string
  nullable = false
}
variable "ciuser" {
  type     = string
  nullable = false
}
variable "cipassword" {
  type     = string
  nullable = false
}

