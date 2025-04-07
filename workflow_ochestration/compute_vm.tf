terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.28.0"
    }
  }
}

provider "google" {
  project = "affable-hydra-455808-q0"
  region  = "us-central1"
  credentials = file(var.credentials)
}

resource "google_compute_instance" "ubuntu_test_1" {
  name         = "ubuntu-test-1"
  zone         = "us-central1-c"
  machine_type = "e2-medium"
  #   min_cpu_platform = "AMD Milan"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      size  = 30
      type  = "pd-standard"
    }
  }

  metadata = {
    enable-osconfig = "TRUE"
  }

  can_ip_forward      = false
  deletion_protection = false
  enable_display      = false

  network_interface {
    access_config {
      network_tier = "PREMIUM"
    }

    queue_count = 0
    stack_type  = "IPV4_ONLY"
    subnetwork  = "projects/affable-hydra-455808-q0/regions/us-central1/subnetworks/default"
  }
}