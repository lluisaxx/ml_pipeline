pipeline {
    agent any

    environment {
        IMAGE_NAME = "sdss-ml-pipeline"
        DATA_PATH  = "sdss_sample.csv"
    }

    stages {

        stage('Checkout') {
            steps {
                echo '📥 Clonando repositorio...'
                checkout scm
            }
        }

        stage('Instalar dependencias') {
            steps {
                echo '📦 Instalando dependencias Python...'
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Pruebas del dataset') {
            steps {
                echo '🧪 Ejecutando pruebas básicas del dataset...'
                sh '''
                    . .venv/bin/activate
                    DATA_PATH="${DATA_PATH}" python -m pytest tests/ -v \
                        --tb=short \
                        --junitxml=outputs/test_results.xml
                '''
            }
            post {
                always {
                    junit 'outputs/test_results.xml'
                }
            }
        }

        stage('Ejecutar pipeline ML') {
            steps {
                echo '🚀 Ejecutando pipeline de Machine Learning...'
                sh '''
                    . .venv/bin/activate
                    mkdir -p outputs
                    python main.py --data "${DATA_PATH}" | tee outputs/pipeline.log
                '''
            }
        }

        stage('Build Docker') {
            steps {
                echo '🐳 Construyendo imagen Docker...'
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} ."
            }
        }

        stage('Run en Docker') {
            steps {
                echo '▶️  Ejecutando pipeline dentro del contenedor Docker...'
                sh """
                    docker run --rm \
                        -v \$(pwd)/outputs:/app/outputs \
                        ${IMAGE_NAME}:${BUILD_NUMBER}
                """
            }
        }

        stage('Almacenar artefactos') {
            steps {
                echo '💾 Archivando métricas y gráficas...'
                archiveArtifacts artifacts: 'outputs/**/*', fingerprint: true
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completado exitosamente.'
        }
        failure {
            echo '❌ El pipeline falló. Revisa los logs.'
        }
        always {
            echo '🧹 Limpiando entorno virtual...'
            sh 'rm -rf .venv'
        }
    }
}
