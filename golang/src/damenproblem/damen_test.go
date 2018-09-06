package main

import "testing"
import "fmt"

func Testbedroht(t *testing.T) {
	type testdata struct {
		expected        bool
		pos             int
		bestehendeDamen []int
	}
	tests := []testdata{
		{true, 2, []int{3, 1, 2, 0}},
		{false, 8, []int{3, 1, 2, 0}},
	}

	for i, test := range tests {
		fmt.Printf("Excuting test %d\n", i)
		ret := bedroht(test.pos, test.bestehendeDamen)
		if ret != test.expected {
			t.Logf("%v - Pos:%v   BestehendeDamen:%v", ret, test.pos, test.bestehendeDamen)
		}
	}
}

/*func TestQueenUnderAttac(t *testing.T) {
	type testdata struct {
		expected bool
		existingQueens []Position
		newQueen Position
	}

	tests := []testdata{
		{true, []Position{{0,0}}, Position{1,1}},
		{true, []Position{{0,0}}, Position{1,0}},
		{true, []Position{{0,0}}, Position{0,1}},
		{true, []Position{{0,0}}, Position{2,2}},
		{true, []Position{{0,0}, {1,2}}, Position{2,1}},
		{true, []Position{{0,2}, {1,0}, {2,3}}, Position{3,0}},
		{false, []Position{{0,2}, {1,0}, {2,3}}, Position{3,1}},
		{true, []Position{{0,2}, {1,0}, {2,3}}, Position{3,2}},
		{true, []Position{{0,2}, {1,0}, {2,3}}, Position{3,3}},
	 }


	for i, test := range tests {
		fmt.Printf("Excuting test %d\n",i)
		ret := QueenUnderAttac(test.newQueen, test.existingQueens)
		if(ret != test.expected) {
		t.Logf("%v - ThisQueen:%v   OtherQueens%v",ret, test.newQueen, test.existingQueens)
		}
	}
}*/
