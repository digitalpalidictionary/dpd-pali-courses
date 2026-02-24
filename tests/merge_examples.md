# Merged Row Examples

## Option 1: First Cell Content (Standard Markdown)
This is what the script currently produces. It places content in the first cell and leaves others empty.

| Pāli | POS | Grammar | English |
|---|---|---|---|




**Merged Pāli Sentence Row**

|  |  |  |  |
|---|---|---|---|

| | | | |
|---|---|---|---|
| word | pos | gram | eng |




*Merged English Translation Row*


## Option 2: HTML Colspan (Advanced Markdown/MkDocs)
This looks like a single cell in many renders (like MkDocs/Material), but the source code is more complex.

|  |  |  |  |
|---|---|---|---|

| | | | |
|---|---|---|---|
| <td colspan="4">**Merged Pāli Sentence Row**</td> |  |  |  |
| word | pos | gram | eng |
| <td colspan="4">*Merged English Translation Row*</td> |  |  |  |





## Option 3: Broken Table (Semantic)
This breaks the table into multiple pieces so the sentence and translation are standard text lines.

**Merged Pāli Sentence**

|  |  |  |  |
|---|---|---|---|

| | | | |
|---|---|---|---|
| word | pos | gram | eng |





*Merged English Translation*

## Option 4: "Centered" Spanning (Visual)
Puts content in a middle cell or spreads it.

|  |  |  |  |
|---|---|---|---|

| | | | |
|---|---|---|---|
|  | **Merged Pāli Sentence Row** |  |  |
| word | pos | gram | eng |
|  | *Merged English Translation Row* |  |  |