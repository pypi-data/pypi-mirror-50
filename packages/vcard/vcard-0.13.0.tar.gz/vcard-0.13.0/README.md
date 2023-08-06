# [vCard module](https://gitlab.com/victor-engmark/vcard)

[![pipeline status](https://gitlab.com/victor-engmark/vcard/badges/master/pipeline.svg)](https://gitlab.com/victor-engmark/vcard/commits/master)

This program can be used for strict validation and parsing of vCards. It currently supports [vCard 3.0 (RFC 2426)](https://tools.ietf.org/html/rfc2426).

Additional scripts:

* [`format-TEL.sh`](./format-TEL.sh) - Format phone numbers according to national standards
* [`split.sh`](./split.sh) - Split a multiple vCards file into individual files
* [`sort-lines.sh`](./sort-lines.sh) - Sort vCard property lines according to a custom key
* [`join-lines.sh`](./join-lines.sh) - Join previously split vCard lines
* [`split-lines.sh`](./split-lines.sh) - Split long vCard lines

## Installation / upgrade

    sudo pip install --upgrade vcard

## Examples

* [`minimal.vcf`](test/minimal.vcf)
* [`maximal.vcf`](test/maximal.vcf)

## Development

**Download:**

    git clone --recurse-submodules git@gitlab.com:victor-engmark/vcard.git

**Release:**

1. Bump the [version](vcard/__init__.py).
2. Commit everything.
2. `make clean test-clean test release`
3. `git push && git push --tags`

Development requirements:

- Docker
- GNU Make

Release requirements:

- GnuPG
