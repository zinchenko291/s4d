# Этап 1: базовый runtime-образ (ASP.NET Core)
FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

# Этап 2: билд и публикация
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src

# Копируем проекты отдельно для кеширования restore
COPY ["Api/Api.csproj", "Api/"]
COPY ["Application/Application.csproj", "Application/"]

# Восстанавливаем зависимости
RUN dotnet restore "Api/Api.csproj"

# Копируем остальной код
COPY . .

# Собираем проект
WORKDIR "/src/Api"
RUN dotnet build "Api.csproj" -c $BUILD_CONFIGURATION -o /app/build

# Публикуем
FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "Api.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

# Этап 3: финальный образ
FROM base AS final
WORKDIR /app

# Копируем результат публикации
COPY --from=publish /app/publish .

# Точка входа
ENTRYPOINT ["dotnet", "Api.dll"]
