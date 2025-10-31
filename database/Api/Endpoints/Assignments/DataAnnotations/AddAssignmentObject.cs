using System.ComponentModel.DataAnnotations;

namespace Api.Endpoints.Assignments.DataAnnotations;

public class AddAssignmentObject
{
    [Required] public required ulong TelegramId { get; set; }
}