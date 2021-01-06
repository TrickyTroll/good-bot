package main

import (
	"flag"
	"fmt"
	"log"
	"regexp"
	"strings"
	"time"

	expect "github.com/google/goexpect"
	"github.com/google/goterm/term"
)

const (
	timeout = 10 * time.Minute
)

var (
	/*
		addr = flag.String("address", "", "address of telnet server")
		user = flag.String("user", "", "username to use")
		pass = flag.String("pass", "", "password to use")
		cmd  = flag.String("cmd", "", "command to run")

		userRE   = regexp.MustCompile("username:")
		passRE   = regexp.MustCompile("password:")
		promptRE = regexp.MustCompile("%")
	*/
	cmd      = "echo"
	args     = "'hello world'"
	flags    = ""
	promptRE = regexp.MustCompile("$")
	all      = [3]string{cmd, args, flags}
)

func main() {
	flag.Parse()
	fmt.Println(term.Bluef("echo example"))
	e, _, err := expect.Spawn("/bin/bash", -1)
	if err != nil {
		log.Fatal(err)
	}
	defer e.Close()

	e.Expect(promptRE, timeout)
	e.Send(parse() + "\n")
	e.Send("exit\n")

	fmt.Println(term.Greenf("Done"))
}

func parse() string {

	var parsed strings.Builder

	for _, element := range all {
		if len(element) > 0 {
			parsed.WriteString(element)
			parsed.WriteString(" ")
		}
	}
	return parsed.String()
}
