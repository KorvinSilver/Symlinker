# Symlinker

### A tool to create, search and find symbolic links, or modify their destinations.

Requirements: Python 3.6 or higher

Note: The examples show usage on Linux

#### View built-in help messages:

```
$ ./symlinker.py -h
```

```
$ ./symlinker.py link -h
```

```
$ ./symlinker.py search -h
```

```
$ ./symlinker.py find -h
```

```
$ ./symlinker.py batch -h
```

```
$ ./symlinker.py hardlink -h
```

#### Example usage:

Example directory structure:

```
.
├── Backup
├── .cfg
│   ├── alphalib32
│   ├── alphalib_old
│   ├── betalib32
│   ├── betalib_old
│   ├── gammalib32
│   ├── gammalib_old
│   ├── lib32
│   └── lib_old
├── .config
│   ├── alphalib32 -> ../.cfg/alphalib32
│   ├── betalib32 -> ../.cfg/betalib32
│   ├── gammalib32 -> ../.cfg/gammalib32
│   └── lib32 -> ../.cfg/lib32
├── Documents
├── .external
│   ├── Pictures
│   └── Videos
├── .internal
│   ├── Pictures
│   └── Videos
├── lorem_ipsum.txt
├── Pictures -> .internal/Pictures
├── symlinker.py
└── Videos -> .internal/Videos
```

##### Create link "Important" pointing to "Documents"

```
$ ./symlinker.py link Documents Important
```

##### Modify link "Important" to point to "Backup":

```
$ ./symlinker.py link -c Backup Important
```

##### Create link with absolute path:

```
$ ./symlinker.py link -a .external External
```

##### Modify link with absolute path:

```
$ ./symlinker.py link -ac .internal External
```

##### Search symlinks in current directory:

```
$ ./symlinker.py search .
External -> /home/dev/Symlinker_Tester/.internal
Important -> Backup
Pictures -> .internal/Pictures
Videos -> .internal/Videos
```

##### Search symlinks in current directory and all subdirectories:

```
$ ./symlinker.py search -r .
.config/lib32 -> ../.cfg/lib32
External -> /home/dev/Symlinker_Tester/.internal
Important -> Backup
Pictures -> .internal/Pictures
Videos -> .internal/Videos
.config/alphalib32 -> ../.cfg/alphalib32
.config/betalib32 -> ../.cfg/betalib32
.config/gammalib32 -> ../.cfg/gammalib32
```

##### Find symlinks in current directory that match pattern "lib32":

```
$ ./symlinker.py find . "lib32"
```

##### Find symlinks in current directory and all subdirectories that match pattern "lib32":

```
$ ./symlinker.py find -r . "lib32"
.config/lib32 -> ../.cfg/lib32
.config/alphalib32 -> ../.cfg/alphalib32
.config/betalib32 -> ../.cfg/betalib32
.config/gammalib32 -> ../.cfg/gammalib32
```

##### Change destination of symlinks in current directory by replacing pattern "internal" with a new pattern "external":

```
$ ./symlinker.py batch . "internal" "external"
```

see changes:

```
$ ./symlinker.py search .
External -> /home/dev/Symlinker_Tester/.external
Important -> Backup
Pictures -> .external/Pictures
Videos -> .external/Videos
```

##### Change destination of symlinks in current directory and all subdirectories by replacing pattern "lib32" with a new pattern "lib_old":

```
$ ./symlinker.py batch -r . "lib32" "lib_old"
```

see changes:

```
$ ./symlinker.py search -r .
.config/lib32 -> ../.cfg/lib_old
External -> /home/dev/Symlinker_Tester/.external
Important -> Backup
Pictures -> .external/Pictures
Videos -> .external/Videos
.config/alphalib32 -> ../.cfg/alphalib_old
.config/betalib32 -> ../.cfg/betalib_old
.config/gammalib32 -> ../.cfg/gammalib_old
```

##### Change destination but with absolute path:

```
$ ./symlinker.py batch -ra . "lib_old" "lib32"
```

see changes:

```
$ ./symlinker.py search -r .
.config/lib32 -> /home/dev/Symlinker_Tester/.cfg/lib32
External -> /home/dev/Symlinker_Tester/.external
Important -> Backup
Pictures -> .external/Pictures
Videos -> .external/Videos
.config/alphalib32 -> /home/dev/Symlinker_Tester/.cfg/alphalib32
.config/betalib32 -> /home/dev/Symlinker_Tester/.cfg/betalib32
.config/gammalib32 -> /home/dev/Symlinker_Tester/.cfg/gammalib32
```

##### Create hard link (not every file system supports this):

```
$ ./symlinker.py hardlink lorem_ipsum.txt lipsum.txt
```

More on hard links:
https://en.wikipedia.org/wiki/Hard_link


