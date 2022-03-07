# LabEquipmentLoanSystem
 
Get Project
git clone https://github.com/SirisakUnknowss/LabEquipmentLoanSystem.git
cd Arkarus

docker-compose up -d
Stop web service docker-compose stop

See Setup Postgres

Start web service docker-compose up -d

Run Migrations

docker-compose exec web sh -c "python manage.py makemigrations --noinput"
docker-compose exec web sh -c "python manage.py migrate --noinput"
Create superuser
docker-compose exec web sh -c "python manage.py createsuperuser --noinput"
go to http://localhost:8000

#Create New App

docker-compose exec web sh -c "python manage.py startapp <name:app>"
