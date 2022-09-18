---
title: ubuntu环境配置
created: 2022-09-06 22:49:14
updated: 2022-09-18 20:46:19
tags: 
- article
- featured
---

# ubuntu环境配置

```sh
# apt换源
sudo cp -a /etc/apt/sources.list /etc/apt/sources.list.bak
sudo sed -i "s@http://.*archive.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list  
sudo sed -i "s@http://.*security.ubuntu.com@http://repo.huaweicloud.com@g" /etc/apt/sources.list
sudo apt update

# pip 换源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple


sudo apt-get update
# sudo apt-get install python2.7-dev python-pip -y
pip install pwntools
# echo 'export PATH=/usr/local/mongodb/bin:$PATH >> ~/.bashrc'
sudo apt-get install libcapstone-dev -y

# wpndbg 适合pwn
cd ~/
git clone https://github.com/pwndbg/pwndbg
cd pwndbg
./setup.sh
cd ~/
git clone https://github.com/scwuaptx/Pwngdb.git
cp ~/Pwngdb/.gdbinit ~/

# peda 适合逆向
git clone https://github.com/longld/peda.git ~/peda
echo "source ~/peda/peda.py" >> ~/.gdbinit

# if not install pwndbg & pwngdb ? use howdays gdb
# wget http://howdays.kr/public/gdb/setupdbg.sh
# chmod 777 setupdbg.sh
# ./setupdbg.sh

# zsh
sudo apt-get install git
sudo apt-get install zsh -y
sudo chsh -s /usr/bin/zsh
sudo sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
# ADD ~/.zshrc -> (zsh-autosuggestions)
source ~/.zshrc

sudo apt install ruby-full -y
gem install one_gadget

sudo pip install ropgadget -y

# pwn端口转发本地部署工具
sudo apt-get install socat

# 32位环境
sudo apt-get update  
sudo apt-get purge libc6-dev  
sudo apt-get install libc6-dev  
sudo apt-get install libc6-dev-i386

# sudo dpkg --add-architecture i386
# sudo apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386 -y

# z3
sudo apt-get install z3
git clone https://github.com/Z3Prover/z3.git
cd z3
cd build
make
sudo make install
```

## gdb插件切换

```sh
# 切换脚本
touch ~/.local/bin/gdbplugin
cat > ~/.local/bin/gdbplugin << \EOF
#!/bin/bash
function Mode_change {
    name=$1
    gdbinitfile=~/.gdbinit    #这个路径按照你的实际情况修改
    peda="source ~/peda/peda.py"   #这个路径按照你的实际情况修改
    gef="source ~/.gdbinit-gef.py"  #这个路径按照你的实际情况修改
    pwndbg="source ~/Downloads/pwndbg/gdbinit.py"

    sign=$(cat $gdbinitfile | grep -n "#this place is controled by user's shell")
           #此处上面的查找内容要和你自己的保持一致

    pattern=":#this place is controled by user's shell"
    number=${sign%$pattern}
    location=$[number+2]

    parameter_add=${location}i
    parameter_del=${location}d

    message="TEST"

    if [ $name -eq "1" ];then
        sed -i "$parameter_del" $gdbinitfile
        sed -i "$parameter_add $peda" $gdbinitfile
        echo -e "Please enjoy the peda!\n"
    elif [ $name -eq "2" ];then
        echo -e "Please enjoy the gef!\n"
        else
        sed -i "$parameter_del" $gdbinitfile
        sed -i "$parameter_add $pwndbg" $gdbinitfile
        echo -e "Please enjoy the pwndbg!\n"
    fi

}

echo -e "Please choose one mode of GDB?\n1.peda    2.gef    3.pwndbg"

read -p "Input your choice:" num

if [ $num -eq "1" ];then
    Mode_change $num
elif [ $num -eq "2" ];then
    Mode_change $num
elif [ $num -eq "3" ];then
    Mode_change $num
else
    echo -e "Error!\nPleasse input right number!"
fi

gdb $1 $2 $3 $4 $5 $6 $7 $8 $9

EOF

sudo chmod +x ~/.local/bin/gdbplugin
```
