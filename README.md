# inventory_order_stream

TABLE OF CONTENTS
-----------------
<ol>
<li> Introduction  </li>
<li> Statement of Work </li>
<li> Requirements </li>
<li> What was automated </li>
<li> Project (Location, Structure) </li>
<li> Directory Structure </li>
<li> Documentation </li>
<li> Command-line Invocation </li>
<li> Output (Expected) </li>
</ol>


1. Introduction
---------------------------------------------------------------------------
This is the README.md file for the Shipwire coding exercise presented to Eric Wiegman
as part of his consideration for the _"Quality Engineering Lead"_ position

2. Statement of Work
------------------------------
 I have created (usign the PyCharm Community Edition 5.01 IDE with the following
 additional Python libraries sys, optparse, logging, and OrderedDict part of
 collections (post 2.6.x) or of ordereddict (pre 2.7)) a program to simulate
 an inventory order stream. This was done by following the specifications
 presented to me.
 
 The specifications said to use Python 2.6, and technically I did that. I
 actually coded using Python 2.6.6 -- where all the 2.6.x releases only fixed
 security issues and did not change (add, modify, or deprecate) any features
 or functionality. I checked the code against the 2.7.10 and 3.4 releases
 and ensured that no runtime errors or change in functionality occurred. 

3. Specified Project Requirements
-------------------------------------------------------------
The requirements are:
<pre>
Please post your code and output to a repository on github or bitbucket and share the repository.
Please implement this project in python 2.6
------------------------------------------------------
The object of the exercise is to show off your coding style and skill.

Initial conditions:
Initially, the system contains inventory of
A x 150
B x 150
C x 100
D x 100
E x 200

Initially, the system contains no orders

Data source:
There should be a data source capable of generating one or more streams of orders.
1. An order consists of a unique identifier (per stream) we will call the "header", and a demand for between 
 zero and five units each of A,B,C,D, and E, except that there must be at least one unit demanded.
2. A valid order (in whatever format you choose): 
{"Header": 1, "Lines": {"Product": "A", "Quantity": "1"},{"Product": "C", "Quantity": "4"}}
3. An invalid order: {"Header": 1, "Lines": {"Product": "B", "Quantity": "0"}}
4. Another invalid order: {"Header": 1, "Lines": {"Product": "D", "Quantity": "6"}}

Feel free to identify streams, as you would like.

Inventory allocator:
There should be an inventory allocator that allocates inventory to the inbound data according to the following rules:
1) Inbound orders to the allocator should be individually identifiable (i.e. two streams may generate orders  
with an identical header, but these orders should be identifiable from their streams)
2) Inventory should be allocated on a first come, first served basis; once allocated, inventory is not available
 to any other order.
3) Inventory should never drop below 0 (zero).
4) If a line cannot be satisfied, it should not be allocated.  
Rather, it should be  backordered (but other lines on the same order may still be satisfied).
5) When all inventory is zero, the system should halt and produce output listing, in the order received by the 
 system, the header of each order, the quantity on each line, the quantity allocated to each line, and the quantity
 backordered for each line.

For instance:
If the initial conditions are:
A x 2
B x 3
C x 1
D x 0
E x 0

And the input is:
{"Header": 1, "Lines": {"Product": "A", "Quantity": "1"}{"Product": "C", "Quantity": "1"}}
{"Header": 2, "Lines": {"Product": "E", "Quantity": "5"}}
{"Header": 3, "Lines": {"Product": "D", "Quantity": "4"}}
{"Header": 4, "Lines": {"Product": "A", "Quantity": "1"}{"Product": "C", "Quantity": "1"}}
{"Header": 5, "Lines": {"Product": "B", "Quantity": "3"}}
{"Header": 6, "Lines": {"Product": "D", "Quantity": "4"}}

The output should be (in whatever format you choose):
1: 1,0,1,0,0::1,0,1,0,0::0,0,0,0,0
2: 0,0,0,0,5::0,0,0,0,0::0,0,0,0,5
3: 0,0,0,4,0::0,0,0,0,0::0,0,0,4,0
4: 1,0,1,0,0::1,0,0,0,0::0,0,1,0,0
5: 0,3,0,0,0::0,3,0,0,0::0,0,0,0,0
</pre>

3.1. Notes on Requirements
--------------------------
1. I chose to post the public git project on GitHub.
2. As explained earlier, although the requirement was to code using Python 2.6 ... I used Python releases
2.6.6, 2.7.10, and 3.4. I ensured the code worked fine (with no errors) in all such versions.
3. Also explained earlier, I made use of these additional Python libraries:
sys, optparse, logging, and OrderedDict part of collections (post 2.6.x) or of ordereddict (pre 2.7).
4. I used a text file to simulate the input order stream. In fact, I used three such files to ensure
that the code handled different situations correctly.
5. The specs state:
<pre>
If a line cannot be satisfied, it should not be allocated.  Rather, it should be  backordered 
(but other lines on the same order may still be satisfied).
</pre>
It is unclear if that means to fullfil a part order and backorder the rest. Example: My inventory
is at 3 units for Line Product D and the request is for 5 units, so I allocate 3 units and
backorder the rest (2 units). This is how I interpreted it. However, it would be simple to refactor
the code if it meant (again using the example) to satsify no units and backorder all 5.
6. It was not clear what to do with orders with identical headers. My solution was to declare any
further instance as illegal and remove it from the stream. This removed order would be output as
a warning.

4. The following is a general outline of what was automated:
---------------------------------------------------------------------------
1. The goal was to write a main function that takes a number of command line arguments.
2. See the section on command-line invocation for details on those arguments / parameters.
3. Other functions (besides main) include:

   3a. get_order_key(header_item, logger) -- gets the key (Header) from the header item line of the stream<br>
   3b. get_order_value(header_item, logger) -- gets the value (line order portion) of the input stream<br>
   3c. remove_invalid_order(order_input, logger) -- determines if a valid is invalid, and if so removes it<br>
   3d. get_product_count(order_key, product_to_count, order_input, logger) -- gets the product counts<br>
   3e. add_order_to_dict(lines, logger) -- adds the parsed key and value pairs to the order dictionary<br>

4. See the docstrings in the code for more details.
5. Project Location and Structure
---------------------------------------------------------------------------
1. Project is stored on GitHub at public repository Eric-Wiegman/inventory_order_stream.

6. Directory Structure
---------------------------------------------------------------------------
1. The directory structure is shown below:

<pre>
.
│   coding_exercise.py
│   my_constants.py
│   order_stream.txt
│   order_stream_2.txt
│   order_stream_3.txt
</pre>

7. Documentation
----------------
Besides this README, the only other documentation are inline comments in the code
and docstrings (mainly for the functions)

8. Command-line invocation
---------------------------
1. To call the program from the command line (from within your Windows (DOS)
    Command Prompt or PowerShell, or from the Macintosh/Linux Terminal), you need 
    to ensure some prerequisites have first been met.
2. You need to have the required Python interpreter(s) installed.
3. You should install all the required packages (already discussed) using your favorite
   package management system, such as pip.
3. Ensure that your environment variables/path are set so that you can refer to the
   Python executable without requiring the full directory path to be specified.
4. As I coded in the PyCharm IDE, it was not required to run on the command line and
   I specified the Python Interpreter for my Project by using the Settings. As the 
   Python executable has the same name for different installed versions, I am not sure
   how to set the path to recognize the correct one.
5. To simplify the command line call, you should use your Terminal to
    navigate to the directory where the py file to run is located.
6. Additionally, it is required to put the required order stream order input text file
    in the same location as the py file (so you don't need to specify full path)
7. The only required parameter is the -r or --read option, which specifies the order
    stream input text file.
8. The usage is:
<pre>
    coding_exercise.py -r \<file\> -a \<int\> -b \<int\> -c \<int\> -d \<int\> -e \<int\>
</pre>
9. Optional parameters -a through -e allow you to change the line product initial inventory
   from values specified in the specifications. If any/all of these parameters are excluded
   from the command line, the default value is used.

8.2. The following are various command line texts to be entered in the Command Prompt
    or Terminal:

       python.exe coding_exercise.py -r order_stream.txt
       python.exe coding_exercise.py -r order_stream_2.txt -a 2 -b 3 -c 1 -d 0 -e 0
       python.exe coding_exercise.py -r order_stream_3.txt

9. Output
---------
9.1. The command line output that I am seeing is shown below.

For the comand line: _python.exe coding_exercise.py -r order_stream.txt_
<pre>
2015-12-06 21:47:14,338 INFO Parsing: order_stream.txt
2015-12-06 21:47:14,340 INFO ---------------
2015-12-06 21:47:14,342 WARNING Order rejected due to duplicate key 4: {"Header":4,"Lines":{"Product":"E","Quantity":"1"}{"Product":"B","Quantity":"1"}{"Product":"C","Quantity":"1"}}
2015-12-06 21:47:14,345 WARNING Order rejected as at least one line product had quantity < 1 or > 5 :{"Product":"E","Quantity":"1"}{"Product":"B","Quantity":"6"}{"Product":"C","Quantity":"3"}{"Product":"A","Quantity":"4"}
2015-12-06 21:47:14,348 WARNING Order rejected as at least one line product had quantity < 1 or > 5 :{"Product":"B","Quantity":"0"}
2015-12-06 21:47:14,350 INFO ---------------
2015-12-06 21:47:14,351 INFO The encoded output strings are ...
2015-12-06 21:47:14,352 INFO 1: 1,0,5,0,0::1,0,5,0,0::0,0,0,0,0
2015-12-06 21:47:14,353 INFO 2: 0,0,0,0,5::0,0,0,0,5::0,0,0,0,0
2015-12-06 21:47:14,354 INFO 3: 0,0,0,4,0::0,0,0,4,0::0,0,0,0,0
2015-12-06 21:47:14,356 INFO 6: 0,0,0,4,0::0,0,0,4,0::0,0,0,0,0
2015-12-06 21:47:14,357 INFO ---------------
2015-12-06 21:47:14,358 INFO Final Inventory is ...
2015-12-06 21:47:14,359 INFO 'A':149
2015-12-06 21:47:14,360 INFO 'B':150
2015-12-06 21:47:14,364 INFO 'C':95
2015-12-06 21:47:14,366 INFO 'D':92
2015-12-06 21:47:14,369 INFO 'E':195
</pre> 

For the comand line: _python.exe coding_exercise.py -r order_stream_2.txt -a 2 -b 3 -c 1 -d 0 -e 0_
<pre>
2015-12-06 22:19:29,183 INFO Parsing: order_stream_2.txt
2015-12-06 22:19:29,185 INFO ---------------
2015-12-06 22:19:29,190 INFO ---------------
2015-12-06 22:19:29,191 INFO The encoded output strings are ...
2015-12-06 22:19:29,195 INFO 1: 1,0,1,0,0::1,0,1,0,0::0,0,0,0,0
2015-12-06 22:19:29,198 INFO 2: 0,0,0,0,5::0,0,0,0,0::0,0,0,0,5
2015-12-06 22:19:29,200 INFO 3: 0,0,0,4,0::0,0,0,0,0::0,0,0,4,0
2015-12-06 22:19:29,202 INFO 4: 1,0,1,0,0::1,0,0,0,0::0,0,1,0,0
2015-12-06 22:19:29,206 INFO 5: 0,3,0,0,0::0,3,0,0,0::0,0,0,0,0
2015-12-06 22:19:29,209 INFO 6: 0,0,0,4,0::0,0,0,0,0::0,0,0,4,0
2015-12-06 22:19:29,214 INFO ---------------
2015-12-06 22:19:29,215 INFO Final Inventory is ...
2015-12-06 22:19:29,218 INFO 'A':0
2015-12-06 22:19:29,221 INFO 'B':0
2015-12-06 22:19:29,223 INFO 'C':0
2015-12-06 22:19:29,227 INFO 'D':0
2015-12-06 22:19:29,229 INFO 'E':0
</pre>

For the command line: _python.exe coding_exercise.py -r order_stream_3.txt_
<pre>
2015-12-06 22:21:37,869 INFO Parsing: order_stream_3.txt
2015-12-06 22:21:37,871 INFO ---------------
2015-12-06 22:21:37,921 INFO ---------------
2015-12-06 22:21:37,922 INFO The encoded output strings are ...
2015-12-06 22:21:37,925 INFO 1: 1,0,5,0,0::1,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:37,928 INFO 2: 0,0,0,0,5::0,0,0,0,5::0,0,0,0,0
2015-12-06 22:21:37,930 INFO 3: 0,0,0,4,0::0,0,0,4,0::0,0,0,0,0
2015-12-06 22:21:37,933 INFO 4: 0,0,3,0,0::0,0,3,0,0::0,0,0,0,0
2015-12-06 22:21:37,936 INFO 5: 1,0,5,0,0::1,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:37,938 INFO 6: 0,0,0,0,5::0,0,0,0,5::0,0,0,0,0
2015-12-06 22:21:37,941 INFO 7: 0,0,0,4,0::0,0,0,4,0::0,0,0,0,0
2015-12-06 22:21:37,944 INFO 8: 0,0,2,0,0::0,0,2,0,0::0,0,0,0,0
2015-12-06 22:21:37,948 INFO 9: 0,0,5,5,0::0,0,5,5,0::0,0,0,0,0
2015-12-06 22:21:37,950 INFO 10: 0,0,0,0,3::0,0,0,0,3::0,0,0,0,0
2015-12-06 22:21:37,953 INFO 11: 1,0,5,0,0::1,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:37,956 INFO 12: 0,0,0,0,5::0,0,0,0,5::0,0,0,0,0
2015-12-06 22:21:37,959 INFO 13: 0,0,0,4,0::0,0,0,4,0::0,0,0,0,0
2015-12-06 22:21:37,965 INFO 14: 0,0,3,0,0::0,0,3,0,0::0,0,0,0,0
2015-12-06 22:21:37,968 INFO 15: 1,0,5,0,0::1,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:37,969 INFO 16: 0,0,0,0,5::0,0,0,0,5::0,0,0,0,0
2015-12-06 22:21:37,971 INFO 17: 0,0,0,4,0::0,0,0,4,0::0,0,0,0,0
2015-12-06 22:21:37,975 INFO 18: 0,0,2,0,0::0,0,2,0,0::0,0,0,0,0
2015-12-06 22:21:37,979 INFO 19: 0,0,5,5,0::0,0,5,5,0::0,0,0,0,0
2015-12-06 22:21:37,980 INFO 20: 0,0,0,0,3::0,0,0,0,3::0,0,0,0,0
2015-12-06 22:21:37,985 INFO 21: 1,0,5,0,0::1,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:37,987 INFO 22: 0,0,5,0,0::0,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:37,989 INFO 23: 0,0,0,4,0::0,0,0,4,0::0,0,0,0,0
2015-12-06 22:21:37,992 INFO 24: 0,0,3,0,0::0,0,3,0,0::0,0,0,0,0
2015-12-06 22:21:37,998 INFO 25: 1,0,5,0,0::1,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:38,000 INFO 26: 0,0,5,0,0::0,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:38,002 INFO 27: 0,0,4,0,0::0,0,4,0,0::0,0,0,0,0
2015-12-06 22:21:38,005 INFO 28: 0,0,2,0,0::0,0,2,0,0::0,0,0,0,0
2015-12-06 22:21:38,008 INFO 29: 0,0,5,5,0::0,0,5,5,0::0,0,0,0,0
2015-12-06 22:21:38,011 INFO 30: 0,0,0,0,3::0,0,0,0,3::0,0,0,0,0
2015-12-06 22:21:38,014 INFO 31: 3,0,5,0,0::3,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:38,017 INFO 32: 0,0,5,0,0::0,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:38,019 INFO 33: 0,0,0,4,0::0,0,0,4,0::0,0,0,0,0
2015-12-06 22:21:38,022 INFO 34: 0,0,3,0,0::0,0,3,0,0::0,0,0,0,0
2015-12-06 22:21:38,025 INFO 35: 3,0,5,0,0::3,0,5,0,0::0,0,0,0,0
2015-12-06 22:21:38,030 INFO 36: 0,0,0,0,5::0,0,0,0,5::0,0,0,0,0
2015-12-06 22:21:38,033 INFO 37: 0,0,4,0,0::0,0,4,0,0::0,0,0,0,0
2015-12-06 22:21:38,036 INFO 38: 0,0,2,0,0::0,0,2,0,0::0,0,0,0,0
2015-12-06 22:21:38,039 INFO 39: 0,0,5,5,0::0,0,2,5,0::0,0,3,0,0
2015-12-06 22:21:38,041 INFO 40: 0,0,0,0,3::0,0,0,0,3::0,0,0,0,0
2015-12-06 22:21:38,045 INFO 41: 1,0,5,0,0::1,0,0,0,0::0,0,5,0,0
2015-12-06 22:21:38,049 INFO 42: 0,0,5,0,0::0,0,0,0,0::0,0,5,0,0
2015-12-06 22:21:38,051 INFO 43: 0,0,0,4,0::0,0,0,4,0::0,0,0,0,0
2015-12-06 22:21:38,053 INFO 44: 0,0,3,0,0::0,0,0,0,0::0,0,3,0,0
2015-12-06 22:21:38,056 INFO 45: 1,0,5,0,0::1,0,0,0,0::0,0,5,0,0
2015-12-06 22:21:38,058 INFO 46: 0,0,1,0,0::0,0,0,0,0::0,0,1,0,0
2015-12-06 22:21:38,062 INFO 47: 0,0,4,0,0::0,0,0,0,0::0,0,4,0,0
2015-12-06 22:21:38,067 INFO 48: 0,0,4,0,0::0,0,0,0,0::0,0,4,0,0
2015-12-06 22:21:38,069 INFO 49: 0,0,5,5,0::0,0,0,5,0::0,0,5,0,0
2015-12-06 22:21:38,072 INFO 50: 0,0,0,0,5::0,0,0,0,5::0,0,0,0,0
2015-12-06 22:21:38,075 INFO 51: 5,0,5,0,0::5,0,0,0,0::0,0,5,0,0
2015-12-06 22:21:38,079 INFO 52: 0,0,5,0,0::0,0,0,0,0::0,0,5,0,0
2015-12-06 22:21:38,082 INFO 53: 0,0,0,4,0::0,0,0,4,0::0,0,0,0,0
2015-12-06 22:21:38,085 INFO 54: 0,0,5,0,0::0,0,0,0,0::0,0,5,0,0
2015-12-06 22:21:38,087 INFO 55: 5,0,5,0,0::5,0,0,0,0::0,0,5,0,0
2015-12-06 22:21:38,089 INFO 56: 0,0,0,0,5::0,0,0,0,5::0,0,0,0,0
2015-12-06 22:21:38,092 INFO 57: 0,0,4,0,0::0,0,0,0,0::0,0,4,0,0
2015-12-06 22:21:38,096 INFO 58: 0,0,2,0,0::0,0,0,0,0::0,0,2,0,0
2015-12-06 22:21:38,099 INFO 59: 0,0,5,5,0::0,0,0,5,0::0,0,5,0,0
2015-12-06 22:21:38,101 INFO 60: 0,0,0,0,3::0,0,0,0,3::0,0,0,0,0
2015-12-06 22:21:38,103 INFO ---------------
2015-12-06 22:21:38,105 INFO Final Inventory is ...
2015-12-06 22:21:38,107 INFO 'A':126
2015-12-06 22:21:38,110 INFO 'B':150
2015-12-06 22:21:38,113 INFO 'C':0
2015-12-06 22:21:38,116 INFO 'D':38
2015-12-06 22:21:38,118 INFO 'E':150
</pre>
</pre>
    
