

INSERT INTO public.products (name, price, is_sale, inventory, created_at) VALUES
('Red T-Shirt', 25, false, 100, '2024-01-10 10:00:00+00'),
('Blue Jeans', 55, true, 40, '2024-02-15 14:30:00+00'),
('Sneakers', 80, false, 60, '2024-03-20 09:15:00+00'),
('Baseball Cap', 15, true, 200, '2024-04-01 12:00:00+00'),
('Leather Jacket', 150, false, 10, '2024-05-05 16:45:00+00'),
('Sunglasses', 45, true, 75, '2024-06-10 18:00:00+00'),
('Backpack', 65, false, 35, '2024-07-01 08:00:00+00'),
('Running Shorts', 30, true, 120, '2024-07-10 11:00:00+00'),
('Watch', 120, false, 25, '2024-07-20 13:30:00+00'),
('Water Bottle', 20, true, 300, '2024-07-22 07:45:00+00');


INSERT INTO public.products (name, price, is_sale, inventory) VALUES
('TV Blue', 250, false, 100),
('TV Red', 550, true, 40),
('TV Yellow', 800, false, 60);

SELECT *
FROM public.products;

SELECT name, id as product_id, price FROM public.products;

SELECT * FROM products p WHERE id = 3;

SELECT * FROM products p WHERE name = 'Keyboard';

select * from products p where price <= 50;

select * from products p where inventory != 0;

select * from products p where inventory > 20 and price > 20;

select * from products p where price > 100 or price < 20;

select * from products p where id = 1 or id = 5 or id = 7;

select * from products p where id in (1,5,7);

select * from products p where name like '%T%';

select * from products p where name not like '%w';

select * from products p order by price desc;

select * from products p order by inventory desc, price;

select * from products p order by created_at desc;

select * from products p where price > 20 order by created_at desc;

update products set name='TV Orange', price = 825 where id=21; 

update products set is_sale = true where id=15 returning *;
















