# Запуск приложения через Docker
docker build -t stocks_products .

docker run -d `
   -p 8000:8000 `
   --name stocks-container `
   stocks_products