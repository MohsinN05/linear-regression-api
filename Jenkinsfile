
pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set -eu
                        echo "$DOCKERHUB_TOKEN" |
                            docker login -u "$DOCKERHUB_USER" --password-stdin
                        docker compose push
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy API') {
            steps {
                sh 'docker compose up -d --no-build'
            }
        }

        stage('Verify API') {
            steps {
                sh '''
                    set -eu
                    for attempt in $(seq 1 30); do
                        if curl -fsS http://127.0.0.1:5000/health; then
                            echo
                            echo "Prediction API is healthy."
                            exit 0
                        fi
                        sleep 2
                    done

                    echo "Prediction API did not become healthy."
                    docker compose logs
                    exit 1
                '''
            }
        }
    }
}
