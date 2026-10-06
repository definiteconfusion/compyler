# Todos

## Variables

Add mutability tracking for variables (class attr)

Add call tracking and prefix unused variables with and `_` for rust conventions purposes (class attr)

## Misc Issues

### Issue
    fix seems to work? - the ending curly brace isnt being placed properly becuase of the if_true rather than if_false.
### Solution
    added class attribute to track how many open expressions require closure, and that is checked and rectified when the loop is closed

### Issue
    fix seems to work? - Also the range -> 0..k isnt working now fsr 
### Solution
    the check to see if the iterative was a variable or a number seemed to be flipped

### Issue
    the vec! needs to be mut if append end up being called
### Solution
    added a loop in the _append function to loop through buildStack to find the array, and toggle the reqMut to True
