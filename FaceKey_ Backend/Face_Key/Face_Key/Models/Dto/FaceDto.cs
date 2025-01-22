namespace Face_Key.Models.Dto
{
    public class FaceDto
    {
        public string Image { get; set; }
        public int DetectedFaces { get; set; }

        public string? FaceName { get; set; }    
        public DateTime CreatedAt { get; set; }
    }
}
