#!/bin/bash

# Generate custom secret
secret_generator() {
    python -c 'import secrets; print(secrets.token_urlsafe(16))'
}

# Create .env and add a base variables
(
    echo '# Enviroment setting'
    echo ENV=development
    echo 
    echo '# Algorithm and Secret stuff'
    echo SECRET=$(secret_generator)
    echo ALGORITHM=HS256
    echo
    echo '# Postgres stuff'
    echo POSTGRES_USER=youruser
    echo POSTGRES_PASSWORD=yourpassword
    echo POSTGRES_HOST=yourhost
    echo POSTGRES_PORT=5432
    echo POSTGRES_DATABASE=yourdatabase
) > api/.env.api

echo "API | enviroment file and variables created successfully"

echo 

(
    echo '# Postgres stuff'
    echo POSTGRES_USER=youruser
    echo POSTGRES_PASSWORD=yourpassword
    echo POSTGRES_HOST=yourhost
    echo POSTGRES_PORT=5432
    echo POSTGRES_DATABASE=yourdatabase
) > ./.env.root

echo "ROOT | enviroment file and variables created successfully"
