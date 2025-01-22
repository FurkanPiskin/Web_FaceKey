using Face_Key.Context;
using Face_Key.Models.Dto;
using Face_Key.Models.Entity;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System;


namespace Face_Key.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class FacesController : ControllerBase
    {
        private readonly ApplicationDbContext _context;
        public FacesController(ApplicationDbContext context)
        {
            _context = context;
        }
        [HttpGet]
        public async Task<IActionResult> GetFaces()
        {
            var faces = await _context.Faces.ToListAsync();
            return Ok(faces);// JSON formatında tüm kayıtları döndürür
        }
        [HttpPost]
        public async Task<IActionResult> CreateFace([FromBody] FaceDto faceDto)
        {
            if (faceDto == null || string.IsNullOrWhiteSpace(faceDto.Image))
            {
                return BadRequest("Geçersiz görüntü verisi.");
            }

            byte[] imageBytes;
            try
            {
                // Eğer Base64 string'inde bir 'data:image' başlığı varsa, onu ayıklayın
                string base64Data = faceDto.Image.Contains(",")
                    ? faceDto.Image.Split(',')[1] // Base64 kısmını al
                    : faceDto.Image;

                // Base64 string'i byte[]'a dönüştür
                imageBytes = Convert.FromBase64String(base64Data);
            }
            catch (FormatException)
            {
                return BadRequest("Base64 formatı hatalı.");
            }

            // Face nesnesini oluştur
            var face = new Face
            {
                Image = imageBytes, // byte[] verisini buraya gönderiyoruz
                DetectedFaces = faceDto.DetectedFaces,
                CreatedAt = DateTime.UtcNow,
            };

            // Veritabanına kaydet
            await _context.Faces.AddAsync(face);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetFaces), new { id = face.Id }, face);
        }

        [HttpGet("get-latest-face")]
        public IActionResult GetLatestFace()
        {
           var latestRecord=_context.FacesRecord.FirstOrDefault();

            if(latestRecord == null)
            {
                return NotFound("Hiçbir yüz kaydı bulumadı");
            }
            return Ok(latestRecord);
        }
        [HttpPost("save-face-recognation")]
        public IActionResult SaveFaceRecognition([FromBody] FaceRecord faceRecord)
        {
            if (faceRecord == null || string.IsNullOrEmpty(faceRecord.FaceName))
            {
                return BadRequest("Geçersiz veriler gönderildi.");
            }

            // _context üzerinden FaceRecords tablosuna erişiyoruz
            var existingRecord = _context.FacesRecord.FirstOrDefault();

            if (existingRecord != null)
            {
                // Kayıt varsa güncelle
                existingRecord.FaceName = faceRecord.FaceName;
                existingRecord.RecognizedAt = DateTime.UtcNow;

                _context.FacesRecord.Update(existingRecord);
            }
            else
            {
                // Kayıt yoksa yeni kayıt oluştur
                var newRecord = new FaceRecord
                {
                    FaceName = faceRecord.FaceName,
                    RecognizedAt = DateTime.UtcNow
                };

                _context.FacesRecord.Add(newRecord);
            }

            // Değişiklikleri kaydet
            _context.SaveChanges();

            return Ok("Kayıt başarıyla güncellendi.");
        }

        [HttpPost("Save-Camera-Frame")]
        public async Task<IActionResult> SaveCameraFrame([FromBody] CameraFrameDto frame)
        {
            if (frame == null || string.IsNullOrWhiteSpace(frame.Frame))
            {
                return BadRequest(new { message = "Geçersiz görüntü verisi." });
            }

            byte[] imageBytes;
            try
            {
                string base64Data = frame.Frame.Contains(",")
                    ? frame.Frame.Split(',')[1] // Base64 kısmını al
                    : frame.Frame;

                imageBytes = Convert.FromBase64String(base64Data);
            }
            catch (FormatException)
            {
                return BadRequest(new { message = "Base64 formatı hatalı." });
            }

            try
            {
                var existingFrame = await _context.CameraFrames.FirstOrDefaultAsync();

                if (existingFrame != null)
                {
                    existingFrame.Frame = imageBytes;
                    _context.CameraFrames.Update(existingFrame);
                }
                else
                {
                    var cameraFrame = new CameraFrame
                    {
                        Frame = imageBytes
                    };

                    await _context.CameraFrames.AddAsync(cameraFrame);
                }

                await _context.SaveChangesAsync();
                return Ok(new { message = "Kayıt başarıyla kaydedildi veya güncellendi." });
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { message = "Bir hata oluştu", error = ex.Message });
            }
        }


        [HttpGet("Camera-Frame")]
        public async Task<IActionResult> GetCameraFrame()
        {
            var cameraFrames = await _context.CameraFrames.ToListAsync();
            return Ok(cameraFrames); // JSON formatında tüm kayıtları döndürür
        }
        [HttpDelete("Delete-All-Camera-Frames")]
        public async Task<IActionResult> DeleteAllCameraFrames()
        {
            try
            {
                // Tüm kayıtları alın
                var allCameraFrames = await _context.CameraFrames.ToListAsync();

                // Eğer kayıt yoksa, kullanıcıyı bilgilendirin
                if (!allCameraFrames.Any())
                {
                    return NotFound("Veritabanında silinecek kayıt bulunamadı.");
                }

                // Tüm kayıtları kaldır
                _context.CameraFrames.RemoveRange(allCameraFrames);

                // Değişiklikleri kaydet
                await _context.SaveChangesAsync();

                return Ok("Tüm kayıtlar başarıyla silindi.");
            }
            catch (Exception ex)
            {
                // Hata durumunda 500 döndür
                return StatusCode(500, $"Bir hata oluştu: {ex.Message}");
            }
        }






        [HttpDelete]
        public async Task<IActionResult> DeleteAllFace()
        {
            var allFaces=await _context.Faces.ToListAsync();
            if (allFaces.Count == 0)
            {
                return NotFound("No faces found to delete");
            }
            _context.Faces.RemoveRange(allFaces);
            await _context.SaveChangesAsync();
            return Ok("All faces have been deleted succesfully");
        }

       
    }


}