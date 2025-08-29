CI Pipeline (GitHub Actions)

This repository includes a CI workflow at `.github/workflows/ci.yml` which:

- Builds backend and frontend images
- Loads images into Minikube in the runner
- Applies Kubernetes manifests to Minikube

Required repository secrets (see `.github/secrets.example`):

- POSTGRES_PASSWORD — password used to initialize Postgres in k8s
- GF_SECURITY_ADMIN_PASSWORD — Grafana admin password

Notes and tips

- The workflow uses Minikube on the runner; ensure the runner has Docker (GitHub-hosted does) and allow ~5-10 minutes for Minikube startup.
- For production deployment, replace the Minikube steps with a cloud-provider deployment flow and use a proper kubeconfig or OIDC. Note: this repository provides local Minikube manifests and CI steps that run Minikube in the runner; it does not include provider-specific cloud hosting configurations out of the box.
