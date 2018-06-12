if [ ! -d "/anaconda" ]; then
    wget https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh
    bash Anaconda3-4.2.0-Linux-x86_64.sh -b -p /anaconda
    echo "export PATH=/anaconda/bin:$PATH" >> /etc/bash.bashrc
    echo "export PYSPARK_PYTHON=/anaconda/bin/python" >> /etc/bash.bashrc
fi

/anaconda/bin/pip install findspark
/anaconda/bin/conda install -y seaborn pandas pyspark