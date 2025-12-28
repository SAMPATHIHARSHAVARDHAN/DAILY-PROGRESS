#include <stdio.h> 
#include <stdlib.h> 
#include <time.h> 
// Function to merge two subarrays void merge(int arr[], int left, int mid, int right) {     int n1 = mid - left + 1;     int n2 = right - mid,i,j,k;         // Create temporary arrays     int *L = (int*)malloc(n1 * sizeof(int));     int *R = (int*)malloc(n2 * sizeof(int));     // Copy data to temporary arrays     for (i = 0; i < n1; i++)         L[i] = arr[left + i];     for (j = 0; j < n2; j++)         R[j] = arr[mid + 1 + j]; 
    // Merge the temporary arrays back into arr[left..right]     i = 0, j = 0, k = left;     while (i < n1 && j < n2) {         if (L[i] <= R[j]) {             arr[k++] = L[i++]; 
        } else { 
            arr[k++] = R[j++]; 
        } 
    } 
    // Copy remaining elements     while (i < n1) {         arr[k++] = L[i++]; 
    }     while (j < n2) {         arr[k++] = R[j++]; 
    }     free(L);     free(R); 
} 
// Merge Sort function void mergeSort(int arr[], int left, int right) {     if (left < right) {         int mid = left + (right - left) / 2;         mergeSort(arr, left, mid);         mergeSort(arr, mid + 1, right);         merge(arr, left, mid, right); 
    } 
} 
// Function to generate a random array void generateRandomArray(int *arr, int size)  
{  	int i; 
    for ( i = 0; i < size; i++) {         arr[i] = rand() % 10000; // Random numbers from 0 to 9999 
    } 
} 
// Function to generate a sorted array void generateSortedArray(int *arr, int size)  
{  	int i; 
    for (i = 0; i < size; i++) {         arr[i] = i; // Sorted 
    } 
} 
// Function to generate a reverse sorted array void generateReverseSortedArray(int *arr, int size) 
{ 
	 	 	int i; 
    for (i = 0; i < size; i++) {         arr[i] = size - i - 1; // Reverse sorted 
    } 
} 
// Function to measure execution time of Merge Sort void measureSortTime(void (*sortFunc)(int *, int, int), int *arr, int size) {     clock_t start = clock();     sortFunc(arr, 0, size - 1);     clock_t end = clock();     double timeTaken = ((double)(end - start)) / CLOCKS_PER_SEC;     printf("Time taken: %f seconds\n", timeTaken); 
} int main()  {     int sizes[] = {1000, 5000, 10000}; // Different input sizes     int i;     for ( i = 0; i < 3; i++)  
   {         int size = sizes[i];         // Average Case 
        int *avgArray = (int*)malloc(size * sizeof(int));         generateRandomArray(avgArray, size);         printf("Average Case (Random Array) for size %d:\n", size);         measureSortTime(mergeSort, avgArray, size);         free(avgArray);         // Best Case         int *bestArray = (int*)malloc(size * sizeof(int));         generateSortedArray(bestArray, size); 
        printf("Best Case (Sorted Array) for size %d:\n", size);         measureSortTime(mergeSort, bestArray, size);         free(bestArray);         // Worst Case 
        int *worstArray = (int*)malloc(size * sizeof(int));         generateReverseSortedArray(worstArray, size);         printf("Worst Case (Reverse Sorted Array) for size %d:\n", size);         measureSortTime(mergeSort, worstArray, size);         free(worstArray);         printf("\n"); 
    }     return 0; 
} 

