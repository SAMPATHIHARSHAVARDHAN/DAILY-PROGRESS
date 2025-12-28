#include <stdio.h> 
#include <stdlib.h> 
#include <time.h> 
// Function to partition the array int partition(int arr[], int low, int high)  
{     int pivot = arr[high];     	// Pivot element     int i = low - 1;  	 	 // Index of smaller element 
    for (int j = low; j < high; j++) 
    { 
         if (arr[j] <= pivot)    // If current element is smaller than or equal to pivot  Swap arr[i] and arr[j] 
        {             i++;             int temp = arr[i];             arr[i] = arr[j];             arr[j] = temp; 
        } 
    }     // Swap arr[i + 1] and arr[high] (or pivot)     int temp = arr[i + 1];     arr[i + 1] = arr[high];     arr[high] = temp; 
    return i + 1; // Return the partition index 
} 
// Quick Sort function 
void quickSort(int arr[], int low, int high)  
{ 
    if (low < high)  
  {         int pi = partition(arr, low, high);         quickSort(arr, low, pi - 1); // Before pi         quickSort(arr, pi + 1, high); // After pi 
    } 
} 
// Function to generate a random array void generateRandomArray(int *arr, int size) {     for (int i = 0; i < size; i++) {         arr[i] = rand() % 10000; // Random numbers from 0 to 9999 
    } 
} 
// Function to generate a sorted array void generateSortedArray(int *arr, int size) {     for (int i = 0; i < size; i++) {         arr[i] = i; // Sorted 
    } 
} 
// Function to generate a reverse sorted array void generateReverseSortedArray(int *arr, int size) {     for (int i = 0; i < size; i++) {         arr[i] = size - i - 1; // Reverse sorted 
    } 
} 
// Function to measure execution time of Quick Sort 
void measureSortTime(void (*sortFunc)(int *, int, int), int *arr, int size) {     clock_t start = clock();     sortFunc(arr, 0, size - 1);     clock_t end = clock(); 
    double timeTaken = ((double)(end - start)) / CLOCKS_PER_SEC;     printf("Time taken: %f seconds\n", timeTaken); 
} int main() {     int sizes[] = {1000, 5000, 10000}; // Different input sizes     for (int i = 0; i < 3; i++) {         int size = sizes[i];         // Average Case         int *avgArray = (int*)malloc(size * sizeof(int));         generateRandomArray(avgArray, size);         printf("Average Case (Random Array) for size %d:\n", size);         measureSortTime(quickSort, avgArray, size);         free(avgArray);         // Best Case         int *bestArray = (int*)malloc(size * sizeof(int));         generateSortedArray(bestArray, size);         printf("Best Case (Sorted Array) for size %d:\n", size);         measureSortTime(quickSort, bestArray, size);         free(bestArray);         // Worst Case         int *worstArray = (int*)malloc(size * sizeof(int));         generateReverseSortedArray(worstArray, size);         printf("Worst Case (Reverse Sorted Array) for size %d:\n", size);         measureSortTime(quickSort, worstArray, size);         free(worstArray);         printf("\n"); 
    }     return 0; 
} 

