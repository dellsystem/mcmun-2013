from fabric.api import local, run

def less():
	local("lessc mcmun/static/css/mcmun.less -X > mcmun/static/css/mcmun.css")

def deploy():
	pass
