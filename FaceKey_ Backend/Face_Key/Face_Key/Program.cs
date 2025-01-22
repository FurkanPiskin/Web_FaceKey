using Face_Key.Context;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllersWithViews();

//Register DbContext
builder.Services.AddDbContext<ApplicationDbContext>(options =>{
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection"));
}

);
// Add CORS
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAllOrigins", builder =>
    {
        builder.AllowAnyOrigin()
               .AllowAnyMethod()
               .AllowAnyHeader();
    });
});

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors("AllowAllOrigins");

app.UseAuthorization();

app.MapControllers();

app.MapControllerRoute
(
    name:"default",
    pattern:"{controller=Students}/{action=Index}/{id?}"
);
using (var scope = app.Services.CreateScope())
{
    var context = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    ResetFaceRecords(context);
}

app.Run();
void ResetFaceRecords(ApplicationDbContext context)
{
    // FaceRecord tablosundaki tüm kayýtlarý al
    var records = context.FacesRecord.ToList();

    // Her bir kaydýn FaceName alanýný "Server is not running" olarak ayarla
    foreach (var record in records)
    {
        record.FaceName = "Server is not running";
    }

    // Deðiþiklikleri kaydet
    context.SaveChanges();

    Console.WriteLine("FaceRecord tablosu sýfýrlandý: FaceName = 'Server is not running'.");
}
