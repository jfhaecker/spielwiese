package main

import (
	"fmt"
	"math"
)


const damen int = 8 
var zeileFrei = [damen+1] bool{}
var spalteFrei = [damen+1] bool{}
var aufstgDiagFrei = [damen*2] bool{true}
var abstgDiagFrei = [damen*2] bool {}
var loesung = [damen+1] int{}


type Position struct {
	row, col int
}


func main() {

	Damenproblem(4)
	//setzeDame(1, 1)
}

func Damenproblem(n int) []Position {
	var positions = make([]Position, n)
	hasSolution := Damenwahl(n, 0, positions)
	if(hasSolution == true ) {
		return positions;
	} else {
		return nil
	}
	
}

func Damenwahl(n int, row int, positions []Position) bool {
	if (n == row) {
		return true
	}
	col := 0
	for col = 0; col < n; col++ {
	
	
		for k, queen := range positions {
			fmt.Println("Position:",k,":",queen)
		}

	}	 
	return false
}

func QueenUnderAttac(thisQueen Position, otherQueens []Position) bool {
	for _, queen := range otherQueens {
		if queen.row == thisQueen.row || queen.col == thisQueen.col {
			return true
		}
	} 
	return false
}



	/*var l =  math.Log10( float64(damen))
	var f = math.Floor(l)
	fmt.Println(" l:", l, "  f:", f);
	var hasQueen =  [damen][damen]int{}
//	fmt.Printf("%v", hasQueen)
	fmt.Println()
	hasQueen[0][1] =  1
	hasQueen[7][3] =  1
	printSchachbrett(hasQueen)
        var  u int = findDiag(0,1)
	fmt.Println(u);
}*/

func setzeDame(zeile int , spalte int) {   //, zeilen[]int, spalten[]int ) {
	loesung[zeile] = spalte
	zeileFrei[spalte] = false
	aufstgDiagNichtFrei(zeile, spalte)
	fmt.Println(aufstgDiagFrei)
	druckeSchachbrett()
}

func aufstgDiagNichtFrei(zeile int, spalte int) {
	index := getIndexForAufstgDiag(zeile, spalte)
	aufstgDiagFrei[index]=false

}

func getIndexForAufstgDiag(zeile int, spalte int) int {
	return int(damen+zeile-spalte)
}

func druckeSchachbrett() {
	for z:=damen; z>0; z-- {
		fmt.Printf("%1d", z)
		for s:=1; s<damen+1; s++ {
			c := "."
			if(loesung[z] == s) {
				c = "Q"
			}
			index := getIndexForAufstgDiag(z, s)
			if(aufstgDiagFrei[index] == false) {
				c = "x"
			}
			fmt.Printf("%2s", c)
		}
		fmt.Println("")
	}
	fmt.Print(" ")
	for s:=1; s<damen+1; s++ {
		fmt.Printf("%2d", s)
	}
	fmt.Println(" ")

}

func damenproblem(schachbrett[][]int ) {
}

func helpLog10(x int)  {
	l := math.Log10(float64(x))
	f := math.Floor(l)
	c := math.Ceil(l)
	fmt.Printf("X: %v, Log: %v, Floor: %v, Ceil: %v", x, l, f, c)
}



func printSchachbrett(data [damen][damen]int) {
	var schachfeld = [2] string {".", "Q"}
	fmt.Print("   |");
	for i := 0; i < damen; i++ {
		fmt.Printf("%02d|", i)
	}
	fmt.Println()
	for i,h := range  data {
		//fmt.Printf("%v", i)// math.Log10(float64(i)))
		fmt.Printf("%02d|", i)
		//helpLog10(i)
		for _,cell := range h  {
			fmt.Printf("%3s", schachfeld[cell])
		}
	fmt.Println()
	}
}


func findDiag(x,y  int)  int  {
	return x-y
}
