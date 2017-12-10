# Django
Preschool Management (application in progress)

The scope of this project is to write Django application which will be helpful in preschool management.

Used technologies:
- Python
- Django
- MySQL
- HTML, CSS (Bootstrap)

Application allows easily adding a new child to the current group of children, adding a child 
to a concrete group, making a relationship between child and parents or group, adding a teacher 
and making relationship with group.

Main functionality of this application is to monthly calculate a fee for preschool for particular persons. There are couple o things which are included in this fee:
- hours in which child will be in preschool (hours free of charge are 7-12, for additional hours there will be a charge)
- big family card (KDR) which provides that those additional hours will be cheaper
- number of meals, declared in agreement with preschool
- how many day a child was in fact in preschool, it makes difference according to additional hours and a charge for meals.

Application will allow easily generate a receipt for a particular person basing on provided above (this functionality is still in development).