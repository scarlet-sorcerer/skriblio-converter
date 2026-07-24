# skriblio-converter
Small script to convert categorized lists to comma separated lists for use at skribl.io

Accepts input as a .txt file in the working directory matching the name `castbars.txt`. <br>
Will detect categories from lines beginning with `--` <br>
Reads input line by line and automatically merges and assigns all lines to the most recent category. Merged lines are comma separated.<br>
Outputs to `output.txt` in the working directory.
