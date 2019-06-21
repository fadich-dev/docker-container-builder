#!/usr/bin/env python

import os
import sys
import argh
import json
import docker
import curses

from .spinner import Spinner

docker_client = docker.from_env()


def stream_out(stream):
    layers = {}

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()

    for line in stream:
        layer = json.loads(line.decode('utf-8'))
        layers[layer.get('id')] = layer

        c = 0
        for l in layers.values():
            stdscr.addstr(c, 0, '{}: {} {}'.format(
                l.get('id', ''),
                l.get('status', ''),
                l.get('progress', ''),
            ))
            c += 1
        stdscr.refresh()

    curses.echo()
    curses.nocbreak()
    curses.endwin()


def build(path, image, push=False, repository=None, tag='latest', quiet: bool = False):
    if quiet:
        sys.stdout = open(os.devnull, 'w')

    spinner = Spinner(stdout=sys.stdout)
    curses.initscr()

    curses.echo()
    curses.nocbreak()
    curses.endwin()

    spinner.start('[{}] Building from {}'.format(image, path))
    img, res = docker_client.images.build(path=path, tag=image)
    spinner.stop()

    for s in res:
        sys.stdout.write(s.get('stream') or '')

    if push:
        img.tag(repository, tag)
        sys.stdout.write('[{}] Pushing...\n'.format(image))
        res = docker_client.images.push(repository, tag, stream=True)
        if not quiet:
            stream_out(res)
        sys.stdout.write('[{}] Pushed successfully.\n'.format(image))


def main(*args):
    parser = argh.ArghParser()
    parser.add_commands([
        build,
    ])

    parser.dispatch()


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
