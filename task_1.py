class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data: int):
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        current = self.head
        while current:
            print(current.data, "--> ", end="")
            current = current.next
        print("None")

    
    def reverse(self):
        """Реверсування однозв'язного списку."""
        prev = None
        current = self.head

        while current:
            nxt = current.next   # запам'ятовуємо наступний
            current.next = prev  # змінюємо напрямок
            prev = current       # рухаємо prev і current вперед
            current = nxt

        self.head = prev

   
    def merge_sort(self, head):
        """Сортування однозв'язного списку методом злиття."""

        if head is None or head.next is None:
            return head

        middle = self.get_middle(head)
        next_to_middle = middle.next
        middle.next = None

        left = self.merge_sort(head)
        right = self.merge_sort(next_to_middle)

        sorted_list = self.sorted_merge(left, right)
        return sorted_list

    # Допоміжний метод
    def get_middle(self, head):
        """Пошук середнього елемента (метод двох вказівників)."""
        if head is None:
            return head

        slow = head
        fast = head

        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        return slow

    # Алгоритм злиття двох відсортованих списків
    def sorted_merge(self, a, b):
        if a is None:
            return b
        if b is None:
            return a

        if a.data <= b.data:
            result = a
            result.next = self.sorted_merge(a.next, b)
        else:
            result = b
            result.next = self.sorted_merge(a, b.next)

        return result

   
    def merge_sorted_lists(self, list1, list2):
        """Об'єднання двох відсортованих списків у один."""
        return self.sorted_merge(list1.head, list2.head)


if __name__ == '__main__':

    first_list = LinkedList()

    first_list.insert_at_beginning(5)
    first_list.insert_at_beginning(10)
    first_list.insert_at_beginning(15)
    first_list.insert_at_end(20)
    first_list.insert_at_end(25)
    print("\nЗв'язний список:")
    first_list.print_list()

    first_list.reverse()
    print("\nЗв'язний список після реверсування:")
    first_list.print_list()

    first_list.head = first_list.merge_sort(first_list.head)
    print("\nЗв'язний список відсортовано:")
    first_list.print_list()

    # створимо другий список
    second_list = LinkedList()
    second_list.insert_at_beginning(1)
    second_list.insert_at_beginning(3)
    second_list.insert_at_beginning(7)

    print("\nДругий список:")
    second_list.print_list()
    
    print("\nДругий список після сортування:")
    second_list.head = second_list.merge_sort(second_list.head)
    second_list.print_list()

    merged_head = first_list.merge_sorted_lists(first_list, second_list)
    merged_list = LinkedList()
    merged_list.head = merged_head

    print("\nОб'єднаний відсортований список:")
    merged_list.print_list()
    print()