docker pull dpage/pgadmin4
docker run --name "postgres" \
    -e "PGADMIN_DEFAULT_EMAIL=1282594929@qq.com" \
    -e "PGADMIN_DEFAULT_PASSWORD=postgres" \
    -e "SCRIPT_NAME=/pgadmin4" \
    -l "traefik.frontend.rule=PathPrefix:/pgadmin4" \
    -d dpage/pgadmin4
