# Definition for singly-linked list.
class ListNode:
     def __init__(self, val=0, next=None):
         self.val = val
         self.next = next

class Solution:
    def mergeTwoLists(self, list1: ListNode, list2: ListNode) -> ListNode:
        finalList = []
        print(list1.val)
        print(list2.val)


obj = Solution()
obj.mergeTwoLists(ListNode(1,ListNode(2,ListNode(3,ListNode))), ListNode(1,ListNode(4,ListNode(5,ListNode))))