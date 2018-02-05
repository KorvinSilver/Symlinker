# Symlinker

### A tool to create symbolic links or modify their destinations.

Requirements: Python 3.6 or higher

#### Example usage:

Example Directory structure:
- .cfg
    - lib_old
    - lib32
    - alphalib_old
    - alphalib32
    - betalib_old
    - betalib32
    - gammalib_old
    - gammalib32
- .config
    - lib32
    - alphalib32
    - betalib32
    - gammalib32
- .external
    - Pictures
    - Videos
- .internal
    - Pictures
    - Videos
- Backup
- Documents
- Pictures
- Videos
- symlinker.py

##### Create link "Important" pointing to "Documents"

```
$ ./symlinker.py link Documents Important
```

##### Modify link "Important" to point to "Backup":

```
$ ./symlinker.py link -c Backup Important
```

##### Search symlinks in current directory:

```
$ ./symlinker.py search .
Important --> Backup
Pictures --> .internal/Pictures
Videos --> .internal/Videos
```

##### Search symlinks in current directory and all subdirectories:

```
$ ./symlinker.py search -r .
.config/lib32 --> ../.cfg/lib32
Important --> Backup
Pictures --> .internal/Pictures
Videos --> .internal/Videos
.config/alphalib32 --> ../.cfg/alphalib32
.config/betalib32 --> ../.cfg/betalib32
.config/gammalib32 --> ../.cfg/gammalib32
```

##### Find symlinks in current directory that match pattern "lib32":

```
$ ./symlinker.py find . "lib32"
```

##### Find symlinks in current directory and all subdirectories that match pattern "lib32":

```
$ ./symlinker.py find -r . "lib32"
.config/lib32 --> ../.cfg/lib32
.config/alphalib32 --> ../.cfg/alphalib32
.config/betalib32 --> ../.cfg/betalib32
.config/gammalib32 --> ../.cfg/gammalib32
```

##### Change destination of symlinks in current directory by replacing pattern "internal" with a new pattern "external":

```
$ ./symlinker.py batch . "internal" "external"
```

see changes:

```
$ ./symlinker.py search .                     
Important --> Backup
Pictures --> .external/Pictures
Videos --> .external/Videos
```

##### Change destination of symlinks in current directory and all subdirectories by replacing pattern "lib32" with a new pattern "lib_old":

```
$ ./symlinker.py batch -r . "lib32" "lib_old"
```

see changes:

```
$ ./symlinker.py search -r .                 
.config/lib32 --> ../.cfg/lib_old
Important --> Backup
Pictures --> .external/Pictures
Videos --> .external/Videos
.config/alphalib32 --> ../.cfg/alphalib_old
.config/betalib32 --> ../.cfg/betalib_old
.config/gammalib32 --> ../.cfg/gammalib_old
```
