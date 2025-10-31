using Api.Endpoints.Assignments.DataAnnotations;
using Api.Entities;
using Application.Infrastructure.Data.Entities;
using Microsoft.AspNetCore.Mvc;

namespace Api.Endpoints.Assignments;

public partial class AssignmentsController
{
    [HttpGet("{assignmentId:guid}")]
    public async Task<IActionResult> GetAssignment(Guid assignmentId)
    {
        var assignment = await _baseRepository.GetAssignmentAsync(assignmentId);

        if (assignment is null || assignment.Status == AssigmentStatus.Declined)
            return Errors.AssignmentWithThisIdNotExists;

        if (assignment.Status == AssigmentStatus.InProcess)
        {
            return Errors.AssignmentWithThisIdIsNotReady;
        }
        
        return Ok(new AssignmentResponseObject()
        {
            Id = assignment.Id,
            Summary = assignment.Summary!
        });
    }
}