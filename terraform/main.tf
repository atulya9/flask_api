terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file("dummy.json")

  project = "new-project-lummo"
  region  = "us-central1"
  zone    = "us-central1-a"
}

resource "google_compute_instance" "vm_instance" {
  name         = "lummo-test-instance"
  machine_type = "e2-micro"
  zone = "us-central1-a"
  tags = ["http-server-8090","http-server","https-server"]


  boot_disk {
    auto_delete = "true"

    initialize_params {
      image = "projects/cos-cloud/global/images/cos-stable-97-16919-103-22"
      size = "10"
    }
  }

  labels = {
    container-vm = "cos-stable-97-16919-103-22"
  }

  network_interface {
    network = "default"
    access_config {
      network_tier = "PREMIUM"
    }
  }

  service_account {
    email  = "130925902413-compute@developer.gserviceaccount.com"
    scopes = ["https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring.write","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append"]
  }

  metadata = {
    gce-container-declaration = "spec:\n  containers:\n    - name: lummo-test-instance\n      image: docker.io/atulyatibrewal/lummo-repo:latest\n      stdin: false\n      tty: false\n  restartPolicy: Always\n\n# This container declaration format is not public API and may change without notice. Please\n# use gcloud command-line tool or Google Cloud Console to run Containers on Google Compute Engine."
    google-logging-enabled    = "true"
  }

  metadata_startup_script = "docker run -p 8090:8090 atulyatibrewal/lummo-repo:latest"
}