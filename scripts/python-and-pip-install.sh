check_python_installed() {
    if command -v python &>/dev/null; then
        echo "Python is already installed."
        return 0
    else
        echo "Python is not installed."
        return 1
    fi
}

install_python() {
    if command -v apt &>/dev/null; then
        sudo apt update
        sudo apt install python3 -y
    fi
}

check_pip_installed() {
    if command -v pip &>/dev/null; then
        echo "Pip is already installed."
        return 0
    else
        echo "Pip is not installed."
        return 1
    fi
}

install_pip() {
    if command -v apt &>/dev/null; then
        sudo apt update
        sudo apt install python3-pip -y
    fi
}

if ! check_python_installed; then
  install_python
fi

if ! check_pip_installed; then
  install_pip
fi
