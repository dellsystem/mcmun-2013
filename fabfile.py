from fabric.api import local, run, env, settings

env.hosts = ['dellsystem@mcmun.org']

def less():
	local("lessc mcmun/static/css/mcmun.less -x > mcmun/static/css/mcmun.css")

def deploy():
	less()
	with settings(warn_only=True):
		local("git add mcmun/static/css/mcmun.css")
		local("git commit -m 'Update compiled CSS'")
	local('git push')
	run('cd mcmun.org && git pull')
	run('echo "yes" | python mcmun.org/manage.py collectstatic')
	run('python mcmun.org/manage.py syncdb')

def up():
	local("python manage.py runserver")

def dump():
	local("python manage.py dumpdata cms --indent=4 > cms/fixtures/initial_data.json")
