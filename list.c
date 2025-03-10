#include <stdio.h>
#include <stdlib.h>

typedef struct slist{
   int data;
   struct slist *next;
} slist;

slist *newnode(int data, slist *next){
   slist *node = (slist*)malloc(sizeof(slist));
   node->data = data;
   node->next = next;
   return node;
}

void rev(slist **root){
   if (!*root || !(*root)->next) return;

   slist *prev = NULL, *curr = *root, *next = NULL;
   while (curr){
      next = curr->next;
      curr->next = prev;
      prev = curr;
      curr = next;
   }
   *root = prev;
}

int hasCycle(slist *root){
   slist *slow = root, *fast = root;

   while (fast && fast->next){
      slow = slow->next;
      fast = fast->next->next;
      if (slow == fast) return 1;
   }
   return 0;
}

slist *merged(slist *s1, slist *s2){
   if (!s1) return s2;
   if (!s2) return s1;

   slist sorted = {0, NULL}, *tail = &sorted;
   while (s1 && s2){
      if (s1->data < s2->data){
         tail->next = s1;
         s1 = s1->next;
      } else{
         tail->next = s2;
         s2 = s2->next;
      }
      tail = tail->next;
   }
   tail->next = s1 ? s1 : s2;
   return sorted.next;
}

void print(slist *root){
   while(root){
      printf("%d->", root->data);
      root = root->next;
   }
   printf("NULL\n");
}

int main(void){
   slist *head = 
      newnode(1, newnode(2, newnode(3, newnode(4, newnode(5, NULL)))));

   print(head);   // 1->2->3->4->5->NULL
   rev(&head);
   print(head);   // 5->4->3->2->1->NULL

   slist *cyc1 = newnode(1, newnode(2, newnode(3, newnode(4, NULL))));
   cyc1->next->next->next->next = cyc1->next;    // 1->2->3->4->2
   
   slist *cyc2 = newnode(1, newnode(2, newnode(3, newnode(4, NULL))));
   cyc2->next->next->next->next = cyc2->next->next;   // 1->2->3->4->3

   printf("%d\n", hasCycle(head));     // 0
   printf("%d\n", hasCycle(cyc1));     // 1
   printf("%d\n", hasCycle(cyc2));     // 1

   slist *sort1 = newnode(1, newnode(3, newnode(5, NULL)));
   slist *sort2 = newnode(2, newnode(4, newnode(6, NULL)));
   slist *sort3 = merged(sort1, sort2);
   print(sort3);  // 1->2->3->4->5->6->NULL
   
   return 0;
}
