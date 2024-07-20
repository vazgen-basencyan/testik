if ! type python &>/dev/null; then
    echo "Creating alias for python to python3..."
    alias python=python3
    echo "alias python=python3" >> ~/.bashrc
    source ~/.bashrc

    echo "Alias 'python' to 'python3' created."
else
    echo "Alias 'python' to 'python3' already exists."
fi

check_java_installed() {
    if command -v java &>/dev/null; then
        echo "Java is already installed."
        return 0
    else
        echo "Java is not installed."
        return 1
    fi
}

install_java() {
    if command -v apt &>/dev/null; then
        sudo apt update
        sudo apt install default-jre -y
    fi
}

if ! check_java_installed; then
  install_java
fi

remove_dir() {
  dir=$1;
  if [ -d "${dir}" ]; then
      rm -r "${dir}"
  fi
}

run_swagger_command() {
  java -jar "$SCRIPTS_DIRECTORY" generate -i ./apis.yaml -l python -o .
}

generate_models() {
  SWAGGER_CODEGEN_URL="https://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/2.4.9/swagger-codegen-cli-2.4.9.jar"
  SCRIPTS_DIRECTORY="${PWD}/scripts/swagger-codegen-cli.jar"

  if [ ! -f "$SCRIPTS_DIRECTORY" ]; then
    echo "Swagger Codegen not found. Downloading and installing..."
    curl "$SWAGGER_CODEGEN_URL" -o "$SCRIPTS_DIRECTORY"
  fi

  remove_dir "swagger_client"
  run_swagger_command
}

generate_models

remove_unnecessary_dirs() {
  UNNECESSARY_DIRS=("./test" "./.swagger-codegen" "./build/lib")
  for dir in "${UNNECESSARY_DIRS[@]}" ; do
    echo "$dir"
    remove_dir "$dir"
  done
}

remove_unnecessary_dirs
