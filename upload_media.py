import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="dsrkmqz5u",
    api_key="",
    api_secret=""
)

MEDIA_ROOT = "media"

for root, dirs, files in os.walk(MEDIA_ROOT):
    for file in files:

        file_path = os.path.join(root, file)

        # remove "media/" and convert Windows "\" → "/"
        public_id = os.path.relpath(file_path, MEDIA_ROOT).replace("\\", "/")

        # remove extension (.jpg, .png etc)
        public_id = os.path.splitext(public_id)[0]

        print("Uploading:", public_id)

        cloudinary.uploader.upload(
            file_path,
            public_id=public_id,
            overwrite=True
        )


print("Upload complete")
