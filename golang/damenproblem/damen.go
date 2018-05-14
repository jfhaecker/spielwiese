package main

import (
	"fmt"
	"math"
)


const damen int =13 

func main() {

	fmt.Println("  %v", math.Log10( float64(damen)))
	var hasQueen  [damen][damen]bool
	fmt.Printf("%v", hasQueen)
	fmt.Println()
	hasQueen[0][1] = true
	printBoolArray(hasQueen)
        var  u int = findDiag(0,1)
	fmt.Println(u);
}

func printBoolArray(data [damen][damen]bool) {
	fmt.Print(" ");
	for i := 0; i < damen; i++ {
		fmt.Printf(" %v", i)
	}
	fmt.Println()
	for i,h := range  data {
		fmt.Printf("%v ", i)
		for _,cell := range h  {
			if cell == true {
				fmt.Print("Q ")
			} else {
				fmt.Print("+ ")
			}
		}
	fmt.Println()
	}
}


func findDiag(x,y  int)  int  {
	return x-y
} 
