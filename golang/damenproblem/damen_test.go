package main
import "testing"


func TestQueenUnderAttac(t *testing.T) {
	type testdata struct {
		expected bool
		queens []Position  // 0 = queen to test; 1: = other queens 
	}


        thisQueen := Position{0, 1}
	otherQueens := []Position{ {0,0}} 
	ret := QueenUnderAttac(thisQueen, otherQueens)
	t.Errorf("%v - ThisQueen:%v   OtherQueens%v",ret, thisQueen, otherQueens)
}
