alias l="ls -lrt"
alias ll="ls -alF"
alias ls='ls -GFh'
alias tclsh='rlwrap tclsh'
alias vmd='/Applications/VMD\ 1.9.4a57-x86_64-Rev12.app/Contents/Resources/VMD.app/Contents/MacOS/VMD'
alias fftool="/Users/marcodigennaro/WORK/external_packages/fftool/fftool"

alias goto_work='cd /Users/marcodigennaro/WORK'
alias mypytest='pytest -skv --cov --continue-on-collection-errors --html=report.html'

alias TME_WS='ssh -XY tme_workstation'
alias TME_CLUSTER='ssh 10.100.192.2 -Yl mdi0316'

function jnb() {
    conda_start
    conda activate perso
    jupyter-lab --NotebookApp.password=""
    }

function goto_elia() {
    cd /Users/marcodigennaro/Desktop/APPLICATIONS/2024/35_ELIA
    }

function goto_kubas() {
    conda_start
    conda activate kubas
    cd /Users/marcodigennaro/WORK/TME/KUBAS
    }

function goto_nagare() {
    conda_start
    conda activate nagare
    cd /Users/marcodigennaro/WORK/PYTHON/pakages/nagare
    }

function goto_pgel() {
    conda_start
    conda activate pgel
    cd /Users/marcodigennaro/WORK/TME/PGEL
    export ASE_LAMMPSRUN_COMMAND=/Users/marcodigennaro/miniconda3/envs/pgel/bin/lmp_serial

    ###### NC_ROOT EXPORTS ########
    export NC_ROOT="/Users/marcodigennaro/WORK/external_packages/ASE_ANI"
    export LD_LIBRARY_PATH="$NC_ROOT/lib:$LD_LIBRARY_PATH"
    export PYTHONPATH="$NC_ROOT/lib:$PYTHONPATH"
    }

function goto_sto() {
    conda_start
    conda activate sto
    cd /Users/marcodigennaro/WORK/TME/STO
    }

function goto_abipy() {
    conda_start
    conda activate abipy
    cd /Users/marcodigennaro/WORK/TME/
    jupyter-lab --NotebookApp.password=''
    }

function conda_start() {
    # >>> conda initialize >>>
    # !! Contents within this block are managed by 'conda init' !!
    __conda_setup="$('/Users/marcodigennaro/miniconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
    if [ $? -eq 0 ]; then
        eval "$__conda_setup"
    else
        if [ -f "/Users/marcodigennaro/miniconda3/etc/profile.d/conda.sh" ]; then
# . "/Users/marcodigennaro/miniconda3/etc/profile.d/conda.sh"  # commented out by conda initialize
        else
# export PATH="/Users/marcodigennaro/miniconda3/bin:$PATH"  # commented out by conda initialize
        fi
    fi
    unset __conda_setup
    # <<< conda initialize <<<
    }

function parse_git_branch() {
    git branch 2> /dev/null | sed -n -e 's/^\* \(.*\)/[\1]/p'
}

function virtualenv_info {
    [ $VIRTUAL_ENV ] && echo '('`basename $VIRTUAL_ENV`') '
}

PROMPT='%*:%~ %% '
PROMPT='%F{green}%*%f:%F{blue}%~%f %% '

COLOR_DEF=$'%f'
COLOR_USR=$'%F{green}'
COLOR_DIR=$'%F{blue}'
COLOR_GIT=$'%F{red}'
setopt PROMPT_SUBST
export PROMPT='${COLOR_USR}mdg@macbook${COLOR_DIR} %c -> ${COLOR_GIT}$(parse_git_branch)${COLOR_DEF} '


export TEXMFHOME=/usr/local/Cellar/texlive/20220321_3/share/texmf-dist:/usr/local/texlive/2022/texmf-dist:$TEXMFHOME

export DISPLAY=:0

#more keys here
#https://zsh.sourceforge.io/Doc/Release/Zsh-Line-Editor.html#Standard-Widgets
bindkey  "^[[H"   beginning-of-line
bindkey  "^[[F"   end-of-line
bindkey  "^[[3~"  delete-char


test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"

# GROMACS setup
autoload -Uz compinit
compinit
source /usr/local/gromacs/bin/GMXRC.bash


## TURBOMOLE setup
#export TURBODIR=/Users/marcodigennaro/WORK/CODES.nosync/TURBOMOLE
#export PATH=$TURBODIR/scripts:$PATH
#export PATH=$TURBODIR/bin/em64t-unknown-linux-gnu_mpi:$PATH


# MacPorts/VirtualBox
export MANPATH=/opt/local/share/man:$MANPATH

# alias clusters
alias nic5="ssh -XY nic5"
alias mtgnx="ssh matgenix-mdi@172.22.25.7"

export PATH="/Users/marcodigennaro/.local/bin:$PATH"

export LC_CTYPE=$LANG
export RDBASE=/usr/local/opt/rdkit/share/RDKit

# PERL
PATH="/Users/marcodigennaro/perl5/bin${PATH:+:${PATH}}"; export PATH;
PERL5LIB="/Users/marcodigennaro/perl5/lib/perl5${PERL5LIB:+:${PERL5LIB}}"; export PERL5LIB;
PERL_LOCAL_LIB_ROOT="/Users/marcodigennaro/perl5${PERL_LOCAL_LIB_ROOT:+:${PERL_LOCAL_LIB_ROOT}}"; export PERL_LOCAL_LIB_ROOT;
PERL_MB_OPT="--install_base \"/Users/marcodigennaro/perl5\""; export PERL_MB_OPT;
PERL_MM_OPT="INSTALL_BASE=/Users/marcodigennaro/perl5"; export PERL_MM_OPT;

# BOSS
export BOSSdir="/Users/marcodigennaro/CODES/boss"
export PATH="/usr/local/opt/tcl-tk/bin:$PATH"

#JAVA
export PATH="/usr/local/opt/openjdk/bin:$PATH"
export JAVA_HOME="/usr/local/opt/openjdk/"
