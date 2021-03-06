package week11

type ListNode struct {
	Next *ListNode
	Val  int
}

// 206. 反转链表 https://leetcode-cn.com/problems/reverse-linked-list/
func reverseList(head *ListNode) *ListNode {
	var prev *ListNode
	for head != nil {
		next := head.Next
		head.Next = prev
		prev = head
		head = next
	}
	return prev
}
