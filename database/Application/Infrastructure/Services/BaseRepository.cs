using Application.Domain.Interfaces;
using Application.Infrastructure.Data;
using Application.Infrastructure.Data.Entities;
using Ardalis.Result;
using Microsoft.EntityFrameworkCore;

namespace Application.Infrastructure.Services;

public class BaseRepository : IBaseRepository
{
    ApplicationDbContext _context;
    
    public BaseRepository(ApplicationDbContext dbContext)
    {
        _context = dbContext;
    }

    public async Task<Assignment?> GetAssignmentAsync(Guid assignmentId)
    {
        return await _context.Assignments.FirstOrDefaultAsync(x => x.Id == assignmentId);
    }
    
    public async Task<Guid> AddAssignmentAsync(Assignment assignment, bool saveChanges = true)
    {
        await _context.Assignments.AddAsync(assignment);
        
        if (saveChanges)
            await _context.SaveChangesAsync();
        
        return assignment.Id;
    }

    public async Task SaveChangesAsync()
    {
        await _context.SaveChangesAsync();
    }

    // public async Task<Result> UpdateUserAsync(User user)
    // {
    //     _context.Users.Update(user);
    //     await  _context.SaveChangesAsync();
    //     return Result.Success();
    // }
    //
    // public async Task<Result> AddUserAsync(User user)
    // {
    //     var result = await _context.Users.Upsert(user)
    //         .On(u => u.Id)
    //         .WhenMatched((existing, incoming) => existing) // ничего не делаем, если есть
    //         .RunAsync();
    //     
    //     if (result <= 0) return Result.Conflict();
    //     
    //     return Result.Success();
    // }
}