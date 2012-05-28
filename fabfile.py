from fabric.api import local, run, env, settings

env.hosts = ['dellsystem@mcmun.org']

def less():
	local("lessc mcmun/static/css/mcmun.less -X > mcmun/static/css/mcmun.css")

def deploy():
	less()
	with settings(warn_only=True):
		local("git add mcmun/static/css/mcmun.css")
		local("git commit -m 'Update compiled CSS'")
	local('git push')
	run('cd mcmun.org && git pull')
	run('echo "yes" | python mcmun.org/manage.py collectstatic')
