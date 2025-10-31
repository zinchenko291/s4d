using Application.Infrastructure.Data.Entities;
using Microsoft.EntityFrameworkCore;

namespace Application.Infrastructure.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options) { }
    
    public DbSet<Assignment> Assignments { get; set; }
}