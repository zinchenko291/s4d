using Api.Endpoints.Assignments.DataAnnotations;
using Api.Entities;
using Application.Infrastructure.Data.Entities;
using Microsoft.AspNetCore.Mvc;

namespace Api.Endpoints.Assignments;

public partial class AssignmentsController
{
    [HttpPost("{assignmentId:guid}")]
    public async Task<IActionResult> UpdateAssignment(Guid assignmentId, [FromBody] UpdateAssignmentObject request)
    {
        var assignment = await _baseRepository.GetAssignmentAsync(assignmentId);

        if (assignment is null)
            return Errors.AssignmentWithThisIdNotExists;
        
        if (request.Status is not null)
            assignment.Status = request.Status.Value;
        
        if (request.ShortSummary is not null)
        {
            assignment.ShortSummary = request.ShortSummary;
        }
        if (request.Summary is not null)
            assignment.Summary = request.Summary;

        await _baseRepository.SaveChangesAsync();
        
        return new OkObjectResult(new
        {
            TelegramId = assignment.TelegramId
        });
    }
}