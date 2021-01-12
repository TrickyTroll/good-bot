// Testing verbose with goexpect
package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"sort"

	expect "github.com/google/goexpect"
)

var (
	cliMap = map[string]string{
		"show system uptime": `Current time:      1998-10-13 19:45:47 UTC
Time Source:       NTP CLOCK
System booted:     1998-10-12 20:51:41 UTC (22:54:06 ago)
Protocols started: 1998-10-13 19:33:45 UTC (00:12:02 ago)
Last configured:   1998-10-13 19:33:45 UTC (00:12:02 ago) by abc
12:45PM  up 22:54, 2 users, load averages: 0.07, 0.02, 0.01
testuser@testrouter#`,
		"show version": `Cisco IOS Software, 3600 Software (C3660-I-M), Version 12.3(4)T
TAC Support: http://www.cisco.com/tac
Copyright (c) 1986-2003 by Cisco Systems, Inc.
Compiled Thu 18-Sep-03 15:37 by ccai
ROM: System Bootstrap, Version 12.0(6r)T, RELEASE SOFTWARE (fc1)
ROM:
C3660-1 uptime is 1 week, 3 days, 6 hours, 41 minutes
System returned to ROM by power-on
System image file is "slot0:tftpboot/c3660-i-mz.123-4.T"
Cisco 3660 (R527x) processor (revision 1.0) with 57344K/8192K bytes of memory.
Processor board ID JAB055180FF
R527x CPU at 225Mhz, Implementation 40, Rev 10.0, 2048KB L2 Cache
3660 Chassis type: ENTERPRISE
2 FastEthernet interfaces
4 Serial interfaces
DRAM configuration is 64 bits wide with parity disabled.
125K bytes of NVRAM.
16384K bytes of processor board System flash (Read/Write)
Flash card inserted. Reading filesystem...done.
20480K bytes of processor board PCMCIA Slot0 flash (Read/Write)
Configuration register is 0x2102
testrouter#`,
		"show system users": `7:30PM  up 4 days,  2:26, 2 users, load averages: 0.07, 0.02, 0.01
USER     TTY FROM              LOGIN@  IDLE WHAT
root     d0  -                Fri05PM 4days -csh (csh)
blue   p0 level5.company.net 7:30PM     - cli
testuser@testrouter#`,
	}
)

// ExampleVerbose changes the Verbose and VerboseWriter options.
func ExampleVerbose() {
	rIn, wIn := io.Pipe()
	rOut, wOut := io.Pipe()
	waitCh := make(chan error)
	outCh := make(chan string)
	defer close(outCh)

    exp, r, err := expect.SpawnGeneric(&)

