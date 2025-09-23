# mdtable2csv (Convert `.md` file to `.csv`)

Convert markdown tables to csvs!

## Install requirements

pip install mdtable2csv

## Usage

### Command Line

Use the following command to convert `<filename>.md` to `<filename>.csv` :

```
mdtable2csv <filename>.md
```

And then you will see a `<filename>.csv` in the same folder.

### Python

```
from mdtable2csv import mdtable2csv
mdtable2csv("temp.md")
```

And then you will see a `<filename>.csv` in the same folder.

## Examples

### table.md

```markdown
# table.md :
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell

$ mdtable2csv table.md

# table.csv :
First Header,Second Header
Content Cell,Content Cell
Content Cell,Content Cell
```

--------------------------------------------------------------------------------

### abc.md

```markdown
# abc.md :
|   |  a | b  | c  |
|---|----|----|----|
| 1 | a1 | b1 | c1 |
| 2 | a2 | b2 | c2 |
| 3 | a3 | b3 | c3 |

$ mdtable2csv abc.md

# abc.csv :
 ,a,b,c
1,a1,b1,c1
2,a2,b2,c2
3,a3,b3,c3
```

--------------------------------------------------------------------------------

**Please give me a star if you find this tool useful, Thank you.**
