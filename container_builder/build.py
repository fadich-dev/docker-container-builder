#!/usr/bin/env python

import sys
import argh
import json
import docker
import curses


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


def build(path, image, push=False, repository=None, tag='latest'):
    sys.stdout.write('Building {}\n'.format(path))

    img, res = docker_client.images.build(path=path, tag=image)
    for s in res:
        sys.stdout.write(s.get('stream') or '')

    if tag:
        img.tag(repository, tag)

    if push:
        sys.stdout.write('Pushing...\n')
        stream_out(docker_client.images.push(repository, tag, stream=True))
        sys.stdout.write('Pushed successfully.\n')


def main(*args):
    curses.initscr()

    curses.echo()
    curses.nocbreak()
    curses.endwin()

    parser = argh.ArghParser()
    parser.add_commands([
        build,
    ])

    parser.dispatch()


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
