pipeline  {
    agent  {
        label 'linux'
    }
    stages {
        stage('Checkout role') {
            steps {
                sh 'python3 -V'
            }
        }
        stage('Molecule installation') {
            steps {
                sh 'ansible-playbook --version'
                sh 'python3 -m pip install molecule'
                sh 'molecule --version'
            }
        }
        stage('Linters Installation') {
            steps {
                sh 'pip3 install ansible-lint yamllint'
                sh 'yamllint --version'
                sh 'ansible-lint --version'
            }
        }
    }
}