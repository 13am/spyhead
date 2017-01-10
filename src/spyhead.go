package main

import (
	"flag"
	"fmt"
	"os"
	"bufio"
	"regexp"
	"compress/gzip"
	"io"
)


var SEP string
var IPNAME string

func parseArgs() {

	flag.StringVar(&SEP, "sep", "", "Column delimiter")
	flag.Parse()

	if SEP == "space" {
		SEP = ""
	}
	if SEP == "tab" {
		SEP = "\\t"
	}

	IPNAME = flag.Arg(0)

}


func main() {

	parseArgs()

	var filePtr *os.File
	var err error
	var ioReader io.Reader
	var byteBuffer []byte

	// check if the input is to be read from from a file
	ioReader = os.Stdin
	if IPNAME != "" {
		filePtr, err = os.Open(IPNAME)
		ioReader = filePtr
		if err != nil {
			fmt.Println("Error: the input could not be read.")
			os.Exit(-1)
		}
		// check if the input is gzipped
		// see http://www.ietf.org/rfc/rfc1952.txt
		byteBuffer = make([]byte, 2)
		nRead, err := io.ReadAtLeast(ioReader, byteBuffer, 2)
		filePtr.Close()
		if err != nil || nRead < 2 {
			fmt.Println(err)
			fmt.Println("Error: the input could not be read.")
			os.Exit(-1)
		}
		filePtr, err = os.Open(IPNAME)
		ioReader = filePtr
		if byteBuffer[0] == 31 && byteBuffer[1] == 139 {
			reader, err := gzip.NewReader(filePtr)
			if err != nil {
				fmt.Println("Error: the input could not be read.")
				os.Exit(-1)
			}
			ioReader = reader
		}
	}
	
	// read at most 100 first lines into a slice of strings
	scanner := bufio.NewScanner(ioReader)
	lines := make([]string, 100)
	lineCounter := 0
	for ; lineCounter < len(lines) && scanner.Scan(); lineCounter++ {
		lines[lineCounter] = scanner.Text()
	}
	if IPNAME != "" {
		filePtr.Close()
	}
	lines = lines[0:lineCounter]
	
	// try to deduce the delimiter if it was not given
	if SEP == "" {

		candidates := []string{" ", "\\t", ";", "\\s"}
		counts := make(map[string]map[int]bool)
		
		for _, candidate := range candidates {
			counts[candidate] = make(map[int]bool)
			iSep := regexp.MustCompile(candidate)
			for _, line := range lines {
				l := len(iSep.Split(line, -1))
				if l > 1 {
					counts[candidate][l] = true
				}
			}
		}

		ok := false
		for _, candidate := range candidates {
			if len(counts[candidate]) == 1 {
				SEP = candidate
				ok = true
				break
			}
		}
		if ok == false {
			fmt.Println("Error: the column delimiter could not be deduced. " +
				        "Please give it explicitly with the --sep argument.")
			os.Exit(-1)
		}

	}

	// show the output
	reSep := regexp.MustCompile(SEP)
	header := reSep.Split(lines[0], -1)
	for i, val := range header {
		fmt.Println(i+1, ":", val)
	}

}
