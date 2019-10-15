package main

import "fmt"
import "errors"

type Node struct {
	str  string
	next *Node
}

func evlAppend(root *Node, str string) *Node {
	if root == nil {
		return &Node{str: str, next: nil}
	}

	curr := root
	for curr.next != nil {
		curr = curr.next
	}
	curr.next = &Node{str: str, next: nil}
	return root
}

func evlPrepend(root *Node, str string) *Node {
	if root == nil {
		return &Node{str: str, next: nil}
	}

	curr := &Node{str: str, next: nil}
	curr.next = root
	root = curr
	return root
}

func evlInsert(root *Node, str string, pos int) (*Node, error) {
	if root == nil {
		return &Node{str: str, next: nil}, nil
	}

	curr := root
	prev := root
	for i := 0; i < pos; i++ {
		prev = curr
		curr = curr.next
		if curr == nil {
			return root, errors.New("Peng krach rummsdibums")
		}
	}
	prev.next = &Node{str: str, next: curr}
	return root, nil
}

func printlist(root *Node) {
	fmt.Print("Liste:")
	curr := root

	for curr != nil {
		fmt.Print(curr.str)
		//fmt.Println(curr.next)
		curr = curr.next
	}
	fmt.Println()
}

func toArray(root *Node) []string {
	curr := root
	output := make([]string, 0)
	for curr != nil {
		output = append(output, curr.str)
		curr = curr.next
	}
	return output
}

func main() {
	str := "Einfach verzeigerte Liste"
	str2 := " ollaH"
	var root *Node
	fmt.Println("-----------Einfaches append")
	for i := range str {
		root = evlAppend(root, string(str[i]))
	}
	printlist(root)
	fmt.Printf("%#v\n", toArray(root))

	fmt.Println("-----------Einfaches prepend")
	for i := range str2 {
		root = evlPrepend(root, string(str2[i]))
	}
	printlist(root)
	fmt.Printf("%#v\n", toArray(root))

	fmt.Println("-----------Einfaches insert")
	root, err := evlInsert(root, "w", 18)
	if err == nil {
		printlist(root)
	} else {
		fmt.Println("Error")
		fmt.Println(err)
	}
	fmt.Printf("%#v\n", toArray(root))

	arr := toArray(root)
	fmt.Println("-------------------")
	for num, i := range arr {
		fmt.Printf("%v:%v\n", num, i)
	}

	fmt.Println("-------------------")
	fmt.Println("-----------kaputtes insert")
	root, err = evlInsert(root, "X", 32)
	if err == nil {
		printlist(root)
	} else {
		fmt.Println(err)
		printlist(root)
	}
}
