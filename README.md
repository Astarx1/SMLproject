Current configuration

Board size = 13
First player = Black (value 1)

Winner :
Black : Top -> Bottom (y = 0 to y = 11)
White : Left to Right (x = 0 to x = 11)

Python Version : 3.6
Packages : See requirements.txt

Few things about keeping the code clean :
- Before coding, always fetch the master to see if changes have been done.
- Do not merge your branch directly on the master branch
- Before pushing ALWAYS launch run.py, it contains test routines which are verifying that you will not be preventing
others to code

Set up a good environment :
1) Create your own virtual environment with virtualenv or conda (many tutorials are available online) and activate it.
You can skip this part but it is not recommended.
2) Clone the github repo and go in the directory.
3) Install the packages by asking Pycharm to do it for you (don't know how though) or run the command in the console
(linux, or conda terminal. Powershell should be ok, but I don't know how)
pip install -r requirements.txt
Hopefully, it will install all the required packages.
4) You can run run.py

The environment should be activated every time the code is run (Pycharm does it automatically).

Something may have been forgotten in requirements.txt and it may change following project progress, so feel free to
repeat the process if you have a problem and mail Romain if it doesn't solve the problem.

TODO :
In UTC,
1) Prune parts of the trees where it is impossible to find new children so that the algorithm will not explore these
parts anymore
2) An option which would, for certain games advantage areas which are not recommanded by the p theta :) , but such
games should not be included in the p-learning process, only for v theta (hard to do ...)
3) Include in the AI a "It is won" option so that v theta would be 1 if the game is won

1) In Coach : To be able to play against previous versions

BUGS :
1) In the coach, the UTC often returns -1 as first move. I do not know why...