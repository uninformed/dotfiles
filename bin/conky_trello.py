#!/usr/bin/env python3
'''Format Trello cards as (Conky) lines'''
from textwrap import shorten

import arrow
import click
from trello import TrelloClient

def formatLine(card, fmt, color='${color}', width=48):
    '''Format contents of a card into a line of output.

    Available formatting elements are:
        * name
        * due_date
        * description
        * listname
        * labels

    :param card: a Trello Card object
    :param fmt: a .format()-style string
    :param color: conky-style color for the line
    '''
    lineout = fmt.format(
        name=card.name,
        due_date=arrow.get(card.due_date).humanize() if card.due_date != '' else 'N/A',
        description=card.description,
        listname=card.get_list().name,
        labels=','.join([l.name for l in card.labels or []])  # maybe change this
        )
    # TODO make width a command-line option
    return color + shorten(lineout, width=width, placeholder='...') if color else shorten(lineout, width=width, placeholder='...')

@click.command()
@click.argument('boardid')
@click.argument('keyfile', type=click.File('r'))
@click.argument('linefmt', default='{name} [{listname}] due {due_date}')
#@click.argument('header')
@click.option('--start', '-s', default=-12, help='range start offset (months from now)', type=int)
@click.option('--end', '-e', default=1, help='range end offset (months from now)', type=int)
@click.option('--target', default='Complete', type=str, help='')
@click.option('--color/--no-color', default='True', help='add conky color directives to output')
def checkBoard(boardid, linefmt, start, end, target, color, keyfile):
    # create arrows
    now = arrow.now()
    astart = now.shift(months=start)
    aend = now.shift(months=end)

    # read key & token
    kfcont = keyfile.readlines()
    key = kfcont[0].partition('\n')[0]
    token = kfcont[1].partition('\n')[0]

    # init client and get board
    client = TrelloClient(api_key=key, token=token)
    board = client.get_board(boardid)

    # grab visible (non-archived) cards within the given range
    openCards = [c for c in board.open_cards() if c.due_date == '' or arrow.get(c.due_date).is_between(astart, aend)]
    
    # if there are no open cards, just stop now
    if len(openCards) == 0:
        return
    
    # print header
    if color:
        print('${color1}'+board.name+' $hr')
    else:
        print(board.name+' -----------------')

    # find upcoming (non-overdue) cards
    activeCards = [c for c in openCards if c.due_date == '' or arrow.get(c.due_date).is_between(now, aend)]
    # filter out completed past items
    activeCards = [c for c in activeCards if c.get_list().name != target]
    
    # locate overdue cards
    overdueCards = [c for c in openCards if c.due_date != '' and (arrow.get(c.due_date).is_between(astart, now) and c.get_list().name != target)]

    # convert each card into an output line
    # print overdue cards first
    for card in overdueCards:
        if color:
            print(formatLine(card, linefmt, color='${color #FF0000}'))
        else:
            print(formatLine(card, linefmt, color=None))

    # and now upcoming items
    for card in activeCards:
        if color:
            print(formatLine(card, linefmt))
        else:
            print(formatLine(card, linefmt, color=None))

if __name__ == '__main__':
    checkBoard()
