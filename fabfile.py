from fabric.api import local, run, env

env.hosts = ['dellsystem@mcmun.org']

def less():
	local("lessc mcmun/static/css/mcmun.less -X > mcmun/static/css/mcmun.css")

def deploy():
	less()
	local('git push')
	run('cd mcmun.org && git pull')
	run('echo "yes" | python manage.py collectstatic')
