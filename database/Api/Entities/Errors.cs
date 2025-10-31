using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;

namespace Api.Entities;

public static class Errors
{
    
    public static readonly ObjectResult AssignmentWithThisIdNotExists = new(new
    {
        Status = "error",
        Message = "Assignment with this id does not exist"
    })
    {
        StatusCode = StatusCodes.Status409Conflict
    };
    
    public static readonly ObjectResult AssignmentWithThisIdIsNotReady = new(new
    {
        Status = "error",
        Message = "Assignment with this id is not ready."
    })
    {
        StatusCode = StatusCodes.Status405MethodNotAllowed
    };
}