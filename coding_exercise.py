#!/usr/bin/env python
# section -- docstrings
"""
Created 20141202
Modified 20141207; Eric Wiegman
Written for: Python 2.6.6
Tested with: Python 2.6.6, Python 2.7.10, and Python 3.4

NOTE 1:
Specs say to implement in Python 2.6, but it is recommended to use a bug-fix
version of Python 2.6 (which addressed security issues). The latest binary
security fix binary download available is Python 2.6.6. Therefore, I am coding
using Python 2.6.6.

NOTE 2:
The only advertised fixes or changes from Python 2.6 to later 2.6.X versions had
to do with security issues. The documentation claims no functinality bug fixes
or additions/deprecations in those dot releases. Thus, by using 2.6.6 I am still
satisying the specification to use Python 2.6.

Initial conditions:
  Initially, the system contains inventory of
  A x 150
  B x 150
  C x 100
  D x 100
  E x 200

  Initially, the system contains no orders

Data source:
  * There should be a data source capable of generating one or more streams of
    orders.
  * An order consists of a unique identifier (per stream) we will call the
    "header", and a demand for between zero and five units each of
    A,B,C,D, and E, except that there must be at least one unit demanded.
  * A valid order (in whatever format you choose):
    {"Header": 1, "Lines": {"Product": "A", "Quantity": "1"},{"Product": "C",
    "Quantity": "4"}}
  * An invalid order: {"Header": 1, "Lines": {"Product": "B", "Quantity": "0"}}
  * Another invalid order:
    {"Header": 1, "Lines": {"Product": "D", "Quantity": "6"}}
  * Feel free to identify streams as you'd like.

Inventory allocator:
  There should be an inventory allocator which allocates inventory to the
    inbound data according to the following rules:
  1) Inbound orders to the allocator should be individually identifiable
    (ie two streams may generate orders with an identical header, but these
    orders should be identifiable from their streams)
  2) Inventory should be allocated on a first come, first served basis;
    once allocated, inventory is not available to any other order.
  3) Inventory should never drop below 0.
  4) If a line cannot be satisfied, it should not be allocated.
    Rather, it should be  back-ordered (but other lines on the same order may
    still be satisfied).
  5) When all inventory is zero, the system should halt and produce output
    listing, in the order received by the system, the header of each order,
    the quantity on each line, the quantity allocated to each line, and
    the quantity back-ordered for each line.

  For instance:
  If the initial conditions are:
  A x 2
  B x 3
  C x 1
  D x 0
  E x 0

  And the input is:
  {"Header": 1, "Lines": {"Product": "A", "Quantity": "1"}
  {"Product": "C", "Quantity": "1"}}
  {"Header": 2, "Lines": {"Product": "E", "Quantity": "5"}}
  {"Header": 3, "Lines": {"Product": "D", "Quantity": "4"}}
  {"Header": 4, "Lines": {"Product": "A", "Quantity": "1"}
  {"Product": "C", "Quantity": "1"}}
  {"Header": 5, "Lines": {"Product": "B", "Quantity": "3"}}
  {"Header": 6, "Lines": {"Product": "D", "Quantity": "4"}}

  The output should be (in whatever format you choose):
  1: 1,0,1,0,0::1,0,1,0,0::0,0,0,0,0
  2: 0,0,0,0,5::0,0,0,0,0::0,0,0,0,5
  3: 0,0,0,4,0::0,0,0,0,0::0,0,0,4,0
  4: 1,0,1,0,0::1,0,0,0,0::0,0,1,0,0
  5: 0,3,0,0,0::0,3,0,0,0::0,0,0,0,0

"""

# section -- imports required for additional functionality beyond base python
import sys
import optparse
import logging

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

# Now use it from any version of Python
# mydict = OrderedDict()

import my_constants

# Module metadata variables, for latest version
__author__ = 'Eric Wiegman'
__contact__ = 'ewiegman113@gmail.com'
__status__ = 'production'
__copyright__ = 'Copyright, Shipwire'
__version__ = '0.0.0.1'
__date__ = '07 December 2015'

# section -- definition for configuration of logging output
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    stream=sys.stdout)


# section -- main executable routine
def main():
    """
    The executable portion, where the command-line is handled and then the
    function calls are made

    :return: None
    """
    # definition and usage of external options/arguments
    # note that the input read file is the only requirement option/argument
    usage = 'usage: %prog -r <file path> -i <file path> ' \
            '-a <positive integer> -b <positive integer> ' \
            '-c <positive integer> -d <positive integer> ' \
            '-e <positive integer>'
    parser = optparse.OptionParser(usage)
    parser.add_option('-r', '--read', dest='read',
                      default=None,
                      help='File to read in and parse for orders input stream')
    parser .add_option('-a', '--a_inv', dest='a',
                       default=150,
                       type='int',
                       help='Initial inventory of line item A')
    parser .add_option('-b', '--b_inv', dest='b',
                       default=150,
                       type='int',
                       help='Initial inventory of line item B')
    parser .add_option('-c', '--c_inv', dest='c',
                       default=100,
                       type='int',
                       help='Initial inventory of line item C')
    parser .add_option('-d', '--d_inv', dest='d',
                       default=100,
                       type='int',
                       help='Initial inventory of line item D')
    parser .add_option('-e', '--e_inv', dest='e',
                       default=200,
                       type='int',
                       help='Initial inventory of line item E')
    
    options, args = parser.parse_args()

    # section -- how to handle improperly used external options/arguments, etc.
    if not options.read:
        parser.error('Must specify an orders file using -r or --read')

    if options.a < 0:
        parser.error('If using a option, must specify value 0 or more')

    if options.b < 0:
        parser.error('If using b option, must specify value 0 or more')

    if options.c < 0:
        parser.error('If using c option, must specify value 0 or more')

    if options.d < 0:
        parser.error('If using d option, must specify value 0 or more')

    if options.e < 0:
        parser.error('If using e option, must specify value 0 or more')

    # section -- Initial logging showing options used
    logger = logging.getLogger('exercise')

    logger.info('Parsing: ' + options.read)
    logger.info('---------------')

    # section -- attempt to open externally defined files as read-only
    try:
        f_read = open(options.read, 'r')
    except IOError as e:
        logger.error('I/O error({0}): {1}'.format(e.errno, e.strerror))
        return

    # section -- makes calls to methods defined below, to achieve spec's goal
    inventory_a = options.a
    inventory_b = options.b
    inventory_c = options.c
    inventory_d = options.d
    inventory_e = options.e

    input_order_dict = add_order_to_dict(f_read, logger)
    remove_invalid_order(input_order_dict, logger)

    inventory_dict = {
            'A': inventory_a,
            'B': inventory_b,
            'C': inventory_c,
            'D': inventory_d,
            'E': inventory_e}

    inventory_dict = OrderedDict(sorted(inventory_dict.items()))
    keylist = map(int, input_order_dict.keys())

    logger.info('---------------')
    logger.info('The encoded output strings are ...')

    for key in keylist:

        str_key = str(key)

        back_order_list = []
        order_satisfied_list = []
        order_want_list = []

        for order_item in my_constants.PROD_LIST:

            product_count = \
                get_product_count(str_key, order_item, input_order_dict, logger)
            if product_count == -1:
                product_count = 0
            order_want_list.append(product_count)
            logger.debug('Key: ' + str_key + ' item: ' + order_item)
            logger.debug(product_count)

            # figure out if inventory is sufficient. If so, subtract product
            # item count from inventory. If not, back-order item.
            # 4: 1,0,1,0,0::1,0,0,0,0::0,0,1,0,0
            # key: order::actually_ordered::back-ordered
            current_inventory = inventory_dict.get(order_item)
            if product_count != -1:

                # For examples, current inventory count is 2

                # EXAMPLE 1
                # 2 C left (current_inventory)
                # 5 C requested (product_count)
                # ---------------------------------
                #
                # put all that you can (2) on C order
                # put the rest (3 --> 5-2) on C back-order

                # EXAMPLE 2
                # 0 C left (current_inventory)
                # 5 C requested (product_count)
                # ---------------------------------
                #
                # put all that you can (0) on C order
                # put the rest (5 --> 5-0) on C back-order

                if product_count > current_inventory:  # 5, 2 ==> 5, 0
                    # back-order
                    back_order = product_count - current_inventory  # 3 ==> 5
                    back_order_list.append(back_order)
                    # inventory is now depleted
                    inventory_dict[order_item] = 0
                    order_satisfied_list.append(current_inventory)  # 2 ==> 0
                else:
                    order_satisfied_list.append(product_count)
                    new_inventory = current_inventory - product_count
                    inventory_dict[order_item] = new_inventory
                    back_order_list.append(0)

        logger.info(str_key + ': ' + ','.join(map(str, order_want_list)) +
                    '::' + ','.join(map(str, order_satisfied_list)) + '::' +
                    ','.join(map(str, back_order_list)))

    logger.info('---------------')
    logger.info('Final Inventory is ...')
    inv_keyset = inventory_dict.keys()
    for inv_key in inv_keyset:
        logger.info("'" + inv_key + "':" + str(inventory_dict.get(inv_key)))

    f_read.close()


def get_order_key(header_item, logger):
    """
    If we have a line order such as:
    {"Header": 1, "Lines": {"Product": "A", "Quantity": "1"}
    {"Product": "C", "Quantity": "1"}}
    ... then we want to parse out the header part to get the integer that
    corresponds to the key for the dict.

    Similar code is used in get_order_value to get the value for that key.

    :param header_item: next line from input order file
    :param logger: the logger, used to print out debug information to ensure
    code correctness

    :return: the parsed key from the header_item
    """
    header_key_string = '"Header":'
    header_key_string_len = len(header_key_string)
    first_index = header_item.find(header_key_string)
    actual_index = first_index + header_key_string_len
    index_first_comma = header_item.find(',')
    key = header_item[actual_index:index_first_comma]
    logger.debug('The header sequence number = ' + key)
    return key


def get_order_value(header_item, logger):
    """
     If we have a line order such as:
    {"Header": 1, "Lines": {"Product": "A", "Quantity": "1"}
    {"Product": "C", "Quantity": "1"}}
    ... then we want to parse out the non-header part to get the string that
    corresponds to the value for that key for the dict.

    Similar code is used in get_order_key to get the key.

    :param header_item: next line from input order file
    :param logger: the logger, used to print out debug information to ensure
    code correctness

    :return: the parsed value from the header_item
    """
    header_value_string = '"Lines":'
    header_value_string_len = len(header_value_string)
    first_index = header_item.find(header_value_string)
    actual_index = first_index + header_value_string_len
    # subtract one from length, as we don't want the terminal } symbol
    value = header_item[actual_index:len(header_item) - 1]
    logger.debug('Product items in order = ' + value)
    return value


def remove_invalid_order(order_input, logger):
    """
    Needs to traverse order dictionary and if ANY product count is outside the
    accepted range, then the entire order is invalid. Thus, we need to notify
    that the order was rejected and remove it from order_input dictionary.

    :type order_input: dict

    :param order_input: the dictionary of non-rejected orders
    :param logger: the logger, used to print out debug information to ensure
    code correctness

    """
    # is_valid = True

    keylist = order_input.keys()
    for key in keylist:
        is_valid = True
        for order_item in my_constants.PROD_LIST:
            # invalid if line product has qty that is not from 1 to 5, inclusive
            count = get_product_count(key, order_item, order_input, logger)
            if count == -1:
                logger.debug('If there is no order item, '
                             'then we define it as having count of -1')
                # special case where the product line is not in the order at all
                # ... not where it is a bad order with zero items specified. We 
                # leave the flag is_valid as the default of True, in this 
                # special case.
            elif count < 1 or count > 5:
                is_valid = False
                break

        if not is_valid:
            bad_order = order_input.get(key)
            logger.warning('Order rejected as at least one line product had '
                           'quantity < 1 or > 5 :' + bad_order)

            # not only pops off the key, but mutates dict so element removed
            order_input.pop(key)

    return


def get_product_count(order_key, product_to_count, order_input, logger):
    """
    Parses the order values (such as one of the following) found in the dict:
    {"Product": "A", "Quantity": "1"},{"Product": "C",
    "Quantity": "4"}

    -- And then given the order_key, we keep checking until we find that key
    (such as 1 or 2 or ...) and then get the value from the dict. Then, given
     the product_to_count (such as a, b, ...) we extract the count from the line
     items in the order.

     Since it is invalid to have a Product Quantity of zero, any return of zero
     means that this order stream did not order any of that product. (In the
     example given above, if we called
        get_product_count(1, "D", order_input, logger)
     then we return 0 (zero) as there is no "D" product in that order.

    :type order_input: dict

    :param order_key: the integer associated with the order Header
    :param product_to_count: one of the string 'a', 'b', 'c', 'd', or 'e'
    :param order_input: the dictionary giving the orders to be considered
    :param logger: the logger, used to print out debug information to ensure
    code correctness

    :return: the integer quantity of the ordered product.
    """
    product_count = -1
    keylist = order_input.keys()
    for key in keylist:
        if order_key == key:
            orderline = order_input.get(key)

            substring = '{"Product":"' + product_to_count.upper() + \
                        '","Quantity":"'
            substring_len = len(substring)
            index = orderline.find(substring)
            product_count = \
                orderline[index + substring_len:index + substring_len + 1]
            # want to explicitly differentiate between no product in order and
            # order that has specified an invalid count of 0 (zero)
            if product_count == '"':
                product_count = -1
            logger.debug('Product count = ...')
            logger.debug(product_count)
    return int(product_count)


def add_order_to_dict(lines, logger):
    """
    Goes through each line in the file and, for each line, adds the value of
    1 as the value for the key if that key is first seen. Otherwise, the key was
    previously seen, so that key's value is incremented by 1.

    :type lines: collections.iterable

    :param lines: the collection of lines that make up the file
    :param logger: the logger, used to print out debug information to ensure
    code correctness

    :return: dict
    """
    order_input = {}
    order_input = OrderedDict(sorted(order_input.items()))
    rejected = {}
    reject_key = -1
    for line in lines:
        line = ''.join(line.split())
        key = get_order_key(line, logger)
        value = get_order_value(line, logger)
        if key not in list(order_input.keys()):
            order_input[key] = value
            logger.debug('Accepted the order (as it does not have a '
                         'duplicate key: ' + line)
        else:
            # if key already in use, duplicate order is rejected
            reject_key += 1
            rejected[reject_key] = value
            logger.warning('Order rejected due to duplicate key ' + key +
                           ': ' + line)
    return order_input


# section -- Allows you to test whether your script is being run directly
# or being imported by something else.
if __name__ == "__main__":
    main()
