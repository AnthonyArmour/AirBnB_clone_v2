#!/usr/bin/python3
"""first fabric script    """


from fabric.api import local, run, put, env
from datetime import datetime
import os.path
from fabric.context_managers import cd

env.hosts = ["54.242.225.135", "3.92.27.64"]


def do_clean(number=0):
    """deletes all but newest files"""
    if int(number) == 0:
        number = 1

    loc_str = local("cd versions; ls -t", capture=True)
    loc_lst = loc_str.split('\n')
    if len(loc_lst) > int(number):
        local("cd versions; rm `ls -t | awk 'NR >" + str(number) + "'`")

    with cd("/data/web_static/releases"):
        run_str = run("ls -t")
        run_lst = run_str.split('\n')
        if len(run_lst) > int(number):
            run("rm `ls -t | awk 'NR >" + str(number) + "'`")


def deploy():
    """deploys archive"""
    archive = do_pack()
    if archive is not None:
        return do_deploy(archive)
    else:
        return False


def do_deploy(archive_path):
    """deploys contetnt to servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        path_file = archive_path[9:]
        path_file_no_extension = path_file[:-4]
        new_dir = "/data/web_static/releases/" + path_file_no_extension + "/"
        put(archive_path, "/tmp/" + path_file)
        run("mkdir -p " + new_dir)
        run("tar -xzvf /tmp/" + path_file + " -C " +
            new_dir + " --strip-components=1")
        run("rm -rf /tmp/" + path_file)
        run("rm -rf /data/web_static/current")
        run("sudo ln -sf " + new_dir + " /data/web_static/current")
        return True
    except:
        return False


def do_pack():
    """stuff"""
    time = datetime.now()
    arch_name = "web_static_" + time.strftime("%Y%M%d%H%M%S") + ".tgz"
    v_path = "versions/" + arch_name
    tzg = "tar -cvzf " + v_path + " web_static"
    try:
        local("mkdir -p versions")
        local(tzg)
        return v_path
    except:
        return None
