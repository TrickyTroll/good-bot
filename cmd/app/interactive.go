// Testing verbose with goexpect
package main

import (
	"fmt"
	"log"
	"regexp"
	"time"

	"github.com/google/goexpect"
	"github.com/google/goterm/term"
)

const (
	timeout = 10 * time.Second
)

var (
	promptRE = regexp.MustCompile("#")
)

func main() {
	fmt.Println(term.Bluef("echo example"))

	e, _, err := expect.Spawn("/bin/bash", -1)
	fmt.Printf("%#v\n", e)
	fmt.Println(e.pty)
	if err != nil {
		log.Fatal(err)
	}
	defer e.Close()

	e.Expect(promptRE, timeout)
	e.Send("echo 'hello world'" + "\n")
	e.Expect(promptRE, timeout)
	e.Send("exit" + "\n")

	fmt.Println(term.Greenf("%s: result: %s\n", "foo", "bar"))
}
