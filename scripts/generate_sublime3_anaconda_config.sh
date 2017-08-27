
echo -e "\n[ Write to postactivate ]"
cat << EOF > $HOME/.virtualenvs/scarlett_os/bin/postactivate
{
    "settings": {
        "python_interpreter": "tcp://localhost:19360?pathmap=~/dev/bossjones/scarlett_os,/home/pi/dev/bossjones/scarlett_os"
    }
}
EOF


