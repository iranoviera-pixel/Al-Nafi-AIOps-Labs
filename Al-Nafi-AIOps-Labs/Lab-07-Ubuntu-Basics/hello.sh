#!/bin/bash
echo "Hello, World!"

#!/bin/bash
greeting="Welcome to Bash Scripting"
echo $greeting

#!/bin/bash
if [ "$1" == "admin" ]; then
  echo "Welcome, Administrator!"
else
  echo "Access Denied"
fi

#!/bin/bash
for i in {1..5}; do
  echo "Iteration $i"
done

