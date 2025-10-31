using System.ComponentModel.DataAnnotations;

namespace Application.Infrastructure.Data.Entities;

public enum AssigmentStatus
{
    Declined = -1,
    InProcess = 0,
    Completed = 1
}

public class Assignment
{
    [Key] public Guid Id { get; set; }
    [Required] public required ulong TelegramId { get; set; }
    public AssigmentStatus Status { get; set; } = AssigmentStatus.InProcess;

    public string? ShortSummary { get; set; }
    public string? Summary {  get; set; }

}