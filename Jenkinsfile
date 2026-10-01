pipeline {
    agent any

    environment {
        IMAGE       = "amaaaal/counter-app"
        DOCKER_CRED = credentials('dockerhub-creds')
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Tests unitaires') {
            steps {
                sh '''
                    docker run --rm \
                      -u $(id -u):$(id -g) -e HOME=/tmp -e PYTHONDONTWRITEBYTECODE=1 \
                      -v "$PWD":/app -w /app python:3.12-alpine \
                      sh -c "pip install --user -q -r requirements.txt pytest && python -m pytest -v -p no:cacheprovider"
                '''
            }
        }

        stage('Build de l\'image') {
            steps {
                sh 'docker build -t $IMAGE:$BUILD_NUMBER -t $IMAGE:latest .'
            }
        }

        stage('Push sur Docker Hub') {
            steps {
                sh '''
                    echo "$DOCKER_CRED_PSW" | docker login -u "$DOCKER_CRED_USR" --password-stdin
                    docker push $IMAGE:$BUILD_NUMBER
                    docker push $IMAGE:latest
                '''
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
        }
        success {
            echo "Image publiée : ${IMAGE}:${BUILD_NUMBER}"
        }
        failure {
            echo "Le pipeline a échoué, consultez les logs."
        }
    }
}
