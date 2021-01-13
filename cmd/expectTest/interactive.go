package main

import (
	"log"
	"os"
	"os/exec"
	"time"

	expect "github.com/Netflix/go-expect"
)

func main() {
	cmd := exec.Command("bash")
	cmd.Stdin = os.Stdin
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	go func() {
		c.ExpectEOF()
	}()

	err = cmd.Start()
	if err != nil {
		log.Fatal(err)
	}

	time.Sleep(time.Second)
	c.Send("echo 'hello world'")
	time.Sleep(time.Second)
	c.SendLine("exit")

	err = cmd.Wait()
	if err != nil {
		log.Fatal(err)
	}
}
