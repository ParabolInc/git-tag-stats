import os
import csv
import pipes
import re
from datetime import datetime

def get_tags_and_dates():
    tags_pipe = pipes.Template()
    tags_pipe.prepend("git for-each-ref --sort=taggerdate --format '%(refname) %(taggerdate)' refs/tags",
      ".-")
    lines = tags_pipe.open("pipefile", "r").read().splitlines()
    tags_and_dates = [ l[10:].split(" ", 1) for l in lines ]
    tags_and_dates = [
      (
        t,
        datetime.strptime(d, "%a %b %d %H:%M:%S %Y %z")
      ) for (t, d) in tags_and_dates
    ]
    return tags_and_dates

def calc_turnover(tags_and_dates):
    t1 = iter(tags_and_dates)
    t2 = iter(tags_and_dates)
    next(t2)
    turnover_list = []
    for tag_from, tag_to in zip(t1, t2):
        stats_pipe = pipes.Template()
        stats_pipe.prepend("git diff --shortstat %s..%s" %
          (tag_from[0], tag_to[0]),
          ".-")
        stats = stats_pipe.open("pipefile", "r").read()
        m = re.match(
          r"\s*([0-9]+) files changed, ([0-9]+) insertions\(\+\), ([0-9]+) deletions\(-\)",
          stats)
        tag_turnover = {
          "tag": tag_to[0],
          "date": tag_to[1],
          "files_changed": int(m.group(1)),
          "insertions": int(m.group(2)),
          "deletions": int(m.group(3))
        }
        turnover_list.append(tag_turnover)
    return turnover_list

def emit_csv(filename, turnover_list):
    with open(filename, 'w') as csvfile:
        fieldnames = ["date", "tag", "files_changed", "insertions", "deletions"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in turnover_list:
            writer.writerow(row)

def main(repo_dir, output_filename):
    orig_dir = os.getcwd()
    os.chdir(repo_dir)
    tds = get_tags_and_dates()
    turnover_list = calc_turnover(tds)
    os.chdir(orig_dir)
    emit_csv(output_filename, turnover_list)
