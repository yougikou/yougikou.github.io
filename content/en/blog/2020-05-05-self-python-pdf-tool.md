---
title: "Self-made Python PDF Tools"
language: "en"
date: 2020-05-05T12:00:00Z
author: "Giko"
image: "/images/posts/2020-05-05-SelfPythonPDFTool-1.jpg"
categories: ["Technology", "Python"]
tags: ["Python", "windows", "PDF", "Tool", "PDF merge, split, rotate"]
draft: false
---

### Convenient fast programming language and rich extensions

&emsp;My impression of Python is that it's easy to write, easy to debug, quick to learn, and a powerful batch processing tool language. Of course, since I don't use it frequently at work, my understanding is relatively shallow.
During this period, in order to help my child review effectively, after buying a duplex scanning printer, I found that home printers after all are not commercial ones—some functions are still relatively inconvenient.
For example, scanned pages can only be vertical; to view them horizontally on the computer, you have to rotate them yourself. Some are booklets; after removing the central binding line and scanning, pages need to be split and order needs to be rearranged. Although there are PDF editing software, the workload for such simple operations each time is still large.
And what's annoying is that many so-called free PDF editing software have some basic functions and require installation. Once you need something slightly more advanced, you need to upgrade your subscription.
At this point, I first thought of Python.

### Using PDF library

&emsp;pdfrw - At least for my needs, this library is very good. Initially, I used PyPDF2, but during splitting, I found it doubled file size and couldn't compress, so I abandoned it midway and switched to pdfrw. Moreover, I found the author very enthusiastic, providing pdfrw writing examples in the PyPDF2 split file size doubling issue thread.

### Self-made tools

&emsp;All tools pursue ease of use; they are designed to select PDFs, drag and drop onto the corresponding py file, and then start execution.
All outputs are unified into a newly created 'out' subfolder in the same folder.
If any exception occurs, the console screen pauses for 10 seconds, allowing you to view the erroneous command line number and error content.

Before using, install pdfrw (pip install pdfrw).
It's best to upgrade Python to 3.8 or above. I found that new python launcher can automatically associate py files.
Double-clicking and dragging files for execution are very convenient.

1. [mergePdf.py](/attached/mergePdf.py)
Merge multiple dragged files into one file. When dragging, the file you first select with the mouse should preferably be the first.
Otherwise, the selected file might jump to the front.
2. [rotateL90.py](/attached/rotateL90.py)
Rotate all dragged files 90 degrees to the left.
3. [split&sort.py](/attached/split&sort.py)
This is a bit more advanced. It processes based on the following scanning premise.
When scanning after removing binding lines - start scanning from the middle page (as the first page).
For example, if the middle pages are 11,12, then Page1(11,12), Page2(13,10), Page3(9,14)...
So this py performs the following operations on all dragged files and outputs each as a new pdf.
Original files can be used for booklet printing; processed files can be used for computer reading.
   - Split pages: Split each page into left and right pages.
   - Sorting: According to the above rule, sort the split pages into actual page order.

2020-05-05 additions

1. [split&sort_reverse.py](/attached/split&sort_reverse.py)
A small modification of the previous script to handle vertical binding book page order (like ancient texts read from right to left, page-turning booklets).
2. [reverse.py](/attached/reverse.py)
Simply reverse the order of PDF pages.
3. [delete.py](/attached/delete.py)
Delete specified pages, only processes a single file. Pages to delete are specified separated by spaces.

Feeling like with Python, I'm too lazy to open bloated PDF editing software.

Sharing py files for friends with similar needs, or as sample references—after all, if needs are similar, it saves a lot of effort compared to starting from scratch.