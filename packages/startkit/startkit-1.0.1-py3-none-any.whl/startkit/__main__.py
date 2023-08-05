#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import getpass
import os
import shutil


def main():
    dest = os.getcwd()
    dest = input(
        '> Create the project under which path [%s]?' % dest).strip() or dest
    if (not os.path.exists(dest) or not os.path.isdir(dest)):
        os.makedirs(dest)
    dest = os.path.abspath(dest)

    project = 'myproject'
    project = input(
        '> Please enter your project name [%s]:' % project).strip() or project
    package = project.replace('-', '_')
    package = input(
        '> Please enter main package name [%s]:' % package).strip() or package
    version = '0.0.1'
    version = input(
        '> Please enter your project version [%s]:' % version).strip() or version
    description = 'None.'
    description = input(
        '> Please enter your project description:').strip() or description
    author = getpass.getuser()
    author = input('> Please enter your name [%s]:' % author).strip() or author
    email = 'Unknown'
    email = input('> Please enter your email:').strip() or email
    date = str(datetime.datetime.now().year)

    table = {
        '{{ project }}': project,
        '{{ package }}': package,
        '{{ version }}': version,
        '{{ description }}': description,
        '{{ author }}': author,
        '{{ email }}': email,
        '{{ date }}': date
    }

    dest = os.path.join(dest, project)
    try:
        shutil.copytree(os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'templates'), dest)
    except Exception as err:
        print('Error occurs: %s' % err)
        exit()
    for root, dirs, files in os.walk(dest):
        for name in dirs:
            path = os.path.join(root, name)
            base = os.path.basename(path)
            for key, value in table.items():
                base = base.replace(key, value)
            if path != os.path.join(root, base):
                os.rename(path, os.path.join(root, base))
        for name in files:
            file = os.path.join(root, name)
            base = os.path.basename(file)
            for key, value in table.items():
                base = base.replace(key, value)
            if file != os.path.join(root, base):
                os.rename(file, os.path.join(root, base))
    for root, dirs, files in os.walk(dest):
        for name in dirs:
            pass
        for name in files:
            file = os.path.join(root, name)
            with open(file, 'r', encoding='utf-8') as f:
                try:
                    lines = f.readlines()
                except:
                    continue
            with open(file, 'w', encoding='utf-8') as f:
                for line in lines:
                    for key, value in table.items():
                        line = line.replace(key, value)
                    f.write(line)
    print('The project has been successfully created!')


if __name__ == '__main__':
    main()
