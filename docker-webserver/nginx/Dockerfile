# nginx/Dockerfile
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

HEALTHCHECK --interval=30s --timeout=5s \
  CMD wget -q --spider http://localhost/nginx-health || exit 1

EXPOSE 80