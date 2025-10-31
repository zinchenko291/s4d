using System.ComponentModel.DataAnnotations;

namespace Api.Endpoints.Assignments.DataAnnotations;

public class AssignmentResponseObject
{
    [Required] public Guid Id { get; set; }
    [Required] public required string Summary { get; set; }
}