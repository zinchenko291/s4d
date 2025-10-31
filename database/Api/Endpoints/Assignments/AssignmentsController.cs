using Application.Domain.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace Api.Endpoints.Assignments;

[ApiController]
[Route("api/v1/[controller]")]
public partial class AssignmentsController: ControllerBase
{
    private readonly IBaseRepository _baseRepository;

    public AssignmentsController(IBaseRepository baseRepository)
    {
        _baseRepository = baseRepository;
    }
}