using System.ComponentModel.DataAnnotations;

namespace Face_Key.Models.Entity
{
    public class Face
    {
        [Key]
        public int Id { get; set; }

        // PostgreSQL'deki BYTEA ile uyumlu bir özellik
        public byte[] Image { get; set; }  // Base64 formatında 
        public int DetectedFaces { get; set; }
        public DateTime CreatedAt { get; set; }
    }
}
