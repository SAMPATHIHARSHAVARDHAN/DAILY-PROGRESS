#include <stdio.h> 
#include <stdlib.h> 
// Function to swap two integers void swap(int *a, int *b) { 
    int temp = *a;     *a = *b; 
    *b = temp; 
} 
// Structure for heap typedef struct { 
    int *array; // Array to store heap elements     int capacity; // Maximum possible size of min heap     int size; // Current number of elements in min heap 
    int is_min_heap; // Flag to indicate if it's a min heap (1) or max heap (0) } Heap; 
// Function to create a new heap 
Heap *createHeap(int capacity, int is_min_heap)  { 
    Heap *heap = (Heap *)malloc(sizeof(Heap));     if (heap == NULL)  
   { 
        perror("Memory allocation failed"); 
        exit(EXIT_FAILURE); 
    } 
    heap->capacity = capacity;     heap->size = 0; 
    heap->is_min_heap = is_min_heap; 
    heap->array = (int *)malloc(capacity * sizeof(int)); 
    if (heap->array == NULL) {         perror("Memory allocation failed"); 
        exit(EXIT_FAILURE); 
    } 
    return heap; 
} 
// Function to heapify a subtree rooted with node i (zero-based index) void heapify(Heap *heap, int i)  
{ 
    int smallest_or_largest = i; 
    int left = 2 * i + 1;     int right = 2 * i + 2; // Determine smallest or largest depending on whether it's a min or max heap     if (heap->is_min_heap) 
   { 
        if (left < heap->size && heap->array[left] < heap->array[smallest_or_largest])  
       { 
            smallest_or_largest = left; 
        } 
        if (right < heap->size && heap->array[right] < heap->array[smallest_or_largest])  
       { 
            smallest_or_largest = right; 
        } 
    } else  
       { 
        if (left < heap->size && heap->array[left] > heap->array[smallest_or_largest])  
       { 
            smallest_or_largest = left; 
        } 
        if (right < heap->size && heap->array[right] > heap->array[smallest_or_largest]) 
       { 
            smallest_or_largest = right; 
        } 
    } 
// If smallest_or_largest is not the root, swap and recursively heapify the affected subtree     if (smallest_or_largest != i)  
   { 
       swap(&heap->array[i], &heap->array[smallest_or_largest]);         heapify(heap, smallest_or_largest); 
    } 
} 
// Function to delete an element from the heap void deleteElement(Heap *heap, int key)  
{ 
    int i; 
    for (i = 0; i < heap->size; i++)  
   { 
        if (heap->array[i] == key) 
            break; 
    } 
    if (i == heap->size)  
    { 
        printf("Element %d not found in the heap.\n", key);         return; 
    } 
    // Replace the key to be deleted with the last element     heap->array[i] = heap->array[heap->size - 1];  heap->size--; // Heapify the root 
    heapify(heap, i); 
} 
// Function to display the elements of the heap 
void displayHeap(Heap *heap)  
{ 
    printf("Heap elements: "); 
    int i; 
    for (i= 0; i < heap->size; i++)  
   { 
        printf("%d ", heap->array[i]); 
    } 
    printf("\n"); 
} 
// Function to free memory used by the heap void freeHeap(Heap *heap)  
{ 
     free(heap->array);     free(heap); 
} int main()  
{ 
    // Example usage: 
    Heap *minHeap = createHeap(20, 1); // Create a min heap with capacity 20 
    Heap *maxHeap = createHeap(20, 0); // Create a max heap with capacity 20 
 // Insert elements into the min heap 
    int minHeapElements[] = {3, 2, 1, 7, 8, 4, 10, 16},i; 
    int numElements = sizeof(minHeapElements) / sizeof(minHeapElements[0]);     for ( i = 0; i < numElements; i++) 
   { 
        minHeap->array[minHeap->size++] = minHeapElements[i]; 
    } 
    // Heapify all internal nodes 
    for ( i = (minHeap->size - 2) / 2; i >= 0; i--)  
    { 
        heapify(minHeap, i); 
    } 
 // Insert elements into the max heap 
    int maxHeapElements[] = {10, 8, 16, 14, 7, 9, 3, 2}; 
    numElements = sizeof(maxHeapElements) / sizeof(maxHeapElements[0]);     for (i = 0; i < numElements; i++) 
   { 
        maxHeap->array[maxHeap->size++] = maxHeapElements[i]; 
} 
    // Heapify all internal nodes 
    for (i = (maxHeap->size - 2) / 2; i >= 0; i--)  
   { 
        heapify(maxHeap, i); 
    } 
    // Display the content of both heaps     printf("Min Heap:\n");     displayHeap(minHeap);     printf("Max Heap:\n");     displayHeap(maxHeap); // Delete an element from the min heap 
    deleteElement(minHeap, 4); // Delete element 4 from min heap     printf("After deleting 4 from Min Heap:\n");     displayHeap(minHeap); // Delete an element from the max heap 
    deleteElement(maxHeap, 16); // Delete element 16 from max heap     printf("After deleting 16 from Max Heap:\n"); 
    displayHeap(maxHeap); // Free allocated memory     freeHeap(minHeap); 
    freeHeap(maxHeap);    return 0; 
} 

