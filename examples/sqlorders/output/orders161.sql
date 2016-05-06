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
insert into order_line values ('234567.0', 2, 2.0, 74.0)

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

