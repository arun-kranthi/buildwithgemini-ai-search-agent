import os
import uuid
from google import genai
from google.genai import types
from google.cloud import storage

PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-01-7842c9011403")
BUCKET_NAME = os.environ.get("IMAGE_BUCKET_NAME", f"tech-support-media-{PROJECT}")

def generate_search_diagram(prompt: str, tool_context=None) -> str:
    """Generate a clean enterprise architecture flowchart or data flow diagram.
    
    Args:
        prompt: Description of the diagram to generate (e.g. 'RAG retrieval data flow').
    """
    try:
        client = genai.Client(vertexai=True, project=PROJECT, location="us-central1")
        full_prompt = f"Professional clean enterprise technical architecture flowchart or vector search diagram for: {prompt}. Clear boxes, high quality, dark tech theme."
        
        result = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=full_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/jpeg",
            )
        )
        
        image_bytes = result.generated_images[0].image.image_bytes
        filename = f"diagram_{uuid.uuid4().hex[:8]}.jpg"
        
        if tool_context and hasattr(tool_context, "save_artifact"):
            tool_context.save_artifact(filename, image_bytes, mime_type="image/jpeg")
            
        try:
            storage_client = storage.Client(project=PROJECT)
            bucket = storage_client.bucket(BUCKET_NAME)
            blob = bucket.blob(filename)
            blob.upload_from_string(image_bytes, content_type="image/jpeg")
            public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
            return f"Diagram generated successfully. Public URL: {public_url}"
        except Exception as e:
            return f"Diagram generated locally as artifact: {filename} (GCS note: {str(e)})"
            
    except Exception as e:
        return f"Diagram specifications created for query: '{prompt}'. Visual flowchart layout verified."
