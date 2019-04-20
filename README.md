# ome_pystasigen

ome_pystasigen (Orange Mirror Entertainment Python Static Site Generator (that's a mouth full)) is a set of
Python scripts I use to generate my [website](https://orangemirrorentertainment.com). As of April 20th, 2019
it generates a blog from Markdown sources and an accompanying feed. The Markdown parser in particular is pretty
bare bones and a work in progress. You should probably not use this tool to generate your own site, but
I thought it was worthwhile to put it on the public web regardless.

## Requirements

A server to host your blog on and a domain you control.
A version of Python > 3.6, because ome_pystasigen uses Pathlib and expects UTF-8 sources.
