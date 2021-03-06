package week11

import (
	"strconv"
)

//150. 逆波兰表达式求值 https://leetcode-cn.com/problems/evaluate-reverse-polish-notation/
//输入：tokens = ["2","1","+","3","*"]
//输出：9

type StringStack []string

func (s *StringStack) Push(r string) {
	*s = append(*s, r)
}

func (s *StringStack) Pop() string {
	last := (*s)[len(*s)-1]
	*s = (*s)[:len(*s)-1]
	return last
}

func calc(b, a, op string) int {
	ib, _ := strconv.Atoi(b)
	ia, _ := strconv.Atoi(a)
	switch op {
	case "+":
		return ia + ib
	case "-":
		return ia - ib
	case "*":
		return ia * ib
	case "/":
		return ia / ib
	}
	return 0
}

func evalRPN(tokens []string) int {
	stack := StringStack{}
	for _, token := range tokens {
		switch token {
		case "+", "-", "*", "/":
			stack.Push(strconv.Itoa(calc(stack.Pop(), stack.Pop(), token)))
		default:
			stack.Push(token)
		}
	}
	result, _ := strconv.Atoi(stack.Pop())
	return result
}
