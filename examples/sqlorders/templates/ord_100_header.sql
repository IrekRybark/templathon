---------------------------
-- Test case: ##seq##
---------------------------
-- Insert order header
select @order_date = getdate()
insert into order_header values ('##order_num##', @order_date, '##bill_to_num##', '##ship_to_num##', '##shipping_method##')
