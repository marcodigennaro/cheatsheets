GIT cheatsheet
==============


git user
--------

git config --global user.name "My Name"

git config --global user.email "myemail@example.com"

git config --global core.editor vim

git config --global color.ui true

git config --list


change user.name and user.email
-------------------------------

https://alvinalexander.com/git/git-show-change-username-email-address/


clone repo to new_folder
------------------------

git clone https://cde.toyota-europe.com/stash/scm/~mdi0316/gec.git new_folder


common commands
---------------

https://www.notion.so/Introduction-to-Git-ac396a0697704709a12b6a0e545db049

git init

git status

touch index.html

git add index.html # --all or . to add everything

git commit -m "create index.html"  #present tense

git log

git remote add origin https://cde.toyota-europe.com/stash/scm/~mdi0316/new.git

git push -u origin HEAD:master

git remote -v


branches
--------

git branch #shows a list

git checkout -b branch_name #create new branch

git checkout main


staging
-------

git status

git add file_name

git rm --cached file_name


merging
-------

##Always merge from main what has been changed

git checkout main

git merge develop


upstream
--------
#https://www.youtube.com/watch?v=deEYHVpE1c8&ab_channel=FaradayAcademy
#Before 

$ git remote -v

    origin	git@github.com:marcodigennaro/nagare.git (fetch)

    origin	git@github.com:marcodigennaro/nagare.git (push)

$ git remote add upstream git@github.com:davidwaroquiers/nagare.git

$ git remote -v

    origin	git@github.com:marcodigennaro/nagare.git (fetch)
    
    origin	git@github.com:marcodigennaro/nagare.git (push)
    
    upstream	git@github.com:davidwaroquiers/nagare.git (fetch)
    
    upstream	git@github.com:davidwaroquiers/nagare.git (push)
