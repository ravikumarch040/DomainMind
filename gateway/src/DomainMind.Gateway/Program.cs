using DomainMind.Gateway;
using DomainMind.Gateway.Data;
using DomainMind.Gateway.Middleware;
using DomainMind.Gateway.Services;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using OpenTelemetry.Resources;
using OpenTelemetry.Trace;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.Configure<GatewayOptions>(builder.Configuration.GetSection("Gateway"));
builder.Services.AddHttpClient<IVllmProxyService, VllmProxyService>();
builder.Services.AddScoped<IRequestLogService, RequestLogService>();
builder.Services.AddScoped<ITenantContext, TenantContext>();
builder.Services.AddSingleton<IRateLimitService, RedisRateLimitService>();

var conn = builder.Configuration.GetConnectionString("Default")
    ?? "Host=localhost;Database=domainmind;Username=domainmind;Password=domainmind";
builder.Services.AddDbContext<GatewayDbContext>(o => o.UseNpgsql(conn));

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Cognito:Authority"];
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateAudience = false,
            ValidateIssuer = !string.IsNullOrEmpty(builder.Configuration["Cognito:Authority"]),
        };
        if (builder.Environment.IsDevelopment())
        {
            options.TokenValidationParameters.ValidateIssuer = false;
            options.TokenValidationParameters.ValidateLifetime = false;
            options.TokenValidationParameters.SignatureValidator = (_, _) => new System.IdentityModel.Tokens.Jwt.JwtSecurityToken();
        }
    });
builder.Services.AddAuthorization();

builder.Services.AddOpenTelemetry()
    .ConfigureResource(r => r.AddService("domainmind-gateway"))
    .WithTracing(t => t.AddAspNetCoreInstrumentation().AddConsoleExporter());

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseMiddleware<RequestLoggingMiddleware>();
app.UseAuthentication();
app.UseAuthorization();
app.UseMiddleware<TenantMiddleware>();
app.UseMiddleware<RbacMiddleware>();
app.UseMiddleware<RateLimitMiddleware>();

app.MapControllers();
app.MapGet("/health", () => Results.Ok(new { status = "ok" }));

using (var scope = app.Services.CreateScope())
{
    try
    {
        scope.ServiceProvider.GetRequiredService<GatewayDbContext>().Database.EnsureCreated();
    }
    catch { /* DB may not be up in local dev */ }
}

app.Run();

public partial class Program { }
