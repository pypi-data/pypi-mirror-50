USAGE
=====

```
json-to-dir <json-file> [output-directory]
```

output-directory defaults to somewhere in /tmp.

EXAMPLE
=======

```
fiatjaf@menger ~> echo '[{"x": 23}, {"y": "23", "www": {"lll": "qwlekwq"}}]' > file
fiatjaf@menger ~> ./json-to-dir file
file written to /tmp/tmpXv1f5X.
fiatjaf@menger ~> tree /tmp/tmpXv1f5X/
/tmp/tmpXv1f5X/
├── 0
│   └── x
└── 1
    ├── www
    │   └── lll
    └── y

3 directories, 3 files
```
