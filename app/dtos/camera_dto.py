from marshmallow import Schema, fields, validate
from datetime import datetime

class CameraDTO(Schema):
    id = fields.Str(required=True)
    location = fields.Str(required=True)
    status = fields.Str(validate=validate.OneOf(['active', 'deactive']), required=True)
    res_width = fields.Int(required=True, validate=validate.Range(min=1))
    res_height = fields.Int(required=True, validate=validate.Range(min=1))
    fps = fields.Int(required=True, validate=validate.Range(min=1))
    rtsp_url = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        ordered = True

# Create schema instances for single and multiple cameras
camera_dto = CameraDTO()
cameras_dto = CameraDTO(many=True)
