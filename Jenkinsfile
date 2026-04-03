pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Pruebas del dataset') {
            steps {
                sh 'docker run --rm -v \C:\Users\luisa\Downloads\ml_pipeline:/app -w /app -e DATA_PATH=sdss_sample.csv python:3.11-slim bash -c "pip install -q pytest pandas scikit-learn && python -m pytest tests/ -v --tb=short"'
            }
        }
        stage('Ejecutar pipeline ML') {
            steps {
                sh 'mkdir -p outputs && docker run --rm -v \C:\Users\luisa\Downloads\ml_pipeline:/app -v \C:\Users\luisa\Downloads\ml_pipeline/outputs:/app/outputs -w /app -e MPLBACKEND=Agg python:3.11-slim bash -c "pip install -q pandas scikit-learn matplotlib seaborn numpy && python main.py --data sdss_sample.csv"'
            }
        }
        stage('Build Docker') {
            steps { sh 'docker build -t sdss-ml-pipeline:latest .' }
        }
        stage('Run en Docker') {
            steps { sh 'docker run --rm -v \C:\Users\luisa\Downloads\ml_pipeline/outputs:/app/outputs sdss-ml-pipeline:latest' }
        }
        stage('Almacenar artefactos') {
            steps { archiveArtifacts artifacts: 'outputs/**/*', fingerprint: true }
        }
    }
    post {
        success { echo 'Pipeline completado exitosamente.' }
        failure { echo 'El pipeline fallo.' }
    }
}