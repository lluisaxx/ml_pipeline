pipeline {
    agent any

    environment {
        IMAGE_NAME = "sdss-ml-pipeline"
        DATA_PATH  = "sdss_sample.csv"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Clonando repositorio...'
                checkout scm
            }
        }

        stage('Pruebas del dataset') {
            steps {
                echo 'Ejecutando pruebas...'
                sh '''
                    mkdir -p outputs
                    docker run --rm \
                        -v $(pwd):/app \
                        -w /app \
                        -e DATA_PATH=sdss_sample.csv \
                        python:3.11-slim \
                        sh -c "pip install -q pytest pandas scikit-learn && python -m pytest tests/ -v --tb=short"
                '''
            }
        }

        stage('Ejecutar pipeline ML') {
            steps {
                echo 'Ejecutando pipeline ML...'
                sh '''
                    mkdir -p outputs
                    docker run --rm \
                        -v $(pwd):/app \
                        -v $(pwd)/outputs:/app/outputs \
                        -w /app \
                        -e MPLBACKEND=Agg \
                        python:3.11-slim \
                        sh -c "pip install -q pandas scikit-learn matplotlib seaborn numpy && python main.py --data sdss_sample.csv"
                '''
            }
        }

        stage('Build Docker') {
            steps {
                echo 'Construyendo imagen Docker...'
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Run en Docker') {
            steps {
                echo 'Ejecutando en Docker...'
                sh """
                    docker run --rm \
                        -v \$(pwd)/outputs:/app/outputs \
                        ${IMAGE_NAME}:${BUILD_NUMBER}
                """
            }
        }

        stage('Almacenar artefactos') {
            steps {
                echo 'Archivando artefactos...'
                archiveArtifacts artifacts: 'outputs/**/*', fingerprint: true
            }
        }
    }

    post {
        success { echo 'Pipeline completado exitosamente.' }
        failure { echo 'El pipeline fallo.' }
    }
}
