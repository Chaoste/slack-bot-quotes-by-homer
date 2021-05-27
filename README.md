




## Flask Server on Netcup

Since python and pip is not available via bash and netcup offers only a very simple framework with Phusion Passenger and Python 3.5, it is tricky to set up a server.

First approach is to use this Passenger framework and move required libraries from local machine via scp to the hosting machine next to the running code. See (this tutorial)[https://saschaszott.github.io/2021/02/14/netcup-python-webhosting.html]. Some libraries will only work with Python >3.6, so you need to check whether there is an older version compatible with Python 3.5, e.g. use MarkupSafe==0.23 instead of the latest version ((Github issue)[https://github.com/pallets/markupsafe/issues/118]).


Second approach is to follow this (neat tutorial)[https://forum.netcup.de/anwendung/wcp-webhosting-control-panel/p156843-wsgi-python-mit-phusion-passenger-auf-webhosting-8000/#post156843] to install miniconda.

```bash
    $ curl https://repo.anaconda.com/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh --output Miniconda3-4.5.11-Linux-x86_64.sh
    $ bash Miniconda3-4.5.11-Linux-x86_64.sh
    $ rm Miniconda3-4.5.11-Linux-x86_64.sh
    $ touch ~/.profile
    $ echo 'if [ -f ~/.bashrc ]; then . ~/.bashrc; fi' >> ~/.profile
    $ source ~/.profile
    $ conda update -n base -c defaults conda
```
