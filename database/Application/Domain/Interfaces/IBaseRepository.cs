using Application.Infrastructure.Data.Entities;
using Ardalis.Result;

namespace Application.Domain.Interfaces;

public interface IBaseRepository
{
    Task<Assignment?> GetAssignmentAsync(Guid assignmentId);
    Task<Guid> AddAssignmentAsync(Assignment assignmentId, bool saveChanges = true);

    Task SaveChangesAsync();
}