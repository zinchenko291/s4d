using Application.Infrastructure.Data.Entities;

namespace Api.Endpoints.Assignments.DataAnnotations;

public class UpdateAssignmentObject
{
    public AssigmentStatus? Status { get; set; }
    public string? ShortSummary { get; set; }
    public string? Summary {  get; set; }

}