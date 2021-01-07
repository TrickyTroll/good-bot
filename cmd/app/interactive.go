package main

import (
	"log"
	"math/rand"
	"os"
	"os/exec"
	"time"

	expect "github.com/Netflix/go-expect"
)

var (
	run = "echo 'hello world'"
)

func main() {
	c, err := expect.NewConsole(expect.WithStdout(os.Stdout))
	if err != nil {
		log.Fatal(err)
	}
	defer c.Close()

	// Random typing
	rand.Seed(time.Now().Unix())

	cmd := exec.Command("/bin/bash")
	cmd.Stdin = c.Tty()
	cmd.Stdout = c.Tty()
	cmd.Stderr = c.Tty()

	go func() {
		c.ExpectEOF()
	}()

	err = cmd.Start()
	if err != nil {
		log.Fatal(err)
	}

	time.Sleep(time.Second)
	for _, rune := range run {
		c.Send(string(rune))
		time.Sleep(time.Duration(rand.Float32()))
	}
	c.Send("\n")
	time.Sleep(time.Second)
	c.Send("exit\n")
	c.Close()
}
