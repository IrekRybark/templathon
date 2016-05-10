# templathon
Template-based data generating Python script.

## Purpose
The program can be used to generate variety of data.  Primarily was develop for supporting application testing by creating:
- SQL scripts
- EDI data
- GUI automation (like AutoIt) scripts

## How it works
The script generates text data based on a list of data items and templates.
The data items are currently in form of rows of .csv file.
Templates contain special tags, which are replaced with values from .csv file fields.

## Example
See examples/sqlorders directory for actual files.

### Task
Generate number of orders in a sales database using SQL.

### Order data
Order data consists of the following fields:  

```
order_num	
bill_to_num	
ship_to_num	
shipping_method	
item_num_1	
item_qty_1	
price_1	
item_num_2	
item_qty_2	
price_2
```  

The field values are provided in .csv file for several orders.
  
```
order_num,bill_to_num,ship_to_num,shipping_method,item_num_1,item_qty_1,price_1,item_num_2,item_qty_2,price_2
A16X001234,BT01234,SH02222,FeExOvNt,123456,1,100,234567,2,74
A16X001235,BT02345,SH03333,FeExOvNt,123456,1,100,,,
A16X001236,BT02345,SH03333,FeExOvNt,123333,2,50,,,
```

### SQL expression templates
SQL insert expressions are dynamically built by replacing tags with actual values.  The tags are just .csv file column names enclosed in delimters (##).

Inserting order header data:

```
-- Insert header
select @order_date = getdate()
insert into order_header values ('##order_num##', @order_date, '##bill_to_num##', '##ship_to_num##', '##shipping_method##')
```

In addition, templates for both order note and...

```
-- Insert order note
insert into order_note values ('##order_num##', 'Test case: ##seq##')
```

...row insertion can be used.

```
-- Insert line
insert into order_line values ('##item_num##', ##line_num##, ##item_qty##, ##price##)
```

### Input data
In addition to field values, the input data contains template names (Like ord_100_header.sql, ord_200_note.sql etc.).
```
seq,template_header,template_note,template_line_1,template_line_2,order_num,bill_to_num ...
101,ord_100_header.sql,ord_200_note.sql,ord_300_line.sql,ord_300_line.sql,A16X001234,BT01234 ...
102,ord_100_header.sql,ord_200_note.sql,ord_300_line.sql,,A16X001235,BT02345 ...
```
Note: in the example above, for order A16X001235 the data row is not showing line #2 template (template_line_2), so only one line insert statement will be generated.

### Outupt
Generated output is a valid SQL script ready for execution.

```
-- select database
user salesdb

declare
    @order_date datetime

start transaction
---------------------------
-- Test case: 101
---------------------------
-- Insert order header
select @order_date = getdate()
insert into order_header values ('A16X001234', @order_date, 'BT01234', 'SH02222', 'FeExOvNt')
-- Insert order note
insert into order_note values ('A16X001234', 'Test case: 101')
-- insert line
insert into order_line values ('123456', 1, 1, 100)

-- insert line
insert into order_line values ('234567', 2, 2.0, 74.0)

---------------------------
-- Test case: 102
---------------------------
-- Insert order header
select @order_date = getdate()
insert into order_header values ('A16X001235', @order_date, 'BT02345', 'SH03333', 'FeExOvNt')
-- Insert order note
insert into order_note values ('A16X001235', 'Test case: 102')
-- insert line
insert into order_line values ('123456', 1, 1, 100)

commit transaction
```

## Configuration
Data generation job is stored in .config file.

