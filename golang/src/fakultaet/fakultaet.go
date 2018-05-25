package main

import "fmt"
import "os"
import "strconv"

func main() {
	argsWithoutProg := os.Args[1:]
	if len(argsWithoutProg) == 0 {
		fmt.Println("Bitte um Zahl > 0. Bye")
		os.Exit(2)
	}
	args := argsWithoutProg[0]
	n, err := strconv.Atoi(args)
	if err != nil {
		fmt.Println(err)
		os.Exit(2)
	}
	if n < 1 {
		fmt.Println("Bitte um Zahl > 0. Bye")
		os.Exit(2)
	}
	fmt.Println("Fak(", n, ")=", fak(n))

}
func fak(n int) int {
	if n == 1 {
		return 1
	} else {
		return n * fak(n-1)
	}
}
