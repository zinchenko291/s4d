using Application.Domain.Interfaces;
using Application.Infrastructure.Data;
using Application.Infrastructure.Services;
using Microsoft.EntityFrameworkCore;
using Scalar.AspNetCore;

var builder = WebApplication.CreateBuilder(args);

// var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
var connectionString = Environment.GetEnvironmentVariable("FULL_DB_CONNECTION_STRING");
builder.Services.AddDbContext<ApplicationDbContext>(options => options.UseNpgsql(connectionString));

builder.Services.AddScoped<IBaseRepository, BaseRepository>();

builder.Services.AddControllers();
builder.Services.AddOpenApi();

builder.WebHost.ConfigureKestrel(options =>
{
    options.ListenAnyIP(int.Parse(Environment.GetEnvironmentVariable("HTTP_PORT"))); // HTTP
    // options.ListenAnyIP(8443, o => o.UseHttps()); // HTTPS при необходимости
});

var app = builder.Build();
app.MapControllers();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.MapScalarApiReference();
}

app.Run();