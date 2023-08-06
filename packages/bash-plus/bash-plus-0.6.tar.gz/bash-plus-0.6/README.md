# bash-plus

`bash-plus` is a preprocesser for shell scripts that provides the following:

* Argument handling using [argbash.io](https://argbash.io)
* Common utility functions.

example:
```
bash-plus script.sh > sponge script.sh
```

Bash plus will then run argbash and embed the common functions into the result.

The processing of bash-plus can be reversed using:
```bash
bash-plus script.sh clean > sponge script.sh
```

This is useful to run before commiting into git and only running compile step during build.


## Common Functions

| Function                     | Args  | Description                            |
| ---------------------------- | ----- | -------------------------------------- |
| epoch                        |       | time in milliseconds                   |
| stopwatch                    | epoch |                                        |
| error                        | msg   |                                        |
| success                      | msg   |                                        |
| info                         | msg   |                                        |
| fatal                        | msg   | Logs an error and then exits with `1`  |
| logv                         | msg   | Log only if `$debug == 'true'`         |
| log                          | msg   | Log to `stderr` with a running time    |
| delete_on_exit               | file  | Deletes the file when the script exits |
| hr, hr1, hr2                 |       | Prints a horizontal rule               |
| strict_mode, strict_mode_off |       | Turn strict mode on or off             |
| is_linux, is_mac             |       |                                        |
| is_jenkins, is_travis, is_ci |       |                                        |
|                              |       |                                        |

