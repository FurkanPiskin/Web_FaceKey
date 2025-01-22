using Face_Key.Models.Dto;
using Face_Key.Models.Entity;
using Microsoft.EntityFrameworkCore;

namespace Face_Key.Context
{
    public class ApplicationDbContext:DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
        { 
           
        }
        public DbSet<Face> Faces { get; set; }
        public DbSet<FaceRecord> FacesRecord { get; set; }
        public DbSet<CameraFrame> CameraFrames { get; set; }

    }
}
