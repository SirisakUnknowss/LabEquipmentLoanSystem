# LabEquipmentLoanSystem
 
1. Get Project 
  - ```git clone https://github.com/SirisakUnknowss/LabEquipmentLoanSystem.git```
  - ``` cd Arkarus ```


2. Start web service
  ``` docker-compose up -d ```
  
3. Stop web service
    ``` docker-compose stop ```

4. Run Migrations
  - ``` docker-compose exec web sh -c "python manage.py makemigrations --noinput" ```
  - ``` docker-compose exec web sh -c "python manage.py migrate --noinput" ```
5. Create superuser
  - ``` docker-compose exec web sh -c "python manage.py createsuperuser --noinput" ```
6. go to http://localhost:8000

#Create New App

  - ``` docker-compose exec web sh -c "python manage.py startapp <name:app>" ```
