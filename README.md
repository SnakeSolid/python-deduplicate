# Deduplicate

Python application to search similar files and replace them to hard
link. Created and tested with Python 2.7.

Files are considered identical if they have same md5 hash, sha256 hash
and size.

### Command line

Optional arguments:

+ -h or --help - show this help message and exit
+ -s SIZE or --min-size SIZE - minimal file size in bytes

positional arguments:

+ file - list of files or directories to analyze

### License

All source code available under MIT License.
