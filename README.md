# good-bot
Automating the recording of documentation videos.

## For the old version

To see the first release, please go to the
[old](https://github.com/TrickyTroll/good-bot/tree/old) branch.

## Initializing the Go program

### GOPATH if using zsh

Add this line to your `zshrc`:

```zsh
export GOPATH=$HOME/go
```

Then, update your current session with

```zsh
source ~/.zshrc
```

All future sessions with have `~/go` as their GOPATH.

### Checking for Go env vars

#### Checking for GOPATH

```zsh
echo $GOPATH
```

#### Checking for all vars

```zsh
go env
```

### Creading the `.mod` and `.sum` files

To create the module file:

```zsh
go mod init example.com/path/to/repo
```

To create the `.sum` file

```zsh
go install example.com/path/to/repo
```

**These files should both be [included](https://golang.org/doc/code.html) to VCS**