using Api.Endpoints.Assignments.DataAnnotations;
using Api.Entities;
using Application.Infrastructure.Data.Entities;
using Microsoft.AspNetCore.Mvc;

namespace Api.Endpoints.Assignments;

public partial class AssignmentsController
{
    [HttpPost("register")]
    public async Task<IActionResult> AddAssignment([FromBody] AddAssignmentObject request)
    {
        var id = await _baseRepository.AddAssignmentAsync(new Assignment
        {
            Id = Guid.NewGuid(),
            TelegramId = request.TelegramId,
            Status = AssigmentStatus.InProcess
        }, saveChanges: true);
        
        return new OkObjectResult(new AddAssignmentResponseObject()
        {
            Id = id
        });
    }
}