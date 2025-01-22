using System.Data;

namespace Face_Key.Models.Entity
{
    public class FaceRecord
    {
        public int Id { get; set; }
        public string FaceName { get; set; }
        public DateTime RecognizedAt { get; set; }
    }
    public static class FaceMemory
    {
        private static readonly List<FaceRecord> Faces = new List<FaceRecord>();

        public static void AddFace(FaceRecord face)
        {
            Faces.Add(face);
        }

        public static FaceRecord GetLatestFace()
        {
            return Faces.OrderByDescending(f => f.RecognizedAt).FirstOrDefault();
        }
    }
}
