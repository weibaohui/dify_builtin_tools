FROM bitnami/kubectl:latest as kubectl
FROM langgenius/dify-api:0.6.11
COPY --from=kubectl /opt/bitnami/kubectl/bin/kubectl /usr/bin/kubectl
