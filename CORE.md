I've to develop a backend with rest APIs
It'll include :
registration (customer):
Name
Email
Number
points
Password


registration (store owner):
name
email
number
store location
points
password


Product Market:
name (str)
image (img)
point to redeem it (integer)
product = foreign key product
redeemed time (time)
qr code =Product.qrcode
redeemed at (date)
quantity(int)


Products:
created at (date-current)
barcode (str)
name (str)
qrcode(image,contain barcode)
is_redeemed (boolean)
got_the_tokens (boolean)


Bulk:
created at (date-current)
barcode (str)
qrcode (image,contain barcode data)
got_the_tokens (boolean)
