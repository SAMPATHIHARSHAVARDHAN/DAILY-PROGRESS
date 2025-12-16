def is_palindrome(input_value):
  """
  Checks if the input (number or string) is a palindrome using slicing.
  """
  s = str(input_value).casefold()
  return s == s[::-1]

# --- Example Usage ---
print(f"'racecar' is palindrome: {is_palindrome('racecar')}")
print(f"12321 is palindrome: {is_palindrome(12321)}")
