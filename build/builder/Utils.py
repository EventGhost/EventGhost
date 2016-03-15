# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.


import os
import sys
import time
import subprocess
import re
import _winreg
from os.path import join, normpath, expanduser
import builder
from builder.subprocess2 import Popen


def EncodePath(path):
    return path.encode('mbcs')


def DecodePath(path):
    return path.decode('mbcs')


def StartProcess(*args):
    #SetIndent(1)
    startupInfo = subprocess.STARTUPINFO()
    startupInfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
    startupInfo.wShowWindow = subprocess.SW_HIDE
    process = Popen(
        args,
        cwd=EncodePath(join(builder.buildSetup.sourceDir, "build")),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        startupinfo=startupInfo,
    )
    while process.returncode is None:
        process.poll()
        errData = process.recv_err()
        if errData is not None:
            sys.stderr.write(errData)
        inData = process.recv()
        if inData is not None:
            if inData:
                sys.stdout.write(inData)
            else:
                time.sleep(0.1)
        else:
            break
    process.wait()
    #SetIndent(0)
    return process.returncode


def ExecutePy(*args):
    return StartProcess(sys.executable, "-u", "-c", "\n".join(args))


def GetRevision(buildSetup):
    """
    Get the app version and revision.
    """
    print "getting version and revision from GitHub."
    parts = GetLastReleaseOrTagName(buildSetup).split('.')[:3]
    parts[0] = parts[0].strip('v')
    while len(parts) < 3:
        parts.append("0")
    parts[2] = int(parts[2]) + 1
    buildSetup.appVersion = '{0}.{1}.{2}'.format(*parts)
    magic = 1722 - 1046  # Last SVN revision - total Git commits at r1722
    commits = GetCommitCount(buildSetup)
    buildSetup.appRevision = (commits + magic) if commits else 0


def GetLastReleaseOrTagName(buildSetup):
    '''
    Get the name of latest release. If none is found, all releases
    will be searched for highest number. If there is although no
    name found, the tags will be searched.
    '''
    from agithub.GitHub import GitHub
    token = buildSetup.gitConfig["token"]
    user = buildSetup.gitConfig["user"]
    repo = buildSetup.gitConfig["repo"]
    branch = buildSetup.gitConfig["branch"]
    gh = GitHub(token=token)

    # first try if there's already a latest release
    rc, data = gh.repos[user][repo].releases.latest.get()
    if rc == 200:
        return data['name']

    # if not, let's try if there's any release
    lastRelease = ''
    page = 1
    while page > 0:
        rc, data = gh.repos[user][repo].releases.get(sha=branch,
                                                     per_page=100, page=page)
        if rc != 200:
            break
        page = NextPage(gh)
        for release in data:
            if release['name'] > lastRelease:
                lastRelease = release['name']

    # ok, no releases, let's check the tags.
    if lastRelease == '':
        page = 1
        while page > 0:
            rc, data = gh.repos[user][repo].git.refs.tags.get(sha=branch,
                                                     per_page=100, page=page)
            if rc != 200:
                break
            page = NextPage(gh)
            for tag in data:
                if tag['ref'][10:] > lastRelease:
                    lastRelease = tag['ref'][10:]
        return lastRelease


def GetCommitCount(buildSetup):
    '''
    Get the count of commits for repository.
    '''
    from agithub.GitHub import GitHub
    token = buildSetup.gitConfig["token"]
    user = buildSetup.gitConfig["user"]
    repo = buildSetup.gitConfig["repo"]
    branch = buildSetup.gitConfig["branch"]
    gh = GitHub(token=token)

    counter = 0
    page = 1
    # get the commit count by adding contributions from all contributors
    while page > 0:
        rc, data = gh.repos[user][repo].contributors.get(sha=branch, anon='true',
                                                         per_page=100, page=page)
        if rc != 200:
            # print "INFO: couldn't get contributors infos."
            return None
        page = NextPage(gh)
        for contr in data:
            counter += contr['contributions']
    return counter


def GetHtmlHelpCompilerPath():
    """
    Try to find the install location of the HTML Help command line compiler
    """
    subkey = r"Software\Microsoft\HTML Help Workshop"
    try:
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, subkey)
        path = _winreg.QueryValueEx(key, "InstallDir")[0]
    except WindowsError:
        path = join(os.environ["PROGRAMFILES"], "HTML Help Workshop")
    programPath = join(path, "hhc.exe")
    if not os.path.exists(programPath):
        return None
    return programPath


def ListDir(path, skip_dirs=[], fullpath=True):
    '''
    Return a list with all files in given path (including subdirs).
    skip_dirs is a list of directories, which contents should not be listet.

    :param path: root directory (full path)
    :param skip_dirs: list of directory names to skip
    :param fullpath: should the list contain the full path?
    :return: list of filenames with full path
    '''

    if not fullpath:
        cwd = os.getcwd()
        os.chdir(path)
        path = '.'

    contents = os.walk(path)
    files = []
    for item in contents:
        parts = set(item[0].split('\\'))
        if parts.intersection(skip_dirs):
            continue
        if len(item[2]) > 0:
            for name in item[2]:
                if name[-4:] not in ('.pyc',):
                    filename = normpath(join(item[0], name))
                    files.append(filename)
        if len(item[1]) > 0:
            for subdir in item[1]:
                parts = set(subdir.split('\\'))
                if parts.intersection(skip_dirs):
                    continue
                else:
                    subpath = normpath(join(path, subdir))
                    sublist = ListDir(subpath, skip_dirs)
                    files.extend(sublist)
    if not fullpath:
        os.chdir(cwd)
    return files


def GetGithubConfig():
    '''
    Get GitHub from .gitconfig .
    '''
    from agithub.GitHub import GitHub
    # read .gitconfig
    cfg = expanduser('~\.gitconfig')
    with open(cfg,"rt") as f:
        cfg = f.readlines()

    # try to to read github section from .gitconfig
    idx = cfg.index("[github]\n")
    gitcfg = {}
    for i in range(idx+1, len(cfg)):
        if cfg[i].strip().startswith('['):
            break
        elif cfg[i].strip() == "":
            continue
        key, val = cfg[i].strip().split('=')
        gitcfg.update({key.strip(): val.strip()})

    # no entry for 'token' and/or 'user' found in .gitconfig
    if "token" not in gitcfg or "user" not in gitcfg:
        raise ValueError

    # try to get some defaults for repo and branch
    gh = GitHub(token=gitcfg["token"])
    gitcfg["all_repos"] = {}
    gitcfg.update({"repo": "", "branch": ""})
    page = 1
    while page > 0:
        rc, data = gh.user.repos.get(page=page)
        page = NextPage(gh)
        if rc == 200:
            for repo in data:
                if repo["name"] == "EventGhost":
                    gitcfg.update({
                        "repo": repo["name"],
                        "repo_full": repo["full_name"],
                        "branch": repo["default_branch"]
                    })
                    page2 = 1
                    branches = []
                    while page2 > 0:
                        rc2, data2 = gh.repos[gitcfg["user"]][repo["name"]].branches.get(page=page2)
                        page2 = NextPage(gh)
                        if rc2 == 200:
                            for br in data2:
                                branches.append(br["name"])
                    gitcfg["all_repos"].update({
                        repo["full_name"]: {
                            "name": repo["name"],
                            "all_branches": branches,
                            "def_branch": repo["default_branch"]
                            }
                        })
    return gitcfg


def NextPage(gh):
    hdr = gh.getheaders()
    header = {item[0].strip(): item[1].strip() for item in hdr}
    if 'link' in header:
        parts = header['link'].split(',')
        for part in parts:
            subparts = part.split(';')
            sub = subparts[1].split('=')
            if sub[0].strip() == 'rel':
                if sub[1] == '"next"':
                    page = int(re.match(ur'.*page=(\d+).*',
                               subparts[0],
                               re.IGNORECASE | re.DOTALL | re.UNICODE).
                               groups()[0])
                    return page
    return 0

